"""
GitHub API data layer.

Fetches public profile, repositories, commit counts, and calculates
lines of code. Caches results to disk for deterministic regeneration.
"""

import json
import os
import sys
import time
from datetime import date
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import urllib.request
import urllib.error
import urllib.parse

from scripts.config import (
    GITHUB_USERNAME, GITHUB_API_BASE, GITHUB_TOKEN,
    CACHE_PROFILE, CACHE_REPOS, CACHE_STATS, CACHE_DIR,
    SKIP_REPOS, MAX_PROJECTS, MAX_DESC_LENGTH, DATE_OF_BIRTH,
)


def _headers() -> dict:
    """Build request headers, including auth token if available."""
    h = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "GitHub-Readme-Stats",
    }
    if GITHUB_TOKEN:
        h["Authorization"] = f"token {GITHUB_TOKEN}"
    return h


def _get(url: str, params: dict | None = None) -> Any:
    """GET with retry and rate-limit awareness."""
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers=_headers())
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 403:
                reset = e.headers.get("X-RateLimit-Reset")
                wait = (int(reset) - int(time.time())) if reset else 60
                print(f"  Rate limited, waiting {max(wait, 1)}s...")
                time.sleep(max(wait, 1))
                continue
            if attempt == 2:
                print(f"  Warning: API request failed: {e}")
                return None
            time.sleep(2 ** attempt)
        except Exception as e:
            if attempt == 2:
                print(f"  Warning: API request failed: {e}")
                return None
            time.sleep(2 ** attempt)
    return None


def _paginate(url: str, params: dict | None = None) -> list:
    """Fetch all pages from a paginated GitHub API endpoint."""
    results = []
    params = dict(params or {})
    params.setdefault("per_page", "100")
    page = 1
    while True:
        params["page"] = str(page)
        data = _get(url, params)
        if not data or not isinstance(data, list):
            break
        results.extend(data)
        if len(data) < 100:
            break
        page += 1
    return results


def _save_cache(path: str, data: Any) -> None:
    """Write data to cache file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, sort_keys=True)


def _load_cache(path: str) -> Any:
    """Load data from cache file if it exists."""
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None


def fetch_profile() -> dict:
    """Fetch user profile data."""
    print("Fetching profile...")
    data = _get(f"{GITHUB_API_BASE}/users/{GITHUB_USERNAME}")
    if data:
        profile = {
            "login": data.get("login", GITHUB_USERNAME),
            "name": data.get("name", ""),
            "public_repos": data.get("public_repos", 0),
            "followers": data.get("followers", 0),
            "following": data.get("following", 0),
            "created_at": data.get("created_at", ""),
        }
        _save_cache(CACHE_PROFILE, profile)
        return profile
    cached = _load_cache(CACHE_PROFILE)
    return cached or {"login": GITHUB_USERNAME, "public_repos": 0, "followers": 0, "following": 0}


def fetch_repositories() -> list[dict]:
    """Fetch all public repositories with relevant metadata."""
    print("Fetching repositories...")
    repos = _paginate(
        f"{GITHUB_API_BASE}/users/{GITHUB_USERNAME}/repos",
        {"type": "owner", "sort": "updated"}
    )

    processed = []
    for r in repos:
        if r.get("fork"):
            continue
        name = r.get("name", "")
        if name in SKIP_REPOS:
            continue

        processed.append({
            "name": name,
            "description": r.get("description") or "",
            "language": r.get("language") or "",
            "stars": r.get("stargazers_count", 0),
            "forks": r.get("forks_count", 0),
            "url": r.get("html_url", ""),
            "size": r.get("size", 0),
            "archived": r.get("archived", False),
            "updated_at": r.get("updated_at", ""),
            "created_at": r.get("created_at", ""),
        })

    # Sort: by update time descending (most recently updated first)
    processed.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
    _save_cache(CACHE_REPOS, processed)
    return processed


def _count_commits_for_repo(repo_name: str) -> int:
    """Count commits in a repo's default branch by the user."""
    commits = _paginate(
        f"{GITHUB_API_BASE}/repos/{GITHUB_USERNAME}/{repo_name}/commits",
        {"author": GITHUB_USERNAME}
    )
    return len(commits) if isinstance(commits, list) else 0


def calculate_statistics(profile: dict, repos: list[dict], use_cache: bool = True) -> dict:
    """Calculate aggregate GitHub statistics.

    If use_cache is True and cached stats exist, uses cached LOC data
    and only refreshes commit counts (which are fast).
    """
    print("Calculating statistics...")

    # Check for cached stats
    cached = _load_cache(CACHE_STATS) if use_cache else None

    total_stars = sum(r.get("stars", 0) for r in repos)
    total_repos = profile.get("public_repos", len(repos))
    followers = profile.get("followers", 0)

    # Count commits across all repos
    total_commits = 0
    for repo in repos:
        name = repo["name"]
        print(f"  Counting commits for {name}...")
        count = _count_commits_for_repo(name)
        total_commits += count

    # LOC stats: use cache if available, otherwise try API with short timeout
    total_additions = 0
    total_deletions = 0

    if cached and cached.get("additions", 0) > 0:
        # Use cached LOC data (it doesn't change much day-to-day)
        total_additions = cached.get("additions", 0)
        total_deletions = cached.get("deletions", 0)
        print(f"  Using cached LOC: +{total_additions} / -{total_deletions}")
    else:
        # Fetch fresh LOC stats with short timeout
        for repo in repos:
            name = repo["name"]
            print(f"  Fetching LOC for {name}...")
            try:
                resp = requests.get(
                    f"{GITHUB_API_BASE}/repos/{GITHUB_USERNAME}/{name}/stats/contributors",
                    headers=_headers(),
                    timeout=10,  # short timeout — this endpoint is notoriously slow
                )
                if resp.status_code == 200:
                    stats = resp.json()
                    if isinstance(stats, list):
                        for contributor in stats:
                            if isinstance(contributor, dict):
                                author = contributor.get("author", {})
                                if isinstance(author, dict) and author.get("login", "").lower() == GITHUB_USERNAME.lower():
                                    for week in contributor.get("weeks", []):
                                        total_additions += week.get("a", 0)
                                        total_deletions += week.get("d", 0)
                elif resp.status_code == 202:
                    print(f"    Stats computing for {name}, skipping...")
                    continue
            except Exception as e:
                print(f"    Warning: {e}")
                continue

    contributed_repos = 0

    statistics = {
        "repos": total_repos,
        "contributed_repos": contributed_repos,
        "stars": total_stars,
        "commits": total_commits,
        "followers": followers,
        "additions": total_additions,
        "deletions": total_deletions,
        "total_loc": total_additions - total_deletions,
    }

    _save_cache(CACHE_STATS, statistics)
    return statistics


def select_projects(repos: list[dict]) -> list[dict]:
    """Select the best projects to display dynamically from GitHub repos."""
    candidates = [
        r for r in repos
        if not r.get("archived")
        and r.get("name") not in SKIP_REPOS
    ]

    for r in candidates:
        has_desc = 3.0 if r.get("description") else 0.0
        stars = r.get("stars", 0) * 5.0
        forks = r.get("forks", 0) * 3.0
        # Give bonus to flagship projects mentioned in user identity
        name_lower = r.get("name", "").lower()
        flagship_bonus = 0.0
        if any(k in name_lower for k in ["relict", "magcomm", "nyx", "finora", "zypher", "anchor"]):
            flagship_bonus = 10.0

        r["_score"] = stars + forks + has_desc + flagship_bonus

    # Sort by score descending, then by updated_at descending, then by name for determinism
    candidates.sort(key=lambda x: (-x["_score"], x.get("updated_at", ""), x["name"]))
    return candidates[:MAX_PROJECTS]


def calculate_uptime() -> str:
    """Calculate age from DOB as 'X years, Y months, Z days'."""
    today = date.today()
    dob = DATE_OF_BIRTH

    years = today.year - dob.year
    months = today.month - dob.month
    days = today.day - dob.day

    if days < 0:
        months -= 1
        # Days in the previous month
        prev_month = today.month - 1 if today.month > 1 else 12
        prev_year = today.year if today.month > 1 else today.year - 1
        import calendar
        days += calendar.monthrange(prev_year, prev_month)[1]

    if months < 0:
        years -= 1
        months += 12

    return f"{years} years, {months} months, {days} days"


def format_number(n: int) -> str:
    """Format number with commas: 12345 → '12,345'."""
    return f"{n:,}"


if __name__ == "__main__":
    print(f"Uptime: {calculate_uptime()}")
    profile = fetch_profile()
    print(f"Profile: {profile}")
    repos = fetch_repositories()
    print(f"Repos: {len(repos)}")
    projects = select_projects(repos)
    for p in projects:
        print(f"  {p['name']}: {p['description'][:50]}")
    stats = calculate_statistics(profile, repos)
    print(f"Stats: {stats}")

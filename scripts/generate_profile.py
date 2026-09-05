#!/usr/bin/env python3
"""
Main orchestrator for the GitHub profile README generator.

Runs the full pipeline:
1. Generate ASCII portrait from source photo
2. Fetch GitHub data (profile, repos, stats)
3. Select best projects
4. Calculate dynamic uptime
5. Render dark and light SVGs
6. Validate output

Usage:
    python scripts/generate_profile.py             # full run (API calls)
    python scripts/generate_profile.py --cached     # use cached data (fast)
"""

import json
import os
import sys
import xml.etree.ElementTree as ET

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.config import (
    DARK_SVG, LIGHT_SVG, SOURCE_PHOTO,
    CACHE_PROFILE, CACHE_REPOS, CACHE_STATS,
)
from scripts.ascii_art import generate_ascii, ascii_to_string
from scripts.github_stats import (
    fetch_profile, fetch_repositories, calculate_statistics,
    select_projects, calculate_uptime,
)
from scripts.svg_renderer import render_svg, save_svg


def _load_json(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None


def validate_svg(path: str) -> bool:
    """Validate that the file is well-formed XML/SVG."""
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        if "svg" not in root.tag.lower():
            print(f"  WARNING: Root element is not <svg>: {root.tag}")
            return False
        print(f"  Valid SVG: {path}")
        return True
    except ET.ParseError as e:
        print(f"  ERROR: Invalid XML in {path}: {e}")
        return False


def main():
    use_cached = "--cached" in sys.argv

    print("=" * 60)
    print("GitHub Profile README Generator")
    print(f"  Mode: {'CACHED (fast)' if use_cached else 'FULL (API calls)'}")
    print("=" * 60)

    # Step 1: ASCII Portrait
    print("\n[1/6] Generating ASCII portrait...")
    if not os.path.exists(SOURCE_PHOTO):
        print(f"  ERROR: Source photo not found: {SOURCE_PHOTO}")
        sys.exit(1)

    ascii_lines = generate_ascii()
    print(f"  Generated: {len(ascii_lines)} lines, max width {max(len(l) for l in ascii_lines)} chars")
    print("\n  Preview:")
    for line in ascii_lines[:10]:
        print(f"  {line}")
    print("  ...")

    # Step 2: Uptime
    print("\n[2/6] Calculating uptime...")
    uptime = calculate_uptime()
    print(f"  Uptime: {uptime}")

    if use_cached:
        # Use cached data for fast visual iteration
        print("\n[3/6] Loading cached GitHub data...")
        profile = _load_json(CACHE_PROFILE) or {"login": "mohith-krishna-mahesh", "public_repos": 9, "followers": 5}
        repos = _load_json(CACHE_REPOS) or []
        print(f"  Profile: {profile.get('login')} | Repos: {len(repos)}")

        print("\n[4/6] Loading cached statistics...")
        stats = _load_json(CACHE_STATS) or {
            "repos": 9, "contributed_repos": 0, "stars": 0,
            "commits": 26, "followers": 5,
            "additions": 43765, "deletions": 5575, "total_loc": 38190,
        }
        print(f"  Commits: {stats.get('commits', 0)}")
        print(f"  LOC: +{stats.get('additions', 0)} / -{stats.get('deletions', 0)}")
    else:
        # Full API fetch
        print("\n[3/6] Fetching GitHub data...")
        profile = fetch_profile()
        repos = fetch_repositories()
        print(f"  Profile: {profile.get('login')} | Repos: {len(repos)}")

        print("\n[4/6] Calculating statistics...")
        stats = calculate_statistics(profile, repos)
        print(f"  Commits: {stats.get('commits', 0)}")
        print(f"  Stars: {stats.get('stars', 0)}")
        print(f"  LOC: +{stats.get('additions', 0)} / -{stats.get('deletions', 0)}")

    # Step 5: Projects
    print("\n[5/6] Selecting projects...")
    projects = select_projects(repos)
    for p in projects:
        desc = p.get("description", "")[:40]
        print(f"  • {p['name']} [{p.get('language', '?')}] — {desc}")

    # Step 6: Render SVGs
    print("\n[6/6] Rendering SVGs...")

    dark_ascii = generate_ascii(mode="dark")
    light_ascii = generate_ascii(mode="light")

    dark_svg = render_svg(dark_ascii, stats, projects, mode="dark")
    save_svg(dark_svg, DARK_SVG)

    light_svg = render_svg(light_ascii, stats, projects, mode="light")
    save_svg(light_svg, LIGHT_SVG)

    # Validation
    print("\nValidating...")
    dark_ok = validate_svg(DARK_SVG)
    light_ok = validate_svg(LIGHT_SVG)

    if dark_ok and light_ok:
        print("\n✓ Both SVGs validated successfully.")
    else:
        print("\n✗ Validation errors detected.")
        sys.exit(1)

    # Summary
    print("\n" + "=" * 60)
    print("Generation complete!")
    print(f"  Dark:  {DARK_SVG}")
    print(f"  Light: {LIGHT_SVG}")
    print(f"  ASCII: {len(ascii_lines)} lines")
    print(f"  Stats: {stats}")
    print(f"  Projects: {len(projects)}")
    print("=" * 60)


if __name__ == "__main__":
    main()

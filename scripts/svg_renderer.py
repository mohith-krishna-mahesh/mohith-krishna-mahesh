"""
SVG renderer for the terminal-style GitHub profile dashboard.

Generates self-contained SVG files for dark and light modes matching the reference dimensions (1045x703).
Layout: Compact 44x30 Face ASCII Portrait (left) | High-Legibility Terminal Dashboard (right)
"""

import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.config import (
    FONT_FAMILY, INFO_FONT_SIZE, INFO_LINE_HEIGHT,
    ASCII_FONT_SIZE, ASCII_LINE_HEIGHT, ASCII_X, ASCII_Y,
    INFO_X, INFO_Y, LEADER_FILL, SEPARATOR_WIDTH,
    DARK, LIGHT, PROFILE_FIELDS, CONTACT, CONTACT_URLS,
    SVG_WIDTH, SVG_CORNER_RADIUS,
)
from scripts.github_stats import calculate_uptime, format_number


def _esc(text: str) -> str:
    """Escape text for safe SVG/XML embedding."""
    return html.escape(str(text), quote=True)


def render_svg(
    ascii_lines: list[str],
    statistics: dict,
    projects: list[dict] = None,
    mode: str = "dark",
) -> str:
    """
    Render a complete SVG profile dashboard with reference dimensions (1045px width)
    and high-contrast VS Code Hacker theme typography.
    """
    colors = DARK if mode == "dark" else LIGHT
    uptime = calculate_uptime()
    font_family_svg = FONT_FAMILY.replace('"', "'")

    font_size = INFO_FONT_SIZE
    line_height = INFO_LINE_HEIGHT

    ascii_x = ASCII_X
    ascii_y = ASCII_Y
    ascii_font_size = ASCII_FONT_SIZE
    ascii_line_height = ASCII_LINE_HEIGHT

    info_x = INFO_X
    info_y = INFO_Y
    sep_len = SEPARATOR_WIDTH
    leader_fill = LEADER_FILL

    svg_width = SVG_WIDTH

    body = []

    # CSS Styles
    body.append("<style>")
    body.append(f'  .label {{ fill: {colors["label"]}; font-weight: 500; }}')
    body.append(f'  .value {{ fill: {colors["value"]}; }}')
    body.append(f'  .primary {{ fill: {colors["primary"]}; }}')
    body.append(f'  .secondary {{ fill: {colors["secondary"]}; }}')
    body.append(f'  .header {{ fill: {colors["header"]}; font-weight: bold; }}')
    body.append(f'  .ascii {{ fill: {colors["ascii"]}; letter-spacing: 1.5px; }}')
    body.append(f'  .positive {{ fill: {colors["positive"]}; font-weight: 600; }}')
    body.append(f'  .negative {{ fill: {colors["negative"]}; font-weight: 600; }}')
    body.append(f'  .link {{ fill: {colors["link"]}; font-weight: 500; }}')
    body.append("  text, tspan { white-space: pre; }")
    body.append("  a { text-decoration: none; }")
    body.append("</style>")

    # ─── ASCII Portrait ─────────────────────────────────────────────────────
    ascii_max_len = max((len(l) for l in ascii_lines), default=50)
    ascii_width = ascii_max_len * (ascii_font_size * 0.605)
    ascii_height = len(ascii_lines) * ascii_line_height

    body.append(f'<text x="{ascii_x}" y="{ascii_y}" class="ascii" font-size="{ascii_font_size}px">')
    for i, line in enumerate(ascii_lines):
        y = ascii_y + i * ascii_line_height
        body.append(f'<tspan x="{ascii_x}" y="{y:.1f}">{_esc(line)}</tspan>')
    body.append("</text>")

    # ─── Right Side Info Panel ──────────────────────────────────────────────
    curr_y = info_y

    # Terminal Prompt Header
    header_name = "mohith"
    header_at = "@"
    header_host = "github"
    header_sep = " " + "─" * max(10, sep_len - len("mohith@github") - 1)

    body.append(
        f'<text x="{info_x}" y="{curr_y:.1f}" font-size="{font_size}px">'
        f'<tspan class="header">{_esc(header_name)}</tspan>'
        f'<tspan class="primary">{_esc(header_at)}</tspan>'
        f'<tspan class="header">{_esc(header_host)}</tspan>'
        f'<tspan class="secondary">{_esc(header_sep)}</tspan>'
        f'</text>'
    )
    curr_y += line_height

    # Info Items Definition
    info_items = [
        ("OS", "macOS, Kali Linux, Fedora, Windows 10", []),
        ("Uptime", uptime, []),
        ("Host", "VIT Chennai", []),
        ("Kernel", "B.Tech Computer Science", []),
        ("IDE", "Zed, VSCode", []),
        (None, None, []),  # spacer
        ("Languages.Programming", "Python, C, C++, Java, JS, TS, Bash", []),
        ("Languages.Computer", "HTML, CSS, SQL, JSON, YAML, LaTeX", []),
        ("Languages.Real", "Malayalam, English, Tamil, Hindi", []),
        (None, None, []),  # spacer
        ("Research.Area", "Cryptography", []),
        ("Research.Project", "MOSAIC", []),
        (None, None, []),  # spacer
        ("Interests.Software", "Cybersecurity, Systems, Full-Stack,", ["AI/ML, Blockchain, Game Development"]),
        ("Interests.Hardware", "Communication Systems, Rover Dev", []),
        ("Interests.Events", "CTFs, Hackathons, Game Jams, Robotics", []),
        ("Interests.Science", "Mathematics, Physics, Chemistry, Biology", []),
        ("Interests.Humanities", "Philosophy, History, Art", []),
    ]

    for label, val, wraps in info_items:
        if label is None:
            # Spacer line
            body.append(f'<text x="{info_x}" y="{curr_y:.1f}" font-size="{font_size}px" class="secondary">·</text>')
            curr_y += line_height
            continue

        prefix = f"· {label}: "
        dots_count = max(2, leader_fill - len(prefix))
        dots = "." * dots_count + " "

        body.append(
            f'<text x="{info_x}" y="{curr_y:.1f}" font-size="{font_size}px">'
            f'<tspan class="label">{_esc(prefix)}</tspan>'
            f'<tspan class="secondary">{_esc(dots)}</tspan>'
            f'<tspan class="value">{_esc(val)}</tspan>'
            f'</text>'
        )
        curr_y += line_height

        for wrap_val in wraps:
            wrap_indent = " " * len(prefix + dots)
            body.append(
                f'<text x="{info_x}" y="{curr_y:.1f}" font-size="{font_size}px">'
                f'<tspan class="secondary">·{wrap_indent[1:]}</tspan>'
                f'<tspan class="value">{_esc(wrap_val)}</tspan>'
                f'</text>'
            )
            curr_y += line_height

    # ─── Contact Section ─────────────────────────────────────────────────────
    curr_y += 8
    contact_title = "- Contact "
    contact_rule = "─" * max(10, sep_len - len(contact_title))
    body.append(
        f'<text x="{info_x}" y="{curr_y:.1f}" font-size="{font_size}px">'
        f'<tspan class="header">{_esc(contact_title)}</tspan>'
        f'<tspan class="secondary">{_esc(contact_rule)}</tspan>'
        f'</text>'
    )
    curr_y += line_height

    for key, val in CONTACT.items():
        url = CONTACT_URLS.get(key, "")
        prefix = f"· {key}: "
        dots_count = max(2, leader_fill - len(prefix))
        dots = "." * dots_count + " "

        if url:
            body.append(
                f'<a xlink:href="{_esc(url)}" target="_blank">'
                f'<text x="{info_x}" y="{curr_y:.1f}" font-size="{font_size}px">'
                f'<tspan class="label">{_esc(prefix)}</tspan>'
                f'<tspan class="secondary">{_esc(dots)}</tspan>'
                f'<tspan class="link">{_esc(val)}</tspan>'
                f'</text></a>'
            )
        else:
            body.append(
                f'<text x="{info_x}" y="{curr_y:.1f}" font-size="{font_size}px">'
                f'<tspan class="label">{_esc(prefix)}</tspan>'
                f'<tspan class="secondary">{_esc(dots)}</tspan>'
                f'<tspan class="value">{_esc(val)}</tspan>'
                f'</text>'
            )
        curr_y += line_height

    # ─── GitHub Stats Section ────────────────────────────────────────────────
    curr_y += 8
    stats_title = "- GitHub Stats "
    stats_rule = "─" * max(10, sep_len - len(stats_title))
    body.append(
        f'<text x="{info_x}" y="{curr_y:.1f}" font-size="{font_size}px">'
        f'<tspan class="header">{_esc(stats_title)}</tspan>'
        f'<tspan class="secondary">{_esc(stats_rule)}</tspan>'
        f'</text>'
    )
    curr_y += line_height

    repos = format_number(statistics.get("repos", 9))
    contrib = format_number(statistics.get("contributed_repos", 0))
    stars = format_number(statistics.get("stars", 0))
    commits = format_number(statistics.get("commits", 26))
    followers = format_number(statistics.get("followers", 5))
    additions = format_number(statistics.get("additions", 43765))
    deletions = format_number(statistics.get("deletions", 5575))
    total_loc = format_number(abs(statistics.get("total_loc", 38190)))

    # Line 1: Repos
    repo_prefix = "· Repos: "
    repo_dots = "." * max(2, leader_fill - len(repo_prefix)) + " "
    star_prefix = "Stars: "
    star_dots = "." * 13 + " "
    body.append(
        f'<text x="{info_x}" y="{curr_y:.1f}" font-size="{font_size}px">'
        f'<tspan class="label">{_esc(repo_prefix)}</tspan>'
        f'<tspan class="secondary">{_esc(repo_dots)}</tspan>'
        f'<tspan class="value">{_esc(repos)}</tspan>'
        f'<tspan class="secondary"> {{Contributed: </tspan>'
        f'<tspan class="value">{_esc(contrib)}</tspan>'
        f'<tspan class="secondary">}} | </tspan>'
        f'<tspan class="label">{_esc(star_prefix)}</tspan>'
        f'<tspan class="secondary">{_esc(star_dots)}</tspan>'
        f'<tspan class="value">{_esc(stars)}</tspan>'
        f'</text>'
    )
    curr_y += line_height

    # Line 2: Commits
    commit_prefix = "· Commits: "
    commit_dots = "." * max(2, leader_fill - len(commit_prefix)) + " "
    commits_str = str(commits)
    padding_needed = max(1, 16 - len(commits_str))
    commits_pad = " " * padding_needed
    follower_prefix = "Followers: "
    follower_dots = "." * 9 + " "
    body.append(
        f'<text x="{info_x}" y="{curr_y:.1f}" font-size="{font_size}px">'
        f'<tspan class="label">{_esc(commit_prefix)}</tspan>'
        f'<tspan class="secondary">{_esc(commit_dots)}</tspan>'
        f'<tspan class="value">{_esc(commits_str)}</tspan>'
        f'<tspan class="secondary">{_esc(commits_pad)}| </tspan>'
        f'<tspan class="label">{_esc(follower_prefix)}</tspan>'
        f'<tspan class="secondary">{_esc(follower_dots)}</tspan>'
        f'<tspan class="value">{_esc(followers)}</tspan>'
        f'</text>'
    )
    curr_y += line_height

    # Line 3: LOC
    loc_prefix = "· Lines of Code on GitHub: "
    loc_dots = ".. "
    body.append(
        f'<text x="{info_x}" y="{curr_y:.1f}" font-size="{font_size}px">'
        f'<tspan class="label">{_esc(loc_prefix)}</tspan>'
        f'<tspan class="secondary">{_esc(loc_dots)}</tspan>'
        f'<tspan class="value">{_esc(total_loc)} </tspan>'
        f'<tspan class="secondary">(</tspan>'
        f'<tspan class="positive"> {_esc(additions)}++</tspan>'
        f'<tspan class="secondary">, </tspan>'
        f'<tspan class="negative"> {_esc(deletions)}-- </tspan>'
        f'<tspan class="secondary">)</tspan>'
        f'</text>'
    )
    curr_y += line_height

    final_height = int(max(curr_y + 15, ascii_y + len(ascii_lines) * ascii_line_height + 25))

    # Assemble complete SVG document
    svg = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="0 0 {svg_width} {final_height}" width="{svg_width}px" height="{final_height}px" '
        f'font-family="{font_family_svg}">',
        f'<rect width="{svg_width}px" height="{final_height}px" fill="{colors["background"]}" rx="{SVG_CORNER_RADIUS}"/>'
    ]
    svg.extend(body)
    svg.append("</svg>")

    return "\n".join(svg)


def save_svg(content: str, path: str) -> None:
    """Write SVG content to file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Saved: {path}")

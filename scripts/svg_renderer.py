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
    body.append(f'  .label {{ fill: {colors["label"]}; }}')
    body.append(f'  .value {{ fill: {colors["value"]}; }}')
    body.append(f'  .number {{ fill: {colors["number"]}; }}')
    body.append(f'  .primary {{ fill: {colors["primary"]}; }}')
    body.append(f'  .secondary {{ fill: {colors["secondary"]}; }}')
    body.append(f'  .rule {{ fill: {colors["rule"]}; font-weight: bold; }}')
    body.append(f'  .header {{ fill: {colors["header"]}; font-weight: bold; }}')
    body.append(f'  .prompt-user {{ fill: {colors["prompt_user"]}; font-weight: bold; }}')
    body.append(f'  .prompt-at {{ fill: {colors["prompt_at"]}; font-weight: bold; }}')
    body.append(f'  .prompt-host {{ fill: {colors["prompt_host"]}; font-weight: bold; }}')
    body.append(f'  .ascii {{ fill: {colors["ascii"]}; }}')
    body.append(f'  .positive {{ fill: {colors["positive"]}; }}')
    body.append(f'  .negative {{ fill: {colors["negative"]}; }}')
    body.append(f'  .link {{ fill: {colors["link"]}; }}')
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
    left_rule = "───[ "
    right_rule_prompt = " ]" + "─" * max(4, sep_len - (len(left_rule) + len(header_name + header_at + header_host) + 2))

    body.append(
        f'<text x="{info_x}" y="{curr_y:.1f}" font-size="{font_size}px">'
        f'<tspan class="rule">{_esc(left_rule)}</tspan>'
        f'<tspan class="prompt-user">{_esc(header_name)}</tspan>'
        f'<tspan class="prompt-at">{_esc(header_at)}</tspan>'
        f'<tspan class="prompt-host">{_esc(header_host)}</tspan>'
        f'<tspan class="rule">{_esc(right_rule_prompt)}</tspan>'
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
        ("Interests.Events", "CTFs, Hackathons, Game Jams,", ["Robotics Competitions"]),
        ("Interests.Science", "Mathematics, Physics, Chemistry,", ["Biology"]),
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
    curr_y += 10
    contact_title = "Contact"
    right_rule_contact = " ]" + "─" * max(4, sep_len - (len(left_rule) + len(contact_title) + 2))
    body.append(
        f'<text x="{info_x}" y="{curr_y:.1f}" font-size="{font_size}px">'
        f'<tspan class="rule">{_esc(left_rule)}</tspan>'
        f'<tspan class="header">{_esc(contact_title)}</tspan>'
        f'<tspan class="rule">{_esc(right_rule_contact)}</tspan>'
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
    curr_y += 10
    stats_title = "GitHub Stats"
    right_rule_stats = " ]" + "─" * max(4, sep_len - (len(left_rule) + len(stats_title) + 2))
    body.append(
        f'<text x="{info_x}" y="{curr_y:.1f}" font-size="{font_size}px">'
        f'<tspan class="rule">{_esc(left_rule)}</tspan>'
        f'<tspan class="header">{_esc(stats_title)}</tspan>'
        f'<tspan class="rule">{_esc(right_rule_stats)}</tspan>'
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

    # Line 1: Repos & Stars
    repo_prefix = "· Repos: "
    repo_dots = "." * max(2, leader_fill - len(repo_prefix)) + " "
    # repos value + contrib: e.g. "9 {Contributed: 0}"
    repos_val_text = f"{repos} {{Contributed: {contrib}}}"
    # Pad so pipe "|" is at column 50
    pipe_pad_len = max(1, 50 - (len(repo_prefix) + len(repo_dots) + len(repos_val_text)))
    pipe_pad = " " * pipe_pad_len
    star_prefix = "Stars: "
    star_dots = "..... "

    body.append(
        f'<text x="{info_x}" y="{curr_y:.1f}" font-size="{font_size}px">'
        f'<tspan class="label">{_esc(repo_prefix)}</tspan>'
        f'<tspan class="secondary">{_esc(repo_dots)}</tspan>'
        f'<tspan class="number">{_esc(repos)}</tspan>'
        f'<tspan class="secondary"> {{Contributed: </tspan>'
        f'<tspan class="number">{_esc(contrib)}</tspan>'
        f'<tspan class="secondary">}}{pipe_pad}| </tspan>'
        f'<tspan class="label">{_esc(star_prefix)}</tspan>'
        f'<tspan class="secondary">{_esc(star_dots)}</tspan>'
        f'<tspan class="number">{_esc(stars)}</tspan>'
        f'</text>'
    )
    curr_y += line_height

    # Line 2: Commits & Followers
    commit_prefix = "· Commits: "
    commit_dots = "." * max(2, leader_fill - len(commit_prefix)) + " "
    commits_val_text = str(commits)
    pipe_pad_len2 = max(1, 50 - (len(commit_prefix) + len(commit_dots) + len(commits_val_text)))
    pipe_pad2 = " " * pipe_pad_len2
    follower_prefix = "Followers: "
    follower_dots = ". "

    body.append(
        f'<text x="{info_x}" y="{curr_y:.1f}" font-size="{font_size}px">'
        f'<tspan class="label">{_esc(commit_prefix)}</tspan>'
        f'<tspan class="secondary">{_esc(commit_dots)}</tspan>'
        f'<tspan class="number">{_esc(commits_val_text)}</tspan>'
        f'<tspan class="secondary">{pipe_pad2}| </tspan>'
        f'<tspan class="label">{_esc(follower_prefix)}</tspan>'
        f'<tspan class="secondary">{_esc(follower_dots)}</tspan>'
        f'<tspan class="number">{_esc(followers)}</tspan>'
        f'</text>'
    )
    curr_y += line_height

    # Line 3: LOC
    loc_prefix = "· Lines of Code: "
    loc_dots = "." * max(2, leader_fill - len(loc_prefix)) + " "
    body.append(
        f'<text x="{info_x}" y="{curr_y:.1f}" font-size="{font_size}px">'
        f'<tspan class="label">{_esc(loc_prefix)}</tspan>'
        f'<tspan class="secondary">{_esc(loc_dots)}</tspan>'
        f'<tspan class="number">{_esc(total_loc)} </tspan>'
        f'<tspan class="secondary">(</tspan>'
        f'<tspan class="positive"> {_esc(additions)}++</tspan>'
        f'<tspan class="secondary">, </tspan>'
        f'<tspan class="negative"> {_esc(deletions)}-- </tspan>'
        f'<tspan class="secondary">)</tspan>'
        f'</text>'
    )
    curr_y += line_height

    final_height = int(max(curr_y + 35, ascii_y + len(ascii_lines) * ascii_line_height + 40))

    # Assemble complete SVG document
    svg = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="0 0 {svg_width} {final_height}" width="{svg_width}px" height="{final_height}px" '
        f'font-family="{font_family_svg}">',
        f'<rect width="{svg_width}px" height="{final_height}px" fill="{colors["background"]}" rx="{SVG_CORNER_RADIUS}"/>'
    ]

    if colors.get("ascii_bg"):
        ascii_card_w = info_x - 30
        ascii_card_h = final_height - 24
        svg.append(f'<rect x="12" y="12" width="{ascii_card_w}" height="{ascii_card_h}" fill="{colors["ascii_bg"]}" rx="10"/>')

    svg.extend(body)
    svg.append("</svg>")

    return "\n".join(svg)


def save_svg(content: str, path: str) -> None:
    """Write SVG content to file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Saved: {path}")

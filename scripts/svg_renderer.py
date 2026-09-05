"""
SVG renderer for the terminal-style GitHub profile dashboard.

Generates self-contained SVG files for dark and light modes using the exact user-provided ASCII art.
Layout: 100% Face ASCII Portrait (left) | Big High-Legibility Terminal Dashboard (right) | Dynamic Projects (bottom)
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
    GITHUB_USERNAME, MAX_DESC_LENGTH,
)
from scripts.github_stats import calculate_uptime, format_number


def _esc(text: str) -> str:
    """Escape text for safe SVG/XML embedding."""
    return html.escape(str(text), quote=True)


def _build_info_line(label: str, value: str, leader_width: int = LEADER_FILL) -> tuple[str, str]:
    """Build a terminal-style info line with dotted leaders."""
    prefix = f"• {label}: "
    dots_needed = leader_width - len(prefix)
    if dots_needed < 2:
        dots_needed = 2
    leader = "." * dots_needed
    label_part = f"{prefix}{leader} "
    return label_part, value


def render_svg(
    ascii_lines: list[str],
    statistics: dict,
    projects: list[dict],
    mode: str = "dark",
) -> str:
    """
    Render a complete SVG profile dashboard with big, bold, high-contrast typography.
    """
    colors = DARK if mode == "dark" else LIGHT
    uptime = calculate_uptime()

    font_family_svg = FONT_FAMILY.replace('"', "'")

    # ASCII dimensions calculation
    ascii_max_len = max((len(l) for l in ascii_lines), default=60)
    ascii_font_size = ASCII_FONT_SIZE
    ascii_line_height = ASCII_LINE_HEIGHT
    ascii_x = ASCII_X
    ascii_y = ASCII_Y
    ascii_width = ascii_max_len * (ascii_font_size * 0.605)
    ascii_height = len(ascii_lines) * ascii_line_height

    # Info panel dimensions
    info_x = int(ascii_x + ascii_width + 50)
    info_y = INFO_Y
    info_font_size = INFO_FONT_SIZE
    info_line_height = INFO_LINE_HEIGHT
    leader_fill = LEADER_FILL
    sep_width = SEPARATOR_WIDTH

    val_color = "#FFFFFF" if mode == "dark" else colors["value"]

    svg_width = int(info_x + (sep_width + 2) * (info_font_size * 0.605) + 60)

    body = []

    # Style block
    body.append("<style>")
    body.append(f'  .label {{ fill: {colors["label"]}; font-size: {info_font_size}px; font-weight: 600; }}')
    body.append(f'  .value {{ fill: {val_color}; font-size: {info_font_size}px; font-weight: 500; }}')
    body.append(f'  .primary {{ fill: {colors["primary"]}; font-size: {info_font_size}px; }}')
    body.append(f'  .secondary {{ fill: {colors["secondary"]}; font-size: {info_font_size}px; }}')
    body.append(f'  .header {{ fill: {colors["header"]}; font-size: {info_font_size + 3}px; font-weight: bold; }}')
    body.append(f'  .ascii {{ fill: {colors["ascii"]}; font-size: {ascii_font_size}px; }}')
    body.append(f'  .positive {{ fill: {colors["positive"]}; font-size: {info_font_size}px; font-weight: 600; }}')
    body.append(f'  .negative {{ fill: {colors["negative"]}; font-size: {info_font_size}px; }}')
    body.append(f'  .link {{ fill: {colors["link"]}; font-size: {info_font_size}px; font-weight: 600; }}')
    body.append("  text, tspan { white-space: pre; }")
    body.append("  a { text-decoration: none; }")
    body.append("</style>")

    # ─── ASCII Portrait ─────────────────────────────────────────────────────
    if mode == "light":
        bg_dark = DARK["background"]
        body.append(
            f'<rect x="{ascii_x - 15}" y="{ascii_y - 18}" '
            f'width="{ascii_width + 30:.1f}" height="{ascii_height + 30:.1f}" '
            f'fill="{bg_dark}" rx="12"/>'
        )

    body.append(f'<text x="{ascii_x}" y="{ascii_y}" class="ascii">')
    for i, line in enumerate(ascii_lines):
        y = ascii_y + i * ascii_line_height
        body.append(f'<tspan x="{ascii_x}" y="{y:.1f}">{_esc(line)}</tspan>')
    body.append("</text>")

    # ─── Info Panel ──────────────────────────────────────────────────────────
    curr_y = info_y
    header_name = "mohith"
    header_at = "@"
    header_host = "github"
    header_sep = " " + "─" * max(10, sep_width - len("mohith@github") - 1)

    body.append(
        f'<text x="{info_x}" y="{curr_y:.1f}">'
        f'<tspan class="header">{_esc(header_name)}</tspan>'
        f'<tspan class="primary">{_esc(header_at)}</tspan>'
        f'<tspan class="header">{_esc(header_host)}</tspan>'
        f'<tspan class="secondary">{_esc(header_sep)}</tspan>'
        f'</text>'
    )
    curr_y += info_line_height + 10

    # Profile fields
    for field in PROFILE_FIELDS:
        if field is None:
            curr_y += 12
            continue

        label, value = field

        if label == "Uptime":
            value = uptime

        label_part, val_part = _build_info_line(label, value, leader_fill)
        body.append(
            f'<text x="{info_x}" y="{curr_y:.1f}">'
            f'<tspan class="label">{_esc(label_part)}</tspan>'
            f'<tspan class="value">{_esc(val_part)}</tspan>'
            f'</text>'
        )
        curr_y += info_line_height

    # ─── Contact Section ─────────────────────────────────────────────────────
    curr_y += 18
    contact_sep = f"─ Contact {'─' * max(10, sep_width - 10)}"
    body.append(
        f'<text x="{info_x}" y="{curr_y:.1f}" class="secondary">'
        f'{_esc(contact_sep)}</text>'
    )
    curr_y += info_line_height + 8

    for key, value in CONTACT.items():
        label_part, val_part = _build_info_line(key, value, leader_fill)
        url = CONTACT_URLS.get(key, "")

        if url:
            body.append(
                f'<a xlink:href="{_esc(url)}" target="_blank">'
                f'<text x="{info_x}" y="{curr_y:.1f}">'
                f'<tspan class="label">{_esc(label_part)}</tspan>'
                f'<tspan class="link">{_esc(val_part)}</tspan>'
                f'</text></a>'
            )
        else:
            body.append(
                f'<text x="{info_x}" y="{curr_y:.1f}">'
                f'<tspan class="label">{_esc(label_part)}</tspan>'
                f'<tspan class="value">{_esc(val_part)}</tspan>'
                f'</text>'
            )
        curr_y += info_line_height

    # ─── GitHub Stats Section ────────────────────────────────────────────────
    curr_y += 18
    stats_sep = f"─ GitHub Stats {'─' * max(10, sep_width - 15)}"
    body.append(
        f'<text x="{info_x}" y="{curr_y:.1f}" class="secondary">'
        f'{_esc(stats_sep)}</text>'
    )
    curr_y += info_line_height + 8

    repos = format_number(statistics.get("repos", 0))
    contrib = format_number(statistics.get("contributed_repos", 0))
    stars = format_number(statistics.get("stars", 0))
    commits = format_number(statistics.get("commits", 0))
    followers = format_number(statistics.get("followers", 0))
    additions = format_number(statistics.get("additions", 0))
    deletions = format_number(statistics.get("deletions", 0))
    total_loc = format_number(abs(statistics.get("total_loc", 0)))

    # Line 1: Repos
    repo_label = "• Repos: "
    repo_dots = "." * (leader_fill - len(repo_label))
    star_label = "Stars: "
    star_dots = "." * 8
    body.append(
        f'<text x="{info_x}" y="{curr_y:.1f}">'
        f'<tspan class="label">{_esc(repo_label + repo_dots)} </tspan>'
        f'<tspan class="value">{_esc(repos)}</tspan>'
        f'<tspan class="secondary"> {{Contributed: </tspan>'
        f'<tspan class="value">{_esc(contrib)}</tspan>'
        f'<tspan class="secondary">}} | </tspan>'
        f'<tspan class="label">{_esc(star_label + star_dots)} </tspan>'
        f'<tspan class="value">{_esc(stars)}</tspan>'
        f'</text>'
    )
    curr_y += info_line_height

    # Line 2: Commits
    commit_label = "• Commits: "
    commit_dots = "." * (leader_fill - len(commit_label))
    commits_str = str(commits)
    padding_needed = max(1, 16 - len(commits_str))
    commits_pad = " " * padding_needed
    follower_label = "Followers: "
    follower_dots = "." * 5
    body.append(
        f'<text x="{info_x}" y="{curr_y:.1f}">'
        f'<tspan class="label">{_esc(commit_label + commit_dots)} </tspan>'
        f'<tspan class="value">{_esc(commits_str)}</tspan>'
        f'<tspan class="secondary">{_esc(commits_pad)}| </tspan>'
        f'<tspan class="label">{_esc(follower_label + follower_dots)} </tspan>'
        f'<tspan class="value">{_esc(followers)}</tspan>'
        f'</text>'
    )
    curr_y += info_line_height

    # Line 3: Lines of Code
    loc_label = "• Lines of Code on GitHub: ...."
    body.append(
        f'<text x="{info_x}" y="{curr_y:.1f}">'
        f'<tspan class="label">{_esc(loc_label)} </tspan>'
        f'<tspan class="value">{_esc(total_loc)} </tspan>'
        f'<tspan class="secondary">(</tspan>'
        f'<tspan class="positive">{_esc(additions)}+</tspan>'
        f'<tspan class="secondary">, </tspan>'
        f'<tspan class="negative">{_esc(deletions)}−</tspan>'
        f'<tspan class="secondary">)</tspan>'
        f'</text>'
    )
    curr_y += info_line_height

    # ─── Projects Section ────────────────────────────────────────────────────
    proj_y = max(curr_y, ascii_y + ascii_height) + 40
    proj_x = ascii_x
    proj_font_size = info_font_size - 2.0
    proj_line_height = info_line_height
    proj_sep_len = int((svg_width - ascii_x * 2) / (proj_font_size * 0.605))

    proj_sep = f"─ Projects {'─' * max(20, proj_sep_len - 11)}"
    body.append(
        f'<text x="{proj_x}" y="{proj_y:.1f}" class="secondary">'
        f'{_esc(proj_sep)}</text>'
    )
    proj_y += proj_line_height + 8

    for proj in projects:
        name = proj["name"]
        desc = proj.get("description", "")
        lang = proj.get("language", "")
        url = proj.get("url", "")
        star_count = proj.get("stars", 0)

        max_desc = 100
        if len(desc) > max_desc:
            desc = desc[:max_desc - 3] + "..."

        name_part = f"• {name}"
        lang_part = f" [{lang}]" if lang else ""
        star_part = f" ★{star_count}" if star_count > 0 else ""

        prefix_len = len(name_part) + len(lang_part) + len(star_part)
        leader_len = max(3, 34 - prefix_len)
        leader = "." * leader_len

        if url:
            body.append(
                f'<a xlink:href="{_esc(url)}" target="_blank">'
                f'<text x="{proj_x}" y="{proj_y:.1f}">'
                f'<tspan class="link" style="font-size:{proj_font_size}px;">{_esc(name_part)}</tspan>'
                f'<tspan class="secondary" style="font-size:{proj_font_size}px;">{_esc(lang_part)}{_esc(star_part)} {_esc(leader)} </tspan>'
                f'<tspan class="primary" style="font-size:{proj_font_size}px;">{_esc(desc)}</tspan>'
                f'</text></a>'
            )
        else:
            body.append(
                f'<text x="{proj_x}" y="{proj_y:.1f}">'
                f'<tspan class="value" style="font-size:{proj_font_size}px;">{_esc(name_part)}</tspan>'
                f'<tspan class="secondary" style="font-size:{proj_font_size}px;">{_esc(lang_part)}{_esc(star_part)} {_esc(leader)} </tspan>'
                f'<tspan class="primary" style="font-size:{proj_font_size}px;">{_esc(desc)}</tspan>'
                f'</text>'
            )
        proj_y += proj_line_height

    final_height = int(proj_y + 35)

    # Assemble complete SVG document
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="0 0 {svg_width} {final_height}" '
        f'width="{svg_width}px" height="{final_height}px" '
        f'font-family="{font_family_svg}">'
    )
    lines.append(
        f'<rect width="{svg_width}px" height="{final_height}px" '
        f'fill="{colors["background"]}" rx="18"/>'
    )
    lines.extend(body)
    lines.append("</svg>")

    return "\n".join(lines)


def save_svg(content: str, path: str) -> None:
    """Write SVG content to file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Saved: {path}")

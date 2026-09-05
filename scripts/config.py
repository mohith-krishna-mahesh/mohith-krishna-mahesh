"""
Central configuration for the GitHub profile README generator.
All magic numbers, colors, dimensions, and personal info live here.
"""

import os
from datetime import date

# ─── Identity ─────────────────────────────────────────────────────────────────

GITHUB_USERNAME = "mohith-krishna-mahesh"
DISPLAY_NAME = "Mohith Krishna Mahesh"
DATE_OF_BIRTH = date(2007, 2, 12)

# ─── Contact ──────────────────────────────────────────────────────────────────

CONTACT = {
    "GitHub": "github.com/mohith-krishna-mahesh",
    "LinkedIn": "linkedin.com/in/mohith-krishna-mahesh",
    "Email": "mohith4533@gmail.com",
}

CONTACT_URLS = {
    "GitHub": "https://github.com/mohith-krishna-mahesh",
    "LinkedIn": "https://www.linkedin.com/in/mohith-krishna-mahesh/",
    "Email": "mailto:mohith4533@gmail.com",
}

# ─── Profile Fields ──────────────────────────────────────────────────────────

PROFILE_FIELDS = [
    ("OS", "macOS, Kali Linux, Fedora, Windows 10"),
    ("Uptime", None),  # dynamically calculated
    ("Host", "VIT Chennai"),
    ("Kernel", "B.Tech Computer Science"),
    ("IDE", "Zed, VSCode"),
    None,  # blank line separator
    ("Languages.Programming", "Python, C, C++, Java, JavaScript, TypeScript, Bash"),
    ("Languages.Computer", "HTML, CSS, SQL, JSON, YAML, LaTeX"),
    ("Languages.Real", "Malayalam, English, Tamil, Hindi"),
    None,
    ("Research.Area", "Cryptography"),
    ("Research.Project", "MOSAIC"),
    None,
    ("Interests.Software", "Cybersecurity, Systems, Full-Stack, AI/ML, Blockchain, Game Development"),
    ("Interests.Hardware", "Communication Systems, Rover Development"),
    ("Interests.Events", "CTFs, Hackathons, Game Jams, Robotics Competitions"),
    ("Interests.Science", "Mathematics, Physics, Chemistry, Biology"),
    ("Interests.Humanities", "Philosophy, History, Art"),
]

# ─── Paths ────────────────────────────────────────────────────────────────────

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
SOURCE_DIR = os.path.join(ASSETS_DIR, "source")
CACHE_DIR = os.path.join(ROOT_DIR, "cache")
SCRIPTS_DIR = os.path.join(ROOT_DIR, "scripts")

SOURCE_PHOTO = os.path.join(SOURCE_DIR, "photo.jpg")
DARK_SVG = os.path.join(ASSETS_DIR, "dark_mode.svg")
LIGHT_SVG = os.path.join(ASSETS_DIR, "light_mode.svg")

CACHE_PROFILE = os.path.join(CACHE_DIR, "profile.json")
CACHE_REPOS = os.path.join(CACHE_DIR, "repositories.json")
CACHE_STATS = os.path.join(CACHE_DIR, "statistics.json")

# ─── SVG Dimensions ──────────────────────────────────────────────────────────

SVG_WIDTH = 2900
SVG_HEIGHT = 1680
SVG_CORNER_RADIUS = 18

# ─── Font ─────────────────────────────────────────────────────────────────────

FONT_FAMILY = '"JetBrainsMono Nerd Font", "JetBrains Mono", "JetBrainsMono NF", monospace'
INFO_FONT_SIZE = 25.0
INFO_LINE_HEIGHT = 42.0

# ─── ASCII Art Configuration ─────────────────────────────────────────────────

ASCII_FONT_SIZE = 4.8
ASCII_LINE_HEIGHT = 6.4
ASCII_SLICE_TOP = 22       # slice top background lines
ASCII_SLICE_BOTTOM = 51    # slice bottom background lines

# ─── Layout ───────────────────────────────────────────────────────────────────

ASCII_X = 30
ASCII_Y = 40

INFO_X = 1220
INFO_Y = 55

# Info panel formatting
LEADER_FILL = 32     # total width including label and leaders
SEPARATOR_WIDTH = 104

# ─── Dark Mode Colors (Hacker / Matrix Terminal Theme) ─────────────────────────

DARK = {
    "background": "#080C08",     # deep terminal black-green
    "primary": "#E2E8F0",       # readable minty white
    "secondary": "#234E35",     # subtle matrix green separators/leaders
    "label": "#00FF66",         # vivid matrix neon green
    "value": "#A7F3D0",         # phosphor mint / soft glow
    "positive": "#00FF66",      # neon additions
    "negative": "#FF3366",      # cyber crimson deletions
    "header": "#00FF66",        # neon prompt
    "ascii": "#00FF66",         # glowing phosphor ASCII portrait
    "link": "#00E5FF",          # electric cyan links
}

# ─── Light Mode Colors (Hacker Light Terminal Theme) ──────────────────────────

LIGHT = {
    "background": "#F0FDF4",     # soft terminal green-tinted light background
    "primary": "#1F2937",       # readable dark charcoal
    "secondary": "#6EE7B7",     # emerald separators/leaders
    "label": "#047857",         # deep emerald hacker green
    "value": "#065F46",         # dark forest value text
    "positive": "#059669",      # additions
    "negative": "#DC2626",      # deletions
    "header": "#064E3B",        # terminal header
    "ascii": "#00FF66",         # identical glowing phosphor ASCII portrait
    "link": "#0D9488",          # cyber teal clickable links
}

# ─── GitHub API ───────────────────────────────────────────────────────────────

GITHUB_API_BASE = "https://api.github.com"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

# Repos to skip in project listing (e.g. the profile repo itself)
SKIP_REPOS = {"mohith-krishna-mahesh"}

# Maximum projects to show
MAX_PROJECTS = 6

# Maximum description length
MAX_DESC_LENGTH = 60

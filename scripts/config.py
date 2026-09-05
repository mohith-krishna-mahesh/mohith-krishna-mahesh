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

SVG_WIDTH = 1290
SVG_HEIGHT = 715
SVG_CORNER_RADIUS = 15

# ─── Font ─────────────────────────────────────────────────────────────────────

FONT_FAMILY = '"JetBrainsMono Nerd Font", "JetBrains Mono", "JetBrainsMono NF", monospace'
INFO_FONT_SIZE = 17.5
INFO_LINE_HEIGHT = 23.5

# ─── ASCII Art Configuration ─────────────────────────────────────────────────

ASCII_FONT_SIZE = 16.5
ASCII_LINE_HEIGHT = 18.2

# ─── Layout ───────────────────────────────────────────────────────────────────

ASCII_X = 22
ASCII_Y = 28

INFO_X = 595
INFO_Y = 28

# Info panel formatting
LEADER_FILL = 26     # total width including label and leaders
SEPARATOR_WIDTH = 52

# ─── Dark Mode Colors (VS Code Hacker Theme) ──────────────────────────────────

DARK = {
    "background": "#080C08",      # Deep terminal black
    "primary": "#E2E8F0",        # Crisp white/light gray
    "secondary": "#284E3A",      # Matrix green separators/leaders
    "header": "#00FF66",         # Neon prompt
    "label": "#00FF66",          # Neon green labels
    "value": "#79C0FF",          # Electric ice blue values
    "ascii": "#FFFFFF",          # Crisp white portrait (Dark mode)
    "positive": "#00FF66",       # Additions
    "negative": "#FF5555",       # Deletions
    "link": "#00E5FF",           # Cyber cyan links
}

# ─── Light Mode Colors (Hacker Light Terminal Theme) ──────────────────────────

LIGHT = {
    "background": "#F0FDF4",     # Matrix light green tint
    "primary": "#1F2937",        # Charcoal
    "secondary": "#6EE7B7",      # Emerald leaders
    "header": "#064E3B",         # Deep dark green prompt
    "label": "#047857",          # Deep emerald labels
    "value": "#0284C7",          # Deep cyan/blue values
    "ascii": "#000000",          # Crisp black portrait (Light mode)
    "positive": "#059669",       # Additions
    "negative": "#DC2626",       # Deletions
    "link": "#0D9488",           # Cyber teal links
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

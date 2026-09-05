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

SVG_WIDTH = 1280
SVG_HEIGHT = 745
SVG_CORNER_RADIUS = 15

# ─── Font ─────────────────────────────────────────────────────────────────────

FONT_FAMILY = '"JetBrainsMono Nerd Font", "JetBrains Mono", "JetBrainsMono NF", monospace'
INFO_FONT_SIZE = 17.0
INFO_LINE_HEIGHT = 22.5

# ─── ASCII Art Configuration ─────────────────────────────────────────────────

ASCII_FONT_SIZE = 16.5
ASCII_LINE_HEIGHT = 18.2

# ─── Layout ───────────────────────────────────────────────────────────────────

ASCII_X = 22
ASCII_Y = 28

INFO_X = 575
INFO_Y = 28

# Info panel formatting
LEADER_FILL = 23     # total width including label and leaders
SEPARATOR_WIDTH = 48

# ─── Dark Mode Colors (VS Code Hacker Theme) ──────────────────────────────────

DARK = {
    "background": "#0A0B0A",      # Deep dark background from Hacker.json
    "primary": "#BBBBBB",        # Base text from Hacker.json
    "secondary": "#4E6554",      # Matrix green-charcoal dotted leaders
    "rule": "#81B38C",           # Solid prominent hacker green header rules
    "header": "#81B38C",         # Bold hacker green section headers
    "prompt_user": "#7fb4ca",    # Electric cyber blue prompt user
    "prompt_at": "#e6c384",      # Golden amber at symbol
    "prompt_host": "#81B38C",    # Hacker green host
    "label": "#81B38C",          # Rich prominent hacker green labels
    "value": "#F8FAFC",          # Crisp bright white values
    "number": "#e6c384",         # Golden stats numbers from Hacker.json
    "ascii": "#FFFFFF",          # Pure white ASCII portrait
    "positive": "#81B38C",       # Hacker green additions
    "negative": "#ff5d62",       # Vibrant coral red deletions
    "link": "#7fb4ca",           # Electric cyber blue links
}

# ─── Light Mode Colors (Hacker Light Terminal Theme) ──────────────────────────

LIGHT = {
    "background": "#F5F5F4",     # Soft light neutral surface
    "primary": "#393836",        # Slate dark text
    "secondary": "#A8A29E",      # Subtle border/leaders
    "rule": "#2D6A4F",           # Bold emerald rules
    "header": "#2D6A4F",         # Deep forest green header
    "prompt_user": "#2563EB",    # Royal blue prompt user
    "prompt_at": "#B45309",      # Amber at symbol
    "prompt_host": "#2D6A4F",    # Forest green host
    "label": "#2D6A4F",          # Deep forest green label
    "value": "#18181B",          # Dark value text
    "number": "#B45309",         # Amber stats numbers
    "ascii": "#000000",          # Pure black ASCII portrait
    "positive": "#2D6A4F",       # Green additions
    "negative": "#DC2626",       # Crimson deletions
    "link": "#2563EB",           # Accent link
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

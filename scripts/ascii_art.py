"""
ASCII art loader & pipeline.

Loads the exact user-provided ASCII art and applies vertical slicing (top & bottom).
Full horizontal character width is preserved to ensure the complete face is 100% intact.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.config import SOURCE_DIR


COMPACT_ASCII_PATH = os.path.join(SOURCE_DIR, "compact_ascii.txt")
COMPACT_ASCII_LIGHT_PATH = os.path.join(SOURCE_DIR, "compact_ascii_light.txt")
USER_ASCII_PATH = os.path.join(SOURCE_DIR, "user_ascii.txt")


def generate_ascii(path: str = None, mode: str = "dark") -> list[str]:
    """
    Load and return the compact 44x30 face ASCII art lines.
    Supports mode='dark' and mode='light'.
    """
    if path is None:
        if mode == "light" and os.path.exists(COMPACT_ASCII_LIGHT_PATH):
            target = COMPACT_ASCII_LIGHT_PATH
        else:
            target = COMPACT_ASCII_PATH if os.path.exists(COMPACT_ASCII_PATH) else USER_ASCII_PATH
    else:
        target = path

    if os.path.exists(target):
        with open(target, "r", encoding="utf-8") as f:
            lines = [l.rstrip("\r\n") for l in f.readlines()]
        # Trim leading and trailing empty lines
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()

        if target == USER_ASCII_PATH:
            # Slice top and bottom background margins for large user_ascii.txt
            total = len(lines)
            start = 22 if total > 73 else 0
            end = total - 51 if total > 73 else total
            lines = lines[start:end]

        # Preserve character spacing, only stripping trailing spaces
        return [l.rstrip() for l in lines]
    return []


def ascii_to_string(lines: list[str]) -> str:
    """Join ASCII lines into a single string for display."""
    return "\n".join(lines)


if __name__ == "__main__":
    lines = generate_ascii()
    print(f"Loaded full-face ASCII: {len(lines)} lines, max width {max(len(l) for l in lines)} chars")

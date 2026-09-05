"""
ASCII art loader & pipeline.

Loads the exact user-provided ASCII art and applies vertical slicing (top & bottom).
Full horizontal character width is preserved to ensure the complete face is 100% intact.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.config import SOURCE_DIR, ASCII_SLICE_TOP, ASCII_SLICE_BOTTOM


USER_ASCII_PATH = os.path.join(SOURCE_DIR, "user_ascii.txt")


def generate_ascii(path: str = USER_ASCII_PATH) -> list[str]:
    """
    Load and return the exact ASCII art lines, preserving 100% full face width.
    """
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            lines = [l.rstrip("\r\n") for l in f.readlines()]
        # Trim leading and trailing empty lines
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()

        # Slice top and bottom background margins
        total = len(lines)
        start = ASCII_SLICE_TOP if total > ASCII_SLICE_TOP + ASCII_SLICE_BOTTOM else 0
        end = total - ASCII_SLICE_BOTTOM if total > ASCII_SLICE_TOP + ASCII_SLICE_BOTTOM else total
        sliced = lines[start:end]

        # Preserve full horizontal width, only stripping trailing spaces
        return [l.rstrip() for l in sliced]
    return []


def ascii_to_string(lines: list[str]) -> str:
    """Join ASCII lines into a single string for display."""
    return "\n".join(lines)


if __name__ == "__main__":
    lines = generate_ascii()
    print(f"Loaded full-face ASCII: {len(lines)} lines, max width {max(len(l) for l in lines)} chars")

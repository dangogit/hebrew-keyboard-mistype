#!/usr/bin/env python3
"""Decode Hebrew keyboard mistypes back to the English keys at the same QWERTY position.

The user wanted to type English but their macOS keyboard layout was set to Hebrew, so the
keystrokes produced Hebrew characters instead of Latin letters. This script reverses the
mapping using the standard Israeli Hebrew (PC) layout — the same mapping used by macOS's
built-in "Hebrew" and "Hebrew - QWERTY" sources for the alphabetic keys.

Usage:
    python decode.py "יקךךם"                 # -> hello
    python decode.py "yje hjvf?"  --reverse  # English typed when Hebrew was meant
    echo "יקךךם, צשנק שמ שפפ" | python decode.py -   # read from stdin
"""
import sys

# Hebrew char -> English key at the same physical QWERTY position.
# Source: standard Israeli "Hebrew (PC)" / "Hebrew - QWERTY" layouts.
HEB_TO_EN = {
    # top row
    "/": "q", "'": "w", "ק": "e", "ר": "r", "א": "t",
    "ט": "y", "ו": "u", "ן": "i", "ם": "o", "פ": "p",
    # home row
    "ש": "a", "ד": "s", "ג": "d", "כ": "f", "ע": "g",
    "י": "h", "ח": "j", "ל": "k", "ך": "l", "ף": ";",
    "," : "'",  # Hebrew layout swaps comma <-> apostrophe
    # bottom row
    "ז": "z", "ס": "x", "ב": "c", "ה": "v", "נ": "b",
    "מ": "n", "צ": "m", "ת": ",", "ץ": ".",
    ".": "/",
}

# Reverse: English key -> Hebrew char at same position (for the rarer case where the
# user wanted Hebrew but the keyboard was on English).
EN_TO_HEB = {v: k for k, v in HEB_TO_EN.items()}


def heb_to_en(text: str) -> str:
    """Map Hebrew chars to the English key at the same QWERTY position.
    Spaces, digits, and any chars not in the table pass through unchanged."""
    return "".join(HEB_TO_EN.get(c, c) for c in text)


def en_to_heb(text: str) -> str:
    """Reverse mapping — English to Hebrew at same positions. Case-insensitive."""
    return "".join(EN_TO_HEB.get(c.lower(), c) for c in text)


def main() -> int:
    args = sys.argv[1:]
    reverse = "--reverse" in args
    args = [a for a in args if a != "--reverse"]
    if not args:
        print("usage: decode.py <text> [--reverse]   (use '-' to read stdin)", file=sys.stderr)
        return 1
    text = sys.stdin.read() if args[0] == "-" else " ".join(args)
    out = en_to_heb(text) if reverse else heb_to_en(text)
    print(out, end="" if text.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

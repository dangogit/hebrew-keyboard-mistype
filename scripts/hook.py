#!/usr/bin/env python3
"""Claude Code UserPromptSubmit hook for hebrew-keyboard-mistype.

Fires on every user prompt. If the prompt contains Hebrew characters, decodes them
back to the English keys at the same QWERTY position and injects an `additionalContext`
note so Claude knows it might be a keyboard-layout mistype and which skill to use.

Stays silent (exit 0, no output) when the prompt has no Hebrew chars — fast path for
the common case so we don't add latency to normal English messages.
"""
import json
import os
import sys

HEBREW_START, HEBREW_END = 0x0590, 0x05FF


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0  # malformed input, don't block the prompt

    prompt = data.get("prompt", "") or ""
    if not any(HEBREW_START <= ord(c) <= HEBREW_END for c in prompt):
        return 0  # no Hebrew, nothing to suggest

    # Decode using the bundled mapping
    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, here)
    try:
        from decode import heb_to_en
    except ImportError:
        return 0  # decoder missing, fail silent rather than block

    decoded = heb_to_en(prompt)

    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": (
                "[hebrew-keyboard-mistype hook] The user's message contains Hebrew characters. "
                "If those characters don't form real Hebrew words, the user likely typed with "
                "the keyboard accidentally set to Hebrew. Decoded back to the English keys at "
                f"the same QWERTY positions: {decoded!r}. "
                "If the decoded text reads as a coherent English request, treat it as the user's "
                "actual intent, acknowledge it in one short line, and proceed. "
                "If the decoded text is also gibberish, the user probably meant real Hebrew — "
                "respond accordingly. See the hebrew-keyboard-mistype skill for the full mapping."
            ),
        }
    }
    print(json.dumps(output))
    return 0


if __name__ == "__main__":
    sys.exit(main())

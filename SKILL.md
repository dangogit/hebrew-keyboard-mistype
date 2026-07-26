---
name: hebrew-keyboard-mistype
description: "Use whenever the user's message contains Hebrew characters that look like English typed with a forgotten/stuck Hebrew keyboard layout — i.e., the Hebrew letters don't form sensible Hebrew words, especially when mixed with English text, code, file paths, brand names, or technical content. The skill decodes the Hebrew back to the English keys at the same physical QWERTY position (e.g., \"יקךךם\" → \"hello\", \"ביקבל איןד\" → \"check this\"), confirms the recovered text in one short line, and proceeds with the corrected request. Always check for this pattern when Hebrew appears unexpectedly in an otherwise English/technical conversation — it costs nothing to decode and the user has explicitly asked for this auto-correction. Also handles the rarer reverse case: Latin-looking gibberish that decodes back to real Hebrew (keyboard was on English when they meant to type Hebrew)."
license: MIT
compatibility: Works with Claude Code, Claude.ai, Codex, Cursor. Requires python3 on PATH for the decoder script. No network required.
---

# Hebrew Keyboard Mistype Recovery

The user is a Hebrew/English bilingual who routinely switches keyboard layouts. They sometimes type a request thinking the keyboard is on English when it's actually on Hebrew (or vice versa). The result is gibberish — Hebrew characters at QWERTY positions, or Latin characters at Hebrew positions. They want you to detect this, decode it, and proceed with what they actually meant — without making them retype.

## When this triggers

Look for these signals in the user's message:

- **Hebrew letters appear in an otherwise English/technical conversation.** This codebase, the user's projects, and most of your interactions are in English. If a Hebrew blob shows up unannounced, suspect a mistype first.
- **The Hebrew "word" violates Hebrew spelling.** Strong tells: a final-form letter (ך ם ן ף ץ) in the middle of a word, two final letters in a row (e.g., "ךך" from "ll"), three consonants with no vowel letters in a place where Hebrew would need one, or sequences that no Hebrew word would form.
- **Hebrew mixed with English fragments, code, URLs, filenames, or numbers.** Real Hebrew sentences rarely interleave with English at the word level — but a half-typed mistype does (the user noticed mid-sentence and switched layouts).
- **A short Hebrew "word" sitting next to a clearly English request.** E.g., "fix the יקך" — that's almost certainly a mistype of "fix the bug" parts.

If the Hebrew genuinely forms a valid Hebrew sentence and the surrounding context is Hebrew, **do not trigger** — the user meant Hebrew. When in doubt, run the decoder anyway and check whether the output is a recognizable English request that fits the conversation. If yes, it was a mistype. If the output is also gibberish, the user probably meant Hebrew.

The reverse case is rarer but possible: Latin-looking gibberish (`yje hjvf` style) that decodes to real Hebrew. Apply the same heuristic — if pure-Latin gibberish appears where Hebrew would make sense, try `--reverse`.

## How to recover

Use the bundled decode script — don't translate by hand. The mapping is the standard Israeli Hebrew (PC) layout, which is what macOS uses for the "Hebrew" and "Hebrew – QWERTY" input sources.

```bash
DECODE=$(ls ~/.claude/skills/hebrew-keyboard-mistype/scripts/decode.py \
            ~/.agents/skills/hebrew-keyboard-mistype/scripts/decode.py \
            ~/.codex/skills/hebrew-keyboard-mistype/scripts/decode.py \
            ~/agent-skills/hebrew-keyboard-mistype/scripts/decode.py 2>/dev/null | head -1)
python3 "$DECODE" "<the suspected text>"
# For the reverse case (English chars where Hebrew was meant):
python3 "$DECODE" "<text>" --reverse
```

The skill directory is wherever the user installed it, so resolve the script path instead of hardcoding one. The snippet above checks the usual locations in order and takes the first hit; if none match, find the script under the skill directory you were loaded from.

Pass the suspect chunk (or the whole message — non-Hebrew chars pass through unchanged, so it's safe to feed mixed content). The script prints the decoded text to stdout.

Then:

1. **Acknowledge in one short line** so the user knows what you interpreted, and can correct you if you guessed wrong. Example: *"Reading that as: 'check this script' (Hebrew keyboard was on)."* Keep it to a single sentence — don't lecture, don't apologize on the user's behalf.
2. **Proceed with the decoded request as if they'd typed it that way.** Don't ask "did you mean…?" unless the decoded output is itself ambiguous or also gibberish — the user has asked for auto-correction, not a confirmation prompt.
3. **If only part of the message is mistyped** (e.g., a project name or filename that they typed before switching layouts), decode just that part and proceed normally with the rest.

## Mapping reference

The decoder handles this — you should not need this table directly — but it's here for transparency and for debugging edge cases.

| Hebrew | → English | | Hebrew | → English | | Hebrew | → English |
|---|---|---|---|---|---|---|---|
| ק | e | | ש | a | | ז | z |
| ר | r | | ד | s | | ס | x |
| א | t | | ג | d | | ב | c |
| ט | y | | כ | f | | ה | v |
| ו | u | | ע | g | | נ | b |
| ן | i | | י | h | | מ | n |
| ם | o | | ח | j | | צ | m |
| פ | p | | ל | k | | ת | , |
| ף | ; | | ך | l | | ץ | . |
| /  | q | | '  | w | | .  | / |

Note the final forms (ך ם ן ף ץ) map to l o i ; . — that's why "hello" → "יקךךם" produces two final-kaf in a row, an illegal Hebrew sequence and a strong mistype tell.

## Examples

**Example 1 — pure mistype**
User: `יקךךם, בשמ טםו אקךך צק ש חםלק?`
Decode: `hello, can you tell me a joke?`
Your response opens with: *"Reading that as: 'hello, can you tell me a joke?' (Hebrew layout was on)."* Then answer the joke request.

**Example 2 — mistype mixed with English**
User: `please ביקבל איןד דברןפא for bugs`
Decode of the Hebrew chunk: `check this script`
Your response opens with: *"Reading the Hebrew chunk as 'check this script'."* Then review the script.

**Example 3 — real Hebrew, do NOT trigger**
User: `תכתוב לי בעברית בבקשה`
This is grammatical Hebrew ("please write to me in Hebrew"). Do not decode — respond in Hebrew.

**Example 4 — reverse direction**
User: `yje hjvf` appears with no English meaning in a Hebrew-leaning conversation.
Decode with `--reverse`: `הימ יםלכ` — still gibberish, so this wasn't the reverse case. (Real reverse-direction Hebrew is rare; only attempt it if forward-decoding also produces gibberish.)

## Why this exists

The user explicitly asked for this skill so they don't have to retype messages when they catch the layout mistake. The cost of decoding is near-zero; the cost of ignoring a mistype is the user has to type the whole thing again. Bias toward decoding and acknowledging, not toward asking "did you mean…?".

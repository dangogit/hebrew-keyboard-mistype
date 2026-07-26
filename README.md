# hebrew-keyboard-mistype

A Claude Code / Claude.ai / Codex skill that recovers messages typed with the wrong keyboard layout.

You meant to type `hello`, but the keyboard was on Hebrew, so what came out was `יקךךם`. This skill teaches the AI to recognize that pattern, decode the Hebrew characters back to the English keys at the same physical QWERTY position, and proceed with your actual request, no retyping needed.

Built for the standard Israeli Hebrew (PC) layout, the same mapping macOS uses for its "Hebrew" and "Hebrew – QWERTY" input sources.

## What it does

| You typed (Hebrew layout was on) | The AI reads it as |
|---|---|
| `יקךךם` | `hello` |
| `ביקבל איןד דברןפא` | `check this script` |
| `please ביקבל איןד דברןפא for bugs` | `please check this script for bugs` (mixed input works) |
| `פןס איןד נוע` | `fix this bug` |
| `תכתוב לי בעברית בבקשה` | *(real Hebrew, left as-is, no decode)* |

The decoder also supports `--reverse` for the rarer case where you wanted Hebrew but the keyboard was on English.

## How it works

The skill ships with `SKILL.md` (instructions for the AI on when and how to trigger) plus a deterministic Python decoder script. When the AI detects Hebrew letters in a context where English makes more sense (gibberish-looking blobs, mixes with code or filenames, final-form letters appearing mid-word), it runs the decoder, acknowledges the recovered text in one short line, and continues with the task.

A strong "tell" for a keyboard mistype is two final-form letters in a row (e.g., `ךך` from `ll` in `hello`), which is illegal in real Hebrew spelling.

## Install

### As a Claude Code skill

Drop the directory into your shared skills location (Claude Code and Codex both look at `~/.claude/skills/` and `~/.codex/skills/`, which on most setups symlink to a shared dir):

```bash
git clone https://github.com/dangogit/hebrew-keyboard-mistype ~/.claude/skills/hebrew-keyboard-mistype
```

Or via the [`skills`](https://www.skills.sh) CLI:

```bash
npx skills add dangogit/hebrew-keyboard-mistype
```

### Optional: auto-detect hook

For the strongest trigger guarantee, add this to your `~/.claude/settings.json` under `hooks`. It runs the decoder on every prompt that contains Hebrew characters and injects a one-line hint to Claude:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 /absolute/path/to/hebrew-keyboard-mistype/scripts/hook.py",
            "timeout": 5000
          }
        ]
      }
    ]
  }
}
```

The hook stays silent (zero output, ~5 ms) on prompts without Hebrew, so it doesn't add latency to normal English messages.

## Manual use

The decoder script is usable on its own:

```bash
python3 scripts/decode.py "יקךךם"           # -> hello
python3 scripts/decode.py "yje hjvf" --reverse   # -> attempt to recover Hebrew from English keys
echo "פןס איןד נוע" | python3 scripts/decode.py -   # read from stdin
```

## The mapping

Standard Israeli Hebrew (PC) layout. Non-mapped characters (digits, spaces, English letters already in the message) pass through unchanged.

| Hebrew | → English | Hebrew | → English | Hebrew | → English |
|---|---|---|---|---|---|
| ק | e | ש | a | ז | z |
| ר | r | ד | s | ס | x |
| א | t | ג | d | ב | c |
| ט | y | כ | f | ה | v |
| ו | u | ע | g | נ | b |
| ן | i | י | h | מ | n |
| ם | o | ח | j | צ | m |
| פ | p | ל | k | ת | , |
| ף | ; | ך | l | ץ | . |
| / | q | ' | w | . | / |

## License

MIT.

## Contributing

PRs welcome, especially for additional layout variants (Hebrew – SI 1452, Hebrew – Hebrew script, custom user layouts), better mistype heuristics, or translations of the SKILL.md.

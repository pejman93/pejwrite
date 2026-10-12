# PejWrite

Fix or rewrite selected text in any macOS app, straight from the right-click menu.

Select text, right-click, choose **Services → PejWrite**, pick what you want, and the
selection is replaced in place. It works in browsers, Mail, Notes, Pages, and most other
apps that support macOS Services.

## Features

- **Fix grammar (keep my tone)** – corrects spelling, grammar and punctuation only
- **Friendly**, **Formal**, **Funny** – rewrites the selection in that tone
- **Custom prompt** – type your own instruction, e.g. *"shorter and softer"*
- Nothing runs in the background; the script starts on click and exits when done
- The API key is stored in the macOS Keychain, never in a file
- If a request fails, the original text is left untouched and a notification explains why

## Requirements

- macOS
- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com)

## Installation

```bash
git clone https://github.com/pejman93/pejwrite.git
cd pejwrite
./install.sh
```

Then store your API key in the Keychain. The command prompts for the key, so it never
ends up in your shell history:

```bash
security add-generic-password -a "$USER" -s ai-rewrite -w
```

## Usage

1. Select text in any app (press `⌘A` first to take the whole field).
2. Right-click → **Services** → **PejWrite**.
3. Choose an option. The result replaces the selection after a few seconds.

The first run asks for permission to control *System Events*; this is what displays the
option list.

To trigger it from the keyboard, assign a shortcut under
**System Settings → Keyboard → Keyboard Shortcuts → Services → Text → PejWrite**.

## Configuration

Everything is at the top of [`rewrite.py`](rewrite.py):

| Setting | Purpose |
|---|---|
| `MODEL` | Claude model used for rewriting |
| `MODES` | The instruction sent for each tone |
| `MENU` | Labels shown in the option list |

To add a tone, add one entry to `MODES` and one to `MENU`. No reinstall is needed.

## How it works

```
selected text ──▶ Quick Action (PejWrite.workflow) ──▶ rewrite.py ──▶ Claude API
                                                          │
      selection replaced ◀── stdout ◀─────────────────────┘
```

`make_services.py` generates an Automator Quick Action in `~/Library/Services` that pipes
the selection to `rewrite.py` and replaces it with the script's output. `rewrite.py` shows
the option list, reads the API key from the Keychain, and sends the text and instruction
to the Claude API.

## Troubleshooting

- **PejWrite is missing from the menu** – enable it under System Settings → Keyboard →
  Keyboard Shortcuts → Services → Text, then restart the app you are in.
- **"The API key was rejected"** – replace the stored key:
  `security add-generic-password -U -a "$USER" -s ai-rewrite -w`
- **Moved the project folder** – run `./install.sh` again; the Quick Action stores the
  absolute path to the script.

## Uninstall

```bash
rm -rf ~/Library/Services/PejWrite.workflow
security delete-generic-password -s ai-rewrite
```

## License

[MIT](LICENSE)

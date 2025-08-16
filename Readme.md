# Meet Bot

A Google Meet automation bot that:
- Reads chat 
- Reply chat
- Detects raised hands

It works by attaching to **Brave/Chrome** running in `--remote-debugging-port` mode via the Chrome DevTools Protocol.

## Demo


https://github.com/user-attachments/assets/00b8044e-442b-47ca-9a67-d90dc0e20e76




---

## Setup

1. Install dependencies:

```bash
uv venv
uv sync
```

2. Start Brave with remote debugging:
```bash
brave-browser --remote-debugging-port=9222 --user-data-dir=$(mktemp -d)
```

3. Join your Google Meet manually in that window.
4. Run
```bash
python -m meetbot.main
```
or
```bash
make run
```

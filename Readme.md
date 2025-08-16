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


## Usage Examples
```py
import asyncio

from meetbot.browser import BrowserController
from meetbot.chat import ChatManager
from meetbot.interact import Interact


async def main():
    browser = BrowserController()
    await browser.connect()
    chat = ChatManager(browser)
    await chat.init_chat_observer()
    msg = await chat.get_message()
    print(msg.user, msg.id, msg.content)
    await chat.send_message(input("enter the reply:- "))

    interaction = Interact(browser)
    [
        await interaction.send_reaction(i)
        for i in [
            "heart",
            "thumbs_up",
            "tada",
            "clap",
            "joy",
            "surprised",
            "cry",
            "thinking",
            "thumbs_down",
        ]
    ]

    await interaction.toggle_camera()
    await interaction.toggle_hand_raise()
    print(await interaction.get_peoples())
    await interaction.share_screen()
    await interaction.toggle_mic()
asyncio.run(main())
```
from pathlib import Path

from typing_extensions import deprecated

from meetbot.browser import BrowserController
from meetbot.type_hints import Reaction_T

MY_DIR = Path(__file__).parent

ReactionMap: dict[Reaction_T, str] = {
    "heart": "💖",
    "thumbs_up": "👍",
    "tada": "🎉",
    "clap": "👏",
    "joy": "😂",
    "surprised": "😮",
    "cry": "😢",
    "thinking": "🤔",
    "thumbs_down": "👎",
}


class Interact:
    def __init__(self, browser: BrowserController):
        self.browser = browser

    async def toggle_hand_raise(self):
        script = """
        (
            document.querySelector('button[aria-label="Raise hand (Ctrl + alt + h)"]') ||
            document.querySelector('button[aria-label="Lower hand (Ctrl + alt + h)"]') 
        )?.click();
        """
        return await self.browser.run_js(script)

    async def toggle_mic(self):
        script = """
        (
            document.querySelector('button[aria-label="Turn off microphone"]') ||
            document.querySelector('button[aria-label="Turn on microphone"]')
        )?.click();
        """
        return await self.browser.run_js(script)

    async def toggle_camera(self):
        script = """
        (

            document.querySelector('button[aria-label="Camera problem. Show more info"]') ||
            document.querySelector('button[aria-label="Turn off camera"]') ||
            document.querySelector('button[aria-label="Turn on camera"]') 
        )?.click()
        """
        return await self.browser.run_js(script)

    async def send_reaction(self, reactions: Reaction_T):
        emoji = ReactionMap.get(reactions, "__no__emoji__")
        script = """
            // toggle emoji palet
            document.querySelector('button[aria-label="Send a reaction"][aria-pressed="false"]')?.click();
            // use timeout to reduce the emoji  clicking event
            // as meet has delay/animation for the emoji pallet
            setTimeout(()=>{
                document.querySelector('button[aria-label="{emoji}"]')?.click();
                // toggle emoji palet
                document.querySelector('button[aria-label="Send a reaction"][aria-pressed="true"]')?.click();
            },300);
        """.replace(
            "{emoji}", emoji
        )
        return await self.browser.run_js(script)

    async def toggle_captions(self):
        script = """
        (
            document.querySelector('button[aria-label="Turn on captions"]') ||
            document.querySelector('button[aria-label="Turn off captions"]')
        )?.click();
        """
        return await self.browser.run_js(script)

    @deprecated(
        "This function servers no good purpose. As it only can toggle the select screen popup."
    )
    async def share_screen(self):
        script = """
        document.querySelector('button[aria-label="Share screen"]')?.click();
        """
        return await self.browser.run_js(script)

    async def get_peoples(self):
        await self.browser.run_js((MY_DIR / "get_people.js").read_text())
        return await self.browser.run_js("window.__participants")

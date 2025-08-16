import asyncio
from json import loads
from typing import Literal

from typing_extensions import deprecated

from meetbot.browser import BrowserController
from meetbot.exception import GetPeopleException
from meetbot.type_hints import Reaction_T
from meetbot.utils import load_js

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

    async def toggle_hand_raise(self) -> Literal["hand raised", "hand lowered"]:
        script = """
        button1 = document.querySelector('button[aria-label="Raise hand (Ctrl + alt + h)"]');
        button2 = document.querySelector('button[aria-label="Lower hand (Ctrl + alt + h)"]');
        
        (button1 || button2)?.click();
        state = button1?'hand raised':'hand lowered';
        state;
        """
        return await self.browser.run_js(script)

    async def toggle_mic(self) -> Literal["mic off", "mic on"]:
        script = """
        button1 =  document.querySelector('button[aria-label="Turn off microphone"]');
        button2 =  document.querySelector('button[aria-label="Turn on microphone"]');
        (button1 || button2)?.click();
        state = button1?'mic off':'mic on';
        state;
        """
        return await self.browser.run_js(script)

    async def toggle_camera(self) -> Literal["camera error", "camera off", "camera on"]:
        script = """
        button1 = document.querySelector('button[aria-label="Camera problem. Show more info"]'); 
        button2 = document.querySelector('button[aria-label="Turn off camera"]');
        button3 = document.querySelector('button[aria-label="Turn on camera"]');
        (button1 || button2 || button3)?.click();
        state = button1?'camera error':(button2?'camera off':'camera on');
        state;
        """
        return await self.browser.run_js(script)

    async def send_reaction(self, reactions: Reaction_T) -> bool:
        emoji = ReactionMap.get(reactions, "__no__emoji__")
        script = """
            // toggle emoji palet
            document.querySelector('button[aria-label="Send a reaction"][aria-pressed="false"]')?.click();
            // use timeout to reduce the emoji  clicking event
            // as meet has delay/animation for the emoji pallet
            is_success = false;
            _ = setTimeout(()=>{
                button = document.querySelector('button[aria-label="{emoji}"]')
                button?.click();
                is_success = `${button!=null}`;
                // toggle emoji palet
                window.__emoji_is_success = is_success;
                document.querySelector('button[aria-label="Send a reaction"][aria-pressed="true"]')?.click();
            },300);
        """.replace(
            "{emoji}", emoji
        )
        await self.browser.run_js(script)
        await asyncio.sleep(0.4)
        return await self.browser.run_js("window.__emoji_is_success") == "true"

    async def toggle_captions(self) -> Literal["caption on", "caption off"]:
        script = """
        button1 = document.querySelector('button[aria-label="Turn on captions"]');
        button2 = document.querySelector('button[aria-label="Turn off captions"]');
        (button1 || button2)?.click();
        state = button1?'caption on':'caption off';
        state;
        """
        return await self.browser.run_js(script)

    @deprecated(
        "This function servers no good purpose. As it only can toggle the select screen popup."
    )
    async def share_screen(self) -> Literal["screen share", "screen share failed"]:
        script = """
        button = document.querySelector('button[aria-label="Share screen"]')
        button?.click();
        state = button?'screen share':'screen share failed';
        state;
        """
        return await self.browser.run_js(script)

    async def get_peoples(self) -> list[str]:
        try:
            script = load_js("get_people.js")
            await self.browser.run_js(script)
            await asyncio.sleep(0.1)
            response = await self.browser.run_js("window.__participants")
            if not response:
                return []
            return loads(response)
        except FileNotFoundError as f:
            raise GetPeopleException("Failed to load 'get_people.js'.\n\t=>\t" + str(f))

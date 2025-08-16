from base64 import b64encode
from json import loads
from pathlib import Path

from meetbot.exception import ChatObserverScriptNotFound
from meetbot.type_hints import ChatResponse

from .browser import BrowserController

MY_DIR = Path(__file__).parent


class ChatManager:
    chat_messages_history: dict[str, ChatResponse] = {}

    def __init__(self, browser: BrowserController):
        self.browser = browser

    async def init_chat_observer(self):
        is_injected = await self.browser.run_js("window.__injected")
        if is_injected == "true":
            print("already injected so skipping")
            return
        observer_script = MY_DIR / "chat_observer.js"
        if not observer_script.exists():
            raise ChatObserverScriptNotFound(
                f"Write your observer script at {observer_script}"
            )
        await self.browser.run_js("window.__injected=true;")
        return await self.browser.run_js(observer_script.read_text())

    def get_messages(self) -> list[ChatResponse]:
        return [i for i in self.chat_messages_history.values()]

    async def get_message(self) -> ChatResponse | None:
        response = await self.browser.run_js("window.__new_message") or "{}"
        mesage_dict = loads(response)
        if not isinstance(mesage_dict, dict):
            return None
        _id = mesage_dict.get("id")
        user = mesage_dict.get("user")
        content = mesage_dict.get("content")
        if _id and user and content and _id not in self.chat_messages_history:
            self.chat_messages_history[_id] = ChatResponse(
                user=user,
                content=content,
                id=_id,
            )
            return self.chat_messages_history[_id]
        return None

    async def send_message(self, msg: str) -> None:
        chat_send_script = MY_DIR / "chat_sender.js"
        await self.browser.run_js(
            chat_send_script.read_text().replace(
                "{{message}}", b64encode(msg.encode()).decode()
            )
        )

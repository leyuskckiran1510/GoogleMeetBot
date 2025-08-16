from base64 import b64encode
from json import loads

from meetbot.exception import ChatMessageSendException, ChatObserverScriptNotFound
from meetbot.type_hints import ChatResponse
from meetbot.utils import load_js

from .browser import BrowserController


class ChatManager:
    chat_messages_history: dict[str, ChatResponse] = {}

    def __init__(self, browser: BrowserController):
        self.browser = browser

    async def init_chat_observer(self):
        is_injected = await self.browser.run_js("window.__injected")
        if is_injected == "true":
            print("already injected so skipping")
            return
        try:
            script = load_js("chat_observer.js")
            await self.browser.run_js("window.__injected=true;")
            return await self.browser.run_js(script)
        except FileNotFoundError as f:
            raise ChatObserverScriptNotFound(
                f"Write your observer script at 'chat_observer.js'.\n\t=>\t" + str(f)
            )

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
        try:
            script = load_js("chat_sender.js")
            await self.browser.run_js(
                script.replace("{{message}}", b64encode(msg.encode()).decode())
            )
        except FileNotFoundError as f:
            raise ChatMessageSendException(
                "Failed to load 'chat_sender.js'.\n\t=>\t" + str(f)
            )
        except Exception:
            raise ChatMessageSendException("Error while sending mesage to")

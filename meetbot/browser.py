import asyncio
import json

import httpx
import websockets

from meetbot.exception import BrowserException, JsSyntaxError, TabNotConnectedException
from meetbot.type_hints import RuntimeDomainMethods_T


class BrowserController:
    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 9222,
        poll_interval: float = 2.0,
    ):
        self.host = host
        self.port = port
        self.poll_interval = poll_interval
        self.ws = None
        self.msg_id = 0

    async def connect(self):
        while True:
            try:
                tabs = httpx.get(f"http://{self.host}:{self.port}/json").json()
                meet_tabs = [t for t in tabs if "meet.google.com" in t.get("url", "")]
                if meet_tabs:
                    ws_url = meet_tabs[0]["webSocketDebuggerUrl"]
                    self.ws = await websockets.connect(ws_url)
                    print(f"Connected to Meet tab: {meet_tabs[0]['url']}")
                    return
            except Exception as e:
                raise BrowserException(f"Error while scanning tabs: {e}")

            print("No Meet tab found. Retrying...")
            await asyncio.sleep(self.poll_interval)

    async def send_cmd(
        self,
        method: RuntimeDomainMethods_T,
        params: dict[str, str] = {},
    ):
        if not self.ws:
            raise TabNotConnectedException("Not connected to a tab.")

        self.msg_id += 1
        msg = {"id": self.msg_id, "method": method, "params": params}
        await self.ws.send(json.dumps(msg))

        while True:
            response = json.loads(await self.ws.recv())
            if response.get("id") == self.msg_id:
                print(response)
                return response

    async def run_js(self, script: str):
        result = await self.send_cmd("Runtime.evaluate", {"expression": script})
        result = result.get("result", {}).get("result", {})
        if result.get("subtype") == "error":
            raise JsSyntaxError(
                f"While executing:\t{script}\n\nError:{result.get('description')}"
            )
        else:
            return result.get("value")

from typing import Literal

from pydantic import BaseModel

# https://chromedevtools.github.io/devtools-protocol/tot/Runtime/
RuntimeDomainMethods_T = Literal[
    "Runtime.addBinding",
    "Runtime.awaitPromise",
    "Runtime.callFunctionOn",
    "Runtime.compileScript",
    "Runtime.disable",
    "Runtime.discardConsoleEntries",
    "Runtime.enable",
    "Runtime.evaluate",
    "Runtime.getProperties",
    "Runtime.globalLexicalScopeNames",
    "Runtime.queryObjects",
    "Runtime.releaseObject",
    "Runtime.releaseObjectGroup",
    "Runtime.removeBinding",
    "Runtime.runIfWaitingForDebugger",
    "Runtime.runScript",
    "Runtime.setAsyncCallStackDepth",
    "Runtime.getExceptionDetails Experimental",
    "Runtime.getHeapUsage Experimental",
    "Runtime.getIsolateId Experimental",
    "Runtime.setCustomObjectFormatterEnabled Experimental",
    "Runtime.setMaxCallStackSizeToCapture Experimental",
    "Runtime.terminateExecution Experimental",
]

Reaction_T = Literal[
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


class ChatResponse(BaseModel):
    user: str | None
    content: str | None
    id: str | None

    def __repr__(self) -> str:
        return f"[{self.id}]{self.user:20s}: {self.content}"

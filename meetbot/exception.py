class ChatException(Exception):
    pass


class ChatObserverScriptNotFound(ChatException):
    pass


class ChatMessageSendException(ChatException):
    pass


class BrowserException(Exception):
    pass


class TabNotConnectedException(BrowserException):
    pass


class JsSyntaxError(BrowserException):
    pass


class InteractionException(Exception):
    pass


class GetPeopleException(InteractionException):
    pass

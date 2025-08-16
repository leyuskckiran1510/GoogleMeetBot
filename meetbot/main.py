import asyncio

from meetbot.browser import BrowserController
from meetbot.chat import ChatManager
from meetbot.interact import Interact


async def let_other_control():
    browser = BrowserController()
    await browser.connect()

    chat = ChatManager(browser)
    interactio = Interact(browser)
    #
    #          "heart": "💖",
    #         "thumbs_up": "👍",
    #         "tada": "🎉",
    #         "clap": "👏",
    #         "joy": "😂",
    #         "surprised": "😮",
    #         "cry": "😢",
    #         "thinking": "🤔",
    #         "thumbs_down": "👎",
    commands = {
        "mute": interactio.toggle_mic,
        "cam": interactio.toggle_camera,
        "cry": lambda: interactio.send_reaction("cry"),
        "like": lambda: interactio.send_reaction("thumbs_up"),
        "dislike": lambda: interactio.send_reaction("thumbs_down"),
        "love": lambda: interactio.send_reaction("heart"),
        "heart": lambda: interactio.send_reaction("heart"),
        "happy": lambda: interactio.send_reaction("joy"),
        "joy": lambda: interactio.send_reaction("joy"),
        "tada": lambda: interactio.send_reaction("tada"),
        "celebrate": lambda: interactio.send_reaction("tada"),
        "wow": lambda: interactio.send_reaction("surprised"),
        "surprised": lambda: interactio.send_reaction("surprised"),
    }
    await chat.init_chat_observer()
    print("Meet bot running... Press Ctrl+C to exit.")
    while True:
        msgs = await chat.get_message()
        if msgs:
            if msgs.user != "You":
                print(msgs)
                if msgs.content in commands:
                    await commands[msgs.content]()
        await asyncio.sleep(0.01)


async def basic_interaction() -> None:
    browser = BrowserController()
    await browser.connect()

    interactio = Interact(browser)
    print(await interactio.get_peoples())
    return
    commands = {
        "mute": interactio.toggle_mic,
        "cam": interactio.toggle_camera,
        "hand_raise": interactio.toggle_hand_raise,
        "cap": interactio.toggle_captions,
    }
    reactions = {
        "cry": lambda: interactio.send_reaction("cry"),
        "like": lambda: interactio.send_reaction("thumbs_up"),
        "dislike": lambda: interactio.send_reaction("thumbs_down"),
        "love": lambda: interactio.send_reaction("heart"),
        "heart": lambda: interactio.send_reaction("heart"),
        "happy": lambda: interactio.send_reaction("joy"),
        "joy": lambda: interactio.send_reaction("joy"),
        "tada": lambda: interactio.send_reaction("tada"),
        "celebrate": lambda: interactio.send_reaction("tada"),
        "wow": lambda: interactio.send_reaction("surprised"),
        "surprised": lambda: interactio.send_reaction("surprised"),
    }
    for name, func in commands.items():
        print(f"Executing... {name}")
        print(await func())
        await asyncio.sleep(1)
        print("reverting toogles if present")
        print(await func())
        print("Done.")
        await asyncio.sleep(1)

    for name, func in reactions.items():
        print(f"Reacting... {name}")
        print("Success: ", await func())
        print("Done.")
        await asyncio.sleep(1)


async def messages_test():
    browser = BrowserController()
    await browser.connect()
    chat = ChatManager(browser)
    await chat.init_chat_observer()
    print("Meet bot running... Press Ctrl+C to exit.")
    while True:
        msgs = await chat.get_message()
        if msgs:
            print(msgs)
            if msgs.user != "You":
                await chat.send_message(input("enter the reply"))
        await asyncio.sleep(0.01)


async def main():
    # await let_other_control()
    # await messages_test()
    await basic_interaction()


if __name__ == "__main__":
    asyncio.run(main())

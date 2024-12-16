import importlib
import sys

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from SprotifyMusic import HELPABLE, LOGGER, app, userbot
from SprotifyMusic.core.call import Sprotify
from SprotifyMusic.plugins import ALL_MODULES
from SprotifyMusic.utils.cache.cache_manager import CacheManager
from SprotifyMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

cache_manager = CacheManager(max_size=100, ttl=3600)


async def init():
    if len(config.STRING_SESSIONS) == 0:
        LOGGER("SprotifyMusic").error(
            "No Assistant Clients Vars Defined!.. Exiting Process."
        )
        return
    if not config.SPOTIFY_CLIENT_ID and not config.SPOTIFY_CLIENT_SECRET:
        LOGGER("SprotifyMusic").warning(
            "No Spotify Vars defined. Your bot won't be able to play spotify queries."
        )
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception:
        pass
    await app.start()

    for all_module in ALL_MODULES:
        imported_module = importlib.import_module(all_module)

        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                HELPABLE[imported_module.__MODULE__.lower()] = imported_module
    LOGGER("SprotifyMusic.plugins").info("Successfully Imported All Modules ")
    await userbot.start()
    await Sprotify.start()
    LOGGER("SprotifyMusic").info("Assistant Started Sucessfully")
    try:
        await Sprotify.stream_call(
            "http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4"
        )

    except NoActiveGroupCall:
        LOGGER("SprotifyMusic").error(
            "Please ensure the voice call in your log group is active."
        )
        sys.exit()

    await Sprotify.decorators()
    LOGGER("SprotifyMusic").info("SprotifyMusic Started Successfully")

    chat = await app.get_chat(config.AI_GROUP_ID)

    await idle()
    await app.stop()
    await userbot.stop()


if __name__ == "__main__":
    app.run(init())
    LOGGER("SprotifyMusic").info("Stopping SprotifyMusic! GoodBye")

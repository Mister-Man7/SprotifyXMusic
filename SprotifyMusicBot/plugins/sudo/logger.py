from pyrogram import filters, Client
from pyrogram.types import Message

import config
from SprotifyMusic import app
from SprotifyMusic.misc import SUDOERS
from SprotifyMusic.utils.database import add_off, add_on
from SprotifyMusic.utils.decorators.language import language
from strings import get_command

LOGGER_COMMAND = get_command("LOGGER_COMMAND")


@app.on_message(filters.command(LOGGER_COMMAND) & SUDOERS)
@language
async def logger(_client: Client, message: Message, _):
    usage = _["log_1"]
    if len(message.command) != 2:
        return await message.reply_text(usage)
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        await add_on(config.LOG)
        await message.reply_text(_["log_2"])
    elif state == "disable":
        await add_off(config.LOG)
        await message.reply_text(_["log_3"])
    else:
        await message.reply_text(usage)

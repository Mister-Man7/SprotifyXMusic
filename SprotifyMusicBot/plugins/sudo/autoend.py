from pyrogram import filters

from SprotifyMusic import app
from SprotifyMusic.misc import SUDOERS
from SprotifyMusic.utils.database import autoend_off, autoend_on
from strings import get_command

AUTOEND_COMMAND = get_command("AUTOEND_COMMAND")


@app.on_message(filters.command(AUTOEND_COMMAND) & SUDOERS)
async def auto_end_stream(client, message):
    usage = "**Uso:**\n\n/autoend [enable|disable]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        await autoend_on()
        await message.reply_text(
            "🔚 Auto End Activated.\n\nThe bot will automatically come out of the voice chat after 30 seconds if no one is listening to the song, with a warning message."
        )
    elif state == "disable":
        await autoend_off()
        await message.reply_text("🔕 Self-end deactivated")
    else:
        await message.reply_text(usage)

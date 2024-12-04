from pyrogram import filters, Client
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

import config
from SprotifyMusic import app
from config import PREFIXES
from strings import get_command

PRIVACY_COMMAND = get_command("PRIVACY_COMMAND")

TEXT = f"""
🔒 **Privacy Policy of {app.mention}!**

Your privacy is important to us.To learn more about how we collect, use and protect your data, please review our privacy policy here: [Privacy Policy] ({config.privacy_link}).

If you have any questions or concern, feel free to contact our [Support team]({config.SUPPORT_GROUP}).
"""


@app.on_message(filters.command(PRIVACY_COMMAND, PREFIXES))
async def privacy(_client: Client, message: Message):
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("See privacy policy", url=config.PRIVACY_LINK)]]
    )
    await message.reply_text(
        TEXT,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )

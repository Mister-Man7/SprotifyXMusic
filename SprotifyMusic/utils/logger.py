from pyrogram.types import Message

from SprotifyMusic import app
from SprotifyMusic.utils.database import is_on_off
from config import LOG, LOG_GROUP_ID


async def play_logs(message: Message, streamtype: str):
    if await is_on_off(LOG):
        if message.chat.username:
            chatusername = f"@{message.chat.username}"
        else:
            chatusername = "🔒 Grupo Privado"

        logger_text = f"""
🎵 ** Reproduction Record - {app.mention} ** 🎵

📌 ** Chat ID: ** `{message.chat.id}`
🏷️ ** Chat Name: ** {message.chat.title}
🔗 ** Chat username: ** {chatusername}

👤 ** User ID: ** `{message.from_user.id}`
📛 ** Name: ** {message.from_user.mention}
📱 ** User Name: ** @{message.from_user.username}

🔍 ** Consultation: ** {message.text.split (None, 1) [1]}
🎧 ** Stream Type: ** {streamtype}"""

        if message.chat.id != LOG_GROUP_ID:
            try:
                await app.send_message(
                    chat_id=LOG_GROUP_ID,
                    text=logger_text,
                    disable_web_page_preview=True,
                )
            except Exception as e:
                print(e)
        return

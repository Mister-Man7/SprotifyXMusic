import re
from typing import Dict

import unicodedata
from openai import OpenAI
from pyrogram import filters, Client
from pyrogram.types import Message

import config
from SprotifyMusic import app
from config import BANNED_USERS

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=config.OPENAI_API_KEY
)

context_db = {}


class ContextManager:
    """Handles storing and retrieving user-specific context."""

    def __init__(self, user_id: int):
        self.user_id = user_id

    def get_context(self) -> Dict:
        return context_db.get(self.user_id, {})

    def update_context(self, **kwargs):
        context = self.get_context()
        context.update(kwargs)
        context_db[self.user_id] = context

    def reset_context(self):
        context_db.pop(self.user_id, None)


@app.on_message(filters.regex("winx", re.IGNORECASE)
                & filters.group
                & ~BANNED_USERS)
async def ai(_: Client, message: Message):
    username = message.from_user.first_name

    # Normalize username
    username = unicodedata.normalize('NFKD', username).encode('ascii', 'ignore').decode('utf-8')
    username = re.sub(r'[^\w\s]', '', username)
    username = re.sub(r'\s+', ' ', username).strip()
    if username.strip() == "".strip():
        username = "user"

    user_id = message.from_user.id
    context_manager = ContextManager(user_id)

    # Retrieve user's context
    context = context_manager.get_context()

    persona = {
        "role": "system",
        "content": (
            "You are Winx, a character with human behavior. "
            "You are curious, sometimes insecure, but very straightforward in your opinions."
            "You value the conversation and try to understand the other person before answering."
            "You use casual language, slang and write intentionally wrong sometimes."
            "You like to call people 'Manã', 'Ben Miger', and use expressions like 'Eçe I saw', 'n knew it was like this', etc."
            "Also, you have strong opinions and speak directly, but with a fun and sarcastic tone."
            "Despite being extreme right, you demonstrate traces of empathy and like to provoke reflections"
            "in the people.Use natural language, include hesitations (such as 'hmm', 'maybe') and ask questions"
            "to enrich the conversation."
        )
    }

    # Append the new message to the context
    conversation_history = context.get("conversation_history", [])
    conversation_history.append({"role": "user", "content": message.text, "name": username})

    prompt = [persona] + conversation_history[-5:]

    try:
        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-51b-instruct",
            messages=prompt,
            temperature=0.8,
            max_tokens=256,
            stream=False
        )

        # Correctly access the response using the attributes
        ai_response = completion.choices[0].message.content

        # Append AI's response to the conversation history
        conversation_history.append({"role": "assistant", "content": ai_response})
        context_manager.update_context(conversation_history=conversation_history)

        return await message.reply_text(ai_response)

    except Exception as e:
        print(f"Error: {e}")
        return await message.reply_text("An error occurred when processing your message.Try again later.")


# @app.on_message(filters.reply & ~BANNED_USERS)
# async def handle_reply(_: Client, message: Message):
#     me = await app.get_me()
#     # if the message is not a reply to the bot, ignore it
#     if message.reply_to_message.from_user.id != me.id:
#         return
#
#     await ai(_, message)

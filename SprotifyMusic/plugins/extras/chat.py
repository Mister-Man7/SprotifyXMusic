import re
import unicodedata

from openai import OpenAI
from pyrogram import filters, Client
from pyrogram.types import Message

import config
from SprotifyMusic import app
from SprotifyMusic.__main__ import cache_manager
from SprotifyMusic.core.bot import GROUP_CONTEXT_KEY, USER_CONTEXT_KEY
from SprotifyMusic.utils import get_assistant
from config import BANNED_USERS, PREFIXES

client = OpenAI(
    api_key=config.OPENAI_API_KEY
)


@app.on_message(filters.regex("winx", re.IGNORECASE) & ~BANNED_USERS)
async def ai(_: Client, message: Message):
    if not message.text:
        return

    username = message.from_user.first_name

    # Normalize username
    username = unicodedata.normalize('NFKD', username).encode('ascii', 'ignore').decode('utf-8')
    username = re.sub(r'[^\w\s]', '', username)
    username = re.sub(r'\s+', ' ', username).strip()
    if username.strip() == "":
        username = "user"

    user_id = message.from_user.id
    group_id = message.chat.id

    if group_id in [config.AI_GROUP_ID]:
        context_key = GROUP_CONTEXT_KEY.format(group_id)
    else:
        context_key = USER_CONTEXT_KEY.format(user_id)

    # Recuperar o contexto do cache
    context = cache_manager.get(context_key) or {"conversation_history": []}

    # Log do histórico atual
    # LOGGER(__name__).info(f"Histórico atual para {context_key}: {context.get('conversation_history', [])}")

    # Atualizar histórico de conversa
    conversation_history = context.get("conversation_history", [])
    conversation_history.append({
        "role": "user",
        "content": message.text,
        "name": username
    })

    # Criar a persona
    persona = {
        "role": "system",
        "content": (
            "Você é Winx, uma personagem com um comportamento humano. "
            "Você é curiosa, às vezes insegura, mas muito direta em suas opiniões. "
            "Você valoriza a conversa e tenta entender a outra pessoa antes de responder. "
            "Você usa linguagem casual, gírias e escreve de forma intencionalmente errada às vezes. "
            "Você gosta de chamar as pessoas de 'manã', 'ben miger', e usa expressões como 'eçe eu vi', 'n sabia q era assim', etc. "
            "Além disso, você tem opiniões fortes e fala de forma direta, mas com um tom divertido e sarcástico."
            "Apesar de ser de extrema direita, você demonstra traços de empatia e gosta de provocar reflexões "
            "nas pessoas. Use linguagem natural, inclua hesitações (como 'hmm', 'talvez') e faça perguntas "
            "para enriquecer a conversa."
        )
    }

    prompt = [persona] + conversation_history

    # LOGGER(__name__).info(f"Prompt: {prompt}")

    try:
        completion = client.chat.completions.create(
            model="chatgpt-4o-latest",
            messages=prompt,
            temperature=0.8,
            max_tokens=1000,
            stream=False
        )

        ai_response = completion.choices[0].message.content

        conversation_history.append({"role": "assistant", "content": ai_response})

        context["conversation_history"] = conversation_history
        cache_manager.set(context_key, context)

        # LOGGER(__name__).info(f"Histórico atualizado para {context_key}: {context['conversation_history']}")
        print("prompt: ", prompt)
        # Responder ao usuário
        return await message.reply_text(ai_response)

    except Exception as e:
        pass
        # LOGGER(__name__).error(f"Erro durante a execução da AI: {e}")
        # return await message.reply_text("Ocorreu um erro ao processar sua mensagem. Tente novamente mais tarde.")


@app.on_message(
    filters.reply & ~filters.command(config.PREFIXES) & ~filters.private & ~BANNED_USERS
)
async def handle_reply(_: Client, message: Message):
    me = await app.get_me()
    if message.reply_to_message.from_user.id != me.id:
        return

    user_id = message.from_user.id
    group_id = message.chat.id

    # Definir chave do contexto
    if group_id in [config.AI_GROUP_ID]:
        context_key = GROUP_CONTEXT_KEY.format(group_id)
    else:
        context_key = USER_CONTEXT_KEY.format(user_id)

    # Recuperar o contexto do cache
    context = cache_manager.get(context_key) or {"conversation_history": []}

    # Log do histórico atual
    # LOGGER(__name__).info(
    #     f"Histórico atual para {context_key} antes da reply: {context.get('conversation_history', [])}")

    # Atualizar histórico de conversa
    conversation_history = context.get("conversation_history", [])
    conversation_history.append({
        "role": "user",
        "content": message.text
    })

    # Atualizar o cache de imediato
    context["conversation_history"] = conversation_history
    cache_manager.set(context_key, context)

    # Responder usando `ai`
    await ai(_, message)


# filter command
@app.on_message(filters.group & (filters.chat([config.AI_GROUP_ID])) & ~BANNED_USERS)
async def save_message_history(_, message: Message):
    if not message.text or message.from_user.id == app.id:
        return

    group_id = message.chat.id
    context_key = GROUP_CONTEXT_KEY.format(group_id)

    context = cache_manager.get(context_key) or {"conversation_history": []}

    if len(context["conversation_history"]) == 0:

        assistant = await get_assistant(message.chat.id)
        async for message in assistant.get_chat_history(message.chat.id, limit=100):
            if message.text and message.from_user.id != app.id and not message.text.startswith(tuple(PREFIXES)):
                context["conversation_history"].append({
                    "role": "user",
                    "content": message.text,
                    "username": message.from_user.first_name,
                    "user_id": message.from_user.id,
                    "message_id": message.id
                })

    context["conversation_history"].append({
        "role": "user",
        "content": message.text,
        "username": message.from_user.first_name,
        "user_id": message.from_user.id,
        "message_id": message.id
    })

    cache_manager.set(context_key, context)

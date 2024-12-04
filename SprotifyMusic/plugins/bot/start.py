import asyncio
import time

from pyrogram import filters, Client
from pyrogram.enums import ChatType, ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch

import config
from SprotifyMusic import HELPABLE, app, Platform
from SprotifyMusic.misc import SUDOERS, _boot_
from SprotifyMusic.plugins.play.playlist import del_plist_msg
from SprotifyMusic.plugins.sudo.sudoers import sudoers_list
from SprotifyMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_assistant,
    get_lang,
    get_userss,
    is_on_off,
    is_served_private_chat,
)
from SprotifyMusic.utils.decorators.language import language_start
from SprotifyMusic.utils.formatters import get_readable_time
from SprotifyMusic.utils.functions import MARKDOWN, WELCOMEHELP
from SprotifyMusic.utils.inline import private_panel, start_pannel
from config import BANNED_USERS, START_IMG_URL
from config.config import OWNER_ID, PREFIXES
from strings import command, get_command, get_string
from .help import paginate_modules

loop = asyncio.get_running_loop()

START_COMMAND = get_command("START_COMMAND")


@app.on_message(filters.command(START_COMMAND, PREFIXES) & filters.private & ~BANNED_USERS)
@language_start
async def start_comm(client: Client, message: Message, _):
    chat_id = message.chat.id
    await add_served_user(message.from_user.id)
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, close=True))
            if config.START_IMG_URL:
                return await message.reply_photo(
                    photo=START_IMG_URL,
                    caption=_["help_1"],
                    reply_markup=keyboard,
                )
            else:
                return await message.reply_text(
                    text=_["help_1"],
                    reply_markup=keyboard,
                )
        if name[0:4] == "song":
            await message.reply_text(_["song_2"])
            return
        if name == "mkdwn_help":
            await message.reply(
                MARKDOWN,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
        if name == "greetings":
            await message.reply(
                WELCOMEHELP,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
        if name[0:3] == "sta":
            m = await message.reply_text("🔎 Seeking your personal statistics!")
            stats = await get_userss(message.from_user.id)
            tot = len(stats)
            if not stats:
                await asyncio.sleep(1)
                return await m.edit(_["ustats_1"])

            def get_stats():
                msg = ""
                limit = 0
                results = {}
                for i in stats:
                    top_list = stats[i]["spot"]
                    results[str(i)] = top_list
                    list_arranged = dict(
                        sorted(
                            results.items(),
                            key=lambda item: item[1],
                            reverse=True,
                        )
                    )
                if not results:
                    return m.edit(_["ustats_1"])
                tota = 0
                videoid = None
                for vidid, count in list_arranged.items():
                    tota += count
                    if limit == 10:
                        continue
                    if limit == 0:
                        videoid = vidid
                    limit += 1
                    details = stats.get(vidid)
                    title = (details["title"][:35]).title()
                    if vidid == "telegram":
                        msg += f"🔗[Telegram files and audios]({config.SUPPORT_GROUP}) ** touched {count} times**\n\n"
                    else:
                        msg += f"🔗 [{title}](https://www.youtube.com/watch?v={vidid}) ** touched {count} times**\n\n"
                msg = _["ustats_2"].format(tot, tota, limit) + msg
                return videoid, msg

            try:
                videoid, msg = await loop.run_in_executor(None, get_stats)
            except Exception as e:
                print(e)
                return
            thumbnail = await Platform.youtube.thumbnail(videoid, True)
            await m.delete()
            await message.reply_photo(photo=thumbnail, caption=msg)
            return
        if name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
            await asyncio.sleep(1)
            if await is_on_off(config.LOG):
                sender_id = message.from_user.id
                sender_mention = message.from_user.mention
                sender_name = message.from_user.first_name
                return await app.send_message(
                    config.LOG_GROUP_ID,
                    f"👤 {message.from_user.mention} has just started the bot to check the <code> Sudo list </code>\n\n🆔 **User ID:** {sender_id}\n📛 **Username:** {sender_name}",
                )
            return
        if name[0:3] == "lyr":
            query = (str(name)).replace("lyrics_", "", 1)
            lyrical = config.lyrical
            lyrics = lyrical.get(query)
            if lyrics:
                await Platform.telegram.send_split_text(message, lyrics)
                return
            else:
                await message.reply_text("Failed to get the lyrics.")
                return
        if name[0:3] == "del":
            await del_plist_msg(client=client, message=message, _=_)
            await asyncio.sleep(1)
        if name[0:3] == "inf":
            m = await message.reply_text("🔎 Seeking information!")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
                searched_text = f"""
🔍__**Video range information**__

❇️**Title:** {title}

⏳**Duration:** {duration} Minutos
👀**Views:** `{views}`
⏰**Published in:** {published}
🎥**Channel name:** {channel}
📎**Link to Channel:** [Visite aqui]({channellink})
🔗**Link to Vídeo:** [Clique aqui]({link})
"""

            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="🎥 Go To", url=f"{link}"),
                        InlineKeyboardButton(text="🔄 Close", callback_data="close"),
                    ],
                ]
            )
            await m.delete()
            await app.send_photo(
                message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=key,
            )
            await asyncio.sleep(1)
            if await is_on_off(config.LOG):
                sender_id = message.from_user.id
                sender_name = message.from_user.first_name
                return await app.send_message(
                    config.LOG_GROUP_ID,
                    f"👤 {message.from_user.mention} has just started the bot to check the <code> video information </code>\n\n🆔 **User ID:** {sender_id}\n📛 **Username:** {sender_name}",
                )
    else:
        try:
            await app.resolve_peer(OWNER_ID[0])
            OWNER = OWNER_ID[0]
        except Exception:
            OWNER = None
        out = private_panel(_, app.username, OWNER)
        if config.START_IMG_URL:
            try:
                await message.reply_photo(
                    photo=config.START_IMG_URL,
                    caption=_["start_1"].format(app.mention),
                    reply_markup=InlineKeyboardMarkup(out),
                )
            except Exception:
                await message.reply_text(
                    text=_["start_1"].format(app.mention),
                    reply_markup=InlineKeyboardMarkup(out),
                )
        else:
            await message.reply_text(
                text=_["start_1"].format(app.mention),
                reply_markup=InlineKeyboardMarkup(out),
            )
        if await is_on_off(config.LOG):
            sender_id = message.from_user.id
            sender_name = message.from_user.first_name
            return await app.send_message(
                config.LOG_GROUP_ID,
                f"👤 {message.from_user.mention} started the bot. \n\n🆔 **User ID:** {sender_id}\n📛 **Username:** {sender_name}",
            )


@app.on_message(filters.command(START_COMMAND, PREFIXES) & filters.group & ~BANNED_USERS)
@language_start
async def testbot(_client: Client, message: Message, _):
    uptime = int(time.time() - _boot_)
    chat_id = message.chat.id
    await message.reply_text(_["start_7"].format(get_readable_time(uptime)))

    return await add_served_chat(message.chat.id)


@app.on_message(filters.new_chat_members, group=-1)
async def welcome(_client: Client, message: Message):
    chat_id = message.chat.id
    if config.PRIVATE_BOT_MODE == str(True):
        if not await is_served_private_chat(message.chat.id):
            await message.reply_text(
                "**The private mode of this bot has been activated, only my owner can use it.If you want to use this bot on your chat, ask my owner to authorize your chat.**"
            )
            return await app.leave_chat(message.chat.id)
    else:
        await add_served_chat(chat_id)
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if member.id == app.id:
                chat_type = message.chat.type
                if chat_type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_5"])
                    return await app.leave_chat(message.chat.id)
                if chat_id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_6"].format(
                            f"https://t.me/{app.username}?start=sudolist"
                        )
                    )
                    return await app.leave_chat(chat_id)
                userbot = await get_assistant(message.chat.id)
                out = start_pannel(_)
                await message.reply_text(
                    _["start_2"].format(
                        app.mention,
                        userbot.username,
                        userbot.id,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
            if member.id in config.OWNER_ID:
                return await message.reply_text(
                    _["start_3"].format(app.mention, member.mention)
                )
            if member.id in SUDOERS:
                return await message.reply_text(
                    _["start_4"].format(app.mention, member.mention)
                )
            return
        except Exception:

            return


__MODULE__ = "Bot"
__HELP__ = f"""
<b>✦ All Command should working on PM.</b>

<b>★ {command("STATS_COMMAND")}</b> - Get the global statistics of the 10 most played tracks, 10 main Bot users, 10 main chats in the bot, 10 most played on a chat, etc.

<b>★ {command("SUDOUSERS_COMMAND")}</b> - Verifique os usuários Sudo do bot.

<b>★ {command("LYRICS_COMMAND")} [Music Name]</b> - Search lyrics for a specific song on the web.

<b>★ {command("SONG_COMMAND")} [Track name] or [Link YT]</b> - Download any YouTube track in MP3 or MP4 formats.

<b>★ {command("QUEUE_COMMAND")}</b> - Check the list of music in line.

    <u><b>⚡️Private bot:</b></u>

<b>✧ {command("AUTHORIZE_COMMAND")} [ID_DO_CHAT]</b> - Allow a chat use your bot.

<b>✧ {command("UNAUTHORIZE_COMMAND")} [ID_DO_CHAT]</b> - Block a chat to use your bot.

<b>✧ {command("AUTHORIZED_COMMAND")}</b> - Check all allowed chats of your bot.
"""

import random

from pyrogram import filters, Client
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InputMediaPhoto

import config
from SprotifyXMusic import app, Platform
from SprotifyXMusic.core.call import Winx
from SprotifyXMusic.misc import SUDOERS, db
from SprotifyXMusic.utils import time_to_seconds
from SprotifyXMusic.utils.channelplay import get_channeplay_cb
from SprotifyXMusic.utils.database import (
    is_active_chat,
    is_music_playing,
    is_muted,
    is_nonadmin_chat,
    music_off,
    music_on,
    mute_off,
    mute_on,
    set_loop,
)
from SprotifyXMusic.utils.decorators import actual_admin_cb
from SprotifyXMusic.utils.decorators.language import language_cb
from SprotifyXMusic.utils.formatters import seconds_to_min
from SprotifyXMusic.utils.inline.play import (
    livestream_markup,
    panel_markup_1,
    panel_markup_2,
    panel_markup_3,
    slider_markup,
    stream_markup,
    telegram_markup,
)
from SprotifyXMusic.utils.stream.autoclear import auto_clean
from SprotifyXMusic.utils.stream.stream import stream
from SprotifyXMusic.utils.thumbnails import gen_thumb
from config import (
    BANNED_USERS,
    SOUNCLOUD_IMG_URL,
    STREAM_IMG_URL,
    SUPPORT_GROUP,
    TELEGRAM_AUDIO_URL,
    TELEGRAM_VIDEO_URL,
    adminlist,
    lyrical,
)
from strings import command

wrong = {}
downvote = {}
downvoters = {}


@app.on_callback_query(filters.regex("PanelMarkup") & ~BANNED_USERS)
@language_cb
async def markup_panel(_client: Client, callback_query: CallbackQuery, _):
    await callback_query.answer()
    callback_data = callback_query.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    videoid, chat_id = callback_request.split("|")
    chat_id = callback_query.message.chat.id
    buttons = panel_markup_1(_, videoid, chat_id)
    try:
        await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception:
        return
    if chat_id not in wrong:
        wrong[chat_id] = {}
    wrong[chat_id][callback_query.message.id] = False


@app.on_callback_query(filters.regex("MainMarkup") & ~BANNED_USERS)
@language_cb
async def del_back_playlist(_client: Client, callback_query: CallbackQuery, _):
    await callback_query.answer()
    callback_data = callback_query.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    videoid, chat_id = callback_request.split("|")
    if videoid == str(None):
        buttons = telegram_markup(_, chat_id)
    else:
        buttons = stream_markup(_, videoid, chat_id)
    chat_id = callback_query.message.chat.id
    try:
        await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception:
        return
    if chat_id not in wrong:
        wrong[chat_id] = {}
    wrong[chat_id][callback_query.message.id] = True


@app.on_callback_query(filters.regex("Pages") & ~BANNED_USERS)
@language_cb
async def del_back_playlist(_client: Client, callback_query: CallbackQuery, _):
    await callback_query.answer()
    callback_data = callback_query.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    state, pages, videoid, chat = callback_request.split("|")
    chat_id = int(chat)
    pages = int(pages)
    if state == "Forw":
        if pages == 0:
            buttons = panel_markup_2(_, videoid, chat_id)
        if pages == 2:
            buttons = panel_markup_1(_, videoid, chat_id)
        if pages == 1:
            buttons = panel_markup_3(_, videoid, chat_id)
    if state == "Back":
        if pages == 2:
            buttons = panel_markup_2(_, videoid, chat_id)
        if pages == 1:
            buttons = panel_markup_1(_, videoid, chat_id)
        if pages == 0:
            buttons = panel_markup_3(_, videoid, chat_id)
    try:
        await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception:
        return


@app.on_callback_query(filters.regex("ADMIN") & ~BANNED_USERS)
@language_cb
async def main_markup_(_client: Client, callback_query: CallbackQuery, _):
    callback_data = callback_query.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    command, chat = callback_request.split("|")
    chat_id = int(chat)
    if not await is_active_chat(chat_id):
        return await callback_query.answer(_["general_6"], show_alert=True)
    mention = callback_query.from_user.mention
    is_non_admin = await is_nonadmin_chat(callback_query.message.chat.id)
    if not is_non_admin:
        if callback_query.from_user.id not in SUDOERS:
            admins = adminlist.get(callback_query.message.chat.id)
            if not admins:
                return await callback_query.answer(_["admin_18"], show_alert=True)
            else:
                if callback_query.from_user.id not in admins:
                    return await callback_query.answer(_["admin_19"], show_alert=True)
    if command == "Pause":
        if not await is_music_playing(chat_id):
            return await callback_query.answer(_["admin_1"], show_alert=True)
        await callback_query.answer()
        await music_off(chat_id)
        await Winx.pause_stream(chat_id)
        await callback_query.message.reply_text(
            _["admin_2"].format(mention), disable_web_page_preview=True
        )
    elif command == "Resume":
        if await is_music_playing(chat_id):
            return await callback_query.answer(_["admin_3"], show_alert=True)
        await callback_query.answer()
        await music_on(chat_id)
        await Winx.resume_stream(chat_id)
        await callback_query.message.reply_text(
            _["admin_4"].format(mention), disable_web_page_preview=True
        )
    elif command == "Stop" or command == "End":
        try:
            check = db.get(chat_id)
            if check[0].get("mystic"):
                await check[0].get("mystic").delete()
        except Exception:
            pass
        await callback_query.answer()
        await Winx.stop_stream(chat_id)
        await set_loop(chat_id, 0)
        await callback_query.message.reply_text(
            _["admin_9"].format(mention), disable_web_page_preview=True
        )
    elif command == "Mute":
        if await is_muted(chat_id):
            return await callback_query.answer(_["admin_5"], show_alert=True)
        await callback_query.answer()
        await mute_on(chat_id)
        await Winx.mute_stream(chat_id)
        await callback_query.message.reply_text(
            _["admin_6"].format(mention), disable_web_page_preview=True
        )
    elif command == "Unmute":
        if not await is_muted(chat_id):
            return await callback_query.answer(_["admin_7"], show_alert=True)
        await callback_query.answer()
        await mute_off(chat_id)
        await Winx.unmute_stream(chat_id)
        await callback_query.message.reply_text(
            _["admin_8"].format(mention), disable_web_page_preview=True
        )
    elif command == "Loop":
        await callback_query.answer()
        await set_loop(chat_id, 3)
        await callback_query.message.reply_text(_["admin_25"].format(mention, 3))

    elif command == "Shuffle":
        check = db.get(chat_id)
        if not check:
            return await callback_query.answer(_["admin_21"], show_alert=True)
        try:
            popped = check.pop(0)
        except Exception:
            return await callback_query.answer(_["admin_22"], show_alert=True)
        check = db.get(chat_id)
        if not check:
            check.insert(0, popped)
            return await callback_query.answer(_["admin_22"], show_alert=True)
        await callback_query.answer()
        random.shuffle(check)
        check.insert(0, popped)
        await callback_query.message.reply_text(
            _["admin_23"].format(mention), disable_web_page_preview=True
        )

    elif command == "Skip":
        check = db.get(chat_id)
        txt = f"» Track skipped by {mention} !"
        popped = None
        try:
            popped = check.pop(0)
            if popped:
                await auto_clean(popped)
            if not check:
                await callback_query.edit_message_text(
                    f"» Track skipped by  {mention} !"
                )
                await callback_query.message.reply_text(
                    _["admin_10"].format(mention), disable_web_page_preview=True
                )
                try:
                    return await Winx.stop_stream(chat_id)
                except Exception:
                    return
        except Exception:
            try:
                await callback_query.edit_message_text(
                    f"» Track skipped by  {mention} !"
                )
                await callback_query.message.reply_text(
                    _["admin_10"].format(mention), disable_web_page_preview=True
                )
                return await Winx.stop_stream(chat_id)
            except Exception:
                return
        await callback_query.answer()
        queued = check[0]["file"]
        title = (check[0]["title"]).title()
        user = check[0]["by"]
        streamtype = check[0]["streamtype"]
        videoid = check[0]["vidid"]
        duration_min = check[0]["dur"]
        status = True if str(streamtype) == "video" else None
        db[chat_id][0]["played"] = 0
        if "live_" in queued:
            n, link = await Platform.youtube.video(videoid, True)
            if n == 0:
                return await callback_query.message.reply_text(
                    _["admin_11"].format(title)
                )
            try:
                await Winx.skip_stream(chat_id, link, video=status)
            except Exception:
                return await callback_query.message.reply_text(_["call_7"])
            button = telegram_markup(_, chat_id)
            img = await gen_thumb(videoid)
            run = await callback_query.message.reply_photo(
                photo=img,
                caption=_["stream_1"].format(
                    user,
                    f"https://t.me/{app.username}?start=info_{videoid}",
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
            await callback_query.edit_message_text(txt)
        elif "vid_" in queued:
            mystic = await callback_query.message.reply_text(
                _["call_8"], disable_web_page_preview=True
            )
            try:
                file_path, direct = await Platform.youtube.download(
                    videoid,
                    mystic,
                    videoid=True,
                    video=status,
                )
            except Exception:
                return await mystic.edit_text(_["call_7"])
            try:
                await Winx.skip_stream(chat_id, file_path, video=status)
            except Exception:
                return await mystic.edit_text(_["call_7"])
            button = stream_markup(_, videoid, chat_id)
            img = await gen_thumb(videoid)
            run = await callback_query.message.reply_photo(
                photo=img,
                caption=_["stream_1"].format(
                    title[:27],
                    f"https://t.me/{app.username}?start=info_{videoid}",
                    duration_min,
                    user,
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"
            await callback_query.edit_message_text(txt)
            await mystic.delete()
        elif "index_" in queued:
            try:
                await Winx.skip_stream(chat_id, videoid, video=status)
            except Exception:
                return await callback_query.message.reply_text(_["call_7"])
            button = telegram_markup(_, chat_id)
            run = await callback_query.message.reply_photo(
                photo=STREAM_IMG_URL,
                caption=_["stream_2"].format(user),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
            await callback_query.edit_message_text(txt)
        else:
            try:
                await Winx.skip_stream(chat_id, queued, video=status)
            except Exception:
                return await callback_query.message.reply_text(_["call_7"])
            if videoid == "telegram":
                button = telegram_markup(_, chat_id)
                run = await callback_query.message.reply_photo(
                    photo=(
                        TELEGRAM_AUDIO_URL
                        if str(streamtype) == "audio"
                        else TELEGRAM_VIDEO_URL
                    ),
                    caption=_["stream_1"].format(
                        title, SUPPORT_GROUP, check[0]["dur"], user
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"
            elif videoid == "soundcloud":
                button = telegram_markup(_, chat_id)
                run = await callback_query.message.reply_photo(
                    photo=(
                        SOUNCLOUD_IMG_URL
                        if str(streamtype) == "audio"
                        else TELEGRAM_VIDEO_URL
                    ),
                    caption=_["stream_1"].format(
                        title, SUPPORT_GROUP, check[0]["dur"], user
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"
            elif "saavn" in videoid:
                button = telegram_markup(_, chat_id)
                run = await callback_query.message.reply_photo(
                    photo=check[0]["thumb"],
                    caption=_["stream_1"].format(
                        title, SUPPORT_GROUP, check[0]["dur"], user
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"

            else:
                button = stream_markup(_, videoid, chat_id)
                img = await gen_thumb(videoid)
                run = await callback_query.message.reply_photo(
                    photo=img,
                    caption=_["stream_1"].format(
                        title[:27],
                        f"https://t.me/{app.username}?start=info_{videoid}",
                        duration_min,
                        user,
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "stream"
            await callback_query.edit_message_text(txt)
    else:
        playing = db.get(chat_id)
        if not playing:
            return await callback_query.answer(_["queue_2"], show_alert=True)
        duration_seconds = int(playing[0]["seconds"])
        if duration_seconds == 0:
            return await callback_query.answer(_["admin_30"], show_alert=True)
        file_path = playing[0]["file"]
        if "index_" in file_path or "live_" in file_path:
            return await callback_query.answer(_["admin_30"], show_alert=True)
        duration_played = int(playing[0]["played"])
        if int(command) in [1, 2]:
            duration_to_skip = 10
        else:
            duration_to_skip = 30
        duration = playing[0]["dur"]
        if int(command) in [1, 3]:
            if (duration_played - duration_to_skip) <= 10:
                bet = seconds_to_min(duration_played)
                return await callback_query.answer(
                    f"Bot is unable to seek because duration exceeds.\n\nCurrently played:** {bet}** minutes out of **{duration}** minutes.",
                    show_alert=True,
                )
            to_seek = duration_played - duration_to_skip + 1
        else:
            if (duration_seconds - (duration_played + duration_to_skip)) <= 10:
                bet = seconds_to_min(duration_played)
                return await callback_query.answer(
                    f"Bot is unable to seek because duration exceeds.\n\nCurrently played:** {bet}** minutes out of **{duration}** minutes.",
                    show_alert=True,
                )
            to_seek = duration_played + duration_to_skip + 1
        await callback_query.answer()
        mystic = await callback_query.message.reply_text(_["admin_32"])
        if "vid_" in file_path:
            n, file_path = await Platform.youtube.video(playing[0]["vidid"], True)
            if n == 0:
                return await mystic.edit_text(_["admin_30"])
        try:
            await Winx.seek_stream(
                chat_id,
                file_path,
                seconds_to_min(to_seek),
                duration,
                playing[0]["streamtype"],
            )
        except Exception:
            return await mystic.edit_text(_["admin_34"])
        if int(command) in [1, 3]:
            db[chat_id][0]["played"] -= duration_to_skip
        else:
            db[chat_id][0]["played"] += duration_to_skip
        string = _["admin_33"].format(seconds_to_min(to_seek))
        await mystic.edit_text(f"{string}\n\nChanges Done by: {mention} !")


@app.on_callback_query(filters.regex("MusicStream") & ~BANNED_USERS)
@language_cb
async def play_music(_client: Client, callback_query: CallbackQuery, _):
    callback_data = callback_query.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    vidid, user_id, mode, cplay, fplay = callback_request.split("|")
    if callback_query.from_user.id != int(user_id):
        try:
            return await callback_query.answer(_["playcb_1"], show_alert=True)
        except Exception:
            return
    try:
        chat_id, channel = await get_channeplay_cb(_, cplay, callback_query)
    except Exception:
        return
    user_name = callback_query.from_user.first_name
    try:
        await callback_query.message.delete()
        await callback_query.answer()
    except Exception:
        pass
    mystic = await callback_query.message.reply_text(
        _["play_2"].format(channel) if channel else _["play_1"]
    )
    try:
        details, track_id = await Platform.youtube.track(vidid, True)
    except Exception:
        return await mystic.edit_text(_["play_3"])
    if details["duration_min"]:
        duration_sec = time_to_seconds(details["duration_min"])
        if duration_sec > config.DURATION_LIMIT:
            return await mystic.edit_text(
                _["play_6"].format(config.DURATION_LIMIT_MIN, details["duration_min"])
            )
    else:
        buttons = livestream_markup(
            _,
            track_id,
            callback_query.from_user.id,
            mode,
            "c" if cplay == "c" else "g",
            "f" if fplay else "d",
        )
        return await mystic.edit_text(
            _["play_15"],
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    video = True if mode == "v" else None
    ffplay = True if fplay == "f" else None
    try:
        await stream(
            _,
            mystic,
            callback_query.from_user.id,
            details,
            chat_id,
            user_name,
            callback_query.message.chat.id,
            video,
            streamtype="youtube",
            forceplay=ffplay,
        )
    except Exception as e:
        ex_type = type(e).__name__
        err = e if ex_type == "AssistantErr" else _["general_3"].format(ex_type)
        return await mystic.edit_text(err)
    return await mystic.delete()


@app.on_callback_query(filters.regex("AnonymousAdmin") & ~BANNED_USERS)
async def anonymous_check(_client: Client, callback_query: CallbackQuery):
    try:
        await callback_query.answer(
            "You are an anonymous admin\nRevert back to user to use me",
            show_alert=True,
        )
    except Exception:
        return


@app.on_callback_query(filters.regex("WinxPlaylists") & ~BANNED_USERS)
@language_cb
async def play_playlists_command(_client: Client, callback_query: CallbackQuery, _):
    callback_data = callback_query.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    (
        videoid,
        user_id,
        ptype,
        mode,
        cplay,
        fplay,
    ) = callback_request.split("|")
    if callback_query.from_user.id != int(user_id):
        try:
            return await callback_query.answer(_["playcb_1"], show_alert=True)
        except Exception:
            return
    try:
        chat_id, channel = await get_channeplay_cb(_, cplay, callback_query)
    except Exception:
        return
    user_name = callback_query.from_user.first_name
    await callback_query.message.delete()
    try:
        await callback_query.answer()
    except Exception:
        pass
    mystic = await callback_query.message.reply_text(
        _["play_2"].format(channel) if channel else _["play_1"]
    )
    videoid = lyrical.get(videoid)
    video = True if mode == "v" else None
    ffplay = True if fplay == "f" else None
    spotify = True
    if ptype == "yt":
        spotify = False
        try:
            result = await Platform.youtube.playlist(
                videoid,
                config.PLAYLIST_FETCH_LIMIT,
                callback_query.from_user.id,
                True,
            )
        except Exception:
            return await mystic.edit_text(_["play_3"])
    if ptype == "spplay":
        try:
            result, spotify_id = await Platform.spotify.playlist(videoid)
        except Exception:
            return await mystic.edit_text(_["play_3"])
    if ptype == "spalbum":
        try:
            result, spotify_id = await Platform.spotify.album(videoid)
        except Exception:
            return await mystic.edit_text(_["play_3"])
    if ptype == "spartist":
        try:
            result, spotify_id = await Platform.spotify.artist(videoid)
        except Exception:
            return await mystic.edit_text(_["play_3"])
    if ptype == "apple":
        try:
            result, apple_id = await Platform.apple.playlist(videoid, True)
        except Exception:
            return await mystic.edit_text(_["play_3"])
    try:
        await stream(
            _,
            mystic,
            user_id,
            result,
            chat_id,
            user_name,
            callback_query.message.chat.id,
            video,
            streamtype="playlist",
            spotify=spotify,
            forceplay=ffplay,
        )
    except Exception as e:
        ex_type = type(e).__name__
        err = e if ex_type == "AssistantErr" else _["general_3"].format(ex_type)
        return await mystic.edit_text(err)
    return await mystic.delete()


@app.on_callback_query(filters.regex("slider") & ~BANNED_USERS)
@language_cb
async def slider_queries(_client: Client, callback_query: CallbackQuery, _):
    callback_data = callback_query.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    (
        what,
        rtype,
        query,
        user_id,
        cplay,
        fplay,
    ) = callback_request.split("|")
    if callback_query.from_user.id != int(user_id):
        try:
            return await callback_query.answer(_["playcb_1"], show_alert=True)
        except Exception:
            return
    what = str(what)
    rtype = int(rtype)
    if what == "F":
        if rtype == 9:
            query_type = 0
        else:
            query_type = int(rtype + 1)
        try:
            await callback_query.answer(_["playcb_2"])
        except Exception:
            pass
        title, duration_min, thumbnail, vidid = await Platform.youtube.slider(query, query_type)
        buttons = slider_markup(_, vidid, user_id, query, query_type, cplay, fplay)
        med = InputMediaPhoto(
            media=thumbnail,
            caption=_["play_11"].format(
                title.title(),
                duration_min,
            ),
        )
        return await callback_query.edit_message_media(
            media=med, reply_markup=InlineKeyboardMarkup(buttons)
        )
    if what == "B":
        if rtype == 0:
            query_type = 9
        else:
            query_type = int(rtype - 1)
        try:
            await callback_query.answer(_["playcb_2"])
        except Exception:
            pass
        title, duration_min, thumbnail, vidid = await Platform.youtube.slider(query, query_type)
        buttons = slider_markup(_, vidid, user_id, query, query_type, cplay, fplay)
        med = InputMediaPhoto(
            media=thumbnail,
            caption=_["play_11"].format(
                title.title(),
                duration_min,
            ),
        )
        return await callback_query.edit_message_media(
            media=med, reply_markup=InlineKeyboardMarkup(buttons)
        )


@app.on_callback_query(filters.regex("close") & ~BANNED_USERS)
async def close_menu(_, callback_query: CallbackQuery):
    try:
        await callback_query.message.delete()
        await callback_query.answer()
    except Exception:
        return


@app.on_callback_query(filters.regex("stop_downloading") & ~BANNED_USERS)
@actual_admin_cb
async def stop_download(_client: Client, callback_query: CallbackQuery, _):
    message_id = callback_query.message.id
    task = lyrical.get(message_id)
    if not task:
        return await callback_query.answer(
            "Download Already Completed..", show_alert=True
        )
    if task.done() or task.cancelled():
        return await callback_query.answer(
            "Downloading already Completed or Cancelled.",
            show_alert=True,
        )
    if not task.done():
        try:
            task.cancel()
            try:
                lyrical.pop(message_id)
            except Exception:
                pass
            await callback_query.answer("Downloading Cancelled", show_alert=True)
            return await callback_query.edit_message_text(
                f"Downloading cancelled by {callback_query.from_user.mention}"
            )
        except Exception:
            return await callback_query.answer(
                "Failed to stop downloading", show_alert=True
            )

    await callback_query.answer("Failed to Recognise Task", show_alert=True)


__MODULE__ = "Admin"
__HELP__ = f"""
<b>c significa reprodução em canal</b>

<b>✧ {command("PAUSE_COMMAND")}</b> - Pausar a música que está tocando.
<b>✧ {command("RESUME_COMMAND")}</b> - Retomar a música pausada.
<b>✧ {command("MUTE_COMMAND")}</b> - Silenciar a música que está tocando.
<b>✧ {command("UNMUTE_COMMAND")}</b> - Desmutar a música silenciada.
<b>✧ {command("SKIP_COMMAND")}</b> - Pular a música que está tocando.
<b>✧ {command("STOP_COMMAND")}</b> - Parar a música que está tocando.
<b>✧ {command("SHUFFLE_COMMAND")}</b> - Embaralhar aleatoriamente a playlist/músicas na fila.
<b>✧ {command("SEEK_COMMAND")}</b> - Avançar a música para um ponto específico.
<b>✧ {command("SEEK_COMMAND")}</b> - Retroceder a música para um ponto específico.
<b>✧ {command("REBOOT_COMMAND")}</b> - Reiniciar o bot para o seu chat.

<b>✧ {command("SKIP_COMMAND")}</b> [Número (Exemplo: 3)] - Pular a música para um número específico. Exemplo: <b>/skip 3</b> vai pular para a terceira música na fila e ignorar 1 e 2.

<b>✧ {command("LOOP_COMMAND")}</b> [Ativar/Desativar] ou [Número entre 1-10] - Quando ativado, o bot irá repetir a música atual de 1 a 10 vezes no chat de voz. O valor padrão é repetir 10 vezes.
"""

#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#

import asyncio

import speedtest

from strings import command
from YukkiMusic import app
from YukkiMusic.misc import SUDOERS


def testspeed(m):
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = m.edit("⇆ Running Download Speedtest ...")
        test.download()
        m = m.edit("⇆ Running Upload SpeedTest...")
        test.upload()
        test.results.share()
        result = test.results.dict()
        m = m.edit("↻ Sharing SpeedTest results")
    except Exception as e:
        return m.edit(e)
    return result


@app.on_message(command("SPEEDTEST_COMMAND") & SUDOERS)
async def speedtest_function(client, message):
    m = await message.reply_text("ʀᴜɴɴɪɴɢ sᴘᴇᴇᴅᴛᴇsᴛ")
    loop = asyncio.get_event_loop_policy().get_event_loop()
    result = await loop.run_in_executor(None, testspeed, m)
    output = f"""<b>Speedtest Results</b>
<u><b>Client:</b></u>
<blockquote><b>ISP :</b> {result['client']['isp']}
<b>Country :</b> {result['client']['country']}</blockquote>
<u><b>Server:</b></u>
<blockquote><b>Name :</b> {result['server']['name']}
<b>Country:</b> {result['server']['country']}, {result['server']['cc']}
<b>Sponsor:</b> {result['server']['sponsor']}
<b>Latency:</b> {result['server']['latency']}
<b>Ping :</b> {result['ping']}</blockquote>"""
    msg = await app.send_photo(
        chat_id=message.chat.id, photo=result["share"], caption=output
    )
    await m.delete()

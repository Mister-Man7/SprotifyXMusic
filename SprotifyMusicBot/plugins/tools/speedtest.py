import asyncio

from pyrogram import filters

import speedtest
from SprotifyMusic import app
from SprotifyMusic.misc import SUDOERS
from strings import get_command

SPEEDTEST_COMMAND = get_command("SPEEDTEST_COMMAND")


def testspeed(m):
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = m.edit("⇆ Testing **download** ... ⬇️")
        test.download()
        m = m.edit("⇆ Testing **upload** ... ⬆️")
        test.upload()
        test.results.share()
        result = test.results.dict()
        m = m.edit("↻ Sharing Speedtest results ... 📊")
    except Exception as e:
        return m.edit(f"⚠️ Error: {e}")
    return result


@app.on_message(filters.command(SPEEDTEST_COMMAND) & SUDOERS)
async def speedtest_function(client, message):
    m = await message.reply_text("🚀 **Starting Speedtest**...")
    loop = asyncio.get_event_loop_policy().get_event_loop()
    result = await loop.run_in_executor(None, testspeed, m)
    output = f"""**Speedtest results** 📊

<u>**Customer:**</u>
🌐 **ISP :** {result['client']['isp']}
🏳️ **Country :** {result['client']['country']}

<u>**Servidor:**</u>
🌍 **Name :** {result['server']['name']}
🇦🇺 **Country:** {result['server']['country']}, {result['server']['cc']}
💼 **Sponsor:** {result['server']['sponsor']}
⚡ **Latency:** {result['server']['latency']} ms  
🏓 **Ping :** {result['ping']} ms"""
    msg = await app.send_photo(
        chat_id=message.chat.id, photo=result["share"], caption=output
    )
    await m.delete()

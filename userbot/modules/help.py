# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
"""Userbot help command"""

import asyncio
from userbot import CMD_HELP, DEFAULTUSER
from userbot.events import register

modules = CMD_HELP


@register(outgoing=True, pattern="^.help(?: |$)(.*)")
async def help(event):
    """For .help command,"""
    args = event.pattern_match.group(1).lower()
    if args:
        try:
            if args in HELP:
                output = f"**Plugin** - `{args}`\n"
                for i in HELP[args]:
                    output += i
                output += "\n© @LynxUserbot"
                await event.client_send_message(event.chat_id, output)
            elif args in CMD_HELP:
                kk = f"**Plugin {args} Salah ❌\nMohon Ketik Nama Plugin Dengan Benar.**"
                kk += str(CMD_HELP[args])
                await event.send_message(event.chat_id, kk)
                await asyncio.sleep(200)
                await event.delete()
    else:
        string = ""
        for i in CMD_HELP:
            string += "`" + str(i)
            string += "`\t|  "
        await event.edit("⚡")
        await asyncio.sleep(2.5)
        await event.edit("**⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡**\n\n"
                         f"**◑» Bᴏᴛ ᴏꜰ {DEFAULTUSER}**\n**◑» Pʟᴜɢɪɴ : {len(modules)}**\n\n"
                         "**• Mᴀɪɴ Mᴇɴᴜ :**\n"
                         f"╰►| {string} ◄─\n\n")
        await event.reply(f"\n**Contoh** : Ketik » `.help admin` Untuk Informasi Pengunaan Plugin Admin.")
        await asyncio.sleep(1000)
        await event.delete()

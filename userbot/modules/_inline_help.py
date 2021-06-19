# Copyright (C) 2020 TeamDerUntergang.
#
# SedenUserBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SedenUserBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# @Qulec tarafından yazılmıştır.
# Thanks @Spechide.

import logging
from datetime import datetime
from userbot import ALIVE_LOGO, API_HASH, BOT_TOKEN, BOT_USERNAME, BOT_VER, DEFAULTUSER, INSTAGRAM_ALIVE, LOGS, bot
from userbot.events import register

from telethon.sync import TelegramClient, custom, events
from telethon import Button
from telethon.utils import get_display_name


logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.WARNING)


def paginate_help(page_number, loaded_modules, prefix):
    number_of_rows = 4
    number_of_cols = 3
    helpable_modules = [p for p in loaded_modules if not p.startswith("_")]
    helpable_modules = sorted(helpable_modules)
    modules = [
        custom.Button.inline("{} {} 」◑".format("◐「", x), data="ub_modul_{}".format(x))
        for x in helpable_modules
    ]
    pairs = list(zip(modules[::number_of_cols],
                     modules[1::number_of_cols],
                     modules[2::number_of_cols]))
    if len(modules) % number_of_cols == 1:
        pairs.append((modules[-1],))
    max_num_pages = ceil(len(pairs) / number_of_rows)
    modulo_page = page_number % max_num_pages
    if len(pairs) > number_of_rows:
        pairs = pairs[
            modulo_page * number_of_rows: number_of_rows * (modulo_page + 1)
        ] + [
            (
                custom.Button.inline(
                    "⋖╯Pʀᴇᴠ", data="{}_prev({})".format(prefix, modulo_page)
                ),
                custom.Button.inline(
                    "ᴄʟᴏꜱᴇ", data="{}_close({})".format(prefix, modulo_page)
                ),
                custom.Button.inline(
                    "Nᴇxᴛ╰⋗", data="{}_next({})".format(prefix, modulo_page)
                )
            )
        ]
    return pairs


with bot:
    try:
        tgbot = TelegramClient(
            "TG_BOT_TOKEN",
            api_id=API_KEY,
            api_hash=API_HASH).start(
            bot_token=BOT_TOKEN)

        dugmeler = CMD_HELP
        me = bot.get_me()
        uid = me.id

        aliplogo = str(ALIVE_LOGO)
        lynxlogo = "resource/logo/LynxUserbot-Button.jpg"
        plugins = CMD_HELP

        @tgbot.on(events.NewMessage(pattern=r"/start"))
        async def handler(event):
            if event.message.from_id != uid:
                u = await event.client.get_entity(event.chat_id)
                await event.reply(
                    f"Hai 👋 [{get_display_name(u)}](tg://user?id={u.id}) Selamat Datang di ⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡\nJika Kalian Datang Kesini dan Ingin Mengetahui Lynx-Robot Lebih Lanjut,\nSilahkan Pilih **Menu Bantuan** Dibawah Ini.\n",
                    buttons=[
                        [
                            Button.url("📢 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 📢",
                                       "t.me/FederationSuperGroup/3"),
                            Button.url("🚨 𝗠𝗲𝗻𝘂-𝗕𝗮𝗻𝘁𝘂𝗮𝗻 🚨",
                                       "https://telegra.ph/Bantuan-06-11")],
                        [Button.url("👤 𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿 👤",
                                    "t.me/FederationSuperGroup/17")],
                    ]
                )

        @tgbot.on(events.NewMessage(pattern=r"/deploy"))
        async def handler(event):
            if event.message.from_id != uid:
                await event.reply(
                    f"⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡ Deploy to Heroku, Click Here 👇🏻",
                    buttons=[
                        [Button.url("⚒️ 𝗗𝗘𝗣𝗟𝗢𝗬 ⚒️", "https://heroku.com/deploy?template=https://github.com/KENZO-404/Lynx-Userbot/tree/Lynx-Userbot")],
                        [Button.url("👥 𝗚𝗥𝗢𝗨𝗣 👥", "t.me/GroupTidakDiketahui")],
                    ],
                )

        @tgbot.on(events.NewMessage(pattern=r"/repo"))
        async def handler(event):
            if event.message.from_id != uid:
                u = await event.client.get_entity(event.chat_id)
                await event.message.get_sender()
                text = (
                    f"Haii 😼 [{get_display_name(u)}](tg://user?id={u.id}) My Name is 𝗟𝘆𝗻𝘅 🐈\n"
                    f"Lynx Used For Fun On Telegram✨,\n"
                    f"and For Maintaining Your Group 🛠️.\n"
                    f"I was **Created by :** @SyndicateTwenty4 For Various Userbots on Github.\n")
                await tgbot.send_file(event.chat_id, file=lynxlogo,
                                      caption=text,
                                      buttons=[
                                          [
                                              custom.Button.url(
                                                  text="🇮🇩 𝗥𝗲𝗽𝗼𝘀𝗶𝘁𝗼𝗿𝘆 🇮🇩",
                                                  url="https://kenzo-404.github.io/Lynx-Userbot/"
                                              )
                                          ]
                                      ]
                                      )

        @tgbot.on(events.NewMessage(pattern=r"/ping"))
        async def handler(event):
            if event.message.from_id != uid:
                start = datetime.now()
                end = datetime.now()
                ms = (end - start).microseconds / 1000
                await tgbot.send_message(
                    event.chat_id,
                    f"**PONG !!**\n `{ms}ms`",
                )

        @tgbot.on(events.InlineQuery)  # pylint:disable=E0602
        async def inline_handler(event):
            builder = event.builder
            result = None
            query = event.text
            if event.query.user_id == uid and query.startswith("@LynxRobot"):
                buttons = paginate_help(0, dugmeler, "helpme")
                result = builder.photo(
                    file=lynxlogo,
                    link_preview=False,
                    text=f"\n**Bᴏᴛ ᴏꜰ {DEFAULTUSER}**\n\n◎› **Bᴏᴛ ᴠᴇʀ :** `v.{BOT_VER}`\n◎› **Pʟᴜɢɪɴꜱ :** `{len(plugins)}`\n\n**Cᴏᴘʏʀɪɢʜᴛ © 𝟤𝟢𝟤𝟣 Lʏɴx-Uꜱᴇʀʙᴏᴛ**".format(
                        len(dugmeler),
                    ),
                    buttons=buttons,
                )
            elif query.startswith("tb_btn"):
                result = builder.article(
                    "Bantuan Dari ⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡ ",
                    text="Daftar Plugins",
                    buttons=[],
                    link_preview=True)
            else:
                result = builder.article(
                    " ╔╡⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡╞╗ ",
                    text="""**Anda Bisa Membuat ⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡ Anda Sendiri\nDengan Cara :**__Tekan Dibawah Ini__ 👇""",
                    buttons=[
                        [
                            custom.Button.url(
                                "⚡𝗟𝘆𝗻𝘅⚡",
                                "https://kenzo-404.github.io/Lynx-Userbot"),
                            custom.Button.url(
                                "Dᴇᴠᴇʟᴏᴘᴇʀ",
                                "t.me/FederationSuperGroup/17")]],
                    link_preview=False,
                )
            await event.answer([result] if result else None)

        @tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(rb"helpme_next\((.+?)\)")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:  # pylint:disable=E0602
                current_page_number = int(
                    event.data_match.group(1).decode("UTF-8"))
                buttons = paginate_help(
                    current_page_number + 1, dugmeler, "helpme")
                # https://t.me/TelethonChat/115200
                await event.edit(buttons=buttons)
            else:
                reply_pop_up_alert = f"🚫!WARNING!🚫 Jangan Menggunakan Milik {DEFAULTUSER}."
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(rb"helpme_close\((.+?)\)")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:  # Lynx-Openeer
                # https://t.me/TelethonChat/115200
                await event.edit(
                    file=aliplogo,
                    link_preview=True,
                    buttons=[
                        [Button.url("⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡", "t.me/LynxUserbot")],
                        [Button.url("[⊙] 𝗠𝘆 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺", f"{INSTAGRAM_ALIVE}")],
                    ]
                )
                await event.delete()

        @tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(rb"helpme_prev\((.+?)\)")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:  # pylint:disable=E0602
                current_page_number = int(
                    event.data_match.group(1).decode("UTF-8"))
                buttons = paginate_help(
                    current_page_number - 1, dugmeler, "helpme"  # pylint:disable=E0602
                )
                # https://t.me/TelethonChat/115200
                await event.edit(buttons=buttons)
            else:
                reply_pop_up_alert = f"🚫!WARNING!🚫 Jangan Menggunakan Milik {DEFAULTUSER}."
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(b"ub_modul_(.*)")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:  # pylint:disable=E0602
                modul_name = event.data_match.group(1).decode("UTF-8")

                cmdhel = str(CMD_HELP[modul_name])
                if len(cmdhel) > 150:
                    help_string = (
                        str(CMD_HELP[modul_name]).replace('`', '')[:150] + "..."
                        + "\n\nBaca Text Berikutnya Ketik .help "
                        + modul_name
                        + " "
                    )
                else:
                    help_string = str(CMD_HELP[modul_name]).replace('`', '')

                reply_pop_up_alert = (
                    help_string
                    if help_string is not None
                    else "{} Tidak Ada Document Yang Tertulis Untuk Plugin".format(
                        modul_name
                    )
                )
            else:
                reply_pop_up_alert = f"🚫!WARNING!🚫 Jangan Menggunakan Milik {DEFAULTUSER}."

            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    except BaseException:
        LOGS.info(
            "Mode Inline Bot Mu Nonaktif. "
            "Untuk Mengaktifkannya, Silahkan Pergi Ke @BotFather Lalu, Settings Bot > Pilih Mode Inline > Turn On."
        )



@register(outgoing=True, pattern=r"^\.helpme")
async def yardim(event):
    try:
        tgbotusername = BOT_USERNAME
        if tgbotusername is not None:
            results = await event.client.inline_query(tgbotusername, "@LynxRobot")
            await results[0].click(
                event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True
            )
            await event.delete()
        else:
            await event.edit(
                "`The bot doesn't work! Please set the Bot Token and Username correctly. The module has been stopped.`"
            )
    except Exception:
        return await event.edit(
            "`You cannot send inline results in this chat (caused by SendInlineBotResultRequest)`"
        )

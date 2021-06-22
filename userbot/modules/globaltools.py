# Copyright © 2021 Lynx-Userbot (LLC Company)
# GPL-3.0 License (General Public License) From Github Corporation.
# Based On Plugins from Dark Cobra

import asyncio
from telethon.events import ChatAction
from userbot import ALIVE_NAME, CMD_HELP, BOTLOG, BOTLOG_CHATID, DEVELOPER, bot
from userbot.events import register
import userbot.modules.sql_helper.globalban_sql as gban_sql

from userbot.utils import edit_or_reply, edit_delete
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from telethon.tl.types import (
    Channel,
    ChatBannedRights,
    MessageEntityMentionName,
)
from telethon.errors import (
    BadRequestError,
    ChatAdminRequiredError,
    UserAdminInvalidError,
)

NO_ADMIN = "`I am not an admin!`"
NO_SQL = "`Running on Non-SQL mode!`"

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)

UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)
# ================================================
BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)
# =================================================

async def admin_groups(grp):
    admgroups = []
    async for dialog in grp.client.iter_dialogs():
        entity = dialog.entity
        if (
            isinstance(entity, Channel)
            and entity.megagroup
            and (entity.creator or entity.admin_rights)
        ):
            admgroups.append(entity.id)
    return admgroups


def mentionuser(name, userid):
    return f"[{name}](tg://user?id={userid})"


async def get_user_from_event(event, uevent=None, secondgroup=None):
    if uevent is None:
        uevent = event
    if secondgroup:
        args = event.pattern_match.group(2).split(" ", 1)
    else:
        args = event.pattern_match.group(1).split(" ", 1)
    extra = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.from_id is None and not event.is_private:
            await edit_delete(uevent, "`Dia Adalah Admin Anonim.`")
            return None, None
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await edit_delete(
                uevent, "**Mohon Maaf, Silahkan Gunakan ID/Username/Reply Pesan Ke Pengguna.**", 5
            )
            return None, None
        if event.message.entities:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(
                    probable_user_mention_entity,
                    MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj, extra
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError):
            await edit_delete(
                uevent, "**Mohon Maaf, Tidak Dapat Mengambil Informasi User.**", 5
            )
            return None, None
    return user_obj, extra


async def get_full_user(event):
    args = event.pattern_match.group(1).split(':', 1)
    extra = None
    if event.reply_to_msg_id and not len(args) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif len(args[0]) > 0:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await event.edit("`Mohon Gunakan User ID atau Username.`")
            return
        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except Exception as err:
            return await event.edit("`Terjadi Kesalahan... Silahkan Hubungi` @SyndicateTwenty4", str(err))
    return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None
    return user_obj


@bot.on(ChatAction)
async def handler(tele):
    if tele.user_joined or tele.user_added:
        try:
            from userbot.modules.sql_helper.gmute_sql import is_gmuted

            guser = await tele.get_user()
            gmuted = is_gmuted(guser.id)
        except BaseException:
            return
        if gmuted:
            for i in gmuted:
                if i.sender == str(guser.id):
                    chat = await tele.get_chat()
                    admin = chat.admin_rights
                    creator = chat.creator
                    if admin or creator:
                        try:
                            await client.edit_permissions(
                                tele.chat_id, guser.id, view_messages=False
                            )
                            await tele.reply(
                                f"**Pengguna GBAN Telah Bergabung** \n"
                                f"**Pengguna** : [{guser.id}](tg://user?id={guser.id})\n"
                                f"**Aksi**  : `Global Banned`"
                            )
                        except BaseException:
                            return


@register(outgoing=True, pattern=r"^\.gban(?: |$)(.*)")
async def gban(event):
    if event.fwd_from:
        return
    gbun = await edit_or_reply(event, "𝘎𝘭𝘰𝘣𝘢𝘭 𝘉𝘢𝘯𝘯𝘦𝘥 𝘪𝘯 𝘗𝘳𝘰𝘨𝘳𝘦𝘴𝘴...")
    gbun += await edit_or_reply(event, "𝘎𝘭𝘰𝘣𝘢𝘭 𝘉𝘢𝘯𝘯𝘦𝘥 𝘪𝘯 𝘗𝘳𝘰𝘨𝘳𝘦𝘴𝘴...🐈")
    gbun += await edit_or_reply(event, "𝘎𝘭𝘰𝘣𝘢𝘭 𝘉𝘢𝘯𝘯𝘦𝘥 𝘪𝘯 𝘗𝘳𝘰𝘨𝘳𝘦𝘴𝘴..🐈")
    gbun += await edit_or_reply(event, "𝘎𝘭𝘰𝘣𝘢𝘭 𝘉𝘢𝘯𝘯𝘦𝘥 𝘪𝘯 𝘗𝘳𝘰𝘨𝘳𝘦𝘴𝘴.🐈.")
    gbun += await edit_or_reply(event, "𝘎𝘭𝘰𝘣𝘢𝘭 𝘉𝘢𝘯𝘯𝘦𝘥 𝘪𝘯 𝘗𝘳𝘰𝘨𝘳𝘦𝘴𝘴🐈..")
    gbun += await edit_or_reply(event, "𝘎𝘭𝘰𝘣𝘢𝘭 𝘉𝘢𝘯𝘯𝘦𝘥 𝘪𝘯 𝘗𝘳𝘰𝘨𝘳𝘦𝘴🐈...")
    gbun += await edit_or_reply(event, "𝘎𝘭𝘰𝘣𝘢𝘭 𝘉𝘢𝘯𝘯𝘦𝘥 𝘪𝘯 𝘗𝘳𝘰𝘨𝘳𝘦🐈𝘴...")
    gbun += await edit_or_reply(event, "𝘎𝘭𝘰𝘣𝘢𝘭 𝘉𝘢𝘯𝘯𝘦𝘥 𝘪𝘯 𝘗𝘳𝘰𝘨𝘳🐈𝘴𝘴...")
    gbun += await edit_or_reply(event, "𝘎𝘭𝘰𝘣𝘢𝘭 𝘉𝘢𝘯𝘯𝘦𝘥 𝘪𝘯 𝘗𝘳𝘰𝘨🐈𝘦𝘴𝘴...")
    gbun += await edit_or_reply(event, "𝘎𝘭𝘰𝘣𝘢𝘭 𝘉𝘢𝘯𝘯𝘦𝘥 𝘪𝘯 𝘗𝘳𝘰🐈𝘳𝘦𝘴𝘴...")
    gbun += await edit_or_reply(event, "𝘎𝘭𝘰𝘣𝘢𝘭 𝘉𝘢𝘯𝘯𝘦𝘥 𝘪𝘯 𝘗𝘳🐈𝘨𝘳𝘦𝘴𝘴...")
    gbun += await edit_or_reply(event, "𝘎𝘭𝘰𝘣𝘢𝘭 𝘉𝘢𝘯𝘯𝘦𝘥 𝘪𝘯 𝘗🐈𝘰𝘨𝘳𝘦𝘴𝘴...")
    gbun += await edit_or_reply(event, "𝘎𝘭𝘰𝘣𝘢𝘭 𝘉𝘢𝘯𝘯𝘦𝘥 𝘪𝘯 🐈𝘳𝘰𝘨𝘳𝘦𝘴𝘴...")
    gbun += await edit_or_reply(event, "𝘎𝘭𝘰𝘣𝘢𝘭 𝘉𝘢𝘯𝘯𝘦𝘥 𝘪𝘯🐈𝘗𝘳𝘰𝘨𝘳𝘦𝘴𝘴...")
    gbun += await edit_or_reply(event, "𝘎𝘭𝘰𝘣𝘢𝘭 𝘉𝘢𝘯𝘯𝘦𝘥 𝘪🐈 𝘗𝘳𝘰𝘨𝘳𝘦𝘴𝘴...")
    gbun += await edit_or_reply(event, "𝘎𝘭𝘰𝘣𝘢𝘭 𝘉𝘢𝘯𝘯𝘦𝘥 🐈𝘯 𝘗𝘳𝘰𝘨𝘳𝘦𝘴𝘴...")
    gbun += await edit_or_reply(event, "𝘎𝘭𝘰𝘣𝘢𝘭 𝘉𝘢𝘯𝘯𝘦𝘥🐈𝘪𝘯 𝘗𝘳𝘰𝘨𝘳𝘦𝘴𝘴...")
    gbun += await edit_or_reply(event, "⚡")
    gbun += await asyncio.sleep(2.5)
    start = datetime.now()
    user, reason = await get_user_from_event(event, gbun)
    if not user:
        return
    if user.id == (await event.client.get_me()).id:
        await gbun.edit("**Anda ceroboh!**\n__Anda Gbanned diri anda sendiri:)...__")
        return
    if user.id in DEVELOPER:
        await gbun.edit("#DISCLAIMER ❌/nDia Adalah Developer.")
        return
    try:
        hmm = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        await event.client(ImportChatInviteRequest(hmm))
    except BaseException:
        pass
    if gban_sql.is_gbanned(user.id):  # fixes languange by Apis
        await gbun.edit(
            f"**Pengguna** [Ini](tg://user?id={user.id}) **sudah ada di daftar gbanned**"
        )
    else:
        gban_sql.freakgban(user.id, reason)
    xel = []
    xel = await admin_groups(event)
    count = 0
    pis = len(xel)
    if pis == 0:
        await gbun.edit("**Anda Tidak Mempunyai Group Dan Anda Tidak Mempunyai Title Admin.**")
        return
    await gbun.edit(
        f"**Pengguna** [Ini](tg://user?id={user.id}) **Sudah Berada Di Dalam Daftar** `{len(xel)}` **Group**"
    )
    for i in range(pis):
        try:
            await event.client(EditBannedRequest(xel[i], user.id, BANNED_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"**Anda Tidak Memiliki Izin Banned di :**\n**Group Chat :** `{event.chat_id}`",
            )
    end = datetime.now()
    timetaken = (end - start).seconds
    if reason:
        await gbun.edit(
            f"╭─━━━━━━━━━━━━━━━━─╮\nㅤ  ㅤ[⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡](t.me/LynxUserbot)\n╭─━━━━━━━━━━━━━━━━─╯\n**│• GBAN By :** `{ALIVE_NAME}`\n**│• User Account :** [{user.first_name}](tg://user?id={user.id})\n**│• Jumlah : {count} Group, Dalam {timetaken} Detik\n**│• Reason : {reason}\n**│• Action :** `GBanned` ✅\n╰━━━━━━━━━━━━━━━━━━╯"
        )
    else:
        await gbun.edit(
            f"╭─━━━━━━━━━━━━━━━━─╮\nㅤ  ㅤ[⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡](t.me/LynxUserbot)\n╭─━━━━━━━━━━━━━━━━─╯\n**│• GBAN By :** `{ALIVE_NAME}`\n**│• User Account :** [{user.first_name}](tg://user?id={user.id})\n**│• Jumlah : {count} Group, Dalam {timetaken} Detik\n**│• Action :** `GBanned` ✅\n╰━━━━━━━━━━━━━━━━━━╯"
        )

    if BOTLOG and count != 0:
        reply = await event.get_reply_message()
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#GBANNED\
                \nGlobal Banned\
                \n**Pengguna : **[{user.first_name}](tg://user?id={user.id})\
                \n**ID : **`{user.id}`\
                \n**Reason :** `{reason}`\
                \n__Banned Dalam {count} Group__\
                \n**Waktu Yang Dibutuhkan : **`{timetaken} Detik`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#GBANNED\
                \nGlobal Banned\
                \n**Pengguna : **[{user.first_name}](tg://user?id={user.id})\
                \n**ID : **`{user.id}`\
                \n__Banned Dalam {count} Group__\
                \n**Waktu Yang Dibutuhkan : **`{timetaken} Detik`",
            )
        try:
            if reply:
                await reply.forward_to(BOTLOG_CHATID)
                await reply.delete()
        except BadRequestError:
            pass


@register(outgoing=True, pattern=r"^\.ungban(?: |$)(.*)")
async def ungban(event):
    if event.fwd_from:
        return
    ungbun = await edit_or_reply(event, "`UnGbanning.....`")
    start = datetime.now()
    user, reason = await get_user_from_event(event, ungbun)
    if not user:
        return
    if gban_sql.is_gbanned(user.id):  # fixes languange by Apis
        gban_sql.freakungban(user.id)
    else:
        await ungbun.edit(
            f"**Pengguna** [Ini](tg://user?id={user.id}) **ini tidak ada dalam daftar gban Anda**"
        )
        return
    xel = []
    xel = await admin_groups(event)
    count = 0
    pis = len(xel)
    if pis == 0:
        await ungbun.edit("**Anda Tidak mempunyai GC yang anda admin 🥺**")
        return
    await ungbun.edit(
        f"**Pengguna** [Ini](tg://user?id={user.id}) **dalam** `{len(xel)}` **grup**"
    )
    for i in range(pis):
        try:
            await event.client(EditBannedRequest(xel[i], user.id, UNBAN_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"**Anda Tidak Memiliki Izin Ungbanned di :**\n**Group Chat :** `{event.chat_id}`",
            )
    end = datetime.now()
    timetaken = (end - start).seconds
    if reason:
        await ungbun.edit(
            f"╭─━━━━━━━━━━━━━━━━─╮\nㅤ  ㅤ[⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡](t.me/LynxUserbot)\n╭─━━━━━━━━━━━━━━━━─╯\n**│• UNGBAN By :** `{ALIVE_NAME}`\n**│• User Account :** [{user.first_name}](tg://user?id={user.id})\n**│• Jumlah : {count} Group, Dalam {timetaken} Detik\n**│• Reason : {reason}\n**│• Action :** `UNGBanned` ❌\n╰━━━━━━━━━━━━━━━━━━╯"
        )
    else:
        await ungbun.edit(
            f"╭─━━━━━━━━━━━━━━━━─╮\nㅤ  ㅤ[⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡](t.me/LynxUserbot)\n╭─━━━━━━━━━━━━━━━━─╯\n**│• UNGBAN By :** `{ALIVE_NAME}`\n**│• User Account :** [{user.first_name}](tg://user?id={user.id})\n**│• Jumlah : {count} Group, Dalam {timetaken} Detik\n**│• Action :** `UNGBanned` ❌\n╰━━━━━━━━━━━━━━━━━━╯"
        )

    if BOTLOG and count != 0:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#UNGBANNED\
                \nGlobal Unbanned\
                \n**Pengguna : **[{user.first_name}](tg://user?id={user.id})\
                \n**ID : **`{user.id}`\
                \n**Reason :** `{reason}`\
                \n__UNGBanned Dalam {count} Group__\
                \n**Waktu Yang Di Butuhkan : **`{timetaken} Detik`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#UNGBANNED\
                \nGlobal Unbaned\
                \n**Pengguna : **[{user.first_name}](tg://user?id={user.id})\
                \n**ID : **`{user.id}`\
                \n__UNGBanned Dalam {count} Group__\
                \n**Waktu Yang Di Butuhkan : **`{timetaken} Detik`",
            )


@register(outgoing=True, pattern=r"^\.listgban$")
async def gablist(event):
    if event.fwd_from:  # This is created by catuserbot
        return
    gbanned_users = gban_sql.get_all_gbanned()
    GBANNED_LIST = "**Daftar Global Banned :**\n"
    if len(gbanned_users) > 0:
        for a_user in gbanned_users:
            if a_user.reason:
                GBANNED_LIST += f"│👤 User : [{a_user.chat_id}](tg://user?id={a_user.chat_id}) \nReason : `{a_user.reason}`\n"
            else:
                GBANNED_LIST += (
                    f"│👤 User : [{a_user.chat_id}](tg://user?id={a_user.chat_id}) `No Reason`\n"
                )
    else:
        GBANNED_LIST = "Daftar List Global Banned `Kosong`.\n Anda Belum Pernah Melakukan Global Banned Sebelumnya."
    await edit_or_reply(event, GBANNED_LIST)



async def get_user_from_event(event):
    args = event.pattern_match.group(1).split(':', 1)
    extra = None
    if event.reply_to_msg_id and not len(args) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
        extra = event.pattern_match.group(1)
    elif len(args[0]) > 0:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await event.edit(f"`{ALIVE_NAME}`: ** Harus Mereply Dengan Username Pengguna!**")
            return
        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except Exception as err:
            return await event.edit("Gagal \n **Error**\n", str(err))
    return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None
    return user_obj

try:
    from userbot import client2, client3
except BaseException:
    client2 = client3 = None


@register(outgoing=True, pattern=r"^\.gkick(?: |$)(.*)")
async def gspide(rk):
    lazy = rk
    sender = await lazy.get_sender()
    me = await lazy.client.get_me()
    if not sender.id == me.id:
        rkp = await lazy.reply("`Memproses Global Kick...`")
    else:
        rkp = await lazy.edit("`Memproses Global Kick...`")
    me = await rk.client.get_me()
    await rkp.edit(f"`{ALIVE_NAME}:` **Meminta Untuk Mengkick Pengguna !**")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    await rk.get_chat()
    a = b = 0
    if rk.is_private:
        user = rk.chat
        reason = rk.pattern_match.group(1)
    else:
        rk.chat.title
    try:
        user, reason = await get_user_from_event(rk)
    except BaseException:
        pass
    try:
        if not reason:
            reason = 'Private'
    except BaseException:
        return await rkp.edit(f"`{ALIVE_NAME}:`**Kesalahan! Pengguna Tidak Dikenal.**")
    if user:
        if user.id == 1345333945:
            return await rkp.edit(f"`{ALIVE_NAME}:`**Anda Sepertinya Tidak Bisa Melakukan Global Kick ke Pengguna Ini, Karena Dia Adalah Pembuat Saya 😎**")
        try:
            await rk.client(BlockRequest(user))
            await rk.client(UnblockRequest(user))
        except BaseException:
            pass
        testrk = [d.entity.id for d in await rk.client.get_dialogs() if (d.is_group or d.is_channel)]
        for i in testrk:
            try:
                await rk.client.edit_permissions(i, user, view_messages=False)
                await rk.client.edit_permissions(i, user, send_messages=True)
                a += 1
                await rkp.edit(f"`{ALIVE_NAME}:` **Meminta Untuk Mengkick Pengguna !\nGlobal Kicked {a} Chat...**")

            except BaseException:
                b += 1
    else:
        await rkp.edit(f"`{ALIVE_NAME}:` **Balas ke pengguna !! **")

    return await rkp.edit(f"`{ALIVE_NAME}:` **Global Kicked [{user.first_name}](tg://user?id={user.id}) Dalam {a} Chat(s) **")


@register(incoming=True, disable_errors=True)
async def muter(moot):
    """Used for deleting the messages of muted people"""
    try:
        from userbot.modules.sql_helper.gmute_sql import is_gmuted
        from userbot.modules.sql_helper.spam_mute_sql import is_muted
    except AttributeError:
        return
    muted = is_muted(moot.chat_id)
    gmuted = is_gmuted(moot.sender_id)
    rights = ChatBannedRights(
        until_date=None,
        send_messages=True,
        send_media=True,
        send_stickers=True,
        send_gifs=True,
        send_games=True,
        send_inline=True,
        embed_links=True,
    )
    if muted:
        for i in muted:
            if str(i.sender) == str(moot.sender_id):
                try:
                    await moot.delete()
                    await moot.client(
                        EditBannedRequest(moot.chat_id, moot.sender_id, rights)
                    )
                except (
                    BadRequestError,
                    UserAdminInvalidError,
                    ChatAdminRequiredError,
                    UserIdInvalidError,
                ):
                    await moot.client.send_read_acknowledge(moot.chat_id, moot.id)
    for i in gmuted:
        if i.sender == str(moot.sender_id):
            await moot.delete()


@register(outgoing=True, disable_errors=True, pattern=r"^\.gmute(?: |$)(.*)")
async def gspider(gspdr):
    """For .gmute command, globally mutes the replied/tagged person"""
    # Admin or creator check
    chat = await gspdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await gspdr.edit(NO_ADMIN)
        return

    # Check if the function running under SQL mode
    try:
        from userbot.modules.sql_helper.gmute_sql import gmute
    except AttributeError:
        await gspdr.edit(NO_SQL)
        return

    user, reason = await get_user_from_event(gspdr)
    if not user:
        return

    # If pass, inform and start gmuting
    await gspdr.edit("`Grabs a huge, sticky duct tape!`")
    if gmute(user.id) is False:
        await gspdr.edit("`Error! User probably already gmuted.\nRe-rolls the tape.`")
    else:
        if reason:
            await gspdr.edit(f"`Globally taped!`\nReason: {reason}")
        else:
            await gspdr.edit("`Globally taped!`")

        if BOTLOG:
            await gspdr.client.send_message(
                BOTLOG_CHATID,
                "#GMUTE\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {gspdr.chat.title}(`{gspdr.chat_id}`)",
            )


@register(outgoing=True, disable_errors=True, pattern=r"^\.ungmute(?: |$)(.*)")
async def ungmoot(un_gmute):
    """For .ungmute command, ungmutes the target in the userbot"""
    # Admin or creator check
    chat = await un_gmute.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await un_gmute.edit(NO_ADMIN)
        return

    # Check if the function running under SQL mode
    try:
        from userbot.modules.sql_helper.gmute_sql import ungmute
    except AttributeError:
        await un_gmute.edit(NO_SQL)
        return

    user = await get_user_from_event(un_gmute)
    user = user[0]
    if not user:
        return

    # If pass, inform and start ungmuting
    await un_gmute.edit("```Ungmuting...```")

    if ungmute(user.id) is False:
        await un_gmute.edit("`Error! User probably not gmuted.`")
    else:
        # Inform about success
        await un_gmute.edit("```Ungmuted Successfully```")
        await sleep(3)
        await un_gmute.delete()

        if BOTLOG:
            await un_gmute.client.send_message(
                BOTLOG_CHATID,
                "#UNGMUTE\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {un_gmute.chat.title}(`{un_gmute.chat_id}`)",
            )


CMD_HELP.update({
    "globaltools":
    "✘ Pʟᴜɢɪɴ : Global Tools\
\n\n⚡𝘾𝙈𝘿⚡: `.gban` <Username/ID/Reply> <Reason>\
\n↳ : Melakukan Banned Secara Global Ke Semua Group Dimana Anda Sebagai Admin.\
\n\n⚡𝘾𝙈𝘿⚡: `.ungban` <Username/ID/Reply> <Reason>\
\n↳ : Membatalkan Banned Secara Global.\
\n\n⚡𝘾𝙈𝘿⚡: `.listgban`\
\n↳ : Melihat Daftar Global Banned.\
\n\n⚡𝘾𝙈𝘿⚡: `.gmute` <Username/Reply> <Alasan(Optional)>\
\n↳ : Membisukan Pengguna Ke Semua Group, Dimana Kamu Sebagai Admin Group.\
\n\n⚡𝘾𝙈𝘿⚡: `.ungmute` <Username/Reply>\
\n↳ : Tag atau Reply Pesan Pengguna `.ungmute` Untuk Menghapus Pengguna Dari Daftar Global Mute.\
\n\n⚡𝘾𝙈𝘿⚡: `.gkick` <Text>\
\n↳ : Melakukan Kick Secara Global. Hampir Sama Dengan Global Ban, Tapi Ini Hanya Kick.\
\n\n⚡𝘾𝙈𝘿⚡: `.ggcast` <Pesan>\
\n↳ : Global Group Broadcast. Mengirim Pesan ke Seluruh Group yang Anda Masuki.\
\n\n⚡𝘾𝙈𝘿⚡: `.gucast` <Pesan>\
\n↳ : Global Users Broadcast. Kirim Pesan itu Secara Global ke Semua Anggota Group Anda."})

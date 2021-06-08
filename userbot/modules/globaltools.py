# Based On Plugins from Dark Cobra
# Lynx Userbot © 2021

import asyncio
from telethon.events import ChatAction
from userbot import ALIVE_NAME, CMD_HELP, bot
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from userbot.events import register
from telethon.tl.types import MessageEntityMentionName


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
            await event.edit("`Mohon Gunakan ID Pengguna atau Username.`")
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


@register(outgoing=True, pattern="^.gban(?: |$)(.*)")
async def gben(userbot):
    dc = userbot
    sender = await dc.get_sender()
    me = await dc.client.get_me()
    if not sender.id == me.id:
        dark = await dc.reply("`Saya Sedang Mengaktifkan Perintah Global Banned !`")
    else:
        dark = await dc.edit("`Connected to server telegram...`")
    me = await userbot.client.get_me()
    await dark.edit(f"`Global Banned Akan Segera Aktif, Anda Akan Dibanned Secara Global Oleh {ALIVE_NAME}`")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    await userbot.get_chat()
    a = b = 0
    if userbot.is_private:
        user = userbot.chat
        reason = userbot.pattern_match.group(1)
    else:
        userbot.chat.title
    try:
        user, reason = await get_full_user(userbot)
    except BaseException:
        pass
    try:
        if not reason:
            reason = "Private"
    except BaseException:
        return await dark.edit(f"`Maaf Terjadi Kesalahan.❌`\nMohon Gunakan Username/ID Saja.")
    if user:
        if user.id == 1345333945:
            return await dark.edit(
                f"🚫 Anda Tidak Bisa Melakukan Global Banned Ke Axel, Dia Adalah Developer."
            )
        try:
            from userbot.modules.sql_helper.gmute_sql import gmute
        except BaseException:
            pass
        try:
            await userbot.client(BlockRequest(user))
        except BaseException:
            pass
        testuserbot = [
            d.entity.id
            for d in await userbot.client.get_dialogs()
            if (d.is_group or d.is_channel)
        ]
        for i in testuserbot:
            try:
                await userbot.client.edit_permissions(i, user, view_messages=False)
                a += 1
                await dark.edit(f"𝘎𝘭𝘰𝘣𝘢𝘭 𝘉𝘢𝘯𝘯𝘦𝘥 𝘪𝘯 𝘗𝘳𝘰𝘨𝘳𝘦𝘴𝘴...🐈")
                await dark.edit(f"𝘎𝘭𝘰𝘣𝘢𝘭 𝘉𝘢𝘯𝘯𝘦𝘥 𝘪𝘯 𝘗𝘳𝘰𝘨𝘳𝘦𝘴𝘴..🐈")
                await dark.edit(f"𝘎𝘭𝘰𝘣𝘢𝘭 𝘉𝘢𝘯𝘯𝘦𝘥 𝘪𝘯 𝘗𝘳𝘰𝘨𝘳𝘦𝘴𝘴.🐈.")
                await dark.edit(f"𝘎𝘭𝘰𝘣𝘢𝘭 𝘉𝘢𝘯𝘯𝘦𝘥 𝘪𝘯 𝘗𝘳𝘰𝘨𝘳𝘦𝘴𝘴🐈..")
                await dark.edit(f"𝘎𝘭𝘰𝘣𝘢𝘭 𝘉𝘢𝘯𝘯𝘦𝘥 𝘪𝘯 𝘗𝘳𝘰𝘨𝘳𝘦𝘴🐈...")
                await dark.edit(f"𝘎𝘭𝘰𝘣𝘢𝘭 𝘉𝘢𝘯𝘯𝘦𝘥 𝘪𝘯 𝘗𝘳𝘰𝘨𝘳𝘦🐈𝘴...")
                await dark.edit(f"𝘎𝘭𝘰𝘣𝘢𝘭 𝘉𝘢𝘯𝘯𝘦𝘥 𝘪𝘯 𝘗𝘳𝘰𝘨𝘳🐈𝘴𝘴...")
                await dark.edit(f"𝘎𝘭𝘰𝘣𝘢𝘭 𝘉𝘢𝘯𝘯𝘦𝘥 𝘪𝘯 𝘗𝘳𝘰𝘨🐈𝘦𝘴𝘴...")
                await dark.edit(f"𝘎𝘭𝘰𝘣𝘢𝘭 𝘉𝘢𝘯𝘯𝘦𝘥 𝘪𝘯 𝘗𝘳𝘰🐈𝘳𝘦𝘴𝘴...")
                await dark.edit(f"𝘎𝘭𝘰𝘣𝘢𝘭 𝘉𝘢𝘯𝘯𝘦𝘥 𝘪𝘯 𝘗𝘳🐈𝘨𝘳𝘦𝘴𝘴...")
                await dark.edit(f"𝘎𝘭𝘰𝘣𝘢𝘭 𝘉𝘢𝘯𝘯𝘦𝘥 𝘪𝘯 𝘗🐈𝘰𝘨𝘳𝘦𝘴𝘴...")
                await dark.edit(f"𝘎𝘭𝘰𝘣𝘢𝘭 𝘉𝘢𝘯𝘯𝘦𝘥 𝘪𝘯 🐈𝘳𝘰𝘨𝘳𝘦𝘴𝘴...")
                await dark.edit(f"𝘎𝘭𝘰𝘣𝘢𝘭 𝘉𝘢𝘯𝘯𝘦𝘥 𝘪𝘯🐈𝘗𝘳𝘰𝘨𝘳𝘦𝘴𝘴...")
                await dark.edit(f"𝘎𝘭𝘰𝘣𝘢𝘭 𝘉𝘢𝘯𝘯𝘦𝘥 𝘪🐈 𝘗𝘳𝘰𝘨𝘳𝘦𝘴𝘴...")
                await dark.edit(f"𝘎𝘭𝘰𝘣𝘢𝘭 𝘉𝘢𝘯𝘯𝘦𝘥 🐈𝘯 𝘗𝘳𝘰𝘨𝘳𝘦𝘴𝘴...")
                await dark.edit(f"𝘎𝘭𝘰𝘣𝘢𝘭 𝘉𝘢𝘯𝘯𝘦𝘥🐈𝘪𝘯 𝘗𝘳𝘰𝘨𝘳𝘦𝘴𝘴...")
                await dark.edit(f"⚡")
                await asyncio.sleep(3)
                await dark.edit(f"𝗚𝗹𝗼𝗯𝗮𝗹 𝗕𝗮𝗻𝗻𝗲𝗱 𝘼𝙘𝙩𝙞𝙫𝙚 ✅")
            except BaseException:
                b += 1
    else:
        await dark.edit(f"`Mohon Reply Ke Pesan Pengguna Yang Ingin Di Ban.`")
    try:
        if gmute(user.id) is False:
            return await dark.edit(f"**❌ Error: Pengguna Ini Sudah Terkena Global Banned.**")
    except BaseException:
        pass
    return await dark.edit(
        f"╭─━━━━━━━━━━━━━━━─╮\nㅤㅤ⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡\n╭─━━━━━━━━━━━━━━━─╯\n**│⊙ GBAN By :** `{ALIVE_NAME}`\n**│⊙ User Account :** [{user.first_name}](tg://user?id={user.id})\n**│⊙ Action :** `Global Banned` ✅\n╰━━━━━━━━━━━━━━━━━╯"
    )


@register(outgoing=True, pattern="^.ungban(?: |$)(.*)")
async def gunben(userbot):
    dc = userbot
    sender = await dc.get_sender()
    me = await dc.client.get_me()
    if not sender.id == me.id:
        dark = await dc.reply("`Membatalkan Global Banned Pengguna Ini.`")
    else:
        dark = await dc.edit("`Connected to server telegram...`")
    me = await userbot.client.get_me()
    await dark.edit(f"`Mulai Membatalkan Global Banned, Pengguna Ini Akan Dapat Bergabung Ke Grup Anda.`")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    await userbot.get_chat()
    a = b = 0
    if userbot.is_private:
        user = userbot.chat
        reason = userbot.pattern_match.group(1)
    else:
        userbot.chat.title
    try:
        user, reason = await get_full_user(userbot)
    except BaseException:
        pass
    try:
        if not reason:
            reason = "Private"
    except BaseException:
        return await dark.edit("`❌ Error: Terjadi Kesalahan.`")
    if user:
        if user.id == 1345333945:
            return await dark.edit("**Anda Tidak Bisa Melakukan Perintah Ini, Dia Adalah Pembuatku.**")
        try:
            from userbot.modules.sql_helper.gmute_sql import ungmute
        except BaseException:
            pass
        try:
            await userbot.client(UnblockRequest(user))
        except BaseException:
            pass
        testuserbot = [
            d.entity.id
            for d in await userbot.client.get_dialogs()
            if (d.is_group or d.is_channel)
        ]
        for i in testuserbot:
            try:
                await userbot.client.edit_permissions(i, user, send_messages=True)
                a += 1
                await dark.edit(f"`Sedang Membatalkan Global Banned\n in Progress... `")
            except BaseException:
                b += 1
    else:
        await dark.edit("`Harap Reply Ke Pesan Pengguna Yang Ingin Anda Batalkan.`")
    try:
        if ungmute(user.id) is False:
            return await dark.edit("**❌ Error: Pengguna Memang Tidak Terkena Global Banned.**")
    except BaseException:
        pass
    return await dark.edit(
        f"╭─━━━━━━━━━━━━━━━─╮\nㅤㅤ⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡\n╭─━━━━━━━━━━━━━━━─╯\n**│⊙ UnGBAN By :** `{ALIVE_NAME}`\n**│⊙ User Account :** [{user.first_name}](tg://user?id={user.id})\n**│⊙ Action :** `Global Banned Canceled`\n╰━━━━━━━━━━━━━━━━━╯"
    )


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


CMD_HELP.update({
    "globaltools":
    "✘ Pʟᴜɢɪɴ : Global Tools\
\n\n⚡𝘾𝙈𝘿⚡: `.gban` <Useraname/ID>\
\n↳ : Melakukan Banned Secara Global Ke Semua Grup Dimana Anda Sebagai Admin.\
\n\n⚡𝘾𝙈𝘿⚡: `.ungban` <Username/ID>\
\n↳ : Membatalkan Banned Secara Global.\
\n\n⚡𝘾𝙈𝘿⚡: `.gkick` <Text>\
\n↳ : Melakukan Kick Secara Global. Hampir Sama Dengan Global Ban, Tapi Ini Hanya Kick."})

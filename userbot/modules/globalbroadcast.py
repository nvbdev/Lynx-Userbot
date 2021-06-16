from userbot.events import register
from userbot import bot


@register(outgoing=True, pattern="^.ggcast (.*)")
async def gcast(event):
    xx = event.pattern_match.group(1)
    if not xx:
        return await event.edit("`Mohon Berikan Sebuah Pesan`")
    tt = event.text
    msg = tt[6:]
    kk = await event.edit("`Sedang Mengirim Pesan Group Secara Global... 📢`")
    er = 0
    done = 0
    async for x in bot.iter_dialogs():
        if x.is_group:
            chat = x.id
            try:
                done += 1
                await bot.send_message(chat, msg)
            except BaseException:
                er += 1
    await kk.edit(f"**✔️Berhasil** Mengirim Pesan Ke : `{done}` Group.\n**❌Gagal** Mengirim Pesan Ke : `{er}` Group.")


@register(outgoing=True, pattern="^.gucast (.*)")
async def gucast(event):
    xx = event.pattern_match.group(1)
    if not xx:
        return await event.edit("`Mohon Berikan Sebuah Pesan`")
    tt = event.text
    msg = tt[7:]
    kk = await event.edit("`Sedang Mengirim Pivate Messages Secara Global... 📢`")
    er = 0
    done = 0
    async for x in bot.iter_dialogs():
        if x.is_user and not x.entity.bot:
            chat = x.id
            try:
                done += 1
                await bot.send_message(chat, msg)
            except BaseException:
                er += 1
    await kk.edit(f"**✔️Berhasil** Mengirim Pesan Ke : `{done}` Orang.\n**❌Gagal** Mengirim Pesan Ke : `{er}` Orang.")

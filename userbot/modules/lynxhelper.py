""" Userbot module for other small commands. """
from userbot import CMD_HELP, DEFAULTUSER
from userbot.events import register


@register(outgoing=True, pattern="^.lhelp$")
async def usit(e):
    await e.edit(
        f"**Hai {DEFAULTUSER} ð Jika Anda Tidak Tau Perintah Untuk Memerintah Ku,\nKetik:** `.help` Atau Bisa Minta Bantuan Ke\n"
        "\nð¬**Developer :**"
        "\n[Telegram](t.me/TeamSecret_Kz)"
        "\n[Dev Repo](https://github.com/KENZO-404)"
        "\n[Instagram](instagram.com/si_axeell)")


@register(outgoing=True, pattern="^.vars$")
async def var(m):
    await m.edit(
        f"**Daftar Vars Untuk {DEFAULTUSER}:**\n"
        "\nClick Â» [ [Lynx-VARS](https://raw.githubusercontent.com/KENZO-404/Lynx-Userbot/Lynx-Userbot/varshelper.txt) ] Â«")


CMD_HELP.update({
    "lynxhelper":
    "â PÊá´É¢ÉªÉ´ : Lynx Helper\
\n\nâ¡ð¾ðð¿â¡: `.lhelp`\
\nâ³ : Bantuan Untuk User Lynx.\
\n\nâ¡ð¾ðð¿â¡: `.vars`\
\nâ³ : Melihat Daftar Vars Lynx-Userbot."
})

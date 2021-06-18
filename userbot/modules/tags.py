# Ultroid - UserBot
# Copyright (C) 2020 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
# Ported for Lynx-Userbot by @SyndicateTwenty4

from telethon.tl.types import ChannelParticipantAdmin as admin
from telethon.tl.types import ChannelParticipantCreator as owner
from telethon.tl.types import UserStatusOffline as off
from telethon.tl.types import UserStatusOnline as onn
from telethon.tl.types import UserStatusRecently as rec
from telethon.utils import get_display_name
from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True,
          pattern=r"^.tags(?: |$)(on|off|all|bots|rec|admin|owner)?")
async def ngeteg(event):
    okk = event.text
    lll = event.pattern_match.group(2)
    users = 0
    o = 0
    nn = 0
    rece = 0
    if lll:
        xx = f"{lll}"
    else:
        xx = ""
    async for bb in event.client.iter_participants(event.chat_id, 99):
        users = users + 1
        x = bb.status
        y = bb.participant
        if isinstance(x, onn):
            o = o + 1
            if "on" in okk:
                xx += f"\n[{get_display_name(bb)}](tg://user?id={bb.id})"
        if isinstance(x, off):
            nn = nn + 1
            if "off" in okk:
                if not (bb.bot or bb.deleted):
                    xx += f"\n[{get_display_name(bb)}](tg://user?id={bb.id})"
        if isinstance(x, rec):
            rece = rece + 1
            if "rec" in okk:
                if not (bb.bot or bb.deleted):
                    xx += f"\n[{get_display_name(bb)}](tg://user?id={bb.id})"
        if isinstance(y, owner):
            if "admin" or "owner" in okk:
                xx += f"\n꧁[{get_display_name(bb)}](tg://user?id={bb.id})꧂"
        if isinstance(y, admin):
            if "admin" in okk:
                if not bb.deleted:
                    xx += f"\n[{get_display_name(bb)}](tg://user?id={bb.id})"
        if "all" in okk:
            if not (bb.bot or bb.deleted):
                xx += f"\n[{get_display_name(bb)}](tg://user?id={bb.id})"
        if "bot" in okk:
            if bb.bot:
                xx += f"\n[{get_display_name(bb)}](tg://user?id={bb.id})"
    await event.client.send_message(event.chat_id, xx)
    await event.delete()


CMD_HELP.update({
    'tags': "✘ Pʟᴜɢɪɴ : Tags"
    "\n\n⚡𝘾𝙈𝘿⚡: `.tags all`"
    "\n↳ : Tag Top 100 Members of Chat."
    "\n\n⚡𝘾𝙈𝘿⚡: `.tags admin`"
    "\n↳ : Tag Admins of That Chat."
    "\n\n⚡𝘾𝙈𝘿⚡: `.tags owner`"
    "\n↳ : Tag Owner of That Chat."
    "\n\n⚡𝘾𝙈𝘿⚡: `.tags bot`"
    "\n↳ : Tag Bots of That Chat."
    "\n\n⚡𝘾𝙈𝘿⚡: `.tags rec`"
    "\n↳ : Tag Recently Active Members."
    "\n\n⚡𝘾𝙈𝘿⚡: `.tags on`"
    "\n↳ : Tag Online Members(Work Only if Privacy Off)."
    "\n\n⚡𝘾𝙈𝘿⚡: `.tags off`"
    "\n↳ : Tag Offline Members(Work Only if Privacy Off)."
})

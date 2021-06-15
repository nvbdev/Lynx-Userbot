# Copyright (C) 2021 Lynx-Userbot GPL-3.0 License:
# You may not use this file except in compliance with the License.
# All Rights Reserved

from userbot import (
    CMD_HELP,
    handler,
    me,
    uid,
    bot
)
import os
import shutil
import subprocess
import time
import asyncio
from telethon import events

from userbot.utils import chrome, progress
from userbot.utils.FastTelethon import upload_file
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from pylast import User
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.types import DocumentAttributeAudio, DocumentAttributeVideo


async def getmusicvideo(cat):
    video_link = ""
    search = cat
    driver = await chrome()
    driver.get("https://www.youtube.com/results?search_query=" + search)
    user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
    for i in user_data:
        video_link = i.get_attribute("href")
        break
    command = 'youtube-dl -f "[filesize<50M]" --merge-output-format mp4 ' + video_link
    os.system(command)


@tgbot.on(events.ChatAction(pattern="/vsong"))
async def handler(event):
    if event.message.from_id != uid:
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
        await event.edit("`Wait..! I am finding your videosong..`")
    elif reply:
        query = str(reply.message)
        await event.edit("`Wait..! I am finding your videosong..`")
    else:
        await event.edit("`What I am Supposed to find?`")
        return
    await getmusicvideo(query)
    l = glob.glob(("*.mp4")) + glob.glob(("*.mkv")) + glob.glob(("*.webm"))
    if l:
        await event.edit("`Yeah..! i found something..`")
    else:
        await event.edit(f"`Sorry..! i can't find anything with` **{query}**")
        return
    try:
        loa = l[0]
        metadata = extractMetadata(createParser(loa))
        duration = 0
        width = 0
        height = 0
        if metadata.has("duration"):
            duration = metadata.get("duration").seconds
        if metadata.has("width"):
            width = metadata.get("width")
        if metadata.has("height"):
            height = metadata.get("height")
        os.system("cp *mp4 thumb.mp4")
        os.system("ffmpeg -i thumb.mp4 -vframes 1 -an -s 480x360 -ss 5 thumb.jpg")
        thumb_image = "thumb.jpg"
        c_time = time.time()
        with open(loa, "rb") as f:
            result = await upload_file(
                client=event.client,
                file=f,
                name=loa,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, event, c_time, "[UPLOAD]", loa)
                ),
            )
        await tgbot.send_file(
            event.chat_id,
            result,
            force_document=False,
            thumb=thumb_image,
            allow_cache=False,
            caption=query,
            supports_streaming=True,
            reply_to=reply_to_id,
            attributes=[
                DocumentAttributeVideo(
                    duration=duration,
                    w=width,
                    h=height,
                    round_message=False,
                    supports_streaming=True,
                )
            ],
        )
        await event.edit(f"**{query}** `Uploaded Successfully..!`")
        os.remove(thumb_image)
        os.system("rm *.mkv *.mp4 *.webm")
    except BaseException:
        os.remove(thumb_image)
        os.system("rm *.mkv *.mp4 *.webm")
        return

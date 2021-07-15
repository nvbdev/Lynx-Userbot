# Copyright (C) 2020 MoveAngel and MinaProject
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Multifunction memes
#
# Based code + improve from AdekMaulana and aidilaryanto
#
# Memify ported from Userge and Refactored by KenHV

import asyncio
import io
import os
import random
import re
import shlex
import textwrap
import time
from random import randint, uniform
from typing import Optional

from glitch_this import ImageGlitcher
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps
from telethon import events, functions, types
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.types import DocumentAttributeFilename

from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY, bot
from userbot.events import register
from userbot.utils import progress

Glitched = TEMP_DOWNLOAD_DIRECTORY + "glitch.gif"

EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "]+"
)


@register(outgoing=True, pattern=r"^\.glitch(?: |$)(.*)")
async def glitch(event):
    if not event.reply_to_msg_id:
        await event.edit("`I Wont Glitch A Ghost!`")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit("`reply to a image/sticker`")
        return
    await event.edit("`Downloading Media..`")
    if reply_message.photo:
        glitch_file = await bot.download_media(
            reply_message,
            "glitch.png",
        )
    elif (
        DocumentAttributeFilename(file_name="AnimatedSticker.tgs")
        in reply_message.media.document.attributes
    ):
        await bot.download_media(
            reply_message,
            "anim.tgs",
        )
        os.system("lottie_convert.py anim.tgs anim.png")
        glitch_file = "anim.png"
    elif reply_message.video:
        video = await bot.download_media(
            reply_message,
            "glitch.mp4",
        )
        extractMetadata(createParser(video))
        os.system("ffmpeg -i glitch.mp4 -vframes 1 -an -s 480x360 -ss 1 glitch.png")
        glitch_file = "glitch.png"
    else:
        glitch_file = await bot.download_media(
            reply_message,
            "glitch.png",
        )
    try:
        value = int(event.pattern_match.group(1))
        if value > 8:
            raise ValueError
    except ValueError:
        value = 2
    await event.edit("```Glitching This Media..```")
    await asyncio.sleep(2)
    glitcher = ImageGlitcher()
    img = Image.open(glitch_file)
    glitch_img = glitcher.glitch_image(img, value, color_offset=True, gif=True)
    DURATION = 200
    LOOP = 0
    glitch_img[0].save(
        Glitched,
        format="GIF",
        append_images=glitch_img[1:],
        save_all=True,
        duration=DURATION,
        loop=LOOP,
    )
    await event.edit("`Uploading Glitched Media..`")
    c_time = time.time()
    nosave = await event.client.send_file(
        event.chat_id,
        Glitched,
        force_document=False,
        reply_to=event.reply_to_msg_id,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, event, c_time, "[UPLOAD]")
        ),
    )
    await event.delete()
    os.remove(Glitched)
    await bot(
        functions.messages.SaveGifRequest(
            id=types.InputDocument(
                id=nosave.media.document.id,
                access_hash=nosave.media.document.access_hash,
                file_reference=nosave.media.document.file_reference,
            ),
            unsave=True,
        )
    )
    os.remove(glitch_file)
    os.system("rm *.tgs *.mp4")


@register(outgoing=True, pattern=r"^\.mmf (.*)")
async def memify(event):
    reply_msg = await event.get_reply_message()
    input_str = event.pattern_match.group(1)
    await event.edit("`Processing...`")

    if not reply_msg:
        return await event.edit("`Reply to a message containing media!`")

    if not reply_msg.media:
        return await event.edit("`Reply to an image/sticker/gif/video!`")

    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)

    input_file = await event.client.download_media(reply_msg, TEMP_DOWNLOAD_DIRECTORY)
    input_file = os.path.join(TEMP_DOWNLOAD_DIRECTORY, os.path.basename(input_file))

    if input_file.endswith(".tgs"):
        await event.edit("`Extracting first frame...`")
        converted_file = os.path.join(TEMP_DOWNLOAD_DIRECTORY, "meme.webp")
        cmd = f"lottie_convert.py --frame 0 {input_file} {converted_file}"
        await runcmd(cmd)
        os.remove(input_file)
        if not os.path.lexists(converted_file):
            return await event.edit("`Couldn't parse this animated sticker.`")
        input_file = converted_file

    elif input_file.endswith(".mp4"):
        await event.edit("`Extracting first frame...`")
        converted_file = os.path.join(TEMP_DOWNLOAD_DIRECTORY, "meme.png")
        await take_screen_shot(input_file, 0, converted_file)
        os.remove(input_file)
        if not os.path.lexists(converted_file):
            return await event.edit("`Couldn't parse this video.`")
        input_file = converted_file

    await event.edit("`Adding text...`")
    try:
        final_image = await add_text_img(input_file, input_str)
    except Exception as e:
        return await event.edit(f"**An error occurred:**\n`{e}`")
    await event.client.send_file(
        entity=event.chat_id, file=final_image, reply_to=reply_msg
    )
    await event.delete()
    os.remove(final_image)
    os.remove(input_file)


async def add_text_img(image_path, text):
    font_size = 12
    stroke_width = 2

    if ";" in text:
        upper_text, lower_text = text.split(";")
    else:
        upper_text = text
        lower_text = ""

    img = Image.open(image_path).convert("RGBA")
    img_info = img.info
    image_width, image_height = img.size
    font = ImageFont.truetype(
        font="userbot/utils/styles/MutantAcademyStyle.ttf",
        size=int(image_height * font_size) // 100,
    )
    draw = ImageDraw.Draw(img)

    char_width, char_height = font.getsize("A")
    chars_per_line = image_width // char_width
    top_lines = textwrap.wrap(upper_text, width=chars_per_line)
    bottom_lines = textwrap.wrap(lower_text, width=chars_per_line)

    if top_lines:
        y = 10
        for line in top_lines:
            line_width, line_height = font.getsize(line)
            x = (image_width - line_width) / 2
            draw.text(
                (x, y),
                line,
                fill="white",
                font=font,
                stroke_width=stroke_width,
                stroke_fill="black",
            )
            y += line_height

    if bottom_lines:
        y = image_height - char_height * len(bottom_lines) - 15
        for line in bottom_lines:
            line_width, line_height = font.getsize(line)
            x = (image_width - line_width) / 2
            draw.text(
                (x, y),
                line,
                fill="white",
                font=font,
                stroke_width=stroke_width,
                stroke_fill="black",
            )
            y += line_height

    final_image = os.path.join(TEMP_DOWNLOAD_DIRECTORY, "memify.webp")
    img.save(final_image, **img_info)
    return final_image


async def runcmd(cmd: str) -> tuple[str, str, int, int]:
    """run command in terminal"""
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )


async def take_screen_shot(
    video_file: str, duration: int, path: str = ""
) -> Optional[str]:
    """take a screenshot"""
    ttl = duration // 2
    thumb_image_path = path or os.path.join(
        TEMP_DOWNLOAD_DIRECTORY, f"{os.path.basename(video_file)}.png"
    )
    command = f'''ffmpeg -ss {ttl} -i "{video_file}" -vframes 1 "{thumb_image_path}"'''
    err = (await runcmd(command))[1]
    return thumb_image_path if os.path.exists(thumb_image_path) else err


CMD_HELP.update(
    {
        "glitch": "✘ Pʟᴜɢɪɴ : Glitch"
        "\n\n⚡𝘾𝙈𝘿⚡: `.glitch <1-8>`"
        "\n↳ : Reply Ke Sticker/Gambar.\nGlitch Level 1-8. Jika Tidak Membuat Level Maka Otomatis Default Level 2"
    }
)

CMD_HELP.update(
    {
       "memify": "✘ Pʟᴜɢɪɴ : Memify"
       "\n\n⚡𝘾𝙈𝘿⚡: `.mmf [Text Atas] ; [Text Bawah`]"
       "\n↳ : Reply Ke Sticker/Image/Gif."
    }
)

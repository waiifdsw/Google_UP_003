import asyncio, re
from datetime import datetime, timedelta

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup
from yt_dlp.utils import DownloadError, ExtractorError

from bot.config import config, user_time, Messages, BotCommands
from bot.helpers.utils import CustomFilters
from bot.helpers.ffmfunc import fetch_thumb
from bot.helpers.ytdlfunc import extract_formats


ytregex = re.compile(
    r"^((?:https?:)?//)?((?:www|m)\.)?(youtube\.com|youtu.be)(/(?:[\w\-]+\?v=|embed/|v/)?)([\w\-]+)(\S+)?$"
)

#@Client.on_message(filters.regex(ytregex))
@Client.on_message(filters.incoming & filters.private & filters.command(BotCommands.YtDl) & CustomFilters.auth_users)
async def ytdl(_, message):
    
    user_id = message.from_user.id

    if "/ytdl" in message.text:
        if len(message.command) and len(message.command) <= 1:
            sent_message = await message.reply_text('**Error**', quote=True)
            return
        else:
            url = message.command[1].strip()
    else:
        url = message.text.strip()
    userLastDownloadTime = user_time.get(user_id)
    if userLastDownloadTime and userLastDownloadTime > datetime.now():
        wait_time = round(
            (userLastDownloadTime - datetime.now()).total_seconds() / 60, 2
        )
        await message.reply_text(f"`Wait {wait_time} Minutes before next Request`")
        return

    await message.reply_chat_action("typing")
    try:
        video_id, thumbnail_url, title, buttons = await extract_formats(url)

        now = datetime.now()
        user_time[user_id] = now + timedelta(minutes=config.TIMEOUT)

    except (DownloadError, ExtractorError) as error:
        await asyncio.gather(
            message.reply_chat_action("cancel"),
            message.reply_text(f"{error}", quote=True, disable_web_page_preview=True),
        )
        return

    status = await message.reply_text("Fetching thumbnail...", quote=True)
    if config.CUSTOM_THUMB:
        await asyncio.sleep(config.EDIT_TIME)
        await status.edit_text("Found Custom thumbnail, Gotta pull it now.")
        thumbnail_url = config.CUSTOM_THUMB
    thumbnail = await fetch_thumb(user_id, thumbnail_url, video_id)
    try:
        await asyncio.gather(
            message.reply_photo(
                thumbnail, caption=title, reply_markup=InlineKeyboardMarkup(buttons), quote=True
            ),
            status.delete(),
        )
    except Exception as e:
        await status.edit(f"<code>{e}</code> #Error")

import os, shutil, time, asyncio, logging, subprocess, datetime, functools
from concurrent.futures import ThreadPoolExecutor
from mega import Mega
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import DOWNLOAD_DIRECTORY

logger = logging.getLogger(__name__)

# Mega Client
mega = Mega()
m = mega.login()

# path we gonna give the download
basedir = DOWNLOAD_DIRECTORY

# Automatic Url Detect (From OneDLBot)
MEGA_REGEX = (r"^((?:https?:)?\/\/)"
              r"?((?:www)\.)"
              r"?((?:mega\.nz))"
              r"(\/)([-a-zA-Z0-9()@:%_\+.~#?&//=]*)([\w\-]+)(\S+)?$")

# https://stackoverflow.com/a/64506715
def run_in_executor(_func):
    @functools.wraps(_func)
    async def wrapped(*args, **kwargs):
        loop = asyncio.get_event_loop()
        func = functools.partial(_func, *args, **kwargs)
        return await loop.run_in_executor(executor=ThreadPoolExecutor(), func=func)
    return wrapped

@run_in_executor
def download_mega(url, alreadylol):
  magapylol = m.download_url(url, alreadylol)
  return magapylol



async def megadl(client, message, sent_message):

    url = message.text
    user = f'[Upload Done!](tg://user?id={message.from_user.id})'
    userpath = str(message.from_user.id)
    alreadylol = basedir + userpath
    if not os.path.isdir(alreadylol):
        megadldir = os.makedirs(alreadylol)
    try:
        await sent_message.edit(f"**Downloading:**\n\n`{url}`")
        magapylol = await download_mega(url, alreadylol)
        return str(magapylol)
    except Exception as e:
        await sent_message.edit(f"**Error:** `{e}`")
        shutil.rmtree(basedir + "/" + userpath)
        return "error"

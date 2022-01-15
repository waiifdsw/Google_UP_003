import os
import shutil
#import filetype
#import moviepy.editor
import time
import asyncio
import logging
import subprocess
import datetime
from mega import Mega
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
#from hurry.filesize import size
#from megadl.progress import progress_for_pyrogram, humanbytes
#from megadl.forcesub import handle_force_subscribe
#from config import Config
#from megadl.file_handler import send_to_transfersh_async, progress
from bot import DOWNLOAD_DIRECTORY

# Logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

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



#@Client.on_message(filters.regex(MEGA_REGEX) & filters.private & filters.incoming & ~filters.edited)
async def megadl(client, message, sent_message):

    url = message.text
    user = f'[Upload Done!](tg://user?id={message.from_user.id})'
    userpath = str(message.from_user.id)
    alreadylol = basedir + userpath
    if not os.path.isdir(alreadylol):
        megadldir = os.makedirs(alreadylol)
    try:
        await sent_message.edit(f"**Downloading:**\n\n`{url}`")
        magapylol = m.download_url(url, alreadylol)
        return str(magapylol)
    except Exception as e:
        await sent_message.edit(f"**Error:** `{e}`")
        shutil.rmtree(basedir + "/" + userpath)
        magapylol = "error"
        return magapylol

import os, wget, glob, functools, logging
from concurrent.futures import ThreadPoolExecutor
from pySmartDL import SmartDL
from urllib.error import HTTPError
from youtube_dl import DownloadError
from bot import DOWNLOAD_DIRECTORY

logger = logging.getLogger(__name__)

# https://stackoverflow.com/a/64506715
def run_in_executor(_func):
    @functools.wraps(_func)
    async def wrapped(*args, **kwargs):
        loop = asyncio.get_event_loop()
        func = functools.partial(_func, *args, **kwargs)
        return await loop.run_in_executor(executor=ThreadPoolExecutor(), func=func)
    return wrapped

@run_in_executor
def download_file2(url, dl_path):
  
  sw1 = "aaa"
  dl = SmartDL(url, dl_path, progress_bar=False)
  logger.info(f'Downloading: {url} in {dl_path}')
  dl.start()
  dl.get_dest()
  if os.path.exists(dl_path):
    return True, dl_path
  else:
    sw1 = "bbb"
  
  if sw1 == "bbb":
    wget.download(url, dl_path)
    if os.path.exists(dl_path):
      return True, dl_path
    else:
      return False, "Erorr"


import os
from pathlib import Path

from yt_dlp import YoutubeDL

def download_audio(url: str, path: Path or str):
    path = Path(path)
    parent_path = path.parent

    # ensuring requested path exists
    if not parent_path.is_dir():
        os.makedirs(parent_path) # create it if it doesn't

    opts = {'quiet': True, 'format': 'm4a/bestaudio/best', 'outtmpl': str(path), 'postprocessors': [
        { 'key': 'FFmpegExtractAudio', 'preferredcodec':'flac', },
        ], }
    YoutubeDL(opts).download([url])

    file_format = opts['postprocessors'][0]['preferredcodec']
    new_path = Path(f'{path}.{file_format}')

    return new_path 

from yt_dlp import YoutubeDL
from .video_object import MediaObject

def download_audio(media_object: MediaObject):
    try:
        url = media_object.url
        opts = {'quiet': True, 'format': 'm4a/bestaudio/best',  'postprocessors': [
            { 'key': 'FFmpegExtractAudio', 'preferredcodec':'m4a', },
            ], }
            YoutubeDL(opts).download([url])
    except:
        return

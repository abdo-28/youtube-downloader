from backend import UrlManagerClass, MediaObject
from datetime import date
import base64

urls = [
        'https://music.youtube.com/watch?v=bDlEN5tDMtg&si=dGAzSs3UshTsXD76'
        ]

#url_manager = UrlManagerClass(urls)
#url_manager.download_videos('dest')
media_object = MediaObject(urls[0])

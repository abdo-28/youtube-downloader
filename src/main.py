from backend import UrlManagerClass

urls = [
        'https://music.youtube.com/watch?v=bDlEN5tDMtg&si=dGAzSs3UshTsXD76'
        ]

url_manager = UrlManagerClass(urls)
url_manager.download_videos('dest')

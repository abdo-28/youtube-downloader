import re
from urllib.parse import urlparse

from yt_dlp import YoutubeDL

from . import opts

def parse_url(url) -> str:
    '''
    checks wether the url is a video url, and if it isn't, extract all content in it
    returns Null if it couldn't parse the url and raises an error if it isn't an https link
    '''
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme
    netloc = parsed_url.netloc
    path = parsed_url.path

    if scheme == "https":
        if "youtube" in netloc:
            match path:
                case "/watch":
                    return url 
                case "/playlist":
                    # parse the playlist url for all urls inside it and return them as a tuple

                    # fetching the entries in the playlist
                    entries = YoutubeDL(opts).extract_info(url, download=False)['entries']
                    urls = list() 
                    for entry in entries:
                        entry_url = parsed_url
                        entry_url = entry_url._replace(path="/watch",query=f'v={entry['id']}')
                        urls.append(entry_url.geturl())
                    return urls
                case _:
                    if bool(re.search('/channel', path)):
                        # search the content of the channel and return a url list of all the channel's content
                        return url
                    else:
                        return Null
    else:
        raise ValueError("This function only supports https scheme")

from datetime import date
from pathlib import Path
import json

from backend import MediaObject, download_audio, embed_metadata, parse_url 

entries = list()

with open('download.json') as f:
    urls = json.load(f)

for url in urls:
    result = parse_url(url)
    if result is list or result is tuple:
        entries.extend(result)
    else:
        entries.append(result)

for i in entries:
    print(f'Downloading -> {i}')

    media_object = MediaObject(i)

    metadata = media_object.selected_metadata_object
    media_object.media_file = Path('Music', metadata.artist, metadata.album, metadata.title)

    url = media_object.source
    path = media_object.media_file
    new_path = download_audio(url,path)
    embed_metadata(new_path,metadata)
    print('Done')

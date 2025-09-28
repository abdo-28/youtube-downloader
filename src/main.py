from datetime import date
from pathlib import Path
import json

from backend import MediaObject, download_audio, embed_metadata

with open('download.json') as f:
    urls = json.load(f)

for i in urls:
    print(f'Downloading -> {i}')
    media_object = MediaObject(i)

    metadata = media_object.selected_metadata_object
    if type(metadata.artist) is list:
        artist = metadata.artist[0]
    elif type(metadata.artist) is str:
        artist = metadata.artist

    media_object.media_file = Path('Music', artist, metadata.album, metadata.title)

    url = media_object.source
    path = media_object.media_file
    new_path = download_audio(url,path)
    embed_metadata(new_path,metadata)

    print('Done')

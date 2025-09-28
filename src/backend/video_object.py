import base64
from dataclasses import dataclass, field
from pathlib import Path
from urllib.request import urlopen

from yt_dlp import YoutubeDL

from .metadata import Metadata


@dataclass
class MediaObject:
    source: str
    media_file: Path = field(default=Path('.'))
    metadata: list[Metadata] = field(default_factory=list)
    selected_metadata_object: Metadata = field(init=False,repr=False)

    def __post_init__(self) -> None:
        self.__fetch_metadata()
        self.select_metadata_object()

    def __fetch_metadata(self) -> None:
        '''internal function to fetch metadata based on the url passed to the media object'''
        metadata = YoutubeDL({'quiet': True}).extract_info(url=self.source, download=False)

        thumbnail = urlopen(metadata['thumbnail']).read() 
        cover_art = base64.b64encode(thumbnail)
        
        metadata_object = Metadata(
            title=metadata['title'],
            album=metadata['album'] or metadata['playlist'],
            artist=metadata['artists'][0] or metadata['uploader'],
            artists=metadata['artists'],
            comment=metadata['description'],
            date=metadata['release_date'] or metadata['release_year'] or metadata['upload_date'],
            cover_art=cover_art,
            )
        
        self.add_metadata_object(metadata_object)

    def add_metadata_object(self, metadata_object: Metadata) -> None:
        '''Add a new metadata object to the list of metadata objects'''

        if type(metadata_object) == Metadata:
            self.metadata.append(metadata_object)
            return

        elif type(metadata_object) == List:
            for object in metadata_object:
                if type(object) == Metadata:
                    self.metadata.append(metadata_object)
                else:
                    break
                return
        raise TypeError("Method only accepts a Metadata object or a List of Metadata objects")

    def select_metadata_object(self, id: int = 0) -> None:
        '''Select metadata object to be used for any further processing

        (embeding metadata, lookups based on current metadata object, etc)
        '''
        self.selected_metadata_object = self.metadata[id]

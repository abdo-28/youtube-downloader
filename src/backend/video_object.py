import base64
from dataclasses import dataclass, field
from pathlib import Path
from urllib.request import urlopen

from yt_dlp import YoutubeDL

from backend import Metadata

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
        cover_art = base64.b64encode(thumbnail) if type(thumbnail) is bytes else None
        
        # album
        for i in ('album', 'playlist'):
            if i in metadata:
                album=metadata[i]
                break
            else:
                album=None
#        if album is None: album='Singles' 

        # artist
        for i in ('artists', 'uploader'):
            if i in metadata:
                if i == 'artists':
                    artist=metadata[i][0]
                    break
                else:
                    artist=metadata[i]
                    break
            else:
                artist=None
#        if artist is None: artist='Unknown'

        # date
        date=None
        for i in ('release_date', 'release_year', 'upload_date'):
            if i in metadata:
                date=metadata[i]
                break

        metadata_object = Metadata(
            title=metadata['title'],
            album=album,
            artist=artist,
            comment=metadata['description'],
            date=date,
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

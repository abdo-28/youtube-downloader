import base64
from pathlib import Path
from tempfile import gettempdir
from urllib.request import urlretrieve

from yt_dlp import YoutubeDL

from dataclasses import dataclass, field
from .metadata import Metadata


@dataclass
class MediaObject:
    url: str
    metadata: list[Metadata] = field(init=False)

    def __post_init__(self) -> None:
        self.metadata = self.fetch_metadata()

    def fetch_metadata(self):
        metadata = YoutubeDL().extract_info(url=self.url,download=False)

        cover_art = base64.b64encode(
                open(str(urlretrieve(
                    metadata['thumbnail'],
                    Path(gettempdir(), 'thumbnail')
                    )[0]),
                    'rb'
                ).read()
                )

        metadata_object = Metadata(
            title=metadata['title'],
            album=metadata['album'],
            artist=metadata['uploader'],
            comment=metadata['description'],
            cover_art=cover_art,
            )
        
        return metadata_object

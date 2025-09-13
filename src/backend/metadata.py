from dataclasses import dataclass, field
from datetime import date

@dataclass
class Metadata:
    title: str
    album: str
    artist: str
    comment: str
    cover_art: bytes = field(repr=False)

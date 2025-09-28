from pathlib import Path

from mutagen import File
from mutagen.flac import FLAC, Picture

from .metadata import Metadata

def embed_metadata(path: Path, metadata: Metadata) -> None:
    # load file to be edited
    file = File(path)
    
    # passing metadata from the MediaObject to the file
    file['TITLE'] = metadata.title
    file['ALBUM'] = metadata.album
    file['ARTIST'] = metadata.artist
    file['COMMENT'] = metadata.comment
    file['DATE'] = metadata.date

    if metadata.artists is not None:
        file['ARITSTS'] = metadata.artists
    
    # filetype specific embedding
    if type(file) == FLAC:
	    # create picture object of the cover art
        cover_art = Picture()
        # BytesIO of cover_art
        image = metadata.get_cover_art_file().getvalue()
#        image = open('image','rb').read()

        # setting it's attributes
        cover_art.type = 3
        cover_art.mime = 'image/png'
        cover_art.desc = 'Front cover'
        cover_art.data = image
        cover_art.height = 1280
        cover_art.width = 720
	
	    # saving the edits done
        file.add_picture(cover_art)

    # saving the edits done
    file.save()

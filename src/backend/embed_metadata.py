from pathlib import Path

from mutagen import File
from mutagen.flac import FLAC, Picture

from backend import Metadata

def embed_metadata(path: Path, metadata: Metadata) -> None:
    # load file to be edited
    file = File(path)
    
    # passing metadata from the Metadata object to the file
    for field in (
            ('COMMENT', 'comment'),
            ('TITLE', 'title'),
            ('ALBUM', 'album'),
            ('ARTIST', 'artist'),
            ('DATE', 'date'),
            ):
        attr = getattr(metadata,field[1])
        if attr is not None:
            file[field[0]] = attr

    # filetype specific embedding
    if type(file) == FLAC:
        # BytesIO of cover_art
        image = metadata.get_cover_art_file()
        if image is not None:
	        # create picture object of the cover art
            cover_art = Picture()

            # setting it's attributes
            cover_art.type = 3
            cover_art.mime = 'image/png'
            cover_art.desc = 'Front cover'
            cover_art.data = image.getvalue()
            cover_art.height = 1280
            cover_art.width = 720
    	
    	    # saving the edits done
            file.add_picture(cover_art)

    # saving the edits done
    file.save()

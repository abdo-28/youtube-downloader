import base64
from dataclasses import dataclass, field
import datetime
from io import BytesIO

from PIL import Image

@dataclass
class Metadata:
    title: str or None
    album: str or None
    artist: str or None
    comment: str or None
    date: str or int or datetime.date or None
    cover_art: bytes = field(repr=False) or None

    def __post_init__(self):
        if self.cover_art is not None:
            self.cover_art = self.__cropping_image(self.cover_art)
            self.cover_art = self.__converting_image(self.cover_art)

        # processing date
        if self.date is not None:
            date = list(self.date) 

            year = int(''.join(date[0:4]))

            if len(date) > 4:
                month, day = int(''.join(date[4:6])), int(''.join(date[6:8]))

            self.date = str(datetime.date(year, month, day))

    def __cropping_image(self, file):
        '''
        cropping cover art to 1:1 ratio at the center
        '''
        # preparing the image
        foo = BytesIO(base64.b64decode(file))
        image = Image.open(foo)
        
        # setting some needed values for cropping
        width,height = image.size
        center_pos=(width/2,height/2) # cropping pos starts from the top left of the image
        length=height
        
        center_crop_cordinates=(center_pos[0]-length/2, # left
                                center_pos[1]-length/2, # top
                                center_pos[0]+length/2, # right
                                center_pos[1]+length/2) # bottom

        # actually cropping the image
        image = image.crop(center_crop_cordinates)
        
        # creating empty BytesIO object
        cropped_image = BytesIO()
        image.save(cropped_image,'PNG')
        return base64.b64encode(cropped_image.getbuffer())

    def __converting_image(self, file: bytes) -> bytes:
        '''
        converting images to png to simplify operations
        '''
        foo = BytesIO(base64.b64decode(file))
        image = Image.open(foo)
        converted_image = BytesIO()
        image.save(converted_image,'PNG')
        return base64.b64encode(converted_image.getbuffer())

    def get_decoded_cover_art(self):
        return base64.b64decode(self.cover_art) if self.cover_art is not None else None

    def get_cover_art_file(self):
        return BytesIO(self.get_decoded_cover_art()) if self.cover_art is not None else None

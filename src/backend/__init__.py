opts = {'quiet': True} # universal options for YoutubeDL

from .metadata import Metadata
from .video_object import MediaObject
from .sort_urls import parse_url 
from .download_audio import download_audio
from .embed_metadata import embed_metadata

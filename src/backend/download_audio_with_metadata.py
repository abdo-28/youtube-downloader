from .embed_metadata import embed_metadata
from .download_audio import download_audio
from .video_object import MediaObject

def download_audio_with_metadata(media_object: MediaObject):
    download_audio(media_object)
    embed_metadata()

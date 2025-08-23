from pathlib import Path
from tempfile import gettempdir
from urllib.request import urlretrieve

from yt_dlp import YoutubeDL

class UrlManagerClass:
    '''
        class to handle querying youtube urls, editing information of said urls and downloading them
    '''
    def __init__(self, urls: list):
        self.default_params = { 'quiet': True, 'no_warnings': True }

        # a list to store all relevant info about each url added
        self.info = []
        self.add_video_url(urls)


    def add_video_url(self, items: str):
        ''' 
            fetches the required information and metadata of a url and stores it 
        '''

        # defining a function to simplify behavior of the for loop later on
        def process(url):
            # paramaters for query object
            params = {
                    }.update(self.default_params)
            yt_dlp_query_object = YoutubeDL(params=self.default_params) # object to query for the requested info
            video_info = yt_dlp_query_object.extract_info(url=url, download=False)
#            video_formats = YoutubeDL({'listformats': True}.update(default_params)).extract_info(url=url, download=False)
            video_formats = 'test'
            
            metadata = dict(
                        title=video_info['title'],
                        artist=video_info['uploader'],
                        author=video_info['uploader'],
                        album=video_info['uploader'],
                        thumbnail=video_info['thumbnail'],
                        thumbnails=video_info['thumbnails'],
                        comment=video_info['description'],
                        )

            paramaters = dict(
                        extension=video_info['ext'],
                        extract_audio=True,
                        embed_metadata=True
                        )

            video_dict = dict(
                    id=len(self.info)+1,
                    url=url,
                    available_formats=video_formats,
                    metadata=metadata,
                    params=paramaters
                    )
            self.info.append(video_dict)

        # what to do whether the url passed is a tuple/list or a string
        if type(items) == str:
            process(items)
        elif type(items) == list or tuple:
            for item in items:
                process(item)


    def request_video_info(self, id: int):
        for url in self.info:
            if url['id'] != id:
                continue
            return url
        return None


    def set_video_metadata(self, id: int, new_info: dict):
        for url in self.info:
            if url['id'] == id:
                index = self.info.index(url)
                url['metadata'].update(new_info)
                self.info.pop(index)
                self.info.insert(index, url)
                self.set_video_paramaters(id, {'embed_metadata': True})


    def set_video_paramaters(self, id: int, new_info: dict):
        for url in self.info:
            if url['id'] == id:
                index = self.info.index(url)
                url['paramaters'].update(new_info)
                self.info.pop(index)
                self.info.insert(index, url)


    def download_video(self, id, dest):
        info = self.request_video_info(id)        
        download_params = dict() 

        # embedding metadata
        if info['params']['embed_metadata'] == True:
            metadata = info['metadata']
            path = Path(gettempdir(), 'thumbnail')
            thumbnail = urlretrieve(metadata['thumbnail'],path)
            params = dict(
                    postprocessors=[{
                            'key': 'FFmpegMetadata',
                        'add_metadata': True
                            }],
                    postprocessor_args=[
                        '-metadata',f'title={metadata['title']}',
                        '-metadata',f'artist={metadata['artist']}',
                        '-metadata',f'album={metadata['album']}',
                        '-metadata',f'cover={thumbnail}',
                        ]
                    )
            download_params.update(params)

        if info['params']['extract_audio'] == True:
            params = dict(format='m4a/bestaudio/best',postprocessors=[{'key': 'FFmpegExtractAudio','preferredcodec': 'm4a'}])
            download_params.update(params)

        yt_dlp_download_object = YoutubeDL(params=download_params)
        yt_dlp_download_object.download(info['url'])


    def download_videos(self, destination: str):
        for item in self.info:
            self.download_video(item['id'],destination)

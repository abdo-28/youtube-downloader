def download_youtube_audio(url):
    info = YoutubeDL({'quiet': True}).extract_info(url, download=False)
    urlretrieve(info['thumbnail'], 'cover.webp')
    thumbnail = 'cover.webp'

    opts = {
    'quiet': True,
    'format': 'm4a/bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec':'m4a',
        },
        {
        'key':'FFmpegMetadata',
        'add_metadata':True,
        },
        ],
    'postprocessor_args': [
        '-metadata', f'title={info['title']} goes hard',
        '-metadata', 'description= ',
        '-metadata', 'synopsis= ',
        '-metadata', f'cover={thumbnail}',
    ],
    }

    YoutubeDL(opts).download([url])

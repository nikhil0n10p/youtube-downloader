from pytube import YouTube


def get_video_options(yt):
    """
    Get the pytube.YouTube() instance video download options
    :param yt: pytube.YouTube(link) instance
    :return: sorted list of qualities ordered by resolution
    """
    delay = 3
    retries = 3
    video_options = []
    progressive_streams = yt.streams.filter(progressive=True).order_by("resolution")
    for res in progressive_streams:
        if res is not None:
            filesize_in_bytes = res.filesize
            filesize_in_kb = filesize_in_bytes / 1024
            formatted_filesize = "{:.1f}".format(filesize_in_kb / 1024)
            video_options.append(res.resolution + ' ' + formatted_filesize + 'MB')

    quality_1080p = yt.streams.filter(resolution="1080p").first()
    if quality_1080p is not None:
        filesize_in_bytes = quality_1080p.filesize
        filesize_in_kb = filesize_in_bytes / 1024
        formatted_filesize = "{:.1f}".format(filesize_in_kb / 1024)
        video_options.append(quality_1080p.resolution + ' ' + formatted_filesize + 'MB')

    return video_options


def get_only_filesize(url, res_code=None):
    """
    Get the video link with specefic quality file size
    :param url: YouTube Video URL
    :param res_code: Resolution Code (1080p,etc... or vc for audio)
    :return: The filzesize of the YouTube Video
    """
    yt = YouTube(url=url)
    if res_code == "1080p":
        filesize = yt.streams.filter(resolution="1080p").first().filesize_mb
    elif res_code == "vc":
        filesize = yt.streams.filter(only_audio=True).last().filesize_mb
    else:
        filesize = yt.streams.filter(resolution=res_code, progressive=True).first().filesize_mb

    return filesize

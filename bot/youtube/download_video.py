import os

import jdatetime
from bot.common.utils import replace_invalid_characters_with_underscore
from pytube import YouTube
import subprocess


def download_yt_video(link, quality):
    """
    This function download the YouTube Link with the specefic quality
    :param link: YouTube Video Link
    :param quality: Wanted Quality (1080p,etc... or vc for audio)
    :return: The Downloaded Video Path In Disk
    """
    yt = YouTube(link)
    datetime = jdatetime.datetime.now().strftime("%Y%m%d%H%M%S")
    download_video_dir = "/videos/"

    def download_stream(stream, filename):
        stream.download(output_path=download_video_dir, filename=filename)
        return os.path.join(download_video_dir, filename)

    if quality == "vc":
        audio = yt.streams.filter(only_audio=True).last()
        if audio is not None:
            audio_title = replace_invalid_characters_with_underscore(yt.title)
            audio_path = download_stream(audio, f"{audio_title} {datetime}.mp3")
            return audio_path

    if quality != "1080p":
        video = yt.streams.filter(resolution=quality, progressive=True).first()
        video_title = replace_invalid_characters_with_underscore(yt.title)
        video_path = download_stream(video, f"{video_title} {datetime}.mp4")
        return video_path

    # if quality == "1080p":
    #     video_title = replace_invalid_characters_with_underscore(yt.title)
    #     output_path = os.path.join(download_video_dir, f"{video_title} {datetime}.mp4")
    #     command = [
    #         'yt-dlp',
    #         '-f', 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
    #         '--merge-output-format', 'mp4',
    #         '-o', output_path,
    #         link
    #     ]
    #     subprocess.run(command)
    #     return output_path

import os

import jdatetime
from bot.youtube.download_video import download_yt_video
from bot.youtube.get_video_information import get_only_filesize
from bot.youtube.send_video import send_video
from config.database import users_collection
from pytube import YouTube


def process_video(msg, bot, link, quality_or_audio, chat_id, user_id):
    """

    :param msg: telebot.types.Message instance
    :param bot: telebot.TeleBot instance
    :param link: YouTube Video Link
    :param quality_or_audio: Resolution code (1080p,etc... or vc for audio)
    :param chat_id: The telegram chat id
    :param user_id: The user id
    :return: it sends the video and save some data in the database if everything is fine
    """
    video_path = download_yt_video(link, quality_or_audio)
    yt = YouTube(link)
    send_video(msg=msg, bot=bot, link=link, chat_id=chat_id, video_path=video_path, user_id=user_id,
               quality=quality_or_audio)
    os.remove(video_path)
    if quality_or_audio != "vc":
        res_code = quality_or_audio
    else:
        res_code = None
    download_entry = {
        "media_title": yt.title,
        "media_link": link,
        "video_audio": quality_or_audio,
        "duration": yt.length,
        "size": get_only_filesize(link, res_code),
        "creator_channel": yt.channel_url,
        "user_subscription": users_collection.find_one({"user_id": user_id})["subscription"][
            'type'],
        "date_time": jdatetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        "date": jdatetime.date.today().strftime("%Y/%m/%d"),
        "time": jdatetime.datetime.now().strftime("%H:%M:%S")
    }
    users_collection.update_one({"user_id": user_id}, {"$push": {"downloads": download_entry}})

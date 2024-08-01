import telebot
from bot.common.button_utils import KeyboardMarkupGenerator
from languages import persian
from pytube import YouTube
from requests.exceptions import ConnectionError
from telebot.apihelper import ApiTelegramException


def send_video(msg: telebot.types.Message, bot: telebot.TeleBot, link, chat_id, video_path, user_id, quality):
    """

    :param msg: telebot.types.Message instance
    :param bot: telebot.TeleBot instance
    :param link: YouTube Video Link
    :param chat_id: The telegram chat id
    :param video_path: The downloaded video path on disk
    :param user_id: The user id
    :param quality: Resolution code (1080p,etc... or vc for audio)
    :return: It send the video if everything is fine
    """
    yt = YouTube(link)
    kb = KeyboardMarkupGenerator(user_id)
    if video_path.endswith((".mp4", ".mp3")):
        keyboard = kb.post_caption_buttons(yt.channel_url, link)
        media_type = "video" if video_path.endswith(".mp4") else "audio"
        publish_date = yt.publish_date.strftime("%Y/%m/%d")
        description = yt.description[:850] if yt.description else ""
        thumbnail_url = yt.thumbnail_url
        if quality == "vc":
            quality = "320kbps"
        caption = persian.caption.format(yt.title, quality, yt.views, description, publish_date)
    try:
        if media_type == "video":
            bot.send_video(chat_id=chat_id, video=open(video_path, "rb"), caption=caption, supports_streaming=True,
                           thumbnail=thumbnail_url, duration=yt.length, reply_markup=keyboard, parse_mode="markdown")
        elif media_type == "audio":
            bot.send_audio(chat_id=chat_id, audio=open(video_path, "rb"), caption=caption, reply_markup=keyboard,
                           parse_mode="markdown")
    except (ConnectionError, ApiTelegramException):
        if ConnectionError:
            bot.send_message(chat_id=chat_id, text=persian.connection_error)
        elif ApiTelegramException:
            bot.send_message(chat_id=chat_id, text=persian.cant_download_larger_than_50mb)

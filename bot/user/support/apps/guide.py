import telebot.types
from languages import persian


def send_guide_message(msg: telebot.types.Message, bot: telebot.TeleBot):
    """
    send guide message to user
    :param msg: telebot.types.Message instance
    :param bot: telebot.TeleBot instance
    """
    bot.send_message(msg.chat.id, persian.guide, parse_mode="Markdown", disable_web_page_preview=True)

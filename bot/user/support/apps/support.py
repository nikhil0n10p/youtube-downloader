import re

import telebot.types
from bot.common.button_utils import KeyboardMarkupGenerator
from config.database import users_collection
from languages import persian
from config.tokens import support_group_id

def join_in_support(msg: telebot.types.Message, bot: telebot.TeleBot):
    """
    join in support (set metadata.joined_in_support to True) to let the user send a message to support
    :param msg: telebot.types.Message instance
    :param bot: telebot.TeleBot instance
    """
    users_collection.update_one({'user_id': msg.from_user.id}, {'$set': {"metadata.joined_in_support": True}})
    bot.send_message(msg.chat.id, persian.youre_connected_to_support,
                     reply_markup=KeyboardMarkupGenerator(msg.from_user.id).return_buttons())


def send_user_msg_to_support(msg: telebot.types.Message, bot: telebot.TeleBot):
    """
    send user message to support group
    :param msg: telebot.types.Message instance
    :param bot: telebot.TeleBot instance
    """
    bot.send_message(chat_id=support_group_id,
                     text=f"Username: {msg.from_user.username}\nUser ID: `{msg.from_user.id}`\nChat ID : `{msg.chat.id}`\nMessage:\n\n {msg.text}",
                     parse_mode="Markdown")
    bot.send_message(chat_id=msg.chat.id, text=persian.your_message_was_sent_to_support,
                     reply_markup=KeyboardMarkupGenerator(msg.from_user.id).homepage_buttons())
    users_collection.update_one({'user_id': msg.from_user.id}, {'$set': {"metadata.joined_in_support": False}})


def send_user_photo_to_support(msg: telebot.types.Message, bot: telebot.TeleBot):
    """
    send user photo to support group
    :param msg: telebot.types.Message instance
    :param bot: telebot.TeleBot instance
    """
    bot.send_photo(chat_id=support_group_id, photo=msg.photo[-1].file_id,
                   caption=f"Username: {msg.from_user.username}\nUser ID: `{msg.from_user.id}`\nChat ID : `{msg.chat.id}`",
                   parse_mode="Markdown")
    bot.send_message(chat_id=msg.chat.id, text=persian.your_message_was_sent_to_support,
                     reply_markup=KeyboardMarkupGenerator(msg.from_user.id).homepage_buttons())
    users_collection.update_one({'user_id': msg.from_user.id}, {'$set': {"metadata.joined_in_support": False}})


def reply_to_user_support_msg(msg: telebot.types.Message, bot: telebot.TeleBot):
    """
    reply to the user message sent to support  (in group)
    :param msg: telebot.types.Message instance
    :param bot: telebot.TeleBot instance
    """
    reply_response_template = persian.reciving_message_from_support
    reply_response = msg.reply_to_message
    if reply_response.text:
        reply_response = reply_response.text
    elif reply_response.caption:
        reply_response = reply_response.caption
    chat_id_match = re.search(r'Chat ID :\s*(\d+)', reply_response)
    if chat_id_match:
        chat_id = chat_id_match.group(1)
        chat_id = chat_id.strip()
        if msg.text:
            bot.send_message(chat_id=chat_id, text=f"{reply_response_template}\n\n{msg.text}")
        elif msg.photo:
            if msg.caption:
                caption = msg.caption
            else:
                caption = ""
            bot.send_photo(chat_id=chat_id, photo=msg.photo[-1].file_id,
                           caption=f"{reply_response_template}\n\n{caption}")

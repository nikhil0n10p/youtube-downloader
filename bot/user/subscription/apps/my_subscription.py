import telebot.types
from bot.user.utils.user_utils import UserManager
from languages import persian


def my_subscription_details(msg: telebot.types.Message, bot: telebot.TeleBot):
    """
    Show my subscription details (type, days, remaining days, etc...)
    :param msg: telebot.types.Message instance
    :param bot: telebot.TeleBot instance
    """
    user_manager = UserManager(msg.from_user.id)
    subscription_data = user_manager.get_user_subscription_details()
    used_data = subscription_data['used_data']
    remaining_data = subscription_data['remaining_data']
    formatted_used_data = "{:.1f}".format(used_data)
    formatted_remaining_data = "{:.1f}".format(remaining_data)
    subscription_type = subscription_data['type']
    type = {"free": "رایگان 🥉", "premium": "پرمیوم 🥇"}
    if subscription_type == "free":
        days = "نامحدود"
        days_left = "نامحدود"
    else:
        days = subscription_data['days']
        days_left = subscription_data['days_left']
    formatted_subscription_type = type[subscription_type]
    max_file_size = subscription_data['max_file_size']
    max_data_per_day = subscription_data['max_data_per_day']
    response = persian.my_subscribtion_details
    response = response.format(formatted_subscription_type, days, days_left, max_file_size, max_data_per_day,
                               formatted_used_data, formatted_remaining_data)

    bot.send_message(msg.chat.id, response, parse_mode='markdown')

import logging
import threading

import telebot
from config.tokens import bot_token

from bot.admin.bot_administration import BotAdministration
from bot.admin.giftcode import generate_code
from bot.admin.user_administration import UserAdministration
from bot.common.utils import modify_daily_data
from bot.handlers.callback_handler import CallbackHandler
from bot.handlers.message_handler import MessageHandler
from bot.handlers.start_handler import StartCommandHandler

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(bot_token, disable_web_page_preview=True)
telebot.apihelper.API_URL = "http://localhost:8081/bot{0}/{1}"

bot.register_message_handler(UserAdministration().send_message_to_premium_users,
                             commands=['send_message_to_premium_users'], pass_bot=True)
bot.register_message_handler(UserAdministration().send_message_to_free_users, commands=['send_message_to_free_users'],
                             pass_bot=True)
bot.register_message_handler(UserAdministration().send_message_to_all_users, commands=['send_message_to_all'],
                             pass_bot=True)
bot.register_message_handler(UserAdministration().send_message_to_user, commands=['send_message_to_user'],
                             pass_bot=True)
bot.register_message_handler(UserAdministration().include_user_balance, commands=['include_balance'], pass_bot=True)
bot.register_message_handler(StartCommandHandler().process_start_command, commands=["start"], pass_bot=True)
bot.register_message_handler(BotAdministration().admin_commands_help, commands=['admin'], pass_bot=True)
bot.register_message_handler(UserAdministration().get_user_stat, commands=['user_stat'], pass_bot=True)
bot.register_message_handler(BotAdministration().get_bot_stats, commands=['stat'], pass_bot=True)
bot.register_message_handler(generate_code, commands=['generate_giftcode'], pass_bot=True)
bot.register_message_handler(MessageHandler().handle_message, content_types=['text'], pass_bot=True)
bot.register_message_handler(MessageHandler().handle_photo, content_types=['photo'], pass_bot=True)

bot.register_callback_query_handler(CallbackHandler().process_callback, pass_bot=True, func=lambda call: True)

if __name__ == "__main__":
    reset_thread = threading.Thread(target=modify_daily_data)
    reset_thread.start()
    bot.infinity_polling()

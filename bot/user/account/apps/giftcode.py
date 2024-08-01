import jdatetime
import telebot.types
from bot.common.button_utils import KeyboardMarkupGenerator
from config.database import giftcodes_collection, users_collection
from languages import persian


def redeem_giftcode(msg: telebot.types.Message, bot: telebot.TeleBot):
    """
    redeems the giftcode
    :param msg: telebot.types.Message instance
    :param bot: telebot.TeleBot instance
    :return: Charge the account if True
    """
    user = msg.from_user
    code = msg.text
    code_db = giftcodes_collection.find_one({"code": code})
    format_number_with_commas = lambda number: f"{number:,}"
    if code_db:
        if code_db["used"] == False:
            users_collection.update_one({"user_id": user.id}, {"$inc": {"balance": code_db["credit"]}})
            user_new_balance = users_collection.find_one({"user_id": user.id})["balance"]
            giftcodes_collection.update_one({"code": code}, {"$set": {"used": True, "used_by": user.id,
                                                                      "used_date": jdatetime.datetime.now().strftime(
                                                                          "%Y/%m/%d %H:%M:%S")}})
            users_collection.update_one({"user_id": user.id}, {"$set": {"metadata.redeeming_code": False}})
            response = persian.redeem_successful
            user_new_balance = format_number_with_commas(user_new_balance)
            response = response.format(user_new_balance)
            bot.send_message(chat_id=msg.chat.id,
                             text=response,
                             reply_markup=KeyboardMarkupGenerator(user.id).homepage_buttons(), parse_mode="Markdown")
        else:
            bot.send_message(chat_id=msg.chat.id, text=persian.code_already_redeemed)
    else:
        bot.send_message(chat_id=msg.chat.id, text=persian.invalid_giftcode)

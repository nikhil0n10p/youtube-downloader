import random
import string

import jdatetime
import telebot
from config.database import giftcodes_collection


def generate_code(msg: telebot.types.Message, bot: telebot.TeleBot):
    """
    Generate giftcode
    :param msg: telebot.types.Message instance
    :param bot: telebot.TeleBot instance
    :return: the generated code
    """
    admin = 1154909190
    if msg.from_user.id == admin:
        code = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(10))
        try:
            credit = msg.text.split()[1]
        except IndexError:
            credit = None
        if not credit:
            bot.send_message(chat_id=msg.chat.id,
                             text="❌ لطفا دستور را به این صورت وارد کنید:\n /generate_giftcode [Credit]")
            return
        try:
            giftcodes_collection.insert_one(
                {"code": code, "credit": int(credit), "created_by": msg.from_user.id, "used": False,
                 "used_by": None,
                 "used_date": None,
                 "create_date": jdatetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")})
            formatted_credit = "{:,}".format(int(credit))
            bot.send_message(chat_id=msg.chat.id,
                             text="✅ کد هدیه با موفقیت ایجاد شد. \nکد: `{}` \nاعتبار: `{}` تومان".format(code,
                                                                                                         formatted_credit),
                             parse_mode="Markdown")
        except ValueError:
            bot.send_message(chat_id=msg.chat.id, text="❌ لطفا اعتبار را به صورت عدد وارد کنید.")
    else:
        pass

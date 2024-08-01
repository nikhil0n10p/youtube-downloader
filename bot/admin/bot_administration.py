import datetime

import jdatetime
import telebot
from config.database import users_collection
from languages import persian
from config.tokens import admin_id

class BotAdministration:
    """
    Bot managing commands
    """

    def __init__(self):
        self.admin = admin_id
        self.today = self._get_today_date()
        self.yesterday = self._get_yesterday_date()
        self.this_week = self._get_this_week_start_date()
        self.this_month = self._get_this_month_start_date()

    def _is_admin(self, user_id):
        """
        Check if the user is admin
        :param user_id: the user id
        :return: True if admins False if not
        """
        return user_id in self.admin

    def _get_today_date(self):
        """
        :return: today jdate (Y/m/d)
        """
        return jdatetime.date.today().strftime("%Y/%m/%d")

    def _get_yesterday_date(self):
        """
        :return: yesterday jdate (Y/m/d)
        """
        yesterday = jdatetime.date.today() - datetime.timedelta(days=1)
        return yesterday.strftime("%Y/%m/%d")

    def _get_this_week_start_date(self):
        """
        :return: the first day of the week jdate (Y/m/d)
        """
        today = jdatetime.date.today()
        this_week_start = today - datetime.timedelta(days=today.weekday())
        this_week_dates = [this_week_start + datetime.timedelta(days=i) for i in range(7)]
        return [date.strftime("%Y/%m/%d") for date in this_week_dates]

    def _get_this_month_start_date(self):
        """
        :return: the first day pf the month jdate (Y/m/d)
        """
        return jdatetime.date.today().replace(day=1).strftime("%Y/%m/%d")

    def get_bot_stats(self, msg: telebot.types.Message, bot: telebot.TeleBot):
        """
        get the bot stats (users, income, etc...)
        :param msg: telebot.types.Message instance
        :param bot: telebot.TeleBot instance
        :return: sends the bot stat message
        """
        if not self._is_admin(msg.from_user.id):
            return

        user_register_date_ranges = {"امروز": {"register_date": self.today}, "دیروز": {"register_date": self.yesterday},
                                     "این هفته": {"register_date": {"$in": self.this_week}},
                                     "این ماه": {"register_date": {"$gte": self.this_month}}, "کل": {}, }

        user_counts = {period: users_collection.count_documents(filter=date_filter) for period, date_filter in
                       user_register_date_ranges.items()}

        response = persian.stats.format(user_counts["امروز"], user_counts["دیروز"], user_counts["این هفته"],
                                        user_counts["این ماه"], user_counts["کل"],
                                        )

        bot.send_message(msg.chat.id, response, parse_mode="Markdown")

    def admin_commands_help(self, msg: telebot.types.Message, bot: telebot.TeleBot):
        """
        :param msg: telebot.types.Message instance
        :param bot: telebot.TeleBot instance
        :return: list of the admins commands
        """
        if not self._is_admin(msg.from_user.id):
            return
        bot.reply_to(msg, persian.admin_commands_help)

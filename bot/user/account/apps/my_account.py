import telebot.types
from bot.common.button_utils import KeyboardMarkupGenerator
from bot.user.utils.user_utils import UserManager
from config.database import users_collection
from languages import persian


class MyAccount:
    def show_account_details(self, msg: telebot.types.Message, bot: telebot.TeleBot):
        """
        show the user account details
        :param msg: telebot.types.Message instance
        :param bot: telebot.TeleBot instance
        :return: Message that shows the user account details
        """
        user = msg.from_user
        format_number_with_commas = lambda number: f"{number:,}"
        user_register_date = users_collection.find_one({"user_id": user.id})["register_date"]
        user_total_downloads = len(users_collection.find_one({"user_id": user.id})["downloads"])
        user_total_downloads_size = sum(i.get("size", 0) for i in
                                        users_collection.find_one({"user_id": user.id}).get("downloads",
                                                                                            [])) if users_collection.find_one(
            {"user_id": user.id}) else 0
        formated_user_total_downloads_size = "{:.1f}".format(user_total_downloads_size)
        formatted_balance = format_number_with_commas(users_collection.find_one({"user_id": user.id})["balance"])
        user_referrals = len(users_collection.find_one({"user_id": user.id})["referrals"])
        formatted_profit = format_number_with_commas(
            users_collection.find_one({"user_id": user.id})["referral_total_profit"])
        buttons = KeyboardMarkupGenerator(user_id=user.id).account_buttons()
        response = persian.account_details.format(user.id, user_register_date, user_total_downloads,
                                                  formated_user_total_downloads_size, formatted_balance, user_referrals,
                                                  formatted_profit)

        bot.send_message(chat_id=msg.chat.id, text=response,
                         reply_markup=KeyboardMarkupGenerator(user.id).account_buttons(), parse_mode="markdown")

    def return_only_user_details_response(self, user_id):
        """
        get user account details
        :param user_id: the user id
        :return: the user account details (dosent send it)
        """
        usermanager = UserManager(user_id)
        format_number_with_commas = lambda number: f"{number:,}"
        user_register_date = users_collection.find_one({"user_id": user_id})["register_date"]
        user_total_downloads = len(users_collection.find_one({"user_id": user_id})["downloads"])
        user_total_downloads_size = sum(i.get("size", 0) for i in
                                        users_collection.find_one({"user_id": user_id}).get("downloads",
                                                                                            [])) if users_collection.find_one(
            {"user_id": user_id}) else 0
        formated_user_total_downloads_size = "{:.1f}".format(user_total_downloads_size)
        formatted_balance = format_number_with_commas(users_collection.find_one({"user_id": user_id})["balance"])
        user_referrals = len(users_collection.find_one({"user_id": user_id})["referrals"])
        formatted_profit = format_number_with_commas(
            users_collection.find_one({"user_id": user_id})["referral_total_profit"])
        response = persian.account_details.format(user_id, user_register_date, user_total_downloads,
                                                  formated_user_total_downloads_size, formatted_balance, user_referrals,
                                                  formatted_profit)
        return response

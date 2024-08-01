import re

import telebot
from bot.common.button_utils import KeyboardMarkupGenerator
from bot.common.plans import Plans
from config.database import users_collection
from languages import persian


class BuySubscription(Plans):
    """
    Buy Subscription App
    """

    def return_to_subscriptions_list(self, msg: telebot.types.Message, bot: telebot.TeleBot, user_id):
        """
        Return to subscriptions list
        :param msg: telebot.types.Message instance
        :param bot: telebot.TeleBot instance
        :param user_id: the user id
        """
        keyboard = KeyboardMarkupGenerator(user_id)
        bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text=persian.subscriptions_list,
                              reply_markup=keyboard.subscriptions_list_buttons())

    def show_subscription_details(self, msg: telebot.types.Message, bot: telebot.TeleBot, subscription, user_id):
        """
        Show the selected subscription plan details
        :param msg: telebot.types.Message instance
        :param bot: telebot.TeleBot instance
        :param subscription: the selected subscription plan
        :param user_id: the user id
        """
        if users_collection.find_one({"user_id": user_id})['subscription']['type'] == 'premium':
            if users_collection.find_one({"user_id": user_id})['subscription']['id'] == 1:
                sub_name = Plans().get_plan_by_id(1)['name']
            elif users_collection.find_one({"user_id": user_id})['subscription']['id'] == 2:
                sub_name = Plans().get_plan_by_id(2)['name']
            return bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id,
                                         text=persian.subscription_already_bought.format(sub_name),
                                         parse_mode='markdown')
        keyboard = KeyboardMarkupGenerator(user_id).subscription_details_buttons(subscription)
        response = persian.subscription_details
        format_number_with_commas = lambda number: f"{number:,}"
        if subscription == 'id_1':
            sub = self.get_plan_by_id(1)
        elif subscription == 'id_2':
            sub = self.get_plan_by_id(2)
        formatted_days = sub['days']
        formatted_max_data_per_day = sub['max_data_per_day'] // 1000
        formatted_max_file_size = sub['max_file_size'] // 1000
        user_balance = users_collection.find_one({"user_id": user_id})['balance']
        formatted_user_balance = format_number_with_commas(user_balance)
        formatted_price = format_number_with_commas(sub['price'])
        discount_percent = sub['discount_percent']
        discount_price = sub['price'] * discount_percent // 100
        formatted_discount_price = format_number_with_commas(discount_price)
        final_price = sub['price'] - discount_price
        formatted_final_price = format_number_with_commas(final_price)
        response = response.format(sub['days'], formatted_max_data_per_day, formatted_max_file_size, formatted_price,
                                   discount_percent,
                                   formatted_discount_price, formatted_user_balance, formatted_final_price)
        bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text=response, reply_markup=keyboard,
                              parse_mode='Markdown')

    def subscriptions_list(self, msg: telebot.types.Message, bot: telebot.TeleBot, user_id):
        """
        Show subscriptions plans list
        :param msg: telebot.types.Message instance
        :param bot: telebot.TeleBot instance
        :param user_id: the user id
        """
        keyboard = KeyboardMarkupGenerator(user_id)
        bot.send_message(msg.chat.id, persian.subscriptions_list, reply_markup=keyboard.subscriptions_list_buttons())

    def buy_via_account_charge(self, msg: telebot.types.Message, bot: telebot.TeleBot, subscription, user_id, msg_id):
        """
        Buy subscription via account charge
        :param msg: telebot.types.Message instance
        :param bot: telebot.TeleBot instance
        :param subscription: the selected subscription plan
        :param user_id: the user id
        :param msg_id: the subscription detail message id (for edit message)
        """
        if re.search("id_1", subscription):
            the_user = users_collection.find_one({"user_id": user_id})
            sub = self.plans[1]
            sub_price = self.id_1_final_price
            user_balance = users_collection.find_one({"user_id": user_id})['balance']
            if user_balance < sub_price:
                keyboard = KeyboardMarkupGenerator(user_id).get_referral_buttons()
                bot.send_message(msg.chat.id, persian.insufficient_balance, reply_markup=keyboard,
                                 parse_mode='Markdown')
                return
            elif user_balance >= sub_price:
                if users_collection.find_one({"user_id": user_id})['subscription']['type'] == "free":
                    users_collection.update_one({"user_id": user_id}, {"$inc": {"balance": -sub_price}})
                    users_collection.update_one({"user_id": user_id}, {"$set": {"subscription": sub}})
                    response = persian.subscription_bought
                    formatted_price = "{:,}".format(sub_price)
                    response = response.format("پرمیوم 30 روزه", formatted_price)
                    bot.edit_message_text(chat_id=msg.chat.id, message_id=msg_id, text=response, parse_mode='Markdown')
                else:
                    response = persian.subscription_already_bought.format("پرمیوم")
                    bot.edit_message_text(chat_id=msg.chat.id, message_id=msg_id, text=response, parse_mode='Markdown')
        elif re.search("id_2", subscription):
            sub = self.plans[2]
            sub_price = self.id_2_final_price
            user_balance = users_collection.find_one({"user_id": user_id})['balance']
            if user_balance < sub_price:
                keyboard = KeyboardMarkupGenerator(user_id).get_referral_buttons()
                bot.send_message(msg.chat.id, persian.insufficient_balance, reply_markup=keyboard,
                                 parse_mode='Markdown')
                return
            elif user_balance >= sub_price:
                if users_collection.find_one({"user_id": user_id})['subscription']['type'] == "free":
                    users_collection.update_one({"user_id": user_id}, {"$inc": {"balance": -sub_price}})
                    users_collection.update_one({"user_id": user_id}, {"$set": {"subscription": sub}})
                    response = persian.subscription_bought
                    formatted_price = "{:,}".format(sub_price)
                    response = response.format("پرمیوم 90 روزه", formatted_price)
                    bot.edit_message_text(chat_id=msg.chat.id, message_id=msg_id, text=response, parse_mode='Markdown')
                else:
                    response = persian.subscription_already_bought.format("پرمیوم")
                    bot.edit_message_text(chat_id=msg.chat.id, message_id=msg_id, text=response, parse_mode='Markdown')

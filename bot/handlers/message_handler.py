import re

import telebot.types
from bot.common.button_utils import KeyboardMarkupGenerator
from bot.handlers.yt_link_handler import YouTubeVideoHandler
from bot.user.account.apps.giftcode import redeem_giftcode
from bot.user.account.apps.my_account import MyAccount
from bot.user.subscription.apps.buy_subscription import BuySubscription
from bot.user.subscription.apps.my_subscription import my_subscription_details
from bot.user.support.apps.guide import send_guide_message
from bot.user.support.apps.support import join_in_support, send_user_msg_to_support, send_user_photo_to_support, \
    reply_to_user_support_msg
from bot.user.utils.user_utils import UserManager
from config.database import users_collection
from languages import persian


class MessageHandler:
    """
    This Class Handle Diffrent Messages From User
    """

    def __init__(self):
        """
        Initialize the MessageHandler class
        """
        self.support_group_id = -4061658551

    def handle_message(self, msg: telebot.types.Message, bot: telebot.TeleBot):
        """

        :param msg: telebot.types.Message instance
        :param bot: telebot.TeleBot instance
        :return: it handles the users message if the user message is text
        """
        self.usermanager = UserManager(msg.from_user.id)
        self.msg = msg
        self.bot = bot
        self.chat_id = msg.chat.id
        self.user_message_text = msg.text
        self.keyboardgenerator = KeyboardMarkupGenerator(msg.from_user.id)
        self.the_user = users_collection.find_one({"user_id": msg.from_user.id})
        # Check if the user is subscribed to the channel
        if not self.usermanager.is_subscribed_to_channel(msg, bot):
            bot.send_message(self.chat_id, persian.subscribe_to_channel,
                             reply_markup=self.keyboardgenerator.subscribe_to_channel_buttons())
            return

        # Check if the user is new and requires a restart
        if not users_collection.find_one({"user_id": msg.from_user.id}):
            bot.reply_to(msg, persian.restart_required)
            return

        # Check if the message is a reply in the support group
        if self.chat_id == self.support_group_id and msg.reply_to_message:
            reply_to_user_support_msg(msg, bot)
            return

        # Check for YouTube video links
        if any(re.search(pattern, self.user_message_text) for pattern in
               [r'https://youtu.be/', r'https://www.youtube.com/watch\?v=', r'https://www.youtube.com/shorts/',
                r'https://youtube.com/shorts/', r'http://youtu.be/', r'http://www.youtube.com/watch\?v=',
                r'http://www.youtube.com/shorts/', r'http://youtube.com/shorts/']):
            YouTubeVideoHandler().process_video(msg, bot)
            return

        # Handle specific commands
        command_handlers = {"↩️ بازگشت": self.handle_return, "🛒 خرید اشتراک": self.handle_buy_subscription,
                            "👤 حساب کاربری": self.handle_account, "📋 اشتراک من": self.handle_my_subscription,
                            "🎁 کد هدیه": self.handle_gift_code, "📖 راهنما": self.handle_guide,
                            "📞 پشتیبانی": self.handle_support}

        # Check if the message corresponds to a known command
        if self.user_message_text in command_handlers:
            command_handlers[self.user_message_text]()
            return

        # Check for other conditions
        if self.the_user['metadata']["redeeming_code"]:
            redeem_giftcode(msg, bot)


        elif self.the_user['metadata']["joined_in_support"]:
            send_user_msg_to_support(msg, bot)

        else:
            bot.reply_to(msg, persian.unknown_request)

    def handle_return(self):
        # Handle the "Return" command
        self.bot.send_message(self.chat_id, persian.returned_to_homepage,
                              reply_markup=self.keyboardgenerator.homepage_buttons())
        for field in ["redeeming_code", "joined_in_support"]:
            users_collection.update_one({"_id": self.the_user["_id"]}, {"$set": {"metadata." + field: False}})

    def handle_buy_subscription(self):
        # Handle the "Buy Subscription" Button
        BuySubscription().subscriptions_list(self.msg, self.bot, self.msg.from_user.id)

    def handle_account(self):
        # Handle the "Account" Button
        MyAccount().show_account_details(self.msg, self.bot)

    def handle_my_subscription(self):
        # Handle the "My Subscription" Button
        my_subscription_details(self.msg, self.bot)

    def handle_gift_code(self):
        # Handle the "Gift Code" Button
        self.bot.send_message(self.chat_id, persian.send_the_giftcode,
                              reply_markup=self.keyboardgenerator.return_buttons())
        users_collection.update_one(filter={"_id": self.the_user["_id"]},
                                    update={"$set": {"metadata.redeeming_code": True}})

    def handle_guide(self):
        # Handle the "Guide" Button
        send_guide_message(self.msg, self.bot)

    def handle_support(self):
        # Handle the "Support" Button
        join_in_support(self.msg, self.bot)

    def handle_photo(self, msg: telebot.types.Message, bot: telebot.TeleBot):
        """

        :param msg: telebot.types.Message instance
        :param bot: telebot.TeleBot instance
        :return: it handles the user message if the message is a photo
        """
        the_user = users_collection.find_one({"user_id": msg.from_user.id})
        if msg.chat.id == self.support_group_id and msg.reply_to_message:
            reply_to_user_support_msg(msg, bot)
        if the_user['metadata']["joined_in_support"]:
            send_user_photo_to_support(msg, bot)
        else:
            bot.reply_to(msg, persian.unknown_request)

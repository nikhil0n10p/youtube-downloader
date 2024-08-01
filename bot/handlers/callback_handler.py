import re

import telebot.types
from bot.handlers.start_handler import StartCommandHandler
from bot.user.subscription.apps.buy_subscription import BuySubscription
from bot.user.utils.subscription_utils import SubscriptionManager
from bot.user.utils.user_utils import UserManager
from bot.youtube.process_video import process_video
from bot.youtube.get_video_information import get_only_filesize
from config.database import users_collection
from languages import persian
from config.tokens import referral_link


class CallbackHandler:
    """
    This class handles all Callback Queries
    """

    def send_error_message(self, error_message):
        self.bot.answer_callback_query(self.callback.id, error_message, show_alert=True)

    def check_subscription_limit(self, filesize):
        subscription_manager = SubscriptionManager(self.callback.from_user.id, filesize)
        if subscription_manager.is_file_size_exceeded() or subscription_manager.is_daily_data_exceeded():
            if subscription_manager.is_file_size_exceeded():
                response = persian.file_data_exceeded
            elif subscription_manager.is_daily_data_exceeded():
                response = persian.daily_limit_exceeded
            self.send_error_message(response)
            return True
        return False

    def process_callback(self, callback: telebot.types.CallbackQuery, bot: telebot.TeleBot):
        self.callback = callback
        self.bot = bot
        the_user = users_collection.find_one({"user_id": callback.from_user.id})
        self.user_manager = UserManager(callback.from_user.id)
        data = callback.data
        self.chat_id = callback.message.chat.id
        if any(re.search(pattern, data) for pattern in
               [r'vc', r'1080p', r'720p', r'480p', r'360p', r'240p', r'144p', ]):
            video_id, res_code_or_vc, chat_id = data.split(" ", 2)
            link = f"https://www.youtube.com/watch?v={video_id}"
            filesize = get_only_filesize(link, res_code_or_vc) if res_code_or_vc != "vc" else get_only_filesize(link)

            if not res_code_or_vc == "vc":
                # when you fix download 1080p add the line (and the_user['subscription']['type'] == "free")
                if res_code_or_vc == "1080p":
                    self.send_error_message(persian.cant_download_1080p_rn)
                    return

            if self.check_subscription_limit(filesize):
                return

            processing_message = persian.processing_message
            self.bot.edit_message_text(processing_message, self.chat_id, message_id=self.callback.message.id)

            process_video(msg=callback.message, bot=bot, link=link, quality_or_audio=res_code_or_vc,
                          chat_id=self.chat_id, user_id=self.callback.from_user.id)

            self.bot.delete_message(chat_id=self.chat_id, message_id=self.callback.message.message_id)
            SubscriptionManager(self.callback.from_user.id, filesize).change_user_subscription_data()

        elif data == "invite_referrals":
            referral_banner = persian.invite_referral_banner
            self.bot.send_message(self.chat_id, referral_banner.format(referral_link + str(callback.from_user.id)))
            self.bot.send_message(self.chat_id, persian.invite_referral_guide)

        elif data == "check_joined":
            if self.user_manager.is_subscribed_to_channel(callback, bot):
                StartCommandHandler().process_start_command(callback.message, bot)
                bot.delete_message(chat_id=self.chat_id, message_id=self.callback.message.message_id)
            else:
                self.bot.answer_callback_query(self.callback.id, persian.not_subscribed_to_channel, show_alert=True)
        elif data == "id_1_in_list":
            BuySubscription().show_subscription_details(msg=self.callback.message, bot=self.bot, subscription="id_1",
                                                        user_id=self.callback.from_user.id)
        elif data == "id_2_in_list":
            BuySubscription().show_subscription_details(msg=self.callback.message, bot=self.bot, subscription="id_2",
                                                        user_id=self.callback.from_user.id)
        elif data in {"buy_id_1_account_charge", "buy_id_2_account_charge"}:
            BuySubscription().buy_via_account_charge(msg=self.callback.message, bot=self.bot, subscription=data,
                                                     user_id=self.callback.from_user.id,
                                                     msg_id=self.callback.message.message_id)
        elif data == "back_to_subscriptions_list":
            BuySubscription().return_to_subscriptions_list(msg=self.callback.message, bot=self.bot,
                                                           user_id=self.callback.from_user.id)

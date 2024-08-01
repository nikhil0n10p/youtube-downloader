import logging
from typing import Any, Mapping

from config.database import users_collection
from config.tokens import channel_id


class UserManager:
    def __init__(self, user_id):
        """
        Initialize UserDataProvider with a user_id.

        :param user_id:
        The unique identifier for the user.
        """

        self.user_id = user_id
        self.user = self._get_user_data()

    def _get_user_data(self) -> Any | None:
        """
        Retrieve user data from the database.

        :return: User data if found, None otherwise.
        """

        try:
            user_data = users_collection.find_one({"user_id": self.user_id})
            return user_data
        except Exception as e:
            logging.error(f"Error retrieving user data: {e}")
            return None

    def get_user_subscription_details(self) -> dict:
        """
        Get details about the user's subscription.
        :return: The user's subscription details.
        """

        if self.user:
            return self.user.get("subscription", {})
        else:
            return {}

    def is_subscribed_to_channel(self, msg, bot):
        """
        Check if the user is subscribed to the channel.
        :param msg: An instance Of telebot.types.Message
        :param bot: An instance Of telebot.TeleBot
        :return: True if the user is subscribed to the channel, False otherwise
        """
        chat_member = bot.get_chat_member(chat_id=channel_id, user_id=msg.from_user.id)
        if chat_member.status in ["member", "administrator", "creator"]:
            return True
        return False

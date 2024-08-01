import re

import telebot
from config.database import users_collection
from config.tokens import how_many_ref, ref_reward


def referral_handler(msg: telebot.types.Message, bot: telebot.TeleBot, referral_user_id: list):
    """
    it processes the user invited by referral link
    :param msg: telebot.types.Message instance
    :param bot: telebot.TeleBot instance
    :param referral_user_id: the user id in the referral link
    """
    the_user = users_collection.find_one({"user_id": msg.from_user.id})
    user_id = msg.from_user.id
    referral_code_match = re.search(r"ref_(\d+)", msg.text)
    if referral_code_match:
        # referral_code = the user who sent the referral link
        referral_code = int(referral_code_match.group(1))
        if the_user and not the_user.get("referred"):
            referral_user = users_collection.find_one({"user_id": referral_code})
            if referral_user and user_id != referral_code and referral_code not in referral_user.get("referrals", []):
                users_collection.update_one({"user_id": referral_code}, {"$push": {"referrals": user_id}})
                users_collection.update_one({"user_id": user_id}, {"$set": {"referred": referral_code}})
                if len(users_collection.find_one({'user_id': referral_code}).get("referrals", [])) % how_many_ref == 0:
                    users_collection.update_one({"user_id": referral_code}, {"$inc": {"balance": ref_reward}})
                    users_collection.update_one({"user_id": referral_code},
                                                {"$inc": {"referral_total_profit": ref_reward}})

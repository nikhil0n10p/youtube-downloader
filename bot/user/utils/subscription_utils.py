from config.database import users_collection


class SubscriptionManager:
    def __init__(self, user_id, filesize: int = None):
        """
        :param user: the user object
        """
        self.user = user_id
        self.the_user = users_collection.find_one({"user_id": user_id})
        self.filesize = filesize

    def change_user_subscription_data(self):
        """
        Change user used_data and remaining_data fields in the database.
        :param user: The user to update (the user object from users_collection)
        :param filesize: the size of the file bytes
        """
        existing_used_size = self.the_user["subscription"]["used_data"]
        existing_remaining_size = self.the_user["subscription"]["remaining_data"]
        monthly_limit = self.the_user["subscription"]["max_data_per_day"]
        new_used_data = existing_used_size + self.filesize
        new_remaining_data = existing_remaining_size - self.filesize
        filter = {"_id": self.the_user["_id"]}
        update = {"$set": {"subscription.used_data": new_used_data, "subscription.remaining_data": new_remaining_data}}
        users_collection.update_one(filter, update)

    def is_file_size_exceeded(self):
        """
        Check if the file size is exceeded
        :param user_data: The user to check (the user object from users_collection)
        :param file_size: the size of the file bytes
        :return: True if the file size is exceeded otherwise False
        """
        max_file_size = self.the_user["subscription"]["max_file_size"]
        if self.filesize > max_file_size:
            return True
        return False

    def is_daily_data_exceeded(self):
        """
        Check if the daily data is exceeded
        :param user_data: The user to check (the user object from users_collection)
        :param file_size: the size of the file bytes
        :return: True if the daily data is exceeded otherwise False
        """
        remaining_size_available = self.the_user["subscription"]["remaining_data"]
        if self.filesize > remaining_size_available:
            return True
        return False

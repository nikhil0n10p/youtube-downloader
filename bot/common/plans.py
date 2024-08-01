from config.database import subscriptions_collection
from jdatetime import datetime


class Plans:
    """
    premium plans
    """
    discount_percent = 0
    id_1_price = 48000
    id_2_price = 118000
    id_1_final_price = id_1_price * discount_percent // 100
    id_1_final_price = id_1_price - id_1_final_price
    id_2_final_price = id_2_price * discount_percent // 100
    id_2_final_price = id_2_price - id_2_final_price

    def get_plan_by_id(self, plan_id: int):
        return subscriptions_collection.find_one({'id': plan_id})

    # download_links_last = 1 means 1 Hour
    plans = [
        {
            "type": "free",
            "id": 0,
            "name": "رایگان",
            "max_file_size": 200,
            "max_data_per_day": 500,
            "used_data": 0,
            "remaining_data": 500,
            "quality_limit": "720p",
            "ads": True,
            "download_links_last": 1,
            "last_reset_date": datetime.today().strftime("%Y-%m-%d"),
        },
        {
            "type": "premium",
            "id": 1,
            "name": "پرمیوم 30 روزه",
            "price": id_1_price,
            "discount_percent": discount_percent,
            "final_price": id_1_final_price,
            "days": 30,
            "days_left": 30,
            "max_file_size": 2000,
            "max_data_per_day": 40000,
            "used_data": 0,
            "remaining_data": 40000,
            "quality_limit": "1080p",
            "ads": False,
            "download_links_last": 24,
            "last_reset_date": datetime.today().strftime("%Y-%m-%d"),
        },
        {
            "type": "premium",
            "id": 2,
            "name": "پرمیوم 90 روزه",
            "price": id_2_price,
            "discount_percent": discount_percent,
            "final_price": id_2_final_price,
            "days": 90,
            "days_left": 90,
            "max_file_size": 2000,
            "max_data_per_day": 40000,
            "used_data": 0,
            "remaining_data": 40000,
            "quality_limit": "1080p",
            "ads": False,
            "download_links_last": 24,
            "last_reset_date": datetime.today().strftime("%Y-%m-%d"),
        }
    ]


if __name__ == "__main__":
    for plan in Plans().plans:
        subscriptions_collection.update_many({"id": plan["id"]}, {"$set": plan}, upsert=True)

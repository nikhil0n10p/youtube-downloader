from pymongo import MongoClient
# configure you mongo server here
client = MongoClient("mongodb://localhost:27017/")

db = client['yt-downloader']
users_collection = db['users']
giftcodes_collection = db['giftcodes']
subscriptions_collection = db['subscriptions']
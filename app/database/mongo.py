from pymongo import MongoClient
from config import MONGODB_URI

client = MongoClient(MONGODB_URI)

db = client["goldsense"]

predictions = db["predictions"]
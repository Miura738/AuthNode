from pymongo import MongoClient

from config import Config

mongo = MongoClient(Config.MONGO_URI)


def db(table: str):

    return mongo[Config.MONGO_DBNAME][f"{Config.MONGO_PREFIX}{table}"]

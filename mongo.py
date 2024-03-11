from pymongo import MongoClient

mongo = MongoClient("mongodb://localhost:27017/")

DATABASE = "AuthNode"
PREFIX = "an_"


def db(table: str):
    return mongo[DATABASE][f"{PREFIX}{table}"]

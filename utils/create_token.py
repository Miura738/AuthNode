import hashlib
import uuid

from mongo import db


def create_token(UserData):
    if UserData is None:
        return None

    UserId = UserData['_id']

    sha256 = hashlib.sha256(uuid.uuid4().bytes)
    accessToken = "AuthNode.accessToken." + sha256.hexdigest()

    db("tokens").insert_one({"uid": UserId, "token": accessToken, "type": "accessToken"})

    return accessToken

from mongo import db
from json import dump
from selenium import webdriver
from urllib.parse import urlparse, parse_qs
from requests import post, get


def getCode(microsoft_url: str):
    result = urlparse(microsoft_url)  # 会被重定向，获取一下 URL
    code = None
    if result.hostname == 'login.live.com' and result.path == '/oauth20_desktop.srf':
        query = parse_qs(result.query)
        if 'code' in query and 'lc' in query and 'error' not in query:
            code = query['code'][0]
    return code


def get_mojang_token():
    token = db("keys").find_one({"_id": "mojang_token"}, {"_id": 0, "key": 1})
    if token is None:
        print("No mojang Token")

    print("Please open this link in your browser:")
    print("https://login.live.com/oauth20_authorize.srf?client_id=00000000402b5328&response_type=code&scope=service%3A%3Auser.auth.xboxlive.com%3A%3AMBI_SSL&redirect_uri=https%3A%2F%2Flogin.live.com%2Foauth20_desktop.srf")
    code = getCode(input("Please enter redirect url: "))


if __name__ == '__main__':
    get_mojang_token()



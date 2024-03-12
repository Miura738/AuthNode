from mongo import db


def get_mojang_token():
    token = db("keys").find_one({"_id": "mojang_token"}, {"_id": 0, "key": 1})
    if token is None:
        print("No mojang Token")


if __name__ == '__main__':
    # get_mojang_token()

    import requests

    code = "M.C510_SN1.2.U.188d48e3-39e5-8757-e08a-93a14fab0504"
    url = f"https://login.live.com/oauth20_token.srf?client_id=00000000402b5328&code={code}&grant_type=authorization_code&scope=service%3A%3Auser.auth.xboxlive.com%3A%3AMBI_SSL&redirect_uri=https%3A%2F%2Flogin.live.com%2Foauth20_desktop.srf"

    headers = {
          "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, headers=headers)

    print(response.text)
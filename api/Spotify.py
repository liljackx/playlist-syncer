import json
import os.path
import requests
from data import *
import base64
import webbrowser

class Spotify:
    token = ""
    auth_uri = ""

    # TODO: write function to check it token is still valid, if not get referesh_token

    def __init__(self):
        self.token_uri = "https://accounts.spotify.com/api/token"
        self.auth_uri = f"https://accounts.spotify.com/authorize?response_type=code&client_id={SPOTIFY_CLIENT_ID}&scope=user-read-private user-read-email&redirect_uri={SPOTIFY_REDIRECT_URI}"
        self.__authenticate()

    def __write_local_perms(self, token):
        with open(".spoty_creds", "w") as perms_file:
            json.dump(token, perms_file)

    def __check_local_perms(self, perms_file="./.spoty_creds"):
        if os.path.isfile(perms_file):
            with open(perms_file) as tokenFile:
                self.token = json.load(tokenFile).get("access_token")
                return True
        else:
            return False

    def __get_code(self):
        webbrowser.open(self.auth_uri)
        uri = input("Insert the URI you've been redirected to: ")
        return uri.split("code=")[1]

    def __get_token(self, code):
        body = {"grant_type": "authorization_code", "code": code, "redirect_uri": SPOTIFY_REDIRECT_URI}
        payload_to_encode = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_SECRET_ID}"
        headers = {"Authorization": f"Basic {base64.urlsafe_b64encode(payload_to_encode.encode()).decode()}"}
        response = requests.post(self.token_uri, data=body, headers=headers).json()
        self.token = response.get("access_token")
        return response

    def __authenticate(self):
        if not self.__check_local_perms():
            code = self.__get_code()
            token = self.__get_token(code)
            self.__write_local_perms(token)

s = Spotify()
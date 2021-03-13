import os.path
import requests
import json
from data import *
import webbrowser

'''
The way I store playlist is using a JSON file that
contains a list of URI that refers to playlist from one
source (Spotify) or the other one (Deezer)
NOTE: if you don't specify any target Playlist the playlist
will be created as new.
'''

class Deezer:
    token = ""
    base_uri = ""

    def __init__(self):
        self.auth_uri = f"https://connect.deezer.com/oauth/auth.php?app_id={DEEZER_APP_ID}&redirect_uri={DEEZ_REDIRECT_URI}&perms=basic_access,email&resopnse_type=token"
        self.base_api = "https://api.deezer.com/{}"
        self.__get_token()

    # Check if local file with perms exists
    def __check_local_perms(self, perms_file="./.deez_perms"):
        if os.path.isfile(perms_file):
            with open(perms_file, "r") as permission_file:
                self.token = json.load(permission_file).get("token")
                return True
        else:
            return False

    # Write local file perms in case it doesn't already exists
    def __write_local_perms(self, token, perms_file="./.deez_perms"):
        with open(perms_file, "w") as perms_file:
            payload = {"token": token}
            json.dump(payload, perms_file)

    # Get deezer token (necessary for POST requests)
    def __get_token(self):
        if not self.__check_local_perms():
            print("No local file")
            webbrowser.open(self.auth_uri)
            uri = input("Insert here the URI you've been redireted to: ")
            self.token = uri.split("code=")[1]
            self.__write_local_perms(self.token)

    # Fetch a playlist from it's URI
    def fetch_playlist(self, playlists_uri=None):
        if playlists_uri is not None:
            current_playlist_id = playlists_uri.split("en/")[1]
            response = requests.get(self.base_api.format(current_playlist_id))
            return response.json()
        else:
            raise Exception("Invalid playlists URI")
    
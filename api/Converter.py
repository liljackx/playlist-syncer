import requests
from Deezer import Deezer
from Spotify import Spotify
from Parser import *

'''
NOTE: this class will update playlists of each
music provider, creating or adding new playlists or tracks
'''

class Converter:
    spotify = None
    deezer = None
    # Playlists to keep synced
    playlists = []

    def __init__(self):
        self.spotify = Spotify()
        self.deezer = Deezer()
        self.__load_playlists()


    def __load_playlists(self, playlists_file="../config/playlists.json"):
        loaded_playlists = get_sync_schema(playlists_file)
        self.playlists = loaded_playlists

    def _check_tracks_differences(self, spotify_playlist_uri, deezer_playlist_uri):
        # Check if playlists have the same tracks, if not add or eventually remove
        spotify_playlist_data = self.spotify.fetch_playlist("https://open.spotify.com/playlist/77tCnL1EOCQc6gmPrx2spq?si=QdT3RV8QRFCzP58rDyhH5g")
        
        deezer_playlist_data = self.deezer.fetch_playlist("https://deezer.page.link/hv7KKSAinffUU4oC8")
        print(deezer_playlist_data)

        if playlist_data["tracks"]["total"] > 100:
            # Parse playlist with limit offset function
        else:
            # Parse playlist as a normal one

c = Converter()
c._check_tracks_differences(None, None)
# print(c.playlists)
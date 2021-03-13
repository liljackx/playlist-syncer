import requests
from Deezer import Deezer
from Spotify import Spotify
from Parser import *
import threading
import itertools

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

    '''
    NOTE this functions returns a list of track names and artists as follows:
    All Me - Drake, where All me is the name of the track and Drake the name of the artist
    '''
    # Improve function, one for each music provider ?
    def __get_tracks_name_lists(self, tracks):
        trakcs_list = []
        for track in tracks:
            try:
                # Try as if it is a spotify playlist format
                current_track = track.get("track")
                trakcs_list.append(
                    {
                        "artist": current_track.get("artists")[0].get("name"),
                        "name": current_track.get("name"),
                    }
                )
            except:
                # If error go on trying with deezer playlist format
                trakcs_list.append(
                    {
                        "artist": track.get('artist').get("name"),
                        "name": track.get("title"),
                    }
                )
        return trakcs_list

    # Set all strings to lower case to avoid errors ?
    # First thread: spotify_tracks, deezer_tracks
    # Second thread: deezer_tracks, spotify_tracks
    # Al primo check bisogna decidere quale deve 
    # sincronizzarsi con quale, definiere qu
    def check_each(self, spotify_tracks, deezer_tracks, master=None):
        # Master will always be the source and destination
        # will be the playlists that adapt itself based on the master
        # Mater could be either spotify or deezer
        if master == "spotify":
            for track in spotify_tracks:
                if track not in deezer_tracks:
                    # Add track to deezer (deezer api)
                else:
                    print("Track is already there")
        elif master == "deezer":
            for track in deezer_tracks:
                if track not in spotify_tracks:
                    # Add track to spotify playlist (spotify api)
                else:
                    print("Track is already there")
        else:
            raise Exception("No master playlist has been defined, please provide one !")


    def _check_tracks_differences(self, spotify_playlist_uri, deezer_playlist_uri):
        # Check if playlists have the same tracks, if not add or eventually remove
        spotify_playlist_data = self.spotify.fetch_playlist("https://open.spotify.com/playlist/77tCnL1EOCQc6gmPrx2spq?si=QdT3RV8QRFCzP58rDyhH5g")
        
        deezer_playlist_data = self.deezer.fetch_playlist("https://deezer.page.link/hv7KKSAinffUU4oC8")

        if spotify_playlist_data.get("tracks").get("total") > 100:
            # Parse playlist with limit offset function
            pass
        else:
            spotify_tracks = self.__get_tracks_name_lists(spotify_playlist_data.get("tracks").get("items"))
            deezer_tracks = self.__get_tracks_name_lists(deezer_playlist_data.get("tracks").get("data"))
            # print(deezer_tracks)
            spotify_scroller = threading.Thread(target=self.check_each, args=(spotify_tracks, deezer_tracks))
            spotify_scroller.start()

c = Converter()
c._check_tracks_differences(None, None)
# print(c.playlists)
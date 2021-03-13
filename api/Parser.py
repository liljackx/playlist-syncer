import json

def parse_plyalists(filename="./config/playlists.json"):
    with open(filename) as jsonFile:
        data = json.load(jsonFile)
    return data

def get_sync_schema(filename="./config/playlists.json"):
    playlists_to_sync = []
    playlists_file = parse_plyalists(filename)
    available_playlists = playlists_file.get("playlists")

    for group in available_playlists:
        playlists_to_sync.append(group)

    return playlists_to_sync

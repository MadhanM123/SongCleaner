from clean import SpotifyClean
import json
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util

def load_config():
    with open("config.json") as f:
        config = json.load(f)
    return config

def token(usrname):
    config = load_config()
    scope = "playlist-modify-public playlist-read-private playlist-modify-private"
    cli_id = config["client-id"]
    cli_sec = config["client-secret"]
    redir_url = config["redirect-url"]
    oauth = SpotifyOAuth(client_id = cli_id, client_secret = cli_sec, show_dialog = True, scope = scope, redirect_uri = redir_url)
    token = util.prompt_for_user_token(usrname, scope, cli_id, cli_sec, redir_url, oauth_manager=oauth)
    return token

print("Welcome to Spotify Cleaner")

usrname = input("Please enter your Spotify user ID: ")
tok = token(usrname)
clean = SpotifyClean(tok)
plists = clean.get_playlists()

for i, plist in enumerate(plists, 0):
    print(f"[{i + 1}] {plist.name}")

while True:
    choice = input("Select a playlist: ")

    if choice.isnumeric():
        choice = int(choice)
        choice -= 1
    else:
        continue

    if choice < 0 and choice >= len(plist):
        continue
    else:
        plist = plists[choice]
        break

clean.get_songs(plist)
cleaned = clean.clean_playlist(plist)
print(cleaned.url)
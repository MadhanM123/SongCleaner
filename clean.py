import spotipy
from math import ceil
from playlist import Playlist
from song import Song
import os

def clear():
    if os.name in ('nt', 'dos'):
        os.system('cls')
    elif os.name in ('linux', 'osx', 'posix'):
        os.system("clear")
    else:
        print("n") * 120



class SpotifyClean(spotipy.Spotify):
    def __init__(self, auth):
        super().__init__(auth=auth)
        self.usr_id = self.me()["id"]
    
    def get_playlists(self):
        result = self.current_user_playlists()
        pls = []

        for pl in result["items"]:
            pl = Playlist(pl)
            pls.append(pl)
        return pls
    
    def get_clean_playlist(self, name):
        pls = self.get_playlists()
        for pl in pls:
            if pl.nm == f"{name} (Clean)":
                return pl
        return None
    
    def get_songs(self, pl: Playlist):
        MAX = 100
        tot_runs = ceil(pl.track_cnt / MAX)
        trks_thru = 0

        for i in range(0, tot_runs):
            res = self.playlist_tracks(pl.id, offset=trks_thru)

            for song in res["items"]:
                pl.songs.append(Song(song))
            
            trks_thru += MAX

    def clean_playlist(self, playlist: Playlist):
        MAX = 100
        self.user_playlist_create(self.usr_id, f"{playlist.nm} (Clean)", public=playlist.is_pub)
        clean_plist = self.get_clean_playlist(playlist.nm)

        if clean_plist:
            clean_songs = []
            i = 1
            tot = 0

            for song in playlist.songs:
                clear()

                print("Cleaning playlist... Large playlists can take a while")
                print(f"Cleaning song {i} of {playlist.track_cnt}")

                if len(clean_songs) == MAX:
                    self.playlist_add_items(clean_plist.id, clean_songs)
                    clean_songs = []

                if not song.is_loc:
                    if song.is_exp:
                        searchs = self.search(f"{song.nm} {song.artist}", type = "track", limit = 30)
                        for search_trk in searchs["tracks"]["items"]:

                            search_trk = Song(search_trk)
                            is_same_song = song.comp_song(search_trk)

                            if is_same_song:
                                tot += 1
                                clean_songs.append(search_trk.id)
                                break
                    else:
                        clean_songs.append(song.id)
                        tot += 1
                
                i += 1

            if len(clean_songs) > 0:
                self.playlist_add_items(clean_plist.id, clean_songs)
        
        print(f"Out of {playlist.track_cnt} songs, {tot} were cleaned")
        
        return clean_plist
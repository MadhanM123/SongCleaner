

class Song:
    
    def __init__(self, data):
        self.data = data
        if self.data.get("track"):
            self.data = self.data["track"]
    
    def comp_song(self, cmp_song):
        if self.name == cmp_song.name:
                if self.artist_id == cmp_song.artist_id: 
                     if not cmp_song.is_exp:
                          return True
        return False
    
    @property
    def nm(self):
        return self.data["name"]
    
    @property
    def artist(self):
        return self.data["artists"][0]["name"]
    
    @property
    def artist_id(self):
        return self.data["artistis"][0]["id"]
    
    @property
    def album(self):
        return self.data["album"]["name"]
    
    @property
    def id(self):
        return self.data["id"]
    
    @property
    def is_exp(self):
        return self.data["explicit"]
    
    @property
    def is_loc(self):
        return self.data["is_local"]
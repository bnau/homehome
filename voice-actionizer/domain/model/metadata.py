class Album:
    album_id: str
    title: str
    artist: str

    def __init__(self, album_id: str, title: str, artist: str):
        self.album_id = album_id
        self.title = title
        self.artist = artist

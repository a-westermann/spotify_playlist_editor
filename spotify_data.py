import api_calls


class Song:
    def __init__(self, artist: str, song: str, id: str):
        self.artist = artist
        self.name = song
        self.id = id

    def __eq__(self, other):
        return self.name == other.name and self.artist == other.artist


class SpotifyData:
    def __init__(self):
        self.liked_songs = []
        self.top_songs = []

    def compile_data(self, user_access_token):
        # liked songs
        count = 100
        start = 0
        while start < count:
            try:
                items = api_calls.get_liked_songs(50, start, user_access_token)
                for item in items:
                    self.liked_songs.append(Song(item['track']['artists'][0]['name'], item['track']['name'],
                                              item['track']['id']))
                start += 50
            except Exception as e:
                print(f'Broke in liked songs:  {e}')
                break
        # top songs
        start = 0
        while start < count:
            try:
                items = api_calls.get_top_items(50, start, user_access_token)
                for item in items:
                    self.top_songs.append(Song(item['artists'][0]['name'], item['name'], item['id']))
                start += 50
            except:
                break


    def get_songs_to_drop(self, drop_percent: float) -> set:
        songs_to_drop = []
        print(len(self.liked_songs))
        for song in self.liked_songs:
            if song not in self.top_songs:
                # song is not in top songs. Mark it to drop
                # print(f'{song.name} not in top')
                songs_to_drop.append(song)
            elif float(self.top_songs.index(song)) / float(len(self.top_songs)) > 1.0 - drop_percent:
                # song is in bottom drop_percent percent of top_songs. Mark it to drop
                # print(f'{song.name} bottom {drop_percent}')
                songs_to_drop.append(song)

        print(f'songs to drop length:  {len(songs_to_drop)}')
        return songs_to_drop

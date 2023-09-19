from ytmusicapi import YTMusic
from urllib.parse import urlparse, parse_qs


class Youtube:
    __yt = YTMusic()

    def get_playlist_tracks(self, url: str):
        playlist_id = self.__resolve_playlist_id(url)
        tracks = self.__yt.get_playlist(playlist_id)['tracks']

        return [{
            'title': track['title'],
            'artist': track['artists'][0]['name'],
        } for track in tracks]

    @staticmethod
    def __resolve_playlist_id(url: str):
        url = urlparse(url)

        if url.netloc != 'music.youtube.com':
            raise Exception('Not supported yet')

        if url.path != '/playlist':
            raise Exception('Not supported yet')

        query = parse_qs(url.query)

        if 'list' not in query:
            raise Exception('Not supported yet')

        return query['list'][0]

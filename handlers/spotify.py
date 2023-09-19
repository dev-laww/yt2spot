from requests import Session
from urllib.parse import parse_qs, urlencode, urlparse


class Spotify:
    AUTH_URL = 'https://accounts.spotify.com/api/token'
    SEARCH_URL = 'https://api.spotify.com/v1/search'
    USERS_URL = 'https://api.spotify.com/v1/users'
    PLAYLISTS_URL = 'https://api.spotify.com/v1/playlists'

    def __init__(self, client_id, client_secret):
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__access_token = None
        self.__user_token = None
        self.__session = Session()

        self.__get_access_token()
        self.__authorize()

    def search(self, song: str, artist: str):
        query = urlencode({
            'q': f'track:{song} artist:{artist}',
            'type': 'track',
            'limit': 1,
        })
        r = self.__session.get(f'{self.SEARCH_URL}?{query}')

        if not r.ok:
            raise Exception('Failed to search for song')

        return r.json()['tracks']['items'][0]['uri']

    def create_playlist(self, name, tracks):
        user_id = self.__resolve_user_id()

        self.__session.headers.update({'Authorization': f'Bearer {self.__user_token}'})

        r = self.__session.post(f'{self.USERS_URL}/{user_id}/playlists', json={
            "name": name,
            "description": "Created by YT2SP",
            "public": False
        })

        if not r.ok:
            raise Exception('Failed to create playlist')

        playlist_id = r.json()['id']

        # add tracks to playlist
        r = self.__session.post(f'{self.PLAYLISTS_URL}/{playlist_id}/tracks', json={
            'uris': tracks
        })

        if not r.ok:
            raise Exception('Failed to add tracks to playlist')

        self.__session.headers.update({'Authorization': f'Bearer {self.__access_token}'})

        return f'https://open.spotify.com/playlist/{playlist_id}'

    def __get_access_token(self):
        r = self.__session.post(self.AUTH_URL, {
            'grant_type': 'client_credentials',
            'client_id': self.__client_id,
            'client_secret': self.__client_secret,
        })

        if not r.ok:
            raise Exception('Failed to get access token')

        self.__access_token = r.json()['access_token']

        self.__session.headers.update({'Authorization': f'Bearer {self.__access_token}'})

    def __authorize(self):
        query = urlencode({
            'client_id': self.__client_id,
            'response_type': 'token',
            'redirect_uri': 'https://google.com',
            'scope': 'playlist-modify-public playlist-modify-private user-read-private user-read-email',
        })

        print(f'Click this link to authorize app: [https://accounts.spotify.com/authorize?{query}]')
        token = input('After authorization, redirected link and paste it here: ')

        token = urlparse(token).fragment
        token = parse_qs(token)['access_token'][0]

        self.__user_token = token

    def __resolve_user_id(self):
        r = self.__session.get('https://api.spotify.com/v1/me', headers={
            'Authorization': f'Bearer {self.__user_token}'
        })

        if not r.ok:
            raise Exception('Failed to get user id')

        return r.json()['id']

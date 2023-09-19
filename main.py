import argparse
from textwrap import dedent

from handlers.spotify import Spotify
from handlers.youtube import Youtube


def spotify_to_yt(url: str, name: str = None):
    raise NotImplementedError


def yt_to_spotify(url: str, name: str = None):
    yt = Youtube()
    spotify = Spotify('b4eab4a6ee4e47c8acb628285fa1d716', '37a562b3a9af4af09fd425b64d7236ad')

    tracks = yt.get_playlist_tracks(url)
    spotify_uris = [spotify.search(track['title'], track['artist']) for track in tracks]

    name = name or input('Playlist name: ')

    spotify_playlist_url = spotify.create_playlist(name, spotify_uris)
    print(f'Playlist created: {spotify_playlist_url}')


def main():
    parser = argparse.ArgumentParser(description='Transfer playlists between Spotify and YouTube Music')
    parser.add_argument(
        '-u',
        '--url',
        type=str,
        metavar='URL',
        help='URL of the playlist to transfer'
    )
    parser.add_argument(
        '-d',
        '--direction',
        type=str,
        choices=['yt-to-spotify', 'spotify-to-yt'],
        metavar='DIRECTION',
        help='Direction of the transfer: [yt-to-spotify, spotify-to-yt]'
    )
    parser.add_argument(
        '-n',
        '--name',
        type=str,
        metavar='NAME',
        help='Name of the playlist to create'
    )
    args = parser.parse_args()

    direction = args.direction or 'yt-to-spotify' if int(input(dedent('''
    Transfer direction:
    1. YouTube Music to Spotify
    2. Spotify to YouTube Music
    Enter your choice: ''')).strip()) == 1 else 'spotify-to-yt'
    url = args.url or input('Playlist URL: ')

    if direction not in ['yt-to-spotify', 'spotify-to-yt']:
        raise ValueError('Invalid direction')

    if direction == 'yt-to-spotify':
        yt_to_spotify(url, args.name)
        return

    spotify_to_yt(url, args.name)


if __name__ == '__main__':
    main()

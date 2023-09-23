import requests, os
import base64
import config
import argparse
#api setup
CLIENT_ID = config.SPOTIFY_CLIENT_ID
CLIENT_SECRET = config.SPOTIFY_CLIENT_SECRET
AUTH_URL = 'https://accounts.spotify.com/api/token'
SEARCH_URL = 'https://api.spotify.com/v1/search'

auth_str = f'{CLIENT_ID}:{CLIENT_SECRET}'
auth_header = {
    'Authorization': f'Basic {base64.b64encode(auth_str.encode()).decode()}'
}

auth_response = requests.post(AUTH_URL, headers=auth_header, data={'grant_type': 'client_credentials'})
auth_data = auth_response.json()
access_token = auth_data['access_token']


def song_link(artist, track_name):
    search_headers = {
        'Authorization': f'Bearer {access_token}'
    }
    search_params = {
        'q': f'artist:{artist} track:{track_name}',
        'type': 'track',
        'limit': 1
    }
    search_response = requests.get(SEARCH_URL, headers=search_headers, params=search_params)
    search_data = search_response.json()

    if 'tracks' in search_data and 'items' in search_data['tracks'] and len(search_data['tracks']['items']) > 0:
        track_url = search_data['tracks']['items'][0]['external_urls']['spotify']
        print(f"Here is the Spotify link to '{track_name}' by {artist}: {track_url}")
    else:
        print(f"No results found for '{track_name}' by {artist}")

parser = argparse.ArgumentParser(description='Spotify Link to a Song')
parser.add_argument('name', type=str, help='format as <Artist>,<Trackname>')
args = parser.parse_args()
deets = args.name.split(',')
song_link(deets[0], deets[1].strip())
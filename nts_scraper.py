import pandas as pd, requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import config, argparse

# Spotify API config
CLIENT_SECRET=config.SPOTIFY_CLIENT_SECRET
CLIENT_ID=config.SPOTIFY_CLIENT_ID
REDIRECT_URI = 'http://localhost:8888/callback'

# Spotify authentication 
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI, scope='playlist-modify-private'))

def get_tracklist(url):
    #bs4 config
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    #get tracks
    tracklist = []
    for track_info in soup.find_all('li', class_='track'):
        track_name = track_info.find('span', class_='track__title').text.strip()
        artist_name = track_info.find('span', class_='track__artist').text.strip()

        track = {
            'Track Name': track_name,
            'Artist Name': artist_name,
        }
        tracklist.append(track)

    df = pd.DataFrame(tracklist)
    return df

def spotify_playlist(url):
    #playlist init
    playlist_name = url.split('/')[-1]
    playlist_description = 'Spotify Playlist for '+str(url)
    
    df = get_tracklist(url)

    # Create the playlist
    playlist = sp.user_playlist_create(sp.current_user()['id'], playlist_name, public=False, description=playlist_description)
    playlist_id = playlist['id']
    for index, row in df.iterrows():
        track_name = row['Track Name']
        artist_name = row['Artist Name']

        # Search for the track
        search_results = sp.search(q=f"track:{track_name} artist:{artist_name}", type='track', limit=1)

        if search_results['tracks']['items']:
            track_uri = search_results['tracks']['items'][0]['uri']
            # Add the track to the playlist
            sp.playlist_add_items(playlist_id, [track_uri])
        else:
            print(f"Track not found on Spotify: {track_name} by {artist_name}")

# spotify_playlist('https://www.nts.live/shows/floating-points/episodes/floating-points-28th-august-2023')

parser = argparse.ArgumentParser(description='NTS-Radio Tracklist to Spotify playlist Scraper, run the scripy with an NTS episode as an argument')
parser.add_argument('Episode_URL', type=str, help='URL for the NTS Radio Episode')
args = parser.parse_args()
try:
    spotify_playlist(args.Episode_URL)
except:
    print('Check the link you have provided, there may be no tracklist or the URL may be invalid')
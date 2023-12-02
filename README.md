# NTS_Episode_Spotify_Playlist
A simple python script to create Spotify Playlists from an NTS-Live Radio Episode's tracklist.

**Requirements** 
- Spotify developer app instance 
- Beautiful Soup 4, Spotipy

## Setup
Clone the repo and create a `config.py` file in the directory. Define your Spotify Client ID and Client Secret variables as
```py
SPOTIFY_CLIENT_ID='your_id'
SPOTIFY_CLIENT_SECRET='your_secret'
```

## Execution
Run the `nts_scraper.py` script with an argument for the NTS Live Radio episode URL.  
  
For example:
```shell
python3 nts_scraper.py 'https://www.nts.live/shows/floating-points/episodes/floating-points-28th-august-2023'
```

import requests
import sys
from params import params
sys.path.append('ewestenburg/cs458-final-project')
from auth_spotify import get_auth_token  # Importing the function from auth_spotify.py
ACCESS_TOKEN = get_auth_token()

def get_recommendations(params):
    SPOTIFY_GET_RECOMMENDATIONS_URL = 'https://api.spotify.com/v1/recommendations'

    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

    response = requests.get(SPOTIFY_GET_RECOMMENDATIONS_URL, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Spotify API Error: {response.json()}")
    return response.json()

def extract_track_urls(recommendations):
    track_urls = []
    if 'tracks' in recommendations and isinstance(recommendations['tracks'], list):
        for track in recommendations['tracks']:
            if 'external_urls' in track and 'spotify' in track['external_urls']:
                track_urls.append(track['external_urls']['spotify'])
    return track_urls

def search_spotify_id(item_name, item_type, access_token):
    search_url = f"https://api.spotify.com/v1/search"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    params = {
        'q': item_name,
        'type': item_type,
        'limit': 1
    }
    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Spotify API Search Error: {response.json()}")

    search_results = response.json()
    items = search_results[item_type + 's']['items']
    return items[0]['id'] if items else None

def main():
    # Check and convert seed_artists and seed_tracks names to Spotify IDs
    if 'seed_artists' in params:
        artist_ids = [search_spotify_id(name, 'artist', ACCESS_TOKEN) for name in params['seed_artists']]
        params['seed_artists'] = ','.join(filter(None, artist_ids))
    
    if 'seed_tracks' in params:
        track_ids = [search_spotify_id(name, 'track', ACCESS_TOKEN) for name in params['seed_tracks']]
        params['seed_tracks'] = ','.join(filter(None, track_ids))

    recommendations = get_recommendations(params)
    track_urls = extract_track_urls(recommendations)
    print(track_urls)

if __name__ == '__main__':
    main()
import requests
import sys
from params import params
sys.path.append('ewestenburg/cs458-final-project')
from auth_spotify import get_auth_token  # Importing the function from auth_spotify.py
ACCESS_TOKEN = get_auth_token()

def spotify_search(params):
    SPOTIFY_SEARCH_URL = 'https://api.spotify.com/v1/search'

    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

    # Spotify search parameters
    spotify_search_params = ['q', 'type', 'market', 'limit', 'album', 'artist', 'track', 'year', 'genre']

    # Separate input parameters into those used for Spotify search and additional parameters
    search_params = {k: v for k, v in params.items() if k in spotify_search_params}
    additional_params = {k: v for k, v in params.items() if k not in spotify_search_params}

    # Prepare search query
    search_query = ' '.join([f'{k}:{v}' for k, v in search_params.items() if k != 'type' and k != 'market' and k != 'limit'])

    # Add the query string to the search parameters
    search_params['q'] = search_query

    # Perform the search
    response = requests.get(SPOTIFY_SEARCH_URL, headers=headers, params=search_params)
    if response.status_code != 200:
        raise Exception(f"Spotify API Search Error: {response.json()}")

    return response.json(), additional_params

def extract_track_urls(search_results):
    track_urls = []
    if 'tracks' in search_results and isinstance(search_results['tracks'], dict):
        for track in search_results['tracks']['items']:
            if 'external_urls' in track and 'spotify' in track['external_urls']:
                track_urls.append(track['external_urls']['spotify'])
    return track_urls

def get_audio_features(track_ids, access_token):
    audio_features_url = 'https://api.spotify.com/v1/audio-features'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(audio_features_url, headers=headers, params={'ids': ','.join(track_ids)})
    if response.status_code != 200:
        raise Exception(f"Spotify API Error in Audio Features: {response.json()}")
    return response.json()['audio_features']

def filter_and_rank_tracks(tracks, criteria):
    def meets_criteria(track, criteria):
        if track is None:  # Add this check
            return False
        for key, value in criteria.items():
            if key.startswith('min_') and track.get(key[4:], float('inf')) < value:
                return False
            elif key.startswith('max_') and track.get(key[4:], float('-inf')) > value:
                return False
        return True

    def calculate_distance(track, criteria):
        if track is None:  # Add this check
            return float('inf')
        distance = 0
        for key, value in criteria.items():
            if key.startswith('target_'):
                feature = key[7:]
                if feature in track:
                    distance += abs(track[feature] - value)
        return distance

    # Filter tracks
    filtered_tracks = [track for track in tracks if meets_criteria(track, criteria)]

    # Rank tracks based on closeness to target criteria
    ranked_tracks = sorted(filtered_tracks, key=lambda track: calculate_distance(track, criteria))

    # Return top 5 tracks
    return ranked_tracks[:5]

def run_spotify_search(params):

    search_results, additional_params = spotify_search(params)
    track_ids = [track['id'] for track in search_results['tracks']['items']]
    print(track_ids)
    
    # Fetch audio features for the tracks
    audio_features = get_audio_features(track_ids, ACCESS_TOKEN)

    # Create a mapping of track IDs to their corresponding URLs
    track_id_to_url = {track['id']: track['external_urls']['spotify'] for track in search_results['tracks']['items']}

    # Filter and rank tracks based on additional criteria
    best_matching_tracks = filter_and_rank_tracks(audio_features, additional_params)

    # Get the URLs of the best matching tracks
    best_matching_track_urls = [track_id_to_url[track['id']] for track in best_matching_tracks if track['id'] in track_id_to_url]

    print(best_matching_track_urls)
    return(best_matching_track_urls)

if __name__ == '__main__':
    track_urls = run_spotify_search(params)
    print(track_urls)

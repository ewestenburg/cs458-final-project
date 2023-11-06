#Simple test version of search function
import requests
import sys
sys.path.append('ewestenburg/cs458-final-project')
from auth_spotify import get_auth_token  # Importing the function from auth_spotify.py

# Replace 'your_access_token' with the actual token you get from the auth_spotify.py process
ACCESS_TOKEN = get_auth_token()

def extract_track_urls(recommendations):
    # This will hold all the track URLs
    track_urls = []

    # Check if 'tracks' key is in the recommendations and it is a list
    if 'tracks' in recommendations and isinstance(recommendations['tracks'], list):
        # Loop through each track and extract the URL
        for track in recommendations['tracks']:
            # Check if 'external_urls' is in the track and it has a 'spotify' key
            if 'external_urls' in track and 'spotify' in track['external_urls']:
                track_urls.append(track['external_urls']['spotify'])

    return track_urls

def get_recommendations(seed_genres, target_danceability):
    # Endpoint for getting recommendations
    SPOTIFY_GET_RECOMMENDATIONS_URL = 'https://api.spotify.com/v1/recommendations'

    # Authorization header
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

    # Parameters for the recommendations
    # For this example, we're using seed_genres and target_danceability,
    # but you can add more parameters as needed.
    params = {
        'seed_genres': seed_genres,
        'target_danceability': target_danceability
    }

    response = requests.get(SPOTIFY_GET_RECOMMENDATIONS_URL, headers=headers, params=params)
    return response.json()

# Example usage
if __name__ == '__main__':
    # Example seed genres and target danceability
    seed_genres = 'indie-pop,indie'
    target_danceability = 0.7

    recommendations = get_recommendations(seed_genres, target_danceability)
    track_urls_list = extract_track_urls(recommendations)
    print(track_urls_list)

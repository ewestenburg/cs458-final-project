#Simple test version of search function
import requests
import sys
sys.path.append('ewestenburg/cs458-final-project')
from auth_spotify import get_auth_token  # Importing the function from auth_spotify.py

# Replace 'your_access_token' with the actual token you get from the auth_spotify.py process
ACCESS_TOKEN = get_auth_token()

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
    print(recommendations)

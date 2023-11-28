import requests
import base64
from urllib.parse import urlencode
import time

# Constants
CLIENT_ID = '87553f892f144b4987071af360d0c470'
CLIENT_SECRET = '44437f232de9413aa87b219d94c1e3ac'
REDIRECT_URI = '3OIe4tBfD9Ca2GRKq9FGuk'
AUTH_URL = 'https://accounts.spotify.com/api/token'

# Function to get the authorization token
def get_auth_token():
    # Spotify requires a base64 encoded string of client_id:client_secret for the headers
    auth_str = f'{CLIENT_ID}:{CLIENT_SECRET}'
    auth_bytes = auth_str.encode('ascii')
    base64_encoded = base64.b64encode(auth_bytes).decode('ascii')

    headers = {
        'Authorization': f'Basic {base64_encoded}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # The body of the POST request contains the grant type and the redirect URI
    body = {
        'grant_type': 'client_credentials',
        'redirect_uri': REDIRECT_URI
    }

    # POST request to get the access token
    auth_response = requests.post(AUTH_URL, headers=headers, data=body)
    auth_response_data = auth_response.json()

    # Extract the access token from the response
    access_token = auth_response_data['access_token']

    # Use the access token to make authenticated requests to the Spotify API
    #print(access_token)
    return access_token

# Function to refresh the token every hour
def refresh_token():
    while True:
        global access_token
        access_token = get_auth_token()
        # Sleep for 1 hour (3600 seconds) minus a small offset to refresh the token before it expires
        time.sleep(3595)

# Run the refresh token function
if __name__ == "__main__":
    refresh_token()
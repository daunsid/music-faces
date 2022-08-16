import requests
import base64
from .config import settings


AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'

# Make a request to the /authorize endpoint to get an authorization code
CLIENT_ID = '2c115b5e727e407d9a7143ee54906b4e'
auth_code = requests.get(AUTH_URL, {
    'client_id': settings.client_id,
    'response_type': 'code',
    'redirect_uri': 'https://open.spotify.com/collection/playlists',
    'scope': 'playlist-read-private',
})

auth_header = base64.urlsafe_b64encode((settings.client_id + ':' + settings.client_secret).encode())


headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic %s' % auth_header.decode()
}

payload = {
    'grant_type': 'client_credentials',
    'code': auth_code,
    'redirect_uri': 'https://open.spotify.com/collection/playlists',
    #'client_id': CLIENT_ID,
    #'client_secret': CLIENT_SECRET,
}
def get_access_token():


    # Make a request to the /token endpoint to get an access token
    access_token_request = requests.post(url=TOKEN_URL, data=payload, headers=headers)

    # convert the response to JSON
    access_token_response_data = access_token_request.json()

    return access_token_response_data['access_token']

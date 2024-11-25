import requests
import json


config = json.loads(open('config.json').read())


def get_token(code: str) -> str:
    token_req = requests.post('https://accounts.spotify.com/api/token',
                              headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                  params={'grant_type': 'authorization_code',
                                          'redirect_uri': 'http://localhost:8000/callback',
                                       'client_id': config['client_id'], 'client_secret': config['client_secret'],
                                          'code': code})
    token = token_req.json()['access_token']
    print(token)
    return token


def send_get(endpoint: str, user_access_token: str, params: {}) -> json:
    url = 'https://api.spotify.com/v1' + endpoint
    response = requests.get(url, headers={'Authorization': f'Bearer {user_access_token}'},
                            params=params)
    return response.json()


def user_login():
    scope = 'user-top-read user-library-read'  # user-read-private user-read-email
    state = 'abcdefghijklmnop'  # randomize
    redirect = 'http://localhost:8000/callback'
    auth_response = requests.get('https://accounts.spotify.com/authorize',
                 params={'response_type': 'code', 'client_id': config['client_id'],
                          'scope': scope, 'redirect_uri': redirect, state: state})
    return auth_response.url


def get_top_items(count: int, start: int, user_access_token: str):
    endpoint = '/me/top/tracks'
    params = {'time_range': 'medium_term', 'limit': count, 'offset': start}
    results = send_get(endpoint, user_access_token, params)
    return results['items']


def get_liked_songs(count: int, start: int, user_access_token: str):
    endpoint = '/me/tracks'
    params = {'limit': count, 'offset': start}
    return send_get(endpoint, user_access_token, params)['items']

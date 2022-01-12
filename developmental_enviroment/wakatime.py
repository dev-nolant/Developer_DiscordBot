import hashlib
import os
import json
import sys
from rauth import OAuth2Service

if sys.version_info[0] == 3:
    raw_input = input


service = OAuth2Service(
    client_id="ci",
    client_secret="cs",
    name='wakatime',
    authorize_url='https://wakatime.com/oauth/authorize',
    access_token_url='https://wakatime.com/oauth/token',
    base_url='https://wakatime.com/api/v1/')

redirect_uri = 'https://wakatime.com/oauth/test'
state = hashlib.sha1(os.urandom(40)).hexdigest()
params = {'scope': 'email,read_stats',
          'response_type': 'code',
          'state': state,
          'redirect_uri': redirect_uri}

url = service.get_authorize_url(**params)

print('**** Visit this url in your browser ****')
print('*' * 80)
print(url)
print('*' * 80)
print('**** After clicking Authorize, paste code here and press Enter ****')
code = raw_input('Enter code from url: ')


def new_decoder(payload):
    print("Decoding")
    return json.loads(payload.decode('utf-8'))


# Make sure returned state has not changed for security reasons, and exchange
# code for an Access Token.
headers = {'Accept': 'application/x-www-form-urlencoded'}
data = {'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri}

print('Getting an access token...')
session = service.get_auth_session(headers=headers,
                                   data=data)

print('Getting current user from API...')
user = session.get('users/current').json()
print('Authenticated via OAuth as {0}'.format(user['data']['email']))
print("Getting user's coding stats from API...")
stats = session.get('users/current/stats')
print(stats.text)

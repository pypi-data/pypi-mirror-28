import time
import json
import requests
from urllib.parse import urlencode
from exceptions import GoogleSheetException


class API:
    _client_id = None
    _client_secret = None
    _api_base_url = 'https://sheets.googleapis.com/v4'
    _auth_url = 'https://accounts.google.com/o/oauth2/auth'
    _exchange_code_url = 'https://accounts.google.com/o/oauth2/token'
    _scope = [
        'https://www.googleapis.com/auth/spreadsheets',
    ]
    _token = None

    def __init__(self, client_id, client_secret, token=None):
        self._client_id = client_id
        self._client_secret = client_secret
        self.set_token(token)

    def get_auth_url(self, redirect_uri, **kwargs):
        kwargs = {**{
            'response_type': 'code',
            'redirect_uri': redirect_uri,
            'client_id': self._client_id,
            'access_type': 'offline',
            'approval_prompt': 'force'
        }, **kwargs}

        if 'scope' not in kwargs:
            kwargs['scope'] = self._scope

        kwargs['scope'] = ' '.join(kwargs['scope'])

        return self._auth_url+'?'+urlencode(kwargs)

    def exchange_code(self, code, redirect_uri):
        data = {
            'code': code, 'client_id': self._client_id, 'client_secret': self._client_secret,
            'redirect_uri': redirect_uri, 'grant_type': 'authorization_code'
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = self._request('post', self._exchange_code_url, data=data, headers=headers)

        if response and 'access_token' in response:
            response['created'] = int(time.time())
            self._token = response

        return response

    def refresh_token(self):
        if self._token and isinstance(self._token, dict) and 'refresh_token' in self._token:
            data = {
                'client_id': self._client_id, 'client_secret': self._client_secret,
                'refresh_token': self._token['refresh_token'], 'grant_type': 'refresh_token'
            }
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            response = self._request('post', self._exchange_code_url, data=data, headers=headers)

            if response and 'access_token' in response:
                response['created'] = int(time.time())
                self._token = {**self._token, **response}

            return self._token

    def get_profile(self):
        return self._request('get', 'https://www.googleapis.com/oauth2/v1/userinfo')

    def set_token(self, token):
        if isinstance(token, str):
            token = json.loads(token)

        if token and isinstance(token, dict) and 'access_token' in token:
            self._token = {**self._token, **token} if self._token else token

    def is_token_expired(self):
        if not self._token and 'access_token' not in self._token:
            return True

        created = 0

        if 'created' in self._token:
            created = self._token['created']

        return (created + (self._token['expires_in'] - 30)) < int(time.time())

    def read(self, sheet_id, ranges, params=None):
        if params is None:
            params = {}

        ranges = ranges if isinstance(ranges, str) else '&ranges='.join(ranges)

        return self._get('/spreadsheets/{}/values:batchGet?ranges={}'.format(sheet_id, ranges), params)

    def update(self, sheet_id, data, params=None):
        if params is None:
            params = {}

        params = {**params, **{
            'valueInputOption': 'USER_ENTERED'
        }}

        if isinstance(data, dict):
            return self._put('/spreadsheets/{}/values/{}'.format(sheet_id, data['range']), {}, json=data, params=params)
        else:
            params['data'] = data
            return self._post('/spreadsheets/{}/values:batchUpdate'.format(sheet_id), None, json=params)

    def _get(self, endpoint, data=None, **kwargs):
        if data is None:
            data = {}

        return self._request('get', self._endpoint(endpoint), data=data, **kwargs)

    def _put(self, endpoint, data=None, **kwargs):
        if data is None:
            data = {}

        return self._request('put', self._endpoint(endpoint), data=data, **kwargs)

    def _post(self, endpoint, data=None, **kwargs):
        if data is None:
            data = {}

        return self._request('post', self._endpoint(endpoint), data=data, **kwargs)

    def _endpoint(self, endpoint):
        return self._api_base_url+endpoint

    def _request(self, method, url, **kwargs):
        if self._token and isinstance(self._token, dict) and 'access_token' in self._token:
            if 'params' in kwargs:
                kwargs['params']['access_token'] = self._token['access_token']
            else:
                kwargs['params'] = {'access_token': self._token['access_token']}

        result = getattr(requests, method)(url, **kwargs)
        _response = result.json()

        if _response and 'error' in _response:
            if isinstance(_response['error'], str):
                raise GoogleSheetException(result.status_code, _response['error'], result)
            else:
                raise GoogleSheetException(_response['error']['code'], _response['error']['message'], result)

        if result.status_code != 200:
            raise GoogleSheetException(result.status_code, result.reason, result)

        return self.response(result)

    @staticmethod
    def response(response):
        return response.json()

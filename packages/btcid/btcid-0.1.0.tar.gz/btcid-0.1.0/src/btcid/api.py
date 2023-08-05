from future import standard_library
standard_library.install_aliases()

from time import time
import urllib.parse
import requests
import hashlib
import hmac


PUBLIC_URL = 'https://vip.bitcoin.co.id/api'
PRIVATE_URL = 'https://vip.bitcoin.co.id/tapi'


class ApiException(Exception):
    pass


class Api(object):
    def __init__(self, api_key, secret_key, public_url=PUBLIC_URL,
                 private_url=PRIVATE_URL):
        super(Api, self).__init__()
        self.api_key = api_key
        self.secret_key = secret_key
        self.public_url = public_url
        self.private_url = private_url

    def form_encode(self, data={}):
        return urllib.parse.urlencode(data).encode('utf8')

    def sign(self, payload, secret):
        key = secret.encode('utf8')
        return hmac.new(key, payload, hashlib.sha512).hexdigest()

    def call(self, method, params={}):
        params[u'nonce'] = int(time() * 1000)
        params[u'method'] = method
        payload = self.form_encode(params)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Key': self.api_key,
            'Sign': self.sign(payload, self.secret_key),
        }
        result = requests.post(self.private_url, headers=headers, data=payload).json()
        if result['success'] != 1:
            raise ApiException(result['error'])
        return result['return']

    def __getattr__(self, name):
        def wrapper(**kwargs):
            return self.call(method=name, params=kwargs)

        return wrapper

import json
from utility import byteify
from tweepy import OAuthHandler


class CustomAuthHandler(OAuthHandler):

    def __init__(self, access_token, access_token_secret, consumer_key, consumer_secret):
        super(CustomAuthHandler, self).__init__(consumer_key, consumer_secret)
        super(CustomAuthHandler, self).set_access_token(access_token, access_token_secret)


class AuthManager:

    auth_handlers = []

    def __init__(self, credentials_file_path):
        self.credentials_file_path = credentials_file_path
        self.set_auth_handlers()

    def set_auth_handlers(self):
        with open(self.credentials_file_path, 'r') as credentials_file:
            credentials = byteify(json.load(credentials_file))

        for item in credentials:
            auth_handler = CustomAuthHandler(item['access_token'], item['access_token_secret'], item['consumer_key'],
                                             item['consumer_secret'])
            self.auth_handlers.append(auth_handler)

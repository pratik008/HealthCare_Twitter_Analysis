"""Read About tweepy at
http://pythoncentral.org/introduction-to-tweepy-twitter-for-python/

Todos:
  * Options for both stdout and file streaming.
"""

from collections import namedtuple

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import tweepy

TWITTER_CONFIGS = 'config.json'
MEDICAL_HASHTAGS = 'medical_hashtags.json'


def get_twitter_configs():
    config = json.load(open(TWITTER_CONFIGS, 'r'))
    twitter_configs = namedtuple(
        'TwitterConfigs',
        'consumer_key, consumer_secret, access_token, access_token_secret')

    # Go to http://dev.twitter.com and create an app.
    # The consumer key and secret will be generated for you.
    twitter_configs.consumer_key = config["consumer_key"]
    twitter_configs.consumer_secret = config["consumer_secret"]
    
    # After the step above, you will be redirected to your app's page.
    # Create an access token under the the "Your access token" section.
    twitter_configs.access_token = config["access_token"]
    twitter_configs.access_token_secret = config["access_token_secret"]
    return twitter_configs


def get_medical_hashtags():
    medical_hashtags = json.load(open(MEDICAL_HASHTAGS, 'r'))
    return medical_hashtags['symplur']


class StdOutListener(StreamListener):
    ''' Handles data received from the stream. '''

    def on_status(self, status):
        # Prints the text of the tweet

        print('Tweet text: ' + status.text.encode('utf-8'))
        directAttrs = ('place,coordinates,lang,created_at,'
                       'retweeted_status,source source_url').split(',')
        for k in directAttrs:
            value = getattr(status, k, None)
            if value is not None:
                print k, str(value).encode('utf-8')
        userAttrs = 'screen_name,location'.split(',')
        for k in userAttrs:
            value = getattr(status, k, None)
            if value is not None:
                print k, str(value).encode('utf-8')

        return True

    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True  # To continue listening

    def on_timeout(self):
        print('Timeout...')
        return True  # To continue listening


if __name__ == '__main__':
    listener = StdOutListener()
    twitter_configs = get_twitter_configs()
    auth = tweepy.OAuthHandler(twitter_configs.consumer_key,
                               twitter_configs.consumer_secret)
    auth.set_access_token(twitter_configs.access_token,
                          twitter_configs.access_token_secret)
    
    stream = Stream(auth, listener)
    tracklists = get_medical_hashtags()
    for tracklist in tracklists:
        stream.filter(track = tracklist)

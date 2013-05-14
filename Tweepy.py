#Read About tweepy at http://pythoncentral.org/introduction-to-tweepy-twitter-for-python/

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import tweepy

config_json = open('config.json', 'r')
config = json.load(config_json)

print 

# Go to http://dev.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key    = config["consumer_key"]
consumer_secret = config["consumer_secret"]

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token = config["access_token"]
access_token_secret = config["access_token_secret"]


class StdOutListener(StreamListener):
    ''' Handles data received from the stream. '''

    def on_status(self, status):
        # Prints the text of the tweet

        print('Tweet text: ' + status.text.encode('utf-8'))
        directAttrs = 'place,coordinates,lang,created_at,retweeted_status,source source_url'.split(',')
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
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, listener)
    stream.filter(track=['Medical', 'Hospital', 'Doctor', 'Nurse', "dentist", "cancer", "heart attack", "dehydration"])
    

'''
    for attr, value in status.__dict__.iteritems():
        print attr, ": ", value
'''

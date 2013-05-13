#Read About tweepy at http://pythoncentral.org/introduction-to-tweepy-twitter-for-python/

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import tweepy

# Go to http://dev.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="3afLWFCa3FeMtKzcQs3x0Q"
consumer_secret="7leKFKI9Gkyi9VFeElUUnTd1MzaVnGT7d9VjVE"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="1414094952-cq2gGGDeqt5TbPh5PGzAmZ8OH3Woi438fPNos36"
access_token_secret="hBaHmAL1nuOfNNL1zV1tIGLptqw9973s44hgVcj7mM"

class StdOutListener(StreamListener):
    ''' Handles data received from the stream. '''
 
    def on_status(self, status):
        # Prints the text of the tweet
        print('Tweet text: ' + status.text.encode('utf-8'))
 
        # There are many options in the status object,
        # hashtags can be very easily accessed.
        #for hashtag in status.entries['hashtags']:
            #print(hashtag['text'])
 
        return True
 
    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True # To continue listening
 
    def on_timeout(self):
        print('Timeout...')
        return True # To continue listening
 
if __name__ == '__main__':
    listener = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
 
    stream = Stream(auth, listener)
    stream.filter(track=['Medical','Hospital','Doctor'])

import sys
import os
import jsonpickle
import tweepy
import datetime

MAX_TWEETS = 10000000
TWEETS_PER_QUERY = 100

class TweetsDownloader:
    def __init__(self,data_dir,tag,auth_manager):
        self.searchQuery = tag
        self.api = tweepy.API(auth_manager.auth_handlers[0])
        self.dir = os.path.join(data_dir,tag,datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        self.fName = '{0}/{0}.json'.format(self.dir)
        self.sinceId = None
        self.max_id = -1L
        self.tweetCount = 0
        self.downloadTweets()

    def downloadTweets(self):
        print("Downloading max {0} tweets".format(MAX_TWEETS))
        with open(self.fName, 'w+') as f:
            while self.tweetCount < MAX_TWEETS:
                try:
                    if (self.max_id <= 0):
                        if (not self.sinceId):
                            new_tweets = self.api.search(q=self.searchQuery, count=TWEETS_PER_QUERY)
                        else:
                            new_tweets = self.api.search(q=self.searchQuery, count=TWEETS_PER_QUERY,
                                                    since_id=self.sinceId)
                    else:
                        if (not self.sinceId):
                            new_tweets = self.api.search(q=self.searchQuery, count=TWEETS_PER_QUERY,
                                                    max_id=str(self.max_id - 1))
                        else:
                            new_tweets = self.api.search(q=self.searchQuery, count=TWEETS_PER_QUERY,
                                                    max_id=str(self.max_id - 1),
                                                    since_id=self.sinceId)
                    if not new_tweets:
                        print("No more tweets found")
                        break
                    for tweet in new_tweets:
                        f.write(jsonpickle.encode(tweet._json, unpicklable=False) +
                                '\n')
                    self.tweetCount += len(new_tweets)
                    print("Downloaded {0} tweets".format(self.tweetCount))
                    self.max_id = new_tweets[-1].id
                except tweepy.TweepError as e:
                    # Just exit if any error
                    print("some error : " + str(e))
                    break
        print ("Downloaded {0} tweets, Saved to {1}".format(self.tweetCount, self.fName))

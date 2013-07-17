##########################################################
#
# Author: Longbo Qiao
# email: longboqiao@gmail.com
# date: June 2013
#
##########################################################
import json
import csv
import collections
import re

from textProc import *
from readColFromFile import *



def tweetsProc(alist,outputFile):
    CleanedTweets = open(outputPath+outputFile,'wb')
    outputCleanedTweetsWriter = csv.writer(CleanedTweets,delimiter='^')
    for tweet in alist:
        #tweets = ''
        #tweets = tweet.decode('utf-8')
        tweets = negconv(tweet)
        tweets = removeLinks(tweets)
        tweets = removeat(tweets)
        tweets = removePunc(tweets)
        filtered_words = []
        tweets = removestop(tweets)
        tweets = toLowercase(tweets)
        print tweets
        outputCleanedTweetsWriter.writerow([tweets])
    return cleanedTweets

cleanedTweets = []
outputList = []
data_by_csv =[]
stopword = []
filtered_words = []
outputPath =  'processed/'
inputPath = '../Data Collection/processed/'
rawTweets = 'Tweets_with_cols.txt'
outputCleanedTweets = "cleanedTweetsOnlyFull.txt"

tweetsProc(readColFromFile(inputPath,rawTweets,7),outputCleanedTweets)

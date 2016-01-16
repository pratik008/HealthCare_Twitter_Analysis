import sys
import json
import os
from concurrence_util import *


def main():
    if len(sys.argv) < 4:
        print "$ score_keywords [afinnFile] [tweetTextFile] [outputDirectory]"
        quit()
    exportScore(processTweets(dumpAfinn(sys.argv[1])))
    
def processTweets(afinn):
    tweetsPath = open(sys.argv[2])
    tweets = {}
    for line in tweetsPath:
        for word in splitTweet(line):
            word = trimWord(word)
            if word is False: continue
            if not tweets.get(word,False):
                tweets[word] = {"occurance_count":0,"sentiment":0}
            sentiment = afinn.get(word,False)
            if sentiment is not False:
                tweets[word]["sentiment"] += int(sentiment)
            tweets[word]["occurance_count"] += 1
    return tweets
    
def exportScore(scores):
    outPath = open(os.path.join(sys.argv[3],'score.csv'),'w+')
    outPath.write('keyword,occurance_count,sentiment\n')
    for keyword in scores:
        s = scores[keyword]
        outPath.write(keyword+','+str(s["occurance_count"])+','+str(s["sentiment"])+'\n')
    outPath.close()
    
if __name__ == '__main__':
    main()
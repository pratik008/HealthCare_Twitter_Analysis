###############################################################
# Author: Liang Tao
# Modified by: Longbo Qiao
# Original File Name: 1_sentiment_for_each_tweet.py
#
# Calculate sentiment score for each tweet and output to a file
###############################################################
import sys
import json
import csv

def main():
    scoreTable = open(dictionaryfilePath+ dictionaryfileName)
    tweets_file = open(textfilePath+textfileName)
    sentimentResult = open(outputFilePath +'sentiment4Tweets.txt','w')
    scores = {}
    wdict ={}
    get = wdict.get
    for line in scoreTable:
        term, score  = line.split("\t")
        scores[term] = int(score)
        wdict[term] = get(term, 0) + 1


    for line in tweets_file:
        point = 0
        #print 'this is the tweets ->> ' + line
        for word in line.split():
            if word in wdict:
                point += scores[word]
            else:
                point += 0
             #print float(point)
        item = str(point) + '^' + line
        sentimentResult.write(item)
    sentimentResult.close()


if __name__ == '__main__':
    dictionaryfilePath = '../../Dictionaries/'
    dictionaryfileName = 'AFINN-111.txt'
    textfilePath = '../../Cleanup Scripts/processed/'
    textfileName = 'cleanedTweetsOnlyFull.txt'
    outputFilePath = 'processed/'
    main()
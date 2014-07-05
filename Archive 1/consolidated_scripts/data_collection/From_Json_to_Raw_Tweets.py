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


def TweetTextProc(inputFileName,outputFileName,inputPath,outputPath):

    timestampedjson = open(inputPath+ inputFileName, "r")
    fulloutput = open(outputPath+outputFileName,'wb')
    fulloutputwriter = csv.writer(fulloutput,delimiter='^')
    none = "\n"
    i = 1
    fulloutputwriter.writerow(["name","created_time", "tweet_id", "user_twitter_name","followers_count","friends_count","time_zone","tweet_text"])
    for item in timestampedjson.readlines():
        d = collections.defaultdict(list)
        data = json.loads(item)
        try:
            if data["lang"] == 'en': #only english tweets will be displayed
                if 'created_at' in data:
                    if(len(data["created_at"]) > 0):
                        d["created_at"].append(data["created_at"])
                else: d["created_at"].append(none)

                if 'id' in data:
                    if(len(str(data["id"])) > 0):
                        d["id"].append(str(data["id"]))
                else: d["id"].append(none)

                if 'text' in data:
                    if(len(data["text"]) > 0):
                        tweets = ''
                        tweets = data["text"].encode('utf-8')

                        d["text"].append(tweets)
                else: d["text"].append(none)

                if 'screen_name' in data['user']:
                    if(len(data["user"]["screen_name"]) > 0):
                        d["screen_name"].append(data["user"]["screen_name"].encode('utf-8'))
                else: d["screen_name"].append(none)

                if 'name' in data['user'] is not None:
                    if 'name' in data['user']:
                        if(len(data["user"]["name"]) > 0):
                            d["name1"].append(data["user"]["name"].encode('utf-8'))
                    else: d["name1"].append(none)
                else: d["name1"].append(none)

                if 'followers_count' in data['user']:
                    if(len(str(data["user"]["followers_count"])) > 0):
                        d["followers_count"].append(data["user"]["followers_count"])
                else: d["followers_count"].append(none)

                if 'friends_count' in data['user']:
                    if(len(str(data["user"]["friends_count"])) > 0):
                        d["friends_count"].append(data["user"]["friends_count"])
                else: d["friends_count"].append(none)

                if 'time_zone' in data["user"]:
                    d["time_zone"].append(data["user"]["time_zone"])
                else: d["time_zone"].append(none)

                #fulloutputwriter.writerow([d["created_at"][0],d["id"][0],d["screen_name"][0],d["text"][0]])
                fulloutputwriter.writerow([d["name1"][0],d["created_at"][0],d["id"][0],d["screen_name"][0],d["followers_count"][0],d["friends_count"][0],d["time_zone"][0],d["text"][0]])
                d['text'] = []
                i = i + 1
                #print i
        except IndexError as err:
            print "IndexError"
        except KeyError as err:
            print "lang not exists"
    timestampedjson.close()


#####  M  A  I  N ######
print 'Starting the script...'
print 'Parsing TimeStamped Json to CSV...'
outputList = []
data_by_csv =[]
stopword = []
filtered_words = []
outputPath = 'processed/'
inputPath = 'processed/'

#@input Json:   sample input from json code
readFromJsonDumpFileName = "output_with_phrases.txt"
#@output csv:   output the raw tweets(without cleaning)
rawTweets = "Tweets_with_cols.txt"

TweetTextProc(readFromJsonDumpFileName,rawTweets,inputPath,outputPath)
print 'Parsing TimeStamped Json to CSV...Done' + '(' + rawTweets + ')'
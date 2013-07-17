##########################################################
#
# Author: Hans Goldman
# email: hansjgoldman@gmail.com
# date: June 2013
#
##########################################################

import os


##########################################################
#
# Author: Hans Goldman
# email: hansjgoldman@gmail.com
# date: June 2013
# Fuction: filterWords()
# Purpose: filter non-necessary words out of tweets.
#
def filterWords():
    wordSet = loadWordsIntoSet(dictionariesPath + dictionariesFile)
    try:
        inputTweetsFileHandle = open(inputTweetsFilePath + inputTweetsFileName, 'r')
        outputTweetsFileHandle = open(outputTweetsFilePath + outputTweetsFileName, 'w')
        newLineChar = ['\n']
        for line in inputTweetsFileHandle:
            line = line.split()
            outputList = []
            for word in line:
                if word in wordSet:
                    outputList.append(word)
            outputTweetsFileHandle.write(' '.join(outputList) + ''.join(newLineChar))
        inputTweetsFileHandle.close()
        outputTweetsFileHandle.close()
        print 'Done!'
    except IOError as e:
        print("{}".format(e))


##########################################################
#
# Author: Hans Goldman
# email: hansjgoldman@gmail.com
# date: June 2013
# Fuction: loadWordsIntoSet()
# Purpose: Read in all words from a local dictionary
#          file and return them all as a set.
#
def loadWordsIntoSet(dictionaryName):
    aList = []
    try:
        keywordFile = open(dictionaryName, 'r')
        for line in keywordFile:
            #remove '\n' and make all text lowercase.
            aList.append(line[:-1].lower())
        print len(aList), "words loaded from", dictionaryName
        keywordFile.close()
    except IOError as e:
        print("{}".format(e))
    return set(aList)


dictionariesPath = '../../Dictionaries/'
dictionariesFile = 'newWL_new.csv'
inputTweetsFilePath = '../../Cleanup Scripts/processed/'
inputTweetsFileName = 'cleanedTweetsOnlyFull.txt'
outputTweetsFilePath = 'processed/'
outputTweetsFileName = 'removedBynewWLTweets.txt'
filterWords()

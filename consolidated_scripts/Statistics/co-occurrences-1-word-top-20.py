##########################################################
#
# Author: Hans Goldman
# email: hansjgoldman@gmail.com
# date: June 2013
#
##########################################################

import json
import os
from collections import OrderedDict

def findCooccurences():
    connDict = {}
    inputFileHandle = open(processedPath + inputFileName,'r')
    for singleInputLine in inputFileHandle:
        currentJSONline = json.loads(singleInputLine)
        #Remove all line breaks and convert all characters to lowercase. 
        tweetText = currentJSONline['text'].replace('\n', ' ').lower()
        #Remove all characters NOT in alphabet
        tempTweet = []
        for char in tweetText:
            if char in alphabet:
                tempTweet.append(char)
        tweetAsString = ''.join(tempTweet)
        tweetWordList = tweetAsString.split()
        tempTweetDict = {}
        for word in tweetWordList:
            if word not in excludeWords:
                if word in tempTweetDict:
                    tempTweetDict[word] = tempTweetDict[word] + 1
                else:
                    tempTweetDict[word] = 1
        if inputWord in tempTweetDict:
            for word in tempTweetDict:
                for connection in tempTweetDict:
                    if tempTweetDict[word] == tempTweetDict[connection] and tempTweetDict[word] > 1:
                        if word in connDict:
                            if connection in connDict[word]:
                                connDict[word][connection] += 1
                            else:
                               connDict[word][connection] = 1
                        else:
                            connDict[word] = {}
                            connDict[word][connection] = 1
                    elif word != connection:
                        if word in connDict:
                            if connection in connDict[word]:
                                connDict[word][connection] += 1
                            else:
                               connDict[word][connection] = 1
                        else:
                            connDict[word] = {}
                            connDict[word][connection] = 1
    writeToFile(connDict)
    print 'Task Completed Successfully!'


##########################################################
#
# Fuction: writeToFile(aDict)
# Purpose: Output data to a file for later use. 
# Parameters:
#   text: the data to be written to the file.
#
def writeToFile(aDict):
    try:
        outFile = open(processedPath + outputFileName, 'w')
    except IOError as e:
        print("{}".format(e))

    singleValueDict = reversed(OrderedDict(sorted(aDict[inputWord].items(), key=lambda t: t[1])))
    count = 0
    for connection in singleValueDict:
        outputList = []
        outputList.append(inputWord)
        outputList.append(' : ')
        outputList.append(connection)
        outputList.append(',')
        outputList.append(str(aDict[inputWord][connection]))
        outputList.append('\n')
        outFile.write(''.join(outputList))
        count += 1
        if count >= 20: break
    outFile.close()


##########################################################
#
# Fuction: loadWordsIntoSet()
# Purpose: Read in all words from a local dictionary
#          file and store them all in a list.
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


##########################################################
#
# Fuction: getAlphabet()
# Purpose: Create an alphabet of characters used in 
#          keywords. Mainly needed to get special
#          characters if they exist in the Dictionary.
#
def getAlphabet(keywordDict, prefixDict, postfixDict):
    standardChars = ['a','b','c','d','e','f','g','h',
                     'i','j','k','l','m','n','o','p',
                     'q','r','s','t','u','v','w','x',
                     'y','z',' ','0','1','2','3','4',
                     '5','6','7','8','9','&','@','#']
    alphabetOfChars = []
    #Add all characters from keywords dictionary
    for word in keywordDict:
        for char in word:
            if char not in alphabetOfChars:
                alphabetOfChars.append(char)
    #Add all characters from prefixes[]
    for word in prefixDict:
        for char in word:
            if char not in alphabetOfChars:
                alphabetOfChars.append(char)
    #Add all characters from postfixes[]
    for word in postfixDict:
        for char in word:
            if char not in alphabetOfChars:
                alphabetOfChars.append(char)
    #Add all characters from standardChars[]
    for char in standardChars:
        if char not in alphabetOfChars:
            alphabetOfChars.append(char)
    return set(alphabetOfChars)


inputWord = raw_input('Please Enter a word: ').lower()
processedPath  = 'processed/'
outputFileName = 'co-occurrence-' + inputWord + '.csv'
inputFileName  = 'output.txt'

#Load the keyword dictionaries
keywords     = loadWordsIntoSet('keywords_v2.csv')
excludeWords = loadWordsIntoSet('exclude-words.csv')
prefixes     = loadWordsIntoSet('prefixes.csv')
postfixes    = loadWordsIntoSet('postfixes.csv')
alphabet     = getAlphabet(keywords, prefixes, postfixes)

findCooccurences()

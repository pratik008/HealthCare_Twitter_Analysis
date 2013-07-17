##########################################################
#
# Author: Hans Goldman
# email: hansjgoldman@gmail.com
# date: June 2013
#
##########################################################

import json
import os
import glob
import time
import re

def parseDataFiles():
    listOfFiles = getFileList(dumpPath)
    for currentFile in listOfFiles:
        #Parse the current file to get only the tweet text
        print dumpPath + currentFile
        inputFileHandle = open(dumpPath + currentFile,'r')
        currentJSON = json.loads(inputFileHandle.read())
        for tweet in currentJSON:
            #Remove all line breaks and convert all characters to lowercase.
            tweetText = tweet['text'].replace('\n', ' ').lower()
            for phrase in keyPhrases:
                if tweetText.find(phrase) != -1:
                    matchFound(tweet, outputFileAndPath)
                    print 'Phrase found! Phrase =', phrase
                    print 'tweetText:', tweetText, '\n'
                    break
            #Remove all characters NOT in alphabet
            tempTweet = []
            for char in tweetText:
                if char in alphabet:
                    tempTweet.append(char)
            tweetAsString = ''.join(tempTweet)
            tweetWordList = tweetAsString.split()
            #Look for words in keywords dictionaries
            for word in tweetWordList:
                if word in keywords:
                    matchFound(tweet, outputFileAndPath)
                elif re.search("[0-9]", word) is None:
                    found = False
                    for prefix in prefixes:
                        if word.startswith(prefix) and len(word) > len(prefix):
                            matchFound(tweet, outputFileAndPath)
                            found = True
                    if found == False:
                        for postfix in postfixes:
                            if word.endswith(postfix) and len(word) > len(postfix):
                                matchFound(tweet, outputFileAndPath)
        inputFileHandle.close()
        #Delete file to save space because no keywords were found in it
        os.remove(dumpPath + currentFile)


##########################################################
#
# Fuction: matchFound(aTweet, outFile)
# Purpose: handles the case of a match found in algorithm
#          Prints output to the user and writes data to a
#          file.
#
def matchFound(aTweet, outFile):
    outputFileHandle = open(outFile,'a')
    json.dump(aTweet, outputFileHandle)
    outputFileHandle.write('\n')
    outputFileHandle.close()
    #print "Match found!"


##########################################################
#
# Fuction: getFileList()
# Purpose: Get all twitter data files from the data dump
#          and store them in a list.
#
def getFileList(path):
    fileList = []
    for currentFile in glob.glob(path + '*.json'):
        filename = currentFile[len(path):len(currentFile)]
        fileList += [filename]
    return fileList


##########################################################
#
# Fuction: loadWordsIntoSet()
# Purpose: Read in all words from a local dictionary
#          file and store them all in a set.
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
# Fuction: loadWordsAndPhrasesIntoSet()
# Purpose: Read in all lines from a local dictionary
#          file and store them all in a set.
#
def loadWordsAndPhrasesIntoSet(dictionaryName):
    wordList = []
    phraseList = []
    aDict = {}
    try:
        keywordFile = open(dictionaryPath+ dictionaryName, 'r')
        for line in keywordFile:
            if line.find(' ') == -1:
                #remove '\n' and make all text lowercase.
                wordList.append(line[:-1].lower())
            else:
                #remove '\n' and make all text lowercase.
                phraseList.append(line[:-1].lower())
        print len(wordList), "words loaded from", dictionaryName
        print len(phraseList), "phrases loaded from", dictionaryName
        keywordFile.close()
        aDict['keywordsSet'] = set(wordList)
        aDict['phrasesSet'] = set(phraseList)
    except IOError as e:
        print("{}".format(e))
    return aDict


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
                     '5','6','7','8','9','&']
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


dumpPath = 'dump/'
dictionaryPath = '../Dictionaries/'
processedPath = 'processed/'
outputFileName = 'output_with_phrases.txt'
outputFileAndPath = processedPath + outputFileName

#Load the keyword dictionaries
keysDict    = loadWordsAndPhrasesIntoSet('keywords_v2.csv')
keywords    = keysDict['keywordsSet']
keyPhrases  = keysDict['phrasesSet']

prefixes  = loadWordsIntoSet(dictionaryPath+'prefixes.csv')
postfixes = loadWordsIntoSet(dictionaryPath+'postfixes.csv')

alphabet  = getAlphabet(keywords, prefixes, postfixes)

#Used for debugging:
#for char in alphabet:
#    print char

while True:
    parseDataFiles()
    #time.sleep(1)

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
import re    #Regular Expressions
import time


##########################################################
#
# Fuction: countWords()
# Purpose: Count the occurrence of each word from the
#          dictionary file in the saved tweets.
#
def countWords():
    processedPath1       = '../Data Collection/processed/'
    processedPath  = 'processed/'
    outputFileName = 'output_with_phrases.txt'
    dictionaryPath = '../Dictionaries/'
    listOfPrefixWords = 'prefix_words.csv'
    listOfPostfixWords = 'postfix_words.csv'

    keywordStatsFileName  = 'stats_keywords.csv'
    prefixStatsFileName   = 'stats_prefixes.csv'
    postfixStatsFileName  = 'stats_postfixes.csv'

    keywords  = loadWordsIntoSet('keywords_v2.csv')
    prefixes  = loadWordsIntoSet('prefixes.csv')
    postfixes = loadWordsIntoSet('postfixes.csv')

    alphabet = getAlphabet(keywords)

    keywordCountDictionary = {}
    prefixCountDictionary = {}
    postfixCountDictionary = {}

    lengthOfLongestWord = 0
    for word in keywords:
        if lengthOfLongestWord < len(word):
            lengthOfLongestWord = len(word)
        keywordCountDictionary[word] = 0
    for word in prefixes:
        if lengthOfLongestWord < len(word):
            lengthOfLongestWord = len(word)
        prefixCountDictionary[word] = 0
    for word in postfixes:
        if lengthOfLongestWord < len(word):
            lengthOfLongestWord = len(word)
        postfixCountDictionary[word] = 0

    #Parse the current file to get only the tweet text
    print "Counting keywords in:", processedPath + outputFileName
    print "Please wait, this may take a minute..."
    inputFileHandle = open(processedPath1 + outputFileName,'r')
    prefixesFoundFileHandle = open(processedPath + listOfPrefixWords,'w')
    postfixesFoundFileHandle = open(processedPath + listOfPostfixWords,'w')
    for singleInputLine in inputFileHandle:
        currentJSONline = json.loads(singleInputLine)
        #Remove all line breaks and convert all characters to lowercase.
        tweetText = currentJSONline['text'].replace('\n', ' ').lower()
        #Remove all characters NOT in alphabet
        tempTweet = ""
        for char in tweetText:
            if char in alphabet:
                tempTweet += char
        tweetWordList = tempTweet.split()
        for word in tweetWordList:
            #Count all keywords in tweet
            if word in keywords:
                keywordCountDictionary[word] += 1
            #Count all prefixes in tweet
            for prefix in prefixes:
                if word.startswith(prefix) and len(word) > len(prefix):
                    prefixCountDictionary[prefix] += 1
                    prefixesFoundFileHandle.write(word + '\n')
            #Count all postfixes in tweet
            for postfix in postfixes:
                if word.endswith(postfix) and len(word) > len(postfix):
                    postfixCountDictionary[postfix] += 1
                    postfixesFoundFileHandle.write(word + '\n')
    inputFileHandle.close()
    prefixesFoundFileHandle.close()
    postfixesFoundFileHandle.close()
    spaceChar = ' '
    print "\n"
    print "---------------------------------------"
    print "Keyword" + spaceChar * (lengthOfLongestWord - 7) + " | Count"
    print "---------------------------------------"
    statsFileHandle = open(processedPath + keywordStatsFileName,'w')
    for entry in keywordCountDictionary:
        if keywordCountDictionary[entry] > 0:
            emptySpaces = spaceChar * (lengthOfLongestWord - len(entry))
            print entry, emptySpaces + ":", keywordCountDictionary[entry]
            statsFileHandle.write(entry + "," + str(keywordCountDictionary[entry]) + "\n")
    statsFileHandle.close()

    print "\n"
    print "---------------------------------------"
    print "Prefix" + spaceChar * (lengthOfLongestWord - 6) + " | Count"
    print "---------------------------------------"
    statsFileHandle = open(processedPath + prefixStatsFileName,'w')
    for entry in prefixCountDictionary:
        if prefixCountDictionary[entry] > 0:
            emptySpaces = spaceChar * (lengthOfLongestWord - len(entry))
            print entry, emptySpaces + ":", prefixCountDictionary[entry]
            statsFileHandle.write(entry + "," + str(prefixCountDictionary[entry]) + "\n")
    statsFileHandle.close()

    print "\n"
    print "---------------------------------------"
    print "Postfix" + spaceChar * (lengthOfLongestWord - 7) + " | Count"
    print "---------------------------------------"
    statsFileHandle = open(processedPath + postfixStatsFileName,'w')
    for entry in postfixCountDictionary:
        if postfixCountDictionary[entry] > 0:
            emptySpaces = spaceChar * (lengthOfLongestWord - len(entry))
            print entry, emptySpaces + ":", postfixCountDictionary[entry]
            statsFileHandle.write(entry + "," + str(postfixCountDictionary[entry]) + "\n")
    statsFileHandle.close()


##########################################################
#
# Fuction: loadWordsIntoSet()
# Purpose: Read in all words from a local dictionary
#          file and store them all in a list.
#
def loadWordsIntoSet(dictionaryName):
    aList = []
    try:
        keywordFile = open(dictionaryPath+dictionaryName, 'r')
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
#          characters.
#
def getAlphabet(keywords):
    charsInWords = []
    standardChars = ['a','b','c','d','e','f','g','h','i','j',
                     'k','l','m','n','o','p','q','r','s','t',
                     'u','v','w','x','y','z',' ','0','1','2',
                     '3','4','5','6','7','8','9','&']

    for word in keywords:
        for char in word:
            if char not in charsInWords:
                charsInWords.append(char)

    for char in standardChars:
        if char not in charsInWords:
            charsInWords.append(char)
    return set(charsInWords)


##########################################################
#
# Fuction: writeToFile()
# Purpose: Output data to a file for later use.
# Parameters:
#   text: the data to be written to the file.
#
def writeToFile(text):
    try:
        outFile = open(processedPath + outputFileName, 'a')
    except IOError as e:
        print("{}".format(e))
    outFile.write(text.encode('utf8'))
    outFile.close()

dictionaryPath = '../Dictionaries/'
countWords()

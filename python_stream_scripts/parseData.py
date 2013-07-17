##########################################################
#
# Author: Hans Goldman
# email: hansjgoldman@gmail.com
# date: May 2013
#
##########################################################

import json
import os
import glob
import time

def parseDataFiles():
    listOfFiles = getFileList()
    for currentFile in listOfFiles:
        #Parse the current file to get only the tweet text
        print "Reading:", dumpPath + currentFile
        inputFileHandle = open(dumpPath + currentFile,'r')
        currentJSON = json.loads(inputFileHandle.read())
        stringBuffer = ""
        for tweet in currentJSON:
            #Remove all line breaks and convert all characters to lowercase. 
            tweetText = tweet['text'].replace('\n', ' ').lower()
            #Remove all characters NOT in alphabet
            tempTweet = ""
            for char in tweetText:
                if char in alphabet:
                    tempTweet += char
            tweetWordList = tempTweet.split()
            for word in tweetWordList:
                if word in keywords:
                    #stringBuffer += tempTweet + '\n'
                    outputFileHandle = open(processedPath + outputFileName,'a')
                    json.dump(tweet, outputFileHandle)
                    outputFileHandle.write('\n')
                    outputFileHandle.close()
                    print "Match found!"
                    break
        inputFileHandle.close()
        #Append data to output file
        #writeToFile(stringBuffer)
        #Delete file to save space because no keywords were found in it
        os.remove(dumpPath + currentFile)


##########################################################
#
# Fuction: getFileList()
# Purpose: Get all twitter data files from the data dump
#          and store them in a list.
#
def getFileList():
    fileList = []
    for currentFile in glob.glob(dumpPath + '*.json'):
        filename = currentFile[len(dumpPath):len(currentFile)]
        fileList += [filename]
    return fileList


##########################################################
#
# Fuction: loadKeywords()
# Purpose: Read in all keywords from a local dictionary
#          file and store them all in a list.
#
def loadKeywords():
    keywordFile = open("keywords.csv", 'r')
    for line in keywordFile:
        keywords.append(line[:-1].lower())
    print len(keywords), "words loaded from keywords.csv"


##########################################################
#
# Fuction: getAlphabet()
# Purpose: Create an alphabet of characters used in 
#          keywords. Mainly needed to get special
#          characters.
#
def getAlphabet():
    standardChars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ','0','1','2','3','4','5','6','7','8','9']
    for word in keywords:
        for char in word:
            if char not in alphabet:
                alphabet.append(char)
    for char in standardChars:
        if char not in alphabet:
            alphabet.append(char)


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
    

dumpPath = 'dump/'
processedPath = 'processed/'
outputFileName = 'output.txt'
alphabet = []
keywords = []
#Load the keyword dictionary
loadKeywords()
getAlphabet()

#Used for debugging:
#for char in alphabet:
 #   print char

while True:
    parseDataFiles()
    time.sleep(1)

##########################################################
#
# Author: Longbo Qiao
# email: longboqiao@gmail.com
# date: June 2013
#
##########################################################
#   @loadWordsIntoSet(dictionaryName): read the list and convert to set
#   @toLowerCase(text): convert all strings to lowercase
#   @removeLinks(text): remove all the url Links
#   @removePunc(text): remove all puncuations
#   @removeat(text): remove all the "@ed" user names
#   @removestop(text): remove all stopwords
#   @negconv(text): convert some abbreviated negation to full phrases

import json
import csv
import collections
import re
import textmining
import os
import sys
import time
import timeit
from nltk.corpus import stopwords

def loadWordsIntoSet(dictionaryName):
    aList = []
    try:
        keywordFile = open(dictionaryName, 'r')
        for line in keywordFile:
            #remove '\n' and make all text lowercase.
            aList.append(line[:-1].lower())
        print len(aList), "words/lines loaded from", dictionaryName
        keywordFile.close()
    except IOError as e:
        print("{}".format(e))
    return set(aList)

def toLowercase(text):
    return text.lower()

def removeLinks(text):
    URLless_string = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text)
    return URLless_string

def removePunc(text):
    punc=("\",./;():'?&-!")
    strp = text.translate(None, punc)
    return strp

def nonascii(file):
    return text

def removeat(text):
        cleantext = re.sub(r'@([A-Za-z0-9_]+)',"",text).strip()
        cleantext = re.sub(r'&([A-Za-z0-9_]+)',"",cleantext).strip()

        return cleantext

def removestop(text):
    #print text
    stopwordDict = open(dictionaryPath+'stopwords.csv','r')
    filtered_words = []
    splitsent = text.split(' ')
    for w in splitsent:
        #print w
        if not w.lower() in stopwords.words('english'):
            filtered_words.append(w)
    return ' '.join(filtered_words)

def readStopWord(inputPath):
    stopword = loadWordsIntoSet(inputPath + 'stopwords.csv')
    return stopword

def negconv(text):
    text=text.replace("can't", "can not")
    text=text.replace("n't", " not")
    text=text.replace("'re", " are")
    text=text.replace("'ll", " will")

    text=text.replace("'m", " am")
    text=text.replace("'ve'", " have")
    return text



stopword = []
dictionaryPath = '../Dictionaries/'
#publicStopword = readStopWord(dictionaryPath)


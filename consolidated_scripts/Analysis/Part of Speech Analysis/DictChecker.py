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



def loadWordsIntoSet(dictionaryPath,dictionaryName):
    aList = []
    try:
        keywordFile = open(dictionaryPath+dictionaryName, 'r')
        for line in keywordFile:
            #remove '\n' and make all text lowercase.
            aList.append(line[:-1].lower())
        print len(aList), "words/lines loaded from", dictionaryName
        keywordFile.close()
    except IOError as e:
        print("{}".format(e))
    return set(aList)

def isStopword(text):
    filtered_words = []
    splitsent = text.split(' ')
    for w in splitsent:
        if w.lower() in  stopwords.words('english'):
            return 'stopword'
        else:
            return 'pass'

def isSubjective(text):
    splitsent = text.split(' ')
    for w in splitsent:
        if w.lower() in subjectivity:
            return 'subjectivity'
        else:
            return 'pass'

def isHonorific(text):
    splitsent = text.split(' ')
    for w in splitsent:
        if w.lower() in honorific:
            return 'honorific'
        else:
            return 'pass'

def isStdChr(text):
    splitsent = text.split(' ')
    for w in splitsent:
        if w in standardCharsSet:
            return 'lower'
        else:
            return 'pass'

def isStdChrCap(text):
    splitsent = text.split(' ')
    for w in splitsent:
        if w in standardCharsCapSet:
            return 'cap'
        else:
            return 'pass'

def hasPunc(text):
    if text in (w for w in punctuationsSet):
        return 'punc'
    else:
        return 'pass'
def capChk(text):

    if text.isupper():
        print 'all cap'
    else:
        return 'pass'

standardCharsCap = ['A','B','C','D','E','F','G',
                    'H','J','K','L','M','N',
                    'O','P','Q','R','S','T','U',
                    'V','W','X','Y','Z']
standardChars = ['a','b','c','d','e','f','g','h',
                 'i','j','k','l','m','n','o','p',
                 'q','r','s','t','u','v','w','x',
                 'y','z']
punctuations = ['\\',',','/',';','(',')',':','\'','?','&','-','!']
standardCharsSet = set(standardChars)
punctuationsSet = set(punctuations)
standardCharsCapSet = set(standardCharsCap)
dictionaryPath = '../../Dictionaries/'
subjectiveDict = 'subjective_words.txt'
honorificDict = 'honorificDict.txt'

honorific = loadWordsIntoSet(dictionaryPath,honorificDict)
subjectivity = loadWordsIntoSet(dictionaryPath,subjectiveDict)
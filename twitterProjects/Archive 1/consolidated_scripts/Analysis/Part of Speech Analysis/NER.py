##########################################################
#
# Author: Longbo Qiao
# email: longboqiao@gmail.com
# date: June 2013
#
# an alternative solution that preserves the order of the occurrence for each (NNP) word
# and output each (NNP)word to a csv file with its frequency sorted
#
##########################################################
import nltk
import csv
from DictChecker import *

def unique_and_order_list(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]

def feq2csv(alist,outputFileName):
    freqCount = nltk.FreqDist()

    for word in alist:
        freqCount.inc(word)
    #print freqCount
    fp = open(outputFilePath + outputFileName, "wb")
    Frequency = csv.writer(fp, delimiter=',')
    Frequency.writerows(freqCount.items())

def fixFirstWordCap(inputtempFileName,outputtempFileName):
    sampletext = open(inputFilePath+ inputtempFileName, "r")
    outputtempFile = open(outputtempFileName,'w')

    func = lambda s: s[:1].lower() + s[1:] if s else ''
    i = 0
    for line in sampletext:
        i = i + 1
        strp = line.translate(None,'\"')
        firstword,space,restOfwords = strp.partition(' ')
        if isStopword(firstword.lower()) == 'stopword':
            outputtempFile.write(func(line))
        if isStopword(firstword.lower()) == 'pass':
            outputtempFile.write(line)
            continue
        outputtempFile.write('\n')
    outputtempFile.close()
    sampletext.close()

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

def fixHonorific(inputtempFileName,outputtempFileName):

    words2line = []
    inputtempFile = open(inputtempFileName,'r')
    outputtempFile = open(outputtempFileName,'w')


    for line in inputtempFile:
        words = line.split()
        words2line = []
        for word in words:
            #print word
            if word.lower() in honorific:
                #print word
                word = word.lower().title()
                words2line.append(word)
            else:
                words2line.append(word)
                continue
        outputtempFile.write(' '.join(words2line))
        outputtempFile.write('\n')
    outputtempFile.close()

def extract_NNP(t):

    entity_names = []
    honorificContainer = []
    continuousNNPContainer = []

    dictContainer={}
    isHonor = False
    isHonor2 = False
    NNPcontinuous = False

    for tagged_tk in t:
        #print tagged_tk[0]

        # remove capped single alphabets
        if isStdChrCap(str(tagged_tk[0])) == 'cap':
            print str(tagged_tk[0]) + '-> its stdchar'
            continue

        if hasPunc(str(tagged_tk[0])) == 'punc':
            continue
        if isSubjective(str(tagged_tk[0])) == 'subjectivity':
            continue

        if isHonor:
            if isHonor2:
                if tagged_tk[1] == POS_TAG_Wanted:
                    honorificContainer.append(tagged_tk[0])
                    entity_names.append(''.join(x for x in ' '.join(honorificContainer)))
                    isHonor = False
                    isHonor2 = False
                    honorificContainer = []
                    continue
                else:
                    entity_names.append(''.join(x for x in ' '.join(honorificContainer)))
                    isHonor = False
                    isHonor2 = False
                    honorificContainer = []
                    continue
            else:
                honorificContainer.append(tagged_tk[0])
                isHonor2 = True
                continue

        if isHonorific(str(tagged_tk[0])) == 'honorific':# check honorific prefixes
            isHonor = True
            honorificContainer.append(tagged_tk[0])
            continue

        if tagged_tk[1] == POS_TAG_Wanted:
            if isStopword(str(tagged_tk[0])) == 'stopword': #check if this capitalized NNP is a stopword?
                #print str(tagged_tk[0]) + '-> its lower case is stopword'
                NNPcontinous = False
                continue
            else:
                NNPcontinuous = True
        else:
            NNPcontinuous = False

        if NNPcontinuous:
            continuousNNPContainer.append(tagged_tk[0])
        else:
            if continuousNNPContainer:
                entity_names.append(''.join(x for x in ' '.join(continuousNNPContainer)))
                continuousNNPContainer = []
            else:
                continue

    return entity_names

POS_TAG_Wanted = 'NNP'

outputFilePath = 'processed/'
feqcsvFileName = 'freqCount.csv'
inputFilePath = '../../Cleanup Scripts/processed/'
inputFileName = 'sample.txt' #sample tweets
honorificDict = 'honorificDict.txt'
dictionaryPath = '../../Dictionaries/'
tempfilename = 'temp.txt'
subjectiveDict = 'subjective_words.txt'


fixFirstWordCap(inputFileName,tempfilename)


cleanedtext = open(tempfilename,'r')
sentences = nltk.sent_tokenize(cleanedtext.read())
cleanedtext.close()
os.remove(tempfilename) # remove temp file

entity_names_collection = [] # temp list
print "starting..."

print "sentences are tokenized..."
tked_sent = [nltk.word_tokenize(sentence) for sentence in sentences]

tged_elements = [nltk.pos_tag(sentence) for sentence in tked_sent]



'''
test line is not WORKING...

readline = 'print photo Photo pHOTO microsoft facebook scrn man the /dont'
#print hasPunc
sentences = nltk.sent_tokenize(readline)
tked_sent1 = [nltk.word_tokenize(sentence1) for sentence1 in sentences1]
tged_elements1 = [nltk.pos_tag(sentence1) for sentence1 in tked_sent1]

print tged_elements1
i = 0
for eachelement in tged_elements1:
    print eachlement
    for element in eachelement:
        if not element[1] == 'NN':
            print element[0]

'''




for tree in tged_elements:
    entity_names_collection.extend(extract_NNP(tree))

print "entity_names_collection is built..."

#use set because we want unique input
print unique_and_order_list(entity_names_collection) #output the NNP in terms of the order of occurrences
#print freqCount

feq2csv(entity_names_collection,feqcsvFileName)
print "all done"
##########################################################
#
# Author: ?
# Modified by: Longbo Qiao
# email: longboqiao@gmail.com
# date: June 2013
#
##########################################################
import json
import csv
import collections
import re
import textmining
import os
import sys
import time
import timeit
from readColFromFile import *



def termdocumentmatrix_example(inputPath,inputFile,outputPath,outputFile):
    with open(inputPath + inputFile, 'rb') as f:
        tdm = textmining.TermDocumentMatrix()
        count = 1
        for line in f:
            vals = line.split('^')
            try:
                tdm.add_doc(vals[0])
            except IndexError, e:
                print str(count) + "th row data format error"
            count = count + 1
    tdm.write_csv(outputPath + outputFile, cutoff=1)

outputPath =  'processed/'
inputPath = '../../Cleanup Scripts/processed/'
rawTweets = 'Tweets_with_cols.txt'
outputCleanedTweets = "cleanedTweetsOnlyFull.txt"
outputMatrix = 'training_matrix.txt'
#outputMatrix = 'testing_matrix.txt'
termdocumentmatrix_example(inputPath,outputCleanedTweets,outputPath,outputMatrix)
print "Matrix is Done.."
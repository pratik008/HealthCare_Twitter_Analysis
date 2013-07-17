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
def readColFromFile(inputPath,filename,colno):
    textcol=[]
    readtextfromfull = open(inputPath+filename, "r")
    textcolumn = csv.reader(readtextfromfull,delimiter='^')
    next(textcolumn)
    for item in textcolumn:
        #print item[7]

        #test commentout# textcol.append(item[7])
        #test add#
        textcol.append(item[colno])
    print len(textcol), "words loaded from", filename ,"......excluded header"
    return textcol
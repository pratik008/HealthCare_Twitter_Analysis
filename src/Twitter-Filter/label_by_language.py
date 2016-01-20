#!/bin/python

from langdetect import detect
import csv
import os
import sys

def main():
    if len(sys.argv) != 3:
        print "$ label_by_language [topicKeysFile] [language]"
        quit()
    filterLanguages(sys.argv[1],sys.argv[2])
    
def filterLanguages(fname,lang='en'):
    lf = open(os.path.join(os.path.dirname(fname),'topic_keys_labeled.txt'),'w+')
    with open(fname,'rb') as f:
        r = csv.reader(f, delimiter='\t')
        for row in r:
            if detect(row[2]) == lang:
                lf.write('1\t'+'\t'.join(row)+'\n')
            else:
                lf.write('0\t'+'\t'.join(row)+'\n')
    f.close()
    lf.close()
        
if __name__ == "__main__":
    main()
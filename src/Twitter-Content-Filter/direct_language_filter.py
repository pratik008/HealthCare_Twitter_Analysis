#!/bin/python
from __future__ import print_function
from langdetect import detect
from utility import byteify
import json
import os
import sys
import codecs
import re
shortword = re.compile(r'\W*\b\w{1,3}\b')

def main():
    if len(sys.argv) != 3:
        print("$ label_by_language [tweetsJsonFile] [language]")
        quit()
    filterLanguages(sys.argv[1],sys.argv[2])
    
def filterLanguages(fpath,lang='en'):
    fname = os.path.basename(fpath)
    lf = open(os.path.join(os.path.dirname(fpath),'{0}_{1}.json'.format(os.path.splitext(fname)[0],lang)),'w+')
    count = 1
    langCount = 0
    with codecs.open(fpath,encoding="utf-8") as f:
        for line in f:
            tweet = json.loads(line)
            out = shortword.sub('', tweet['text'].encode('ascii','ignore'))
            if not out or out == '': continue
            if detect(out) == lang:
                lf.write(str(json.dumps(tweet))+'\n')
                langCount += 1
            print(langCount,'out of',count,'is in',lang,end='\r')
            count += 1
    print 
    f.close()
    lf.close()
        
if __name__ == "__main__":
    main()
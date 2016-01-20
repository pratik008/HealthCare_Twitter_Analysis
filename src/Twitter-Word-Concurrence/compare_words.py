import sys
import json
import os
from concurrence_util import *

def main():
    if len(sys.argv) != 4:
        print "$ score_keywords [afinnFile] [tweetTextFile] [outputDirectory]"
        quit()
    exportConcurrence(processTweets(),dumpAfinn(sys.argv[1]))
    
def processTweets():
    tweetsPath = open(sys.argv[2])
    wordPairs = {}
    for line in tweetsPath:
        text = splitTweet(line)
        wordInThisLine = {}
        for word in splitTweet(line):
            word = trimWord(word)
            if word is False: continue
            makePairs(wordPairs,wordInThisLine,word)
    return wordPairs
    
def makePairs(pairs, words, newWord):
    for word in words:
        if word != newWord:
            if word < newWord:
                pairKey = word+'-'+newWord
                if pairs.get(pairKey,False): pairs[pairKey][1] += 1
                else: pairs[pairKey] = [1,1]
            else:
                pairKey = newWord+'-'+word
                if pairs.get(pairKey,False): pairs[pairKey][0] += 1
                else: pairs[pairKey] = [1,1]
    words[newWord] = True
    
def exportConcurrence(concurrence,afinn):
    outPath = open(os.path.join(sys.argv[3],'concurrence.csv'),'w+')
    outPath.write('word1,word2,concurrence_count,word1_occurance,word2_occurance,sentiment_weighted_sum\n')
    
    for pair in concurrence:
        words = pair.split('-')
        word1 = words[0]
        word2 = words[1]
        word1_count = concurrence[pair][0]
        word2_count = concurrence[pair][1]
        concurrence_count = word1_count + word2_count
        weighted_sentiment = (afinn.get(word1,0)*word1_count + afinn.get(word2,0)*word2_count)
        outPath.write(word1+','+word2+','+str(concurrence_count)+','+str(word1_count)+','+str(word2_count)+','+str(weighted_sentiment)+'\n')
    outPath.close()
    
if __name__ == '__main__':
    main()
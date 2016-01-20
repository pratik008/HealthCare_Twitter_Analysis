#!/usr/bin/python
import os
import sys
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print '$ get_concurrence [afinnFile] [jsonTweetsFile] [destinationDirectory]'
        quit()
    afinnPath = sys.argv[1]
    srcPath = sys.argv[2]
    dataDir = os.path.dirname(sys.argv[2])
    srcfname = os.path.splitext(os.path.basename(srcPath))[0]
    destDir = os.path.join(sys.argv[3],srcfname)
    
    if not os.path.exists(destDir):
        os.makedirs(destDir)
        
    # Get dumped tweets without meta-data
    filterScriptDir = os.path.join('../Twitter-Filter/dump_tweet_text.py')
    os.system('python '+filterScriptDir+' '+srcPath)
    
    # Get the following in a file: keyword, occurance_count, sentiment_total
    dumpPath = os.path.join(dataDir,'tweet_text','all_tweets.txt')
    os.system('python score_keywords.py '+afinnPath+' '+dumpPath+' '+destDir)
    
    print '--------------------------------------------------------------------------------'
    print 'Concurrence files generated: score.csv'
    print
    print '--------------------------------------------------------------------------------'
    
    # Get the following in a file: word1,word2,concurrence_count,word1_occurance,word2_occurance,sentiment_weighted_sum
    os.system('python compare_words.py '+afinnPath+' '+dumpPath+' '+destDir)
    
    print '--------------------------------------------------------------------------------'
    print 'Concurrence files generated: conccurance.csv'
    print
    print '--------------------------------------------------------------------------------'

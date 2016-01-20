#!/usr/bin/python
import os
import sys
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print '$ gen_topics [jsonTweetsFile]'
        quit()
    fname = sys.argv[1]
<<<<<<< HEAD
    dumpScript = os.path.join(os.path.dirname(sys.argv[0]),'dump_tweet_text.py')
    dir = os.path.join(os.path.dirname(fname),'')
    os.system('python '+dumpScript+' '+fname)
=======
    dir = os.path.join(os.path.dirname(fname),'')
    os.system('python dump_tweet_text.py '+fname)
>>>>>>> e1f1750c014f9de2e78fe17fa9314602ce6d05f0
    os.system('mallet import-dir --input '+dir+'tweet_text --output '+dir+'tweet.mallet --keep-sequence --remove-stopwords')
    os.system('mallet train-topics --input '+dir+'tweet.mallet --num-topics 50 --num-iterations 1000 --optimize-interval 0 --output-doc-topics '+dir+'doc_topics.txt --output-topic-keys '+dir+'topic_keys.txt --num-threads 4')
    print '--------------------------------------------------------------------------------'
    print 'Complete: Please open '+dir+'topic_keys.txt and add a zeroth column indicating whether or not the topic is: 0 = spam, 1 = not spam. Then, "run gen_training_data"'
    print
    print '--------------------------------------------------------------------------------'

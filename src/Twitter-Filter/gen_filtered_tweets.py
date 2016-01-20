#!/usr/bin/python
import os
import sys
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print '$ gen_filtered_tweets [unfilteredTweetsFile] [trainingFolder] [destinationFolder]'
        quit()
    filepath = sys.argv[1]
    trainDir = sys.argv[2]
    destDir = sys.argv[3]
    dir = os.path.join(os.path.dirname(filepath),'')
    scriptsDir = os.path.join(os.path.dirname(sys.argv[0]),'')
    os.system('python {0}dump_tweet_text.py '.format(scriptsDir)+filepath)
    os.system('mallet import-dir --input '+dir+'tweet_text --output '+dir+'tweet.mallet --keep-sequence --remove-stopwords')
    os.system('mallet train-topics --input '+dir+'tweet.mallet --num-topics 50 --num-iterations 1000 --optimize-interval 0 --output-doc-topics '+dir+'doc_topics.txt --output-topic-keys '+dir+'topic_keys.txt --num-threads 4')
    os.system('python {0}gen_features.py '.format(scriptsDir)+filepath)
    os.system('python {0}gen_matrix.py '.format(scriptsDir)+dir)
    print 'Unfiltered matrix generated.'
    os.system('python {0}calc_target_matrix.py '.format(scriptsDir)+dir+' '+trainDir)
    os.system('python {0}gen_labels_from_matrix.py '.format(scriptsDir)+filepath)
    os.system('python {0}folder_to_tweets.py '.format(scriptsDir)+filepath+' '+destDir)
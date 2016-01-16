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
    os.system('python dump_tweet_text.py '+filepath)
    os.system('mallet import-dir --input '+dir+'tweet_text --output '+dir+'tweet.mallet --keep-sequence --remove-stopwords')
    os.system('mallet train-topics --input '+dir+'tweet.mallet --num-topics 50 --num-iterations 1000 --optimize-interval 0 --output-doc-topics '+dir+'doc_topics.csv --output-topic-keys '+dir+'topic_keys.csv --num-threads 4')
    os.system('python gen_features.py '+filepath)
    os.system('python gen_matrix.py '+dir)
    print 'Unfiltered matrix generated.'
    os.system('python calc_target_matrix.py '+dir+' '+trainDir)
    os.system('python gen_labels_from_matrix.py '+filepath)
    os.system('python folder_to_tweets.py '+filepath+' '+destDir)
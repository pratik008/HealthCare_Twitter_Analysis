#!/usr/bin/python
import numpy as np
import json
import pickle 
import os
import sys

dir = sys.argv[1]
if not os.path.exists(dir+'topic_keys_labeled.txt'):
    print 'Cannot find '+dir+'topic_keys_labeled.txt'
    quit()
labels = np.loadtxt(dir+'topic_keys_labeled.txt', usecols=[0,1], dtype='int')
labels = dict((labels[i,1], labels[i,0]) for  i in range(labels.shape[0]))

print 'Reading inputs...'
# Output
outfile_targ = open(dir+'ids_and_labels.txt','w')

docs = open(dir+'doc_topics.txt')

docs.readline()
docs.readline()
lines = docs.readlines()
print 'Iterating...'
for i in range(len(lines)):
    line = lines[i]
    fractions = json.loads('['+','.join(line.split('.txt')[1].split())+']')
    # Only use as training example if label is unambiguous
    id = line.split('.txt')[0].split('/tweet_')[-1]
    topic = max( (v, i) for i, v in enumerate(fractions) )[1]
    outfile_targ.write('{0},{1}\n'.format(id,labels[topic]) )

print 'Saving output...'
outfile_targ.close()

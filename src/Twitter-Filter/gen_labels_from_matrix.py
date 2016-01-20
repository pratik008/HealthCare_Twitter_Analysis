#!/usr/bin/python
import sys
import os
import numpy

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print '$ gen_tweets_from_matrix [tweetJsonFile]'
        quit()
    dir = os.path.join(os.path.dirname(sys.argv[1]),'')
    fname = os.path.basename(sys.argv[1])
    YFile = os.path.join(dir,'Y')
    ids = numpy.loadtxt(dir+'ids_and_features.txt', usecols=[0], dtype='str', unpack=True, delimiter=',')
    labels = numpy.loadtxt(YFile, usecols=[0], dtype='int', unpack=True)
    print 'Labeling spam for incoming tweets...'
    outFile = open(os.path.join(dir,'ids_and_labels.txt'), 'w+')
    for i in range(len(ids)):
        outFile.write(str(ids[i])+','+str(labels[i])+'\n')
    outFile.close()
    print 'finished'
    
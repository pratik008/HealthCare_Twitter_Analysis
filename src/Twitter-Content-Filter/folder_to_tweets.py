#!/usr/bin/python

import numpy
import sys
import os

srcPath = sys.argv[1]
srcDir = os.path.dirname(srcPath)
fname = os.path.basename(srcPath)
destDir = os.path.join(sys.argv[2],os.path.splitext(fname)[0])
destPath = os.path.join(destDir,fname)
labelFile = os.path.join(srcDir,'ids_and_labels.txt')

if __name__ == '__main__':
    if not os.path.exists(destDir):
        os.makedirs(destDir)
    labels = numpy.loadtxt(labelFile, usecols=[1], dtype='int', unpack=True, delimiter=',')
    outFile = open(destPath, 'w+')
    print 'filtering spam...'
    with open(srcPath, 'r') as f:
        i = 0
        for tweet in f:
            if labels[i] == 1:
                outFile.write(tweet)
            i += 1
    f.close()
    outFile.close()
    print 'Results is recorded in '+destPath

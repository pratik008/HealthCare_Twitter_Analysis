#!/usr/bin/python
import sys
import os
import numpy as np
import math
from sklearn.ensemble import GradientBoostingClassifier

unfilteredDir = os.path.join(sys.argv[1])
trainingDir = os.path.join(sys.argv[2])
XTrainingFile = os.path.join(trainingDir,'X')
YTrainingFile = os.path.join(trainingDir,'Y')
XUnfilteredFile = os.path.join(unfilteredDir,'X')
YUnfilteredFile = os.path.join(unfilteredDir,'Y')

if __name__ == '__main__':
    if not (os.path.isfile(XTrainingFile) and os.path.isfile(YTrainingFile)):
        print 'Error: Training files not found. Please see README for instructions.'
        quit()
    est = GradientBoostingClassifier(learning_rate=0.3, n_estimators=200, max_depth=3)
    print 'loading files from training set...'
    X = np.asarray(np.loadtxt(XTrainingFile, delimiter=','))
    Y = np.asarray(np.loadtxt(YTrainingFile, delimiter=','))
    print 'finished.'
    print 'loading files from incoming set...'
    incX = np.loadtxt(XUnfilteredFile, delimiter=',')
    print 'finished.'
    print 'fitting model...'
    est.fit(X,Y)
    print 'calculating prediction...'
    newY = est.predict(incX)
    print 'writing to Y file...'
    YFile = open(YUnfilteredFile, 'w')
    newY.astype(int).tofile(YFile,'\n')
    YFile.close()
    print 'finished.'
    
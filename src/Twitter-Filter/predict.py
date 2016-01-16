#!/usr/bin/python

import os
import sys
import datetime
import time
import csv
import math

import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
import ml

def predict(X,Y,estimator):
    estimator.fit(X,Y)
    outfile = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.csv'
    print X,Y,estimator
    
if __name__=='__main__':
    if len(sys.argv) < 3:
        print '> predict [doc] [Xfile] [Yfile]'
        quit()
    dir = '../predicted_set'
    if not os.path.exists(dir):
        os.makedirs(dir)
    predict(sys.argv[1],sys.argv[2],GradientBoostingClassifier)
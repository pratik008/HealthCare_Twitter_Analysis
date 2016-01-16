#!/usr/bin/python
# Train classifier using parameters from

import os
import sys
import datetime
import time
import csv
import math
import matplotlib.pyplot as plt
import numpy as np
import pickle
from sklearn.ensemble import GradientBoostingClassifier

import ml


def transform(opt):
    for dic in opt:
        for key in dic:
            dic[key] = parse(dic[key])
    return opt


def parse(item):
    try: 
        item = float(item)
    except ValueError:
        if item == 'FALSE': return False
        if item == 'None': return None
        return item

    if item == math.floor(item): return int(item)
    return item

    
def load_csv(filename):
    opts = csv.DictReader(open(filename))
    opt_list = [opt for opt in opts]
    return opt_list


def write_csv(dlist, filename='output.csv'):
    csvfile = open(filename,'w')
    fieldnames = dlist[0].keys()
    row1 = dict(zip(fieldnames, fieldnames))
    out = csv.DictWriter(csvfile,fieldnames)
    out.writerow(row1)
    for dic in dlist:
        out.writerow(dic)
    csvfile.close()


def benchmark(X, Y, estimator, opts=None, decision=0.5):
    for i, opt in enumerate(opts):
        print i+1, ' of ', len(opts)
        t0 = time.time()

        # n_folds and decision are specific to NFold only, 
        # so pop them out separately.
        kwargs = {}
        if 'n_folds' in opt:
            kwargs.update({'n_folds':opt.pop('n_folds')})
        if 'decision' in opt:
            kwargs.update({'decision':opt.pop('decision')})

        out  = ml.NFold(X, Y, estimator = estimator(**opts[i]), **kwargs)
        dt = time.time() - t0
        opts[i].update({'dt':dt})
        opts[i].update(out['mean_CV_scores'])
        opts[i].update(out['mean_train_scores'])
        opts[i].update(kwargs)

    #  Save results    
    filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.csv'
    write_csv(opts, filename=filename)

if __name__=='__main__':
    os.system('cls')
    if len(sys.argv) == 1:
        print '> bench [paramfile] [Xfile] [Yfile]'
        quit()

    # APPL stock
    print 'Loading data...',
    X = np.loadtxt(sys.argv[2], delimiter=',')
    Y = np.loadtxt(sys.argv[3], delimiter=',')
    print 'finished.'

    os.system('cls')
    opts = transform(load_csv(sys.argv[1]))
    estimator = GradientBoostingClassifier
    benchmark(X, Y, estimator, opts)
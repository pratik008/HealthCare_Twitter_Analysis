#!/usr/bin/python

import csv
import numpy
import time
import sys
import os

dir = sys.argv[1]
fname = dir+'ids_and_labels.txt'
Xfile = open(dir+'X', 'w')
if os.path.isfile(fname):
    Yfile = open(dir+'Y', 'w')
features_reader = csv.reader(open(dir+'ids_and_features.txt'))

if os.path.isfile(fname):
    labels_ids = numpy.loadtxt(dir+'ids_and_labels.txt', usecols=[0], dtype='str', unpack=True, delimiter=',')
    labels = numpy.loadtxt(dir+'ids_and_labels.txt', usecols=[1], dtype='str', unpack=True, delimiter=',')

print 'Scanning feature vectors...'
count=0
for l in features_reader:
    if os.path.isfile(fname):
        i = (numpy.argwhere(l[0] == labels_ids))
        if len(i)<1:
            print 'Skipping missing label'
            continue

    Xfile.write(','.join(l[1:])+'\n')
    if os.path.isfile(fname):
        Yfile.write(labels[i[0][0]]+'\n')

Xfile.close()
if os.path.isfile(fname):
    Yfile.close()

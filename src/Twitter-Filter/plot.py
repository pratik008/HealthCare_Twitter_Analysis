#!/usr/bin/python

import os
import sys
import matplotlib.pyplot as plt
import numpy as np

def plot(csvfile, xcol, ycols):

    cols = np.loadtxt(csvfile, dtype='str', delimiter=',')[0]
    coli_x = np.argwhere(xcol == cols)[0]
    colis_y = [np.argwhere(ycol == cols)[0][0] for ycol in ycols]
   
    x_data = np.loadtxt(csvfile, delimiter=',', skiprows=1, usecols=coli_x)
    y_data = np.loadtxt(csvfile, delimiter=',', skiprows=1, usecols=colis_y,ndmin=2)

    for i, ycol in enumerate(ycols):
        plt.plot(x_data, y_data[:,i],'-o',label=ycol, ms=5, lw=1.5)
        plt.xlabel(xcol)
    plt.legend(loc=0, numpoints=1)
    plt.show()
    

if __name__=='__main__':

    os.system('cls')
    if len(sys.argv) == 1:
        print '> plot filename x y1 [y2, y3, ...]'
        quit()

    csvfile = sys.argv[1]

    if len(sys.argv) == 2:
        cols = np.loadtxt(csvfile, dtype='str', delimiter=',')[0]
        print cols 
        quit()

    if len(sys.argv) == 3:
        print 'Error: Expected as least one y-value'
        quit()

    xcol, ycols = sys.argv[2], sys.argv[3:]
    plot(csvfile, xcol, ycols )
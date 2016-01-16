#!/usr/bin/python
import os
import sys
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print '$ usage: gen_training_data [jsonTweetsFile]'
    fname = sys.argv[1]
    dir = os.path.join(os.path.dirname(fname),'')
    os.system('python gen_labels.py '+dir)
    os.system('python gen_features.py '+fname)
    os.system('python gen_matrix.py '+dir)
    print '--------------------------------------------------------------------------------'
    print 'Complete: X and Y training matrixes generated.'
    print
    print '--------------------------------------------------------------------------------'

#!/usr/bin/python
import os
import sys
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print '$ gen_training_data [jsonTweetsFile]'
        quit()
    fname = sys.argv[1]
    dir = os.path.join(os.path.dirname(fname),'')
    scriptsDir = os.path.join(os.path.dirname(sys.argv[0]),'')
    os.system('python {0}gen_labels.py '.format(scriptsDir)+dir)
    os.system('python {0}gen_features.py '.format(scriptsDir)+fname)
    os.system('python {0}gen_matrix.py '.format(scriptsDir)+dir)
    print '--------------------------------------------------------------------------------'
    print 'Complete: X and Y training matrixes generated.'
    print
    print '--------------------------------------------------------------------------------'

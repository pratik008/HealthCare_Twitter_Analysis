#!/usr/bin/python
import os
import sys
if __name__ == '__main__':
    if len(sys.argv) != 2:
<<<<<<< HEAD
        print '$ gen_training_data [jsonTweetsFile]'
        quit()
    fname = sys.argv[1]
    dir = os.path.join(os.path.dirname(fname),'')
    scriptsDir = os.path.join(os.path.dirname(sys.argv[0]),'')
    os.system('python {0}gen_labels.py '.format(scriptsDir)+dir)
    os.system('python {0}gen_features.py '.format(scriptsDir)+fname)
    os.system('python {0}gen_matrix.py '.format(scriptsDir)+dir)
=======
        print '$ usage: gen_training_data [jsonTweetsFile]'
    fname = sys.argv[1]
    dir = os.path.join(os.path.dirname(fname),'')
    os.system('python gen_labels.py '+dir)
    os.system('python gen_features.py '+fname)
    os.system('python gen_matrix.py '+dir)
>>>>>>> e1f1750c014f9de2e78fe17fa9314602ce6d05f0
    print '--------------------------------------------------------------------------------'
    print 'Complete: X and Y training matrixes generated.'
    print
    print '--------------------------------------------------------------------------------'

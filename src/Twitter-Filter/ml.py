import os
import numpy as np
import matplotlib.pyplot as plt
import math

# ML models
import sklearn.linear_model
from sklearn.ensemble import GradientBoostingClassifier


def mean_keys(dict_list):
    return dict([(key,np.mean([dic[key] for dic in dict_list])) for key in dict_list[0]])


def score(x, y, val='precision', tag=''):
    if len(x)!=len(y):
        print 'Arrays need to be the same size.'
        return
    if tag: tag = '-'+tag

    x = np.array(x)
    y = np.array(y)
    TP = 1.0 * np.sum( (x == 1)  & (y == 1) )
    TN = 1.0 * np.sum( (x == 0)  & (y == 0) )
    FP = 1.0 * np.sum( (x == 1)  & (y == 0) )
    FN = 1.0 * np.sum( (x == 0)  & (y == 1) )
    acc = 1.0 * np.sum( x == y ) / len(x)
    precision = TP / (TP + FP) if TP > 0 else 0.
    recall = TP / (TP + FN) if TP > 0 else 0.

    if precision == 0. or recall == 0: 
        F1 = 0.
    else:
        F1 = 2. * precision * recall / (precision + recall)
    out = dict([('Acc'+tag,acc),('F1'+tag,F1),('precision'+tag,precision),('recall'+tag,recall),
                 ('TP'+tag,TP),('TN'+tag,TN),('FP'+tag,FP),('FN'+tag,FN)])
    return out


def NFold(X, Y, n_folds = 4, val='precision', decision=0.5, estimator=None):

    m = len(Y)
    factor, remainder = divmod(m, n_folds)
    index = np.arange(m)
    CV_scores = [None for i in range(n_folds)]
    train_scores = [None for i in range(n_folds)]
    for i in range(n_folds):
        # CV
        w1 = i * factor 
        w2 = (i+1) * factor if i != n_folds - 1 else (i+1) * factor + remainder
        w_CV = (w1 <= index) &  (index <  w2)
        X_CV = X[w_CV]
        Y_CV = Y[w_CV]

        # Training Data
        w_train = np.logical_not(w_CV)
        X_train = X[w_train]
        Y_train = Y[w_train]
        
        print X_train
        quit()

        estimator.fit(X_train, Y_train)
        cv_predictions = estimator.predict_proba(X_CV)[:,1] >= decision
        train_predictions = estimator.predict_proba(X_train)[:,1] >= decision

        CV_scores[i] = score(cv_predictions, Y_CV, val=val, tag='cv')
        train_scores[i] = score(train_predictions, Y_train, val=val, tag='train')

    print mean_keys(CV_scores)
    print mean_keys(train_scores)
    out = {'mean_CV_scores':mean_keys(CV_scores),
          'mean_train_scores':mean_keys(train_scores)}
    return out

if __name__=='__main__':
    pass
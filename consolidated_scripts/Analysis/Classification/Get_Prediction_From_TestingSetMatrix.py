##########################################################
#
# Author: ?
# Modified by: Longbo Qiao
# email: longboqiao@gmail.com
# date: June 2013
#
##########################################################
from sklearn.ensemble import RandomForestClassifier
from numpy import genfromtxt, savetxt

def main():
    #create the training & test sets, skipping the header row with [1:]
    dataset = genfromtxt(open('processed/training_matrix.txt','r'), delimiter=',', dtype='f8')[1:]
    target = [x[0] for x in dataset]
    train = [x[1:] for x in dataset]
    test = genfromtxt(open('processed/testing_matrix.txt','r'), delimiter=',', dtype='f8')[1:]

    #create and train the random forest

    rf = RandomForestClassifier(n_estimators=100)
    rf.fit(train, target)
    predicted_probs = [x[1] for x in rf.predict_proba(test)]

    savetxt('processed/result.csv', predicted_probs, delimiter=',', fmt='%f')

if __name__=="__main__":
    main()
##########################################################
#
# Author: Juan Ignacio Gil
# email: juan.ignacio.gil.gomez@gmail.com
# date: July 2014
#
##########################################################

import sys
import csv
from nltk.util import ngrams

#############################################################################

def main():
    
    onegrams=[]
    twograms=[]
    threegrams=[]
    fourgrams=[]

    with open(sys.argv[1],'r') as disease_file:
        tweets = csv.reader(disease_file)
    
        for row in tweets:
            if not tweets.line_num == 1:
                text=row[3]
                onegrams.append(ngrams(text.split(), 1))
                twograms.append(ngrams(text.split(), 2))
                threegrams.append(ngrams(text.split(), 3))
                fourgrams.append(ngrams(text.split(), 4))

    disease_file.close()
    print fourgrams


###################################################################################

if __name__ == '__main__':
    main()
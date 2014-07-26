##########################################################
#
# Author: Juan Ignacio Gil
# email: juan.ignacio.gil.gomez@gmail.com
# date: July 2014
#
##########################################################

"""
   generate_ngrams.py
   
   Creates a csv file with all the n-grams
   
   Execute as:
   python generate_ngrams.py ./HealthCare_Twitter_Analysis/Twitter\ Data/Jan\ to\ May 4  salida.csv
"""

import sys
import csv
import os
from nltk.util import ngrams
import pymongo

############################################################################

def analize_file(tweets,n,group,disease,csvfile):

    print disease

    frequencies=[[] for rank in range(n)]
    grams=[[] for rank in range(n)]
    writer = csv.writer(csvfile, delimiter=',')
        
    for row in tweets:
        if not tweets.line_num == 1:
            text=row[3]
            for rank in range(1,n+1):
                #Generate n-grams
                grams[rank-1]+=ngrams(text.split(), rank)

    for rank in range(n):
        #Compute frecuencies
        frequencies=freq_dist(grams[rank])

        #Write to the csv file
        #"Group,Disease,n,n-gram,frequency"
        
        for (ngram,value) in zip(frequencies.keys(),frequencies.values()):
            writer.writerow([group,disease,rank+1,ngram,value])

#####################################################################################

def process_disease_file(path,group,file,n,csvfile):

    wholepath=path+'/'+group+'/'+file
    with open(wholepath,'r') as disease_file:
        tweets = csv.reader(disease_file)
        disease=file[7:-4]
        
        analize_file(tweets,n,group,disease,csvfile)
    
    disease_file.close()



###################################################################################

if __name__ == '__main__':
    
    
    path=sys.argv[1]
    n=int(sys.argv[2])
    csvfile=open(sys.argv[3], 'wb')
    
    #Navigate directory structure
    for group in os.listdir(path):
        try:
            for file in os.listdir(path+'/'+group):
                process_disease_file(path,group,file,n,csvfile)
        except:
                continue

    csvfile.close()

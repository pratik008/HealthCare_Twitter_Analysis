##########################################################
#
# Author: Juan Ignacio Gil
# email: juan.ignacio.gil.gomez@gmail.com
# date: July 2014
#
##########################################################

"""
   send_tweets_to_mongodb.py
   
   Send tweets from csv files to mongodb
   
   Execute as:
   python generate_ngrams.py ./HealthCare_Twitter_Analysis/Twitter\ Data/Jan\ to\ May 4
"""

import sys
import csv
import os
import pymongo

############################################################################

def send_tweets(tweets,group,disease):
    
    """
        Send the tweets from a csv file to mongodb
    """

    

#####################################################################################

def process_disease_file(path,group,file,n,csvfile):

    wholepath=path+'/'+group+'/'+file
    with open(wholepath,'r') as disease_file:
        tweets = csv.reader(disease_file)
        disease=file[7:-4]
        
        send_tweets(tweets,group,disease)
    
    disease_file.close()



###################################################################################

if __name__ == '__main__':
    
    
    path=sys.argv[1]

    
    #Navigate directory structure
    for group in os.listdir(path):
        try:
            for file in os.listdir(path+'/'+group):
                process_disease_file(path,group,file)
        except:
                continue

    csvfile.close()

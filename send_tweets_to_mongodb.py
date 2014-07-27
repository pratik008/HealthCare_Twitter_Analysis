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
from pymongo import MongoClient
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial

#############################################################################


def process_disease_file(path,group,collection,file):
    
    ni=0
    nu=0
    wholepath=path+'/'+group+'/'+file
    with open(wholepath,'r') as disease_file:
        #Read the tweet file as a dictionary
        tweets=csv.DictReader(disease_file)
        disease=file[7:-4]
    
        #Adding the group and disease fields to all tweets
        for thistweet in tweets:
            thistweet['group']=[group]
            thistweet['disease']=[disease]
            
            #Is this tweet in the database?
            tweetindb=collection.find_one({"url": thistweet['url']})
            if tweetindb==None:

                #Insert tweet in the database
                ni+=1
                thistweet_id = collection.insert(thistweet)

            else:
                #Maybe the tweet was in the database for other disease file
                nu+=1
                tweetindb['group']=list(set(tweetindb['group']+group))
                tweetindb['disease']=list(set(tweetindb['disease']+disease))
                mycollection.update({'_id':tweetindb['_id']}, {"$set": tweetindb}, upsert=False)


    
    disease_file.close()
    print repr(disease)+': '+repr(ni)+' inserted, '+repr(nu)+' updated'



###################################################################################

if __name__ == '__main__':
    
    
    path=sys.argv[1]
    pool = ThreadPool(6)#You should modify this function depending on the number of cores in your computer
    
    #Database
    client = MongoClient()
    db = client['HealthCare_Twitter_Analysis']
    #collection = db.tweets
    
    #Use test database for debugging
    #db = client['test']
    
    


    #Navigate directory structure
    for g in os.listdir(path):
        try:
            files=os.listdir(path+'/'+g)
            partial_process_disease_file=partial(process_disease_file,path,g,db.tweets)
            pool.map(partial_process_disease_file,files)
            pool.close

        except:
                continue


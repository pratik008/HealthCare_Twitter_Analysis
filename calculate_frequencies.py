##########################################################
#
# Author: Juan Ignacio Gil
# email: juan.ignacio.gil.gomez@gmail.com
# date: August 2014
#
##########################################################

"""
    calculate_frequencies.py
    
    Explore the database and calculate (and include in the database) the frecuencies for all
    ngrams for the whole corpus, the different groups, and each disease
"""


from pymongo import MongoClient

#Database
def calculate_frequency(ngram,level,field):
    
    """
        Finds the frequency of the ngram with level(all,group,disease)=field
    """

    client = MongoClient()
    db = client['HealthCare_Twitter_Analysis']
    col = db.tweets
    n=len(ngram)

    #Defining the pipeline
    pipeline=[\
             {'$unwind' : '$n-grams' },\
             {'$match' : {'n-grams.rank' : n}},\
             {'$match' : {'n-grams.text' : ngram}},\
             {'$group' : \
             { '_id' : '$n-grams.text',\
             'frequency' : { '$sum' : 1 }}\
             }
             ]
    

    if level is not 'all':
        pipeline=[{'$match' : {level:field}}]+pipeline

    f=col.aggregate(pipeline, allowDiskUse=True)

    if f['result']==[]:
        return 0
    else:
        return f['result'][0]['frequency']
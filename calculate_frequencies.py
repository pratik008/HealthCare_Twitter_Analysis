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

###########################################################################################

#Calculate frequencies
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


#################################################################################################

#Count total number of n-grams
def count_total_number_ngrams(n,level):
    
    """
        Count the total number of ngrams for level(group,disease)
    """
    
    client = MongoClient()
    db = client['HealthCare_Twitter_Analysis']
    col = db.tweets
    
    #Defining the pipeline
    pipeline=[\
              {'$unwind' : '$n-grams' },\
              {'$match' : {'n-grams.rank' : n}},\
              {'$group' : \
              { '_id' : '$'+level,\
              'frequency' : { '$sum' : 1 }\
              }},\
              {'$sort' : {'frequency' : -1}}
              ]
        
    f=col.aggregate(pipeline, allowDiskUse=True)
    return f

#################################################################################################

#Count all n-grams of rank n
def count_all_ngrams_rank_n():
    
    """
        Count the total number of ngrams for each rank
    """
    
    client = MongoClient()
    db = client['HealthCare_Twitter_Analysis']
    col = db.tweets
    
    #Defining the pipeline
    pipeline=[\
              {'$unwind' : '$n-grams' },\
              {'$group' : \
              { '_id' : '$n-grams.rank',\
              'frequency' : { '$sum' : 1 }\
              }},\
              {'$sort' : {'frequency' : -1}}
              ]
              
    f=col.aggregate(pipeline, allowDiskUse=True)
    return f


######################################################################################

#Insert in the database the total number of n-grams for each group and disease

def insert_total_number_ngrams():
    client = MongoClient()
    db = client['HealthCare_Twitter_Analysis']
    ctw = db.tweets
    ctot= db.totals
    
    #Count and insert all n-grams:
    groups=count_all_ngrams_rank_n()
    groups_to_insert=[{'total':True,'n':g['_id'],'frequency':g['frequency']} for g in groups['result']]
    ctot.insert(groups_to_insert)
    print 'Inserted total n-grams'

    #Get the groups
    for n in range(1,5):
        groups=count_total_number_ngrams(n,'group')
        groups_to_insert=[{'total':False,'group':g['_id'],'n':n,'frequency':g['frequency']} \
                          for g in groups['result']]
        ctot.insert(groups_to_insert)
        print 'Inserted '+repr(n)+'-grams for groups'

        diseases=count_total_number_ngrams(n,'disease')
        groups_to_insert=[{'total':False,'disease':g['_id'],'n':n,'frequency':g['frequency']} \
                          for g in groups['result']]
        ctot.insert(groups_to_insert)
        print 'Inserted '+repr(n)+'-grams for diseases'



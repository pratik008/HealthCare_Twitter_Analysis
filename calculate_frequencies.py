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

    if len(f['result'])==0:
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
    
    #Drop the old collection
    ctot.drop()
    
    #Count and insert all n-grams:
    groups=count_all_ngrams_rank_n()
    groups_to_insert=[{'total':True,'n':g['_id'],'frequency':g['frequency']} for g in groups['result']]
    ctot.insert(groups_to_insert)
    print 'Inserted total n-grams'

    #Get the groups
    for n in range(1,5):
        groups=count_total_number_ngrams(n,'group')
        groups_to_insert=[{'total':False,'group':g['_id'][0],'n':n,'frequency':g['frequency']} \
                          for g in groups['result']]
        ctot.insert(groups_to_insert)
        print 'Inserted '+repr(n)+'-grams for groups'

        diseases=count_total_number_ngrams(n,'disease')
        groups_to_insert=[{'total':False,'disease':g['_id'][0],'n':n,'frequency':g['frequency']} \
                          for g in diseases['result']]
        ctot.insert(groups_to_insert)
        print 'Inserted '+repr(n)+'-grams for diseases'

###########################################################################################

#Calculate relative frequencies
def calculate_relative_frequency(ngram,level,field):
    
    """
        Finds the relative frequency of the ngram with level(all,group,disease)=field
    """
    
    client = MongoClient()
    db = client['HealthCare_Twitter_Analysis']
    ctot= db.totals
    n=len(ngram)
    
    #Find the absolute frequency
    absf=calculate_frequency(ngram,level,field)
    
    #If the absolute frequency is not greater than 1, we don't bother calculating relative frequencies
    if absf>1:
        #Find the total number of tweets
        if level is 'all':
            f=ctot.find_one({'total':True,'n':n})
        else:
            f=ctot.find_one({level:field,'n':n})
        
        #Calculate the relative frequency
        if f is not None:
            return float(absf)/float(f['frequency'])
        else:
            return 0
    else:
        return 0

###########################################################################################

#Calculate all relative frequencies
def calculate_all_relative_frequencies(n,level,field):

    """
        Finds the relative frequency of all ngrams with level(all,group,disease)=field
        and insert them into the database
    """

    client = MongoClient()
    db = client['HealthCare_Twitter_Analysis']
    ctw = db.tweets
    ctot= db.totals
    cfreq= db.frequencies

    #List of all n-grams
    #Defining the pipeline
    pipeline=[\
              {'$unwind' : '$n-grams' },\
              {'$match' : {'n-grams.rank' : n}},\
              {'$group' : { '_id' : '$n-grams.text'}}
              ]
              
              
    if level is not 'all':
        pipeline=[{'$match' : {level:field}}]+pipeline
              
    ngramslist=ctw.aggregate(pipeline, allowDiskUse=True)['result']

    rf=[]
    for ng in ngramslist:
        f=calculate_relative_frequency(ng['_id'],level,field)
        
        #Only insert in the database frecuencies for n-grams than appear more than once
        if f>0:
            if level is 'all':
                nf={'text':ng['_id'],'frequency':f,'n':n,'all':True}
                #Find and modify rd
                cfreq.find_and_modify(query={'text':ng['_id'],'n':n,'all':True},
                        update={"$set": {'frequency':f}}, upsert=True, full_response= True)
            else:
                nf={'text':ng['_id'],'frequency':f,'n':n,level:field}
                #Find and modify rd
                cfreq.find_and_modify(query={'text':ng['_id'],'n':n,level:field},
                        update={"$set": {'frequency':f}}, upsert=True, full_response= True)

            print nf
            rf.append(nf)

    return rf


######################################################################################

#Insert in the database all relative frequencies for each group and disease

def insert_all_relative_frequencies():
    
    client = MongoClient()
    db = client['HealthCare_Twitter_Analysis']
    ctw = db.tweets
    cfreq= db.frequencies
    
    #List of groups
    groups=db.tweets.distinct('group')
    diseases=db.tweets.distinct('disease')

    for n in range(1,5):
        #Insert the relative frequencies in the whole corpus
        calculate_all_relative_frequencies(n,'all','')

        #Insert the relative frequencies for each group
        for g in groups:
            calculate_all_relative_frequencies(n,'group',g)

        #Insert the relative frequencies for each disease
        for d in diseases:
            calculate_all_relative_frequencies(n,'disease',d)











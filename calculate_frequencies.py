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

###########################################################################################

#Calculate frequencies
def calculate_all_frequencies(n,level,field):
    
    """
        Finds the frequency of the ngram with level(all,group,disease)=field
        """
    
    client = MongoClient()
    db = client['HealthCare_Twitter_Analysis']
    col = db.tweets
    results=db.myresults
    nguncol=db.ngun
    
    #Create a temporary collection unwinding the n-grams
    nguncol.drop()
    
    #Defining the pipeline
    pipeline=[
              {'$match' : {level : field}},\
              {'$unwind' : '$n-grams' },\
              {'$match' : {'n-grams.rank' : n}},\
              {'$project':{'_id':0,'n-grams.text':1}},\
              {'$group' : \
              { '_id' : {'text':'$n-grams.text'},\
              'frequency' : { '$sum' : 1 }},\
              },\
              {'$sort' : {'frequency' : -1}},\
              {'$out':'ngun'}
              ]

    col.aggregate(pipeline, allowDiskUse=True)
  
    #Calculate total number of n-grams
  
    agtotal=nguncol.aggregate([ {'$group': {'_id': 'null', 'total': {'$sum': '$frequency'}}} ] )
    ntot=float(agtotal['result'][0]['total'])
  
    f=[]
    for ngram in nguncol.find():
        ngram[level]=field
        ngram['n']=n
        ngram['relative frequency']=float(ngram['frequency'])/ntot
        f.append(ngram)

    nguncol.drop()
    return f

###########################################################################################

#Calculate frequencies
def calculate_frequencies_whole_corpus(n):
    
    """
        Finds the frequency of the ngram with level(all,group,disease)=field
    """
    
    client = MongoClient()
    db = client['HealthCare_Twitter_Analysis']
    col = db.tweets
    results=db.myresults
    nguncol=db.ngun
    
    #Create a temporary collection unwinding the n-grams
    nguncol.drop()
    
    #Defining the pipeline
    pipeline=[
              {'$unwind' : '$n-grams' },\
              {'$match' : {'n-grams.rank' : n}},\
              {'$project':{'_id':0,'n-grams.text':1}},\
              {'$group' : \
              { '_id' : {'text':'$n-grams.text'},\
              'frequency' : { '$sum' : 1 }},\
              },\
              {'$sort' : {'frequency' : -1}},\
              {'$out':'ngun'}
              ]
              
    col.aggregate(pipeline, allowDiskUse=True)
    
    #Calculate total number of n-grams
    
    agtotal=nguncol.aggregate([ {'$group': {'_id': 'null', 'total': {'$sum': '$frequency'}}} ] )
    ntot=float(agtotal['result'][0]['total'])

    f=[]
    for ngram in nguncol.find():
        ngram['all']=True
        ngram['n']=n
        ngram['relative frequency']=float(ngram['frequency'])/ntot
        f.append(ngram)

    nguncol.drop()
    return f


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

#Insert in the database all relative frequencies for each group and disease

def insert_all_relative_frequencies():
    
    client = MongoClient()
    db = client['HealthCare_Twitter_Analysis']
    ctw = db.tweets
    cfreq= db.frequencies
    cfreq.drop()
    
    #List of groups
    groups=db.tweets.distinct('group')
    diseases=db.tweets.distinct('disease')

    for n in range(1,5):
        #Insert the relative frequencies in the whole corpus
        f=calculate_frequencies_whole_corpus(n)
        cfreq.insert(f)
        print('Completed for the whole corpus, n='+repr(n))

        #Insert the relative frequencies for each group
        for g in groups:
            f=calculate_all_frequencies(n,'group',g)
            cfreq.insert(f)
            print('Completed for the group '+repr(g)+' n='+repr(n))

        #Insert the relative frequencies for each disease
        for d in diseases:
            f=calculate_all_frequencies(n,'disease',d)
            cfreq.insert(f)
            print('Completed for the group '+repr(d)+' n='+repr(n))











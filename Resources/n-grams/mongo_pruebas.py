from pymongo import MongoClient

#Database
client = MongoClient()
db = client['HealthCare_Twitter_Analysis']
col = db.tweets

#Get the number of tweets for each group
tweets_by_group=col.aggregate({ '$group' : { '_id' : '$group','number_of_tweets' : { '$sum' : 1 }}})

#Get the frecuency of each n-gram (start with n=1)
pipeline=[\
          {'$match' : {'group':'Blood'}},\
          {'$unwind' : '$n-grams' },\
          {'$match' : {'n-grams.rank' : 1}},\
          {'$group' : \
          { '_id' : '$n-grams.text',\
          'frequency' : { '$sum' : 1 }}\
          },\
          {'$sort' : {'frequency' : -1}}
          ]

frequencies=col.aggregate(pipeline, allowDiskUse=True)

for gram in frequencies['result'][:10]:
    print gram

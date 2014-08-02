from pymongo import MongoClient

#Database
client = MongoClient()
db = client['HealthCare_Twitter_Analysis']
col = db.tweets

col.find()

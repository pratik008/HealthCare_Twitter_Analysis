import send_tweets_to_mongodb as st

path='/Users/cato/programacion/HealthCare_Twitter_Analysis/Twitter Data/Jan to May'
group='Blood'
file='Tweets_BleedingDisorders.csv'

client = MongoClient()
    db = client['HealthCare_Twitter_Analysis']
    
    #Use test database for debugging
    #db = client['test']
    
    collection = db.tweets

st.process_disease_file(path,group,file,collection)
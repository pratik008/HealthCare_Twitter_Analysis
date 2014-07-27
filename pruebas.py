import send_tweets_to_mongodb as st

path1='/Users/cato/programacion/HealthCare_Twitter_Analysis/Twitter Data/Jan to May'
path2='/Users/cato/programacion/HealthCare_Twitter_Analysis/Twitter Data/June'

st.send_tweets_one_core(path1)
st.send_tweets_one_core(path2)
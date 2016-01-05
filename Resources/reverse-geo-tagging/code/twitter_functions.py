def mapquest_single_location(location, key):
    """
    find the MapQuest location json for a single location
    
    Input:    location    Twitter location, check that it's not null before calling
              key         MapQuest developer key
    
    Output:   json returned by MapQuest, or {}
    """
    import json
    import requests
    import random
    mapq_url = 'http://open.mapquestapi.com/geocoding/v1/address?key='
    mapq_url = mapq_url + key + '&location='
    
    loc_url  = mapq_url + location
    response = requests.get(loc_url)
    mapq_ret = response.text
    
    mapq_ret_json = json.loads(mapq_ret)
    if mapq_ret_json['results'][0]['locations']:
        # if they give us more than one, choose at random
        index = random.randint(0,len(mapq_ret_json['results'][0]['locations'])-1)
        return(mapq_ret_json['results'][0]['locations'][index])
    else:
        empty_dict = {}
        return(empty_dict)

def twitterreq(url, method, parameters):
    """
    Send twitter URL request
    
    Utility function used by the others in this package
    
    Note: calls a function twitter_credentials() contained in
          a file named twitter_credentials.py which must be provided as follows:

            api_key = " your credentials "  
            api_secret = " your credentials "  
            access_token_key = " your credentials "  
            access_token_secret = " your credentials "  
            return (api_key,api_secret,access_token_key,access_token_secret)
          
     This function is based on a shell provided by
     Bill Howe
     University of Washington
     for the Coursera course Introduction to Data Science
     Spring/Summer 2014
     (which I HIGHLY recommend)
    """
    import oauth2 as oauth
    import urllib2 as urllib
    import sys, time

    # this is a private function containing my Twitter credentials
    from twitter_credentials import twitter_credentials
    api_key,api_secret,access_token_key,access_token_secret = twitter_credentials()

    _debug = 0

    oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
    oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

    signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

    http_method = "GET"


    http_handler  = urllib.HTTPHandler(debuglevel=_debug)
    https_handler = urllib.HTTPSHandler(debuglevel=_debug)

    '''
    Construct, sign, and open a twitter request
    using the hard-coded credentials above.
    '''
    req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                                 token=oauth_token,
                                                 http_method=http_method,
                                                 http_url=url, 
                                                 parameters=parameters)

    req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

    headers = req.to_header()

    if http_method == "POST":
      encoded_post_data = req.to_postdata()
    else:
      encoded_post_data = None
      url = req.to_url()

    opener = urllib.OpenerDirector()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)

    try:
        response = opener.open(url, encoded_post_data)
    except:
        print "\n ERROR IN TWITTERREQ"
        print sys.exc_info()
        time.sleep(60) # wait 60 seconds
        # try one more time
        response = opener.open(url, encoded_post_data)

    return response

def lookup_tweet(tweet_id):
    """
    Ask Twitter for information about a specific tweet by its id
    
    the Twitter API for this is here:
    https://dev.twitter.com/docs/api/1.1/get/statuses/show/%3Aid
    
#Use: 
#import json
#from twitter_functions import lookup_tweet
#
#result = lookup_tweet("473010591544520705")
#for foo in result:
#    tweetdata = json.loads(foo)
#    break
# there must be a better way
#
#print json.dumps(tweetdata, sort_keys = False, indent = 4)
    """
    
    url = "https://api.twitter.com/1.1/statuses/show.json?id=" + tweet_id
    parameters = []
    response = twitterreq(url, "GET", parameters)
      
    return response
    
def lookup_multiple_tweets(list_of_tweet_ids):
    """
    Ask Twitter for information about 
    a bulk list of tweets by id
    
    the Twitter API for this is here:
    https://dev.twitter.com/docs/api/1.1/get/statuses/lookup
    
    Use: 
import json
from twitter_functions import lookup_multiple_tweets

list_of_tweet_ids = ["473010591544520705","473097867465224192"]
result = lookup_multiple_tweets(list_of_tweet_ids)
for foo in result:
    tweetdata_list = json.loads(foo)
    break
# there must be a better way

for tweetdata in tweetdata_list:
    print json.dumps(tweetdata, sort_keys = False, indent = 4)
    """
    
    csv_of_tweet_ids = ",".join(list_of_tweet_ids)
    url = "https://api.twitter.com/1.1/statuses/lookup.json?id=" + csv_of_tweet_ids
    parameters = []
    response = twitterreq(url, "GET", parameters)
      
    return response
    
def lookup_user(rsarver):
    """
    Ask Twitter for information about a user name
    
    the Twitter API for this is here:
    https://dev.twitter.com/docs/api/1.1/get/users/show
    
Use: 
import json
from twitter_functions import lookup_user

result = lookup_user("flgprohemo")
for foo in result:
    userdata = json.loads(foo)
    break
# there must be a better way

print json.dumps(userdata, sort_keys = False, indent = 4)


# all may be null; have to check
userdata["location"].encode('utf-8')
userdata["description"].encode('utf-8')
userdata["utc_offset"].encode('utf-8')
userdata["time_zone"].encode('utf-8')
userdata["status"]["lang"].encode('utf-8')
    """
    
    url = "https://api.twitter.com/1.1/users/show.json?screen_name=" + rsarver
    parameters = []
    response = twitterreq(url, "GET", parameters)
      
    return response
    
def lookup_multiple_users(csv_of_screen_names):
    """
    Ask Twitter for information about up to 100 screen names
    The input argument must be a string of screen names separated by commas
    
    the Twitter API for this is here:
    https://dev.twitter.com/docs/api/1.1/get/users/lookup
    
    Version 0.1 uses GET; Twitter urges POST; I will get to that later
    
Use: 
import json
from twitter_functions import lookup_multiple_users

screen_name_list    = ["grfiv","flgprohemo"]
csv_of_screen_names = ",".join(screen_name_list)

result = lookup_multiple_users(csv_of_screen_names)
for foo in result:
    userdata = json.loads(foo)
    break
# there must be a better way

for user in userdata:
    print "For screen name: " + user["screen_name"]
    print json.dumps(user, sort_keys = False, indent = 4)

    """
    
    url = "https://api.twitter.com/1.1/users/lookup.json?screen_name=" + csv_of_screen_names
    parameters = []
    response = twitterreq(url, "GET", parameters)
      
    return response
    
        
def find_WordsHashUsers(input_filename, text_field_name="content", list_or_set="list"):
    """
    Input:  input_filename: the csv file
            text_field_name: the name of the column containing the tweet text
            list_or_set: do you want every instance ("list") or unique entries ("set")?
    
    Output: lists or sets of
            words
            hashtags
            users mentioned
            urls
            
    Usage:  word_list, hash_list, user_list, url_list, num_tweets = \
            find_WordsHashUsers("../files/Tweets_BleedingDisorders.csv", "content", "list")
    
            word_set, hash_set, user_set, url_set, num_tweets =  \
            find_WordsHashUsers("../files/Tweets_BleedingDisorders.csv", "content", "set")
    """
    import csv
    
    if list_or_set != "set" and list_or_set != "list":
        print "list_or_set must be 'list' or 'set', not " + list_or_set
        return()
    
    if list_or_set == "list":
        word_list = list()
        hash_list = list()
        user_list = list()
        url_list  = list()
    else:
        word_set = set()
        hash_set = set()
        user_set = set()
        url_set  = set()
    
    with open(input_filename, "rb" ) as infile:
       reader     = csv.DictReader(infile)
       lines      = list(reader) # list of all lines/rows in the input file
       totallines = len(lines)   # number of lines in the input file
       
       # read the input file line-by-line
       # ================================
       for linenum, row in enumerate(lines):
        
           content                    = row[text_field_name]
           words, hashes, users, urls = parse_tweet_text(content)
           
           if list_or_set == "list":
               word_list.extend(words)
               hash_list.extend(hashes)
               user_list.extend(users)
               url_list.extend(urls)
           else:
               word_set.update(words)
               hash_set.update(hashes)
               user_set.update(users)
               url_set.update(urls)
           
    if list_or_set == "list":
        return (word_list, hash_list, user_list, url_list, totallines)
    else:
        return (word_set, hash_set, user_set, url_set, totallines)
        
def parse_tweet_text(tweet_text):
    """
    Input:  tweet_text: a string with the text of a single tweet
                        or a concatenation of tweets
                
    Output: lists of tokens in the text:
              words (many emoticons are recognized as words)
              hashtags
              users mentioned
              urls
              
    Usage: words, hashes, users, urls = parse_tweet_text(tweet_text)
    """
    import re
    
    content = tweet_text
           
    # collect and remove URLs
    urls    = re.findall(r"\b((?:https?|ftp|file)://[-A-Z0-9+&@#/%?=~_|$!:,.;]*[A-Z0-9+&@#/%=~_|$])", content, re.IGNORECASE)
    content = re.sub(r"\b((?:https?|ftp|file)://[-A-Z0-9+&@#/%?=~_|$!:,.;]*[A-Z0-9+&@#/%=~_|$])", "", content, 0, re.IGNORECASE)
    
    content = content.lower()
    
    # collect and remove users mentioned
    users   = re.findall(r"@(\w+)", content)
    content = re.sub(r"@(\w+)", "", content, 0)
   
    # collect and remove hashtags
    hashes  = re.findall(r"#(\w+)", content)
    content = re.sub(r"#(\w+)", "", content, 0)
    
    # strip out extra whitespace in the remaining text
    content = re.sub(r"\s{2,}", " ", content)
    
    # strip out singleton punctuation
    raw_words   = content.split()
    words = []
    for word in raw_words:
        if word in ['.',':','!',',',';',"-","-","?",'\xe2\x80\xa6',"!","|",'"','~','..','/']: continue
        re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
        word       = re_pattern.sub(u'\uFFFD', word) 
        #if word.encode('utf-8') in ['\xe2\x80\xa6']: continue
        
        # remove trailing commas, periods, question marks, colons, exclamation marks
        word = re.sub(r"(.*)[,\.,\?,:,!]$", r"\1", word, 0, re.MULTILINE)
        words.append(word)
        
    return (words, hashes, users, urls)
    
def parse_AFINN(afinnfile_name):
    """
    Parse the AFIN-111 sentiment file
    
    Input:  afinnfile_name: the [path/] file name of AFIN-111.txt
    
    Output: dicts of:
              sentiment_words: score
              sentiment_phrases: score
            
    Usage: from twitter_functions import parse_AFINN
           sentiment_words, sentiment_phrases = parse_AFINN("AFINN-111.txt")
    """
    import re
    afinnfile = open(afinnfile_name)
    
    sentiment_phrases = {}
    sentiment_words   = {}
    for line in afinnfile:
      key, val  = line.split("\t")        
      if " " in key:
        key = re.sub(r"\s{2,}", " ", key) # strip extra whitespace
        sentiment_phrases[key.lower()] = int(val)
      else:
        sentiment_words[key.lower()] = int(val)
    return (sentiment_words, sentiment_phrases)
    
def twitter_search(twitter_api, q, max_results=200, **kw):
    
    # from Chapter 9 - Twitter Cookbook, 
    # Example 4. Searching for tweets 

    # See https://dev.twitter.com/docs/api/1.1/get/search/tweets and 
    # https://dev.twitter.com/docs/using-search for details on advanced 
    # search criteria that may be useful for keyword arguments
    
    # See https://dev.twitter.com/docs/api/1.1/get/search/tweets    
    search_results = twitter_api.search.tweets(q=q, count=100, **kw)
    
    statuses = search_results['statuses']
    
    # Iterate through batches of results by following the cursor until we
    # reach the desired number of results, keeping in mind that OAuth users
    # can "only" make 180 search queries per 15-minute interval. See
    # https://dev.twitter.com/docs/rate-limiting/1.1/limits
    # for details. A reasonable number of results is ~1000, although
    # that number of results may not exist for all queries.
    
    # Enforce a reasonable limit
    max_results = min(1000, max_results)
    
    for _ in range(10): # 10*100 = 1000
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError, e: # No more results when next_results doesn't exist
            break
            
        # Create a dictionary from next_results, which has the following form:
        # ?max_id=313519052523986943&q=NCAA&include_entities=1
        kwargs = dict([ kv.split('=') 
                        for kv in next_results[1:].split("&") ])
        
        search_results = twitter_api.search.tweets(**kwargs)
        statuses += search_results['statuses']
        
        if len(statuses) > max_results: 
            break
            
    return statuses
    
def lexical_diversity(set_, list_):
    """
    A function for computing lexical diversity
    """
    if len(list_) < 1: return 0
    return 1.0*len(set_)/len(list_) 

def average_words(list_, num_tweets): 
    """
    A function for computing the average number of entity per tweet
    """
    if num_tweets < 1: return 0
    return 1.0*len(list_)/num_tweets
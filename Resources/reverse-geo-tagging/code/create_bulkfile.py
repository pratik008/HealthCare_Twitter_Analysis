def create_bulkfile(list_of_filenames, starting_at=1, ending_at=0):
    """
    - reads in a list of fully-qualified filenames from "list_of_filenames"
    
        I'm expecting file names to have the Windows Google Drive structure, for example
        ... Twitter Data\June\Cardiovasucular\Tweets_AFib.csv   
        
        the code is commented with a simple solution you can implement to allow you to have
        any arbitrary fully-qualified filename, for any operating system
        
    - processes each row of each file in the file list, 
      making batched calls to Twitter to retrieve the data for each tweet
    
    - after every 13,500 rows, or whenever there is a threshold-exceeded error
      the output_file is written and the program goes to sleep for 15 minutes.
      
    Note: AFINN-111.txt must be in the same folder
          you can use it as is or include your own n-grams
          the 'sentiment' field is the sum of the scores of all the n-grams found  
          
    Note: Requires pygeocoder
    
    Input: list_of_filenames   a text file with fully-qualified file names
           starting_at         the line number of "list_of_filenames" where processing should start
           ending_at           if 0   process all files beginning with the "starting_at" line in "list_of_filenames"
                               if > 0 process the files from line "starting_at" to line "ending_at" in "list_of_filenames"
                                    
           
    Output: a csv file named "bigtweet_filexxx.csv", where xxx is the "starting_at" number
        
    Usage: %run create_bulkfile.py "filename_list.csv" 1 0
    
    A message like "263 skipped id 463811853097787392" indicates that Twitter did not return data
    for a tweet with the id of 463811853097787392 and this is the 263rd instance of this. 
    As a result of this and other less-common errors the output file will have fewer rows than 
    the total rows in the input files.
    """
    import csv
    import json
    import re
    import time
    import sys
    import six
    import datetime
    from twitter_functions import lookup_multiple_tweets
    from twitter_functions import parse_AFINN
    
    # convert input parameter strings to integer
    starting_at = int(starting_at) 
    ending_at   = int(ending_at)
    
    process_start = datetime.datetime.now()
    print "\n================================"
    print "process start: %s"%process_start.strftime("%c")
    print "================================\n"
    
    # read the list of filenames into "filename_list"
    # ===============================================
    filename_list = []
    with open(list_of_filenames, "rb") as namefile:
        csv_reader = csv.reader(namefile)
        for row in csv_reader:
            filename_list.extend(row)
    
    output_filename   = "bigtweet_file" + "%03d"%(starting_at,) + ".csv"
    step              = 100 # we're going to process in groups of "step"
    bulk_list         = []  # batch of rows from input file 
    list_of_tweet_ids = []  # tweet ids of these rows
    output_dict       = []  # list of dicts to send to output file
    
    # the Twitter rate limits are documented here
    # https://dev.twitter.com/docs/rate-limiting/1.1/limits
    sleep_batch       = 13500 # we sleep after this many lines processed
    sleep_batch_rows  = 0     # the number of lines we've processes since the last sleep
    
    number_of_files   = len(filename_list) # how many files in the list
    file_counter      = 1                  # which one is this one
    first_sleep       = True               # first time through, we write an output_file header
    invalid_json      = False              # in case Twitter sends us junk
    skip_counter      = 0                  # how many rows did we skip because Twitter didn't send us info
    
    # read in the n-grams for sentiment processing
    sentiment_words, sentiment_phrases = parse_AFINN("AFINN-111.txt")
    
    # read each file in and process it
    # ==================================
    for input_filename in filename_list:
        
        # skip the first "starting_at-1" files
        if file_counter < starting_at:
            print "Skipping %d of %d %s"%(file_counter, number_of_files, input_filename)
            file_counter+=1
            continue  
            
        if ending_at != 0: number_of_files = ending_at
            
        # find the shortened file name
        #
        # note: if your filenames do not fit my convention
        #       replace the two lines below with
        #
        #       short_file_name = input_filename
        #
        match = re.search(r"Twitter Data\\(.*)", input_filename) 
        short_file_name = match.group(1)  

        # stop if we're beyond "ending_at"
        if ending_at > 0:
            if file_counter > ending_at:
                print "Ending before %d of %d %s"%(file_counter, number_of_files, input_filename)
                break
        
        # open an input file
        with open(input_filename, "rb" ) as infile:
            reader     = csv.DictReader(infile)
            lines      = list(reader) # list of all lines/rows in the input file
            totallines = len(lines)   # number of lines in the input file
            
            print "\n--Processing %d of %d %s rows %d"%(file_counter, number_of_files, short_file_name,totallines)
            
            # read the input file line-by-line
            # ================================
            for linenum, row in enumerate(lines):
                
                # sleep if we're over the limit of lines processed
                sleep_batch_rows+=1
                if sleep_batch_rows > sleep_batch:
                    print "sleeping after %d lines of file %d of %d %s"%(linenum, file_counter, number_of_files, short_file_name)
                    sleep_batch_rows = 0
                    sleep_process(output_dict, output_filename, first_sleep)
                    
                # accumulate a batch of rows from the input file
                # ==============================================
                tweet_id  = row['url'].split("/")[-1]
                # make sure tweet_id is actually numeric
                if re.match(r"^\d+", tweet_id):
                    # Successful match at the start of the string
                    row['id'] = tweet_id
                    bulk_list.append(row)
                    list_of_tweet_ids.append(tweet_id)
                else:
                    print "tweet url terminated with non-numeric in line %d"%(linenum+1)
                    print row['url']
                
                # if batch-size reached, process the batch
                if len(bulk_list) >= step or (linenum+1) >= totallines:
                   
                    # make a batch request to Twitter 
                    # ===============================
                    while True:
                        result = lookup_multiple_tweets(list_of_tweet_ids)
                        if result: break
                        print "\nTwitter returned an empty result\n"
                        time.sleep(1)
                        
                    list_of_tweet_ids = []
                    for foo in result:
                        try:
                            tweetdata_list = json.loads(foo)
                            break
                        except ValueError, e:
                            print "\nTwitter returned invalid json"
                            print e
                            print "after %d lines of file %d of %d %s"%(linenum, file_counter, number_of_files, short_file_name)
                            bulk_list = []
                            invalid_json = True
                            break
                            
                    if invalid_json:
                        invalid_json = False
                        break
                        
                    # if Twitter returns an error
                    #
                    # better process
                    # try:
                    #     statuses = api.GetUserTimeline(u.id)
                    #     print [s.text for s in statuses]
                    # except TwitterError, t:
                    #     print t
                    if 'errors' in tweetdata_list:
                        print "Twitter returned an error message:"
                        print "message: " + str(tweetdata_list["errors"][0]['message'])
                        print "code:    " + str(tweetdata_list["errors"][0]['code'])
                        print "after %d lines of file %d of %d %s"%(linenum, file_counter, number_of_files, short_file_name)
                        sleep_batch_rows = 0
                        sleep_process(output_dict, output_filename, first_sleep)
                        bulk_list = [] # we lose the batch
                        continue
                    
                    # Twitter's response is in arbitrary order and doesn't necessarily
                    # contain a response for every id we requested
                    #
                    # So we create a dictionary for the tweetdata_list
                    # associating id's with their position in the list
                    # and a list of id's for searching
                    
                    tweet_id_dict = {}
                    tweet_id_list = []
                    
                    # find every id in tweetdata_list and its position
                    for i in range(len(tweetdata_list)):
                        id = str(tweetdata_list[i]['id'])
                        tweet_id_dict[id] = i
                        tweet_id_list.append(id)
                        
                    # pull each of the lines and its corresponding Twitter response
                    batch_process_count = 0
                    for line in bulk_list:
                        if line['id'] not in tweet_id_list:
                            skip_counter+=1
                            # check the entire line['id'] is numeric
                            if re.match(r"^\d+", line['id']):
                                # yes
                                print "%d skipped id %d"%(skip_counter, int(line['id']))
                            else:
                                # no
                                print skip_counter
                                print "line['id'] is not all numeric"
                                print line['id']                               
                            continue
                            
                        tweetdata = tweetdata_list[tweet_id_dict[line['id']]]
                        if str(line['id']) != str(tweetdata['id']):
                            skip_counter+=1
                            print "id mismatch, skipping %d"%(skip_counter)
                            print "line  id %s"%(str(line['id']))
                            print "tweet id %s"%(str(tweetdata['id']))
                            continue

                        # parse Twitter's response
                        line["file_counter"]    = file_counter
                        line["short_file_name"] = short_file_name
                        line = parse_tweet_json(line, tweetdata)
                        line['sentiment'] = find_sentiment(tweetdata, sentiment_words, sentiment_phrases)
                        
                        output_dict.append(line)
                        batch_process_count+=1
                        
                       
                    print "Rows processed: " + str(len(output_dict)) 
                    bulk_list = []
                    
        file_counter+=1
       
    # process the output file for the final time
    # ==========================================
    process_output_file(output_dict, output_filename, first_sleep)
                    
    # how long did it take?
    process_end     = datetime.datetime.now()
    process_elapsed = process_end - process_start
    process_seconds = process_elapsed.seconds
    process_minutes = process_seconds/60.0
    process_hours   = process_minutes/60.0
    
    print "\n================================"
    print "process start: %s"%process_start.strftime("%c")
    print "process end:   %s"%process_end.strftime("%c")
    print "process elapsed hours %0.2f"%process_hours
    print "================================\n"

def parse_tweet_json(line, tweetdata):
    """
    Take in a line from the file as a dict
    Add to it the relevant fields from the json returned by Twitter
    
    Documentation https://dev.twitter.com/docs
    """
    import time
    import datetime

    line["tweet_coordinates"]  = str(tweetdata["coordinates"])
    # unix timestamp...better for sorting, searching, indexing
    line["tweet_timestamp"] = ""
    try:
        line["tweet_timestamp"] = str(time.mktime(datetime.datetime.strptime(line['firstpost_date'], "%m/%d/%Y").timetuple()))
    except:
        try:
            line["tweet_timestamp"] = str(time.mktime(datetime.datetime.strptime(line['firstpost_date'], "%m/%d/%y").timetuple()))
        except:
            pass
    
    line["tweet_favorited"]    = str(tweetdata["favorited"])
    if tweetdata["entities"] is not None:
         if tweetdata["entities"]["hashtags"] is not None:
             hashtag_string = ""
             for tag in tweetdata["entities"]["hashtags"]:
                 hashtag_string = hashtag_string + tag["text"] + "~"
             hashtag_string = hashtag_string[:-1]
             line["hashtags"] = str(hashtag_string.encode('utf-8'))
         else:
             line["hashtags"] = ""
         if tweetdata["entities"]["user_mentions"] is not None:
             user_mentions_string = ""
             for tag in tweetdata["entities"]["user_mentions"]:
                 user_mentions_string = user_mentions_string + tag["screen_name"] + "~"
             user_mentions_string = user_mentions_string[:-1]
             line["user_mentions"] = str(user_mentions_string)
         else:
             line["user_mentions"] = ""
    line["tweet_retweet_count"]  = str(tweetdata["retweet_count"])
    line["tweet_favorite_count"] = str(tweetdata["favorite_count"])
    line["tweet_retweeted"]      = str(tweetdata["retweeted"])
    line["tweet_place"]          = str(tweetdata["place"])
    line["tweet_geo"]            = str(tweetdata["geo"])
    line["tweet_coordinates"]    = str(tweetdata["coordinates"])
    line["tweet_in_reply_to_screen_name"]    = str(tweetdata["in_reply_to_screen_name"])
    if tweetdata["user"] is not None:
        line["user_friends_count"]    = str(tweetdata["user"]["friends_count"])
        line["user_name"]             = tweetdata["user"]["name"].encode('utf-8')
        line["user_favourites_count"] = str(tweetdata["user"]["favourites_count"])
        line["user_screen_name"]      = tweetdata["user"]["screen_name"].encode('utf-8')
        line["user_listed_count"]     = str(tweetdata["user"]["listed_count"])
        line["user_location"]         = tweetdata["user"]["location"].encode('utf-8')
        line["user_utc_offset"]       = str(tweetdata["user"]["utc_offset"])
        line["user_followers_count"]  = str(tweetdata["user"]["followers_count"])
        line["user_listed_count"]     = str(tweetdata["user"]["listed_count"])
        line["user_lang"]             = tweetdata["user"]["lang"].encode('utf-8')
        line["user_geo_enabled"]      = str(tweetdata["user"]["geo_enabled"])
        line["user_time_zone"]        = str(tweetdata["user"]["time_zone"])
        line["user_statuses_count"]   = str(tweetdata["user"]["statuses_count"])
        line["user_verified"]         = str(tweetdata["user"]["verified"])
        line["user_description"]      = tweetdata["user"]["description"].encode('utf-8')
        
    # geo location data
    from pygeocoder import Geocoder
    try:
        geo_results = Geocoder.geocode(line["user_time_zone"])
    except:
        geo_results = "error"
    line["user_time_zone_coordinates"] = ""
    line["user_time_zone_placename"]   = ""
    if geo_results != "error":
        line["user_time_zone_coordinates"] = geo_results.coordinates
        for foo in geo_results:
            line["user_time_zone_placename"] = foo
            break
    try:
        geo_results = Geocoder.geocode(line["user_location"])
    except:
        geo_results = "error"
    line["user_location_coordinates"] = ""
    line["user_location_placename"]   = ""
    if geo_results != "error":
        line["user_location_coordinates"] = geo_results.coordinates
        for foo in geo_results:
            line["user_location_placename"] = foo
            break
    
    return line
    
def find_sentiment(tweet_data, sentiment_words, sentiment_phrases):
    import re
    
    content = tweet_data['text'].lower()
    
    # remove URLs
    content = re.sub(r"\b((?:https?|ftp|file)://[-A-Z0-9+&@#/%?=~_|$!:,.;]*[A-Z0-9+&@#/%=~_|$])", "", content, 0, re.IGNORECASE)
   
    # remove hashtags
    content = re.sub(r"#(\w+)", "", content, 0)
   
    # remove users mentioned
    content = re.sub(r"@(\w+)", "", content, 0)
    
    # strip out extra whitespace in the remaining text
    content = re.sub(r"\s{2,}", " ", content)
    
    words   = content.split()
    
    AFINN_score = 0
    # single words
    for word in words:
        if word in sentiment_words:
            AFINN_score += sentiment_words[word]
    # phrases
    for phrase in sentiment_phrases:
        if phrase in content:
            AFINN_score += sentiment_phrases[phrase]
    
    return AFINN_score
    
    
def sleep_process(output_dict, output_filename, first_sleep):
    import time
    import sys
    import datetime
    from datetime import timedelta
    
    process_output_file(output_dict, output_filename, first_sleep)
    
    length_of_sleep = int(15.1*60)  # seconds
    timenow    = datetime.datetime.today().strftime("%H:%M:%S")
    timeplus15 = (datetime.datetime.today()+timedelta(seconds=length_of_sleep)).strftime("%H:%M:%S")
    print "sleeping at %s, will resume at %s"%(timenow, timeplus15)
    sys.stdout.flush()
    
    time.sleep(length_of_sleep)
    
def process_output_file(output_dict, output_filename, first_sleep):
    import csv
    import datetime
    if first_sleep:
        first_sleep = False
        f = open(output_filename,'wb')
        w = csv.DictWriter(f, delimiter=",", fieldnames=output_dict[0].keys())
        w.writeheader()
        w.writerows(output_dict)
        f.close()
    else:
        f = open(output_filename,'a')
        w = csv.DictWriter(f, delimiter=",", fieldnames=output_dict[0].keys())
        w.writerows(output_dict)
        f.close()
    output_dict = []
    timenow     = datetime.datetime.today().strftime("%H:%M:%S")
    print "%s processed at %s"%(output_filename, timenow)
    
                    
if __name__ == '__main__':
    import sys
    create_bulkfile(sys.argv[1],sys.argv[2],sys.argv[3])
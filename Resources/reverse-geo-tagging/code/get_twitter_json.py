def get_twitter_json(list_of_filenames, starting_at=1, ending_at=0, geocode=True):
    """
    1) reads in a list of fully-qualified filenames from "list_of_filenames"
        
    2) processes each row of each topsy file in the "list_of_filenames", 
       making batched calls to Twitter to retrieve the json for each tweet
           adding the data from the topsy file such as "score"
           plus unix timestamps for the topsy firstpost_date field and Twitter's created_at field
           plus coordinate and place name data for Twitter's user location field
    
    - after every 13,500 rows, or whenever there is a threshold-exceeded error
      the program goes to sleep for 15 minutes.
      
    Note: a file named twitter_credentials.py must be in the folder with the code
          see the repo: it contains your Twitter credentials
    
    Note: if geocode=True a file named mapquest_key.txt must be in the folder with the code
          get a MapQuest key here: http://developer.mapquest.com/
   
      
    Input: list_of_filenames   a text file with fully-qualified file names
           starting_at         the line number of "list_of_filenames" where processing should start
           ending_at           if 0   process all files beginning with the "starting_at" line in "list_of_filenames"
                               if > 0 process the files from line "starting_at" to line "ending_at" in "list_of_filenames"
           geocode             if True, batched requests are made to the MapQuest Developers API for coordinate and place name data
                               if False, these call are not made and no geo info is added
                                 
           
    Output: a text file named "bigtweet_filexxx.json", where xxx is the "starting_at" number
        
    Usage: %run get_twitter_json.py "filename_list.csv" 2 2
                          - or -
           nohup python get_twitter_json.py "filename_list.csv" 1 0 &
    
    A message like "6 skipped id 448176144668721152" means that Twitter failed to return any data about 
    a tweet with id 448... and that this is the 6th instance of this. 
    """
    
    import csv, json
    import re
    import time, datetime
    import sys, os
    import urllib2,urllib
    import os.path
    from twitter_functions import lookup_multiple_tweets
    
    # convert input parameter strings to integer
    starting_at = int(starting_at) 
    ending_at   = int(ending_at)
    geocode     = bool(geocode)
    msg = "\nlist_of_filenames %s; starting_at %d; ending_at %d; geocode %d"%(list_of_filenames,starting_at,ending_at,geocode)
    logging.info(msg)
    
    process_start = datetime.datetime.now()
    msg = "\n=======================================\nprocess start: %s"%process_start.strftime("%c") + \
          "\n=======================================\n"
    print msg
    sys.stdout.flush()
    logging.info(msg)
    
    # read the list of filenames into "filename_list"
    # ===============================================
    filename_list = []
    with open(list_of_filenames, "rb") as namefile:
        csv_reader = csv.reader(namefile)
        for row in csv_reader:
            filename_list.extend(row)
    
    output_filename   = "bigtweet_file" + "%03d"%(starting_at,) + ".json"
    step              = 100 # we're going to process in groups of "step"
    bulk_list         = []  # batch of rows from input file
    list_of_tweet_ids = []  # tweet ids of these rows
    output_dict       = []  # list of dicts to send to output file
    
    # the Twitter rate limits are documented here
    # https://dev.twitter.com/docs/rate-limiting/1.1/limits
    sleep_batch       = 13500 # we sleep after this many lines processed
    sleep_batch_rows  = 0     # the number of lines we've processes since the last sleep
    
    # MapQuest Developer API documentation: http://developer.mapquest.com/
    Geocoder_count    = 0     # how many records did did we Geocode?
    if geocode:
        f = open('mapquest_key.txt','r')
        key = f.readline()
        f.close()
        mapq_url = 'http://www.mapquestapi.com/geocoding/v1/batch?key='
        mapq_url = mapq_url + key + '&outFormat=json&maxResults=1&callback=renderBatch'
        logging.info("MAPQUEST URL " + mapq_url)

    
    number_of_files   = len(filename_list) # how many files in the list
    file_counter      = 1                  # which one is this one
    global first_sleep
    first_sleep       = True               # first time through, we write an output_file header
    invalid_json      = False              # in case Twitter sends us junk
    global total_processed
    total_processed   = 0                  # how many rows have we processed
    skip_counter      = 0                  # how many rows did we skip because Twitter didn't send us info
    
    # read each file in and process it
    # ==================================
    for input_filename in filename_list:
        
        # skip the first "starting_at-1" files
        if file_counter < starting_at:
            msg = "Skipping %d of %d %s"%(file_counter, number_of_files, input_filename)
            print msg
            logging.info(msg)
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
        #match = re.search(r"Twitter Data\\(.*)", input_filename) # Windows Google Drive
        match = re.search("/home/ubuntu/files(.*)", input_filename) # AWS Ubuntu
        short_file_name = match.group(1)  

        # stop if we're beyond "ending_at"
        if ending_at > 0:
            if file_counter > ending_at:
                msg = "Ending before %d of %d %s"%(file_counter, number_of_files, input_filename)
                print msg
                logging.info(msg)
                break
                
        # check that the file exists
        if not os.path.isfile(input_filename):
            msg = "%s does not exist"%input_filename
            print msg
            logging.info(msg)
            file_counter+=1
            continue
        
        # open an input file
        with open(input_filename, "rb" ) as infile:
            reader     = csv.DictReader(infile)
            lines      = list(reader) # list of all lines/rows in the input file
            totallines = len(lines)   # number of lines in the input file
            
            msg = "\n--Processing %d of %d %s rows %d"%(file_counter, number_of_files, short_file_name,totallines)
            print msg
            logging.info(msg)
            sys.stdout.flush()
            
            # read the input file line-by-line
            # ================================
            for linenum, row in enumerate(lines):
                
                # sleep if we're over the limit of lines processed
                sleep_batch_rows+=1
                if sleep_batch_rows > sleep_batch:
                    msg = "sleeping after %d lines of file %d of %d %s"%(linenum, file_counter, number_of_files, short_file_name)
                    print msg
                    logging.info(msg)
                    sleep_batch_rows = 0
                    sleep_process(output_dict, output_filename)
                    
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
                    msg = "tweet url terminated with non-numeric in line %d"%(linenum+1)
                    print msg
                    logging.info(msg)
                    print row['url']
                    logging.info(row['url'])
                
                # if batch-size reached, process the batch
                if len(list_of_tweet_ids) >= step or (linenum+1) >= totallines:
                   
                    # make a batch request to Twitter 
                    # ===============================
                    result = lookup_multiple_tweets(list_of_tweet_ids)
                        
                    list_of_tweet_ids = []
                    
                    for foo in result:
                        try:
                            tweetdata_list = json.loads(foo)
                            break
                        except ValueError, e:
                            msg = "\nTwitter returned invalid json"
                            print msg
                            logging.info(msg)
                            print e
                            logging.info(e)
                            msg = "after %d lines of file %d of %d %s"%(linenum, file_counter, number_of_files, short_file_name)
                            print msg
                            logging.info(msg)
                            bulk_list = []
                            invalid_json = True
                            break
                            
                    if invalid_json:
                        invalid_json = False
                        break
                        
                    # if Twitter returns an error
                    if 'errors' in tweetdata_list:
                        msg = "Twitter returned an error message:\n" + \
                              "message: " + str(tweetdata_list["errors"][0]['message']) + \
                              "\ncode:    " + str(tweetdata_list["errors"][0]['code']) + \
                              "\nafter %d lines of file %d of %d %s"%(linenum, file_counter, number_of_files, short_file_name)
                        print msg
                        logging.info(msg)
                        sleep_batch_rows = 0
                        sleep_process(tweetdata_list, output_filename)
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
                    
                    tweet_loc_dict = {}
                    tweet_loc_list = []
                    
                    # save every id in tweetdata_list and its position
                    for i in range(len(tweetdata_list)):
                        id = str(tweetdata_list[i]['id'])
                        tweet_id_dict[id] = i
                        tweet_id_list.append(id)
                        
                        # save every location and its position
                        if tweetdata_list[i]['user']['location'] is not None and tweetdata_list[i]['user']['location'].strip() != "":
                            try:
                                loc = str(tweetdata_list[i]['user']['location'])
                                tweet_loc_dict[loc] = i
                                tweet_loc_list.append(loc)
                            except:
                                pass
                        
                    # pull each of the lines and its corresponding Twitter response
                    for line in bulk_list:
                        if line['id'] not in tweet_id_list:
                            skip_counter+=1
                            # check the entire line['id'] is numeric
                            if re.match(r"^\d+", line['id']):
                                # yes
                                msg = "%d skipped id %d"%(skip_counter, int(line['id']))
                                print msg
                                logging.info(msg)
                            else:
                                # no
                                print skip_counter
                                logging.info(skip_counter)
                                msg = "line['id'] is not all numeric"
                                print msg
                                logging.info(msg)
                                print line['id']            
                                logging.info(line['id'])
                            continue
                            
                        tweetdata = tweetdata_list[tweet_id_dict[line['id']]]
                        if str(line['id']) != str(tweetdata['id']):
                            skip_counter+=1
                            msg = "id mismatch, skipping %d"%(skip_counter) + \
                                   "\nline  id %s"%(str(line['id'])) + \
                                   "\ntweet id %s"%(str(tweetdata['id']))
                            print msg
                            logging.info(msg)
                            continue
                            
                        # ===========================================
                        # add Topsy fields to Twitter's json response
                        # ===========================================
                            
                        # add a timestamp for 'created_at'
                        # time.ctime(tweet['timestamp']) # will decode this field
                        tweetdata_list[tweet_id_dict[line['id']]]['timestamp'] = \
                            time.mktime(datetime.datetime.strptime(tweetdata_list[tweet_id_dict[line['id']]]['created_at'], '%a %b %d %H:%M:%S +0000 %Y').timetuple())
                            
                        tweetdata_list[tweet_id_dict[line['id']]]['topsy'] = {}
                        # add a timestamp for topsy's 'firstpost_date' 
                        try: 
                            tweetdata_list[tweet_id_dict[line['id']]]['topsy']['timestamp'] = \
                                time.mktime(datetime.datetime.strptime(line['firstpost_date'], "%m/%d/%Y").timetuple())
                        except:
                            try:
                                tweetdata_list[tweet_id_dict[line['id']]]['topsy']['timestamp'] = \
                                    time.mktime(datetime.datetime.strptime(line['firstpost_date'], "%m/%d/%y").timetuple())
                            except:
                                tweetdata_list[tweet_id_dict[line['id']]]['topsy']['timestamp'] = ""
                                
                        # add the topsy csv file fields to the Twitter json
                        tweetdata_list[tweet_id_dict[line['id']]]['topsy']['firstpost_date']        = line['firstpost_date']
                        tweetdata_list[tweet_id_dict[line['id']]]['topsy']['score']                 = float(line['score'])
                        tweetdata_list[tweet_id_dict[line['id']]]['topsy']['trackback_author_nick'] = line['trackback_author_nick']
                        tweetdata_list[tweet_id_dict[line['id']]]['topsy']['trackback_author_url']  = line['trackback_author_url']
                        tweetdata_list[tweet_id_dict[line['id']]]['topsy']['trackback_permalink']   = line['trackback_permalink']
                        tweetdata_list[tweet_id_dict[line['id']]]['topsy']['url']                   = line['url']
                        
                        tweetdata_list[tweet_id_dict[line['id']]]['topsy']['file_counter']          = file_counter
                        tweetdata_list[tweet_id_dict[line['id']]]['topsy']['short_file_name']       = short_file_name
                        
                    # =======================================
                    # add geo data to Twitter's json response
                    # =======================================
                    
                    if geocode:
                        # give everybody a blank 
                        for idx in range(len(tweetdata_list)):
                            tweetdata_list[idx]["user"]["location_geoinfo"] = {}
                            
                        # create a list of locations to send to MapQuest
                        loc_url = ''
                        for tweet_loc in tweet_loc_list:
                            loc_url = loc_url + '&location=' + tweet_loc
                        # send 'em
                        urllib.urlretrieve (mapq_url + loc_url, "batch.json")
                        # get the answer
                        batch = open("batch.json","r")
                        lines = batch.readlines()
                        batch.close()
                        
                        # what they send back has superfluous stuff at the front and back ends
                        match = []
                        if lines: match = re.search(r"renderBatch\((\{.*\})", lines[0])
                        if match:
                            result = match.group(1)
                            try:
                                locs = json.loads(result)
                                
                                # step through MapQuest's response and add data to Twitter's json response
                                for results in locs['results']:
                                    if results['providedLocation']['location'] in tweet_loc_dict.keys():
                                    #===========================
                                    # an idea for an alternative
                                    #===========================
                                    #needle   = results['providedLocation']['location']
                                    #haystack = tweet_loc_dict.keys()
                                    #indices  = [i for i, s in enumerate(haystack) if needle in s]
                                        dict_loc = tweet_loc_dict[results['providedLocation']['location']]
                                        tweetdata_list[dict_loc]["user"]["location_geoinfo"] = results['locations'][0]
                                        if tweetdata_list[dict_loc]["user"]["location_geoinfo"]:
                                            Geocoder_count += 1
                                    else:
                                        logging.warning("\nMAPQUEST KEY MISMATCH")
                                        logging.warning(tweet_loc_dict.keys())
                                        logging.warning(results)
                            except:
                                msg = "MapQuest sent invalid json"
                                print msg
                                logging.warning(msg)
                                logging.warning(lines)
                        else:
                            msg = "MapQuest sent empty response"
                            print msg
                            logging.warning(msg)
                            logging.warning(lines)
                        
                        
                                    
                    # process the json file and start over with a new batch from Twitter
                    # ==================================================================
                    process_output_file(tweetdata_list, output_filename)
                    bulk_list = []
                  
        file_counter+=1
                            
    # how long did it take?
    process_end     = datetime.datetime.now()
    process_elapsed = process_end - process_start
    process_seconds = process_elapsed.seconds
    process_minutes = process_seconds/60.0
    process_hours   = process_minutes/60.0
    
    msg = "\n=======================================\n" + \
          "process start: %s"%process_start.strftime("%c") + \
          "\nprocess end:   %s"%process_end.strftime("%c") + \
          "\nprocess elapsed hours %0.2f"%process_hours
    if Geocoder_count > 0:
        msg = msg + "\n%d records geo-encoded"%Geocoder_count
    msg = msg + "\n=======================================\n" 
    print msg
    logging.info(msg)
    
                    
    
def sleep_process(output_dict, output_filename):
    import time
    import sys
    import datetime
    from datetime import timedelta
    
    process_output_file(output_dict, output_filename)
    
    length_of_sleep = int(15.1*60)  # seconds
    timenow    = datetime.datetime.today().strftime("%H:%M:%S")
    timeplus15 = (datetime.datetime.today()+timedelta(seconds=length_of_sleep)).strftime("%H:%M:%S")
    msg = "sleeping at %s, will resume at %s"%(timenow, timeplus15)
    print msg
    logging.info(msg)
    sys.stdout.flush()
    
    time.sleep(length_of_sleep)
    
def process_output_file(output_dict, output_filename):
    import json
    import datetime
    import io
    import sys
    
    global total_processed
    global first_sleep
    
    if 'errors' not in output_dict:
        if first_sleep:
            with io.open(output_filename, 'w', encoding='utf-8') as f:
                first_sleep = False
                for tweet in output_dict:
                    f.write(unicode(json.dumps(tweet, ensure_ascii=False)))
                    f.write(u"\n")
                    total_processed+=1
        else:
            with io.open(output_filename, 'a', encoding='utf-8') as f:
                for tweet in output_dict:
                    f.write(unicode(json.dumps(tweet, ensure_ascii=False)))
                    f.write(u"\n")
                    total_processed+=1
                
        timenow     = datetime.datetime.today().strftime("%H:%M:%S")
        msg = "%s processed at %s, rows %d"%(output_filename, timenow, total_processed)
        print msg
        logging.info(msg)
        sys.stdout.flush()
    output_dict = []
    
                    
if __name__ == '__main__':
    import sys
    # set up for logging to a file
    import logging
    logging.basicConfig(filename='logfile.log',level=logging.DEBUG, \
                        format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    if len(sys.argv) == 2: get_twitter_json(sys.argv[1],starting_at=1, ending_at=0, geocode=True)
    if len(sys.argv) == 3: get_twitter_json(sys.argv[1],sys.argv[2], ending_at=0, geocode=True)
    if len(sys.argv) == 4: get_twitter_json(sys.argv[1],sys.argv[2], sys.argv[3], geocode=True)
    if len(sys.argv) == 5: get_twitter_json(sys.argv[1],sys.argv[2], sys.argv[3], sys.argv[4])
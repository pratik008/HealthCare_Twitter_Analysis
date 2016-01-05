from __future__ import division
"""
This program reads in a text file of Twitter json augmented with geo data
by update_geo_data.py and provides reverse geo coding          

Output:     "HTA_reversegeo.json"   

Usage:      nohup python reverse_geocoding.py > nohuprev.out &
"""

def main():
    import json
    import datetime
    import sys, os, io
    from geolocate_reverse import geolocate_reverse

    process_start = datetime.datetime.now()
    msg = "\n============================================="  + \
          "\nupdate augmented geo data                    "  + \
          "\nprocess start: %s"%process_start.strftime("%c") + \
          "\n=============================================\n"
    print msg
    sys.stdout.flush()
    
    total_lines           = 0    # how many total input lines?
    total_geo_tags        = 0    # how many geo tags did we end up with?
    orig_geo_tags         = 0    # how many geo tags did we already have?
    
    output_list           = []   # list of tweets to send to output file
    
    global first_sleep
    first_sleep       = True               # first time through, we write to a new file
    global total_written
    total_written     = 0                  # how many rows have we written to the output file
    
    file_counter      = 0                  # which one is this one?
    
    output_json_filename = "HTA_reversegeo.json"
    # read in the files one-by-one
    # ============================
    for input_filename in ["HTA_geotagged.json"]:
        file_counter+=1
        print "---Processing file %d %s"%(file_counter, input_filename)
        sys.stdout.flush()
        
        # check that the file exists
        if not os.path.isfile(input_filename):
            msg = "%s does not exist "%input_filename
            print msg
            sys.stdout.flush()
            continue
            
        # open the file and read it line-by-line
        # ======================================
        with open(input_filename, "r" ) as infile:
            file_lines = 0
            for line in infile:
                file_lines+=1
                total_lines+=1
                    
                # read a line of json
                try:
                    tweet = json.loads(str(line))
                except Exception, e:
                    print "\nat line %d of %s "%(file_lines, input_filename)
                    print repr(e)
                    print "line will not be included in the output file\n"
                    sys.stdout.flush()
                    continue
                    
                # create the empty field to be added to each record
                tweet["geo_reverse"] = {"country_code": "", 
                                           "country": "",
                                           "zipcode": "",
                                           "city": "",
                                           "state": "",
                                           "state_abbr": "",
                                           "areacode": "",
                                           "FIPS": "",
                                           "county": "",
                                           "Type": "",
                                           "Pop_2010": "",
                                           "Land_Sq_Mi": ""}   
                if tweet['geo']:
                    lat = tweet['geo']["coordinates"][0]
                    lon = tweet['geo']["coordinates"][1]
                    #print (lat,lon)
                    tweet["geo_reverse"] = geolocate_reverse((lat,lon))
                output_list.append(tweet)
                
                if total_lines%500 == 0:
                    process_output_file(output_list, output_json_filename)
                    output_list = []
                    right_now = datetime.datetime.now()
                    print "%s line %d of file %s"%(right_now.strftime("%c"), file_lines, input_filename)
                    sys.stdout.flush()
                    
    process_output_file(output_list, output_json_filename)
    output_list = []
    right_now = datetime.datetime.now()
    print "%s line %d of file %s"%(right_now.strftime("%c"), file_lines, input_filename)
    sys.stdout.flush()
    
    process_end     = datetime.datetime.now()
    process_elapsed = process_end - process_start
    process_seconds = process_elapsed.seconds
    process_minutes = process_seconds/60.0
    process_hours   = process_minutes/60.0

    msg = "\n=======================================\n" + \
          "process start: %s"%process_start.strftime("%c") + \
          "\nprocess end:   %s"%process_end.strftime("%c") + \
          "\nprocess elapsed hours %0.2f"%process_hours
    msg = msg + "\n=======================================\n" 
    print msg
    
def process_output_file(output_list, output_json_filename):
    import json
    import datetime
    import io
    import sys
    
    global total_written
    global first_sleep
    
    if first_sleep:
        with io.open(output_json_filename, 'w', encoding='utf-8') as f:
            first_sleep = False
            for tweet in output_list:
                try:
                    #f.write(unicode(json.dumps(tweet, ensure_ascii=False)))
                    f.write(unicode(json.dumps(tweet, ensure_ascii=True)))
                    f.write(u"\n")
                    total_written+=1
                except Exception,e:
                    print e
                    print tweet

    else:
        with io.open(output_json_filename, 'a', encoding='utf-8') as f:
            for tweet in output_list:
                try:
                    #f.write(unicode(json.dumps(tweet, ensure_ascii=False)))
                    f.write(unicode(json.dumps(tweet, ensure_ascii=True)))
                    f.write(u"\n")
                    total_written+=1
                except Exception,e:
                    print e
                    print tweet            
    output_list = []

if __name__ == '__main__':
    import sys
    main()
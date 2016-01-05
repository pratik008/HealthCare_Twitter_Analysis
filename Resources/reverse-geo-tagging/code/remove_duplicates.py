from __future__ import division
"""
This program produces the final output file of the project to
supplement the Twitter data that the Healthcare Twitter Analysis 
project began with.

Input:      All the reverse geo-coded Twitter files for Healthcare Twitter Analysis project         

Output:     "HTA_noduplicates.json" 
            A consolidated file with
            1) duplicates removed
            2) additional reverse geo-coding based on "coordinates"            

Usage:      nohup python remove_duplicates.py > remdups.out &
"""

def main():
    import json
    import datetime
    import sys, os, io
    from geolocate_reverse import geolocate_reverse
    
    output_json_filename = "HTA_noduplicates.json"
    input_file_list      = ["HTA_reversegeo.json",  \
                            "HTA_reversegeo2.json", \
                            "HTA_reversegeo3.json", \
                            "HTA_reversegeo4.json"]


    process_start = datetime.datetime.now()
    msg = "\n============================================="  + \
          "\nremove duplicates                            "  + \
          "\nprocess start: %s"%process_start.strftime("%c") + \
          "\n=============================================\n"
    print msg
    sys.stdout.flush()
    
    input_lines           = 0     # how many total input lines?
    output_lines          = 0     # how many output lines?
    duplicates            = 0     # how many duplicates were found?
    coord_count           = 0     # how many coordinate fields did we process?
    id_set                = set() # keep track of unique id's
    output_list           = []    # list of lines to write
    global first_sleep
    first_sleep       = True               # first time through, we write to a new file
    global total_written
    total_written     = 0                  # how many rows have we written to the output file
        
    # read in the files one-by-one
    # ============================
    for input_filename in input_file_list:
        print "---Processing file %s"%input_filename
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
                input_lines+=1
                file_lines+=1
                    
                # read a line of json
                try:
                    tweet = json.loads(line)
                except Exception, e:
                    print "\nat line %d of %s "%(file_lines, input_filename)
                    print repr(e)
                    print "line will not be included in the output file\n"
                    sys.stdout.flush()
                    continue
                     
                # have we already seen this tweet's id?
                tweet_id = tweet["id"]
                if tweet_id in id_set:
                    duplicates+=1
                    continue
                id_set.add(tweet_id)

                # does this tweet have a coordinates field?
                # https://dev.twitter.com/docs/platform-objects/tweets
                # reverse geo using it, if it does
                if tweet['coordinates']:
                    coord_count+=1
                    lon = tweet['coordinates']["coordinates"][0]
                    lat = tweet['coordinates']["coordinates"][1]
                    tweet["geo_reverse"] = geolocate_reverse((lat,lon))
                    # print (lat,lon)
                    # print json.dumps(tweet["geo_reverse"],indent=4)
                    # print
                    
                # add to the output list
                output_list.append(tweet)
                output_lines+=1
                
                if output_lines%5000 == 0:
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
    print "input_lines  %d"%input_lines
    print "output_lines %d"%output_lines
    print "input_lines - output_lines %d"%(input_lines - output_lines)
    print "duplicates                 %d"%duplicates
    print "output_lines/input_lines*100 %0.2f"%(output_lines/input_lines*100)
    print "duplicates/input_lines*100    %0.2f\n"%(duplicates/input_lines*100)
    print "coord_count                   %d"%coord_count
    print "coord_count/output_lines*100  %0.2f"%(coord_count/output_lines*100)
    print "total_written %d"%total_written
    print "len(id_set)   %d"%len(id_set)
    
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
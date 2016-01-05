from __future__ import division
#
# following the initial file creation with the full Twitter data
# this program 
#   1. consolidates the resulting three output files
#   2. adds lat and lon to the tweet['geo'] field
#
# Usage: nohup python update_geo_data.py &

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
                f.write(unicode(json.dumps(tweet, ensure_ascii=False)))
                f.write(u"\n")
                total_written+=1

    else:
        with io.open(output_json_filename, 'a', encoding='utf-8') as f:
            for tweet in output_list:
                f.write(unicode(json.dumps(tweet, ensure_ascii=False)))
                f.write(u"\n")
                total_written+=1
                
    right_now = datetime.datetime.now()
    print "%s %d lines written"%(right_now.strftime("%c"), total_written)
    sys.stdout.flush()

import json
import datetime
import sys, os, io, re
from twitter_functions import mapquest_single_location

process_start = datetime.datetime.now()
msg = "\n============================================="  + \
      "\nupdate geo tagging and consolidate json files"  + \
      "\nprocess start: %s"%process_start.strftime("%c") + \
      "\n=============================================\n"
print msg
sys.stdout.flush()

geo_count        = 0
place_count      = 0
loc_count        = 0
mapq_count       = 0
bigplace_count   = 0
line_count       = 0
file_count       = 0
key = '<replace with your personal mapquest key>'

output_list      = []       # list of tweets to send to output file
global first_sleep
first_sleep      = True     # first time through, we write to a new file
global total_written
total_written    = 0        # how many rows have we written to the output file

# top cities in the United States
bigones={'new york':'New York, New York',
         'nyc':'New York, New York',
         'los angeles':'Los Angeles, California',
         'chicago':'Chicago, Illinois',
         'houston':'Houston, Texas',
         'philadelphia':'Philadelphia, Pennsylvania',
         'phoenix':'Phoenix, Arizona',
         'san antonio':'San Antonio, Texas',
         'san diego':'San Diego, California',
         'dallas':'Dallas, Texas',
         'san jose':'San Jose, California',
         'austin':'Austin, Texas',
         'indianapolis':'Indianapolis, Indiana',
         'jacksonville':'Jacksonville, Florida',
         'san francisco':'San Francisco, California',
         'columbus':'Columbus, Ohio',
         'charlotte':'Charlotte, North Carolina',
         'fort worth':'Fort Worth, Texas',
         'detroit':'Detroit, Michigan',
         'el paso':'El Paso, Texas',
         'memphis':'Memphis, Tennessee',
         'seattle':'Seattle, Washington',
         'denver':'Denver, Colorado',
         'boston':'Boston, Massachusetts',
         'nashville':'Nashville, Tennessee',
         'baltimore':'Baltimore, Maryland',
         'louisville':'Louisville, Kentucky',
         'portland':'Portland, Oregon',
         'atlanta':'Atlanta, Georgia',
         'washington, dc':'Washington, District of Columbia',
         'tampa bay':'St. Petersburg, Florida'}
         
st_abbr = {'WA': 'Washington', 'DE': 'Delaware', 'DC': 'District of Columbia', 'WI': 'Wisconsin', 
           'WV': 'West Virginia', 'HI': 'Hawaii', 'FL': 'Florida', 'WY': 'Wyoming', 
           'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'TX': 'Texas', 
           'LA': 'Louisiana', 'NC': 'North Carolina', 'ND': 'North Dakota', 'NE': 'Nebraska', 
           'TN': 'Tennessee', 'NY': 'New York', 'PA': 'Pennsylvania', 'CA': 'California', 
           'NV': 'Nevada', 'VA': 'Virginia', 'CO': 'Colorado', 'AK': 'Alaska', 'AL': 'Alabama', 
           'AR': 'Arkansas', 'VT': 'Vermont', 'IL': 'Illinois', 'GA': 'Georgia', 'IN': 'Indiana', 
           'IA': 'Iowa', 'OK': 'Oklahoma', 'AZ': 'Arizona', 'ID': 'Idaho', 'CT': 'Connecticut', 
           'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 'OH': 'Ohio', 'UT': 'Utah', 
           'MO': 'Missouri', 'MN': 'Minnesota', 'MI': 'Michigan', 'RI': 'Rhode Island', 
           'KS': 'Kansas', 'MT': 'Montana', 'MS': 'Mississippi', 'SC': 'South Carolina', 
           'KY': 'Kentucky', 'OR': 'Oregon', 'SD': 'South Dakota','ON': 'Ontario Canada'}
           
state_cities = {'Mississippi': 'Jackson, Mississippi', 'Oklahoma': 'Oklahoma City, Oklahoma', 'Delaware': 'Wilmington, Delaware', 
                'Minnesota': 'Minneapolis, Minnesota', 'Illinois': 'Chicago, Illinois', 'Arkansas': 'Little Rock, Arkansas', 
                'New Mexico': 'Santa Fe, New Mexico', 'Indiana': 'Indianapolis, Indiana', 'Maryland': 'Baltimore, Maryland', 
                'Louisiana': 'Baton Rouge, Louisiana', 'Idaho': 'Boise ,Idaho', 'Wyoming': 'Cheyenne, Wyoming', 
                'Tennessee': 'Nashville, Tennessee', 'Arizona': 'Phoenix, Arizona', 'Iowa': 'Des Moines, Iowa', 
                'Michigan': 'Detroit, Michigan', 'Kansas': 'Wichita, Kansas', 'Utah': 'Salt Lake City, Utah', 
                'Virginia': 'Richmond, Virginia', 'Oregon': 'Portland, Oregon', 'Connecticut': 'Bridgeport, Connecticut', 
                'Montana': 'Billings, Montana', 'California': 'San Francisco, California', 'Massachusetts': 'Boston, Massachusetts', 
                'West Virginia': 'Charleston, West Virginia', 'South Carolina': 'Columbia, South Carolina', 
                'New Hampshire': 'Manchester, New Hampshire', 'Wisconsin': 'Milwaukee, Wisconsin', 'Vermont': 'Burlington, Vermont', 
                'Georgia': 'Atlanta, Georgia', 'North Dakota': 'Fargo, North Dakota', 'Pennsylvania': 'Philadelphia, Pennsylvania', 
                'Florida': 'Orlando, Florida', 'Alaska': 'Anchorage, Alaska', 'Kentucky': ' Louisville, Kentucky', 'Hawaii': 'Honolulu, Hawaii', 
                'Nebraska': 'Omaha, Nebraska', 'Missouri': 'St. Louis, Missouri', 'Ohio': 'Columbus, Ohio', 'Alabama': 'Birmingham, Alabama', 
                'New York': 'New York, New York', 'South Dakota': 'Sioux Falls, South Dakota', 'Colorado': 'Denver, Colorado', 
                'New Jersey': 'Haddonfield, New Jersey', 'Washington': 'Washington, District of Columbia', 'North Carolina': 'Charlotte, North Carolina', 
                'Texas': 'Dallas, Texas', 'Nevada': 'Reno, Nevada', 'Maine': 'Portland, Maine', 'Rhode Island': 'Providence, Rhode Island',
                'Canada':'Toronto, Canada','Egypt':'Cairo, Egypt','Toronto': 'Toronto, Canada','Ottawa': 'Ottawa, Canada'}


         
output_json_filename = "HTA_geotagged.json"
         
for input_filename in ["bigtweet_file001.json","bigtweet_file329.json","bigtweet_file361.json"]:
#for input_filename in ["bigtweet_file329.json"]:
    print "---Processing file %s"%input_filename
    sys.stdout.flush()
    
    file_count+=1
    file_lines = 0
    f = open(input_filename,'r')
    
    # process line-by-line
    for line in f:
        #
        #  AFTER A FAILURE
        #  ===============
        #
        if line_count < 211499:
            line_count+=1
            file_lines+=1
            first_sleep = False
            continue
            
        line_count+=1
        file_lines+=1
        try:
            tweet = json.loads(line)
        except Exception, e:
            print "\nat line %d of %s "%(file_lines, input_filename)
            print repr(e)
            print "line will not be included in the output file\n"
            continue
        
        tweet["user"]["location_geoinfo"] = {}           # null out this field
        location = tweet['user']['location'].strip()     # get the location
        
        # if the geo field exists, continue
        # =================================
        if tweet['geo']:
           geo_count+=1
           #print "geo:      %s %s"%(tweet['geo'], location)
        else:
            
            # if place exists, create a geo item with the lat and lon
            # =======================================================
            if tweet['place']:
                if tweet['place']['bounding_box']:
                    if tweet['place']['bounding_box']['coordinates']:
                        place_count+=1
                        place_lon = tweet['place']['bounding_box']['coordinates'][0][0][0]
                        place_lat = tweet['place']['bounding_box']['coordinates'][0][0][1]
                        geo_dict  = {}
                        geo_dict['type']        = 'Point'
                        geo_dict['coordinates'] = [place_lat, place_lon]
                        orig_tweet   = tweet.copy()
                        tweet['geo'] = geo_dict
                        #print "place:    %s %s"%(tweet['geo'], location)
                        try:
                            json.loads(json.dumps(tweet))
                        except Exception, e:
                            print "invalid tweet resulted from mapquest return"
                            print e
                            print mapq_ret
                            # revert to the original if there is a problem
                            tweet = orig_tweet.copy()
                            print "original tweet will be written to the output file"
            else:
                
                # if neither geo nor place exists, ask MapQuest for lat and lon
                # =============================================================
                if tweet['user']['location']:
                    #print
                    #print location
                    loc_count+=1
                    for city in bigones:
                        if city in tweet['user']['location'].lower():
                            bigplace_count+=1
                            location = bigones[city]
                            break
                    location = re.sub("^us$|^usa$|,? usa?$", "", location, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
                    #print location
                    match = re.search(", (AL|AK|AZ|AR|CA|CO|CT|DE|DC|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY)$", location, re.DOTALL | re.MULTILINE)
                    if match:
                        abbr    = match.group(1)
                        full    = st_abbr[abbr]
                        location = re.sub(abbr, full, location)
                    else:
                        for state in state_cities:
                            if state.lower() == location.lower():
                                location = state_cities[state]
                                break
                    #print location    
                    mapq_ret = mapquest_single_location(location.strip(), key)
                    if mapq_ret:
                        #print "%s ****"%location
                        mapq_count+=1
                        mapq_lat = mapq_ret['displayLatLng']['lat']
                        mapq_lon = mapq_ret['displayLatLng']['lng']
                        geo_dict  = {}
                        geo_dict['type']        = 'Point'
                        geo_dict['coordinates'] = [mapq_lat, mapq_lon]
                        orig_tweet   = tweet.copy()
                        tweet['geo'] = geo_dict
                        
                        # make sure that the resulting tweet is still valid json
                        try:
                            json.loads(json.dumps(tweet))
                        except Exception, e:
                            print "invalid tweet resulted from mapquest return"
                            print e
                            print mapq_ret
                            # revert to the original if there is a problem
                            tweet = orig_tweet.copy()
                            print "original tweet will be written to the output file"

        output_list.append(tweet)
        
        # write out the records every ...
        if line_count%500 == 0:
            print "after %d lines"%line_count
            process_output_file(output_list, output_json_filename)
            sys.stdout.flush()
            output_list = []
            
        #if line_count > 5000: break
        
    f.close()
    
process_output_file(output_list, output_json_filename)
output_list = []

print
print "file_count     %d"%file_count
print "line_count     %d"%line_count
print "geo_count      %d"%geo_count
print "place_count    %d"%place_count
print "loc_count      %d"%loc_count
print "mapq_count     %d"%mapq_count
print "bigplace_count %d"%bigplace_count
print "pct geo+place  %0.2f"%((geo_count+place_count)/line_count*100.)
print "pct big/loc    %0.2f"%(bigplace_count/loc_count*100.)
print "pct mapq/loc   %0.2f"%(mapq_count/loc_count*100.)
print "pct reliable   %0.2f"%((geo_count+place_count+bigplace_count)/line_count*100.)

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
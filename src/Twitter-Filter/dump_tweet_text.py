#!/usr/bin/python
import sys
import json
import codecs
import re
import os
import time
import sys
from utility import byteify

allowed_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ '
shortword = re.compile(r'\W*\b\w{1,3}\b')

def extract_tweets(file_name):
    output_dir = os.path.join(os.path.dirname(file_name),"tweet_text")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_big_file = 'all_tweets.txt'
    bigflattext = open(os.path.join(output_dir,output_big_file),'w')
    count = 0
    with codecs.open(file_name,encoding="utf-8") as f1:
        for line in f1:            
            if float(count)/10000. == count/10000:
				print count
            try: 
                data = byteify(json.loads(line))
	    except ValueError:
                print 'Bad JSON record, skipping...', count
		continue

	    result = output_dir + '/tweet_' + str(data['id']) + '.txt'
	    out = shortword.sub('', data['text'].encode('ascii','ignore').translate(None,'\n'))
	    json.dump(out, open(result, 'w'))
            bigflattext.write(str(data['id']) + ' '*5 + out + '\n' )
	    count = count + 1


    bigflattext.close()
    return count


if __name__ == '__main__':
    t0 = time.time()
    if len(sys.argv) < 2:
        print "usage: dump_tweet_text [jsonTweetsFile]"
        quit()
    count = extract_tweets(sys.argv[1])
    print 'Finished. Took {0:4.1f} minutes.'.format((time.time()-t0)/60.)
    print '{0} tweets dumped.'.format(count)

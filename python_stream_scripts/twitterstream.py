##########################################################
#
# Author: ?
# Modified by: Hans Goldman
# email: hansjgoldman@gmail.com
# date: May 2013
#
##########################################################
import oauth2 as oauth
import urllib2 as urllib
import json
import os
import time
import datetime


config_json = open('config.json', 'r')
config = json.load(config_json)

# Go to http://dev.twitter.com and create an app.
# The consumer key and secret will be generated for you.
consumer_key = config["consumer_key"]
consumer_secret = config["consumer_secret"]

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section.
access_token_key = config["access_token"]
access_token_secret = config["access_token_secret"]


_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
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

  response = opener.open(url, encoded_post_data)

  return response

def fetchsamples():
  url = "https://stream.twitter.com/1/statuses/sample.json?geocode=37.781157,-122.398720,1mi"
  parameters = []
  response = twitterreq(url, "POST", parameters)
  
  counter = 0
  stringBuffer = "["
  for line in response:
    line = line.strip()
    if line.startswith("{\"delete\"") is False:
      #check if Tweet is in English
      if line.endswith('"en"}'):
        stringBuffer += line
        counter = counter + 1
        #check if size limit is met
        if counter == 100:
          counter = 0
          timestamp = '[' + datetime.datetime.now().strftime("%H.%M.%S.%f") + ']'
          stringBuffer += ']'
          outFile = open("dump\\twitterDump" + timestamp + ".json", "w")
          outFile.write(stringBuffer)
          outFile.close()
          stringBuffer = '['
          #Log successful assignment
          print timestamp, 'New dump successfully archived.'
        else:
          stringBuffer += ','
      
fetchsamples()

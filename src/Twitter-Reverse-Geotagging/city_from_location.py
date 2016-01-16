from __future__ import print_function
from citySuggestion import CitySuggestion
from utility import *
import sys
import json
import os

def main():
	if len(sys.argv) != 4:
		print("$ city_from_location [tweetsJsonFile] [citiesFile] [destDir]")
		quit()
	conformizeCities(sys.argv[1],sys.argv[2],sys.argv[3])
	
def conformizeCities(tweetsFile,cityFile,destDir,export=True,threshold=80,delim='\t'):
	tweets = {}
	if export is True: cFile = openWithHeaders(destDir,'city_conformed.txt','tweet_id,location,search_words')
	if export is True: openWithHeaders(destDir,'no_match.txt','match_score,close_match,location').close()
	suggestion = CitySuggestion(cityFile,delim)
	with open(tweetsFile) as tFile:
		count = 0
		filtered = 0
		noMatch = 0
		notSpecified = 0
		for line in tFile:
			tweet = byteify(json.loads(line))
			searchWords = tweet['user']['location']
			city = suggestion.predictCity(searchWords,threshold,destDir,export)
			if city is True:
				filtered += 1
			elif city is False:
				noMatch += 1
			elif city is None:
				notSpecified += 1
			else:
				tweet['user']['location'] = city
			tweets[str(tweet['id'])] = {"location":tweet['user']['location']}
			if export is True: cFile.write('{0},"{1}","{2}"\n'.format(tweet['id'],tweet['user']['location'],searchWords))
			count += 1
			print("{0}/{1} city > {2}% match".format((count-notSpecified-filtered-noMatch),count,threshold),end="\r")
	print()
	print(notSpecified,'tweets did not specify locations')
	print(noMatch,'tweet locations have no match'.format(os.path.join(destDir,'no_match.txt')))
	print(filtered,' locations have no strong match'.format(os.path.join(destDir,'stron_match.txt')))
	if export is True: cFile.close()
	return tweets

if __name__ == "__main__":
	main()

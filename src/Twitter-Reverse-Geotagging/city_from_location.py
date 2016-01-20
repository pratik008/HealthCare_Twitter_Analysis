from __future__ import print_function
from citySuggestion import CitySuggestion
from utility import *
import sys
import json
import os

def main():
<<<<<<< HEAD
=======
	print('huh?')
>>>>>>> e1f1750c014f9de2e78fe17fa9314602ce6d05f0
	if len(sys.argv) != 4:
		print("$ city_from_location [tweetsJsonFile] [citiesFile] [destDir]")
		quit()
	conformizeCities(sys.argv[1],sys.argv[2],sys.argv[3])
	
def conformizeCities(tweetsFile,cityFile,destDir,export=True,threshold=80,delim='\t'):
	tweets = {}
<<<<<<< HEAD
	if export is True: cFile = openWithHeaders(destDir,'strong_match.txt','tweet_id,location,search_words')
=======
	if export is True: cFile = openWithHeaders(destDir,'city_conformed.txt','tweet_id,location,search_words')
>>>>>>> e1f1750c014f9de2e78fe17fa9314602ce6d05f0
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
<<<<<<< HEAD
			tweets[str(tweet['id'])] = {"location":tweet['user']['location']}
=======
>>>>>>> e1f1750c014f9de2e78fe17fa9314602ce6d05f0
			if city is True:
				filtered += 1
			elif city is False:
				noMatch += 1
			elif city is None:
				notSpecified += 1
			else:
				tweet['user']['location'] = city
<<<<<<< HEAD
				if export is True: cFile.write('{0},"{1}","{2}"\n'.format(tweet['id'],tweet['user']['location'],searchWords))
			count += 1
			print("{0}/{1} cities with > {2}% match".format((count-notSpecified-filtered-noMatch),count,threshold),end="\r")
	print()
	print(notSpecified,'tweets did not specify locations')
	print(noMatch,' tweet locations have no match (included in {0})'.format(os.path.join(destDir,'no_match.txt')))
	print(filtered,' locations have no strong match (included in {0})'.format(os.path.join(destDir,'no_match.txt')))
=======
			tweets[str(tweet['id'])] = {"location":tweet['user']['location']}
			if export is True: cFile.write('{0},"{1}","{2}"\n'.format(tweet['id'],tweet['user']['location'],searchWords))
			count += 1
			print("{0}/{1} city > {2}% match".format((count-notSpecified-filtered-noMatch),count,threshold),end="\r")
	print()
	print(notSpecified,'tweets did not specify locations')
	print(noMatch,'tweet locations have no match'.format(os.path.join(destDir,'no_match.txt')))
	print(filtered,' locations have no strong match'.format(os.path.join(destDir,'stron_match.txt')))
>>>>>>> e1f1750c014f9de2e78fe17fa9314602ce6d05f0
	if export is True: cFile.close()
	return tweets

if __name__ == "__main__":
	main()

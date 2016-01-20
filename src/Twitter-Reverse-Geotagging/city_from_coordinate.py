from __future__ import print_function
from citySuggestion import CitySuggestion
from utility import *
import sys
import json
import os
import csv

def main():
	if len(sys.argv) != 4:
		print("$ city_from_coordinate [tweetsJsonFile] [citiesFile] [destDir]")
		quit()
	extractCitiesWithCoordinates(sys.argv[1],sys.argv[2],sys.argv[3])
	
def extractCitiesWithCoordinates(tweetsFile,cityFile,destDir):
	cities = getCoordinatesFromCSV(cityFile)
	tweets = []
	hasCoordinates = 0
	hasClosest = 0
	count = 0
	out = open(os.path.join(destDir,'coordinate_match.txt'),'w+')
	out.write('id,city\n')
	with open(tweetsFile) as tFile:
		for line in tFile:
			tweet = byteify(json.loads(line))
			result = findCloesetKnownCity(cities,tweet)
			if result is not None:
				hasClosest += 1
				tweets.append(result)
				out.write('{0},{1}\n'.format(result[0],result[1]))
			if tweet['coordinates']: hasCoordinates += 1
			count += 1
			print('{0}/{1} tweets has coordinates'.format(hasCoordinates,count),end='\r')
	print()
	print('In the {0} tweets processed, {1} out of {2} has matched with a location'.format(count,hasClosest,hasCoordinates))
	out.close()
	return tweets
	
def makeCoordinateKey(longitude):
	return str(abs(int(float(longitude)*100)))
	
def findCloesetKnownCity(cities,tweet):
	shortestRelativeDistance = 2056
	closestLoc = None
	if not tweet['coordinates']: return None
	t = tweet['coordinates']['coordinates']
	key = makeCoordinateKey(t[0])
	places = cities[key]
	for loc in places:
		if closestLoc is None: closestLoc = loc
		d = ((t[0]+float(loc['longitude']))**2 + (t[1]+float(loc['latitude']))**2) ** 0.5
		if d < shortestRelativeDistance:
			shortestRelativeDistance = d
			closestLoc = loc
	return [closestLoc['id'],closestLoc]
	
def getCoordinatesFromCSV(cityFile,delim='\t'):
	reader = csv.DictReader(open(os.path.join(cityFile)),delimiter=delim)
	result = {}
	for row in reader:
		if not row.get('longitude',False): continue
		key = makeCoordinateKey(row['longitude'])
		if key not in result:
			result[key] = []
			pass
		result[key].append(row)
	return result

if __name__ == "__main__":
	main()

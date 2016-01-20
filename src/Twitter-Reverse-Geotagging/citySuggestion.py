import autocomplete
import re
import os
import csv
from autocomplete import models
from fuzzywuzzy import fuzz

cityNames = None

class CitySuggestion:
	def __init__(self,cityFile,delim):
		cities = self.getCitiesFromCSV(cityFile,delim)
		self.cityNames = self.fuzzyHashList(cities)
		self.trainModel(' '.join(self.cityNames.keys()))
	def fuzzyHashList(self,list):
		fuzzyList = {}
		for string in list:
			fuzzTags = self.getFuzzTags(string)
			for tag in fuzzTags:
				if not fuzzyList.get(tag,False):
					fuzzyList[tag] = []
				fuzzyList[tag].append(string)
		return fuzzyList
	def getFuzzTags(self,string):
		return re.sub(' +',' ',re.sub(r'[^\w]', ' ', string.strip())).lower().split(' ')
	def trainModel(self,string):
		print('Training autcomplete tool to look for cities from file specified...')
		models.train_models(string)
	def getCitiesFromCSV(self,cityFile,delim):
		reader = csv.DictReader(open(os.path.join(cityFile)),delimiter=delim)
		result = {}
		for row in reader:
			key = row['city'].lower()
			if key in result:
				pass
			result[key] = row
		return result
	def predictCity(self,string,threshold,newLocationDir,export=True):
		if not string: return None
		words = self.getFuzzTags(string)
		match = None
		score = 0
		autoCompleteCache = {}
		for word in words:
			searchWord = word[:4].strip().lower()
			if autoCompleteCache.get(searchWord,False):
				predictedWords = autoCompleteCache.get(searchWord,0)
			else:
				predictedWords = autocomplete.predict_currword(searchWord,top_n=10)
				autoCompleteCache[searchWord] = predictedWords
			for predictedWord in predictedWords:
				predictedCityNames = self.cityNames[predictedWord[0]]
				if not predictedCityNames:
					continue
				for candidate in predictedCityNames:
					newScore = fuzz.token_sort_ratio(string,candidate)
					if newScore > score:
						score = newScore
						match = candidate
		if export is True: f = open(os.path.join(newLocationDir,'no_match.txt'),'a+')
		if match is None:
			if export is True:
				f.write('{0},{1},"{2}"\n'.format(str(score),str(match),string))
				f.close()
			return False #No match
		if score >= threshold:
			print 'match:'+str(score)+'---'+str(match)+'---'+string
			return match
		else:
			if export is True: 
				f.write('{0},"{1}","{2}"\n'.format(str(score),str(match),string))
				f.close()
			return True #Not close enough match
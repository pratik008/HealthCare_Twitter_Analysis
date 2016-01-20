from city_from_location import *
from city_from_coordinate import *
import sys
import os

def main():
	if len(sys.argv) != 4:
		print("$ clean_city_file [tweetsJsonFile] [citiesFile] [destDir]")
		quit()
	print 'Finding cities names which match ones in the specified city file...'
	tweetsWithLocation = conformizeCities(sys.argv[1],sys.argv[2],sys.argv[3],True,80,'\t')
	while True:
		input = raw_input("Are results sufficient for you purpose? (y/n) ")
		if input == 'n':
			print 'Please select cities names to add from {0} to {1} for improve results.'.format(os.path.join(sys.argv[3],'no_match.txt'),sys.argv[2])
			quit()
		elif input == 'y': break
	print 'Using coordinates to find cities...'
	tweetsWithCoordinates = extractCitiesWithCoordinates(sys.argv[1],sys.argv[2],sys.argv[3])
	print 'Extracting relevant data using city names...'
	

if __name__ == "__main__":
	main()

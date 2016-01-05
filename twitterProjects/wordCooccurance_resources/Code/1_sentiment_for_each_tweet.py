import sys
import json

def main():
	afinnfile = open(sys.argv[1])
	tweet_file = open(sys.argv[2])
	scores = {}
	wdict ={}
	get = wdict.get
	for line in afinnfile:
		term, score  = line.split("\t")
		scores[term] = int(score)
		wdict[term] = get(term, 0) + 1

	for line in tweet_file:
		point = 0
		for word in line.split():
			if word in wdict:
				point += scores[word]
			else:
				point += 0
		print float(point)

if __name__ == '__main__':
    main()
import sys
import json

def main():
	afinnfile = open(sys.argv[1])
	theme_file = open(sys.argv[3])
	scores = {} 
	wdict ={}
	get = wdict.get
	for line in afinnfile:
			term, score  = line.split("\t") 
			scores[term] = int(score)
			wdict[term] = get(term, 0) + 1

	for line in theme_file:
		for word in line.split():
			point(word)

def point(t):
	afinnfile = open(sys.argv[1])
	tweet_file = open(sys.argv[2])
	scores = {}
	wdict ={}
	get = wdict.get
	for line in afinnfile:
			term, score  = line.split("\t")
			scores[term] = int(score)
			wdict[term] = get(term, 0) + 1
	tweet_file = open(sys.argv[2])
	count = 0
	for line in tweet_file:
		point = 0
		for word in line.split():
			if word == t:
				for word in line.split():
					if word in wdict:
						point += scores[word]
					else:
						point += 0
				count += point
	print t, count

if __name__ == '__main__':
    main()
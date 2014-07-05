import sys
import json

def main():
	keyword_file = open(sys.argv[1])
	for line in keyword_file:
			term, score  = line.split()
			point(term)

def point(t):
	keyword_file = open(sys.argv[1])
	tweet_file = open(sys.argv[2])
	scores = {}
	wdict ={}
	get = wdict.get
	for line in keyword_file:
			term, score  = line.split()
			scores[term] = int(score)
			wdict[term] = get(term, 0) + 1

	relation = {}
	get = relation.get
	for line in tweet_file:
		point = 0
		for word1 in line.split():
			if word1 == t:
				for word in line.split():
					if word in wdict:
						relation[word] = get(word, 0) + 1
	for term in relation:
		print t, term, relation[term]

if __name__ == '__main__':
    main()
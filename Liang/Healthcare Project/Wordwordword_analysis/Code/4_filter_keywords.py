import sys
import json

def main():
	afinnfile = open(sys.argv[1])
	for line in afinnfile:
		term, score  = line.split()
		if abs(int(score)) >= 100:
			print term, score

if __name__ == '__main__':
    main()
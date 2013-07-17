import sys
import json

###############################################################
# Author: Liang Tao
# Modified by: Longbo Qiao
# Original File Name: 4_filter_keywords.py
# Changed: output to a file, unify the input output file format
#
# filter keywords by its score
###############################################################
def main():
    stdScore = 10 # where you decide the filter score
    wordScore = open(filePath+'Theme_Score.txt')
    filteredScore = open(filePath +'Filtered_Theme_Score_by_'+str(stdScore)+'.txt','w')
    next(wordScore)
    filteredScore.write('Sentiment_Score^Word^Frequency')
    filteredScore.write('\n')
    for line in wordScore:
        score,term,freq  = line.split("^")
        if abs(int(score)) >= stdScore:
            print score, term, freq
            filteredScore.write(score+'^'+ term +'^'+ freq)

if __name__ == '__main__':
    filePath = 'processed/'
    main()
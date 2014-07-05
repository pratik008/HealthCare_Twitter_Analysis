import sys
import json
import operator

###############################################################
# Author: Liang Tao
# Modified by: Longbo Qiao
# Original File Name: 3_Theme_topic.py
# Changed: removed duplicated words, output to a file
#
# Appending each word in the document with its frequecy and
# its sentiment score
###############################################################
def main():
    wordsetdict = {}
    wordToSet=[]
    scoreTable = open(dictionaryfilePath+ dictionaryfileName)
    tweets_file = open(textfilePath+textfileName)
    scores = {}
    wdict ={}
    get = wdict.get
    for line in scoreTable:
            term, score  = line.split("\t")
            scores[term] = int(score)
            #wdict[term] = get(term, 0) + 1

    for line in tweets_file:
        for word in line.split():
            term = word
            wdict[term] = get(term,0) + 1
            wordsetdict[word] = point(word)
            wordToSet.append(word)
    themeScorefile = open(outputFilePath+ 'Theme_Score.txt','w')
    count = wdict.items()
    count.sort(key=operator.itemgetter(1),reverse=True)
    themeScorefile.write('Semtiment_Score^Word^Frequency')
    themeScorefile.write('\n')
    for i in range(len(count)):
        print wordsetdict[count[i][0]],count[i][0], count[i][1]
        inputline = str(wordsetdict[count[i][0]])+ '^' +str(count[i][0]) + '^' + str(count[i][1])
        themeScorefile.write(inputline)
        themeScorefile.write('\n')

def point(t):
    scoreTable = open(dictionaryfilePath+ dictionaryfileName)
    tweets_file = open(textfilePath+textfileName)
    scores = {}
    wdict ={}
    get = wdict.get
    for line in scoreTable:
            term, score  = line.split("\t")
            scores[term] = int(score)
            wdict[term] = get(term, 0) + 1
    #tweet_file = open(sys.argv[2])
    count = 0
    for line in tweets_file:
        point = 0
        for word in line.split():
            if word == t:
                for word in line.split():
                    if word in wdict:
                        point += scores[word]
                    else:
                        point += 0
                count += point
    return str(count)


if __name__ == '__main__':
    dictionaryfilePath = '../../Dictionaries/'
    dictionaryfileName = 'AFINN-111.txt'
    textfilePath = '../../Cleanup Scripts/processed/'
    textfileName = 'cleanedTweetsOnlyFull.txt'
    outputFilePath = 'processed/'
    main()

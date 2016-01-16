TWEET_ID_LEN = 18

def dumpAfinn(file):
    afinnPath = open(file)
    afinn = {}
    for line in afinnPath:
        a = line.split('\t')
        afinn[a[0]] = int(a[1])
    return afinn

def trimWord(word):
    if not word or "http" in word: return False
    word = word.translate(None,'.,/<>?[]{}!@$%^&*()_+-=\\\'\"|~`:;').lower()
    if not word or word.isdigit(): return False
    return word
    
def splitTweet(string):
    return string[TWEET_ID_LEN:].lstrip().split()

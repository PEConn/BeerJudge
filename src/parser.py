__author__ = 'michelleyeo'
from flask import Flask
import nltk
import TFIDF_thingy
import itertools
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

########## Functions ###########
def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist

def topn(n, list):
    if (n > len(list)):
        return list
    else:
        return list[0:n]

################################
TFIDF_thingy.init()

# Get the set of English stopwords from nltk
stop = stopwords.words('english')
stop.extend(["sauce", "side", "served", "english", "french", "italian", "mixed", "leaves", "baked", "toasted", "fried", "cooked", "spanish", "seasonal", "w"])
tokeniser = RegexpTokenizer(r'\w+')

# Tokenise and clean string, remove duplicates
testString = "Fried kimchi (pickled chinese cabbage) & pork w/ steamed tofu"
testString = testString.lower()
tokenisedString = tokeniser.tokenize(testString)
filtered_words = [w for w in tokenisedString if not w in stop]
uniqueFilteredWords = unique_list(filtered_words)

# Sort and get top n words
n = 3
wordList = []
for word in uniqueFilteredWords:
    if word in TFIDF_thingy.d:
        wordList.append((word, TFIDF_thingy.d[word]))
    else:
        wordList.append((word, 0))

wordList.sort(key=lambda tup: tup[1], reverse=True)
topWordList = topn(n, wordList)

# transform into string and pass to beer API
query = ""
for word in topWordList:
    query += " "
    query += word[0]
print(query)









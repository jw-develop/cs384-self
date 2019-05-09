#!/usr/bin/python
'''
Created on Nov 13, 2013

@author: tvandrun
'''

import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk import FreqDist
from nltk.corpus import wordnet as wn
from collections import Counter
import sys

# English stopwords
stopwords = nltk.corpus.stopwords.words('english')


# open the corpus
reader = PlaintextCorpusReader('.', '.*\.txt')
text = nltk.Text([x.lower() for x in nltk.Text(reader.words(sys.argv[1]))])
vocab = set(text)
freq_dist = FreqDist(text)

# suggested list of words to consider:
# words that aren't stop words, don't have any
# punctuation in them, occur more than 5 times,
# and aren't recognized by WordNet
interesting_words = [w for w in vocab if 
                     w not in stopwords and 
                     w.isalpha() and
                     freq_dist[w] > 5 and 
                     wn.synsets(w) == []]

# find the nearby words
nearbys = {}
for w in interesting_words :
    nearby = []

    # populate the nearby list for this word
    
    nearbys[w] = Counter(nearby)
    
# print the five most common nearbys for each interesting word
for w in interesting_words:
    print w
    for (x, y) in nearbys[w].most_common(5) :
        print x, y
    print "*****"
    



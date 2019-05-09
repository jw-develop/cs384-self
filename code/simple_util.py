import nltk

from nltk.corpus import PlaintextCorpusReader

def text_from_file(filename) :
    return nltk.Text(PlaintextCorpusReader('.', filename).words(filename))

def lexical_diversity(text) :
    return float(len(text)) / len(set([x.lower() for x in text]))

def hapaxes(text) :
    text_lower = [x.lower() for x in text]
    freq_dist = FreqDist(text_lower)
    return  [x for x in freq_dist.keys() if freq_dist[x] == 1]




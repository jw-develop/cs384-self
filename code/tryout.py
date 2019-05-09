# Initial demo of NLTK
# CSCI 384, Computational Linguistics
# Wheaton College
# Fall 2015

import nltk

from nltk.corpus import PlaintextCorpusReader

# PlaintextCorpusReader is a class. An instance of
# PlaintextCorpusReader knows a set of text files in a folder
# and is used to read those files.

children = PlaintextCorpusReader('.', '.*\.txt')


#  Sources in this folder:
#
# Frank L Baum:
#   The Emeral City of Oz; Glinda of Oz; Ozma of Oz; The Scarecrow of Oz;
#    Tik-Tok of Oz; The Tin Woodsman of Oz; The Wonderful Wizard of Oz
#
# Lewis Carroll:
#   Alice's Adventures in Wonderland; Alice through the Looking-glass
#
# Rudyard Kipling:
#   The Jungle Book; The Second Jungle Book; Just-So Stories; Kim;
#    Captains Corageous
#
# George MacDonald:
#   The Light Princess and Other Fairy Stories; The Princess and Curdie;
#    The Princess and the Goblin; Lilith; Phantastes

# Make a dict associating filenames with objects of
# nltk's Text class
children_texts = {a:nltk.Text(children.words(a))
                  for a in children.fileids()}

# Python dicts have a set of keys associated with them
children_texts.keys()

# Let's grab a specific text, Lewis Carroll's two books:

text_name = 'carroll-all.txt'

text = children_texts[text_name]

# text refers to an instance of nltk's Text class, which
# can be treated as a sequence (len, subscript, etc)

text[:100]

# How many words?
len(text)

# The "vocabulary" is the set of distinct types
vocab = set([x.lower() for x in text])

# Let's see the first 200 types (alphabetically)
sorted(vocab)[:200]

# lexical diversity; the average number of times each word occurs
float(len(text)) / len(vocab)

# The name is a little misleading. It would be better to call it
# "lexical diversity score", since a *lower score* means that
# the text is *more* lexically diverse.

# Compare to the lexical diversity of the other authors.
# Let's make this a function
def lexical_diversity(text) :
    return 10000.0 / len(set([x.lower() for x in text[:10000]]))

lexical_diversity(children_texts["baum-all.txt"])
lexical_diversity(children_texts["kipling-all.txt"])
lexical_diversity(children_texts["macdonald-all.txt"])

for x in sorted(children_texts.keys()) :
    print x, len(children_texts[x]), lexical_diversity(children_texts[x])
    
for x in sorted(children_texts.keys()) :
    print x, lexical_diversity(children_texts[x])
    
# Find contexts in which a type occurs
text.concordance('curious')

# Find types used similarly to a given type
text.similar('curious')

text.similar('alice')

# Find pairs (bigrams) that occur frequently
text.collocations()




# --- frequency distribution ---

from nltk import FreqDist

# convert to all lowercase
text_lower = [x.lower() for x in text]

#The frequency distribution itself is a dict (or a bag)
freq_dist = FreqDist(text_lower)

# Show the frequency of 100 arbitrary words
for x in freq_dist.keys()[:100] :
    print x, freq_dist[x]

# sort the keys by frequency (most frequent first), and then
# print the 100 most frequent
keys_by_freq = sorted(freq_dist.keys(), key=lambda x : freq_dist[x], reverse=True)

for x in keys_by_freq[:100] :
    print x, freq_dist[x]

# make frequency distributions for all the texts
freq_dists = {a:FreqDist([x.lower() for x in children_texts[a]])
                         for a in children.fileids()}

# Hapaxes (short for "hapax legomena", Greek for "[things] written once")
# are the types
hapaxes = [x for x in freq_dist.keys() if freq_dist[x] == 1]

# Make a function for hapaxes
def hapaxes(text) :
    text_lower = [x.lower() for x in text]
    freq_dist = FreqDist(text_lower)
    return  [x for x in freq_dist.keys() if freq_dist[x] == 1]

len(hapaxes(text))
len(hapaxes(children_texts["baum-all.txt"]))
len(hapaxes(children_texts["kipling-all.txt"]))
len(hapaxes(children_texts["macdonald-all.txt"]))


# How frequently do authors use 'and'?
# Is this frequency characteristic of an author?
for a in sorted(freq_dists.keys()) :
    print a, float(freq_dists[a]["and"])/len(children_texts[a])

def type_rate(w) :
    for a in sorted(freq_dists.keys()) :
        print a, (float(freq_dists[a][w])/len(children_texts[a])) * 100
    


for a in sorted(freq_dists.keys()) :
    print a, float(freq_dists[a]["and"])/freq_dists[a]["but"]

            
# POS tagging

# grab the first two sentences
sample = text[7:73]

# tag it
# (may need to download "averaged_perceptron_tagger"
nltk.pos_tag(sample)

# Give it something harder
nltk.pos_tag(["I", "rose", "to", "saw", "off", "the", "still", "rose", "that", "I", "saw", "still", "grew", "near", "the", "still"])


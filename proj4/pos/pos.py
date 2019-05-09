'''
Created on Aug 22, 2013

@author: tvandrun
'''


import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk import FreqDist

# 1. Load a (training) corpus.
# In the code below, the corpus will be
# referred to by variable all_text
all_text = []


# make the training text lowercase
all_text_lower = [x.lower() for x in all_text]
freq_dist = FreqDist(all_text_lower)

# make a reduced vocabulary
# In choosing a vocabulary size there is a trade-off.
# A larger vocabulary will in principle make for a more accurate
# tagger, but will be slower and will have a greater risk of underflow.
vocab_size = 500
vocab = sorted(freq_dist.keys(), key=lambda x : freq_dist[x], reverse=True)[:vocab_size]
# "***" is for all out-of-vocabulary types
vocab = vocab + ["***"]




# 2. Make a reduced form of the PennTB tagset
penntb_to_reduced = {}
# noun-like
for x in ['NN', 'NNS', 'NNP', 'NNPS', 'PRP', 'EX', 'WP'] :
    penntb_to_reduced[x] = 'N'
# verb-like
for x in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'MD', 'TO'] :
    penntb_to_reduced[x] = 'V'
# adjective-like
for x in ['POS', 'PRP$', 'WP$', 'JJ', 'JJR', 'JJS', 'DT', 'CD', 'PDT', 'WDT', 'LS']:
    penntb_to_reduced[x] = 'AJ'
# adverb-like
for x in ['RB', 'RBR', 'RBS', 'WRB', 'RP', 'IN', 'CC']:
    penntb_to_reduced[x] = 'AV'
# interjections
for x in ['FW', 'UH'] :
    penntb_to_reduced[x] = 'I'
# symbols
for x in ['SYM', '$', '#'] :
    penntb_to_reduced[x] = 'S'
# groupings
for x in ['\'\'', '(', ')', ',', ':', '``'] :
    penntb_to_reduced[x] = 'G'
# end-of-sentence symbols
penntb_to_reduced['.'] = 'E'

reduced_tags = ['N', 'V', 'AJ', 'AV', 'I', 'S', 'G', 'E']

# 3. tag the corpus
all_tagged = nltk.pos_tag(all_text)

# 4. make the probability matrices

# a tally from types to tags; a tally from tags to next tags
word_tag_tally = {y:{x:0 for x in reduced_tags} for y in vocab}
tag_transition_tally = {y:{x:0 for x in reduced_tags} for y in reduced_tags}

previous_tag = 'E' # "ending" will be the dummy initial tag
for (word, tag) in all_tagged :
    word = word.lower()

    # fill this out:
        # For most tags, you want to convert it to the reduced tag
        # For most tags and words, update the tag transition tally
        # and the word-tag tally
        # But what if the tag is '-NONE-'?
        # What if the word is not in the vocabulary?
 


# now, make the actual transition probability matrices 
trans_probs = {}
for tg1 in reduced_tags :
    pass
    # fill this out:
        # For each tag tg1 compute the probabilities for transitioning to
        # each tag (say, tg2). Using relative frequency estimation,
        # that would mean dividing the number of times tg2 follows tg1 by
        # the absolute number of times t1 occurs. (But, what if tg1 never occurs..?)
        # Recommendation: think in terms of "for each tg2, how many times had
        # we transitioned from tg1?"


# similarly for the emission (observation) probabilities
emit_probs = {}
for tg in reduced_tags :
    pass
    # fill this out:
        # For each tag tg1 compute the probabilities for emitting each word v.
        # Recommendation: think in terms of "for each word v, how many times
        # did tg1 emit v?"
    

# 5. implement Viterbi. 
# Write a function that takes a sequence of tokens,
# a matrix of transition probs, a matrix of emit probs,
# a vocabulary, a set of tags, and the starting tag

def pos_tagging(sequence, trans_probs, emit_probs, vocab, tags, start) :

    # fill this out

    tagged = []

        
    return tagged

# 6. try it out: run the algorithm on the test data
test_sample = []
test_tagged = pos_tagging(test_sample, trans_probs, emit_probs, vocab, reduced_tags, 'E')            
print test_tagged

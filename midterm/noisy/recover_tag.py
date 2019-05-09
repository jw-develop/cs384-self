##################
#
#
#      Your task in Problem 1 is to complete the function stub
#      found at the end of this file
#
#
##################


import nltk
from nltk import FreqDist

source_file = open('training-tagged.txt', 'r')

#############  You may find some of the following useful ############

# messages is a ist of all messages and their hashes tags
# Each item in messages is a tuple.
# The first thing in each tuple is a list of the tokens
# in the message (no hash symbol),
# the second thing in each tuple is the hash tag
# of that message.
#
# example:
# messages[3] = (['a', 'slack', 'hand', 'causes', 'poverty', 'but', 'the', 'hand', 'of',
#                 'the', 'diligent', 'makes', 'rich'], 'poverty')

messages = []

for line in source_file :
    line = line.strip()
    if len(line) == 0 :
        continue
    message = []
    for w in line.split(' ') :
        if w[0] == '#' :
            message.append(w[1:])
            tag = w[1:]
        else:
            message.append(w)
    messages.append((message, tag))

# hash_occurrences is a dict from hash tags to the number of messages
# in which that hash occurs. Its keys can be used as a list of all hash tags.

hash_occurrences = {h: sum([1 for (mm, hh) in messages if h == hh]) for (m,h) in messages}


# hash_tokens is a dict from hash tags to a list of all tokens in all
# messages with that hash tag

hash_tokens = {}

for m in messages:
    h = m[1]
    if h not in hash_tokens:
        hash_tokens[h] = []
    for w in m[0] :
        hash_tokens[h].append(w)

# total_freqs is a dict from hash tags to the total number of words
# in all messages with that tag

total_freqs = {h:len(hash_tokens[h]) for h in hash_tokens}

# fds is a dict from hash tags to frequency distributions of
# words in messages with that tag

fds = {h:FreqDist(hash_tokens[h]) for h in hash_tokens}
    
########### End given utility stuff ##################



# ----- Write this function -------

def recover_tag(message) :
    return None

    
    

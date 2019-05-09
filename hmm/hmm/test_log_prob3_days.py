'''
Created on Oct 27, 2015

@author: thomasvandrunen
'''

from hmm_log import Trained_HMM
import math

observation = ["0", "0", "1", "0", "1", "0", "0", #Aug 24-30
               "1", "0", "1", "0", "1", "0", "0", #Aug 31-Sept 6
               "0", "0", "1", "0", "1", "0", "0", #Sept 7-13
               "1", "0", "1", "0", "1", "0", "0", #Sept 14-20
               "1", "0", "1", "0", "1", "0", "0", #Sept 21-27
               "1", "0", "1", "0", "1", "0", "0", #Sept 28-Oct 4
               "1", "0", "1", "0", "1", "0", "0", #Oct 5-11
               "1", "0", "1", "0", "1", "0", "0", #Oct 12-18
               "0", "0", "1", "0", "1", "0", "0", #Oct 19-25
               "1", "0", "1", "0", "1", "0", "0", #Oct 26-Nov 1
               "1", "0", "1", "0", "1", "0", "0", #Nov 2-8
               "1", "0", "1", "0", "1", "0", "0", #Nov 9-15
               "1", "0", "1", "0", "1", "0", "0", #Nov 16-22
               "1", "0", "0", "0", "0", "0", "0", #Nov 23-29
               "1", "0", "1", "0", "1", "0", "0", #Nov 30-Dec 6
               "1", "0", "1", "0", "1", "0", "0", #Dec 7-13
               ]
num_states = 7
#num_states = 2

trained_model = Trained_HMM(observation, ["0", "1"], num_states)

# print the trained model's probabilities
print "a:"
for i in range(num_states):
    for j in range(num_states) :
        print("\t%.2f" % trained_model.trans_probs[i][j]),
    print ""
print "b:"
for i in range(num_states) :
    for k in range(2) :
        print("\t%.2f" % trained_model.obs_probs[i][k]),
    print ""

# compute the observation's probability according to the
# model trained on it (NOT a good way to test a model, of course
# but useful for demonstration/debugging)
prob =  trained_model.prob_observations(observation)
perplexity = math.pow(prob, - (1.0/len(observation)))
print "Probability and perplexity by the trained model"
print prob, perplexity


'''
Created on Oct 27, 2015

@author: tvandrun
'''

from hmm_log import HMM, Trained_HMM
import math

# Make a model using chosen probabilities
#fiat_model = HMM(["S", "M", "L"], [[0.9, 0.1],[0.2, 0.8]], [[0.1, 0.1, 0.8],[0.75, 0.2, 0.05]], 
#            [0.6, 0.4])
fiat_model = HMM(["S", "M", "L"], [[0.7, 0.3],[0.4, 0.6]], [[0.1, 0.4, 0.5],[0.7, 0.2, 0.1]], 
            [0.6, 0.4])


# Generate an observation by simulation
train_text =  fiat_model.simulate(5000)

#print "Observation (from simulation):"
#print train_text

# compute the observation's probability according to the
# model that generated it

#prob =  fiat_model.prob_observations(train_text)
#perplexity = math.pow(prob, - (1.0/len(train_text)))
#print "Probability and perplexity by the generating model"
#print prob, perplexity

# train a new model
trained_model = Trained_HMM(train_text, ["S", "M", "L"], 2)

# print the trained model's probabilities
print "pi:"
print trained_model.init_state_probs
print "a:"
print trained_model.trans_probs
print "b:"
print trained_model.obs_probs

# compute the observation's probability according to the
# model trained on it (NOT a good way to test a model, of course
# but useful for demonstration/debugging)

#prob =  trained_model.prob_observations(train_text)
#perplexity = math.pow(prob, - (1.0/len(train_text)))
#print "Probability and perplexity by the trained model"
#print prob, perplexity



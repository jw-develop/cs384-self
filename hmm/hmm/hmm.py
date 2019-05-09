'''
Created on Oct 15, 2015

Implementation of a generalized Hidden Markov Model

@author: tvandrun
'''


import random

# ---------------- Utilities ----------------


# Given a discrete distribution as a list of probabilities
# (for example, if distribution[i] = p, then i occurs with
# probability p), generate a random value, represented as
# an index into this list, based on this distribution
def find_random(distribution):
    x = random.random()
    i = 0
    s = 0.0
    while True :
        s += distribution[i]
        if x < s or i == len(distribution) - 1:
            break
        i += 1
    return i

# Given a list, find the max value and its index
def max_argmax(xx):
    # max is predefined in python :(
    maxx = xx[0]
    argmax = 0
    for i in range(1, len(xx)) :
        x = xx[i]
        if x > maxx :
            maxx = x
            argmax = i
    return (maxx, argmax)
    
# Given a list, find the index of the max value
def argmax(xx) :
    return max_argmax(xx)[1]
 
# Are observations known by their actual symbol or by their index?
# obs_syms is a list of actual symbols, with their canonical index
# being where that symbol is found in obs_syms

# Class to model Hidden Markov Models
class HMM :
    def __init__(self, obs_syms, trans_probs, obs_probs, init_state_probs):
        M = len(obs_syms)
        N = len(trans_probs)
        for row in trans_probs :
            assert len(row) == N
        assert len(obs_probs) == N
        for row in obs_probs :
            assert len(row) == M
        assert len(init_state_probs) == N       
        self.obs_syms = obs_syms
        self.trans_probs = trans_probs
        self.obs_probs = obs_probs
        self.init_state_probs = init_state_probs
        # "observation symbols reversed", which lets us look up the
        # index for an observation symbol.
        self.obs_syms_rev = {obs_syms[i]:i for i in range(len(obs_syms))}
        
    # Emit a sequence of symbols by simulating a sequence of state
    # based on the probabilities of this model    
    def simulate(self, T):
        state = find_random(self.init_state_probs)
        observations = []
        while T > 0 :
            observations.append(self.obs_syms[find_random(self.obs_probs[state])])
            state = find_random(self.trans_probs[state])
            T -= 1
        return observations
    
    # Emit a sequence of symbols together with the states emitting them,
    # simulated based on the probabilities of this model
    def simulate_tagged(self, T):
        state = find_random(self.init_state_probs)
        observations = []
        while T > 0 :
            observations.append((self.obs_syms[find_random(self.obs_probs[state])], state))
            state = find_random(self.trans_probs[state])
            T -= 1
        return observations

    # Retrieve the probability of transitioning from state i to state j,
    # here for notational convenience
    def a(self, i, j):
        return self.trans_probs[i][j]
    
    # Retrieve the probability of emitting an observation symbol when in state i,
    # here for notational convenience.
    # obs can be either a symbol itself or an index into the list of symbols
    def b(self, i, obs):
        # the variable v is unused, appearing only for clarity
        if isinstance(obs, int) :
            j = obs
            v = self.obs_symbs[j]
        else :
            v = obs
            j = self.obs_syms_rev[v]
        return self.obs_probs[i][j]

    # Retrieve the probability of starting in state i,
    # here for notational convenience.
    def pi(self, i):
        return self.init_state_probs[i]

    # compute the probability of an observation sequence (Problem 1; the Forward algorithm)
    def prob_observations(self, obs_seq):
        N = len(self.init_state_probs)
        T = len(obs_seq)
        alphas = self.forward_alphas(obs_seq)
        return sum([alphas[T-1][i] for i in range(N)])
 
    def forward_alphas(self, obs_seq):
        N = len(self.init_state_probs)
        T = len(obs_seq)
        alphas = [[0 for i in range(N)] for t in range(T)]

        # compute the left column
        for i in range(N) :
            alphas[0][i] = self.pi(i) * self.b(i, obs_seq[0])

        # fill in the other columns
        for t in range(1, T) :
            o_t = obs_seq[t]
            for i in range(N) :
                alphas[t][i] = (sum([alphas[t-1][j]*self.a(j, i) for j in range(N)]) 
                                * self.b(i, o_t))
        return alphas
    
    def prob_observations_alt(self, obs_seq):
        N = len(self.init_state_probs)
        T = len(obs_seq)
        betas = self.backward_betas(obs_seq)
        o_0 = obs_seq[0]
        return sum([self.pi(i) * betas[0][i] * self.b(i, o_0) for i in range(N)])

    def backward_betas(self, obs_seq):
        N = len(self.init_state_probs)
        T = len(obs_seq)
      
        betas = [[0 for i in range(N)] for t in range(T)]
        
        for i in range(N) :
            betas[T-1][i] = 1
        
        for t in reversed(range(T-1)) :
            o_tp = obs_seq[t+1]  # observation at time t+1
            for i in range(N) :
                betas[t][i] = sum([self.a(i,j) * betas[t+1][j] * self.b(j, o_tp) for j in range(N)])
                               
        
        return betas
    
    
        
        


# The so-called problem 0
# Assume data is formatted as a list of lists of observation, state tuples
def MLE_HMM_from_known_states(obs_syms, num_states, data):
    init_counts = [1 for i in range(num_states)]
    emission_counts = [{sym:1 for sym in obs_syms} for i in range(num_states)]
    transition_counts = [[1 for j in range(num_states)] for i in range(num_states)]
    state_counts = [1 for i in range(num_states)]
    for obs_seq in data :
        state = obs_seq[0][1]        
        init_counts[state] += 1
        emission_counts[state][obs_seq[0][0]] += 1
        for (obs, next_state) in obs_seq[1:] :
            transition_counts[state][next_state] += 1
            emission_counts[next_state][obs] += 1
            state_counts[next_state] += 1
            state = next_state
    init_probs = [float(init_counts[i])/len(data) for i in range(num_states)]
    transition_probs = [[float(transition_counts[i][j])/state_counts[i] for j in range(num_states)]
                        for i in range(num_states)]

    emission_probs = [[float(emission_counts[i][obs_syms[j]])/state_counts[i] 
                       for j in range(len(obs_syms))]
                      for i in range(num_states)]

    # the next line is an alternate way to have done this, if we stored emission
    # probabilities as dicts from symbols to probabilities
    #emission_probs = [{v:float(emission_counts[i][v])/state_counts[i] for v in obs_syms}
    #                   for i in range(num_states)]

    return HMM(obs_syms, transition_probs, emission_probs, init_probs)

class Trained_HMM(HMM):
    
    def __init__(self, train_seq, obs_syms, num_states):
        self.train_seq = train_seq
        N = num_states
        M = len(obs_syms)
        T = len(train_seq)
        # make random initial pi, a, and b
        pi = [1.0 for i in range(N)]
        for i in range(5) :
            pi[random.randint(0,N-1)] += 1
        for i in range(N) :
            pi[i] /= (N+5)
        a = [[1.0 for j in range(N)] for i in range(N)]
        for i in range(N) :
            for j in range(5) :
                a[i][random.randint(0, N-1)] += 1
            for j in range(N) :
                a[i][j] /= (N+5)
        b = [[1.0 for j in range(M)] for i in range(N)]
        for i in range(N) :
            for j in range(5) :
                b[i][random.randint(0, M-1)] += 1
            for j in range(M) :
                b[i][j] /= (M+5)
       
        HMM.__init__(self, obs_syms, a, b, pi)
        
        self.train()

    def train(self):
        N = len(self.init_state_probs)
        M = len(self.obs_syms)
        T = len(self.train_seq)
        
        alphas = self.forward_alphas(self.train_seq)
        old_likelihood = sum([alphas[T-1][i] for i in range(N)])
        
        print old_likelihood

        print "original like", old_likelihood

        epsilon = .0001

        
        while True :
            xis = self.forward_backward_xis(alphas)
            gammas = [[sum([xis[t][i][j] for j in range(N)])
                       for i in range(N)]
                      for t in range(T-1)]
            gamma_sums = [sum([gammas[t][i] for t in range(T-1)]) for i in range(N)]
            
            pi = [gammas[0][i] for i in range(N)]
            a = [[sum([xis[t][i][j]/gamma_sums[i] for t in range(T-1)])
                  for j in range(N)]
                 for i in range(N)]
            b = [[sum([gammas[t][j]/gamma_sums[j] for t in range(T-1) 
                       if self.train_seq[t] == self.obs_syms[k]])
                  for k in range(M)]
                 for j in range(N)]
            
            self.init_state_probs = pi
            self.trans_probs = a
            self.obs_probs = b
            
            alphas = self.forward_alphas(self.train_seq)
            new_likelihood = sum([alphas[T-1][i] for i in range(N)])
            if new_likelihood - old_likelihood < epsilon :
                break
            print "new like", new_likelihood, (new_likelihood - old_likelihood)
            old_likelihood = new_likelihood
        
        
    def forward_backward_xis(self, alphas):
        N = len(self.init_state_probs)
        T = len(self.train_seq)
        betas = self.backward_betas(self.train_seq)
        xi_numerators = [[[alphas[t][i] * self.a(i, j) * self.b(j, self.train_seq[t+1]) * betas[t+1][j] 
                           for j in range(N)] 
                          for i in range(N)] 
                         for t in range(T-1)]
        # The xi denominators are the same for every t.
        xi_denom = sum([sum([xi_numerators[0][i][j] for j in range(N)]) for i in range(N)])

        xis = [[[xi_numerators[t][i][j]/xi_denom
                 for j in range(N)] 
                for i in range(N)]
               for t in range(T-1)]
        
        return xis
   

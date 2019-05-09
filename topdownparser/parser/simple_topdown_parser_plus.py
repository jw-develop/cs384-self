'''
Created on Nov 16, 2015

@author: tvandrun
'''

from nltk.corpus import wordnet as wn
import sys

# Exception to be thrown if an unexpected token is found
# during a parse
class ParseException(Exception):
    def __init__(self, expected, found):
        self.expected = expected
        self.found = found
        
    def __str__(self):
        return "Cannot parse. Found " + self.found + ", expected " + self.expected

id_gen = 0

class Nonterminal:
    def __init__(self, label, children) :
        global id_gen
        self.id = "x" + str(id_gen)
        id_gen += 1
        self.label = label
        self.children = children

    def print_tree(self) :
        print self.id + ' [label = "' + self.label + '"];'
        for child in self.children :
            print self.id + ' -> ' + child.id + ';'
            child.print_tree()

class LastStopNonterminal :
    def __init__(self, label, token) :
        global id_gen
        self.id = "x" + str(id_gen)
        id_gen += 1
        self.label = label
        self.token = token

    def print_tree(self) :
        print self.id + ' [style=bold, label = "' + self.label +':' + self.token + '"];'




# We check for articles and prepositions directly from a list

articles = ['the', 'a', 'an']
preps = [x.strip() for x in open("preps").readlines()]

# For other parts of speech, we use WordNet

# Map to convert WordNet pos tags to our pos abbreviations
# The POS 's' means "satellite adjective" (whatever that is) in WordNet
pos_map = {'n':'Noun', 'v':'Verb', 'a':'Adj', 's':'Adj', 'r':'Adv'}

# Class that acts as a parser. The only conceptual public
# method is sentence(), which, given a sentence as a list of
# tokens, returns a parse tree, or throws a ParseException.
# The sentence method sets the list of sentence tokens and calls
# other methods which read (and remove) from that list.
class SimpleTopDown:
    
    # Parse a "last stop" nonterminal from the sentence tokens
    # A "last stop nonterminal" is a nonterminal that expands
    # into a single terminal; basically a POS.         
    def last_stop_NT(self, pos):
        if len(self.sentence_toks) == 0:
            raise ParseException(pos, 'END')
        tok = self.sentence_toks[0]
        self.sentence_toks = self.sentence_toks[1:]
        if pos == 'Art':
            if tok in articles :
                return LastStopNonterminal('Art', tok)
            else :
                raise ParseException('Art', tok)
        elif pos == 'Prep':
            if tok in preps :
                return LastStopNonterminal('Prep', tok)
            else :
                raise ParseException('Prep', tok)
        else :
            if self.is_pos(tok, pos) :
                return LastStopNonterminal(pos, tok)
            raise ParseException(pos, tok)

    def is_pos(self, tok, pos) :
        for sysnet in wn.synsets(tok) :
                if pos_map[sysnet.pos()] == pos :
                    return True
        return False

    # Parse a sentence given as a list of tokens    
    def sentence(self, sentence_toks):
        self.sentence_toks = sentence_toks
        return Nonterminal("Sentence", [self.noun_phrase(), self.verb_phrase()])

    # Parse a noun phrase from the list of tokens.
    # Precondition: We expect that a prefix of what's left on the token sequence
    # constitutes a noun phrase.
    # Postcondition: We have removed the tokens comprised by the noun phrase
    # from the token sequence
    def noun_phrase(self):
        return Nonterminal("NounPhrase", [self.article(), self.adj_seq(), self.noun()])

    # The other parsing functions have pre/post conditions analogous to
    # that of noun_phrase()

    def article(self):
        return self.last_stop_NT('Art')

    def adjective(self):
        return self.last_stop_NT('Adj')
    
    def noun(self):
        return self.last_stop_NT('Noun')

    def verb_phrase(self):
        return Nonterminal("VerbPhrase", [self.adv_opt(), self.verb(), self.noun_phrase(), self.prep_phrase()])

    def verb(self) :
        return self.last_stop_NT('Verb')

    def prep_phrase(self) :
        return Nonterminal('PrepPhrase', [self.prep(), self.noun_phrase()])

    def prep(self) :
        return self.last_stop_NT('Prep')

    def adj_seq(self) :
        if self.is_pos(self.sentence_toks[0], "Adj"):
            return Nonterminal("AdjSeq", [self.adjective(), self.adj_seq()])
        else :
             return Nonterminal("AdjSeq", [])
            
    def adv_opt(self) :
        if self.is_pos(self.sentence_toks[0], "Adv") :
            return Nonterminal("AdvOpt", [self.adverb()])
        else:
            return Nonterminal("AdvOpt", [])
            
    def adverb(self) :
        return self.last_stop_NT('Adv')

# Read a sentence from the commandline, tokenize it, make a parser,
# and (try to) parse the tokens as a sentence.

sentence_text = sys.argv[1]
sentence_toks = sentence_text.split()
parser = SimpleTopDown()
print 'digraph G {'
parser.sentence(sentence_toks).print_tree()
print '}'

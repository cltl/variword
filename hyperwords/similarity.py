'''
Created on Nov 17, 2014

@author: Minh Ngoc Le
'''
import logging
import math

from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import WordNetError
from math import exp
import numpy as np

_log = logging.getLogger('kbcomplete.similarity')
        

def _safe_apply(sims, func):
    sims = [s for s in sims if s is not None and not math.isnan(s)]
    if sims:
        return func(sims)
    else:
        return float('nan')
        

class LemmaPos2WordNetAdapter():
    
    def __init__(self, sim_func, aggregate_func=max):
        self.sim_func = sim_func
        self.aggregate_func = aggregate_func
        

    def __call__(self, w1, w2):
        lemma1, pos1 = w1
        lemma2, pos2 = w2
        sims = [self.sim_func(s1, s2) for s1 in wn.synsets(lemma1, pos1)
                                      for s2 in wn.synsets(lemma2, pos2)]
        return _safe_apply(sims, self.aggregate_func)


class LemmaPos2LemmaAdapter():
    
    def __init__(self, sim_func, aggregate_func=max):
        self.sim_func = sim_func
        self.aggregate_func = aggregate_func
        

    def __call__(self, w1, w2):
        lemma1, _ = w1
        lemma2, _ = w2
        return self.sim_func(lemma1, lemma2)


class Text2WordNetAdapter():
    
    def __init__(self, sim_func, aggregate_func=max):
        self.sim_func = sim_func
        self.aggregate_func = aggregate_func
        

    def __call__(self, w1, w2):
        sims = [self.sim_func(s1, s2) for s1 in wn.synsets(w1)
                                      for s2 in wn.synsets(w2)]
        return _safe_apply(sims, self.aggregate_func)


class DynamicAverageSimilarity(object):
    
    def __init__(self, sim_funcs, weights=None):
        assert isinstance(sim_funcs, (list, tuple))
        assert len(sim_funcs) > 0
        if not weights:
            weights = [1]*len(sim_funcs)
        self.sim_funcs = sim_funcs
        self.weights = weights


    def __call__(self, a, b):
        numerator = 0 
        denominator = 0
        for i in range(len(self.sim_funcs)):
            sim = self.sim_funcs[i](a, b)
            if sim is not None and not math.isnan(sim):
                numerator += sim * self.weights[i]
                denominator += self.weights[i]
        if denominator <= 0: return float('nan')
        return numerator / denominator


class WeightedSumSimilarity(object):
    
    def __init__(self, sim_funcs, weights=None):
        assert isinstance(sim_funcs, (list, tuple))
        assert len(sim_funcs) >= 1
        self.sim_funcs = sim_funcs
        if not weights:
            weights = np.ones(len(sim_funcs))
        else:
            assert len(sim_funcs) == len(weights)
            weights = np.asarray(weights)
        self.weights = weights / np.linalg.norm(weights)


    def __call__(self, a, b):
        sims = np.zeros(len(self.sim_funcs), 'float')
        for i in range(len(self.sim_funcs)):
            sims[i] = self.sim_funcs[i](a, b) or 0
        return np.dot(np.nan_to_num(sims), self.weights)


class SimilarityPool(object):
    
    def __init__(self, sim_funcs, aggregate_func=max):
        assert isinstance(sim_funcs, (list, tuple))
        assert len(sim_funcs) > 0
        self.sim_funcs = sim_funcs
        self.aggregate_func = aggregate_func


    def __call__(self, a, b):
        sims = [f(a, b) for f in self.sim_funcs]
        return self.aggregate_func(sims)


def antonyms(s):
    a = set()
    for l in s.lemmas():
        a.update(ant.synset() for ant in l.antonyms())
    return a


def wup_similarity(s1, s2):
    """
    Fix the broken version of NLTK I have on server.
    """
    if s1 == s2:
        return 1.0
    p1 = s1.pos().replace('s', 'a')
    p2 = s2.pos().replace('s', 'a')
    if p1 != p2:
        return 0
    return wn.wup_similarity(s1, s2)


def lch_similarity(s1, s2):
    """
    Allow calls on different parts of speech.
    """
    try:
        return wn.lch_similarity(s1, s2)
    except WordNetError:
        return None
    except ZeroDivisionError:
        return None
    
    
def lch_similarity_scaled(s1, s2):
    lch = lch_similarity(s1, s2)
    if lch is not None:
        lch = 1-exp(-lch)
    return lch
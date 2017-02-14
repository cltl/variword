'''
Created on Apr 24, 2015

@author: Minh Ngoc Le
'''

import numpy as np
from collections import defaultdict
import sys
import docopt
from representations.representation_factory import create_representation

def choice_with_replacement(group, k):
    indices = np.random.randint(len(group), size=(k,))
    return np.asarray(group)[indices]


def score_with_tie_correction(ab_pred, xy_pred, ab_gold, xy_gold):
    ''' 
    Score a similarity measure against a gold standard on the comparison of
    pairs of pairs (a,b) and (x,y) 
    '''
    g = np.sign(ab_gold-xy_gold)
    p = np.sign(ab_pred-xy_pred)
    if g == 0 or p == 0: return 0.5
    if g == p: return 1
    return 0


def score_naive(ab_pred, xy_pred, ab_gold, xy_gold):
    ''' 
    Score a similarity measure against a gold standard on the comparison of
    pairs of pairs (a,b) and (x,y) 
    '''
    g = np.sign(ab_gold-xy_gold)
    p = np.sign(ab_pred-xy_pred)
    return g == p


def accuracy(gold, predicted, score_func=score_with_tie_correction):
    '''
    Accept two lists of similarity scores and output ordering accuracy.
    There are two possible scoring functions, see "score_naive" and
    "score_with_tie_correction".
    '''
    n = len(gold)
    assert n == len(predicted)
    correct = 0
    count = 0
    for i in xrange(n):
        for j in xrange(n):
            if predicted[i] is None or predicted[j] is None: continue
            correct += score_func(predicted[i], predicted[j], gold[i], gold[j])
            count += 1
    return float(correct)/count, count
            

def accuracy_by_group(gold, predicted, group_indices, 
                      score_func=score_with_tie_correction):
    '''
    Accept two lists of similarity scores and a list of group indices.
    Returns two elements: 
    - a Numpy matrix of component scores, cell [i,j] corresponds to pairs with
      one element in group i and the other in group j  
    - a Numpy matrix of component weights, i.e. the number of comparisons 
      corresponding to each component score
    '''
    groups = defaultdict(list)
    for i, g, s in zip(group_indices, gold, predicted):
        if s is None: continue
        groups[i].append((g, s))
    n = max(groups.keys())+1
    correct = np.zeros((n, n), dtype=float)
    count = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            count[i,j] = len(groups[i])*len(groups[j])
            for ab in groups[i]:
                for xy in groups[j]:
                    correct[i,j] += score_func(ab[1], xy[1], ab[0], xy[0])
    return correct/count, count

if __name__ == '__main__':
    args = docopt("""
    Usage:
        ordering.py [options] <representation> <representation_path>

    Options:
        --score_func    The scoring function (naive or tie)
    """)
    func_name = args['--score_func']
    if func_name == 'tie':
        score_func = score_with_tie_correction
    elif func_name == 'naive':
        score_func = score_naive
    representation = create_representation(args)
    accura
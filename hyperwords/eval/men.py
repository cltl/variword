'''
Created on Dec 18, 2014

@author: Minh Ngoc Le
'''
import os
import re
import sys

from nltk.corpus import wordnet as wn
from eval import _safe_spearmanr 
from collections import defaultdict
assert wn.get_version() == '3.0'

_home_dir = os.path.dirname(__file__)
_data_path = os.path.join(_home_dir, 'MEN_dataset_lemma_form_%s')

dataset_name="full"
data = None
data_by_pos = None

def _parse_lemma(l):
    m = re.match('(\\w+)-(\\w)', l)
    lemma = m.group(1)
    pos = m.group(2)
    pos = pos.replace('j', 'a')
    return (lemma, pos)


def read_data(dataset_name):
    if dataset_name not in ('dev', 'test', 'full'):
        raise ValueError('Unknown dataset name: %s' %dataset_name)
    path = _data_path %dataset_name
    with open(path) as f:
        sys.stderr.write('Reading MEN dataset from %s... ' %path)
        fields = (line.strip().split(' ') for line in f)
        data = [(_parse_lemma(s1), _parse_lemma(s2), float(score)) 
                for s1, s2, score in fields]
        sys.stderr.write('Done\n')
    return data


def _evalute_on_dataset(sim, data):
    _, _, gold = zip(*data)
    sims = [sim(l1, l2) for l1, l2, _ in data]
    return _safe_spearmanr(sims, gold) 
    
    
def _divide_by_pos(data):
    ret = defaultdict(list)
    for l1, l2, s in data:
        code = '+'.join(sorted([l1[1], l2[1]]))
        ret[code].append((l1, l2, s))
    return ret

    
def _init(dn):
    global data, data_by_pos, dataset_name
    if dataset_name == dn and data and data_by_pos:
        return
    dataset_name = dn
    data = read_data(dataset_name)
    data_by_pos = _divide_by_pos(data)

    
def evaluate_and_print(sim, dataset_name="full", verbose=False):
    _init(dataset_name)
    ret = ([('all',) + _evalute_on_dataset(sim, data)] +
            [(code,) + _evalute_on_dataset(sim, data_by_pos[code]) 
             for code in sorted(data_by_pos)])
    print
    print "Spearman's correlation with MEN:"
    print '\n'.join('%s\t%.4f\t(%d pairs)' %row for row in ret)
    if verbose:
        b1s, b2s, scores = zip(*data)
        sims = [sim(l1, l2) for l1, l2, _ in data]
        print "\n".join("%s\t%s\t%f\t%f" %x 
                        for x in zip(b1s, b2s, sims, scores))

    
def _filter_data_by_pos(data, pos):    
    return [dp for dp in data if '+'.join((dp[0][1], dp[1][1])) in pos]


def evaluate_and_print_nv(sim, dataset_name="full", verbose=False):
    _init(dataset_name)
    data_nv = _filter_data_by_pos(data, ('n+n', 'v+v'))
    ret = ([('nv',) + _evalute_on_dataset(sim, data_nv)] +
            [(code,) + _evalute_on_dataset(sim, data_by_pos[code]) 
             for code in sorted(('n+n', 'v+v'))])
    print
    print "Spearman's correlation with MEN(nv):"
    print '\n'.join('%s\t%.4f\t(%d pairs)' %row for row in ret)
    if verbose:
        b1s, b2s, scores = zip(*data)
        sims = [sim(l1, l2) for l1, l2, _ in data]
        print "\n".join("%s\t%s\t%f\t%f" %x 
                        for x in zip(b1s, b2s, sims, scores))


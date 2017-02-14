'''
Created on Dec 18, 2014

@author: Minh Ngoc Le
'''
import os
import sys

from nltk.corpus import wordnet as wn
from eval import _safe_spearmanr

assert wn.get_version() == '3.0'

_home_dir = os.path.dirname(__file__)
_data_path = os.path.join(_home_dir, 'wordsim353_%s.tab')

def read_data(dataset_name):
    if dataset_name not in ('combined', 'set1', 'set2'):
        raise ValueError('Unknown dataset name: %s' %dataset_name)
    path = _data_path %dataset_name
    with open(path) as f:
        sys.stderr.write('Reading WordSim-353 dataset from %s... ' %path)
        f.readline() # skip headdings
        fields = (line.strip().split('\t') for line in f)
        data = [(fs[0], fs[1], float(fs[2])) for fs in fields]
        sys.stderr.write('Done\n')
    return data

dataset_name = None
data = None

def _init(dn):
    global dataset_name, data
    if dn == dataset_name and data:
        return
    dataset_name = dn
    data = read_data(dataset_name)


def evaluate_and_print(sim, dataset_name="combined", verbose=False):
    """
    Call sim on pairs of lemmas. Compute Spearman's correlation with 
    gold standard.
    """
    _init(dataset_name)
    sims = [sim(l1, l2) for l1, l2, _ in data]
    b1s, b2s, scores = zip(*data)
    print
    print "Spearman's correlation with WordSim-353:"
    if verbose:
        print "\n".join("%s\t%s\t%f\t%f" %fields 
                        for fields in zip(b1s, b2s, sims, scores))
    print '%.4f (%d pairs)' %_safe_spearmanr(sims, scores)
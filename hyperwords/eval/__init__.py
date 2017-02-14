import sys

from operator import itemgetter
from scipy.stats import spearmanr, pearsonr
import math
import numpy as np

def _safe_parallel_lists(a, b):
    indices = [i for i in range(len(a)) 
               if (a[i] is not None) and (b[i] is not None) and
               (not math.isnan(a[i])) and (not math.isnan(b[i]))]
    if len(indices) < len(a):
        sys.stderr.write("Omitted %d points\n" %(len(a)-len(indices)))
    if not indices:
        return [], []
    return np.asarray(a)[indices], np.asarray(b)[indices]


def _safe_spearmanr(a, b):
    safe_a, safe_b = _safe_parallel_lists(a, b)
    if len(safe_a) <= 1:
        return float('nan'), 0
    return spearmanr(safe_a, safe_b)[0], len(safe_a)


def _safe_pearson(a, b):
    safe_a, safe_b = _safe_parallel_lists(a, b)
    if len(safe_a) <= 1:
        return float('nan'), 0
    return pearsonr(safe_a, safe_b)[0], len(safe_a)
'''
Created on May 14, 2015

@author: Minh Ngoc Le
'''

import numpy as np

def _first_n_indices_break_tie_randomly(arr, n):    
    arr_no_tie = np.zeros((len(arr)), dtype=[('sim', 'f4'),('perm', 'i4')])
    arr_no_tie['sim'] = -np.asarray(arr, dtype=np.float)
    arr_no_tie['perm'] = np.random.permutation(len(arr))
    indices = np.argsort(arr_no_tie)[:n]
    return indices


def overlap(predicted, gold, n, repeats=100):
    overlap_ratios = np.zeros(repeats)
    for i in range(repeats):
        gold_items = _first_n_indices_break_tie_randomly(gold, n)
        pred_items = _first_n_indices_break_tie_randomly(predicted, n)
        overlap_ratios[i] = len(set(gold_items).intersection(pred_items))/float(n)
    return np.mean(overlap_ratios), np.std(overlap_ratios)


def overlap_dynamic(predicted, gold, n):
    pred_sorted_idx = np.argsort(-np.asarray(predicted, dtype=np.float))
    gold_sorted_idx = np.argsort(-np.asarray(gold, dtype=np.float))
    while (n < len(gold) and 
            (predicted[pred_sorted_idx[n-1]] == predicted[pred_sorted_idx[n]]
             or gold[gold_sorted_idx[n-1]] == gold[gold_sorted_idx[n]])):
        n += 1
    gold_items = gold_sorted_idx[:n]
    pred_items = pred_sorted_idx[:n]
    overlap_ratio = len(set(gold_items).intersection(pred_items))/float(n)
    return overlap_ratio, n


if __name__ == '__main__':
    print overlap([0.1, 0.3, 0.5], [0.3, 0.4, 0.2], 2, repeats=100)
    print overlap([0.5, 0.3, 0.3], [0.3, 0.4, 0.2], 2, repeats=100)
    print overlap_dynamic([0.1, 0.3, 0.5], [0.3, 0.4, 0.2], 2)
    print overlap_dynamic([0.5, 0.3, 0.3], [0.3, 0.4, 0.2], 2)
    
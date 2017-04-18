'''
Created on Dec 18, 2014

@author: Minh Ngoc Le
'''
from collections import defaultdict
import itertools
import os
import sys
from nltk.corpus import wordnet as wn
from similarity import LemmaPos2WordNetAdapter, wup_similarity
from eval import _safe_spearmanr, _safe_pearson, threshold
import numpy as np
from math import floor
from eval import ordering
from eval.ordering import accuracy, score_with_tie_correction, score_naive
from scipy.stats import rankdata


home_dir = os.path.dirname(__file__)
data_path = os.path.join(home_dir, 'SimLex-999.txt')
assert wn.get_version() == '3.0'

data = None
data_by_pos = None
data_high_assoc = None
data_low_assoc = None

def _init():
    global data, data_by_pos, data_high_assoc, data_low_assoc
    if data and data_by_pos:
        return
    data = []
    data_high_assoc = []
    data_low_assoc = []
    with open(data_path) as f:
        sys.stderr.write('Reading SimLex-999 dataset from %s... ' %data_path)
        f.readline() # skip headders
        for line in f:
            fields = line.strip().split('\t')
            dp = (fields[0], fields[1], fields[2].lower(), float(fields[3]))
            data.append(dp)
            if fields[8] == '1': data_high_assoc.append(dp)
            else: data_low_assoc.append(dp)
        sys.stderr.write('Done\n')
    data_by_pos = defaultdict(list)
    for point in data:
        data_by_pos[point[2]].append(point)
    return data, data_by_pos


def get_lemma_and_pos():
    _init()
    ret = set()
    for lemma1, lemma2, pos, _ in data:
        ret.add((lemma1, pos))
        ret.add((lemma2, pos)) 
    return ret


def _evalute_on_dataset(sim, data):
    _, _, _, gold = zip(*data)
    predicted = [sim((lemma1, pos), (lemma2, pos)) 
                 for lemma1, lemma2, pos, _ in data]
#     print predicted
    return _safe_spearmanr(predicted, gold)


def _pearson_on_dataset(sim, data):
    _, _, _, gold = zip(*data)
    predicted = [sim((lemma1, pos), (lemma2, pos)) 
                 for lemma1, lemma2, pos, _ in data]
    return _safe_pearson(predicted, gold)


def evaluate(sim):
    """
    Evaluate sim by calling it on 999 pairs of words in SimLex.
    Each word is represented by a tuple (lemma, pos).
    Return a list of  results on the dataset and 3 subsets of it.
    """
    _init()
    return ([['all'] + list(_evalute_on_dataset(sim, data))] +
            [[pos] + list(_evalute_on_dataset(sim, data_by_pos[pos])) 
             for pos in sorted(data_by_pos)])


def evaluate_and_print(sim):
    print "Spearman's correlation with SimLex-999:"
    for part, score, num in evaluate(sim):
        print "%s\t%.4f\t(%d pairs)" %(part, score, num)
    sys.stdout.flush()
    
    
def evaluate_and_print_333(sim):
    _init()
    print ("Spearman's correlation with SimLex-333: %.4f (%d pairs)" 
           %_evalute_on_dataset(sim, data_high_assoc))
    print ("Pearson correlation with SimLex-333: %.4f (%d pairs)" 
           %_pearson_on_dataset(sim, data_high_assoc))
    sys.stdout.flush()
    

def _filter_data_by_pos(data, pos):    
    return [dp for dp in data if dp[2] in pos]


def thresholded_overlap(sim, outpath=None, thresholds=None):
    _init()
    nv = _filter_data_by_pos(data, ('n', 'v'))
    print 
    print "Overlap with gold standard with different thresholds:"
    print "Size of SimLex-999(nv): %d" %len(nv)
    w1s, w2s, poss, gold = zip(*nv)
    predicted = np.array([sim((lemma1, pos), (lemma2, pos)) 
                          for lemma1, lemma2, pos, _ in nv], dtype='float')
    if outpath:
        with open(outpath, 'w') as f:
            ranks = rankdata(-predicted)
            f.write("\n".join("%s\t%s\t%s\t%f\t%d" %dp 
                              for dp in zip(w1s, w2s, poss, predicted, ranks)))
    print "\tn\toverlap\tactual-n"
    if thresholds is None:
        thresholds = range(50, 501, 50)
    for n in thresholds:
        print "\t%d\t%f\t%d" %((n,) + threshold.overlap_dynamic(predicted, gold, n))


def evaluate_and_print_high_assoc_nv(sim):
    _init()
    data_high_assoc_nv = _filter_data_by_pos(data_high_assoc, ('n', 'v'))
    print
    print "Size of SimLex-999(assoc,nv): %d" %len(data_high_assoc_nv)
    _, _, _, gold = zip(*data_high_assoc_nv)
    predicted = [sim((lemma1, pos), (lemma2, pos)) 
                 for lemma1, lemma2, pos, _ in data_high_assoc_nv]
    print ("Ordering accuracy on SimLex-999(assoc,nv): %.4f (%d pairs)" 
           %accuracy(gold, predicted))
    print ("Spearman's correlation on SimLex-999(assoc,nv): %.4f (%d pairs)" 
           %_safe_spearmanr(predicted, gold))
    print ("Pearson correlation on SimLex-999(assoc,nv): %.4f (%d pairs)" 
           %_safe_pearson(predicted, gold))
#     print "\n".join("%.2f\t%.2f" %dp for dp in zip(predicted, gold))
    sys.stdout.flush()


def evaluate_and_print_low_assoc_nv(sim):
    _init()
    data_low_assoc_nv = _filter_data_by_pos(data_low_assoc, ('n', 'v'))
    print "Size of SimLex(assoc,nv): %d" %len(data_low_assoc_nv)
    _, _, _, gold = zip(*data_low_assoc_nv)
    predicted = [sim((lemma1, pos), (lemma2, pos)) 
                 for lemma1, lemma2, pos, _ in data_low_assoc_nv]
    print ("Ordering accuracy on SimLex(assoc,nv): %.4f (%d pairs)" 
           %accuracy(gold, predicted))
    print ("Spearman's correlation on SimLex(assoc,nv): %.4f (%d pairs)" 
           %_safe_spearmanr(predicted, gold))
    print ("Pearson correlation on SimLex(assoc,nv): %.4f (%d pairs)" 
           %_safe_pearson(predicted, gold))
#     print "\n".join("%.2f\t%.2f" %dp for dp in zip(predicted, gold))
    sys.stdout.flush()


def evaluate_and_print_nv(sim):
    """
    Evaluate sim by calling it on 999 pairs of words in SimLex.
    Each word is represented by a tuple (lemma, pos).
    Return a list of  results on the dataset and 3 subsets of it.
    """
    _init()
    print
    data_nv = data_by_pos['n']+data_by_pos['v']
    results = [['nv'] + list(_evalute_on_dataset(sim, data_nv)),
               ['n'] + list(_evalute_on_dataset(sim, data_by_pos['n'])),
               ['v'] + list(_evalute_on_dataset(sim, data_by_pos['v'])),]
    print "Spearman's correlation with SimLex-999(nv):"
    for part, score, num in results:
        print "%s\t%.4f\t(%d pairs)" %(part, score, num)
    
    _, _, _, gold = zip(*data_nv)
    predicted = [sim((lemma1, pos), (lemma2, pos)) 
                 for lemma1, lemma2, pos, _ in data_nv]
    print ("Ordering accuracy (no tie correction) on SimLex-999(nv): %.4f (%d pairs)" 
           %accuracy(gold, predicted, score_naive))
    print ("Ordering accuracy (tie correction) on SimLex-999(nv): %.4f (%d pairs)" 
           %accuracy(gold, predicted, score_with_tie_correction))
    
    sys.stdout.flush()


def evaluate_groups_nv(sim, score_func, group_num=5):
    _init()
    nv = _filter_data_by_pos(data, ('n', 'v'))
    print
    print "Ordering accuracy of groups measured against SimLex-999(nv)"
    print "Score function used: %s" %score_func.__name__
    print "Number of pairs: %d" %len(nv)
    _, _, _, gold = zip(*nv)
    predicted = [sim((lemma1, pos), (lemma2, pos)) 
                 for lemma1, lemma2, pos, _ in nv]
    group_indices = [int(floor(g*group_num/10)) for g in gold]
    print "Total accuracy: %f (%d comparisons)" %ordering.accuracy(gold, predicted, score_func)
    a, c = ordering.accuracy_by_group(gold, predicted, group_indices, score_func)
    print "\tDelta\tAccuracy\t#Pairs"
    for k in range(group_num):
        correct = 0.0
        count = 0
        for i in range(group_num):
            for j in range(group_num):
                if abs(i-j) == k:
                    correct += a[i,j]*c[i,j]
                    count += c[i,j]
        accuracy = correct / count
        print "\t%d\t%f\t%d" %(k, accuracy, count)


def print_dislocations(sim, max_num=-1):
    _init()
    lemma1s, lemma2s, poss, gold = zip(*data)
    predicted = [sim((lemma1, pos), (lemma2, pos)) or 0
                 for lemma1, lemma2, pos, _ in data]
    gold_ranks = (-np.array(gold)).argsort().argsort()
    predicted_ranks = (-np.array(predicted)).argsort().argsort()
    dislocations = np.absolute(predicted_ranks - gold_ranks)
    vals = zip(lemma1s, lemma2s, poss, gold, gold_ranks, predicted, predicted_ranks, dislocations)
    vals = sorted(vals, key=lambda x: -x[7])
    if max_num > 0: vals = vals[:-max_num] 
    print 'lemma1\tlemma2\tpos\tgold\tgold rank\tpredicted\tpredicted rank\tabs. dislocation'
    for val in vals: 
        print "%s\t%s\t%s\t%.4f\t%d\t%.4f\t%d\t%d" %val
    sys.stdout.flush()


def print_wup_report():
    _init()
    ret = []
    for w1, w2, pos, gold_sim in data:
        wn_s1s = wn.synsets(w1, pos)
        wn_s2s = wn.synsets(w2, pos)
        best_wup_sim = None
        for wn_s1, wn_s2 in itertools.product(wn_s1s, wn_s2s):
            wup_r = wn.wup_similarity(wn_s1, wn_s2)
            if (best_wup_sim is None and wup_r is not None) \
                        or wup_r > best_wup_sim:
                best_wup_sim = wup_r
                best_synsets = (wn_s1, wn_s2)
        if best_wup_sim is not None:
            subsumer = best_synsets[0].lowest_common_hypernyms(best_synsets[1], simulate_root=True)[0]
            len1 = best_synsets[0].shortest_path_distance(subsumer, simulate_root=True)
            len2 = best_synsets[1].shortest_path_distance(subsumer, simulate_root=True)
            distant_to_subsumer = max(len1, len2)
            ret.append((w1, w2, pos, gold_sim, best_synsets[0], best_synsets[1], best_wup_sim, distant_to_subsumer))
    w1s, w2s, poss, gold, _, _, sims, distants = zip(*ret)
    gold_ranks = np.array(gold).argsort().argsort()
    predicted_ranks = np.array(sims).argsort().argsort()
    dislocations = list(predicted_ranks - gold_ranks)
    for val in zip(w1s, w2s, poss, dislocations, distants):
        print "%s\t%s\t%s\t%d\t%d" %val
    sys.stdout.flush()


def evaluate_wup():
    return evaluate(LemmaPos2WordNetAdapter(wup_similarity))


def print_histogram_nv(sim):
    _init()
    data_nv = data_by_pos['n'] + data_by_pos['v']
    predicted = [sim((lemma1, pos), (lemma2, pos)) 
                 for lemma1, lemma2, pos, _ in data_nv]
    predicted = [s for s in predicted if s is not None]
#     for x in zip(lemma1s, lemma2s, poss, gold, predicted):
#         print "%s\t%s\t%s\t%.4f\t%.4f" % x
    sys.stdout.write("Histogram (nv): ")
    print np.histogram(predicted)[0]


def compare(sim1, sim2):
    _init()
    print "Compare using SimLex-999:"
    scores1 = np.array([sim1((lemma1, pos), (lemma2, pos)) or -1000
                        for lemma1, lemma2, pos, _ in data])
    scores2 = np.array([sim2((lemma1, pos), (lemma2, pos)) or -1000 
                        for lemma1, lemma2, pos, _ in data])
    ranks1 = rankdata(scores1)
    ranks2 = rankdata(scores2)
    diffs_rank = np.absolute(ranks1 - ranks2)
    diffs_score = np.absolute(scores1 - scores2)
    print 'lemma1\tlemma2\tpos\trank_diff\tscore1\tscore2\trank1\trank2'
    for i in sorted(range(len(data)), key=lambda x: (diffs_rank[x], diffs_score[x])):
        if scores1[i] is not None and scores2[i] is not None:
            lemma1, lemma2, pos, _ = data[i]
            print('%s\t%s\t%s\t%d\t%.2f\t%.2f\t%d\t%d' 
                  %(lemma1, lemma2, pos, diffs_rank[i], 
                    scores1[i], scores2[i], ranks1[i], ranks2[i]))
    sys.stdout.flush()
    

if __name__ == '__main__':
    _init()
    
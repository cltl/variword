import os
import time
import random
import argparse

from multiprocessing import Process, Queue

from align_models import get_models

import ioutils
import alignment
from representations.representation_factory import create_representation

def get_cosine_deltas(base_embeds, delta_embeds, words, type):
    deltas = {}
    if type == "PPMI":
        base_embeds, delta_embeds = alignment.explicit_intersection_align(base_embeds, delta_embeds)
    else:
        base_embeds, delta_embeds = alignment.intersection_align(base_embeds, delta_embeds)
    print base_embeds.m.shape, delta_embeds.m.shape
    for word in words:
        if base_embeds.oov(word) or delta_embeds.oov(word):
            deltas[word] = float('nan')
        else:
            delta = base_embeds.represent(word).dot(delta_embeds.represent(word).T)
            if type == "PPMI":
                delta = delta[0,0]
            deltas[word] = delta
    return deltas

def merge(out_pref, years, word_list):
    vol_yearstats = {}
    disp_yearstats = {}
    for word in word_list:
        vol_yearstats[word] = {}
        disp_yearstats[word] = {}
    for year in years:
        vol_yearstat = ioutils.load_pickle(out_pref + str(year) + "-vols.pkl")
        disp_yearstat = ioutils.load_pickle(out_pref + str(year) + "-disps.pkl")
        for word in word_list:
            if word not in vol_yearstat:
                vol = float('nan')
            else:
                vol = vol_yearstat[word]
            if word not in disp_yearstat:
                disp = float('nan')
            else:
                disp = disp_yearstat[word]
            vol_yearstats[word][year] = vol
            disp_yearstats[word][year] = disp
        os.remove(out_pref + str(year) + "-vols.pkl")
        os.remove(out_pref + str(year) + "-disps.pkl")
    ioutils.write_pickle(vol_yearstats, out_pref + "vols.pkl")
    ioutils.write_pickle(disp_yearstats, out_pref + "disps.pkl")

def worker(proc_num, queue, out_pref, in_dir, target_lists, context_lists, displacement_base, thresh, year_inc, type):
    time.sleep(10*random.random())
    while True:
        if queue.empty():
            print proc_num, "Finished"
            break
        year = queue.get()
        print proc_num, "Loading matrices..."
        base = create_representation(type, in_dir + str(year-year_inc),  thresh=thresh, restricted_context=context_lists[year], normalize=True, add_context=False)
        delta = create_representation(type, in_dir + str(year),  thresh=thresh, restricted_context=context_lists[year], normalize=True, add_context=False)
        print proc_num, "Getting deltas..."
        year_vols = get_cosine_deltas(base, delta, target_lists[year], type)
        year_disp = get_cosine_deltas(displacement_base, delta, target_lists[year], type)
        print proc_num, "Writing results..."
        ioutils.write_pickle(year_vols, out_pref + str(year) + "-vols.pkl")
        ioutils.write_pickle(year_disp, out_pref + str(year) + "-disps.pkl")

def run_parallel(num_procs, out_pref, in_dir, years, target_lists, context_lists, displacement_base, thresh, year_inc, type):
    queue = Queue()
    for year in years:
        queue.put(year)
    procs = [Process(target=worker, args=[i, queue, out_pref, in_dir, target_lists, context_lists, displacement_base, thresh, year_inc, type]) for i in range(num_procs)]
    for p in procs:
        p.start()
    for p in procs:
        p.join()
    print "Merging"
    full_word_set = set([])
    for year_words in target_lists.itervalues():
        full_word_set = full_word_set.union(set(year_words))
    merge(out_pref, years, list(full_word_set))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Computes semantic change statistics for words.")
    parser.add_argument("dir", help="path to word vectors")
    parser.add_argument("num_procs", type=int, help="number of processes to spawn")
    parser.add_argument("word_file", help="path to sorted word file")
    parser.add_argument("out_dir", help="output path")
    parser.add_argument("--target-words", type=int, help="Number of words (of decreasing average frequency) to analyze", default=-1)
    parser.add_argument("--context-words", type=int, help="Number of words (of decreasing average frequency) to include in context. -2 means all regardless of word list", default=-1)
    parser.add_argument("--context-word-file")
    parser.add_argument("--type", default="SGNS")
    args = parser.parse_args()

    models = get_models(os.path.dirname(args.dir), os.path.basename(args.dir))
    print(models)

    with open(args.word_file) as infile:
        word_list = infile.read().split('\n')[:-1]


    ioutils.mkdir(args.out_dir)

    base_embeds, delta_embeds = alignment.intersection_align(base_embeds, delta_embeds)

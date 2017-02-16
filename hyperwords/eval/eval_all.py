'''
Created on Feb 16, 2015

@author: Minh Ngoc Le
'''
import os
import sys

from gensim.models.word2vec import Word2Vec

from eval.ordering import score_with_tie_correction

class Word2VecSim(object):

    def __init__(self, model_path, binary):
        sys.stderr.write("Loading word2vec model from %s... " %model_path)
        self.w2v = Word2Vec.load_word2vec_format(model_path, binary=binary)
        sys.stderr.write("Done.\n")
        
    def __call__(self, w1, w2):
        try:
            return self.w2v.similarity(w1, w2)
        except KeyError:
            return None


if __name__ == '__main__':
    path = sys.argv[1]
    sim = Word2VecSim(path, False)
    print 'Evaluating embeddings from file: %s' %path
    from similarity import LemmaPos2LemmaAdapter
    from eval import simlex999, men, wordsim353
    simlex999.evaluate_and_print_nv(LemmaPos2LemmaAdapter(sim))
    men.evaluate_and_print_nv(LemmaPos2LemmaAdapter(sim))
    wordsim353.evaluate_and_print(sim)
    simlex999.evaluate_and_print_high_assoc_nv(LemmaPos2LemmaAdapter(sim))
    simlex999.evaluate_groups_nv(LemmaPos2LemmaAdapter(sim), score_with_tie_correction)
    simlex999.thresholded_overlap(LemmaPos2LemmaAdapter(sim), 
                                  outpath="w2v.out", 
                                  thresholds=(89, 94, 108, 172, 178, 191, 305, 645))
    print '----- END -----'
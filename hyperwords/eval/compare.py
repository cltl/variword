'''
Created on Feb 16, 2015

@author: Minh Ngoc Le
'''
import os
import sys

from gensim.models import KeyedVectors

class Word2VecSim(object):

    def __init__(self, model_path, binary):
        sys.stderr.write("Loading word2vec model from %s... " %model_path)
        self.w2v = KeyedVectors.load_word2vec_format(model_path, binary=binary)
        sys.stderr.write("Done.\n")
        
    def __call__(self, w1, w2):
        try:
            return self.w2v.similarity(w1, w2)
        except KeyError:
            return None


if __name__ == '__main__':
    path1, path2 = sys.argv[1:]
    sim1 = Word2VecSim(path1, False)
    sim2 = Word2VecSim(path2, False)
    print 'Comparing embeddings from two files: %s and %s' %(path1, path2)
    from similarity import LemmaPos2LemmaAdapter
    from eval import simlex999, men, wordsim353
    simlex999.compare(LemmaPos2LemmaAdapter(sim1), LemmaPos2LemmaAdapter(sim2))
    men.compare(LemmaPos2LemmaAdapter(sim1), LemmaPos2LemmaAdapter(sim2))
    wordsim353.compare(sim1, sim2)
    print '----- END -----'
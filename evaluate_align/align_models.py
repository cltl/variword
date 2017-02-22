"""align_models

Usage:
    align_models.py <folder> <matchname>

"""
from __future__ import print_function
import os
import alignment
import numpy as np
import re
from docopt import docopt
from representations.embedding import Embedding
from representations.sequentialembedding import SequentialEmbedding

def align_models(path, matchname, outfolder, add_context=True):
    """
    Aligns a series of spins to each other.
    :param path:
    :param matchname:
    :param outfolder:
    :param add_context:
    :return:
    """

    vocabulary = []
    models = get_models(path, matchname)

    base_embedding = None
    for n, model in enumerate(models):
        print("Aligning ", model)

        if n == 0: #  first run, nothing to align
            aligned_embedding = Embedding.load(os.path.join(path, model), add_context=add_context)
        else:
            embedding_path = os.path.join(path, models[n])
            embedding = Embedding.load(embedding_path, add_context=add_context)

            aligned_embedding = align(base_embedding, embedding)

        base_embedding = aligned_embedding

        #  Save it to the output dir!
        save(aligned_embedding, model, outfolder)
        vocabulary.append(set(aligned_embedding.iw))

    common_vocab = set.intersection(*vocabulary)
    with open(os.path.join(outfolder, matchname + '.aligned.words.vocab'), 'w') as vocabfile:
        for i in sorted(common_vocab):
            vocabfile.write(i)
            vocabfile.write('\n')

def save(aligned_embedding, model, outfolder):

    np.save(os.path.join(outfolder, model + '.aligned.words.npy'), aligned_embedding.m)

    with open(os.path.join(outfolder, model + '.aligned.words.vocab'), 'w') as vocabfile:
        for i in aligned_embedding.iw:
            vocabfile.write(i)
            vocabfile.write('\n')

def get_models(path, matchname):
    """
    Return a list of models in given directory path. Matchname is prefix.
    :param path:
    :param matchname:
    :return:
    """
    models = set()
    for model in [m for m in os.listdir(path) if re.match(matchname + '\d' + '\.', m)]:
        models.add(model.split('.')[0])

    return sorted(models)

def align(embed1, embed2):
    """
    Align embed 2 to embed1
    :return: aligned_embedding
    """

    aligned_embedding = alignment.smart_procrustes_align(embed1, embed2)

    return aligned_embedding

if __name__ == "__main__":

    arguments = docopt(__doc__)

    PATH = arguments['<folder>']
    MATCHNAME = arguments['<matchname>']

    align_models(PATH, MATCHNAME, outfolder="output")


    # PATH = '/home/leon/Documenten/5.2_Machine_learning/3/histwords/MODELS/wiki_100M_recom/run.2017-02-01-10:05:16'
    # MATCHNAME = 'sgns_rand_pinit'
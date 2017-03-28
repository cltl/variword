"""align_models

Usage:
    align_models.py <modellist> <outputdir> 

"""
from __future__ import print_function
import os
import alignment
import numpy as np
import scipy
from scipy.spatial import distance
from docopt import docopt
from representations.embedding import Embedding
from itertools import combinations
from collections import defaultdict

def align_models(path, models, outfolder, add_context=True):
    """
    Aligns a series of spins to each other. 
    Stores them at `outfolder` and outputs a common vocabulary file to that folder. 
    :param path: where to find the models
    :param models: list of models to align
    :param outfolder:
    :param add_context:
    :return: all aligned embeddings in a list of tuples (modelname, embedding).
    """

    vocabulary = []
    # models = get_models(path, matchname)
    print(models)

    all_aligned_embeddings = []

    base_embedding = None
    for n, modelname in enumerate(models):
        print("Aligning ", modelname)

        embedding_path = os.path.join(path, models[n])

        if n == 0: #  first run, nothing to align
            aligned_embedding = Embedding.load(embedding_path, add_context=add_context)
        else:
            embedding = Embedding.load(embedding_path, add_context=add_context)
            aligned_embedding = align(base_embedding, embedding)

        base_embedding = aligned_embedding

        #  Save it to the output dir!
        save(aligned_embedding, modelname, outfolder)
        vocabulary.append(set(aligned_embedding.iw))

        # But also add it to a list of embeddings for comparing the similarity between models.
        # Then we don't have to load it again.
        all_aligned_embeddings.append((modelname, aligned_embedding))

    common_vocab = set.intersection(*vocabulary)

    with open(os.path.join(outfolder, 'aligned.common.vocab'), 'w') as vocabfile:
        for i in sorted(common_vocab):
            vocabfile.write(i)
            vocabfile.write('\n')

    return all_aligned_embeddings

def save(aligned_embedding, model, outfolder):
    """
    Save the model and the vocabulary in the same way the hyperwords script does.
    :param aligned_embedding: the aligned embedding (Embedding)
    :param model: model name
    :param outfolder: output folder
    :return: None
    """

    np.save(os.path.join(outfolder, model + '.aligned.words.npy'), aligned_embedding.m)

    with open(os.path.join(outfolder, model + '.aligned.words.vocab'), 'w') as vocabfile:
        for i in aligned_embedding.iw:
            vocabfile.write(i)
            vocabfile.write('\n')

def get_models(list_of_models):
    """
    Return a list of models in given directory path.
    :param list_of_models: models from the input file
    :return: filtered models for usage in the script
    """
    models = set()
    for model in list_of_models:
        if model.endswith('.words.npy'):
            models.add(model.split('.words.npy')[0])

    return sorted(models, key=lambda x: x[::-1])  # alphabetical backwards sorted

def align(embed1, embed2):
    """
    Align embed2 to embed1
    :return: aligned_embedding
    """
    aligned_embedding = alignment.smart_procrustes_align(embed1, embed2)

    return aligned_embedding

def check_similarity(all_aligned_embeddings, vocab):
    """
    Check similarity for every word in the vocab between all models (aligned)
    :param all_aligned_embeddings: list of tuples (modelname, embedding)
    :param vocab:
    :return: resultsdictionary. Every word is a key. Value is a dictionary of models and similarity.
    """

    results = []
    resultsdictionary = defaultdict(dict)

    with open(vocab) as vocabfile:
        vocablist = vocabfile.read().split('\n')[:-1]

    model_combinations = list(combinations(all_aligned_embeddings, 2))

    for word in vocablist:
        sims = []
        for embeddingtuple in model_combinations:

            models, embeddings = zip(*embeddingtuple)

            sim = similarity(word, embeddings)
            sims.append(sim)

            resultsdictionary[word][models] = sim

        results.append((word, sims))
        # print(word, sims)

    print(sorted(results, key=lambda x: x[1])[:20])
    print('vocab', len(vocablist), 'results', len(results))

    return resultsdictionary


def calculate_distance(all_aligned_embeddings, vocab):
    """
    Calculate distance for every word in the vocab between all models (aligned)
    :param all_aligned_embeddings: list of tuples (modelname, embedding)
    :param vocab:
    :return: resultsdictionary. Every word is a key. Value is a dictionary of models and similarity.
    """

    results = []
    resultsdictionary = defaultdict(dict)

    with open(vocab) as vocabfile:
        vocablist = vocabfile.read().split('\n')[:-1]

    model_combinations = list(combinations(all_aligned_embeddings, 2))

    for word in vocablist:
        dists = []
        for embeddingtuple in model_combinations:

            models, embeddings = zip(*embeddingtuple)

            dist = cosine_distance(word, embeddings)
            dists.append(dist)

            resultsdictionary[word][models] = dist

        results.append((word, dists))

    print(sorted(results, key=lambda x: x[1])[:20])
    print('vocab', len(vocablist), 'results', len(results))

    return resultsdictionary




def similarity(word, embeddings):
    """
    Compute similarity for a word in two embeddings by taking the dot product.
    :param embeddings: tuple of two embeddings
    :return: similarity
    """

    emb1, emb2 = embeddings

    sim = emb1.represent(word).dot(emb2.represent(word))
    dist = scipy.spatial.distance.cosine(emb1.represent(word), emb2.represent(word))

    return sim

def cosine_distance(word, embeddings):
    """
    Compute distance for a word in two embeddings by taking the dot product.
    :param embeddings: tuple of two embeddings
    :return: similarity
    """

    emb1, emb2 = embeddings

    dist = scipy.spatial.distance.cosine(emb1.represent(word), emb2.represent(word))

    return dist


if __name__ == "__main__":

    arguments = docopt(__doc__)
    MODELS = arguments['<modellist>']
    OUTPUT = arguments['<outputdir>']

    if not os.path.exists(OUTPUT):
        os.makedirs(OUTPUT)

    with open(MODELS) as infile:
        list_of_models = infile.read().split('\n')[:-1]
    models = get_models((list_of_models))

    if os.path.isfile(models[0]):
        path = None
    else:
        path = os.path.dirname(MODELS)
    print('Model locations:', path)

    all_aligned_models = align_models(path, models, outfolder=OUTPUT)

    default_vocab = os.path.join(OUTPUT, 'aligned.common.vocab')
    results = calculate_distance(all_aligned_models, vocab=default_vocab)

    # make a panda out of it
    import pandas as pd
    df = pd.DataFrame.from_dict(results, orient='index')
    df.to_csv(os.path.join(OUTPUT, 'results.csv'), float_format='%.17g') # 17 is the standard python2 notation


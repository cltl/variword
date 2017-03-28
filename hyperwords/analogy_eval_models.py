from __builtin__ import sorted

from docopt import docopt
import numpy as np
import os

from representations.representation_factory import create_representation


def main():
    args = docopt("""
    Usage:
        analogy_eval_models.py [options] <model1_output_path> <model2_output_path> <resultsfile> <runresultsfile>

    Options:
        --neg NUM    Number of negative samples; subtracts its log from PMI (only applicable to PPMI) [default: 1]
        --w+c        Use ensemble of word and context vectors (not applicable to PPMI)
        --eig NUM    Weighted exponent of the eigenvalue matrix (only applicable to SVD) [default: 0.5]
    """)

    model1_output = read_model_output(args['<model1_output_path>'])
    model2_output = read_model_output(args['<model2_output_path>'])
    #xi, ix = get_vocab(data)
    #representation = create_representation(args)
    accuracy_add, accuracy_mul = evaluate_models(model1_output, model2_output)
    accuracy_cosadd, accuracy_cosmul = results_to_file(model1_output, model2_output, args['<resultsfile>'])
    write_scores(accuracy_cosadd, accuracy_cosmul, args['<resultsfile>'], args['<runresultsfile>'])
    print args['<model1_output_path>'], args['<model2_output_path>'], '\t%0.3f' % accuracy_add, '\t%0.3f' % accuracy_mul


def read_test_set(path):
    test = []
    with open(path) as f:
        for line in f:
            analogy = line.strip().lower().split()
            test.append(analogy)
    return test

def read_model_output(path_model_output):
    output_list = []
    with open(path_model_output) as f:
        for line in f:
            gold, model_add, model_mul = line.strip().split('\t')
            output_list.append((model_add, model_mul))
    return output_list



def evaluate_models(model1_output, model2_output):

    correct_add = 0.0
    correct_mul = 0.0

    for guess_tuple1, guess_tuple2 in zip(model1_output, model2_output):
        b1_add = guess_tuple1[0]
        b1_mul = guess_tuple1[1]
        b2_add = guess_tuple2[0]
        b2_mul = guess_tuple2[1]

        if b1_add == b2_add:
            correct_add += 1
        if b1_mul == b2_mul:
            correct_mul += 1

    return correct_add/len(model1_output), correct_mul/len(model1_output)


def results_to_file(model1_output, model2_output, resultsfile):

    correct_add = 0.0
    correct_mul = 0.0
    with open(resultsfile, 'w') as outfile:

        for guess_tuple1, guess_tuple2 in zip(model1_output, model2_output):

            b1_add = guess_tuple1[0]
            b1_mul = guess_tuple1[1]
            b2_add = guess_tuple2[0]
            b2_mul = guess_tuple2[1]

            if b1_add == b2_add:
                correct_add += 1
            if b1_mul == b2_mul:
                correct_mul += 1

            outfile.write(b1_add+'\t'+b1_mul+'\t'+b2_add+'\t'+b2_mul+'\n')

    return correct_add/len(model1_output), correct_mul/len(model1_output)



def prepare_similarities(representation, vocab):
    vocab_representation = representation.m[[representation.wi[w] if w in representation.wi else 0 for w in vocab]]
    sims = vocab_representation.dot(representation.m.T)

    dummy = None
    for w in vocab:
        if w not in representation.wi:
            dummy = representation.represent(w)
            break
    if dummy is not None:
        for i, w in enumerate(vocab):
            if w not in representation.wi:
                vocab_representation[i] = dummy

    if type(sims) is not np.ndarray:
        sims = np.array(sims.todense())
    else:
        sims = (sims+1)/2
    return sims


def guess(representation, sims, xi, a, a_, b):
    sa = sims[xi[a]]
    sa_ = sims[xi[a_]]
    sb = sims[xi[b]]

    add_sim = -sa+sa_+sb
    if a in representation.wi:
        add_sim[representation.wi[a]] = 0
    if a_ in representation.wi:
        add_sim[representation.wi[a_]] = 0
    if b in representation.wi:
        add_sim[representation.wi[b]] = 0
    b_add = representation.iw[np.nanargmax(add_sim)]

    mul_sim = sa_*sb*np.reciprocal(sa+0.01)
    if a in representation.wi:
        mul_sim[representation.wi[a]] = 0
    if a_ in representation.wi:
        mul_sim[representation.wi[a_]] = 0
    if b in representation.wi:
        mul_sim[representation.wi[b]] = 0
    b_mul = representation.iw[np.nanargmax(mul_sim)]


    return b_add, b_mul

def write_scores(accuracy_cosadd, accuracy_cosmul, resultsfile, runresultsfile):
    """
    Write spearman correlation to txt file.

    :param representation: results from create_representation
    :param data: testset data
    :return: None
    """

    filename = os.path.basename(resultsfile)

    with open(runresultsfile, 'a') as outfile:
        outfile.write(str(filename) + '_cosadd')
        outfile.write('\t')
        outfile.write(str(accuracy_cosadd))
        outfile.write('\n')

        outfile.write(str(filename) + '_cosmul')
        outfile.write('\t')
        outfile.write(str(accuracy_cosmul))
        outfile.write('\n')




if __name__ == '__main__':
    main()

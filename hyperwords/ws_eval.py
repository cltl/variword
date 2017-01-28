import os
from docopt import docopt
from scipy.stats.stats import spearmanr

from representations.representation_factory import create_representation


def main():
    args = docopt("""
    Usage:
        ws_eval.py [options] <representation> <representation_path> <task_path> <resultsfile> <runresultsfile>

    Options:
        --neg NUM    Number of negative samples; subtracts its log from PMI (only applicable to PPMI) [default: 1]
        --w+c        Use ensemble of word and context vectors (not applicable to PPMI)
        --eig NUM    Weighted exponent of the eigenvalue matrix (only applicable to SVD) [default: 0.5]
    """)

    data = read_test_set(args['<task_path>'])
    representation = create_representation(args)
    correlation = evaluate(representation, data)
    evaluate_to_file(representation, data, args['<resultsfile>'])
    write_scores(correlation, args['<resultsfile>'], args['<runresultsfile>'])  # write spearman scores to results.txt

    print args['<representation>'], args['<representation_path>'], '\t%0.3f' % correlation


def read_test_set(path):
    test = []
    with open(path) as f:
        for line in f:
            x, y, sim = line.strip().lower().split()
            test.append(((x, y), sim))
    return test




def evaluate(representation, data):
    results = []
    for (x, y), sim in data:
        results.append((representation.similarity(x, y), sim))
    actual, expected = zip(*results)
    return spearmanr(actual, expected)[0]

def evaluate_to_file(representation, data, resultsfile):
    results = []

    with open(resultsfile, 'w') as outfile:

        for (x, y), sim in data:
            results.append((representation.similarity(x, y), sim))
            outfile.write(str(representation.similarity(x, y))+'\t'+str(sim)+'\n')


        # #outfile.write('spearman correlation\n')
        # actual, expected = zip(*results)
        # outfile.write('spearman:'+'\t'+str(spearmanr(actual, expected)[0]))


def write_scores(correlation, resultsfile, runresfile):
    """
    Write spearman correlation to txt file.

    :param representation: results from create_representation
    :param data: testset data
    :return: None
    """

    filename = os.path.basename(resultsfile)

    with open(runresfile, 'a') as outfile:
        outfile.write(str(filename))
        outfile.write('\t')
        outfile.write(str(correlation))
        outfile.write('\n')

if __name__ == '__main__':
    main()

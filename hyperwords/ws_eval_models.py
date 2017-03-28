import os
from docopt import docopt
from scipy.stats.stats import spearmanr

from representations.representation_factory import create_representation


def main():
    args = docopt("""
    Usage:
        ws_eval_models.py [options] <model1_output_path> <model2_output_path> <resultsfile> <runresultsfile>

    Options:
        --neg NUM    Number of negative samples; subtracts its log from PMI (only applicable to PPMI) [default: 1]
        --w+c        Use ensemble of word and context vectors (not applicable to PPMI)
        --eig NUM    Weighted exponent of the eigenvalue matrix (only applicable to SVD) [default: 0.5]
    """)

    model1_output = read_model_output(args['<model1_output_path>'])
    model2_output = read_model_output(args['<model2_output_path>'])
    correlation = evaluate_models(model1_output, model2_output)
    evaluate_to_file(model1_output, model2_output, args['<resultsfile>'])
    write_scores(correlation, args['<resultsfile>'], args['<runresultsfile>'])  # write spearman scores to results.txt

    print args['<model1_output_path>'], args['<model2_output_path>'], '\t%0.3f' % correlation




def read_model_output(path_model_output):
    output_list = []
    with open(path_model_output) as f:
        for line in f:
            model, gold = line.strip().split('\t')
            output_list.append(model)
    return output_list



def evaluate_models(model1_output, model2_output):
    results = []
    for sim1, sim2 in zip(model1_output, model2_output):
        results.append((sim1, sim2))
    actual1, actual2 = zip(*results)
    return spearmanr(actual1, actual2)[0]


def evaluate_to_file(model1_output, model2_output, resultsfile):


    with open(resultsfile, 'w') as outfile:

        for sim1, sim2 in zip(model1_output, model2_output):

            outfile.write(str(sim1)+'\t'+str(sim2)+'\n')


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

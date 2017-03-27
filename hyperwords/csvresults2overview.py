import sys
import csv
import os
from collections import defaultdict

evalIndex = {'ws353sim': [0, 203], 'ws353rel': [1, 252], 'bruniMEN': [2, 3000], 'radinskyTurk': [3, 280],
             'luongRare': [4, 2034], 'hill999': [5, 999], 'google-cosadd': [6, 19258], 'google-cosmul': [7, 19258],
             'msr-cosadd': [8, 7118], 'msr-cosmul': [9, 7118]}


def collect_results(resultfile):
    '''
    Function that collects the results from one experiment and stores them in a dictionary
    :param resultfile: csv file with results from experiment
    :return: dictionary key is evaluation set, value outcome of evaluation
    '''

    result_dict = {}
    myresults = open(resultfile, 'r')

    for line in myresults:
        # if key occurs multiple times, first scores are NaN or they are the same;
        # i.e. it's okay if score is overwritten
        parts = line.rstrip().split(',')
        key = parts.pop(0)
        if not key == 'model':
            result_dict[key] = parts

    return result_dict


def get_results_from_one_initiations(results_list):
    score = 0.0
    for result in results_list:
        score += float(result)

    return score


def determine_worst_middle_best_random_init(result_dict):
    '''
    Function that checks results and compares outcome randomized numbers
    Returns dictionary with -best, worst-, middle- instead
    :param result_dict: results retrieved from results file
    :return: dictionary with score as key and (basic) SGNS name as value
    '''

    init_models = {}

    init1_res = get_results_from_one_initiations(result_dict.get('SGNSpinit1'))
    init1_res_rev = get_results_from_one_initiations(result_dict.get('SGNSpinit1-rev'))
    init1 = init1_res + init1_res_rev

    init_models[init1] = '1'

    init2_res = get_results_from_one_initiations(result_dict.get('SGNSpinit2'))
    init2_res_rev = get_results_from_one_initiations(result_dict.get('SGNSpinit2-rev'))
    init2 = init2_res + init2_res_rev

    if not init2 in init_models:
        init_models[init2] = '2'
    else:
        print(init2, 'init2')

    init3_res = get_results_from_one_initiations(result_dict.get('SGNSpinit3'))
    init3_res_rev = get_results_from_one_initiations(result_dict.get('SGNSpinit3-rev'))
    init3 = init3_res + init3_res_rev

    if not init3 in init_models:
        init_models[init3] = '3'
    else:
        print(init3, 'init3')

    number2rank = {}
    mapping = {0: '-lowest', 1: '-middle', 2: '-highest'}
    for i, k in enumerate(sorted(init_models)):
        model = init_models.get(k)
        rank = mapping.get(i)
        number2rank[model] = rank

    return number2rank


def add_results(eval2results, eval):
    global evalIndex

    totalSim = 0
    weigthedSim = 0
    tSimWeight = 0
    totalAnalog = 0
    weigthedAnalog = 0
    tAnalogWeight = 0
    for eset, info in evalIndex.items():
        # info provides index in evalset
        index = info[0]
        score = float(eval[index])
        eval2results[eset].append(str(score))
        if index < 6:
            totalSim += score
            weigthedSim += score * float(info[1])
            tSimWeight += info[1]
        else:
            totalAnalog += score
            weigthedAnalog += score * float(info[1])
            tAnalogWeight += info[1]
    eval2results['simAverage'].append(str(float(totalSim) / float(6)))
    eval2results['weigthedSimAverage'].append(str(float(weigthedSim) / float(tSimWeight)))
    eval2results['analogAverage'].append(str(float(totalAnalog) / float(4)))
    eval2results['weightedAnalogAverage'].append(str(float(weigthedAnalog) / float(tAnalogWeight)))


def create_evaluation_to_result_dictionary(resultdict):
    eval2result = defaultdict(list)
    for system, eval in sorted(resultdict.items()):
        add_results(eval2result, eval)

    return eval2result


def convert_to_dictionary_for_graph(result_dict):
    '''
    Takes result dict compares random initiation outcomes and creates dictionary with performances as base
    for random initializations
    :param result_dict: result_dict as read from files
    :return: result dict with random initiated named after relative performance
    '''

    number2rank = determine_worst_middle_best_random_init(result_dict)
    new_results_dict = {}
    for k, val in result_dict.items():
        if not 'SGNSpinit' in k:
            new_results_dict[k] = val
        else:
            number = k.split('-')[0].lstrip('SGNSpinit')
            rank = number2rank.get(number)
            new_name = k.replace(number, rank)
            new_results_dict[new_name] = val

    return new_results_dict


def print_out_results(overall_resultdir, variable_factor, eval2resultdict):

    for eval, results in eval2resultdict.items():
        outfile = open(overall_resultdir + '/' + eval + '.csv','a')
        outfile.write(variable_factor + ',' + ','.join(results) + '\n')
        outfile.close()



def initiate_files_if_necessary(result_dict, eval_dict, overall_resultdir):

    for eval in eval_dict:
        if not os.path.isfile(overall_resultdir + '/' + eval + '.csv'):
            myout = open(overall_resultdir + '/' + eval + '.csv', 'w')
            myout.write('size\model,')
            myout.write(",".join(sorted(result_dict.keys())) + '\n')
            myout.close()



def add_results_to_overall(resultfile, overall_result_dir, variable_factor):
    '''
    Retrieves results from single experiment and adds it to files providing overall results of the research
    :param resultfile: input file with results of experiment
    :param overall_result_dir: directory where overall results are stored
    :param variable_factor: the factor we're varying in the range of experiments (for now corpus size)
    :return: None
    '''

    #TO ADD; INITIATION FUNCTION FOR RESULT FILES IF THEY DON'T EXIST YET
    result_dict = collect_results(resultfile)
    updated_result_dict = convert_to_dictionary_for_graph(result_dict)
    eval2resultdict = create_evaluation_to_result_dictionary(updated_result_dict)
    initiate_files_if_necessary(updated_result_dict, eval2resultdict, overall_result_dir)
    print_out_results(overall_result_dir, variable_factor, eval2resultdict)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    if len(argv) < 4:
        print('Usage: python csvresults2overview.py csvresultfile overallresultdir variable_factor')
    else:
        add_results_to_overall(argv[1], argv[2], argv[3])


if __name__ == '__main__':
    main()

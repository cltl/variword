import os
import glob
from itertools import combinations



models_ws353sim = glob.glob('results/run.2017-03-20-14:01:36/ws/ws353sim*')
models_ws353rel = glob.glob('results/run.2017-03-20-14:01:36/ws/ws353rel*')
models_brunimen = glob.glob('results/run.2017-03-20-14:01:36/ws/brunimen*')
models_hillsimlex = glob.glob('results/run.2017-03-20-14:01:36/ws/hillsimlex*')
models_luongrare = glob.glob('results/run.2017-03-20-14:01:36/ws/luongrare*')
models_radinskyturk = glob.glob('results/run.2017-03-20-14:01:36/ws/radinskyturk*')

models_google = glob.glob('results/run.2017-03-20-14:01:36/analogies/google*')
models_msr = glob.glob('results/run.2017-03-20-14:01:36/analogies/msr*')
def combinations_to_file_ws(model_list, outfile):

    for combination in combinations(model_list, 2):
        model1 = combination[0].split('/ws/')[1]
        model2 = combination[1].split('/ws/')[1]
        name = model1.strip('.tsv')+'-'+model2.strip('.tsv')

        outfile.write('python hyperwords/ws_eval_models.py $wc results/$UUID/ws/'+model1+' results/$UUID/ws/'+model2+' $RESULTSDIR/ws/'+name+'$suffix.tsv $UUIDRES\n')

def combinations_to_file_analogy(model_list, outfile):

    for combination in combinations(model_list, 2):
        model1 = combination[0].split('/analogies/')[1]
        model2 = combination[1].split('/analogies/')[1]
        name = model1.strip('.tsv')+'-'+model2.strip('.tsv')

        outfile.write('python hyperwords/analogy_eval_models.py $wc results/$UUID/analogies/'+model1+' results/$UUID/analogies/'+model2+' $RESULTSDIR/analogies/'+name+'$suffix.tsv $UUIDRES\n')


with open('get_results_spearman.sh', 'w') as outfile:
    outfile.write('echo "# Evaluate on Word Similarity"\n')
    outfile.write('echo\n')
    outfile.write('UUID=$1\n')
    outfile.write('RESULTSDIR=$2/$UUID\n')
    outfile.write('UUIDRES=$RESULTSDIR/results.txt\n')
    outfile.write('suffix=$3\n')
    outfile.write('wc=$4\n\n')
    outfile.write('mkdir -p $RESULTSDIR/ws\n\n')

    combinations_to_file_ws(models_ws353sim, outfile)
    combinations_to_file_ws(models_ws353rel, outfile)
    combinations_to_file_ws(models_brunimen, outfile)
    combinations_to_file_ws(models_hillsimlex, outfile)
    combinations_to_file_ws(models_luongrare, outfile)
    combinations_to_file_ws(models_radinskyturk, outfile)

    outfile.write('echo "# Evaluate on Analogies"\n')
    outfile.write('echo\n')
    outfile.write('mkdir -p $RESULTSDIR/analogies\n\n')

    combinations_to_file_analogy(models_google, outfile)
    combinations_to_file_analogy(models_msr, outfile)

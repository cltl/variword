import os
import glob


#all_results = glob.glob('results/run*/*')

# test: count files in results_spearman_models

all_rundirs = glob.glob('results/*/')

with open('unique_run_ids.txt', 'w') as outfile:
    for rundir in all_rundirs:
        uuid = rundir.rstrip('/').split('/')[1]
        outfile.write(uuid+'\n')

from docopt import docopt

#global variables determining order of printout

eval_sets = ["ws353sim","ws353rel","brunimen","radinskyturk","luongrare","hillsimlex","google-cosadd","google-cosmul","msr-cosadd","msr-cosmul"]

models = ['PPMI','SVD','SGNSpinit1','SGNSpinit2','SGNSpinit3','SGNSsvd','SGNSpinit1-rev','SGNSpinit2-rev','SGNSpinit3-rev','SGNSsvd-rev']


def main():
    args = docopt("""
        Usage:
        results2csv.py [options] <resultsfile_in> <resultsfile_out>
        """)
    results = read_in_results(args['<resultsfile_in>'])
    create_output_file(args['<resultsfile_out>'], results)


def create_output_file(outfile, results):

    global eval_sets, models
    
    myout = open(outfile, 'w')
    myout.write('model')
    
    #write out evaluation sets
    for eset in eval_sets:
        myout.write(',' + eset)
    myout.write('\n')

    for model in models:
        myout.write(model)
        modelresults = results.get(model)

        for eset in eval_sets:
            myout.write(',' + modelresults.get(eset))
        myout.write('\n')
    myout.close()





def update_info(myresults, testset, model, score):

    if model in myresults:
        modelscores = myresults.get(model)
    else:
        modelscores = {}

    if testset in modelscores:
        print('Possible problem; multiple evaluations scores for model', model, 'on set', testset)
    else:
        modelscores[testset] = score

    myresults[model] = modelscores



def read_in_results(inputfile):

    myresults = {}
    resfile = open(inputfile, 'r')
    for line in resfile:
        parts = line.rstrip().split()
        components = parts[0].split('_')
        testset = components[0]
        if components[-1] in ['cosadd', 'cosmul']:
            testset += '-' + components.pop()
        if components[-1] == 'w2.tsv':
            model = components[-2]
        else:
            model = components[-1].split('.')[0]
    
        update_info(myresults, testset, model, parts[-1])
        
    resfile.close()
    return myresults


if __name__ == '__main__':
    main()

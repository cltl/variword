import matplotlib.pyplot as plt
import csv
import sys
import os


model2representation = {'SGNSpinit-highest':'b--','SGNSpinit-middle':'b--','SGNSpinit-lowest':'b--','SGNSsvd':'b^','SGNSpinit-highest-rev':'y--','SGNSpinit-middle-rev':'y--','SGNSpinit-lowest-rev':'y--','SGNSsvd-rev':'y^','PPMI':'r','SVD':'g'}

def update_info(modelname, size, value, my_info):

    if not modelname in my_info:
        modeldict = {}
        my_info[modelname] = modeldict
    else:
        modeldict = my_info.get(modelname)
    modeldict[size] = float(value)


def get_relevant_info(inputfile):

    my_info = {}
    max_size = 0
    with open(inputfile, 'r') as csvin:
        csvreader = csv.DictReader(csvin)
        for row in csvreader:
            size = float(row.get('size\model'))
            if not size == 750.0:
                if size > max_size:
                    max_size = size
                for field, value in row.items():
                    if not field == 'size\model':
                        update_info(field, size, value, my_info)
    
    return my_info, max_size

def create_plot_structure(information):

    #TODO:
    #2. SET NAME AND FORMAT OF LINE
    global model2representation
    plot_structure = []
    max_val = 0.0
    min_val = 0.0
    for k, info in information.items():
        sizes = []
        outcomes = []
        for size in sorted(info.keys()):
            sizes.append(size)
            outcome = info.get(size)
            if outcome > max_val:
                max_val = outcome
            if outcome < min_val:
                min_val = outcome
            outcomes.append(outcome)
        plot_structure.append(sizes)
        plot_structure.append(outcomes)
        plot_structure.append(model2representation.get(k))

    return plot_structure, max_val, min_val


def plot_graph(plotstructure, corpus_max, max_val, min_val, evalname, outputdir):

    #TODO: PRINT PLOT TO FILE
    plt.figure()
    plt.plot(*plotstructure)
    if min_val < 0:
        min_val =- 0.01
    plt.axis([0, corpus_max, min_val, max_val + 0.03])
    plt.xlabel('corpus size (M words)')
    plt.ylabel('Spearman rho')
    plt.title(evalname)
    plt.savefig(outputdir + evalname + '.png')


def create_graphs(inputdir, outputdir):

    for f in os.listdir(inputdir):
        information, corpus_max = get_relevant_info(inputdir + f)
        plotstructure, max_val, min_val = create_plot_structure(information)
        plot_graph(plotstructure, corpus_max, max_val, min_val, f.split('.')[0], outputdir)


def main():

    argv = sys.argv
    
    if len(argv) < 3:
        print('Usage: python create_graphs.py inputdir/ outputdir/')
    else:
        create_graphs(argv[1], argv[2])


if __name__ == '__main__':
    main()

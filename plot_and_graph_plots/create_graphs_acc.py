import matplotlib.pyplot as plt
import csv
import sys
import os


model2representation = {'SGNSpinit1':'b--','SGNSpinit2':'b--','SGNSpinit3':'b--','SGNSsvd':'b^','SGNSpinit1-rev':'y--','SGNSpinit2-rev':'y--','SGNSpinit3-rev':'y--','SGNSsvd-rev':'y^','PPMI':'r','SVD':'g'}



def get_relevant_info(inputfile):

    my_info = {}
    with open(inputfile, 'r') as csvin:
        csvreader = csv.DictReader(csvin)
        for row in csvreader:
            myvalues = {}
            for field, value in row.items():
                if field == 'model':
                    model = value
                else:
                    if not value is 'nan':
                    
                    #set value to 0.0 when nan
                        try:
                            myvalues[float(field)] = float(value) * 100.0
                        except:
                            myvalues[float(field)] = float(0.0)
                    else:
                        myvalues[float(field)] = float(0.0)
                        
            my_info[model] = myvalues
    return my_info

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


def plot_graph(plotstructure, max_val, min_val, evalname, outputdir):

    #TODO: PRINT PLOT TO FILE
    plt.figure()
    plt.plot(*plotstructure)
    if min_val < 0:
        min_val =- 0.01
    plt.axis([0, 2000, min_val, max_val + 3])
    plt.xlabel('corpus size (M words)')
    plt.ylabel('Accuracy (%)')
    plt.title(evalname)
    plt.savefig(outputdir + evalname + '.png')


def create_graphs(inputdir, outputdir):

    for f in os.listdir(inputdir):
        information = get_relevant_info(inputdir + f)
        plotstructure, max_val, min_val = create_plot_structure(information)
        plot_graph(plotstructure, max_val, min_val, f.split('.')[0], outputdir)


def main():

    argv = sys.argv
    
    if len(argv) < 3:
        print('Usage: python create_graphs.py inputdir/ outputdir/')
    else:
        create_graphs(argv[1], argv[2])


if __name__ == '__main__':
    main()

import csv
import sys
import os



def obtain_information(indir):

    
    sizes = set()
    evaluationsets = {}
    for f in os.listdir(indir):
        mysize = float(f.split('M')[0])
        sizes.add(mysize)
        with open(indir + f, 'r') as csvin:
            csvreader = csv.DictReader(csvin)
            for row in csvreader:
                modelname = row.get('model')
                for k, val in row.items():
                    if not k == 'model':
                        if k in evaluationsets:
                            myoutcome = evaluationsets.get(k)
                        else:
                            myoutcome = {}
                            evaluationsets[k] = myoutcome
                        if modelname in myoutcome:
                            result = myoutcome.get(modelname)
                        else:
                            result = {}
                            result['model'] = modelname
                            myoutcome[modelname] = result
                        result[mysize] = float(val)

    return sizes, evaluationsets


def create_overview_per_evaluation(indir, outdir):

    sizes, evaluationsets = obtain_information(indir)
    fieldnames = ['model']
    for size in sorted(sizes):
        fieldnames.append(size)
    for evalset, results in evaluationsets.items():
        
        with open(outdir + evalset + '.csv', 'w') as csvout:
            csvwriter = csv.DictWriter(csvout,fieldnames=fieldnames)
            csvwriter.writeheader()
            for row in results.values():
                csvwriter.writerow(row)



def main():

    myargs = sys.argv

    if len(myargs) < 3:
        print('Usage: python create_overview_per_evaluation.py indir/ outdir/')
    else:
        create_overview_per_evaluation(myargs[1], myargs[2])

if __name__ == '__main__':
    main()

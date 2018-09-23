import csv
import sys

def analyze_name(name):

    evalset = name.split('_')[0]
    modelname = name.split(evalset + '_')[1]
    if '_cos' in modelname:
        suffix = '_' + modelname.split('_')[-1]
        evalset += suffix
        modelname = modelname.split(suffix)[0]

    return evalset, modelname


def obtain_input_information(inputfile):
    
    fieldnames = ['model']
    evaluation_outcome = {}

    for line in open(inputfile, 'r'):
        parts = line.split('\t')
        score = float(parts[1].rstrip())
        evalset, model = analyze_name(parts[0])
        if not evalset in fieldnames:
            fieldnames.append(evalset)
        if model in evaluation_outcome:
            row = evaluation_outcome.get(model)
        else:
            row = {}
            row['model'] = model
            evaluation_outcome[model] = row
        row[evalset] = score

    return fieldnames, evaluation_outcome


def convert_results(inputfile, outputfile):

    fieldnames, model2eval = obtain_input_information(inputfile)
    with open(outputfile, 'w') as csvoutput:
        csvwriter = csv.DictWriter(csvoutput, fieldnames=fieldnames)
        csvwriter.writeheader()
        for row in model2eval.values():
            csvwriter.writerow(row)


def main():


    myargs = sys.argv

    if len(myargs) < 3:
        print('Usage: python convert_results_model2eval.py inputfile outputfile')
    else:
        convert_results(myargs[1], myargs[2])

if __name__ == '__main__':
    main()

import csv
import os
from docopt import docopt

def main():
    args = docopt("""
    Usage:
        results_to_csv.py <UUID> <RESULTSDIR> <sharedcsv>

    """)

    d = dict()

    runid = args['<UUID>']
    sharedcsv = args['<sharedcsv>']
    resultsdir = args['<RESULTSDIR>']

    with open(resultsdir + '/' + runid + '/results.txt') as infile:
        entries = infile.readlines()

        for entry in entries:
            print(entry)
            method, corr = entry.split('\t')

            d[method] = corr

    d['_runid'] = runid
    fieldnames = sorted(d.keys())

    file_exists = os.path.exists(sharedcsv)



    with open(sharedcsv, 'a') as csvfile:

        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')

        if not file_exists:
            csvwriter.writeheader()

        csvwriter.writerow(d)

if __name__ == "__main__":

    main()


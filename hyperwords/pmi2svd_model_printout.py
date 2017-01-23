from sparsesvd import sparsesvd

from docopt import docopt
import numpy as np

from representations.explicit import PositiveExplicit
from representations.matrix_serializer import save_vocabulary
from representations.embedding import SVDEmbedding




def print_out_matrix(mymatrix, iw, suffix, output_path, dim):
    
    outfile = open(output_path + suffix + '.txt', 'w')
    outfile.write(str(dim) + '\n')
    for i, scores in enumerate(mymatrix):
        line = iw[i]
        for score in scores:
            line += '\t' + str(score)
        outfile.write(line + '\n')
    outfile.close()



def main():
    args = docopt("""
    Usage:
        pmi2svd.py [options] <pmi_path> <output_path>
    
    Options:
        --dim NUM    Dimensionality of eigenvectors [default: 500]
        --neg NUM    Number of negative samples; subtracts its log from PMI [default: 1]
        --eig NUM    Eigenvalue for matrix multiplication U S in [default: 0.0]
    """)
    
    pmi_path = args['<pmi_path>']
    output_path = args['<output_path>']
    dim = int(args['--dim'])
    neg = int(args['--neg'])
    eig = float(args['--eig'])
    
    explicit = PositiveExplicit(pmi_path, normalize=False, neg=neg)

    ut, s, vt = sparsesvd(explicit.m.tocsc(), dim)

#probably ut is a matrix with all relevant data, we can write that out one row at the time.

    np.save(output_path + '.ut.npy', ut)
    np.save(output_path + '.s.npy', s)
    np.save(output_path + '.vt.npy', vt)
    save_vocabulary(output_path + '.words.vocab', explicit.iw)
    save_vocabulary(output_path + '.contexts.vocab', explicit.ic)

    svd = SVDEmbedding(output_path, True, eig)
    print_out_matrix(svd.m, explicit.iw, '.svd', output_path, dim)


if __name__ == '__main__':
    main()

from sparsesvd import sparsesvd

from docopt import docopt
import numpy as np

from representations.explicit_words_only import PositiveExplicit
from representations.matrix_serializer import save_vocabulary
from representations.embedding import SVDEmbedding

def print_out_matrices(words1, embs1, words2, embs2, output_path):
    with open(output_path + ".txt", 'w') as outfile:
        for words, embs in ((words1, embs1), (words2, embs2)):
            outfile.write('%d\t%d\n' %embs.shape)
            for word, vector in zip(words, embs):
                outfile.write(word)
                for num in vector:
                    outfile.write('\t%f' %num)
                outfile.write('\n')

def main():
    args = docopt("""
    Usage:
        pmi2svd_model_print.py [options] <pmi_path> <output_path>
    
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

    svd = SVDEmbedding(output_path, False, eig)
    words, word_embeddings = explicit.iw, svd.m
    svd = SVDEmbedding(output_path, True, eig)
    contexts, context_embeddings = explicit.iw, svd.m
    print_out_matrices(words, word_embeddings, 
                       contexts, context_embeddings, output_path)


if __name__ == '__main__':
    main()

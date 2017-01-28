This README provides details on how to carry out word2vec variation experiments.

1. Variation 1: use different initations.

1.A. Alternative variations and storing them:

modified pipeline:

[init step]

repeat 10 times:
  word2vecf/create_init -wvocab <word_vocab_file> -cvocab <context_vocab_file> -output <params_file>

[experiment]

repeat 10 times:
  word2vecf/word2vecf_var -pinit <params_file> <other_options>

1.B. Initiating with SVD model of the corpus

Steps:

1. Create the pmi model of the corpus as explained in the original README:

(example for window size 2; for all scripts; check Usage for further options)

#create co-occurrence pairs within specific window 
python hyperwords/corpus2pairs.py --win 2 corpus.clean > corpusdir2/pairs

#create counts from the pairs
scripts/pairs2counts.sh corpusdir2/pairs > corpusdir2/counts

#create vocabularies from the counts
python hyperwords/counts2vocab.py corpusdir2/counts

#create pmi models
python hyperwords/counts2pmi.py corpusdir2/counts corpusdir2/pmi

#create svd models printing out the model as file
python hyperwords/pmi2svd_model_printout.py corpusdir2/pmi corpusdir2/svd

The svd model will be printed out in file corpusdir2/svd.svd.txt
The option --eig allows you to define the multiplication factor of the eigenvalue.





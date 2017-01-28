#!/bin/bash

DIR=$1
cds=$2
dim=$3
neg=$4
eig=$5

# calculate pmi value
python hyperwords/counts2pmi_words_only.py --cds $cds $DIR/counts $DIR/pmi
cp $DIR/pmi.words.vocab $DIR/pmi.contexts.vocab

# create embeddings svd
python hyperwords/pmi2svd_model_printout.py --dim $dim --neg $neg --eig $eig $DIR/pmi $DIR/svd

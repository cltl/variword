#!/bin/bash

mkdir -p $2
python hyperwords/corpus2pairs.py --win $3 $1 > $2/pairs
echo 'created pairs'
scripts/pairs2counts.sh $2/pairs > $2/counts
echo 'created counts'
python hyperwords/counts2vocab_only_words.py $2/counts
echo 'created vocabs'

#!/bin/bash

INF=$1
DIR=$2
WIN=$3
sub=$4


mkdir -p $DIR
python hyperwords/corpus2pairs.py --win $WIN --dyn --sub $sub --del $INF > $DIR/pairs
echo 'created pairs'
scripts/pairs2counts.sh $DIR/pairs > $DIR/counts
echo 'created counts'
python hyperwords/counts2vocab_only_words.py $DIR/counts
echo 'created vocabs'

#!/bin/bash

PAIRS=$1
VOC=$2
INIT=$3
OUT=$4
size=$5
neg=$6
iters=$7

./word2vecf/word2vecf_var -train $PAIRS -cvocab $VOC -wvocab $VOC -dumpcv $OUT.contexts -output $OUT.words -threads 10 -negative $neg -size $size -iters $iters -pinit $INIT

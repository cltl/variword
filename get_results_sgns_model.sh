#!/usr/bin/env bash
echo "# Evaluate on Word Similarity"
echo
echo "WS353 Results"
echo "-------------"

UUID=$1
RUNFILE=$2
RESULTSDIR=$3/$UUID
UUIDRES=$RESULTSDIR/results.txt
suffix=$4
wc=$5


mkdir -p $RESULTSDIR/ws

# ws353_similarity

python hyperwords/ws_eval.py $wc SGNS $RUNFILE testsets/ws/ws353_similarity.txt $RESULTSDIR/ws/ws353sim_wc_SGNS$suffix.tsv $UUIDRES

# ws353_relatedness

python hyperwords/ws_eval.py $wc SGNS $RUNFILE testsets/ws/ws353_relatedness.txt $RESULTSDIR/ws/ws353rel_wc_SGNS$suffix.tsv $UUIDRES

# Bruni MEN

python hyperwords/ws_eval.py $wc SGNS $RUNFILE testsets/ws/bruni_men.txt $RESULTSDIR/ws/brunimen_wc_SGNS$suffix.tsv $UUIDRES

# Radinsky M Turk

python hyperwords/ws_eval.py $wc SGNS $RUNFILE testsets/ws/radinsky_mturk.txt $RESULTSDIR/ws/radinskyturk_wc_SGNS$suffix.tsv $UUIDRES

# Luong Rare Words

python hyperwords/ws_eval.py $wc SGNS $RUNFILE testsets/ws/luong_rare.txt $RESULTSDIR/ws/luongrare_wc_SGNS$suffix.tsv $UUIDRES

# Hill SimLex

python hyperwords/ws_eval.py $wc SGNS $RUNFILE testsets/ws/simlex_999.txt $RESULTSDIR/ws/hillsimlex_wc_SGNS$suffix.tsv $UUIDRES

echo "# Evaluate on Analogies"
echo
echo "Google Analogy Results"
echo "----------------------"
mkdir -p $RESULTSDIR/analogies

# Google

python hyperwords/analogy_eval.py SGNS $RUNFILE testsets/analogy/google.txt $RESULTSDIR/analogies/google_wc_SGNS$suffix.tsv $UUIDRES

# MSR

python hyperwords/analogy_eval.py SGNS $RUNFILE testsets/analogy/msr.txt $RESULTSDIR/analogies/msr_wc_SGNS$suffix.tsv $UUIDRES

#!/usr/bin/env bash
echo "# Evaluate on Word Similarity"
echo
echo "WS353 Results"
echo "-------------"

UUID=$1
RESULTSDIR=$2/$UUID
UUIDRES=$RESULTSDIR/results.txt
suffix=$3
wc=$4


mkdir -p $RESULTSDIR/ws

# ws353_similarity

# init1 - init1-rev
python hyperwords/ws_eval_models.py $wc results/$UUID/ws/ws353sim_wc_SGNSpinit1.tsv results/$UUID/ws/ws353sim_wc_SGNSpinit1-rev.tsv $RESULTSDIR/ws/ws353sim_wc_SGNS$suffix.tsv $UUIDRES

# ws353_relatedness

python hyperwords/ws_eval_models.py $wc results/$UUID/ws/ws353rel_wc_SGNSpinit1.tsv results/$UUID/ws/ws353rel_wc_SGNSpinit1-rev.tsv $RESULTSDIR/ws/ws353rel_wc_SGNS$suffix.tsv $UUIDRES


# Bruni MEN

python hyperwords/ws_eval_models.py $wc results/$UUID/ws/brunimen_wc_SGNSpinit1.tsv results/$UUID/ws/brunimen_wc_SGNSpinit1-rev.tsv $RESULTSDIR/ws/brunimen_wc_SGNS$suffix.tsv $UUIDRES


# HILL simlex

python hyperwords/ws_eval_models.py $wc results/$UUID/ws/hillsimlex_wc_SGNSpinit1.tsv results/$UUID/ws/hillsimlex_wc_SGNSpinit1-rev.tsv $RESULTSDIR/ws/hillsimlex_wc_SGNS$suffix.tsv $UUIDRES

# Rare

python hyperwords/ws_eval_models.py $wc results/$UUID/ws/luongrare_wc_SGNSpinit1.tsv results/$UUID/ws/luongrare_wc_SGNSpinit1-rev.tsv $RESULTSDIR/ws/luongrare_wc_SGNS$suffix.tsv $UUIDRES

# Radinsky M Turk

python hyperwords/ws_eval_models.py $wc results/$UUID/ws/radinskyturk_wc_SGNSpinit1.tsv results/$UUID/ws/radinskyturk_wc_SGNSpinit1-rev.tsv $RESULTSDIR/ws/radinskyturk_wc_SGNS$suffix.tsv $UUIDRES

echo "# Evaluate on Analogies"
echo
echo "Google Analogy Results"
echo "----------------------"
mkdir -p $RESULTSDIR/analogies

python hyperwords/analogy_eval_models.py $wc results/$UUID/analogies/google_wc_SGNSpinit1.tsv results/$UUID/analogies/google_wc_SGNSpinit1-rev.tsv $RESULTSDIR/analogies/google_wc_SGNS$suffix.tsv $UUIDRES

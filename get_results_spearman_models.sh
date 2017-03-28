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


#python hyperwords/ws_eval.py $wc SGNS $RUNFILE testsets/ws/ws353_relatedness.txt $RESULTSDIR/ws/ws353rel_wc_SGNS$suffix.tsv $UUIDRES

# Bruni MEN



# Radinsky M Turk

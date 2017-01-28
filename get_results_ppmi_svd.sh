#!/usr/bin/env bash
echo "# PPMI-SVD evaluation"
echo
echo "# Evaluate on Word Similarity"
echo
echo "WS353 Results"
echo "-------------"
echo
echo "WS353 Results"
echo "-------------"

UUID=$1
RESULTSDIR=$3/$UUID
RUNDIR=$2
UUIDRES=$RESULTSDIR/results.txt

neg=$4
eig=$5

mkdir -p $RESULTSDIR/ws

# ws353_similarity

python hyperwords/ws_eval.py --neg $neg PPMI $RUNDIR/pmi testsets/ws/ws353_similarity.txt $RESULTSDIR/ws/ws353sim_neg_PPMI_w2.tsv $UUIDRES
python hyperwords/ws_eval.py --eig $eig SVD $RUNDIR/svd testsets/ws/ws353_similarity.txt $RESULTSDIR/ws/ws353sim_eig_SVD_w2.tsv $UUIDRES

# ws353_relatedness

python hyperwords/ws_eval.py --neg $neg PPMI $RUNDIR/pmi testsets/ws/ws353_relatedness.txt $RESULTSDIR/ws/ws353rel_neg_PPMI_w2.tsv $UUIDRES
python hyperwords/ws_eval.py --eig $eig SVD $RUNDIR/svd testsets/ws/ws353_relatedness.txt $RESULTSDIR/ws/ws353rel_eig_SVD_w2.tsv $UUIDRES

# Bruni MEN

python hyperwords/ws_eval.py --neg $neg PPMI $RUNDIR/pmi testsets/ws/bruni_men.txt $RESULTSDIR/ws/brunimen_neg_PPMI_w2.tsv $UUIDRES
python hyperwords/ws_eval.py --eig $eig SVD $RUNDIR/svd testsets/ws/bruni_men.txt $RESULTSDIR/ws/brunimen_eig_SVD_w2.tsv $UUIDRES

# Radinsky M Turk

python hyperwords/ws_eval.py --neg $neg PPMI $RUNDIR/pmi testsets/ws/radinsky_mturk.txt $RESULTSDIR/ws/radinskyturk_neg_PPMI_w2.tsv $UUIDRES
python hyperwords/ws_eval.py --eig $eig SVD $RUNDIR/svd testsets/ws/radinsky_mturk.txt $RESULTSDIR/ws/radinskyturk_eig_SVD_w2.tsv $UUIDRES

# Luong Rare Words

python hyperwords/ws_eval.py --neg $neg PPMI $RUNDIR/pmi testsets/ws/luong_rare.txt $RESULTSDIR/ws/luongrare_neg_PPMI_w2.tsv $UUIDRES
python hyperwords/ws_eval.py --eig $eig SVD $RUNDIR/svd testsets/ws/luong_rare.txt $RESULTSDIR/ws/luongrare_eig_SVD_w2.tsv $UUIDRES

# Hill SimLex

python hyperwords/ws_eval.py --neg $neg PPMI $RUNDIR/pmi testsets/ws/simlex_999.txt $RESULTSDIR/ws/hillsimlex_neg_PPMI_w2.tsv $UUIDRES
python hyperwords/ws_eval.py --eig $eig SVD $RUNDIR/svd testsets/ws/simlex_999.txt $RESULTSDIR/ws/hillsimlex_eig_SVD_w2.tsv $UUIDRES


echo "# Evaluate on Analogies"
echo
echo "Google Analogy Results"
echo "----------------------"
mkdir -p $RESULTSDIR/analogies

# Google

python hyperwords/analogy_eval.py PPMI $RUNDIR/pmi testsets/analogy/google.txt $RESULTSDIR/analogies/google_neg_PPMI_w2.tsv $UUIDRES
python hyperwords/analogy_eval.py --eig $eig SVD $RUNDIR/svd testsets/analogy/google.txt $RESULTSDIR/analogies/google_eig_SVD_w2.tsv $UUIDRES

# MSR
echo
echo "Google Analogy Results"
echo "----------------------"

python hyperwords/analogy_eval.py PPMI $RUNDIR/pmi testsets/analogy/msr.txt $RESULTSDIR/analogies/msr_neg_PPMI_w2.tsv $UUIDRES
python hyperwords/analogy_eval.py --eig $eig SVD $RUNDIR/svd testsets/analogy/msr.txt $RESULTSDIR/analogies/msr_eig_SVD_w2.tsv $UUIDRES

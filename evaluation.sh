#!/usr/bin/env bash
echo "# Evaluate on Word Similarity"
echo
echo "WS353 Results"
echo "-------------"

UUID=$1
DATADIR=$2
RESULTSDIR=$3/$UUID
RUNDIR=$DATADIR/$UUID

mkdir $RESULTSDIR/ws

# ws353_similarity

python hyperwords/ws_eval.py --neg 5 PPMI $RUNDIR/w2.sub/pmi testsets/ws/ws353_similarity.txt $RESULTSDIR/ws/ws353sim_neg_PPMI_w2.tsv $UUID
python hyperwords/ws_eval.py --eig 0.5 SVD $RUNDIR/w2.sub/svd testsets/ws/ws353_similarity.txt $RESULTSDIR/ws/ws353sim_eig_SVD_w2.tsv $UUID
python hyperwords/ws_eval.py --w+c SGNS $RUNDIR/w2.sub/sgns testsets/ws/ws353_similarity.txt $RESULTSDIR/ws/ws353sim_wc_SGNS_w2.tsv $UUID

python hyperwords/ws_eval.py --neg 5 PPMI $RUNDIR/w5.dyn.sub.del/pmi testsets/ws/ws353_similarity.txt $RESULTSDIR/ws/ws353sim_neg_PPMI_w5.tsv $UUID
python hyperwords/ws_eval.py --eig 0.5 SVD $RUNDIR/w5.dyn.sub.del/svd testsets/ws/ws353_similarity.txt $RESULTSDIR/ws/ws353sim_eig_SVD_w5.tsv $UUID
python hyperwords/ws_eval.py --w+c SGNS $RUNDIR/w5.dyn.sub.del/sgns testsets/ws/ws353_similarity.txt $RESULTSDIR/ws/ws353sim_wc_SGNS_w2.tsv $UUID

# ws353_relatedness

python hyperwords/ws_eval.py --neg 5 PPMI $RUNDIR/w2.sub/pmi testsets/ws/ws353_relatedness.txt $RESULTSDIR/ws/ws353rel_neg_PPMI_w2.tsv $UUID
python hyperwords/ws_eval.py --eig 0.5 SVD $RUNDIR/w2.sub/svd testsets/ws/ws353_relatedness.txt $RESULTSDIR/ws/ws353rel_eig_SVD_w2.tsv $UUID
python hyperwords/ws_eval.py --w+c SGNS $RUNDIR/w2.sub/sgns testsets/ws/ws353_relatedness.txt $RESULTSDIR/ws/ws353rel_wc_SGNS_w2.tsv $UUID

python hyperwords/ws_eval.py --neg 5 PPMI $RUNDIR/w5.dyn.sub.del/pmi testsets/ws/ws353_relatedness.txt $RESULTSDIR/ws/ws353rel_neg_PPMI_w5.tsv $UUID
python hyperwords/ws_eval.py --eig 0.5 SVD $RUNDIR/w5.dyn.sub.del/svd testsets/ws/ws353_relatedness.txt $RESULTSDIR/ws/ws353rel_eig_SVD_w5.tsv $UUID
python hyperwords/ws_eval.py --w+c SGNS $RUNDIR/w5.dyn.sub.del/sgns testsets/ws/ws353_relatedness.txt $RESULTSDIR/ws/ws353rel_wc_SGNS_w2.tsv $UUID

# Bruni MEN

python hyperwords/ws_eval.py --neg 5 PPMI $RUNDIR/w2.sub/pmi testsets/ws/bruni_men.txt $RESULTSDIR/ws/brunimen_neg_PPMI_w2.tsv $UUID
python hyperwords/ws_eval.py --eig 0.5 SVD $RUNDIR/w2.sub/svd testsets/ws/bruni_men.txt $RESULTSDIR/ws/brunimen_eig_SVD_w2.tsv $UUID
python hyperwords/ws_eval.py --w+c SGNS $RUNDIR/w2.sub/sgns testsets/ws/bruni_men.txt $RESULTSDIR/ws/brunimen_wc_SGNS_w2.tsv $UUID

python hyperwords/ws_eval.py --neg 5 PPMI $RUNDIR/w5.dyn.sub.del/pmi testsets/ws/bruni_men.txt $RESULTSDIR/ws/brunimen_neg_PPMI_w5.tsv $UUID
python hyperwords/ws_eval.py --eig 0.5 SVD $RUNDIR/w5.dyn.sub.del/svd testsets/ws/bruni_men.txt $RESULTSDIR/ws/brunimen_eig_SVD_w5.tsv $UUID
python hyperwords/ws_eval.py --w+c SGNS $RUNDIR/w5.dyn.sub.del/sgns testsets/ws/bruni_men.txt $RESULTSDIR/ws/brunimen_wc_SGNS_w2.tsv $UUID

# Radinsky M Turk

python hyperwords/ws_eval.py --neg 5 PPMI $RUNDIR/w2.sub/pmi testsets/ws/radinsky_mturk.txt $RESULTSDIR/ws/radinskyturk_neg_PPMI_w2.tsv $UUID
python hyperwords/ws_eval.py --eig 0.5 SVD $RUNDIR/w2.sub/svd testsets/ws/radinsky_mturk.txt $RESULTSDIR/ws/radinskyturk_eig_SVD_w2.tsv $UUID
python hyperwords/ws_eval.py --w+c SGNS $RUNDIR/w2.sub/sgns testsets/ws/radinsky_mturk.txt $RESULTSDIR/ws/radinskyturk_wc_SGNS_w2.tsv $UUID

python hyperwords/ws_eval.py --neg 5 PPMI $RUNDIR/w5.dyn.sub.del/pmi testsets/ws/radinsky_mturk.txt $RESULTSDIR/ws/radinskyturk_neg_PPMI_w5.tsv $UUID
python hyperwords/ws_eval.py --eig 0.5 SVD $RUNDIR/w5.dyn.sub.del/svd testsets/ws/radinsky_mturk.txt $RESULTSDIR/ws/radinskyturk_eig_SVD_w5.tsv $UUID
python hyperwords/ws_eval.py --w+c SGNS $RUNDIR/w5.dyn.sub.del/sgns testsets/ws/radinsky_mturk.txt $RESULTSDIR/ws/radinskyturk_wc_SGNS_w2.tsv $UUID

# Luong Rare Words

python hyperwords/ws_eval.py --neg 5 PPMI $RUNDIR/w2.sub/pmi testsets/ws/luong_rare.txt $RESULTSDIR/ws/luongrare_neg_PPMI_w2.tsv $UUID
python hyperwords/ws_eval.py --eig 0.5 SVD $RUNDIR/w2.sub/svd testsets/ws/luong_rare.txt $RESULTSDIR/ws/luongrare_eig_SVD_w2.tsv $UUID
python hyperwords/ws_eval.py --w+c SGNS $RUNDIR/w2.sub/sgns testsets/ws/luong_rare.txt $RESULTSDIR/ws/luongrare_wc_SGNS_w2.tsv $UUID

python hyperwords/ws_eval.py --neg 5 PPMI $RUNDIR/w5.dyn.sub.del/pmi testsets/ws/luong_rare.txt $RESULTSDIR/ws/luongrare_neg_PPMI_w5.tsv $UUID
python hyperwords/ws_eval.py --eig 0.5 SVD $RUNDIR/w5.dyn.sub.del/svd testsets/ws/luong_rare.txt $RESULTSDIR/ws/luongrare_eig_SVD_w5.tsv $UUID
python hyperwords/ws_eval.py --w+c SGNS $RUNDIR/w5.dyn.sub.del/sgns testsets/ws/luong_rare.txt $RESULTSDIR/ws/luongrare_wc_SGNS_w2.tsv $UUID

# Hill SimLex

python hyperwords/ws_eval.py --neg 5 PPMI $RUNDIR/w2.sub/pmi testsets/ws/simlex_999.txt $RESULTSDIR/ws/hillsimlex_neg_PPMI_w2.tsv $UUID
python hyperwords/ws_eval.py --eig 0.5 SVD $RUNDIR/w2.sub/svd testsets/ws/simlex_999.txt $RESULTSDIR/ws/hillsimlex_eig_SVD_w2.tsv $UUID
python hyperwords/ws_eval.py --w+c SGNS $RUNDIR/w2.sub/sgns testsets/ws/simlex_999.txt $RESULTSDIR/ws/hillsimlex_wc_SGNS_w2.tsv $UUID

python hyperwords/ws_eval.py --neg 5 PPMI $RUNDIR/w5.dyn.sub.del/pmi testsets/ws/simlex_999.txt $RESULTSDIR/ws/hillsimlex_neg_PPMI_w5.tsv $UUID
python hyperwords/ws_eval.py --eig 0.5 SVD $RUNDIR/w5.dyn.sub.del/svd testsets/ws/simlex_999.txt $RESULTSDIR/ws/hillsimlex_eig_SVD_w5.tsv $UUID
python hyperwords/ws_eval.py --w+c SGNS $RUNDIR/w5.dyn.sub.del/sgns testsets/ws/simlex_999.txt $RESULTSDIR/ws/hillsimlex_wc_SGNS_w2.tsv $UUID


echo "# Evaluate on Analogies"
echo
echo "Google Analogy Results"
echo "----------------------"
mkdir $RESULTSDIR/analogies

# Google

python hyperwords/analogy_eval.py PPMI $RUNDIR/w2.sub/pmi testsets/analogy/google.txt $RESULTSDIR/analogies/google_neg_PPMI_w2.tsv $UUID
python hyperwords/analogy_eval.py --eig 0 SVD $RUNDIR/w2.sub/svd testsets/analogy/google.txt $RESULTSDIR/analogies/google_eig_SVD_w2.tsv $UUID
python hyperwords/analogy_eval.py SGNS $RUNDIR/w2.sub/sgns testsets/analogy/google.txt $RESULTSDIR/analogies/google_wc_SGNS_w2.tsv $UUID

python hyperwords/analogy_eval.py PPMI $RUNDIR/w5.dyn.sub.del/pmi testsets/analogy/google.txt $RESULTSDIR/analogies/google_neg_PPMI_w5.tsv $UUID
python hyperwords/analogy_eval.py --eig 0 SVD $RUNDIR/w5.dyn.sub.del/svd testsets/analogy/google.txt $RESULTSDIR/analogies/google_eig_SVD_w5.tsv $UUID
python hyperwords/analogy_eval.py SGNS $RUNDIR/w5.dyn.sub.del/sgns testsets/analogy/google.txt $RESULTSDIR/analogies/google_wc_SGNS_w2.tsv $UUID

# MSR
echo
echo "Google Analogy Results"
echo "----------------------"

python hyperwords/analogy_eval.py PPMI $RUNDIR/w2.sub/pmi testsets/analogy/msr.txt $RESULTSDIR/analogies/msr_neg_PPMI_w2.tsv $UUID
python hyperwords/analogy_eval.py --eig 0 SVD $RUNDIR/w2.sub/svd testsets/analogy/msr.txt $RESULTSDIR/analogies/msr_eig_SVD_w2.tsv $UUID
python hyperwords/analogy_eval.py SGNS $RUNDIR/w2.sub/sgns testsets/analogy/msr.txt $RESULTSDIR/analogies/msr_wc_SGNS_w2.tsv $UUID

python hyperwords/analogy_eval.py PPMI $RUNDIR/w5.dyn.sub.del/pmi testsets/analogy/msr.txt $RESULTSDIR/analogies/msr_neg_PPMI_w5.tsv $UUID
python hyperwords/analogy_eval.py --eig 0 SVD $RUNDIR/w5.dyn.sub.del/svd testsets/analogy/msr.txt $RESULTSDIR/analogies/msr_eig_SVD_w5.tsv $UUID
python hyperwords/analogy_eval.py SGNS $RUNDIR/w5.dyn.sub.del/sgns testsets/analogy/msr.txt $RESULTSDIR/analogies/msr_wc_SGNS_w2.tsv $UUID


echo "Put the scores in a CSV file"
python results_to_csv.py $UUID $3 $3/shared_results.csv

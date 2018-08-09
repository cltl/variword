#!/bin/sh


# Generate unique id to distinguish between runs:
start=$(date "+%F-%T")
UUID='run'.$start
IN=$1
DIR=$2
MODELDIR=$DIR/$UUID
RESDIR=$3
# default dim is 500
DIM=500

mkdir -p $MODELDIR
mkdir -p $RESDIR$UUID

echo "./run_experiment_recommended_w2_settings.sh $1 $2 $3" > $RESDIR$UUID/setup.txt 

#1. create pairs (win=2, dyn=dirty, sub=10^-5) and counts
./clean_data_2_sub_dirty_pairs_and_counts.sh $IN $DIR 2 1e-5

#2 create ppmi and svd models (neg=5, cds=0.75, eig=0)
# get_ppmi_and_svd_print_out.sh dir cds dim neg eig
./get_ppmi_and_svd_print_out.sh $DIR 0.75 ${DIM} 5 0.0

#4 move data to MODELDIR

mv $DIR/pairs $MODELDIR
mv $DIR/counts* $MODELDIR
mv $DIR/pmi* $MODELDIR
mv $DIR/svd* $MODELDIR

#3 get results for ppmi and svd models
./get_results_ppmi_svd.sh $UUID $MODELDIR $RESDIR 5 0.0 

echo 'Done evaluating ppmi and svd'

#4 initiate embeddings for word2vec
./initiate_word2vec.sh $MODELDIR/counts.words.vocab $MODELDIR/pinit1 ${DIM}
./initiate_word2vec.sh $MODELDIR/counts.words.vocab $MODELDIR/pinit2 ${DIM}
./initiate_word2vec.sh $MODELDIR/counts.words.vocab $MODELDIR/pinit3 ${DIM}

#5 create and evaluate word2vec with all 3 random initiations and svd
# settings: neg=1, iters=50
# create_word2vec_with_init.sh pairs voc init out size neg iter
./create_word2vec_with_init.sh $MODELDIR/pairs $MODELDIR/counts.words.vocab $MODELDIR/pinit1 $MODELDIR/sgns_rand_pinit1 ${DIM} 1 50
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit1.words
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit1.contexts
./get_results_sgns_model.sh $UUID $MODELDIR/sgns_rand_pinit1 $RESDIR pinit1


echo 'Pinit 1 has been evaluated'

./create_word2vec_with_init.sh $MODELDIR/pairs $MODELDIR/counts.words.vocab $MODELDIR/pinit2 $MODELDIR/sgns_rand_pinit2 ${DIM} 1 50
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit2.words
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit2.contexts
./get_results_sgns_model.sh $UUID $MODELDIR/sgns_rand_pinit2 $RESDIR pinit2

echo 'Pinit 2 has been evaluated'

./create_word2vec_with_init.sh $MODELDIR/pairs $MODELDIR/counts.words.vocab $MODELDIR/pinit3 $MODELDIR/sgns_rand_pinit3 ${DIM} 1 50
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit3.words
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit3.contexts
./get_results_sgns_model.sh $UUID $MODELDIR/sgns_rand_pinit3 $RESDIR pinit3

echo 'Pinit 3 has been evaluated'

./create_word2vec_with_init.sh $MODELDIR/pairs $MODELDIR/counts.words.vocab $MODELDIR/svd.txt $MODELDIR/sgns_svd ${DIM} 1 50
python hyperwords/text2numpy.py $MODELDIR/sgns_svd.words
python hyperwords/text2numpy.py $MODELDIR/sgns_svd.contexts
./get_results_sgns_model.sh $UUID $MODELDIR/sgns_svd $RESDIR svd

cp $MODELDIR/pairs $MODELDIR/pairs-orig
tac $MODELDIR/pairs-orig > $DIR/pairs
mv $DIR/pairs $MODELDIR/pairs


./create_word2vec_with_init.sh $MODELDIR/pairs $MODELDIR/counts.words.vocab $MODELDIR/pinit1 $MODELDIR/sgns_rand_pinit1-rev ${DIM} 1 50
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit1-rev.words
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit1-rev.contexts
./get_results_sgns_model.sh $UUID $MODELDIR/sgns_rand_pinit1-rev $RESDIR pinit1-rev


echo 'Pinit 1 has been evaluated'

./create_word2vec_with_init.sh $MODELDIR/pairs $MODELDIR/counts.words.vocab $MODELDIR/pinit2 $MODELDIR/sgns_rand_pinit2-rev ${DIM} 1 50
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit2-rev.words
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit2-rev.contexts
./get_results_sgns_model.sh $UUID $MODELDIR/sgns_rand_pinit2-rev $RESDIR pinit2-rev

echo 'Pinit 2 has been evaluated'

./create_word2vec_with_init.sh $MODELDIR/pairs $MODELDIR/counts.words.vocab $MODELDIR/pinit3 $MODELDIR/sgns_rand_pinit3-rev ${DIM} 1 50
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit3-rev.words
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit3-rev.contexts
./get_results_sgns_model.sh $UUID $MODELDIR/sgns_rand_pinit3-rev $RESDIR pinit3-rev

echo 'Pinit 3 has been evaluated'

./create_word2vec_with_init.sh $MODELDIR/pairs $MODELDIR/counts.words.vocab $MODELDIR/svd.txt $MODELDIR/sgns_svd-rev ${DIM} 1 50
python hyperwords/text2numpy.py $MODELDIR/sgns_svd-rev.words
python hyperwords/text2numpy.py $MODELDIR/sgns_svd-rev.contexts
./get_results_sgns_model.sh $UUID $MODELDIR/sgns_svd-rev $RESDIR svd-rev


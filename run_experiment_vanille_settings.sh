#!/bin/sh


# Generate unique id to distinguish between runs:
start=$(date "+%F-%T")
UUID='run'.$start
IN=$1
DIR=$2
MODELDIR=$DIR/$UUID
RESDIR=$3

mkdir -p $MODELDIR
mkdir -p $RESDIR$UUID


#0 create setup.txt file with command that led to the results

echo "./run_experiment_vanille_settings.sh $1 $2 $3" > $3$UUID/setup.txt


#1. create pairs (win=2, dyn=None, sub=None) and counts
./clean_data_2_pairs_and_counts.sh $IN $MODELDIR 2

#2 create ppmi and svd models (neg=1, cds=1, eig=0, dim=500)
# get_ppmi_and_svd_print_out.sh dir cds dim neg eig
./get_ppmi_and_svd_print_out.sh $MODELDIR 1.0 500 1 0.0

#3 get results for ppmi and svd models
./get_results_ppmi_svd.sh $UUID $MODELDIR $RESDIR 1 0.0 

echo 'Done evaluating ppmi and svd'

#4 initiate embeddings for word2vec
./initiate_word2vec.sh $MODELDIR/counts.words.vocab $MODELDIR/pinit1
./initiate_word2vec.sh $MODELDIR/counts.words.vocab $MODELDIR/pinit2
./initiate_word2vec.sh $MODELDIR/counts.words.vocab $MODELDIR/pinit3

#5 create and evaluate word2vec with all 3 random initiations and svd
# settings: size=500, neg=1, iters=50
# create_word2vec_with_init.sh pairs voc init out size neg iter
./create_word2vec_with_init.sh $MODELDIR/pairs $MODELDIR/counts.words.vocab $MODELDIR/pinit1 $MODELDIR/sgns_rand_pinit1 500 1 50
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit1.words
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit1.contexts
./get_results_sgns_model.sh $UUID $MODELDIR/sgns_rand_pinit1 $RESDIR pinit1


echo 'Pinit 1 has been evaluated'

./create_word2vec_with_init.sh $MODELDIR/pairs $MODELDIR/counts.words.vocab $MODELDIR/pinit2 $MODELDIR/sgns_rand_pinit2 500 1 50
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit2.words
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit2.contexts
./get_results_sgns_model.sh $UUID $MODELDIR/sgns_rand_pinit2 $RESDIR pinit2

echo 'Pinit 2 has been evaluated'

./create_word2vec_with_init.sh $MODELDIR/pairs $MODELDIR/counts.words.vocab $MODELDIR/pinit3 $MODELDIR/sgns_rand_pinit3 500 1 50
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit3.words
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit3.contexts
./get_results_sgns_model.sh $UUID $MODELDIR/sgns_rand_pinit3 $RESDIR pinit3

echo 'Pinit 3 has been evaluated'

./create_word2vec_with_init.sh $MODELDIR/pairs $MODELDIR/counts.words.vocab $MODELDIR/svd.txt $MODELDIR/sgns_svd 500 1 50
python hyperwords/text2numpy.py $MODELDIR/sgns_svd.words
python hyperwords/text2numpy.py $MODELDIR/sgns_svd.contexts
./get_results_sgns_model.sh $UUID $MODELDIR/sgns_svd $RESDIR svd

echo 'svd initiation has been evaluated'

#creating reversed ordered corpus
mv $MODELDIR/pairs $MODELDIR/pairs-orig
tac $MODELDIR/pairs-orig > /data/pairs
mv /data/pairs $MODELDIR/pairs

# running word2vec with reversed data models
./create_word2vec_with_init.sh $MODELDIR/pairs $MODELDIR/counts.words.vocab $MODELDIR/pinit1 $MODELDIR/sgns_rand_pinit1-rev 500 1 50
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit1-rev.words
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit1-rev.contexts
./get_results_sgns_model.sh $UUID $MODELDIR/sgns_rand_pinit1-rev $RESDIR pinit1-rev


echo 'Pinit 1 has been evaluated'

./create_word2vec_with_init.sh $MODELDIR/pairs $MODELDIR/counts.words.vocab $MODELDIR/pinit2 $MODELDIR/sgns_rand_pinit2-rev 500 1 50
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit2-rev.words
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit2-rev.contexts
./get_results_sgns_model.sh $UUID $MODELDIR/sgns_rand_pinit2-rev $RESDIR pinit2-rev

echo 'Pinit 2 has been evaluated'

./create_word2vec_with_init.sh $MODELDIR/pairs $MODELDIR/counts.words.vocab $MODELDIR/pinit3 $MODELDIR/sgns_rand_pinit3-rev 500 1 50
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit3-rev.words
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit3-rev.contexts
./get_results_sgns_model.sh $UUID $MODELDIR/sgns_rand_pinit3-rev $RESDIR pinit3-rev

echo 'Pinit 3 has been evaluated'

./create_word2vec_with_init.sh $MODELDIR/pairs $MODELDIR/counts.words.vocab $MODELDIR/svd.txt $MODELDIR/sgns_svd-rev 500 1 50
python hyperwords/text2numpy.py $MODELDIR/sgns_svd-rev.words
python hyperwords/text2numpy.py $MODELDIR/sgns_svd-rev.contexts
./get_results_sgns_model.sh $UUID $MODELDIR/sgns_svd-rev $RESDIR svd-rev

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

echo "./run_experiment_recommended_w2_settings.sh $1 $2 $3" > $RESDIR$UUID/setup.txt

#1. create pairs (win=2, dyn=dirty, sub=10^-5) and counts
./clean_data_2_sub_dirty_pairs_and_counts.sh $IN $MODELDIR 2 1e-5

#2 create ppmi and svd models (neg=5, cds=0.75, eig=0, dim=500)
# get_ppmi_and_svd_print_out.sh dir cds dim neg eig
#./get_ppmi_and_svd_print_out.sh $MODELDIR 0.75 500 5 0.0

#3 get results for ppmi and svd models
#./get_results_ppmi_svd.sh $UUID $MODELDIR $RESDIR 1 0.0

echo 'Done evaluating ppmi and svd'

#4 initiate embeddings for word2vec

./initiate_word2vec.sh $MODELDIR/counts.words.vocab $MODELDIR/pinit4
./initiate_word2vec.sh $MODELDIR/counts.words.vocab $MODELDIR/pinit5
./initiate_word2vec.sh $MODELDIR/counts.words.vocab $MODELDIR/pinit6
./initiate_word2vec.sh $MODELDIR/counts.words.vocab $MODELDIR/pinit7
./initiate_word2vec.sh $MODELDIR/counts.words.vocab $MODELDIR/pinit8
./initiate_word2vec.sh $MODELDIR/counts.words.vocab $MODELDIR/pinit9
./initiate_word2vec.sh $MODELDIR/counts.words.vocab $MODELDIR/pinit10

#5 create and evaluate word2vec with all 3 random initiations and svd
# settings: size=500, neg=1, iters=50
# create_word2vec_with_init.sh pairs voc init out size neg iter

./create_word2vec_with_init.sh $MODELDIR/pairs $MODELDIR/counts.words.vocab $MODELDIR/pinit4 $MODELDIR/sgns_rand_pinit4 500 1 50
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit4.words
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit4.contexts
./get_results_sgns_model.sh $UUID $MODELDIR/sgns_rand_pinit4 $RESDIR pinit4


echo 'Pinit 4 has been evaluated'

./create_word2vec_with_init.sh $MODELDIR/pairs $MODELDIR/counts.words.vocab $MODELDIR/pinit5 $MODELDIR/sgns_rand_pinit5 500 1 50
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit5.words
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit5.contexts
./get_results_sgns_model.sh $UUID $MODELDIR/sgns_rand_pinit5 $RESDIR pinit5

echo 'Pinit 5 has been evaluated'

./create_word2vec_with_init.sh $MODELDIR/pairs $MODELDIR/counts.words.vocab $MODELDIR/pinit6 $MODELDIR/sgns_rand_pinit6 500 1 50
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit6.words
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit6.contexts
./get_results_sgns_model.sh $UUID $MODELDIR/sgns_rand_pinit6 $RESDIR pinit6

echo 'Pinit 6 has been evaluated'

./create_word2vec_with_init.sh $MODELDIR/pairs $MODELDIR/counts.words.vocab $MODELDIR/pinit7 $MODELDIR/sgns_rand_pinit7 500 1 50
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit7.words
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit7.contexts
./get_results_sgns_model.sh $UUID $MODELDIR/sgns_rand_pinit7 $RESDIR pinit7

echo 'Pinit 7 has been evaluated'

./create_word2vec_with_init.sh $MODELDIR/pairs $MODELDIR/counts.words.vocab $MODELDIR/pinit8 $MODELDIR/sgns_rand_pinit8 500 1 50
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit8.words
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit8.contexts
./get_results_sgns_model.sh $UUID $MODELDIR/sgns_rand_pinit8 $RESDIR pinit8


echo 'Pinit 8 has been evaluated'

./create_word2vec_with_init.sh $MODELDIR/pairs $MODELDIR/counts.words.vocab $MODELDIR/pinit9 $MODELDIR/sgns_rand_pinit9 500 1 50
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit9.words
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit9.contexts
./get_results_sgns_model.sh $UUID $MODELDIR/sgns_rand_pinit5 $RESDIR pinit9

echo 'Pinit 9 has been evaluated'

./create_word2vec_with_init.sh $MODELDIR/pairs $MODELDIR/counts.words.vocab $MODELDIR/pinit10 $MODELDIR/sgns_rand_pinit10 500 1 50
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit10.words
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit10.contexts
./get_results_sgns_model.sh $UUID $MODELDIR/sgns_rand_pinit10 $RESDIR pinit10

echo 'Pinit 10 has been evaluated'

# Don't initiate with SVD:

#./create_word2vec_with_init.sh $MODELDIR/pairs $MODELDIR/counts.words.vocab $MODELDIR/svd.txt $MODELDIR/sgns_svd 500 1 50
#python hyperwords/text2numpy.py $MODELDIR/sgns_svd.words
#python hyperwords/text2numpy.py $MODELDIR/sgns_svd.contexts
#./get_results_sgns_model.sh $UUID $MODELDIR/sgns_svd $RESDIR svd


# Reverse order of examples (tac prints file upside down)
cp $MODELDIR/pairs $MODELDIR/pairs-orig
tac $MODELDIR/pairs-orig > /data/pairs
mv /data/pairs $MODELDIR/pairs



./create_word2vec_with_init.sh $MODELDIR/pairs $MODELDIR/counts.words.vocab $MODELDIR/pinit4 $MODELDIR/sgns_rand_pinit4-rev 500 1 50
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit4-rev.words
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit4-rev.contexts
./get_results_sgns_model.sh $UUID $MODELDIR/sgns_rand_pinit4-rev $RESDIR pinit4-rev


echo 'Pinit 4-rev has been evaluated'

./create_word2vec_with_init.sh $MODELDIR/pairs $MODELDIR/counts.words.vocab $MODELDIR/pinit5 $MODELDIR/sgns_rand_pinit5-rev 500 1 50
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit5-rev.words
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit5-rev.contexts
./get_results_sgns_model.sh $UUID $MODELDIR/sgns_rand_pinit5-rev $RESDIR pinit5-rev

echo 'Pinit 5-rev has been evaluated'

./create_word2vec_with_init.sh $MODELDIR/pairs $MODELDIR/counts.words.vocab $MODELDIR/pinit6 $MODELDIR/sgns_rand_pinit6-rev 500 1 50
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit6-rev.words
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit6-rev.contexts
./get_results_sgns_model.sh $UUID $MODELDIR/sgns_rand_pinit6-rev $RESDIR pinit6-rev

echo 'Pinit 6-rev has been evaluated'

./create_word2vec_with_init.sh $MODELDIR/pairs $MODELDIR/counts.words.vocab $MODELDIR/pinit7 $MODELDIR/sgns_rand_pinit7-rev 500 1 50
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit7-rev.words
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit7-rev.contexts
./get_results_sgns_model.sh $UUID $MODELDIR/sgns_rand_pinit7-rev $RESDIR pinit7-rev

echo 'Pinit 7-rev has been evaluated'

./create_word2vec_with_init.sh $MODELDIR/pairs $MODELDIR/counts.words.vocab $MODELDIR/pinit8 $MODELDIR/sgns_rand_pinit8-rev 500 1 50
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit8-rev.words
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit8-rev.contexts
./get_results_sgns_model.sh $UUID $MODELDIR/sgns_rand_pinit8-rev $RESDIR pinit8-rev


echo 'Pinit 8-rev has been evaluated'

./create_word2vec_with_init.sh $MODELDIR/pairs $MODELDIR/counts.words.vocab $MODELDIR/pinit9 $MODELDIR/sgns_rand_pinit9-rev 500 1 50
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit9-rev.words
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit9-rev.contexts
./get_results_sgns_model.sh $UUID $MODELDIR/sgns_rand_pinit9-rev $RESDIR pinit9-rev

echo 'Pinit 9-rev has been evaluated'

./create_word2vec_with_init.sh $MODELDIR/pairs $MODELDIR/counts.words.vocab $MODELDIR/pinit10 $MODELDIR/sgns_rand_pinit10-rev 500 1 50
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit10-rev.words
python hyperwords/text2numpy.py $MODELDIR/sgns_rand_pinit10-rev.contexts
./get_results_sgns_model.sh $UUID $MODELDIR/sgns_rand_pinit10-rev $RESDIR pinit10-rev

echo 'Pinit 10-rev has been evaluated'

# Don't initiate with SVD reversed

#./create_word2vec_with_init.sh $MODELDIR/pairs $MODELDIR/counts.words.vocab $MODELDIR/svd.txt $MODELDIR/sgns_svd-rev 500 1 50
#python hyperwords/text2numpy.py $MODELDIR/sgns_svd-rev.words
#python hyperwords/text2numpy.py $MODELDIR/sgns_svd-rev.contexts
#./get_results_sgns_model.sh $UUID $MODELDIR/sgns_svd-rev $RESDIR svd-rev

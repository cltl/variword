#!/bin/sh

# Generate unique id to distinguish between runs:
export UUID=$(uuidgen)

DATADIR=$1
mkdir $DATADIR/$UUID
export RUNDIR=$DATADIR/$UUID
CORPUS=$2
RESULTSDIR=$3/$UUID

mkdir $1
mkdir $RUNDIR
mkdir $3
mkdir $RESULTSDIR

echo 'this is the cleaned corpus:'
echo $CORPUS

# Download and install word2vecf
mkdir word2vecf
wget https://bitbucket.org/yoavgo/word2vecf/get/1b94252a58d4.zip
unzip 1b94252a58d4.zip
rm 1b94252a58d4.zip
mv yoavgo-word2vecf-1b94252a58d4/*.c word2vecf/.
mv yoavgo-word2vecf-1b94252a58d4/*.h word2vecf/.
mv yoavgo-word2vecf-1b94252a58d4/makefile word2vecf/.
rm -r yoavgo-word2vecf-1b94252a58d4

chmod 755 . *.sh -R

make -C word2vecf

echo "# Create two example collections of word-context pairs:"

echo "# A) Window size 2 with 'clean' subsampling"
mkdir $RUNDIR/w2.sub
python hyperwords/corpus2pairs.py --win 2 --sub 1e-5 $CORPUS > $RUNDIR/w2.sub/pairs
scripts/pairs2counts.sh $RUNDIR/w2.sub/pairs > $RUNDIR/w2.sub/counts
python hyperwords/counts2vocab.py $RUNDIR/w2.sub/counts

echo "# B) Window size 5 with dynamic contexts and 'dirty' subsampling"
mkdir $RUNDIR/w5.dyn.sub.del
python hyperwords/corpus2pairs.py --win 5 --dyn --sub 1e-5 --del $CORPUS > $RUNDIR/w5.dyn.sub.del/pairs
scripts/pairs2counts.sh $RUNDIR/w5.dyn.sub.del/pairs > $RUNDIR/w5.dyn.sub.del/counts
python hyperwords/counts2vocab.py $RUNDIR/w5.dyn.sub.del/counts

echo "# Calculate PMI matrices for each collection of pairs"
python hyperwords/counts2pmi.py --cds 0.75 $RUNDIR/w2.sub/counts $RUNDIR/w2.sub/pmi
python hyperwords/counts2pmi.py --cds 0.75 $RUNDIR/w5.dyn.sub.del/counts $RUNDIR/w5.dyn.sub.del/pmi


echo "# Create embeddings with SVD"
python hyperwords/pmi2svd.py --dim 500 --neg 5 $RUNDIR/w2.sub/pmi $RUNDIR/w2.sub/svd
cp $RUNDIR/w2.sub/pmi.words.vocab $RUNDIR/w2.sub/svd.words.vocab
cp $RUNDIR/w2.sub/pmi.contexts.vocab $RUNDIR/w2.sub/svd.contexts.vocab
python hyperwords/pmi2svd.py --dim 500 --neg 5 $RUNDIR/w5.dyn.sub.del/pmi $RUNDIR/w5.dyn.sub.del/svd
cp $RUNDIR/w5.dyn.sub.del/pmi.words.vocab $RUNDIR/w5.dyn.sub.del/svd.words.vocab
cp $RUNDIR/w5.dyn.sub.del/pmi.contexts.vocab $RUNDIR/w5.dyn.sub.del/svd.contexts.vocab


echo "# Create embeddings with SGNS (A). Commands 2-5 are necessary for loading the vectors with embeddings.py"
word2vecf/word2vecf -train $RUNDIR/w2.sub/pairs -pow 0.75 -cvocab $RUNDIR/w2.sub/counts.contexts.vocab -wvocab $RUNDIR/w2.sub/counts.words.vocab -dumpcv $RUNDIR/w2.sub/sgns.contexts -output $RUNDIR/w2.sub/sgns.words -threads 10 -negative 15 -size 500;
python hyperwords/text2numpy.py $RUNDIR/w2.sub/sgns.words
#rm w2.sub/sgns.words
python hyperwords/text2numpy.py $RUNDIR/w2.sub/sgns.contexts
#rm w2.sub/sgns.contexts

echo "# Create embeddings with SGNS (B). Commands 2-5 are necessary for loading the vectors with embeddings.py"
word2vecf/word2vecf -train $RUNDIR/w5.dyn.sub.del/pairs -pow 0.75 -cvocab $RUNDIR/w5.dyn.sub.del/counts.contexts.vocab -wvocab $RUNDIR/w5.dyn.sub.del/counts.words.vocab -dumpcv $RUNDIR/w5.dyn.sub.del/sgns.contexts -output $RUNDIR/w5.dyn.sub.del/sgns.words -threads 10 -negative 15 -size 500;
python hyperwords/text2numpy.py $RUNDIR/w5.dyn.sub.del/sgns.words
#rm w5.dyn.sub.del/sgns.words
python hyperwords/text2numpy.py $RUNDIR/w5.dyn.sub.del/sgns.contexts
#rm w5.dyn.sub.del/sgns.contexts


echo "# Evaluate on Word Similarity"


sh evaluation.sh $UUID $DATADIR $RESULTSDIR

## Important Note

This repository contains code written by third parties in addition to our own. Please make sure to credit the right people when using (parts of) this code. In case of doubt, please ask (antske.fokkens@vu.nl).

## Warning

This is word in progress! As you can probably see, this repository has not been cleaned (yet) and documentation is (still) limited.

This repository provides the experimental setup for studying the impact of initialization and the order of examples while training word2vec.

It contains modified scripts originally provided by Omer Levy: https://bitbucket.org/omerlevy/hyperwords

For questions about the programs (and particularly the modifications we made) in this repository please contact:

* Antske Fokkens: antske.fokkens@vu.nl
* Minh Le:	m.n.le@vu.nl

## How to use:

### Clean the corpus:

```
    corpus=news1k.shuffled
    scripts/clean_corpus.sh $CORPUS > $CORPUS.clean
```

### Build our modified version of word2vec

cd word2vecf
sudo apt-get install build-essential libc6-dev
make

### Run the pipeline

Then start the pipeline:


```
    modified_pipeline.sh $DATADIR $CORPUS.clean $RESULTSDIR
```

Example:

```
    modified_pipeline /data corpora/news1k.shuffled.clean results
```

## Requirements

* docopt
* sparsesvd
* numpy
* scipy
* sklearn
* pandas

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

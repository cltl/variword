
Forked and severely adapted from [histwords](https://github.com/williamleif/histwords) repo. It is unfortunately still using python 2.7...

# How to use

```

    python2 align_models.py /path/to/models/ prefix

```

## example

```
    $ python2 align_models.py /home/leon/histwords/MODELS/wiki_100M_recom/run.2017-02-01-10:05:16 sgns_rand_pinit
```

# What does it do?

The script first aligns the models that it finds in an directory, all starting with the specified prefix. Then it aligns them to each other and outputs them in the `output` folder. Then, it processes the entire vocabulary and outputs the cosine distance between the word in two embeddings. Values are written to `results.csv`.

Similar vector spacing would return a distance of 1. Values are saved with a precision of 17 decimals, and that is also the standard representation in python2 when displaying a float. 

Try to run it in an ipython notebook (e.g. `run align_models.py %arguments%`, then you can inspect dictionary `results` and pandas.df `df`. 




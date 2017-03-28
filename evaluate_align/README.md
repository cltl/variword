
Forked and severely adapted from [histwords](https://github.com/williamleif/histwords) repo. It is unfortunately still using python 2.7...

# How to use

```

    python2 align_models.py /path/to/file/with/models.txt outfolder

```

## example

```
    $ python2 align_models.py /home/leon/wiki_100M_recom/run.2017-02-01-10:05:16/listofmodels.txt output
```

## example of listofmodels.txt
The file should contain pointers to .words.npy files as outputted by the hyperwords code. 
```
    /home/leon/wiki_100M_recom/run.2017-02-01-10:05:16/sgns_rand_pinit1-rev.words.npy
    /home/leon/wiki_100M_recom/run.2017-02-01-10:05:16/sgns_rand_pinit2-rev.words.npy
    /home/leon/wiki_100M_recom/run.2017-02-01-10:05:16/sgns_rand_pinit3-rev.words.npy
    /home/leon/wiki_100M_recom/run.2017-02-01-10:05:16/sgns_rand_pinit1.words.npy
    /home/leon/wiki_100M_recom/run.2017-02-01-10:05:16/sgns_rand_pinit2.words.npy
    /home/leon/wiki_100M_recom/run.2017-02-01-10:05:16/sgns_rand_pinit3.words.npy
```

# What does it do?

The script first aligns the models from the specified file (can be absolute paths or relative paths. In the latter case, the program uses the location of the input file as directory for the models). Then it aligns them to each other and outputs them in the specified `output` folder. Then, it processes the entire vocabulary and outputs the cosine distance between the word in two embeddings. Values are written to `results.csv`.

Similar vector spacing would return a distance of 0. Values are saved with a precision of 17 decimals, the standard representation in python2 when displaying a float. 

Try to run it in an ipython notebook (e.g. `run align_models.py %arguments%`, then you can inspect dictionary `results` and pandas.df `df`. 




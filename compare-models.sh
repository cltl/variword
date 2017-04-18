cd hyperwords
DIR=~/scistor2/group/projects/variword/wikipedia-material/wiki_experiments/wiki_100M_recom/run.2017-02-01-10\:05\:16
python -u -m eval.compare $DIR/sgns_rand_pinit1.words $DIR/sgns_rand_pinit2.words

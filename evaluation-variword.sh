cd hyperwords
DIR=~/scistor/group/projects/variword/wikipedia-material/wiki_experiments/wiki_100M_recom/run.2017-02-01-10\:05\:16
python -u -m eval.eval_all $DIR/sgns_rand_pinit1.words      
python -u -m eval.eval_all $DIR/sgns_rand_pinit2.words      
python -u -m eval.eval_all $DIR/sgns_rand_pinit3.words      
python -u -m eval.eval_all $DIR/sgns_rand_pinit1-rev.words  
python -u -m eval.eval_all $DIR/sgns_rand_pinit2-rev.words  
python -u -m eval.eval_all $DIR/sgns_rand_pinit3-rev.words  
python -u -m eval.eval_all $DIR/sgns_svd.words
python -u -m eval.eval_all $DIR/sgns_svd-rev.words

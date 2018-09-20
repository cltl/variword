#!/bin/bash
#Usage: to be run inside the wikiextractor folder on scistor

mkdir -p wikipedia-dump

wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2

mv enwiki-latest-pages-articles.xml.bz2 ./wikipedia-dump/

mkdir -p wikipedia-out 

#for file in ./wikipedia-dump/*.bz2;
for file in /mnt/scistor1/group/projects/variword/wikipedia-material/wikiextractor/wikipedia-dump/*.bz2;
do
	echo "Running WikiExtractor $file"
	python WikiExtractor.py -c -o wikipedia-out $file
done

cat ./wikipedia-out/*/*.bz2 > wikipages_full.bz2

bzip2 -d wikipages_full.bz2

sed '/^$/d' wikipages_full | sed '/^<doc/d' | sed '/^<\/doc>/d' > wikipages_full_ordered.txt

#perl -MList::Util=shuffle -e 'print shuffle(<STDIN>);' < wikipages_full_ordered.txt > wikipages_full_shuffled.txt

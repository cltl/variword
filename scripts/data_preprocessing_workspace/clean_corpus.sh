#!/bin/sh
#iconv -c -f utf-8 -t ascii $1 | tr '[A-Z]' '[a-z]' | sed "s/[^a-z0-9]*[ \t\n\r][^a-z0-9]*/ /g" | sed "s/[^a-z0-9]*$/ /g" | sed "s/  */ /g"
## NEW VERSION - 2018-08-09 Author: Tommaso Caselli

# convert the wikipedia data from UTF-8 to ASCII
echo "Converting to ASCII"
iconv -c -f utf-8 -t ascii $1 > $1.ascii

echo "Tokenize data"
perl /mnt/scistor1/group/projects/variword/wikipedia-material/wikiextractor/mosesdecoder/scripts/tokenizer/pre-tokenizer.perl $1.ascii | perl /mnt/scistor1/group/projects/variword/wikipedia-material/wikiextractor/mosesdecoder/scripts/tokenizer/tokenizer.perl | perl /mnt/scistor1/group/projects/variword/wikipedia-material/wikiextractor/mosesdecoder/scripts/tokenizer/deescape-special-chars.perl > $1.ascii.tokenize


echo "Remove punctuaction and split per sentence"
sed -i 's/[][,:;/\\"()-^*]\+//g' $1.ascii.tokenize
sed -i 's/[[:blank:]]\.[[:blank:]]/ \. \n/g' $1.ascii.tokenize

# remove duplicate sentences
echo "Remove duplicate sentences"
python2 remove_duplicate_lines.py $1.ascii.tokenize

# lowercase all
echo "lowercasing"
tr '[A-Z]' '[a-z]' < $1.ascii.tokenize.no-duplicates > $1.ascii.tokenize.no-duplicates.lower 

# shuffle the order of sentences
echo "Shuffle corpus"
perl -MList::Util=shuffle -e 'print shuffle(<STDIN>);' < $1.ascii.tokenize.no-duplicates.lower > $1.ascii.tokenize.no-duplicates.lower.shuffled.txt


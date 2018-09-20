#!/bin/bash
# Create wikipages subcorpora
# Ratio word/sentences computed using wc is 21,02, rounded to 21
# All subcorpora approximates the amount of tokens reported
# All subcorpora have been created on the shuffled wikipedia pages - after pre-processing (ascii, tokenization with moses, remove punctuation, removed duplicate sentences, lowercase)

# 120k
head -2858 wikipages_full_shuffled.txt.ascii.tokenize.no-duplicates.lower > head_out
tail -2858 wikipages_full_shuffled.txt.ascii.tokenize.no-duplicates.lower > tail_out
cat head_out tail_out > ./wikipedia-subcorpora/120k.txt
# 750k - wrong
#head -17588 wikipages_full_shuffled.txt.ascii.tokenize.no-duplicates.lower > head_out
#tail -17588 wikipages_full_shuffled.txt.ascii.tokenize.no-duplicates.lower > tail_out
#cat head_out tail_out > ./wikipedia-subcorpora/750k.txt
#750k - correct 20180830
head -17857 wikipages_full_shuffled.txt.ascii.tokenize.no-duplicates.lower > head_out
tail -17857 wikipages_full_shuffled.txt.ascii.tokenize.no-duplicates.lower > tail_out
cat head_out tail_out > ./wikipedia-subcorpora/750k.txt
# 2M
head -47619 wikipages_full_shuffled.txt.ascii.tokenize.no-duplicates.lower > head_out
tail -47619 wikipages_full_shuffled.txt.ascii.tokenize.no-duplicates.lower > tail_out
cat head_out tail_out > ./wikipedia-subcorpora/2M.txt
# 5M
head -119048 wikipages_full_shuffled.txt.ascii.tokenize.no-duplicates.lower > head_out
tail -119048 wikipages_full_shuffled.txt.ascii.tokenize.no-duplicates.lower > tail_out
cat head_out tail_out > ./wikipedia-subcorpora/5M.txt
# 15M
head -357143 wikipages_full_shuffled.txt.ascii.tokenize.no-duplicates.lower > head_out
tail -357143 wikipages_full_shuffled.txt.ascii.tokenize.no-duplicates.lower > tail_out
cat head_out tail_out > ./wikipedia-subcorpora/15M.txt
# 20M
head -476190 wikipages_full_shuffled.txt.ascii.tokenize.no-duplicates.lower > head_out
tail -476190 wikipages_full_shuffled.txt.ascii.tokenize.no-duplicates.lower > tail_out
cat head_out tail_out > ./wikipedia-subcorpora/20M.txt
# 50M
head -1190476 wikipages_full_shuffled.txt.ascii.tokenize.no-duplicates.lower > head_out
tail -1190476 wikipages_full_shuffled.txt.ascii.tokenize.no-duplicates.lower > tail_out
cat head_out tail_out > ./wikipedia-subcorpora/50M.txt
# 100M
head -2380952 wikipages_full_shuffled.txt.ascii.tokenize.no-duplicates.lower > head_out
tail -2380952 wikipages_full_shuffled.txt.ascii.tokenize.no-duplicates.lower > tail_out
cat head_out tail_out > ./wikipedia-subcorpora/100M.txt
# 200M
head -4761904 wikipages_full_shuffled.txt.ascii.tokenize.no-duplicates.lower > head_out
tail -4761904 wikipages_full_shuffled.txt.ascii.tokenize.no-duplicates.lower > tail_out
cat head_out tail_out > ./wikipedia-subcorpora/200M.txt
# 300M
head -7142857 wikipages_full_shuffled.txt.ascii.tokenize.no-duplicates.lower > head_out
tail -7142857 wikipages_full_shuffled.txt.ascii.tokenize.no-duplicates.lower > tail_out
cat head_out tail_out > ./wikipedia-subcorpora/300M.txt
# 500M
head -11904762 wikipages_full_shuffled.txt.ascii.tokenize.no-duplicates.lower > head_out
tail -11904762 wikipages_full_shuffled.txt.ascii.tokenize.no-duplicates.lower > tail_out
cat head_out tail_out > ./wikipedia-subcorpora/500M.txt
# 750M
head -17857143 wikipages_full_shuffled.txt.ascii.tokenize.no-duplicates.lower > head_out
tail -17857143 wikipages_full_shuffled.txt.ascii.tokenize.no-duplicates.lower > tail_out
cat head_out tail_out > ./wikipedia-subcorpora/750M.txt

rm head_out
rm tail_out

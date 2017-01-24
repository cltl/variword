./create_init -wvocab ../minicounts.words.vocab -cvocab ../minicounts.contexts.vocab -output minicounts.pinit1.bin
./create_init -wvocab ../minicounts.words.vocab -cvocab ../minicounts.contexts.vocab -output minicounts.pinit2.bin
./create_init -wvocab ../minicounts.words.vocab -cvocab ../minicounts.contexts.vocab -output minicounts.pinit3.bin
python hyperwords/pmi2svd_model_printout.py --dim 50 minipmi minisvd

word2vecf/word2vecf_var -train minipairs -pow 0.75 -cvocab minicounts.contexts.vocab -wvocab minicounts.words.vocab -output miniembeddings1.txt -threads 10 -negative 15 -size 500 -pinit minicounts.pinit1.bin
word2vecf/word2vecf_var -train minipairs -pow 0.75 -cvocab minicounts.contexts.vocab -wvocab minicounts.words.vocab -output miniembeddings2.txt -threads 10 -negative 15 -size 500 -pinit minicounts.pinit2.bin
word2vecf/word2vecf_var -train minipairs -pow 0.75 -cvocab minicounts.contexts.vocab -wvocab minicounts.words.vocab -output miniembeddings3.txt -threads 10 -negative 15 -size 500 -pinit minicounts.pinit3.bin
word2vecf/word2vecf_var -train minipairs -pow 0.75 -cvocab minicounts.contexts.vocab -wvocab minicounts.words.vocab -output miniembeddings4.txt -threads 10 -negative 15 -size 50 -pinit minisvd.txt
modified pipeline:

[init step]

repeat 10 times:
  word2vecf/create_init -wvocab <word_vocab_file> -cvocab <context_vocab_file> -output <params_file>

[experiment]

repeat 10 times:
  word2vecf/word2vecf_var -pinit <params_file> <other_options>

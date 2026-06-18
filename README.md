# "HMM, let's try"
## *an implementation of a Hidden Markov Model POS Tagger*

This is an implementation of a Part-Of-Speech Tagger using a Hidden Markov Model. The purpose of this project was purely educational. It is, at present, hard-coded to be tested on the [UD GUM](https://universaldependencies.org/treebanks/en_gum/index.html) test dataset. It reports an accuracy of 83.09% on the same. To see its tagged output, open ```hmm_output.conllu```.
It was trained on UD GUM's training dataset.

The HMM uses the Universal Dependencies Tagset along with auxiliary ```<s>``` and ```</s>``` tags to mark the beginning and end of sentences.

For the student who wants a theoretical understanding of HMMs, ```theory.md``` has a brief note explaining the same.
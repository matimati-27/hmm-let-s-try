# The theory behind how an HMM POS Tagger Works

## What we want to do

Given an utterance, do the most-likely-correct POS tagging of the sentence.
More formally, sequence of words, make a model that assigns the most probable tag to every word. 

## How do we go about this?

For starters, how do we assign a tag to a word? Tag assignment depends on context. How much context? Well, in an ideal world, we can assign a tag to a word based on every word-tag pair that came before it. But realistically, that is an unreasonably huge number of preceding words to consider, especially if the corpus is big. Do we really need all those words? It is better to use a reasonable number $n$, such that the word we are assigning a tag to is the $n^{th}$ word, and we consider the $n - 1$ tags we've already assigned before it. 

## Using Bayes to compute this

A quick recap of Bayes' theorem:
$$P(H | E) = \frac{P(H) P(E | H)} {P(E)}$$
Here, $H$ and $E$ are both conditions. We are evaluating the probability of condition $H$ being satisfied, given that condition $E$ is satisfied. 

*\[I highly recommend [3b1b's lecture](https://youtu.be/HZGCoVF3YvM?si=Icb15IshjzH-9khLhttps://youtu.be/HZGCoVF3YvM?si=Icb15IshjzH-9khL) for a solid feel of Bayes' theorem.]*

We have a given word sequence (evidence). Assume we are 'testing out' tag sequences (and a current tag sequence is our present hypothesis). In the spirit of the Bayesian test, the probability of this - the tag sequence we are probing in hopes of finding the best one for our given word sequence - is, informally,

$\frac{P(this\_n-length\_tag\_sequence) P(this\_particular\_word\_sequence\_with\_this\_particular\_n-length\_tag\_sequence)}{P(finding\_this\_particular\_n-length\_word\_sequence)}$

But this poses several problems. 

## What problems?

First, the probability of any given random utterance (that is, our 'given sequence of $n$ words' that we wish to tag) is pretty much zero. This is because - as you can see - if the size of our vocabulary is $V$, the universe of utterances of length $n$ is $V^n$. Why is that a problem? It comes with a severe impracticality.  

>The Brown Corpus has a vocabulary of at least 50,000 words. The average length of sentences in it can be reasonably estimated at 25, if not higher. You can imagine the magnitude of 'all possible utterances of length 25': $(5 × 10^5)^{25}$. That is of the order of 10 raised to 125. Approximately 100 moles of googols. Haha.
>Even with tags, which are only a handful in number and more predictable in combination, sequences of typical length $n$ grow exceptionally large. Even with just the 17 tags of the UD POS tagset, that would be $17^{25}$ possible tag combinations, which is still of the order 10 raised to 31. Even if the number of permissible combinations is only a handful, we may not be able to account for edge cases, and for creative use of language. Any rules written will be stumped by exceptions. 

This highlights why we need the Markov assumptions. And of course, the productivity and creativity of language. If we proceed with this formula, our HMM will confidently assign a probability of 0 to every tag sequence, and every tag sequence will have an equal probability, so you can pick any one. Which is exactly what we don't want.

Thankfully, we notice that this denominator is a constant. We remember that we are always considering different tag sequences *for the same word sequence*. So this comes out to just be a constant scaling factor for our problem. We remove the denominator to get:

probability of the tag sequence we have in our hands for this given utterance i.e. word sequence = 
$P(this\_n-length\_tag\_sequence) P(finding\_this\_particular\_word\_sequence\_with\_this\_n-length\_tag\_sequence)$

However, the exact same problem crops up in another place - notice the second term of the probability product. The 'probability of these exact words filling up the slots provided by these tags' is rather vacuous. There would be no way of computing that probability - the universe of word sequences is vast, arguably infinite. What is the guarantee that the model has seen the exact same sentence we are asking it to tag now before? Zero. So we need to resolve this problem meaningfully.

## The Markov assumptions

So far we have been looking at a sequence of $n$ words as a sequence of $n$ words, and a sequence of $n$ tags as a sequence of $n$ tags. This is the very thing that had led us to the problem of massive permutations and plummeting probabilities. But if we start looking at smaller groups of words, we lose the high resolution of choosing an $n-word$ context window. If we go to the level of a single word, we may indeed have no context at all. 

How do we reduce our dependency on the length of the observation (which is flattening our probabilities) while also retaining the benefit of a sufficiently-long context window? Here come the crucial Markov assumptions:

1. *Emission assumption.* **A word depends only on its own tag.** 

Note that this means that the probability of the given word sequence i.e. utterance, given the tag sequence we are currently analysing, is just the product of these individual probabilities - of each word, given its particular tag.

2. *Transition assumption.* **A tag depends only on its previous tag.**

And thus, we have our revised probability formula!

$$\hat{t}^n=max(\prod\limits_{i=1}^{n}P(w_i | t_i)P(t_i | t_{i-1}))$$
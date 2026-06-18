import re
import math

TAG_TYPES = 19
SMOOTHING_FACTOR = 1

def main():
    with open("en_gum-ud-train.conllu", "r") as f:
        training_text = f.read().splitlines()

    with open("en_gum-ud-test.conllu", "r") as f:
        testing_text = f.read().splitlines()


    parsed_training_sentences = parser(training_text)
    parsed_testing_sentences = parser(testing_text)

    emission_counts, transition_counts, tag_pairs = countTraining(parsed_training_sentences)
    emission_probabilities, transition_probabilities = probabilities(emission_counts, transition_counts, tag_pairs)
    
    words_sequence = [[word for word, tag in sentence] for sentence in parsed_testing_sentences]
    
    hmm_tagged_corpus = viterbi(words_sequence, emission_counts, emission_probabilities, transition_counts, transition_probabilities, tag_pairs)
    print(len(hmm_tagged_corpus), "sentences tagged by HMM in testing corpus.")

    hmm_test = ""

    with open("hmm_output.conllu", "w") as f:
        for sentence in hmm_tagged_corpus:
            i = 1
            for word, tag in sentence:
                hmm_test += f"{i}\t{word}\t\t{tag}\n"
                i += 1
            hmm_test += f"\n"
        
        f.write(hmm_test)

    accuracy_percent = accuracyCheck(parsed_testing_sentences, hmm_tagged_corpus)
    print("Accuracy =", accuracy_percent, "%")

def parser(text: list) -> list[list]:
    
    words_tags = []

    sentence = [('<s>', '<s>')]
    for line in text:

        if(line):
            all_cols = line.split('\t')

            if(all_cols):                
                if(line[0] == '#'):
                    # print(line)
                    continue

                elif(re.search('-', all_cols[0])):
                    continue
                
                else:
                    sentence.append((all_cols[1], all_cols[3]))
            
        else:
            # new sentence
            sentence.append(('<\s>', '<\s>'))            
            words_tags.append(sentence)
            sentence = [('<s>', '<s>')]
            
    return words_tags    

def countTraining(parsed_sentences: list[list]) -> tuple[dict, dict, dict]:

    emission_counts = {}
    transition_counts = {}
    tag_counts = {}

    for sentence in parsed_sentences:

        for pair in sentence:
            word = pair[0].lower()
            tag = pair[1]
            
            if tag in tag_counts:
                tag_counts[tag] += 1
            else:
                tag_counts[tag] = 1

            if word in emission_counts:
                if tag in emission_counts[word]:
                    emission_counts[word][tag] += 1
                else:   # word is present but never with this tag
                    emission_counts[word].update({tag: 1})
            else:
                emission_counts.update({word: {tag: 1}})

        for i in range(len(sentence) - 1):
            
            tag_1 = sentence[i][1]
            tag_2 = sentence[i + 1][1]
            
            if tag_1 in transition_counts:
                
                if tag_2 in transition_counts[tag_1]:
                    transition_counts[tag_1][tag_2] += 1
                else:
                    transition_counts[tag_1].update({tag_2: 1})
            
            else:
                transition_counts.update({tag_1: {tag_2: 1}})   

    return emission_counts, transition_counts, tag_counts

def probabilities(emission_counts: dict[dict], transition_counts: dict[dict], tag_pairs: dict) -> tuple[dict, dict]:
    
    VOCABULARY_SIZE = len(emission_counts)
    emission_probabilities = {}
    transition_probabilities = {}

    for word in emission_counts:
        emission_probabilities[word] = {}

        for tag in emission_counts[word]:
            log_probability = math.log(emission_counts[word][tag] + SMOOTHING_FACTOR) - math.log(tag_pairs[tag] + (VOCABULARY_SIZE * SMOOTHING_FACTOR))
            emission_probabilities[word].update({tag: log_probability})
        
    for tag1 in transition_counts:
        transition_probabilities[tag1] = {}

        for tag2 in transition_counts[tag1]:
            log_probability = math.log(transition_counts[tag1][tag2] + SMOOTHING_FACTOR) - math.log(tag_pairs[tag1] + (TAG_TYPES * SMOOTHING_FACTOR))
            transition_probabilities[tag1].update({tag2: log_probability})

    return emission_probabilities, transition_probabilities

def viterbi(word_sequence: list, train_emission_counts: dict, train_emission_probabilities: dict,
            train_transition_counts: dict, train_transition_probabilities: dict, train_tag_pairs: dict):
    
    VOCABULARY_SIZE = len(train_emission_counts)
    hmm_tagged_sentences = []

    for sentence in word_sequence:
        
        # dp[][] stores 'highest probability of any prior sequence reaching here'
        # backpointer[][] stores 'previous tag that gave this cell its highest probability'
        
        dp = [[float('-inf')] * TAG_TYPES for _ in range(len(sentence))]
        backpointers = [[None] * TAG_TYPES for _ in range(len(sentence))]

        # map tags to indices
        tags = list(train_tag_pairs.keys())
        tag_indices = {tag: i for i, tag in enumerate(tags)}
        
        dp[0][tag_indices['<s>']] = 0.0  # log(1)

        # perform dp
        for i in range(1, len(sentence)):
            for j in range(len(tags)):
                log_P_emission = (train_emission_probabilities[sentence[i]][tags[j]] 
                              if sentence[i] in train_emission_counts and tags[j] in train_emission_probabilities[sentence[i]] 
                              else math.log(SMOOTHING_FACTOR) - math.log(train_tag_pairs[tags[j]] + VOCABULARY_SIZE * SMOOTHING_FACTOR))
                
                for k in range(len(tags)):
                    log_P_transition = (train_transition_probabilities[tags[k]][tags[j]] 
                                    if tags[k] in train_transition_counts and tags[j] in train_transition_counts[tags[k]]
                                    else math.log(SMOOTHING_FACTOR) - math.log(train_tag_pairs[tags[k]] + TAG_TYPES * SMOOTHING_FACTOR))
                
                    # print(log_P_emission, log_P_transition, dp[i - 1][k], dp[i][j])

                    if dp[i - 1][k] + log_P_transition + log_P_emission > dp[i][j]:
                        dp[i][j] = dp[i - 1][k] + log_P_transition + log_P_emission 
                        backpointers[i][j] = tags[k]                    

        # unfurl backpointers
        current_word_index = len(sentence) - 1
        current_tag = tags[dp[current_word_index].index(max(dp[current_word_index]))]
        tag_sequence = []

        while current_tag != '<s>':
            tag_sequence.insert(0, current_tag)
            current_tag = backpointers[current_word_index][tag_indices[current_tag]]
            current_word_index -= 1
        
        tag_sequence.insert(0, '<s>')
        
        tagged_sentence = [(sentence[i], tag_sequence[i]) for i in range(len(sentence))]
        hmm_tagged_sentences.append(tagged_sentence)
    
    return hmm_tagged_sentences

def accuracyCheck(testing_gold: list, testing_hmm: list):
    
    total_tags = 0
    incorrect_tags = 0
    
    for i in range(len(testing_gold)):
        for j in range(len(testing_gold[i])):
            
            total_tags += 1
            if(testing_gold[i][j] != testing_hmm[i][j]):
                incorrect_tags += 1

    return (1 - (incorrect_tags / total_tags)) * 100

if __name__ == "__main__":
    main()


import re
import math

TAG_TYPES = 19
SMOOTHING_FACTOR = 1

def main():
    with open("en_gum-ud-train.conllu", "r") as f:
        text = f.read().splitlines()

    parsed_sentences = parser(text)
    emission_counts, transition_counts, tag_pairs = countTraining(parsed_sentences)
    emission_probabilities, transition_probabilities = probabilities(emission_counts, transition_counts, tag_pairs)
    words_sequence = [[word for word, tag in sentence] for sentence in parsed_sentences]
    viterbi(words_sequence, emission_counts, emission_probabilities, transition_counts, transition_probabilities, tag_pairs)

def parser(text: list) -> list[list]:
    
    train_words_tags = []

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
                    # print(train_words_tags[-1])
            
        else:
            # new sentence
            sentence.append(('<\s>', '<\s>'))            
            train_words_tags.append(sentence)
            sentence = [('<s>', '<s>')]
            
    return train_words_tags    

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

    for sentence in word_sequence:
        
        # dp[][] stores 'highest probability of any prior sequence reaching here'
        # backpointer[][] stores 'previous tag that gave this cell its highest probability'
        
        dp = [[0] * TAG_TYPES for _ in range(len(sentence))]
        backpointers = [[None] * TAG_TYPES for _ in range(len(sentence))]

        # map tags to indices
        tags = list(train_tag_pairs.keys())
        tag_indices = {tag: i for i, tag in enumerate(tags)}
        
        print(tag_indices)

        dp[0][tag_indices['<s>']] = 0.0  # log(1)
        for i in range(len(tags)):
            if tags[i] != '<s>':
                dp[0][i] = float('-inf')

        for i in range(len(tags)):
            backpointers[0][i] = None

        # perform dp
        for i in range(len(sentence)):
            for j in range(1, len(tags)):
                # P_emission = train_emission_probabilities[sentence[i]] if train_emission_counts[sentence[i]] else SMOOTHING_FACTOR / VOCABULARY_SIZE
                # P_transition = train_transition_probabilities[sentence[i]] if train_transition_counts[]
                pass
    return

if __name__ == "__main__":
    main()


import re

def main():
    parsed_sentences = parser()
    emission_counts, transition_counts = countTraining(parsed_sentences)
    with open("testing.txt", "w+") as f:
        f.write(str(transition_counts))

    
def parser() -> list:
    
    with open("en_gum-ud-train.conllu", "r") as f:
        text = f.read().splitlines()

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

def countTraining(parsed_sentences: list) -> tuple:

    emission_counts = {}
    transition_counts = {}

    for sentence in parsed_sentences:
        for pair in sentence:
            word = pair[0].lower()
            tag = pair[1]

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
    return emission_counts, transition_counts

if __name__ == "__main__":
    main()


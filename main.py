import re

def main():
    pass
    
def parser():
    
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
        
if __name__ == "__main__":
    main()


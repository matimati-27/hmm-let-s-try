def main():
    print(parser())        
    
def parser():
    # PARSER
    
    with open("en_gum-ud-train.conllu", "r") as f:
        TEXT = f.read().splitlines()

    TRAIN_WORDS_TAGS = [('<s>, <s>')]

    for line in TEXT:

        if(line):
            all_cols = line.split('\t')

            if(all_cols):                
                if(line[0] == '#'):
                    # print(line)
                    continue
                
                else:
                    TRAIN_WORDS_TAGS.append((all_cols[1], all_cols[3]))
                    print(TRAIN_WORDS_TAGS[-1])
            
        else:
            # new sentence
            TRAIN_WORDS_TAGS.append(('<\s>', '<\s>'))            
            TRAIN_WORDS_TAGS.append(('<s>', '<s>'))      
            continue  

    return TRAIN_WORDS_TAGS    
        
if __name__ == "__main__":
    main()


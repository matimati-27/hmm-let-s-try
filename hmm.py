## PARSER
with open("en_gum-ud-train.conllu", "r") as f:
	TEXT = f.read().splitlines()


for line in TEXT:
	all_cols = line.split('\t')
	if(all_cols):
		if(all_cols[0] == '#'):
			continue
		for i in range(all_cols):
			
			pass
	else:
		# new sentence
		sentence = []
		
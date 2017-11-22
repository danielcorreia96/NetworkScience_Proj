

with open("tweets00.txt","r") as fin, open("newtweets00.txt","a") as fout:
	for line in fin:
		outline = line.strip().replace('\"','')[1:-1].split(",")
		outline = [item.strip() for item in outline]
		
from collections import Counter

result = ["id_str", "user_id_str", "created_at", "lang", "hashtags", "retweeted_id_str", "retweeted_user_id_str", "retweeted_created_at"]

def clean_tweets():
	open("clean_tweets00.txt","w").close()	 #reset file
	with open("full_data.00.out","r") as fin, open("clean_tweets00.txt","a") as fout:
		fout.write(",".join(result)+"\n")
		for line in fin:
			outline = line.strip()[3:].split("|")
			fout.write(",".join(outline)+"\n")


def get_hashtags(min_count=10):
	hashtags = Counter()
	with open("clean_tweets00.txt","r") as fin:
		for line in fin:
			l1 = line.strip().split(",")
			for tag in l1[4].split("#"):
				hashtags[tag] += 1

		for k in list(hashtags):
			if hashtags[k] < min_count:
				del(hashtags[k])
	return hashtags


def filter_by_language(lang="en"):
	open(lang+"_clean_tweets00.txt","w").close()	 #reset file
	with open("clean_tweets00.txt","r") as fin, open(lang+"_clean_tweets00.txt","a") as fout:
		for line in fin:
			l1 = line.strip().split(",")
			if l1[3] == lang:
				fout.write(",".join(l1)+"\n")
				

import pandas as pd 
import sys
import operator
import re
import matplotlib.pyplot as plt
import networkx as nx

global best_hashtags

def count_hashtags_per_tweet(f1):
	line_num = 1
	max_hashtags = 0
	max_line = 0
	total_hashtags = 0
	count_hashtag_dict = {}
	hashtags_dict = {}
	global best_hashtags
	for line in f1:
		l = line.split(',')
		hashtags = l[4]
		hashtag = hashtags.split('#')
		#num_hashtags = len(hashtag)

		for el in hashtag:
			el_with_hash = "#"+ str(el) + "#"
			if el_with_hash in hashtags_dict:
				hashtags_dict[el_with_hash] = hashtags_dict[el_with_hash] + 1
			else:
				hashtags_dict[el_with_hash] = 1

		# if num_hashtags in count_hashtag_dict:
		# 	count_hashtag_dict[num_hashtags] = count_hashtag_dict[num_hashtags] + 1
		# else:
		# 	count_hashtag_dict[num_hashtags] = 1
		# if num_hashtags > max_hashtags:
		# 	max_hashtags = num_hashtags 
		# 	max_line = line_num
		# #print(str(line_num), num_hashtags)
		# line_num = line_num + 1
		# total_hashtags = total_hashtags + num_hashtags

	#media = total_hashtags / line_num
	sorted_hashtags = sorted(hashtags_dict.items(), key=lambda x: x[1])
	sorted_hashtags.reverse()
	best_hashtags = []
	for el in sorted_hashtags[:10]:
		best_hashtags.append(el[0])
	#print(max_line, max_hashtags, media)
	#rint(count_hashtag_dict)
	#print(best_hashtags)


def process_1_best(f1,name_out,hashtag):
	open(str(name_out)+"_"+str(hashtag)+".txt","w").close()
	fout = open(str(name_out)+"_"+str(hashtag)+".txt","a")
	first_line = True
	for line in f1:
		if first_line:
			fout.write(line)
			first_line = False
		else:
			l = line.split(',')
			hashtags = "#" + str(l[4]) +"#"
			res_search = re.search(str(hashtag), hashtags)
			if res_search != None:
				fout.write(line)
	fout.close()		


def process_best2(f1, name_out):
	open(str(name_out)+".txt","w").close()
	fout = open(str(name_out)+".txt","a")
	first_line = True
	for line in f1:
		if first_line:
			fout.write(line)
			first_line = False
		else:
			l = line.split(',')
			hashtags = "#" + str(l[4]) +"#"
			exists_in_line = False
			for el in best_hashtags:
				res_search = re.search(str(el), hashtags)
				if res_search != None:
					exists_in_line = True
			if exists_in_line:
				fout.write(line)
	fout.close()		


def is_in_best(l):
	for el in l:
		proc_el = "#" + str(el)
		if proc_el in best_hashtags:
			return True
	return False

def day_hashtag(f1, out, mes):
	day_hashtags_dict = {}
	first_line = True
	for line in f1:
		if first_line:
			first_line = False
		else:
			l = line.split(',')
			date = l[2]
			day = int(date.split(" ")[2])
			time = date.split(" ")[3]
			hour = int(time.split(":")[0])
			key = day * 24 + hour
			hashtags = "#" + str(l[4]) +"#"
			for el in best_hashtags:
				res_search = re.search(str(el), hashtags)
				if res_search != None:
					if key < 10 :
						chave = str(el)+"00"+str(key)
					elif key < 100:
						chave = str(el)+"0"+str(key)
					else:
						chave = str(el) + str(key) 
					if chave in day_hashtags_dict:
						day_hashtags_dict[chave] = day_hashtags_dict[chave] + 1
					else:
						day_hashtags_dict[chave] = 1
	sorted_day_hashtags = sorted(day_hashtags_dict.items(), key=lambda x: x[0])
	#graphics_day_hashtags(sorted_day_hashtags, hashtag)
	key1 = (sorted_day_hashtags[0][0].split("#"))[1]
	graphic_list = []
	for el in sorted_day_hashtags:
		if  (el[0].split("#"))[1] != key1:
			graphics_day_hashtags(graphic_list,"#"+str(key1)+"#", out, mes)
			key1 = (el[0].split("#"))[1]
			graphic_list = []
			pair = [(el[0].split("#"))[2],el[1]]
			graphic_list.append(pair)
		else:
			pair = [(el[0].split("#"))[2],el[1]]
			graphic_list.append(pair)
	graphics_day_hashtags(graphic_list,"#"+str(key1)+"#", out, mes)


def graphics_day_hashtags(day_hashtag_list, hashtag, out, mes):
	

	y = [int(el[1]) for el in day_hashtag_list]
	x = [int(el[0]) for el in day_hashtag_list] 
	fig = plt.figure()
	ax1 = fig.add_subplot(111)

	ax1.set_title("Hashtag: "+ str(hashtag[1:-1]))
	ax1.set_xlabel("hour of month")
	ax1.set_ylabel("number of occurrences")

	ax1.plot(x, y, c="r")

	# plt.show()
	# plt.draw()

	f_out = out.split("/")[:4]
	first_out = str(f_out[0]) + "/" + str(f_out[1]) + "/" + str(f_out[2]) + "/" + str(f_out[3])
	second_out = out.split("/")[4]
	plt.savefig(str(first_out) + "/"+ str(mes) + "/"+ str(second_out)+ "_" +str(hashtag[1:-1])+".png")
	plt.close()


def make_graph_hashtag(f):
	G = nx.Graph()
	for line in f:
		l = line.split(",")
		a = l[0]
		b = l[5]
		G.add_node(a)
		G.add_node(b)
		G.add_edge(a,b)
	nx.draw(G)
	plt.show()

if __name__ == '__main__':
	f1 = open(sys.argv[1] , 'r')
	count_hashtags_per_tweet(f1)
	f1.close()
	# for el in best_hashtags:
	# 	f1 = open(sys.argv[1] , 'r')
	# 	process_1_best(f1,sys.argv[2],el)
	# 	f1.close()
	# f = open("./best_hashtags/pt/pt_best_hastags_Apr_#BayernRealMadrid#.txt", 'r')
	# print("Beggining graph")
	# make_graph_hashtag(f)
	#f1 = open(sys.argv[1] , 'r')
	#process_best2(f1, sys.argv[2])
	#f1.close()
	#for el in best_hashtags:
	f1 = open(sys.argv[1] , 'r')
	mes = ((sys.argv[1].split("/"))[2].split("_"))[3].split(".")[0]
	day_hashtag(f1, sys.argv[2], mes)
	f1.close()
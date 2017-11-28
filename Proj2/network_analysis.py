import pandas as pd
import networkx as nx
import pylab as plt
from collections import Counter
import argparse

def extract_network(filename):
	dataset = pd.read_csv(filename)
	graph = dataset[["user_id_str","retweeted_user_id_str"]]
	net = nx.from_pandas_dataframe(graph, "retweeted_user_id_str", "user_id_str", create_using=nx.MultiDiGraph())
	net.name = filename.split("/")[1][:-4]
	print(nx.info(net))
	return net

def do_degree_stuff(graph):
	in_degrees = dict(graph.in_degree())
	in_values = sorted(set(in_degrees.values()))
	in_counts = Counter(in_degrees.values())
	in_hist = [in_counts[x] for x in in_values]


	out_degrees = dict(graph.out_degree())
	out_values = sorted(set(out_degrees.values()))
	out_counts = Counter(out_degrees.values())
	out_hist = [out_counts[x] for x in out_values]


	fig = plt.figure()
	fig.set_figheight(7.5)
	fig.set_figwidth(14)
	ax1 = fig.add_subplot(121)
	ax1.grid(True)
	ax1.plot(in_values, in_hist, "ro")
	ax1.plot(out_values, out_hist, "bv")
	ax1.legend(["In-Degree", "Out-Degree"])
	ax1.set_xlabel("Degree")
	ax1.set_ylabel("Number of nodes")
	# ax1.title()
	# plt.savefig("degree_dist_%s" % (name_id))


	# plt.figure()
	ax2 = fig.add_subplot(122)
	ax2.grid(True)
	ax2.loglog(in_values, in_hist, "ro")
	ax2.loglog(out_values, out_hist, "bv")
	ax2.legend(["In-Degree", "Out-Degree"])
	ax2.set_xlabel("Degree")
	ax2.set_ylabel("Number of nodes")

	plt.suptitle("Degree Distribution for %s" % (graph.name))
	
	plt.savefig("degree_dist_graphs/degdist_%s" % (graph.name))

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("dataset",help="dataset to be processed")
	args = parser.parse_args()

	#graph = extract_network(args.dataset)
	#do_degree_stuff(graph)
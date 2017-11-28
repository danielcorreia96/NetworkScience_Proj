import pandas as pd
import pylab as plt
import argparse
from graph_tool.all import *

def extract_network(filename):
	dataset = pd.read_csv(filename)
	graph = dataset[["retweeted_user_id_str","user_id_str"]]
	net = Graph()
	vmap = net.add_edge_list(graph.values, hashed=True)
	net.name = filename.split("/")[1][:-4]
	return net

def do_degree_stuff(graph):
	in_vals_hist = vertex_hist(graph,"in")
	out_vals_hist = vertex_hist(graph,"out")
	in_values, in_hist = in_vals_hist[1][:-1], in_vals_hist[0]
	out_values, out_hist = out_vals_hist[1][:-1], out_vals_hist[0]

	plt.figure()
	plt.grid(True)
	plt.xlim([10**(-0.5),10**(7)])
	plt.ylim([10**(-0.5),10**(7)])
	plt.loglog(in_values, in_hist, "ro")
	plt.loglog(out_values, out_hist, "bv")
	plt.legend(["In-Degree", "Out-Degree"])
	plt.xlabel("Degree")
	plt.ylabel("Number of nodes")
	plt.suptitle("Log-Log Degree Distribution for %s" % (graph.name))
	
	plt.savefig("degree_dist_graphs/degdist_%s" % (graph.name))



if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("dataset",help="dataset to be processed")
	args = parser.parse_args()

	graph = extract_network(args.dataset)
	# do_degree_stuff(graph)
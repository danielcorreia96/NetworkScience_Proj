import pandas as pd
import pylab as plt
import numpy as np
import argparse
import igraph

def extract_network(filename):
	dataset = pd.read_csv(filename,low_memory=False)
	graph = dataset[["retweeted_user_id_str","user_id_str"]]
	graph = graph.drop_duplicates(subset=['user_id_str', 'retweeted_user_id_str'])
	net = igraph.Graph.TupleList(graph.values, directed=True)
	return net

def do_degree_stuff(graph, graph_name):
	# in-degree distribution
	in_vals_hist = graph.degree_distribution(mode="IN")
	in_values = np.array(list(in_vals_hist.bins()))[:,0]
	in_hist = np.array(list(in_vals_hist.bins()))[:,2]

	in_plfit = igraph.power_law_fit(in_hist)

	# out-degree distribution
	out_vals_hist = graph.degree_distribution(mode="OUT")
	out_values = np.array(list(out_vals_hist.bins()))[:,0]
	out_hist = np.array(list(out_vals_hist.bins()))[:,2]

	out_plfit = igraph.power_law_fit(out_hist)

	f, (ax1, ax2) = plt.subplots(1, 2,sharey=True)
	
	# plt.figure()
	# plt.grid(True)
	#plt.xlim([10**(-0.5),10**(7)])

	#plt.ylim([10**(-0.5),10**(7)])
	# plt.loglog(in_values, in_hist, "ro")
	# plt.loglog(out_values, out_hist, "bv")
	# plt.legend(["In-Degree", "Out-Degree"])
	ax1.grid(True)
	ax1.set_xlabel("In-Degree")
	ax1.set_xlim([10**(-0.5),10**(6)])
	ax1.set_xscale("log")
	ax1.set_ylim([10**(-0.5),10**(7)])
	ax1.set_ylabel("Number of nodes")
	ax1.set_yscale("log")
	ax1.plot(in_values, in_hist, "ro")

	ax2.grid(True)
	ax2.set_xlabel("Out-Degree")
	ax2.set_xlim([10**(-0.5),10**(6)])
	ax2.set_xscale("log")
	ax2.set_ylim([10**(-0.5),10**(7)])
	ax2.set_yscale("log")
	ax2.plot(out_values, out_hist, "bv")
	# plt.suptitle("Log-Log Degree Distribution for %s" % (graph_name))
	# plt.savefig("degree_dist_graphs/degdist_%s" % (graph_name))
	f.suptitle("Log-Log Degree Distribution for %s" % (graph_name))
	f.savefig("degree_dist_graphs/degdist_%s" % (graph_name))

	with open("degree_dist_graphs/degdist_%s.txt" % (graph_name),"w") as fout:
		fout.write("In-degree power law fitting\n"+in_plfit.summary()+"\n")
		fout.write("Out-degree power law fitting\n"+out_plfit.summary()+"\n")

def do_path_length_stuff(graph, graph_name):
	in_vals_hist = graph.path_length_hist()
	in_values = np.array(list(in_vals_hist.bins()))[:,0]
	in_hist = np.array(list(in_vals_hist.bins()))[:,2]

	plt.figure()
	plt.grid(True)
	plt.plot(in_values, in_hist, "ro-")
	plt.legend(["Path Length"])
	plt.xlabel("Path Length")
	plt.ylabel("Number of nodes")
	plt.suptitle("Path Length Distribution for %s" % (graph_name))
	plt.savefig("pathlen_dist_graphs/degdist_%s" % (graph_name))

def print_path_hist(graph,graph_name):
	in_vals_hist = graph.path_length_hist()
	print("Path Length Histogram for %s" % (graph_name))
	print(in_vals_hist)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("dataset",help="dataset to be processed")
	args = parser.parse_args()
	graph = extract_network(args.dataset)
	graph_name = args.dataset.split("/")[1][:-4]
	print("ja carreguei o dataset")
	#do_degree_stuff(graph,graph_name)

	#do_path_length_stuff(graph,graph_name)

	do_rank_stuff(graph,graph_name)
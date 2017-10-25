#!/usr/bin/env python3

import networkx as nx
import os

DATAFOLDER = "datasets/"

def read_datasets_gml():
	datasets = dict()
	for filename in os.listdir(DATAFOLDER):
		try:
			data = nx.read_gml(DATAFOLDER+filename)
			data.name = filename[:-4]
			datasets[data.name] = data
			print(nx.info(data))
			print("--------------------------")
		except Exception as err:
			print(err)
			print("failed to load dataset " + filename +  " in gml format")
	return datasets

def get_main_graph_attrs(graph):
	print("\n====== Total elements ======")
	print("# nodes: ",nx.number_of_nodes(graph)) 
	print("# edges: ",nx.number_of_edges(graph)) 
	if not nx.is_directed(graph):
		print("# connected components: ",nx.number_connected_components(graph)) 
	print("# self-loops: ",nx.number_of_selfloops(graph)) 

def get_is_of_type_attrs(graph):
	print("\n====== is of type X? ======")
	print("Directed? ->", "Yes" if nx.is_directed(graph) else "No")
	print("Directed acyclic? ->", "Yes" if nx.is_directed_acyclic_graph(graph) else "No")
	print("Weighted? ->", "Yes" if nx.is_weighted(graph) else "No")

	if nx.is_directed(graph):
		print("Aperiodic? ->", "Yes" if nx.is_aperiodic(graph) else "No")
		print("Arborescence? ->", "Yes" if nx.is_arborescence(graph) else "No")
		print("Weakly Connected? ->", "Yes" if nx.is_weakly_connected(graph) else "No")
		print("Semi Connected? ->", "Yes" if nx.is_semiconnected(graph) else "No")
		print("Strongly Connected? ->", "Yes" if nx.is_strongly_connected(graph) else "No")

	else:
		print("Connected? ->", "Yes" if nx.is_connected(graph) else "No")		
		print("Bi-connected? ->", "Yes" if nx.is_biconnected(graph) else "No")
		print("Chordal? -> ", "Yes" if nx.is_chordal(graph) else "No")
		print("Forest? -> ", "Yes" if nx.is_chordal(graph) else "No")

	print("Distance regular? -> ", "Yes" if nx.is_distance_regular(graph) else "No")
	print("Eulerian? -> ", "Yes" if nx.is_eulerian(graph) else "No")
	print("Strongly regular? -> ", "Yes" if nx.is_strongly_regular(graph) else "No")
	print("Tree? -> ", "Yes" if nx.is_tree(graph) else "No")


def get_degreee_metrics(graph):
	print("\n====== Degree Metrics ======")
	deg_hist = nx.degree_histogram(graph)
	all_degrees = nx.degree(graph)
	degree_values = list(map(lambda x: x[1], all_degrees))
	print("Average: ", sum(degree_values)/len(degree_values))
	print("Minimum: ", min(degree_values))
	print("Maximum: ", max(degree_values))
	print("Most frequent: ", deg_hist.index(max(deg_hist)), "(", max(deg_hist), "times) \n")





if __name__ == '__main__':
	# load all the data into a dictionary
	all_data = read_datasets_gml()

	# pick a dataset and get some basic stats
	graph = all_data["lesmiserables"]
	print("\nGraph: ", graph.name)
	get_main_graph_attrs(graph)
	get_is_of_type_attrs(graph)
	get_degreee_metrics(graph)
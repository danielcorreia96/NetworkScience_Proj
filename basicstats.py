#!/usr/bin/env python3

import networkx as nx
import os
import json


def try_to_read_gml(filename):
	try:
		data = nx.read_gml(filename)
		data.name = filename.split("/")[1][:-4]
		print(nx.info(data))
		print("--------------------------")
		return data
	except Exception as err:
		print(err)
		print("failed to load dataset " + filename +  " in gml format")

def try_to_read_json(filename):
	try:
		with open(filename) as json_file:
			dataset = nx.node_link_graph(json.load(json_file))
			return dataset
	except Exception as err:
		print(err)
		print("failed to load dataset " + filename +  " in gml format")		

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
	degree_values = list(map(lambda x: x[1], nx.degree(graph)))
	print("Average degree: ", sum(degree_values)/len(degree_values))
	print("Minimum degree: ", min(degree_values))
	print("Maximum degree: ", max(degree_values))
	get_top_n_by_metric(nx.degree(graph),"degree")
	
	if nx.is_directed(graph):
		in_degree_vals = list(map(lambda x: x[1], graph.in_degree()))
		print("Average in-degree: ", sum(in_degree_vals)/len(in_degree_vals))
		print("Minimum in-degree: ", min(in_degree_vals))
		print("Maximum in-degree: ", max(in_degree_vals))
		get_top_n_by_metric(graph.out_degree(),"in-degree")

		out_degree_vals = list(map(lambda x: x[1], graph.out_degree()))
		print("Average out-degree: ", sum(out_degree_vals)/len(out_degree_vals))
		print("Minimum out-degree: ", min(out_degree_vals))
		print("Maximum out-degree: ", max(out_degree_vals))
		get_top_n_by_metric(graph.in_degree(),"in-degree")


def get_clustering_metrics(graph):
	print("\n===== Clustering Metrics ======")
	print("Transitivity: ", nx.transitivity(graph))
	print("")
	
	if not nx.is_directed(graph):
		triangles_values = list(nx.triangles(graph).values())
		print("# triangles: ", sum(triangles_values))
		print("Average triangles: ", sum(triangles_values)/len(triangles_values))
		print("Minimum # triangles: ", min(triangles_values))
		print("Maximum # triangles: ", max(triangles_values))
		get_top_n_by_metric(nx.triangles(graph),"# of triangles")
		
		clustercoff_values = list(nx.clustering(graph).values())
		print("Average clustering coefficient: ", sum(clustercoff_values)/len(clustercoff_values))
		print("Minimum clustering coefficient: ", min(clustercoff_values))
		print("Maximum clustering coefficient: ", max(clustercoff_values))
		get_top_n_by_metric(nx.clustering(graph),"clustering coefficient")
		print("")

		clustercoff_values = list(nx.square_clustering(graph).values())
		print("Average square clustering coefficient: ", sum(clustercoff_values)/len(clustercoff_values))
		print("Minimum square clustering coefficient: ", min(clustercoff_values))
		print("Maximum square clustering coefficient: ", max(clustercoff_values))
		get_top_n_by_metric(nx.square_clustering(graph), "square clustering coefficient")
		print("")

	

def get_top_n_by_metric(metric_data, metric_name, n=10):
	print("Top", n, "by", metric_name)
	metric_dict = dict(metric_data)
	for i in range(1,n+1):
		top_node = max(metric_dict, key=metric_dict.get)
		print(i,": ", top_node, " (", metric_dict.pop(top_node),")",sep="")
	print("")


def get_all_info(graph):
	print("******************************************")
	print("\nGraph: ", graph.name)
	get_main_graph_attrs(graph)
	get_is_of_type_attrs(graph)
	get_degreee_metrics(graph)
	get_clustering_metrics(graph)
	print("******************************************")



if __name__ == '__main__':
	# pick a dataset and get some basic stats
	graph = try_to_read_gml("datasets/word_adjacencies.gml")
	# graph = try_to_read_json("datasets/miserables.json")
	get_all_info(graph)

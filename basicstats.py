#!/usr/bin/env python3

import networkx as nx
import matplotlib.pyplot as plt
import json
import argparse

def try_to_read_gml(filename):
	try:
		data = nx.read_gml(filename)
		data.name = filename.split("/")[1][:-4]
		return data
	except Exception as err:
		print(err)
		print("failed to load dataset " + filename +  " in gml format")

def try_to_read_json(filename):
	try:
		with open(filename) as json_file:
			dataset = nx.node_link_graph(json.load(json_file))
			dataset.name = filename.split("/")[1][:-5]
			return dataset
	except Exception as err:
		print(err)
		print("failed to load dataset " + filename +  " in json format")		

def print_main_graph_attrs(graph):
	print("\n====== Total elements ======")
	print("# nodes: ",nx.number_of_nodes(graph)) 
	print("# edges: ",nx.number_of_edges(graph)) 
	if not nx.is_directed(graph):
		print("# connected components: ",nx.number_connected_components(graph)) 
	print("# self-loops: ",nx.number_of_selfloops(graph)) 

def print_is_of_type_attrs(graph):
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
		if not graph.is_multigraph():
			print("Chordal? -> ", "Yes" if nx.is_chordal(graph) else "No")
			print("Forest? -> ", "Yes" if nx.is_chordal(graph) else "No")

	print("Distance regular? -> ", "Yes" if nx.is_distance_regular(graph) else "No")
	print("Eulerian? -> ", "Yes" if nx.is_eulerian(graph) else "No")
	print("Strongly regular? -> ", "Yes" if nx.is_strongly_regular(graph) else "No")
	print("Tree? -> ", "Yes" if nx.is_tree(graph) else "No")


def print_degreee_metrics(graph):
	print("\n====== Degree Metrics ======")
	degree_values = list(map(lambda x: x[1], nx.degree(graph)))
	print("Average degree: ", sum(degree_values)/len(degree_values))
	print("Minimum degree: ", min(degree_values))
	print("Maximum degree: ", max(degree_values))
	print_top_n_by_metric(nx.degree(graph),"degree")
	
	if nx.is_directed(graph):
		in_degree_vals = list(map(lambda x: x[1], graph.in_degree()))
		print("Average in-degree: ", sum(in_degree_vals)/len(in_degree_vals))
		print("Minimum in-degree: ", min(in_degree_vals))
		print("Maximum in-degree: ", max(in_degree_vals))
		print_top_n_by_metric(graph.out_degree(),"in-degree")

		out_degree_vals = list(map(lambda x: x[1], graph.out_degree()))
		print("Average out-degree: ", sum(out_degree_vals)/len(out_degree_vals))
		print("Minimum out-degree: ", min(out_degree_vals))
		print("Maximum out-degree: ", max(out_degree_vals))
		print_top_n_by_metric(graph.in_degree(),"in-degree")


def print_clustering_metrics(graph):
	print("\n===== Clustering Metrics ======")
	if not graph.is_multigraph():
		print("Transitivity: ", nx.transitivity(graph))
		print("")
	
		if not nx.is_directed(graph):
			triangles_values = list(nx.triangles(graph).values())
			print("# triangles: ", sum(triangles_values))
			print("Average triangles: ", sum(triangles_values)/len(triangles_values))
			print("Minimum # triangles: ", min(triangles_values))
			print("Maximum # triangles: ", max(triangles_values))
			print_top_n_by_metric(nx.triangles(graph),"# of triangles")
			
			clustercoff_values = list(nx.clustering(graph).values())
			print("Average clustering coefficient: ", sum(clustercoff_values)/len(clustercoff_values))
			print("Minimum clustering coefficient: ", min(clustercoff_values))
			print("Maximum clustering coefficient: ", max(clustercoff_values))
			print_top_n_by_metric(nx.clustering(graph),"clustering coefficient")
			print("")

			clustercoff_values = list(nx.square_clustering(graph).values())
			print("Average square clustering coefficient: ", sum(clustercoff_values)/len(clustercoff_values))
			print("Minimum square clustering coefficient: ", min(clustercoff_values))
			print("Maximum square clustering coefficient: ", max(clustercoff_values))
			print_top_n_by_metric(nx.square_clustering(graph), "square clustering coefficient")
			print("")
	else:
		print("Multigraph clustering metrics are not supported by Networkx")


	

def print_top_n_by_metric(metric_data, metric_name, n=10):
	print("Top", n, "by", metric_name)
	metric_dict = dict(metric_data)
	for i in range(1,n+1):
		top_node = max(metric_dict, key=metric_dict.get)
		print(i,": ", top_node, " (", metric_dict.pop(top_node),")",sep="")
	print("")


def print_all_info(graph):
	print("******************************************")
	print("\nGraph: ", graph.name)
	print_main_graph_attrs(graph)
	print_is_of_type_attrs(graph)
	print_degreee_metrics(graph)
	print_clustering_metrics(graph)
	print("******************************************")

def draw_graph_by_metric(graph, metric_data, n=10, size=100):
	metrics_dict = dict(metric_data)
	top_n_metrics_dict = dict()
	for _ in range(n):
		top_node = max(metrics_dict,key=metrics_dict.get)
		top_n_metrics_dict[top_node] = metrics_dict.pop(top_node)
	
	top_n_graph = graph.subgraph(top_n_metrics_dict.keys())
	coords=nx.spring_layout(graph)
	plt.figure()
	nx.draw(top_n_graph, 
		pos=coords, 
		with_labels=sorted(top_n_graph.nodes()),
		nodelist=sorted(top_n_graph.nodes()), 
		node_size=[(v[1]+1) * size for v in sorted(top_n_metrics_dict.items())]
	)
	plt.show()


def draw_all_metrics(graph, n=10):
	print("******************************************")

	print("Graph by degree (top ",n,")",sep="")
	draw_graph_by_metric(graph, nx.degree(graph), n, size=100)
	
	print("\nGraph by triangles (top ",n,")",sep="")
	draw_graph_by_metric(graph, nx.triangles(graph), n, size=50)
	
	print("\nGraph by clustering coefficient (top ",n,")",sep="")
	draw_graph_by_metric(graph, nx.clustering(graph), n, size=500)

	print("******************************************")

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("dataset",help="dataset to be processed")
	parser.add_argument("format", choices=["gml","json"], help="format of the dataset (only supports gml and json)")
	parser.add_argument("-a","--all", help="print all possible metrics available",action="store_true")
	parser.add_argument("-d","--draw", type=int, help="draw graphs by top n of metrics")
	args = parser.parse_args()
	graph = None

	if args.format == "gml":
		graph = try_to_read_gml(args.dataset)
	elif args.format == "json":
		graph = try_to_read_json(args.dataset)

	if args.all:
		print_all_info(graph)

	if args.draw:
		draw_all_metrics(graph,args.draw)
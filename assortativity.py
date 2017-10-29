#!/usr/bin/env python3

import sys
import basicstats as bs
import networkx as nx
import collections

global graph_name
graph_name = ""

def assortativity(graph):
    print("\n------------------------------------")
    print("Assortativity coefficient r: " + str(get_assortativity_coefficient(G)))
    print("------------------------------------\n")
    all_or_top(G)
    get_mixing(G)

def assortativity_node(graph, node):
    a = nx.average_neighbor_degree(graph)
    print_all(a, "Average neighbor degree", node)

def description_for_every_node_in_graph(graph):
	for node in graph.nodes():
		print("\n---------------- "+ node + "'s' Assortativity -----------------")
		assortativity_node(graph, node)

def all_or_top(graph, n=0):
    if n == 0:
        description_for_every_node_in_graph(graph)
        print("------------------------------------")
        d = nx.average_degree_connectivity(graph)
        od = collections.OrderedDict(sorted(d.items()))
        for key, value in od.items():
             print("Degree: " + str(key) + "\t Average degree connectivity: " + str(value))
        print("------------------------------------")
    else:
        bs.get_top_n_by_metric(nx.average_neighbor_degree(graph), "Average neighbor degree", n)
        bs.get_top_n_by_metric(nx.average_degree_connectivity(graph), "Average degree Connectivity", n)

def get_assortativity_coefficient(graph, atribute=None):
    if atribute == None:
        return nx.degree_assortativity_coefficient(graph)
    else:
        return nx.attribute_assortativity_coefficient(graph, atribute)

#relation between a pair of attributes
def get_mixing(graph, atribute=None, probability=False):
    if atribute == None:
        degree_mixing(graph, probability)
    else:
        atribute_mixing(graph, probability)

def degree_mixing(graph, probability):
    d = nx.degree_mixing_dict(graph, normalized=probability)
    od = collections.OrderedDict(sorted(d.items()))
    for key, value in od.items():
        print("------------------------------------")
        print("Degree1: " + str(key))
        print("------------------------------------")
        ovalue = collections.OrderedDict(sorted(value.items()))
        for k, v in ovalue.items():
            print("Degree2: " + str(k), end='\t')
            if probability == True:
                print("Probability: " + str(v))
            else:
                print("Count: " + str(v))

def atribute_mixing(graph, probability):
    d = nx.attribute_mixing_dict(G, attribute,  normalized=probability)
    od = collections.OrderedDict(sorted(d.items()))
    for key, value in d.items():
        print("------------------------------------")
        print("Atribute1: " + str(key))
        print("------------------------------------")
        ovalue = collections.OrderedDict(sorted(value.items()))
        for k, v in value.items():
            print("Atribute2: " + str(k), end='\t')
            if probability == True:
                print("Probability: " + str(v))
            else:
                print("Count: " + str(v))

def print_all(metric_dict, metric_name, node):
    print(metric_name + ": " + str(metric_dict[node]))

if __name__ == '__main__':
	
	if len(sys.argv) != 2:
		print('USAGE: '+sys.argv[0]+' input.gml <model')
		exit(0)

	# pick a dataset and get some basic stats

	graph_name = sys.argv[1]
	G = bs.try_to_read_gml(graph_name)
	# bs.get_all_info(graph)
	
	assortativity(G)
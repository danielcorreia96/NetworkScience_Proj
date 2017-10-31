#!/usr/bin/env python3

import basicstats as bs
import argparse
import networkx as nx
import collections

global graph_name
graph_name = ""

def assortativity(graph):
    print("\n------------------------------------")
    print("Assortativity coefficient r: " + str(get_assortativity_coefficient(graph)))
    print("------------------------------------\n")
    all_or_top(graph)
    get_mixing(graph)

# def assortativity_node(graph, node):
#     a = nx.average_neighbor_degree(graph)
#     #print_all(a, "Average neighbor degree", node)

def description_for_every_node_in_graph(graph):
    metrics_dict = nx.average_neighbor_degree(graph)
    for node in graph.nodes():
        print(node,": ", str(metrics_dict[node]), sep="") 
        #print("\n---------------- "+ node + "'s' Assortativity -----------------")
		#assortativity_node(graph, node)

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
    d = nx.attribute_mixing_dict(graph, attribute,  normalized=probability)
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
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset",help="dataset to be processed")
    parser.add_argument("format", choices=["gml","json"], help="format of the dataset (only supports gml and json)")
    parser.add_argument("-a","--all", help="print all possible metrics available",action="store_true")
    parser.add_argument("-t","--top",type=int, help="print top n by metrics available")
    args = parser.parse_args()

    graph = None

    if args.format == "gml":
        graph = try_to_read_gml(args.dataset)
    elif args.format == "json":
        graph = try_to_read_json(args.dataset)

    if args.all:
        assortativity(graph)

    if args.top:
        all_or_top(graph,args.top)



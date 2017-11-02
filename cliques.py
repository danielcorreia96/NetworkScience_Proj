#!/usr/bin/env python3

import sys
import basicstats as bs
import networkx as nx
from math import *
import matplotlib.pylab as plt
import itertools as it

global graph_name
graph_name = ""
global colors, hatches
colors=it.cycle('mykwbgc')
hatches=it.cycle('/\|-+*')

def cliques_graph(graph):
	if nx.is_directed(graph):
		print("Err, only graph undirected")
		return
	print("Description of cliques in graph " + graph_name[9:-4])
	print("Number of Cliques: " + str(len(list(nx.algorithms.clique.enumerate_all_cliques(graph)))))
	print("Number of Maximals cliques: "+ str(nx.algorithms.clique.graph_number_of_cliques(graph)))
	print("The size of the largest clique in the graph: ", str(nx.algorithms.clique.graph_clique_number(graph)))

def cliques_node(graph, node):
	if nx.is_directed(graph):
		print("Err, only graph undirected")
		return
	print("Description of cliques in graph " + graph_name[9:-4] + " node: "+ node)
	print("Number of Cliques: " + number_of_cliques_for_node(graph, node))
	print("Number of Maximals Cliques: " + str(nx.algorithms.clique.number_of_cliques(graph, node)))
	print("Size of Largest maximal clique containing node " + str(len(nx.algorithms.clique.node_clique_number(graph))))

def description_for_every_node_in_graph(graph):
	if nx.is_directed(graph):
		print("Err, only graph undirected")
		return
	for node in graph.nodes():
		print("\n---------------- "+ node + "'s' Cliques -----------------")
		cliques_node(graph, node)


def number_of_cliques_for_node(graph, node):
	if nx.is_directed(graph):
		print("Err, only graph undirected")
		return
	return str(len(nx.algorithms.clique.cliques_containing_node(graph, node)))

def maximal_clique(graph):
	if nx.is_directed(graph):
		print("Err, only graph undirected")
		return
	return nx.algorithms.clique.make_max_clique_graph(graph)

def draw_circle_around_clique(clique,coords, color):
	dist=0
	temp_dist=0
	center=[0 for i in range(2)]
	for a in clique:
		for b in clique:
			temp_dist=(coords[a][0]-coords[b][0])**2+(coords[a][1]-coords[b][1])**2
			if temp_dist>dist:
				dist=temp_dist
				for i in range(2):
					center[i]=(coords[a][i]+coords[b][i])/2
	rad=dist**0.5/2
	cir = plt.Circle((center[0],center[1]),   radius=rad*1.3,fill=False,color=color,hatch=next(hatches))
	plt.gca().add_patch(cir)
	plt.axis('scaled')
	

def draw_colored_clique_with_size_N(graph, size=2, circle=False, layout="spring"):
	if nx.is_directed(graph):
		print("Err, only graph undirected")
		return

	coords=layout_dealer(graph, layout)
	
	cliques=[clique for clique in nx.find_cliques(graph) if len(clique)>size]
	plt.figure()
	nx.draw(graph, pos=coords, with_labels=graph.nodes().values())
	print("Number of Cliques: " + str(len(cliques)))
	for clique in cliques:
		print("Clique to appear: ",clique, " length: ", str(len(clique)))
		color = next(colors)
		if circle is True:
			draw_circle_around_clique(clique, coords, color)
		nx.draw_networkx_nodes(graph,pos=coords,nodelist=clique,node_color=color)
	plt.show()


def draw_colored_maximal_clique(graph, size=2, circle=False, layout="spring"):
	if nx.is_directed(graph):
		print("Err, only graph undirected")
		return
	graph = maximal_clique(graph)
	draw_colored_clique_with_size_N(graph, size, circle, layout)


def draw_clique_bipartite(graph, size=2, layout="spring"):
	if nx.is_directed(graph):
		print("Err, only graph undirected")
		return
	graph = nx.algorithms.clique.make_clique_bipartite(graph)
	draw_colored_clique_with_size_N(graph, size, layout)

def draw_top_size_cliques(graph, top=10, layout="spring"):
	if nx.is_directed(graph):
		print("Err, only graph undirected")
		return
	print("Showing the top "+ str(top) + " for sizes")
	top_n_size_cliques = []
	all_cliques = list(nx.algorithms.clique.enumerate_all_cliques(graph))
	cliques = []
	for i in range(len(all_cliques)):
		k = sorted(all_cliques[i], key=lambda j:j)
		if k not in cliques:
			cliques.append(k) 

	s = []
	for i in cliques:
		s.append((i,len(i)))

	s = sorted(s , key=lambda i: i[1])
	s.reverse()
	max_size = int(s[0][1])
	print("Max Size: ", str(max_size))
	clique_for_size= dict()
	for i in range(1, max_size+1):
		clique_for_size[i]=[]
	for i in s:
		clique_for_size[i[1]] += i[0]	

	if top > max_size:
		top = max_size
	a = []
	for i in range(max_size, max_size-top, -1):
		a += clique_for_size[i]
	
	for n in graph:
		if n in a and n not in top_n_size_cliques :
			top_n_size_cliques.append(n)
	graph = graph.subgraph(top_n_size_cliques)


	coords=layout_dealer(graph, layout)

	cliques=[clique for clique in nx.find_cliques(graph) if len(clique) >= max_size-top]

	print("Number of Cliques: " + str(len(cliques)))
	
	for clique in cliques:
		if len(clique) > max_size-top:
			plt.figure()
			nx.draw(graph, pos=coords, with_labels=graph.nodes().values())
			print("Clique to appear: ",clique, " length: ", str(len(clique)))
			nx.draw_networkx_nodes(graph, pos=coords, nodelist=clique,node_color=next(colors))		
			plt.show()



def layout_dealer(graph, layout):
	if nx.is_directed(graph):
		print("Err, only graph undirected")
		return
	if layout == "spring":
		return	nx.spring_layout(graph)
	elif layout == "circular":
		return	nx.circular_layout(graph)
	elif layout == "spectral":
		return	nx.spectral_layout(graph)
	elif layout == "shell":
		return	nx.shell_layout(graph)
	elif layout == "random":
		return	nx.random_layout(graph)

if __name__ == '__main__':
	
	if len(sys.argv) != 2:
		print('USAGE: '+sys.argv[0]+' input.gml <model')
		exit(0)

	graph_name = sys.argv[1]
	G = bs.try_to_read_gml(graph_name)
	if nx.is_directed(G):
		print("Err, only graph undirected")
		exit(0)	
	
	# cliques_graph(G)
	# description_for_every_node_in_graph(G)
	# draw_colored_clique_with_size_N(G, 2, False, "circular")
	# draw_colored_clique_with_size_N(G, 2, True)
	# draw_colored_maximal_clique(G, 2)
	# draw_clique_bipartite(G)
	draw_top_size_cliques(G, 2)
	
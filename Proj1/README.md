# NetworkScience_Proj
Repository for the network science project deliveries (MEIC-A 2017/2018)

## Part 1 - Exploration of Networkx Python package
The goal of this project was the exploration of the functionalities provided by the Networkx Python package and constructing a report of feedback (dificulties, strong points, neat tricks, etc.)

### Project Structure
For this project we developed 3 modules with examples and utilities for analysing a dataset in the Networkx environment:

- basicstats.py
	- functions to import the datasets in GML and JSON formats
	- functions to return basic details on the dataset such as number of nodes/edges and is_type_X questions (is directed/connected/weighted/etc?)
	- functions to print and draw information related to clustering metrics: triangles, clustering coeffcients and transitivity

- cliques.py
	- functions to calculate metrics related to cliques
	- visualization utility functions to draw different types of graphs

- assortativity.py
	- functions to describe and calculate metrics of assortativity

There is also a datasets folder which contains the datasets we used during development to test our examples.


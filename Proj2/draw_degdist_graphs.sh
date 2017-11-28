#!/bin/bash
echo "Drawing degree distribution graphs for each file in {lang}_data folders..."
for f in pt_data/*.out;
do
	echo "processing $f"
	python network_analysis.py $f
done

for f in es_data/*.out;
do
	echo "processing $f"
	python network_analysis.py $f
done

for f in en_data/*.out;
do
	echo "processing $f"
	python network_analysis.py $f
done
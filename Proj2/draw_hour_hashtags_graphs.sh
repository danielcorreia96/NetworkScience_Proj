#!/bin/bash 

for f in ./pt_data/*.out; 
do 
    echo "processing $f";
    python3 process_hashtags.py $f ./best_hashtags/pt/plots/pt_best_hastags; 
done

for f in ./es_data/*.out; 
do 
    echo "processing $f";
    python3 process_hashtags.py $f ./best_hashtags/es/plots/es_best_hastags; 
done

for f in ./en_data/*.out; 
do 
    echo "processing $f";
    python3 process_hashtags.py $f ./best_hashtags/en/plots/en_best_hastags; 
done


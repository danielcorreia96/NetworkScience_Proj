#!/bin/bash

echo "Splitting by month"
sh split_by_month.sh

echo "Splitting files by language"
# rm -r en_data es_data pt_data
mkdir en_data
mkdir es_data
mkdir pt_data
python split_by_language.py

sh freq_user.sh
sh freq_by_day.sh
sh drawing_montlhy_graphs.sh

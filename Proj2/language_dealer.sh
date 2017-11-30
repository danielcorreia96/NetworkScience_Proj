#!/bin/bash

echo "Splitting by month"
sh split_by_month.sh

echo "Splitting files by language"
# rm -r en_data es_data pt_data
#mkdir en_data
#mkdir es_data
#mkdir pt_data
python split_by_language.py

#echo "Sorting by date"
#sh sort_lang_data.sh
# sh freq_user.sh
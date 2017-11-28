#!/bin/bash

rm -r data_by_month
mkdir data_by_month

echo "parsing March"
head -1 parsed_data/full_data.00.out > data_by_month/full_data_Mar.out
cat parsed_data/full_data.*.out | grep "Mar.* 2014|" >> data_by_month/full_data_Mar.out

echo "parsing April"
head -1 parsed_data/full_data.00.out > data_by_month/full_data_Apr.out
cat parsed_data/full_data.*.out | grep "Apr.* 2014|" >> data_by_month/full_data_Apr.out

echo "parsing May"
head -1 parsed_data/full_data.00.out > data_by_month/full_data_May.out
cat parsed_data/full_data.*.out | grep "May.* 2014|" >> data_by_month/full_data_May.out

echo "parsing June"
head -1 parsed_data/full_data.00.out > data_by_month/full_data_Jun.out
cat parsed_data/full_data.*.out | grep "Jun.* 2014|" >> data_by_month/full_data_Jun.out

echo "parsing July"
head -1 parsed_data/full_data.00.out > data_by_month/full_data_Jul.out
cat parsed_data/full_data.*.out | grep "Jul.* 2014|" >> data_by_month/full_data_Jul.out
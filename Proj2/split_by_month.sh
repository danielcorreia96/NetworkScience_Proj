#!/bin/bash

rm -r data_by_month
mkdir data_by_month

echo "parsing March"
cat data_parsed/full_data.*.out | grep "Mar.* 2014|" >> data_by_month/full_data_Mar.out

echo "parsing April"
cat data_parsed/full_data.*.out | grep "Apr.* 2014|" >> data_by_month/full_data_Apr.out

echo "parsing May"
cat data_parsed/full_data.*.out | grep "May.* 2014|" >> data_by_month/full_data_May.out

echo "parsing June"
cat data_parsed/full_data.*.out | grep "Jun.* 2014|" >> data_by_month/full_data_Jun.out

echo "parsing July"
cat data_parsed/full_data.*.out | grep "Jul.* 2014|" >> data_by_month/full_data_Jul.out
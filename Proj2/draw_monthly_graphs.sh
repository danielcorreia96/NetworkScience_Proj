rm graphs_tweetspermonth/*
mkdir graphs_tweetspermonth
chmod 777 freq_dayly/*

for f in freq_dayly/count*;
do
	echo "$f"
	python users_graphics.py "$f"
done

rm graphs_tweetspermonth/*

chmod 777 freq_dayly/*
chmod 777 graphs_tweetspermonth/*

for f in freq_dayly/count*;
do
	echo "$f"
	python users_graphics.py "$f"
done

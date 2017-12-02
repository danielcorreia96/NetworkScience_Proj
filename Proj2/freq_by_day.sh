mkdir freq_dayly
rm freq_dayly/*
chmod 700 freq_dayly/*
chmod 700 *_data/*

for f in *_data/*;
do
	echo "$f"
	python freq_dayly.py "$f"
done

for f in freq_dayly/*;
do
	echo "$f"
	filename=$(basename $f)
	grep -ho "[0-9]*$" "$f" | sort | uniq -c > "freq_dayly/count-$filename"
done
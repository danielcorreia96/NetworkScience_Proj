chmod 600 *_mt*/*
rm graphs_tweetsperuser/*
mkdir graphs_tweetsperuser

for f in *_mt*/*;
do
	echo "$f"
	filename=$(basename $f)
	grep -ho "[0-9]*,[0-9]*" "$f" | sort | uniq -c > "$f""-count"
done

for f in *_mt*/*-count;
do
	echo "$f"
	python random_user_profiling.py "$f"
done

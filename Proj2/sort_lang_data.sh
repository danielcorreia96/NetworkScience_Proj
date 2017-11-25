echo "Sorting retweets in each file by created_at timestamp attribute..."
for f in *_data/*;
do
	echo "processing $f"
	chmod a+w "$f"; cat "$f" | sort -t, -k3,3 -o "$f"

done
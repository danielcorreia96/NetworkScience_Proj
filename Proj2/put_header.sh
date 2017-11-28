for f in *_data/*;
do
	chmod a+w "$f"
	mv "$f" aux
	echo "id_str,user_id_str,created_at,lang,hashtags,retweeted_id_str,retweeted_user_id_str,retweeted_created_at" > "$f" 
	cat aux >> "$f"
	rm aux
done
rm -r *_mt*/*
mkdir en_mt050tweets
mkdir es_mt050tweets
mkdir pt_mt050tweets
mkdir en_mt075tweets
mkdir es_mt075tweets
mkdir pt_mt075tweets
mkdir en_mt150tweets
mkdir es_mt150tweets
mkdir pt_mt150tweets
chmod 600 *_data/*
for f in *_data/*;
do
	echo "$f"
	python freq_user.py "$f"
done
rm -r en_mt25tweets pt_mt25tweets es_mt25tweets en_mt50tweets pt_mt50tweets es_mt50tweets en_mt100tweets pt_mt100tweets es_mt100tweets
mkdir en_mt50tweets
mkdir es_mt50tweets
mkdir pt_mt50tweets
mkdir en_mt25tweets
mkdir es_mt25tweets
mkdir pt_mt25tweets
mkdir en_mt100tweets
mkdir es_mt100tweets
mkdir pt_mt100tweets
chmod 600 *_data/*
for f in *_data/*;
do
	echo "$f"
	python freq_user.py "$f"
done
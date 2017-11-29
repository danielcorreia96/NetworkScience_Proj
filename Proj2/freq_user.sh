rm -r en_users-daily es_users-daily pt_users-daily en_mt30tweets pt_mt30tweets es_mt30tweets
mkdir en_users-daily
mkdir es_users-daily
mkdir pt_users-daily
mkdir en_mt30tweets
mkdir es_mt30tweets
mkdir pt_mt30tweets
for f in *_data/*;
do
	echo "$f"
	python freq_user.py "$f"
done
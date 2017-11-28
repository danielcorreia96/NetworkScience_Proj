rm -r en_users-daily es_users-daily pt_users-daily
mkdir en_users-daily
mkdir es_users-daily
mkdir pt_users-daily

for f in *_data/*;
do
	echo "$f"
	python freq_user.py "$f"
done
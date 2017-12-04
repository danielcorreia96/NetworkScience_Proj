import pandas as pd
import sys

def count_tweets(doc, num):

	data = pd.read_csv(doc, low_memory=False)
	
	data['freq-u'] = data.groupby('user_id_str')['user_id_str'].transform('count')	
	data = data[data["freq-u"]>=num]
	data["day"] = format_datetime(data["created_at"])
	data = data.drop('freq-u', 1)
	data = data.drop("id_str",1)
	data = data.drop("created_at",1) 
	data = data.drop("lang",1)
	data = data.drop("hashtags",1)
	data = data.drop("retweeted_id_str",1)
	data = data.drop("retweeted_user_id_str",1)
	data = data.drop("retweeted_created_at",1)
	data.to_csv(doc[:2]+"_mt"+str(num).zfill(3)+"tweets/"+doc[8:], index=False)


def format_datetime(dt_series):

    def get_split_date(strdt):
        split_date = strdt.split()
        str_date = split_date[1] + ' ' + split_date[2] + ' ' + split_date[5] + ' ' + split_date[3]
        return str_date

    dt_series = pd.to_datetime(dt_series.apply(lambda x: get_split_date(x)), format = '%b %d %Y %H:%M:%S')

    return dt_series.dt.day


if __name__ == '__main__':
	f = sys.argv[1]
	count_tweets(f, 75)
	count_tweets(f, 50)
	count_tweets(f, 150)


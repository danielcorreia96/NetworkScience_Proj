import pandas as pd
import sys

def count_tweets_daily(doc):

	data = pd.read_csv(doc, low_memory=False)
	
	data['freq-u'] = data.groupby('user_id_str')['user_id_str'].transform('count')	
	data = data[data["freq-u"]>=30]

	data = data.drop('freq-u', 1)

	data["day"] = format_datetime(data["created_at"])

	data['freq'] = data.groupby('user_id_str')['day'].nunique()
	
	data = data[data["freq"]>=30]
	
	data = data.drop('freq', 1)
	data.groupby('user_id_str')
	data.to_csv(doc[:2]+"_users-daily/"+doc[8:], index=False)

def count_tweets(doc):

	data = pd.read_csv(doc, low_memory=False)
	
	data['freq-u'] = data.groupby('user_id_str')['user_id_str'].transform('count')	
	data = data[data["freq-u"]>=30]

	data = data.drop('freq-u', 1)

	data.to_csv(doc[:2]+"_mt30tweets/"+doc[8:], index=False)


def format_datetime(dt_series):

    def get_split_date(strdt):
        split_date = strdt.split()
        str_date = split_date[1] + ' ' + split_date[2] + ' ' + split_date[5] + ' ' + split_date[3]
        return str_date

    dt_series = pd.to_datetime(dt_series.apply(lambda x: get_split_date(x)), format = '%b %d %Y %H:%M:%S')

    return dt_series.dt.day


if __name__ == '__main__':
	count_tweets(sys.argv[1])



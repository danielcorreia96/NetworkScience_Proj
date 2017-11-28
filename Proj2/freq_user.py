import pandas as pd
# import sys

# def count_tweets(doc):
# 	data = pd.read_csv(doc)
# 	data['freq'] = data.groupby('user_id_str')['user_id_str'].transform('count')
# 	data.write_csv(doc[:-4]+"_freqs.out")
# 	data1 = data[data["freq"]>30]

def format_datetime(dt_series):

    def get_split_date(strdt):
        split_date = strdt.split()

        str_date = split_date[2]
        # split_date[1] + ' ' +  + ' ' + split_date[5] + ' ' + split_date[3]
        return str_date

    dt_series = pd.to_datetime(dt_series.apply(lambda x: get_split_date(x)), format = '%d')

    return dt_series

# if __name__ == '__main__':
# 	count_tweets(sys.argv[0])	
memery_low=False
dt = pd.read_csv("en_data/en_full_data_Apr.out")
# data1 = dt[format_datetime(dt["created_at"])]
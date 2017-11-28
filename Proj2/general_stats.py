import pandas as pd
from multiprocessing import JoinableQueue, Process, cpu_count
import datetime

data_folders = ["en","es","pt"]
months = ["Mar", "Apr", "May", "Jun", "Jul"]


def do_work(in_queue,stop_token):
	while True:
		try:
			filename = in_queue.get(block=True, timeout=5)
		except queues.Empty as error:
			#print("Empty queue. Exiting child process")
			sys.exit()

		if filename == stop_token:
			#print("Reached end of queue")
			in_queue.task_done()
			continue

		# process
		dataset = pd.read_csv(filename)
		print("%s - # retweets: %d" % (filename, len(dataset)))
		print("%s - # users: %d" % (filename, len(dataset.user_id_str.unique())))
		print("%s - # original tweets: %d" % (filename, len(dataset.retweeted_id_str.unique())))

		t2 = format_datetime_1(dataset.created_at)
		t1 = format_datetime_1(dataset.retweeted_created_at)
		tdelta = t2 - t1
		print("%s - interval between retweet time and original tweet time" % (filename))
		print(tdelta.describe())

		in_queue.task_done()


# FROM STACKOVERFLOW POST: https://stackoverflow.com/questions/32034689/why-is-pandas-to-datetime-slow-for-non-standard-time-format-such-as-2014-12-31
# explicit conversion of essential information only -- parse dt str: concat
def format_datetime_1(dt_series):

    def get_split_date(strdt):
        split_date = strdt.split()
        str_date = split_date[1] + ' ' + split_date[2] + \
            ' ' + split_date[5] + ' ' + split_date[3]
        return str_date

    dt_series = pd.to_datetime(dt_series.apply(
    	lambda x: get_split_date(x)), format='%b %d %Y %H:%M:%S')

    return dt_series


def start_multiprocessing():
	work = JoinableQueue()
	STOP_TOKEN = "STOP!"

	for lang in data_folders:
		for month in months:
			work.put("%s_data/%s_full_data_%s.out" % (lang, lang, month))

	procs = []
	for _ in range(4):
		t = Process(target=do_work, args=(work, STOP_TOKEN))
		t.daemon = True
		t.start()
		procs.append(t)

	work.put(STOP_TOKEN)
	#print("Waiting to join processes...")
	for p in procs:
		p.join()


if __name__ == '__main__':
	start_multiprocessing()



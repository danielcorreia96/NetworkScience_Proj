import json
import gzip
from collections import namedtuple
import threading
import queue
import sys

import multiprocessing

jsonfilename = "data.00.gz"

def do_work(in_queue, out_queue):
	while True:
		item = in_queue.get()
		# process
		l1 = json.loads(item.decode(), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
		try:
			if l1.entities.hashtags != []:
				hashtags = [item.text for item in l1.entities.hashtags]

				if l1.retweeted_status is not None:
					result = ["RT", l1.id_str, l1.user.id_str, l1.created_at, l1.lang, hashtags, l1.retweeted_status.id_str, l1.retweeted_status.user.id_str, l1.retweeted_status.created_at]
					# print(result)
					out_queue.put(result)
					in_queue.task_done()

		except AttributeError as e:
			continue


def write_to_file(in_queue):
	while True:
		item = in_queue.get()
		#print("writing...")
		with open("tweets2.txt","a") as outfile:
			json.dump(item,outfile)
			outfile.write("\n")
		
		in_queue.task_done()


def start_multiprocessing():
	work = multiprocessing.JoinableQueue()
	results = multiprocessing.JoinableQueue()

	# start for workers
	for i in range(32):
		t = multiprocessing.Process(target=do_work, args=(work, results))
		t.daemon = True
		t.start()

	# workers to write output
	for i in range(16):
		t = multiprocessing.Process(target=write_to_file, args=(results,))
		t.daemon = True
		t.start()

	# produce data
	with gzip.GzipFile(jsonfilename, "r") as fin:
		for line in fin:
			work.put(line)

	
	work.join()
	results.join()
	
	sys.exit()

with gzip.GzipFile(jsonfilename, "r") as fin:
	for line in fin:
		#l1 = json.loads(line)
		l1 = json.loads(line.decode(), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
		break

#print(json.dumps(l1,indent=2))

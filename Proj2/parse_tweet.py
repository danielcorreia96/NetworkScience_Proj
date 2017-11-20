import json
import gzip
from collections import namedtuple
import threading
import queue
import sys

jsonfilename = "data.00.gz"

def do_work(in_queue, out_queue):
	while True:
		item = in_queue.get()
		# process
		l1 = json.loads(item, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
		if l1.entities.hashtags != []:
			hashtags = [item.text for item in l1.entities.hashtags]
			result = [l1.created_at, l1.lang, l1.user.id, hashtags]
			print(result)
			out_queue.put(result)
			in_queue.task_done()

def start_multithreads():
	work = queue.Queue()
	results = queue.Queue()

	# start for workers
	for i in range(16):
		t = threading.Thread(target=do_work, args=(work, results))
		t.daemon = True
		t.start()

	# produce data
	with gzip.GzipFile(jsonfilename, "r") as fin:
		for line in fin:
			work.put(line)

	work.join()

	# get the results
	#print(results)

	sys.exit()




with gzip.GzipFile(jsonfilename, "r") as fin:
	for line in fin:
		l1 = json.loads(line)
		break

#print(json.dumps(l1,indent=2))

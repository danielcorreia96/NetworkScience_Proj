import json
import gzip
from collections import namedtuple
import threading
from multiprocessing import JoinableQueue, Process, cpu_count, Pool, Manager
import argparse
import time
import sys
#from pympler import summary, muppy
import gc
import os
import resource

def do_work(in_queue, outfilename, stop_token):
	while True:
		item = in_queue.get(block=True,timeout=10)
		if item == stop_token:
			print("Reached end of queue")
			in_queue.task_done()
                        continue

		# process
		l1 = json.loads(item.decode(), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
		try:
			if l1.entities.hashtags != []:
				hashtags = "#".join([item.text for item in l1.entities.hashtags])
				if l1.retweeted_status is not None:
					result = "|".join(["RT", l1.id_str, l1.user.id_str, l1.created_at, l1.lang, hashtags, l1.retweeted_status.id_str, l1.retweeted_status.user.id_str, l1.retweeted_status.created_at])
					with open(outfilename,"a") as outfile:
						outfile.write(result.encode("utf-8")+"\n")
						outfile.flush();
#					print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024)
						in_queue.task_done()

		except AttributeError as e:
			continue


def start_multiprocessing(jsonfilename):
	work = JoinableQueue()
	STOP_TOKEN = "STOP!"
	filenames = []
	# start for workers


        procs = []
	for i in range(int(cpu_count()-8)):
		# slice .gz and unique identifier
		outfile = "%s_%d.txt" % (jsonfilename[5:-3],i)
		filenames.append(outfile)
		# reset output file
		open(outfile,"w").close()
		t = Process(target=do_work, args=(work, outfile, STOP_TOKEN))
		t.daemon = True
		t.start()
                procs.append(t)

	# produce data
	with gzip.GzipFile(jsonfilename, "r") as fin:
		for line in fin:
			work.put(line)
			if work.qsize() > 300000: # try to avoid too much memory usage
				print("sleeping for 20 seconds to relax memory usage...")
				time.sleep(20)
				print("back to work! current queue size: %d" % (work.qsize()))

	work.put(STOP_TOKEN)
        print("Waiting to join processes...")
        for p in procs:
            p.join()

	print("collect output of multiple jobs into a single file??")
	with open("full_%s.out" % (jsonfilename[5:-3]), 'w') as outfile:
		for fname in filenames:
		 	with open(fname) as infile:
		 		for line in infile:
		 			outfile.write(line)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("dataset",help="gzip dataset to be processed")
	args = parser.parse_args()

	start_multiprocessing(args.dataset)


import json
import gzip
from collections import namedtuple
import threading
from multiprocessing import Queue, Process, cpu_count
import argparse
import time
import sys
from pympler import summary, muppy

def do_work(in_queue, outfilename, stop_token):
	while True:
		item = in_queue.get()
		if item == stop_token:
			print("Reached end of queue")
			return

		# process
		l1 = json.loads(item.decode(), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
		try:
			if l1.entities.hashtags != []:
				hashtags = "#".join([item.text for item in l1.entities.hashtags])
				if l1.retweeted_status is not None:
					result = "|".join(["RT", l1.id_str, l1.user.id_str, l1.created_at, l1.lang, hashtags, l1.retweeted_status.id_str, l1.retweeted_status.user.id_str, l1.retweeted_status.created_at])
					with open(outfilename,"a") as outfile:
						outfile.write(result+"\n")
					#outfile.flush();
						#in_queue.task_done()

		except AttributeError as e:
			continue

def start_multiprocessing(jsonfilename):
	work = Queue()
	STOP_TOKEN = "STOP!"
	filenames = []
	# start for workers
	for i in range(int(cpu_count()/2)):
		# slice .gz and unique identifier
		outfile = "%s_job%d.txt" % (jsonfilename[:-3], i)
		filenames.append(outfile)
		# reset output file
		open(outfile,"w").close()
		t = Process(target=do_work, args=(work, outfile, STOP_TOKEN))
		t.daemon = True
		t.start()

	# produce data
	with gzip.GzipFile(jsonfilename, "r") as fin:
		for line in fin:
			work.put(line)
			if work.qsize() > 200000: # try to avoid too much memory usage
				print("sleeping for 1 minute to relax memory usage...")
				summary.print_(summary.summarize(muppy.get_objects()))	
				time.sleep(20)
				print("back to work! current queue size: %d" % (work.qsize()))
				summary.print_(summary.summarize(muppy.get_objects()))	

	work.put(STOP_TOKEN)
	#work.join()
	while True:
		if work.empty():
			print("Queue is empty")
			break
	
	print("collect output of multiple jobs into a single file")
	with open("full_%s" % (jsonfilename[:-3]), 'r') as outfile:
		for fname in filenames:
			with open(fname) as infile:
				for line in infile:
					outfile.write(line)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("dataset",help="gzip dataset to be processed")
	args = parser.parse_args()

	start_multiprocessing(args.dataset)


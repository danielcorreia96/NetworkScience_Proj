from multiprocessing import JoinableQueue, Process, cpu_count, Pool, Manager, queues
import os
import sys

result = ["id_str", "user_id_str", "created_at", "lang", "hashtags", "retweeted_id_str", "retweeted_user_id_str", "retweeted_created_at"]

def do_work(in_queue, langs, stop_token):
	while True:
		try:
			item = in_queue.get(block=True,timeout=5)
		except queues.Empty as error:
			print("Empty queue. Exiting child process")
			sys.exit()
		if item == stop_token:
			print("Reached end of queue")
			in_queue.task_done()
			continue

		# process
		for lang in langs:
			fname = "%s_data/%s_%s" % (lang,lang,item.split("/")[1])
			if os.path.isfile(fname): 
				# print("File %s already exists. Skipping..." % (fname))
				continue
			open(fname,"w").close()
			with open(item,"r") as fin, open(fname,"a") as fout:
				fout.write(",".join(result)+"\n")
				for line in fin:
					outline = line.strip()[3:].split("|")
					if outline[3] == lang:
						fout.write(",".join(outline)+"\n")
						fout.flush()
		in_queue.task_done()


def start_multiprocessing():
	work = JoinableQueue()
	STOP_TOKEN = "STOP!"
	for file in os.listdir("data_by_month/"):
		work.put(os.path.join("data_by_month/",file))
	# start for workers

	procs = []
	langs = ["en","es","pt"]
	for _ in range(cpu_count()-1):
		t = Process(target=do_work, args=(work, langs, STOP_TOKEN))
		t.daemon = True
		t.start()
		procs.append(t)

	work.put(STOP_TOKEN)
	print("Waiting to join processes...")
	for p in procs:
		p.join()


if __name__ == '__main__':
	start_multiprocessing()

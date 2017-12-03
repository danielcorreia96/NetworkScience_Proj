import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import string
import sys

def graphics_users_tweets(file):
	
	f = open(file, "r+")
	data = f.read() 

	data = data.split("\n")[:-1]

	y = [int(row.strip(" ").split(" ")[0]) for row in data]
	x = [int(row.strip(" ").split(" ")[1]) for row in data] 
	x = sorted(x, key=lambda i: i)
	fig = plt.figure()
	ax1 = fig.add_subplot(111)

	ax1.set_title("Lang: "+string.upper(file[17:19])+" Month:"+file[-7:-4])
	ax1.set_xlabel("Day")
	ax1.set_ylabel("#tweets", rotation=360)

	ax1.plot(x, y, c="r")
	ax1.yaxis.set_label_coords(-0.075,1.030)
	plt.xlim(1, 31)
	# plt.ylim(0, 1000000)
	# plt.show()
	# plt.draw()

	plt.savefig("graphs_tweetspermonth/"+file[17:19]+"_"+file[-7:-4]+".png")
	plt.close()

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print "USAGE: "+sys.argv[0]+" freq_daily/data.out"
	graphics_users_tweets(sys.argv[1])
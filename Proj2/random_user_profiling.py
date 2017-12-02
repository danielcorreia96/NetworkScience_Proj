import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import string
import sys
import random

def graphics_user_profiling(file):
	
	f = open(file, "r+")
	data = f.readline()
	data = f.read()
	if len(data) > 0:
		days = []
		for i in range(32):
			days.append(i)

		data = data.split("\n")[:-1]
		user = ""
		users = []
		while len(users)< 3:
			i = random.randint(0, len(data)-1)
			d = data[i]
			u = (d.strip(" ").split(" ")[1]).split(",")[0]
			if user != u and u not in users:
				users.append(u)
				user = u
				if len(users) == 3:
					break
			
		ux = []
		uy = []
		for i in range(3):
			ux.append([])
			uy.append([])
			z = []
			for d in data:
				val = d.strip(" ").split(" ")
				u = (val[1]).split(",")
				if u[0] == users[i]:
					z.append((int(u[1]), int(val[0])))
			z = sorted(z, key=lambda i:i[0])
			for j in range(len(z)):
				ux[i].append(z[j][0])
				uy[i].append(z[j][1])

		fig = plt.figure()
		ax1 = fig.add_subplot(111)

		ax1.set_title(string.upper(file[0:2])+" Users with more than: "+str(int(file[5:8]))+" tweets - "+file[-13:-10])
		ax1.set_xlabel("Day")
		ax1.set_ylabel("#tweets")

		ax1.plot(ux[0], uy[0], c="r")
		ax1.plot(ux[1], uy[1], c="g")
		ax1.plot(ux[2], uy[2], c="b")

		plt.legend(["user1", "user2", "user3"])
		# plt.show()
		# plt.draw()

		plt.savefig("graphs_tweetsperuser/"+file[15:17]+"_"+file[-13:-10]+".png")
		plt.close()

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print "USAGE: "+sys.argv[0]+" freq_daily/data.out"
	graphics_user_profiling(sys.argv[1])
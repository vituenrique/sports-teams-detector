import os

path = '/home/vituenrique/Desktop/dataset/2013-11-03/First Half/0'

a = open("output0.txt", "w")
for path, subdirs, files in os.walk(path):
	for filename in files:
		a.write("file " + "'" + filename + "'" + "\n") 
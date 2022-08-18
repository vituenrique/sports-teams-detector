#!/usr/bin/python
from PIL import Image
import os, sys

def resize(path):
	dirs = os.listdir(path)
	if dirs:
		if not os.path.exists(path + "resized/"):
			os.mkdir(path + "resized/")
		for item in dirs:
			if os.path.isfile(path + item):
				im = Image.open(path + item)

				f, e = os.path.splitext(path + "resized/" + item)
				imResize = im.resize((64, 128), Image.ANTIALIAS)
				imResize.save(f + '.png', 'PNG')

path = "../Detection/dataset/"

resize(path)
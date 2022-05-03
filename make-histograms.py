import os
import numpy as np
import shutil

targetpath = '/home/bram/Documents/grand-data/graphs/histograms'
tempdir = '/home/bram/Documents/grand-data/.temp'
pathdir = '/home/bram/Documents/grand-data/data/zips/'
filename = 'data-adaq-20220503103856.zip'
path = str(pathdir) + str(filename)

def files(path):
	if os.path.exists(tempdir):
		shutil.rmtree(tempdir)
		os.mkdir(tempdir)
	else:
		os.mkdir(tempdir)
	shutil.unpack_archive(path, extract_dir= tempdir)
	AD = [], MD =[], MON=[], TD=[]
	folders = ['AD', 'MD', 'MON', 'TD']
	for i in range (4):
		file = os.listdir(str(tempdir) +'/cur/' +str(folders[i]) +'/')
		np.append(files, np.array([[file]]), 0) 
	shutil.rmtree(tempdir)
	return files

f = files(path)

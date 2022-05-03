import os
import numpy as np
import shutil

Histdir = '~/github/grand/grand-daq-master/tools'
targetpath = '/home/bram/Documents/grand-data/histograms'
tempdir = '/home/bram/Documents/grand-data/.temp'
pathdir = '/home/bram/Documents/grand-data/data/zips'
#filename = 'data-adaq-20220503103856'
#measurement = 'Noise-XY'
#path = str(pathdir) +'/' +str(measurement) +'/' +str(filename) +'.zip'




def makeroot(measurement, filename, update=True):
	path = str(pathdir) +'/' +str(measurement) +'/' +str(filename)
	if os.path.exists(tempdir):
		shutil.rmtree(tempdir)
		os.mkdir(tempdir)
	else:
		os.mkdir(tempdir)
	shutil.unpack_archive(path, extract_dir= tempdir)
	try:
		os.mkdir(str(targetpath) +'/' +str(measurement))
	except FileExistsError:
		pass
	try:
		os.mkdir(str(targetpath) +'/' +str(measurement) +'/' +str(filename))
	except FileExistsError:
		pass
	folders = ['AD', 'MD', 'MON', 'TD']
	for i in range (4):
		try:
			os.mkdir(str(targetpath) +'/' +str(measurement) +'/' +str(filename) +'/' +str(folders[i]))
		except FileExistsError:
			pass
		data = os.listdir(str(tempdir) +'/cur/' +str(folders[i]) +'/')
		for d in data:
			os.chdir(str(targetpath) +'/' +str(measurement) +'/' +str(filename) +'/' +str(folders[i]))
			if os.path.exists(str(Histdir) + '/Hist ' +str(tempdir) +'/cur/' +str(folders[i]) +'/' +str(d)) and update==False:
				pass
			else:		
				os.system(str(Histdir) + '/Hist ' +str(tempdir) +'/cur/' +str(folders[i]) +'/' +str(d))
				os.system('mv Hist.root ' + str(d) +'.root')
	os.chdir(pathdir)
	shutil.rmtree(tempdir)
	return

def loopmake():
	measurements = os.listdir(str(pathdir))
	for m in measurements:
		filenames = os.listdir(str(pathdir) +'/' +str(m))
		for f in filenames:
			makeroot(m,f)
	return


loopmake()


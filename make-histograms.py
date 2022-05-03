import os
import numpy as np
import shutil


#fill in your machine's specifics:
cwd = os.getcwd()
Histdir = '~/github/grand/grand-daq-master/tools'
targetpath = '/home/bram/Documents/grand-data/histograms'
tempdir = '/home/bram/Documents/grand-data/.temp'
pathdir = '/home/bram/Documents/grand-data/data/zips'
#filename = 'data-adaq-20220503103856'
#measurement = 'Noise-XY'
#path = str(pathdir) +'/' +str(measurement) +'/' +str(filename) +'.zip'


def makeroot(measurement, filename, update):
	path = str(pathdir) +'/' +str(measurement) +'/' +str(filename)
	if os.path.exists(tempdir):	#Create a temporary directory to unpack into
		shutil.rmtree(tempdir)
		os.mkdir(tempdir)
	else:
		os.mkdir(tempdir)
	shutil.unpack_archive(path, extract_dir= tempdir)
	try:	#make empty directories for the file structure
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
		data = os.listdir(str(tempdir) +'/cur/' +str(folders[i]) +'/') #get the filenames of the subfolder i
		for d in data:
			os.chdir(str(targetpath) +'/' +str(measurement) +'/' +str(filename) +'/' +str(folders[i])) #change directory so the Hist.root is placed in the correct place
			if os.path.exists(str(Histdir) + '/Hist ' +str(tempdir) +'/cur/' +str(folders[i]) +'/' +str(d)) and update==False: #update determines if existing histograms are rewritten
				print('jup')
			else:		
				os.system(str(Histdir) + '/Hist ' +str(tempdir) +'/cur/' +str(folders[i]) +'/' +str(d)) #Execute the Hist file for the given measurement
				os.system('mv Hist.root ' + str(d) +'.root') #rename
	os.chdir(cwd)
	shutil.rmtree(tempdir)
	return

def loopmake(update = False): #loops over all the measurement folders + subfolders
	measurements = os.listdir(str(pathdir))
	for m in measurements:
		filenames = os.listdir(str(pathdir) +'/' +str(m))
		for f in filenames:
			makeroot(m,f,update)
	return

up = input('Do you want to update existing histograms? Answer yes or no. ' )
if up == 'yes':
	loopmake(True)
else:
	loopmake()
	
	

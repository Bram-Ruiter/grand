import numpy as np
import matplotlib.pyplot as plt
import os
import ROOT
import time
import shutil


start = time.time()
targetpath = '/home/bram/Documents/grand-data/graphs'
histdir = '/home/bram/Documents/grand-data/histograms'
#file = ROOT.TFile.Open(str(path)+'.root')

logy= True


def AmpTooHighV1(data,cut=500): #Determines if any measured amplitude is unphysically high
	amp = np.asarray(data)
	for j in amp:
		if j>cut:
			return True
	return False

def AmpTooHighV2(data, cut=8300): #A bit more effcient than V1
	amp = np.asarray(data)
	if np.max(amp)>cut:
		return True
	else:
		return False


def histtotal(file, filepath, channel): #returns the total FM hist of channel j
	total = 0 
	for i in range(5000):
		try:
			hist = eval('file.H' +str(i) +'FM' +str(channel)) #loads the ith histogram of channel j
			if not AmpTooHighV2(eval('file.H' +str(i) +'T1')): #Discard unphysical measurements
				if total == 0: #use the first histogram to create the object
					total = hist
				else:
						total += hist #Add the histograms
			else:
				print( 'Hist' +str(i) +' is rejected')
		except AttributeError: #If the specified histogram doesnt exist continue the loop
			pass
	return total

def histavg(file, filepath, channel): #returns the average FM hist of channel j
	total = 0
	counter=0
	for i in range(5000):
		try:
			hist = eval('file.H' +str(i) +'FM' +str(channel)) #loads the ith histogram of channel j
			counter +=1
			if not AmpTooHighV2(eval('file.H' +str(i) +'T1')): #Discard unphysical measurements
				if total == 0: #use the first histogram to create the object
					total = hist
				else:
						total += hist #Add the histograms
			else:
				print( 'Hist' +str(i) +' is rejected')
		except AttributeError: #If the specified histogram doesnt exist continue the loop
			pass
	return total, counter


def graph(hist, counter, filepath, graphpath, j): #matplotlib graph
	global f
	bins= hist.GetNbinsX()
	if counter == 0:
		return
	else:
		pass
	avg = np.asarray(hist)/counter
	f = np.linspace(0,250,bins+2)
	plt.figure(1)
	plt.title('Average fourrier transform')
	plt.grid()
	if logy:
		plt.yscale('log')
	else:
		pass
	plt.xlabel('Frequency (MHz)')
	plt.ylabel('Amplitude (' +str(bins) +'/250 MHz$^{-1}$)')
	plt.plot(f, avg, linewidth = 0.5)
	if logy: 
		plt.savefig(str(graphpath) +'LogY' +'ch' +str(j) +'.pdf')
	else:
		plt.savefig(str(graphpath) +'LogOff' +'ch' +str(j) +'.pdf')
	plt.close()
	return 

def graphV1(hist, filepath, graphpath, j): #ROOT graph
	bins= hist.GetNbinsX()
	if logy:
		c1.SetLogy()
	else:
		pass
	hist.SetTitle('Accumulated Frequency Plot')
	hist.GetXaxis().SetTitle('Frequency (MHz)')
	hist.GetYaxis().SetTitle('Amplitude (' +str(bins) +'/250 MHz$^{-1}$)')
	hist.SetStats(False)
	hist.Draw()
	c1.Update()
	if logy: 
		c1.Print(str(graphpath) +'LogY' +'ch' +str(j) +'.pdf')
	else:
		c1.Print(str(graphpath) +'LogOff' +'ch' +str(j) +'.pdf')
	return 

def channelloop(filepath, graphpath):	#Makes graphs for every channel
	try: 
		rootfile = ROOT.TFile.Open(filepath)
		for j in range(1,5):
			hist,counter = histavg(rootfile, filepath, j) 
			if hist != 0:	#if hist=0 no recorded events for specified channel
				graph(hist, counter, filepath, graphpath, j)
			else:
				pass
	except OSError:
		pass
	return	
	

def fileloop(update = True): #loops over all the measurement folders + subfolders
	measurements = os.listdir(str(histdir))
	for m in measurements:
		dirs = os.listdir(str(histdir) + '/' +str(m))
		try:
			os.mkdir(str(targetpath) +'/' +str(m))
		except FileExistsError:
			pass 
		for d in dirs:
			folders = os.listdir(str(histdir) + '/' +str(m) +'/' +str(d))
			try:
				os.mkdir(str(targetpath) +'/' +str(m) +'/' +str(d))
			except FileExistsError:
				pass 
			for f in folders:
				filenames = os.listdir(str(histdir) + '/' +str(m) +'/' +str(d) +'/' +str(f))
				try:
					os.mkdir(str(targetpath) +'/' +str(m) +'/' +str(d) +'/' +str(f))
				except FileExistsError:
					pass 
				for k in filenames:
					filepath = str(histdir) + '/' +str(m) + '/' +str(d) + '/' +str(f) +'/' +str(k)
					graphpath = str(targetpath) + '/' +str(m) + '/' +str(d) + '/' +str(f) +'/' +str(k)
					channelloop(str(filepath), str(graphpath))
	return


log = input('Do you want logarithmic plot? Answer yes or no. ')
if log == 'no':
	logy = False
else:
	logy = True
	
fileloop()


end = time.time()
print('Elapsed time = ' +str(end-start) +' s')



##
#hist1 = file.H4FM1
#hist2 = file.H8FM1
#histtot = hist + hist2
#histtot.SetTitle('Total Frequency Plot')


#c1= ROOT.TCanvas('c1')
#hist1.Draw()
#c2= ROOT.TCanvas('c2')
#hist2.Draw()
#c3= ROOT.TCanvas('c3')
#histtot.Draw()
#print(hist)
##







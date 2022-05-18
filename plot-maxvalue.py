import numpy as np
import os
import ROOT
import time
import shutil

start = time.time()
channels = [1,2,3]

voltages = []

maxamps1, maxamps2, maxamps3 = [],[],[]
maxamps = [maxamps1, maxamps2, maxamps3]


targetpath = '/home/bram/Documents/grand-data/graphs'
histdir = '/home/bram/Documents/grand-data/histograms/Casting-X/data-adaq-20220503150954.zip/MD/md030522.f'
number = input('number = ')
file = ROOT.TFile.Open(str(histdir)+str(number) +'.root')

def AmpTooHigh(data,cut=500): #Determines if any measured amplitude is unphysically high
	amp = np.asarray(data)
	for j in amp:
		if j>cut:
			return True
	return False

def AmpTooHighV2(data, cut=8300):
	amp = np.asarray(data)
	if np.max(amp)>cut:
		return True
	else:
		return False

def histtotal(file, channel): #returns the total FM hist of channel j
	total = 0 
	events = 0
	for i in range(5000):
		try:
			hist = eval('file.H' +str(i) +'FM' +str(channel)) #loads the ith histogram of channel j
			if not AmpTooHighV2(eval('file.H' +str(i) +'T1')): #Discard unphysical measurements
				if total == 0: #use the first histogram to create the object
					total = hist
				else:
						total += hist #Add the histograms
				events += 1
			else:
				print( 'Hist' +str(i) +' is rejected')
		except AttributeError: #If the specified histogram doesnt exist continue the loop
			pass
	return total, events

def amp_per_event(hist, events):
	amp = np.asarray(hist)
	maxamp = np.amax(amp)
	maxfreqbin = np.where(amp==maxamp)[0][0]
	bins = hist.GetNbinsX()
	maxfreq = (maxfreqbin-0.5)*250/bins #-1 to correct for python counting, +0.5 to get the middle of the bin
	freqerror = 250/bins *0.5
	return maxamp, maxfreq,freqerror
	
def channelloop():
	for j in channels:
		hist,events = histtotal(file,j)
		try:
			maxamp, maxfreq,freqerror = amp_per_event(hist,events)
			maxamps[j-1].append(maxamp)
		except AttributeError:
			print('Channel ' +str(j) +' is empty.')
	return

def voltageloop():
	numbers = []
	for n in range(np.size(voltages)):
		numbers.append
		
channelloop()


end = time.time()
print('Elapsed time = ' +str(end-start) +' s')

input('Press enter to exit')









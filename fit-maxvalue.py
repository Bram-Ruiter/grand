import numpy as np
import os
import ROOT
import time
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

start = time.time()
channels = [1,2,3]

voltages = np.array([0.5,0.6,1.5,2.0,4.0,5.0,4.8,4.6,4.4,4.2,3.6,3.2,2.8,2.8,2.4])

maxamps1, maxamps2, maxamps3 = [],[],[]
maxamps = [maxamps1, maxamps2, maxamps3]


targetpath = '/home/bram/Documents/grand-data/graphs'
histdir = '/home/bram/Documents/grand-data/histograms/Casting-X/data-adaq-20220518174702.zip/MD/md160522.f'
#number = input('number = ')
#file = ROOT.TFile.Open(str(histdir)+str(number) +'.root')

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
	
def channelloop(file):
	for j in channels:
		hist,events = histtotal(file,j)
		try:
			maxamp, maxfreq,freqerror = amp_per_event(hist,events)
			maxamps[j-1].append(maxamp)
		except AttributeError:
			print('Channel ' +str(j) +' is empty.')
	return

def voltageloop():
	for n in range(np.size(voltages)):
		number=str(n+1).rjust(4,'0')
		file = ROOT.TFile.Open(str(histdir)+str(number) +'.root')
		channelloop(file)
	return
		
voltageloop()

xamps = np.array(maxamps[0])
yamps = np.array(maxamps[1])
zamps = np.array(maxamps[2])
ratioxz = xamps/zamps


def fitfunc(x, a, b):
	return a*x +b


plt.figure(1)
plt.title('Amplitude ratio plot of x/z')
plt.xlabel('Voltage (V)')
plt.ylabel('Ratio')
plt.scatter(voltages, ratioxz)
plt.ylim(bottom = 0)
plt.show()

print(xamps)
print(voltages)
input('')
#xamps = xamps[1:6]
#yamps = yamps[1:6]
#zamps = zamps[1:6]
#voltages = voltages[1:6]

plt.figure(2)
plt.title('Amplitude plot')
plt.xlabel('Voltage (V)')
plt.ylabel('Average amplitude per event')
plt.scatter(voltages, xamps, c='r', label = 'X-Amp')


poptx, pcovx = curve_fit(fitfunc, voltages, xamps)
plt.plot(voltages, fitfunc(voltages, *poptx), 'r--', label ='X-fit: a = %5.3f, b= %5.3f' %tuple(poptx))
plt.scatter(voltages, yamps, c='g', label = 'Y-Amp')

popty, pcovy = curve_fit(fitfunc, voltages, yamps)
plt.plot(voltages, fitfunc(voltages, *popty), 'g--', label ='Y-fit: a = %5.3f, b= %5.3f' %tuple(popty))
plt.scatter(voltages, zamps, c='b', label = 'Z-Amp')

poptz, pcovz = curve_fit(fitfunc, voltages, zamps)
plt.plot(voltages, fitfunc(voltages, *poptz), 'b--', label ='Z-fit: a = %5.3f, b= %5.3f' %tuple(poptz))
plt.legend()
plt.ylim(bottom = 0)
plt.show()


end = time.time()
print('Elapsed time = ' +str(end-start) +' s')

input('Press enter to exit')









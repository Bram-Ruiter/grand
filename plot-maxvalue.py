import numpy as np
import os
import time
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import ROOT


start = time.time()
channels = [1,2,3]

voltages = np.array([0.5,0.6,1.5,2.0,4.0,5.0,4.8,4.6,4.4,4.2,3.6,3.2,2.8,2.8,2.4])

maxamps1, maxamps2, maxamps3 = [],[],[]
maxamps = [maxamps1, maxamps2, maxamps3]

amperrors1, amperrors2, amperrors3 = [],[],[]
amperrors = [amperrors1, amperrors2, amperrors3]


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

def sqamp(hist): #returns squared of amplitude at f broadcast
	amp = np.asarray(hist)
	maxamp =np.amax(amp)
	return maxamp**2

def histtotal(file, channel): #returns the total FM hist of channel j
	total = 0
	events = 0
	sqtotal = 0
	for i in range(5000):
		try:
			hist = eval('file.H' +str(i) +'FM' +str(channel)) #loads the ith histogram of channel j
			if not AmpTooHighV2(eval('file.H' +str(i) +'T1')): #Discard unphysical measurements
				if total == 0: #use the first histogram to create the object
					total = hist
				else:
						total += hist #Add the histograms
				events += 1
				sqtotal += sqamp(hist)
			else:
				print( 'Hist' +str(i) +' is rejected')
		except AttributeError: #If the specified histogram doesnt exist continue the loop
			pass
	return total, events, sqtotal

def amp_per_event(hist, events):
	amp = np.asarray(hist)
	maxamp = np.amax(amp)
	maxfreqbin = np.where(amp==maxamp)[0][0]
	bins = hist.GetNbinsX()
	maxfreq = (maxfreqbin-0.5)*250/bins #-1 to correct for python counting, +0.5 to get the middle of the bin
	freqerror = 250/bins *0.5
	return maxamp/events, maxfreq,freqerror



def channelloop(file):
	for j in channels:
		hist,events,sqtotal = histtotal(file,j)
		try:
			maxamp, maxfreq,freqerror = amp_per_event(hist,events)
			sigma = np.sqrt(sqtotal/events-maxamp**2) #Standard deviation.
			amperrors[j-1].append(sigma)
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

voltages = voltages[3:]
xamps = np.array(maxamps[0])[3:]
xampserror = np.array(amperrors[0])[3:]
yamps = np.array(maxamps[1])[3:]
yampserror = np.array(amperrors[1])[3:]
zamps = np.array(maxamps[2])[3:]
zampserror = np.array(amperrors[2])[3:]
ratioxz = xamps/zamps


def fitfunc(x, a, b):
	return a*x +b


#fitx, covx = curve_fit(func, voltages, xamps)
#fity, covy = curve_fit(func, voltages, yamps)
#fitz, covz = curve_fit(func, voltages, zamps)
#plt.figure(3)
#plt.plot(voltages, fitfunc(voltages, *fitx), 'b--', label ='Z-fit: a = %5.3f, b= %5.3f' %tuple(fitx))
#plt.plot(voltages, fitfunc(voltages, *fity), 'b--', label ='Z-fit: a = %5.3f, b= %5.3f' %tuple(fity))
#plt.plot(voltages, fitfunc(voltages, *fitz), 'b--', label ='Z-fit: a = %5.3f, b= %5.3f' %tuple(fitz))
#fit, cov = curve_fit(fitfunc, voltages, xamps)

#plt.plot(voltages, fitfunc(voltages, *fit))
#plt.scatter(voltages, xamps)
#plt.show()

def ratiograph():
	plt.figure(1)
	plt.title('Amplitude ratio plot of x/z')
	plt.xlabel('Voltage (V)')
	plt.ylabel('Ratio')
	plt.scatter(voltages, ratioxz)
	plt.ylim(bottom = 0)
	plt.show()
	return

def fitgraph():
	fitx, covx = curve_fit(fitfunc, voltages, xamps)
	fity, covy = curve_fit(fitfunc, voltages, yamps)
	fitz, covz = curve_fit(fitfunc, voltages, zamps)

	plt.figure(2)
	plt.title('Amplitude plot')
	plt.xlabel('Voltage (V)')
	plt.ylabel('Average amplitude per event')

	plt.errorbar(voltages, xamps, yerr=xampserror, c='r', fmt = 'o', label = 'X-Amp')
	plt.plot(voltages, fitfunc(voltages, *fitx), 'r-', label ='X-fit: a = %5.3f, b= %5.3f' %tuple(fitx))
	plt.errorbar(voltages, yamps, yerr=yampserror, c='g', fmt = 'o', label = 'Y-Amp')
	plt.plot(voltages, fitfunc(voltages, *fity), 'g-', label ='Y-fit: a = %5.3f, b= %5.3f' %tuple(fity))
	plt.errorbar(voltages, zamps, yerr=zampserror, c='b', fmt = 'o', label = 'Z-Amp')
	plt.plot(voltages, fitfunc(voltages, *fitz), 'b-', label ='Z-fit: a = %5.3f, b= %5.3f' %tuple(fitz))
	plt.legend()
	plt.ylim(bottom = 0)
	plt.show()
	return

def graph():
	plt.figure(1)
	plt.title('Amplitude ratio plot of x/z')
	plt.xlabel('Voltage (V)')
	plt.ylabel('Ratio')
	plt.scatter(voltages, ratioxz)
	plt.grid()
	plt.ylim(bottom = 0)
	plt.show()
	plt.figure(2)
	plt.title('Amplitude plot')
	plt.xlabel('Voltage (V)')
	plt.ylabel('Average amplitude per event')
	plt.scatter(voltages, xamps, c='r', label = 'X-Amp')
	plt.scatter(voltages, yamps, c='g', label = 'Y-Amp')
	plt.scatter(voltages, zamps, c='b', label = 'Z-Amp')
	plt.legend()
	plt.grid()
	plt.ylim(bottom = 0)
	plt.show()
	return

##
a = input('Enter graph or fit ')
if a == 'fit':
	ratiograph()
	fitgraph()
elif a == 'no':
	pass
else:
	graph()



end = time.time()
print('Elapsed time = ' +str(end-start) +' s')

input('Press enter to exit')









import numpy as np
import os
import time
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import ROOT
import itertools


start = time.time()


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

def phase_max(hist,freqbin): #returns phase at certain bin
	phase = np.asarray(hist)
	phase_max = phase[freqbin]
	return phase_max


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
				sqtotal += sqamp(hist) #get the sum of squared amplitudes at broadcast frequency
			else:
				print( 'Hist' +str(i) +' is rejected')
		except AttributeError: #If the specified histogram doesnt exist continue the loop
			pass
	return total, events, sqtotal

def amp_per_event(hist, events):
	amp = np.asarray(hist)
	maxamp = np.amax(amp)
	maxfreqbin = np.where(amp==maxamp)[0][0]
	global bins #this value is used for ylabel i plots
	bins = hist.GetNbinsX()
	ampperevent = maxamp/events
	return ampperevent

def max_freq(hist):
	amp = np.asarray(hist)
	maxamp = np.amax(amp)
	maxfreqbin = np.where(amp==maxamp)[0][0]
	bins = hist.GetNbinsX()
	maxfreq = (maxfreqbin-0.5)*250/bins #-1 to correct for python counting, +0.5 to get the middle of the bin
	freqerror = 250/bins *0.5
	return maxfreq, maxfreqbin, freqerror

def phases(file,channel):
	phases = []
	for i in range(5000):
		try:
			hist = eval('file.H' +str(i) +'FP' +str(channel)) #loads the ith histogram of channel j
			hist3 = eval('file.H' +str(i) +'FP' +str(1)) #always use channel 3 to determine the broadcast frequency.
			maxfreq, maxfreqbin, freqerror = max_freq(hist)

			if not AmpTooHighV2(eval('file.H' +str(i) +'T1')): #Discard unphysical measurements
				phase = phase_max(hist, maxfreqbin)
				phases.append(phase)
			else:
				print( 'Hist' +str(i) +' is rejected')
		except AttributeError: #If the specified histogram doesnt exist continue the loop
			pass
	return phases




def channelloop(file):
	for j in channels:
		hist,events,sqtotal = histtotal(file,j)
		try:
			phase = phases(file,j)
			phasedata[j-1].append(phase)
			maxamp = amp_per_event(hist,events)
			sigma = np.sqrt(sqtotal/events-maxamp**2) #Standard deviation.
			avgerror = sigma/np.sqrt(events) #Error on average of standard distribution
			amperrors[j-1].append(avgerror)
			maxamps[j-1].append(maxamp)
		except AttributeError:
			print('Channel ' +str(j) +' is empty.')
	return

def voltageloop():
	for n in range(np.size(xdata)):
		number=str(n+1).rjust(4,'0')
		file = ROOT.TFile.Open(str(histdir)+str(number) +'.root')
		channelloop(file)
	return


def fitfunc(x, a, b):
	return a*x +b


def constant(x, a):
	return a+ 0*x


def ratiograph():
	plt.figure(1)
	plt.title('Ratio of amplitudes x/z of fourrier transform at broadcast frequency')
	plt.xlabel(xlabel)
	plt.ylabel('Ratio x/z')
	plt.errorbar(xdata, ratioxz, yerr= ratioerr, fmt='o')
	plt.ylim(bottom = 0)
	plt.grid()
	plt.savefig(targetpath +'ratio.pdf')
	return

def ratiofit():
	fit, cov = curve_fit(constant, xdata, ratioxz)
	plt.figure()
	plt.title('Ratio of amplitudes x/z of fourrier transform at broadcast frequency')
	plt.xlabel(xlabel)
	plt.ylabel('Ratio x/z')
	plt.errorbar(xdata, ratioxz, yerr= ratioerr, fmt='o', label='Ratio')
	plt.plot(xdata, constant(xdata, *fit), 'r-', label ='Ratio-fit: c = %5.3f' %tuple(fit))
	plt.ylim(bottom = 0)
	plt.grid()
	plt.legend()
	plt.savefig(targetpath +'ratiofit.pdf')
	plt.clf()
	return

def fitgraph():
	fitx, covx = curve_fit(fitfunc, xdata, xamps)
	fity, covy = curve_fit(fitfunc, xdata, yamps)
	fitz, covz = curve_fit(fitfunc, xdata, zamps)

	plt.figure()
	plt.title('Amplitude of fourrier transform at broadcast frequency')
	plt.xlabel(xlabel)
	plt.ylabel('Average amplitude per event (' +str(bins) +'/250 MHz$^{-1}$)')

	plt.errorbar(xdata, xamps, yerr=xampserror, c='r', fmt = 'o', label = 'X-Amp')
	plt.plot(xdata, fitfunc(xdata, *fitx), 'r-', label ='X-fit: a = %5.3f, b= %5.3f' %tuple(fitx))
	plt.errorbar(xdata, yamps, yerr=yampserror, c='g', fmt = 'o', label = 'Y-Amp')
	plt.plot(xdata, fitfunc(xdata, *fity), 'g-', label ='Y-fit: a = %5.3f, b= %5.3f' %tuple(fity))
	plt.errorbar(xdata, zamps, yerr=zampserror, c='b', fmt = 'o', label = 'Z-Amp')
	plt.plot(xdata, fitfunc(xdata, *fitz), 'b-', label ='Z-fit: a = %5.3f, b= %5.3f' %tuple(fitz))
	plt.legend()
	plt.ylim(bottom = 0)
	plt.grid()
	plt.savefig(targetpath +'scatterfit.pdf')
	plt.clf()
	return

def graph():
	plt.figure(2)
	plt.title('Amplitude of fourrier transform at broadcast frequency')
	plt.xlabel(xlabel)
	plt.ylabel('Average amplitude per event (' +str(bins) +'/250 MHz$^{-1}$)')
	plt.errorbar(xdata, xamps, yerr = xampserror, c='r', fmt='o', label = 'X-Amp')
	plt.errorbar(xdata, yamps, yerr = yampserror, c='g', fmt='o', label = 'Y-Amp')
	plt.errorbar(xdata, zamps, yerr = zampserror, c='b', fmt='o', label = 'Z-Amp')
	plt.legend()
	plt.grid()
	plt.ylim(bottom = 0)
	plt.savefig(targetpath +'scatter.pdf')
	plt.clf()
	return

def phasehist(channel):
	plt.figure(3)
	plt.title('Phase distribution of fourrier transform at broadcast frequency')
	plt.xlabel('Phase')
	plt.ylabel('Count')
	data = phasedata[channel-1]
	dataflat = list(itertools.chain(*data))
	plt.hist(data)
	plt.savefig(targetpath +'phasehist' +str(channel) +'.pdf')
	plt.clf()
	plt.title('Phase distribution of fourrier transform at broadcast frequency')
	plt.xlabel('Phase')
	plt.ylabel('Count')
	plt.hist(dataflat)
	plt.savefig(targetpath +'phasehistflat' +str(channel) +'.pdf')
	plt.clf()
	return

def make_graphs():
	for i in [1,2,3]:
		phasehist(i)
	graph()
	fitgraph()
	ratiofit()
	ratiograph()
	return


channels = [1,2,3]
measurements = []


#voltages Bij voltages beginnen slicen [3:] 1e metingen ongeldig
xdata = np.array([0.5, 0.6, 1.5, 2.0, 4.0, 5.0, 4.8, 4.6, 4.4, 4.2, 3.6, 3.2, 2.8, 2.8, 2.4])
dir = '/home/bram/Documents/grand-data/histograms/Casting-X/'
zip = 'data-adaq-20220518174702.zip/'
m = 'MD'
f = '/md160522.f'
xlabel = 'Voltage (V)'
targetpath = '/home/bram/Documents/grand-data/graphs/Casting-X/' +zip + m +'/voltage'
histdir = dir + zip+ m + f
a = 3 #1e 3 metingen ongeldig
b = None
deltam = [xdata,dir,zip,m,f,xlabel,targetpath,histdir,a,b]
measurements.append(deltam)

#frequencies x:
xdata = np.array([70,80,90,100,110,120,130,140,150,160])
dir = '/home/bram/Documents/grand-data/histograms/Casting-X/'
zip = 'data-adaq-20220519133441.zip/'
m = 'MD'
f = '/md190522.f'
xlabel = 'Frequency (MHz)'
targetpath = '/home/bram/Documents/grand-data/graphs/Casting-X/' +zip + m +'/frequency'
histdir = dir + zip+ m + f
a = None
b = None
deltam = [xdata,dir,zip,m,f,xlabel,targetpath,histdir,a,b]
measurements.append(deltam)


#Distances:
xdistance = (10.0+1.9+28.5+207.8)*np.ones(10) - np.array([0,20,40,60,80,100,120,140,160,180]) #horizontal distance in cm
ydistance = ((80.2-1.0+24.7)-(82.5+2.2))*np.ones(10)
xdata = np.sqrt(xdistance**2+ydistance**2) #absolute distance in cm
xlabel = 'Distance (cm)'
dir = '/home/bram/Documents/grand-data/histograms/Casting-X/'
zip = 'data-adaq-20220519182942.zip/'
m = 'TD'
f = '/td190522.f'
targetpath = '/home/bram/Documents/grand-data/graphs/Casting-X/' +zip + m +'/distance'
histdir = dir + zip+ m + f
a = None
b = None
deltam = [xdata,dir,zip,m,f,xlabel,targetpath,histdir,a,b]
measurements.append(deltam)

#frequencies z:
xdata = np.array([70,80,90,100,110,120,130,140,150,160])
dir = '/home/bram/Documents/grand-data/histograms/Casting-Z/'
zip = 'data-adaq-20220520141911.zip/'
m = 'TD'
f = '/td200522.f'
xlabel = 'Frequency (MHz)'
targetpath = '/home/bram/Documents/grand-data/graphs/Casting-Z/' +zip + m +'/frequency'
histdir = dir + zip+ m + f
a = None
b = None
deltam = [xdata,dir,zip,m,f,xlabel,targetpath,histdir,a,b]
measurements.append(deltam)


def measurementloop():
	for n in range(len(measurements)): #loop over all different measurements
		global xdata
		global dir
		global zip
		global m
		global f
		global xlabel
		global targetpath
		global histdir
		global phasedata
		global maxamps
		global amperrors
		global xamps
		global yamps
		global zamps
		global xampserror
		global yampserror
		global zampserror
		global ratioxz
		global ratioerr
		xdata = measurements[n][0]
		dir = measurements[n][1]
		zip = measurements[n][2]
		m = measurements[n][3]
		f = measurements[n][4]
		xlabel = measurements[n][5]
		targetpath = measurements[n][6]
		histdir = measurements[n][7]
		a = measurements[n][8]
		b = measurements[n][9]
		phasedata = [[],[],[]]
		maxamps = [[],[],[]]
		amperrors = [[],[],[]]
		voltageloop()
		print(np.size(xdata))
		xdata = xdata[a:b]
		xamps = np.array(maxamps[0])[a:b]
		xampserror = np.array(amperrors[0])[a:b]
		yamps = np.array(maxamps[1])[a:b]
		yampserror = np.array(amperrors[1])[a:b]
		zamps = np.array(maxamps[2])[a:b]
		zampserror = np.array(amperrors[2])[a:b]
		ratioxz = xamps/zamps
		ratioerr= np.sqrt(((1/zamps)**2)*xampserror**2 + ((xamps/	(zamps**2))**2)*zampserror**2)
		make_graphs()
	return

measurementloop()


end = time.time()
print('Elapsed time = ' +str(end-start) +' s')

#input('Press enter to exit')





import numpy as np
import os
import ROOT
import time
import shutil

start = time.time()
targetpath = '/home/bram/Documents/grand-data/graphs'
path = '/home/bram/Documents/grand-data/graphs-legacy/castantenna/Histtd29040002'
file = ROOT.TFile.Open(str(path)+'.root')


def AmpTooHighV1(data,cut=500): #Determines if any measured amplitude is unphysically high
	amp = np.asarray(data)
	for j in amp:
		if j>cut:
			return True
	return False

def AmpTooHighV2(data, cut=500): #A bit more effcient than V1
	amp = np.asarray(data)
	if np.max(amp)>cut:
		return True
	else:
		return False


def histtotal(file, channel): #returns the total FM hist of channel j
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

def graph(hist, channel, logy=True):
	bins= hist.GetNbinsX()
	c1 = ROOT.TCanvas('c1','Accumulated Frequency Plot')
	c1.SetGrid()
	if logy:
		c1.SetLogy()
	else:
		pass
	hist.SetTitle('Accumulated Frequency Plot')
	hist.GetXaxis().SetTitle('Frequency (MHz)')
	hist.GetYaxis().SetTitle('Amplitude (1/' +str(bins) +'1/MHz)')
	hist.SetStats(False)
	hist.Draw()
	c1.Update()
	if logy: 
		c1.Print(str(targetpath) +'/nameLogY' +'ch' +str(channel) +'.pdf')
	else:
		c1.Print(str(targetpath) +'graphs/name' +'ch' +str(channel) +'.pdf')
	return 

def channelloop(file):	#Makes graphs for every channel
	for j in range(1,5):
		hist = histtotal(file, j) 
		if hist != 0:	#if hist=0 no recorded events for specified channel
			graph(hist, j)
		else:
			pass
	return	
	
def filelloop(path):
	
	os.listdir(

channelloop(file)


end = time.time()
print('Elapsed time = ' +str(end-start) +' s')

input('Press enter to exit')


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







import numpy as np
import os
import ROOT
import matplotlib.pyplot as plt
import time

path = './zendantenne/Histtd29040001'
file = ROOT.TFile.Open(str(path)+'.root')

def AmpTooHigh(data,cut=500): #Determines if any measured amplitude is unphysically high
	amp = np.asarray(data)
	for j in amp:
		if j>cut:
			return True
	return False

def AmpTooHighV2(data, cut=500):
	amp = np.asarray(data)
	if np.max(amp)>cut:
		return True
	else:
		return False

histtotal = 0

start = time.time()



for i in range(5000):
	try:
		hist = eval('file.H' +str(i) +'FM1') #loads the ith histogram
		if not AmpTooHighV2(eval('file.H' +str(i) +'T1')): #Discard unphysical measurements
			if histtotal == 0: #use the first histogram to create the object
				histtotal = hist
			else:
					histtotal += hist #Add the histograms
		else:
			print( 'Hist' +str(i) +' is rejected')
	except AttributeError: #If the specified histogram doesnt exist continue the loop
		pass


end = time.time()
print('Elapsed time = ' +str(end-start) +' s')

bins= histtotal.GetNbinsX()

c1 = ROOT.TCanvas('c1','Accumulated Frequency Plot')
c1.SetGrid()
c1.SetLogy()
histtotal.SetTitle('Accumulated Frequency Plot')
histtotal.GetXaxis().SetTitle('Frequency (MHz)')
histtotal.GetYaxis().SetTitle('Amplitude (1/' +str(bins) +'1/MHz)')
histtotal.SetStats(False)
histtotal.Draw()
c1.Update()
c1.Print(str(path) +'.pdf')





raw_input('Press enter to exit')


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







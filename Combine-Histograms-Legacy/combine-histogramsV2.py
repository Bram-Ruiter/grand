import numpy as np
import os
import ROOT
import matplotlib.pyplot as plt

file = ROOT.TFile.Open('./noantenna/Histtd21040001.root')

def AmpTooHigh(data,cut=500): #Determines if any measured amplitude is unphysically high
	amp = np.asarray(data)
	for j in amp:
		if j>cut:
			return True
	return False

histtotal = 0

for i in range(5000):
	try:
		hist = eval('file.H' +str(i) +'FM1') #loads the ith histogram
		if not AmpTooHigh(eval('file.H' +str(i) +'T1')): #Discard unphysical measurements
			if histtotal == 0: #use the first histogram to create the object
				histtotal = hist
			else:
				histtotal += hist #Add the histograms
		else:
			print( 'Hist' +str(i) +'is rejected')
	except AttributeError: #If the specified histogram doesnt exist continue the loop
		pass

histtotal.SetTitle('Accumulated Frequency Plot (with filtering)')
histtotal.Draw()

array = np.asarray(histtotal)
bins = np.linspace(0,250,5010)
plt.plot(bins,array)
plt.show()



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







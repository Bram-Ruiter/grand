#No filtering of Data sets in this version
import os
import ROOT

file = ROOT.TFile.Open('./histograms-with-antenna/Hist21040001.root')

histtotal = 0

for i in range(5000):
	try:
		hist = eval('file.H' +str(i) +'FM1') #loads the ith histogram
		if histtotal == 0: #use the first histogram to create the object
			histtotal = hist
		else:
			histtotal += hist #Add the histograms 
	except AttributeError: #If the specified histogram doesnt exist continue the loop
		pass

histtotal.SetTitle('Accumulated Frequency Plot')
histtotal.Draw()


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







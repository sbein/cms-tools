#!/usr/bin/env python

import os, sys, re
from string import *
from rgsutil import *
from time import sleep
from ROOT import *
from glob import glob
import argparse
import pickle

gROOT.SetBatch(1)

NAME = 'x10x20x10'
bkgfiledir = "/afs/desy.de/user/n/nissanuv/work/x1x2x1/bg/skim/sum/type_sum"

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Create skims for x1x2x1 process.')
parser.add_argument('-i', '--input_dir', nargs=1, help='Input Directory', required=False)
parser.add_argument('-p', '--pickle', dest='pickle', help='Use Pickle', action='store_true')
args = parser.parse_args()

input_dir = None
if args.input_dir:
	input_dir = args.input_dir[0]

data_pickle = args.pickle
	
######## END OF CMDLINE ARGUMENTS ########

def main():
    global cut
    
    print("="*80)
    print("\t=== %s: find best cuts ===" % NAME)
    print("="*80)
    
    dir = None
    cuts_name = None
    if input_dir:
    	dir = os.path.realpath(input_dir)
    	cuts_name = os.path.basename(dir)
    else:
    	dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    	cuts_name = NAME
    
    #setStyle()
    
    # Create a 2-D histogram for ROC plot
    msize = 0.20  # marker size for points in ROC plot
    
    xbins =  10000   # number of bins in x (background)
    xmin  =  0.0    # lower bound of x
    xmax  =  1.0    # upper bound of y

    ybins =  10000
    ymin  =  0.0
    ymax  =  1.0

    color = kBlue+1
    hroc  = mkhist2("hroc",
                    "#font[12]{#epsilon_{B}}",
                    "#font[12]{#epsilon_{S}}",
                    xbins, xmin, xmax,
                    ybins, ymin, ymax,
                    color=color)
    hroc.SetMinimum(0)
    hroc.SetMarkerSize(msize)
    
    hrocrej  = mkhist2("hrocrej",
                    "#font[12]{Signal Efficiency}",
                    "#font[12]{Background Rejection}",
                    xbins, xmin, 0.5,
                    ybins, 0.8, ymax,
                    color=color)
    hrocrej.SetMinimum(0)
    hrocrej.SetMarkerSize(msize)
    
    # loop over all cut-points, compute a significance measure Z
    # for each cut-point, and find the cut-point with the highest
    # significance and the associated cuts.

    bestZ   = -1    # best Z value
    bestRow = -1    # row with best cut-point
    
    treename = "RGS"
    varfilename  = None
    var_count = None
    
    ts = 0
    tb = 0
    
    sCount = None
    bCount = None
    
    varfilename  = dir + "/" + "%s.cuts" % cuts_name
    
    if data_pickle:
    	print("Opening pickle!")
	with open(dir + "/output.pickle", "rb") as f:
    		data = pickle.load(f)
    		ts = data[0]
    		tb = data[1]
    		sCount = data[2]
    		bCount = data[3]
    else:
    
    	resultsfilenames = glob(dir + "/single/*")

    	numFiles = 0

    	for resultsfilename in resultsfilenames:
		print("\n\topen RGS file: %s"  % resultsfilename)
		filename = os.path.basename(resultsfilename).split(".")[0].replace("-", "_")
		print("\n\tFilename: " + filename)
		ntuple = Ntuple(resultsfilename, treename)
		variables = ntuple.variables()
		if var_count is None:
		    var_count = {}
		    for name, count in variables:
			print("\t\t%-30s\t%5d" % (name, count))
			var_count[name] = count
		print("\tnumber of cut-points: ", ntuple.size())

		if sCount is None:
			sCount = [0] * ntuple.size()
			bCount = [0] * ntuple.size()

		totals = ntuple.totals()

		# get the totals

		print("totals", totals)
		print("len(totals)", len(totals))

		if filename == "signal":
			ts = totals[0][0]
		else:
			tb += totals[0][0]

		for row, cuts in enumerate(ntuple):
			if row % 100000 == 0:
				print("In row:", row)
			if filename == "signal":
				sCount[row] = cuts.count_signal
			else:
				bCount[row] += cuts("count_" + filename)

		numFiles += 1
		print("Number of files:", numFiles)
    
    	with open(dir + "/output.pickle", "wb") as f:
    		pickle.dump((ts, tb, sCount, bCount), f)
    
    print("Totals:")
    print("Signal: " + str(ts))
    print("Background: " + str(tb))
    for row, b in enumerate(bCount):
    	#print("Row " + str(row))
    	#print("Cuts: ")
    	#print(cuts)
        b  = bCount[row] #  background count        
        s  = sCount[row] #  signal count
        
        fs = s / ts
        fb = b / tb
        
        hroc.Fill(fb, fs)
        hrocrej.Fill(fs, 1-fb)
        #print("----------------------------")
        #print("Fraction Signal: " + str(fs))
        #print("Fraction Background: " + str(fb))

        Z = signalSignificance(s, b)
        if Z > bestZ:
            bestZ = Z
            bestRow = row
        
    
    print("\t== plot ROC ==="	)
    croc = TCanvas("h_%s_ROC" % cuts_name, "ROC", 520, 10, 500, 500)
    croc.cd()
    #croc.SetLogx()
    hroc.Draw()
    croc.Update()
    gSystem.ProcessEvents()    
    croc.SaveAs(dir + "/" + cuts_name + "_eff.pdf")
    hrocrej.Draw()
    croc.Update()
    croc.SaveAs(dir + "/" + cuts_name + "_rej.pdf")
    
    print("\t=== %s: best cut ===" % NAME)
    print("Best Z: " + str(bestZ))
    
    b  = bCount[bestRow]     
    s  = sCount[bestRow]

    fs = s / ts
    fb = b / tb
    print("-------------")
    print("(fs,fb,1-fb)=("+str(fs)+","+str(fb)+","+str(1-fb)+")")
    print("-------------")
    print("b=" + str(b))
    print("s=" + str(s))
    
    
# ---------------------------------------------------------------------
try:
    main()
except KeyboardInterrupt:
    print('\nciao!')
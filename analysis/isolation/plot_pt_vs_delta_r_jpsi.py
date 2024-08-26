#!/usr/bin/env python

from ROOT import *
from glob import glob
from sys import exit
import argparse
import sys
import os
import re
from datetime import datetime
from math import *
import numpy as np

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes"))
import utils
import analysis_ntuples

 
gROOT.SetBatch(True)
gStyle.SetOptStat(0)

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Plot Scale Factors.')
args = parser.parse_args()

#0 - pt1
#1 - deta
def ptdr(x, par):
    delta = x[0]**2-par[1]**2
    if delta < 0:
        print("WHAT?", x[0], par[1])
    return (3.096916**2)/(2*par[0]*(cosh(par[1])-cos(sqrt(delta))))

def main():
    print("Start: " + datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    print("End: " + datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    
    c1 = TCanvas("c1", "c1", 800, 800)
    c1.SetLeftMargin(0.13)
    #c1.SetRightMargin(0.02)
    c1.SetGridx()
    c1.SetGridy()
    
    
    
    hist = None
    
    samples = "sim"
    #samples = "data"
    
    select_jpsi = True
    
    if select_jpsi and samples ==  "sim":
        #basicCond = "tagJpsi == 1 && probeJpsi == 1 && tracks[probeTrack].Pt()>3 && abs(tracks[probeTrack].Eta()) <= 1.2  && Muons[tagMuon].Pt() > 25"
        basicCond = "tagJpsi == 1 && probeJpsi == 1 && tracks[probeTrack].Pt()>2 && Muons[tagMuon].Pt() > 5"
    else:
        #basicCond = "tracks[probeTrack].Pt()>3 && abs(tracks[probeTrack].Eta()) <= 1.2  && Muons[tagMuon].Pt() > 5"
        basicCond = "tracks[probeTrack].Pt()>2 &&  Muons[tagMuon].Pt() > 5 && invMass < 3.2 && invMass > 3.0"
    
    idMuons = True
    if idMuons:
        basicCond += " && tracks_mi[probeTrack] > -1 && Muons_mediumID[tracks_mi[probeTrack]] == 1"
    
    if samples == "sim":
        fileNames = glob("/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_jpsi_single_electron/sum/type_sum/*")
    else:
        fileNames = glob("/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim_jpsi_single_electron/sum/*")
    
    for fileName in fileNames:
        print(fileName)
        rootFile = TFile(fileName)
        c = rootFile.Get('tEvent')
                        
        tmpHist = utils.getHistogramFromTree("hist", c, "tracks[probeTrack].Pt():deltaR", 20, 0, 1, basicCond, False, "hsqrt", False, True, 20, 2, 20)
        
        if hist is None:
            hist = tmpHist.Clone("2dhist")
            hist.SetDirectory(0)
        else:
            hist.Add(tmpHist)
        
        rootFile.Close()
        #break

    # for f in rootfiles:
#         if os.path.basename(f) in plot_par.ignore_bg_files:
#             print("File", f, "in ignore list. Skipping...")
#             continue
#         rootFile = TFile(f)
#         if not_full and i > 0:
#             break
#         i += 1
#         print(f)
#         c = rootFile.Get('tEvent')
    
    #hist = TH1F("ptdrhist", "ptdrhist", 50, 0, 1)
    #hist.SetMinimum(1)
    #hist.SetMaximum(20)
    hist.SetTitle("simulation" if samples ==  "sim" else "data")
    hist.GetYaxis().SetTitle("probe p_{T} [GeV]")
    hist.GetXaxis().SetTitle("#Delta_{}R")
    
    hist.Draw("colz")

    legend = TLegend(.60,.40,.89,.60)
    legend.SetNColumns(1)
    legend.SetBorderSize(1)
    legend.SetFillStyle(0)
    
    fFullModel5 = TF1("ptdr5", ptdr, 0, 1, 2)
    fFullModel5.SetNpx(500);
    fFullModel5.SetParameter(0,5.0)
    fFullModel5.SetParameter(1,0)    
    fFullModel5.SetLineWidth(2)
    fFullModel5.SetLineColor(kYellow)
    
    fFullModel75 = TF1("ptdr75", ptdr, 0, 1, 2)
    fFullModel75.SetNpx(500);
    fFullModel75.SetParameter(0,7.5)
    fFullModel75.SetParameter(1,0)    
    fFullModel75.SetLineWidth(2)
    fFullModel75.SetLineColor(kGray)
    
    fFullModel15 = TF1("ptdr15", ptdr, 0, 1, 2)
    fFullModel15.SetNpx(500);
    fFullModel15.SetParameter(0,15)
    fFullModel15.SetParameter(1,0)    
    fFullModel15.SetLineWidth(2)
    fFullModel15.SetLineColor(kGreen)
    
    fFullModel25 = TF1("ptdr25", ptdr, 0, 1, 2)
    fFullModel25.SetNpx(500);
    fFullModel25.SetParameter(0,25)
    fFullModel25.SetParameter(1,0)    
    fFullModel25.SetLineWidth(2)
    fFullModel25.SetLineColor(kRed)
    
    fFullModel35 = TF1("ptdr2", ptdr, 0, 1, 2)
    fFullModel35.SetNpx(500);
    fFullModel35.SetParameter(0,35)  
    fFullModel35.SetParameter(1,0)    
    fFullModel35.SetLineWidth(2)
    fFullModel35.SetLineColor(kBlue)
    
    fFullModel55 = TF1("ptdr55", ptdr, 0, 1, 2)
    fFullModel55.SetNpx(500);
    fFullModel55.SetParameter(0,55) 
    fFullModel55.SetParameter(1,0)     
    fFullModel55.SetLineWidth(2)
    fFullModel55.SetLineColor(kBlack)
    
    fFullModel85 = TF1("ptdr85", ptdr, 0, 1, 2)
    fFullModel85.SetNpx(500);
    fFullModel85.SetParameter(0,85) 
    fFullModel85.SetParameter(1,0)     
    fFullModel85.SetLineWidth(2)
    fFullModel85.SetLineColor(kMagenta)
    
    fFullModel120 = TF1("ptdr120", ptdr, 0, 1, 2)
    fFullModel120.SetNpx(500);
    fFullModel120.SetParameter(0,150) 
    fFullModel120.SetParameter(1,0)     
    fFullModel120.SetLineWidth(2)
    fFullModel120.SetLineColor(kCyan)
    
    fFullModel5.Draw("SAME")
    fFullModel75.Draw("SAME")
    fFullModel15.Draw("SAME")
    fFullModel25.Draw("SAME")
    fFullModel35.Draw("SAME")
    fFullModel55.Draw("SAME")
    fFullModel85.Draw("SAME")
    fFullModel120.Draw("SAME")
    
    
    legend.AddEntry(fFullModel5, "#Delta#eta=0 tag p_{T} 5.0 [GeV]", 'l')
    legend.AddEntry(fFullModel75, "#Delta#eta=0 tag p_{T} 7.5 [GeV]", 'l')
    legend.AddEntry(fFullModel15, "#Delta#eta=0 tag p_{T} 15 [GeV]", 'l')
    legend.AddEntry(fFullModel25, "#Delta#eta=0 tag p_{T} 25 [GeV]", 'l')
    legend.AddEntry(fFullModel35, "#Delta#eta=0 tag p_{T} 35 [GeV]", 'l')
    legend.AddEntry(fFullModel55, "#Delta#eta=0 tag p_{T} 55 [GeV]", 'l')    
    legend.AddEntry(fFullModel85, "#Delta#eta=0 tag p_{T} 85 [GeV]", 'l')    
    legend.AddEntry(fFullModel120, "#Delta#eta=0 tag p_{T} 150 [GeV]", 'l')    
    
    
    legend.Draw("SAME")
    baseName = "ptdr_barrel"
    if samples == "sim":
        baseName += "_sim"
        if select_jpsi:
            baseName += "_jpsi"
        if idMuons:
            baseName += "_id"
    else:
        baseName += "_data"
    
    c1.SaveAs(baseName + ".pdf")
    

main()
exit(0)
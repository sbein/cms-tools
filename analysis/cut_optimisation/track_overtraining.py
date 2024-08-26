#!/usr/bin/env python

from ROOT import *
from glob import glob
from sys import exit
import argparse
import sys
import math
import os

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib"))

import cut_optimisation
import utils

gROOT.SetBatch(True)
gStyle.SetOptStat(0)

colors = [kBlue-4, kRed+1, kGreen+1, kRed-7, kOrange+1, kTeal-7, kViolet-1, 28, kBlue+1, kMagenta, kYellow, kRed, kSpring, kTeal, kTeal+1, kTeal+2,kTeal+3,kTeal+4,kTeal+5,kTeal+6,kTeal+7,kTeal+8]
mstyles = [20,21,22,23,29,33,34,47,43,45]
mstyles*=3
lstyles = [1, kDashed, kDotted]
lstyles*=5

colorInx = 0

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='ROC Comparison.')
parser.add_argument('-i', '--input_dir', nargs=1, help='Input Dir', required=False)
parser.add_argument('-o', '--output_file', nargs=1, help='Output File', required=True)
args = parser.parse_args()

outputFile = "roc_comparison.pdf"
inputDir = None
if args.output_file:
    outputFile = args.output_file[0]
if args.input_dir:
    inputDir = args.input_dir[0]

if inputDir is None:
    inputDir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/lepton_track/cut_optimisation/tmva"

######## END OF CMDLINE ARGUMENTS ########

memory = []

def plot_rocs():
    dirs = glob(inputDir + "/*")
    dirs.sort()
    print(dirs)

    c2 = TCanvas("c2")
    c1 = TCanvas("c1")

    titlePad = TPad("titlePad", "titlePad",0.0,0.93,1.0,1.0)
    memory.append(titlePad)
    histPad = TPad("histPad", "histPad",0.0,0.0,1.0,0.93)

    titlePad.Draw()
    t = TPaveText(0.0,0.93,1.0,1.0,"NB")
    t.SetFillStyle(0)
    t.SetLineColor(0)
    t.SetTextFont(40);
    t.AddText("Track Selection Overtraining")
    t.Draw()

    histPad.Draw()
    histPad.Divide(2,2)
    c1.Print(outputFile + "[");

    needToDraw = False

    t.Draw();
    titlePad.Update()

    pId = 1

    rocIndx = 0

    count = 0

    for dir in dirs:

        count += 1
        #if count > 2:
        #    break

        name = os.path.basename(dir)

        print("Processing " + name)

        file = [dir]
        c2.cd()
        (testBGHists, trainBGHists, testSignalHists, trainSignalHists, methods, names) = cut_optimisation.get_bdt_hists(file, None, None, None, None, None, None, 40)
        #cut_optimisation.get_mlp_hists(file, testBGHists, trainBGHists, testSignalHists, trainSignalHists, methods, names)
        c1.cd()

        t.Draw();
        titlePad.Update()

        pad = histPad.cd(pId)

        memory.extend(testBGHists)
        memory.extend(trainBGHists)
        memory.extend(testSignalHists)
        memory.extend(trainSignalHists)

        legend = TLegend(0.75, 0.7, 0.95, 0.9)
        memory.append(legend)

        rocIndx += 1

        for inx in range(len(testBGHists)):
    
            testBGHist, trainBGHist, testSignalHist, trainSignalHist, method, name = testBGHists[inx], trainBGHists[inx], testSignalHists[inx], trainSignalHists[inx], methods[inx], names[inx]
            
            cpBlue = utils.colorPalette[2]
            cpRed = utils.colorPalette[6]

            trainBGHist.SetTitle(name)
            trainBGHist.GetXaxis().SetTitle("BDT Output")
            trainBGHist.GetYaxis().SetTitle("Arbitrary Units")

            fillC = TColor.GetColor(cpRed["fillColor"])
            lineC = TColor.GetColor(cpRed["lineColor"])
            trainBGHist.SetFillStyle(cpRed["fillStyle"])
            trainBGHist.SetFillColorAlpha(fillC, 0.35)
            trainBGHist.SetLineColor(lineC)
            trainBGHist.SetLineWidth(1)
            trainBGHist.SetOption("HIST")
            trainBGHist.Draw("HIST")

            legend.AddEntry(trainBGHist, "B (train)", 'F')

            fillC = TColor.GetColor(cpBlue["fillColor"])
            lineC = TColor.GetColor(cpBlue["lineColor"])
            trainSignalHist.SetFillStyle(cpBlue["fillStyle"])
            trainSignalHist.SetFillColorAlpha(fillC, 0.35)
            trainSignalHist.SetLineColor(lineC)
            trainSignalHist.SetLineWidth(1)
            trainSignalHist.SetOption("HIST")
            trainSignalHist.Draw("SAME")
            
            legend.AddEntry(trainSignalHist, "S (train)", 'F')
            
            testBGHist.SetMarkerColor(kRed)
            testBGHist.SetMarkerSize(0.5)
            testBGHist.SetMarkerStyle(20)
            testBGHist.SetOption("p E1")
            testBGHist.SetLineColor(kRed)
            testBGHist.Draw("SAME p E1")
            
            legend.AddEntry(testBGHist, "B (test)", "p e2")
            
            testSignalHist.SetMarkerColor(kBlue)
            testSignalHist.SetMarkerSize(0.5)
            testSignalHist.SetMarkerStyle(20)
            testSignalHist.SetOption("p E1")
            testSignalHist.SetLineColor(kBlue)
            testSignalHist.Draw("SAME p E1")
            
            legend.AddEntry(testSignalHist, "S (test)", "p e2")
            
            

        legend.SetBorderSize(0)
        legend.SetFillStyle(0)
        legend.SetNColumns(1)
        legend.Draw()

        c1.Update()

        needToDraw = True
        
        pId += 1
        if pId > 4:
            pId = 1
            c1.Print(outputFile);
            needToDraw = False;

    if needToDraw:
        print("HERE")
        for id in range(pId, 5):
            print("Clearing pad " + str(id))
            pad = histPad.cd(id)
            pad.Clear()
        c1.Print(outputFile);
    
    c1.Print(outputFile+"]");


if __name__ == "__main__":
    plot_rocs()
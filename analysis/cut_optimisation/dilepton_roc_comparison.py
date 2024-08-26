#!/usr/bin/env python

from ROOT import *
from glob import glob
from sys import exit
import argparse
import sys
import math
import os
import traceback
import logging

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib"))

import cut_optimisation
from lib import utils

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
    inputDir = "/afs/desy.de/user/n/nissanuv/nfs/2lx1x2x1/cut_optimisation/tmva/dilepton_bdt"

######## END OF CMDLINE ARGUMENTS ########

memory = []

cuts = {"low":9,
        "dm5":10,
        "dm7":12,
        "dm9":14,
        "high":18}

def plot_rocs():
    dirs = glob(inputDir + "/*")
    dirs.sort()
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
    t.AddText("Dilepton ROC Comparison")
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
    
        name = os.path.basename(dir)
        #cut = cuts[name]
        print("Processing " + name)
    
        file = [dir]
        c2.cd()
        try:
            (testBGHists, trainBGHists, testSignalHists, trainSignalHists, methods, names) = cut_optimisation.get_bdt_hists(file)
            #condition = "&& invMass < " + str(cut)
            #condition = "1"
            #print("Condition=" + condition)
            #(testBGHistsCut, trainBGHistsCut, testSignalHistsCut, trainSignalHistsCut, methodsCut, namesCut) = cut_optimisation.get_bdt_hists(file, None, None, None, None, None, None, 10000, condition)
        except Exception as e:
                logging.error(traceback.format_exc())
                print("Skipping this one....")
                continue
    
        count += 1
        c1.cd()
    
        t.Draw();
        titlePad.Update()
        
        memory.extend(testBGHists)
        memory.extend(trainBGHists)
        memory.extend(testSignalHists)
        memory.extend(trainSignalHists)
       #  memory.extend(testBGHistsCut)
#         memory.extend(trainBGHistsCut)
#         memory.extend(testSignalHistsCut)
#         memory.extend(trainSignalHistsCut)
        inx = 0
        print("Here!!!!")
        for mode in ([[testBGHists[inx], trainBGHists[inx], testSignalHists[inx], trainSignalHists[inx], methods[inx], names[inx], ""]]):#, [testBGHistsCut[inx], trainBGHistsCut[inx], testSignalHistsCut[inx], trainSignalHistsCut[inx], methodsCut[inx], namesCut[inx], " - invMass Cut"]):
            print("***")
            histPad.cd(pId)
            testBGHist, trainBGHist, testSignalHist, trainSignalHist, method, name, title = mode
            print("title=" + title)
            legend = TLegend(0.2, 0.2, 0.7, 0.45)
            memory.append(legend)
    
            colorInx = 0
    
            hist = TH1F("hroc" + str(rocIndx), name + title, 1000, 0, 1)
            hist.SetMinimum(0)
            hist.SetMaximum(1)
            hist.GetXaxis().SetTitle("#font[12]{#epsilon_{S}}")
            hist.GetYaxis().SetTitle("background rejection (1 - #font[12]{#epsilon_{B}})")

            rocIndx += 1
            hist.Draw("p")
    
            pt = TPaveText(.15,.45,.5,.85, "NDC")
            pt.SetFillColor(0)
            pt.SetTextAlign(11)
            pt.SetBorderSize(0)
    
            memory.append(hist)
            memory.append(pt)
            

            h = TGraph()
            h.SetTitle(name + title)
            memory.append(h)
    
            highestZ, highestS, highestB, highestMVA, ST, BT = cut_optimisation.getHighestZ(trainSignalHist, trainBGHist, testSignalHist, testBGHist, h, utils.LUMINOSITY)

            color = colors[colorInx]
            colorInx += 1

            h.SetLineColor(color)
            h.SetMarkerSize(0.2)
            #hbdt.SetFillColor(kRed)

            h.Draw("same")

            print("highestZ=" + str(highestZ))
            print("highestS=" + str(highestS))
            print("highestB=" + str(highestB))

            hHighestZ = TGraph()
            hHighestZ.SetPoint(0, highestS/ST, 1-highestB/BT)
            #color = colors[colorInx]
            #colorInx += 1
            hHighestZ.SetLineColor(color)
            hHighestZ.SetMarkerColor(color)
            hHighestZ.SetMarkerStyle(kFullCircle)
            #hHighestZ.SetMarkerSize(0.75)
            hHighestZ.SetFillColor(0)
            hHighestZ.Draw("p same")

            memory.append(hHighestZ)

            #legend.AddEntry(h, method + " " + name, "l")
            legend.AddEntry(hHighestZ, method + " "  + "(highest S/#sqrt{S+B})=" + str(highestZ), "lp")
    
            pt.AddText(method + " ST=" + str(ST))
            pt.AddText(method + " BT=" + str(BT))
            pt.AddText(method + " Highest S=" + str(highestS))
            pt.AddText(method + " Highest B=" + str(highestB))
            pt.AddText(method + " HighestMVA=" + str(highestMVA))
    
            legend.SetBorderSize(0)
            legend.SetFillStyle(0)
            legend.SetNColumns(1)
            legend.Draw()
    
            pt.Draw()
    
            c1.Update()
    
            needToDraw = True
            
            pId += 1
            if pId > 4:
                pId = 1
                c1.Print(outputFile);
                needToDraw = False;
            break
    
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
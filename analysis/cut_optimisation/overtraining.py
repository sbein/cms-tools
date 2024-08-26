#!/usr/bin/env python

from ROOT import *
from glob import glob
from sys import exit
import argparse
import sys
import math
import os

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes"))

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
parser.add_argument('-i', '--input_file', nargs=1, help='Input File', required=True)
parser.add_argument('-o', '--output_file', nargs=1, help='Output File', required=True)
parser.add_argument('-m', '--method', nargs=1, help='Method', required=False)
parser.add_argument('-w', '--weight', dest='weight', help='Plot With Weight', action='store_true')
args = parser.parse_args()

outputFile = "roc_comparison.pdf"
method = ""
weight = args.weight
inputFile = None
if args.output_file:
    outputFile = args.output_file[0]
if args.input_file:
    inputFile = args.input_file[0]
    
if args.method:
    method = args.method[0]
print("input", input)
print("method", method)
######## END OF CMDLINE ARGUMENTS ########

memory = []

def plot_rocs():
    # Create canvas
    global method
    canvas = TCanvas("roc", "roc", 520, 10, 1000, 1000)
    canvas.SetTopMargin(0.5 * canvas.GetTopMargin())
    canvas.SetBottomMargin(1 * canvas.GetBottomMargin())
    canvas.SetLeftMargin(1 * canvas.GetLeftMargin())
    canvas.SetRightMargin(0.5 * canvas.GetRightMargin())
    inx = 0
    (testBGHists, trainBGHists, testSignalHists, trainSignalHists, methods, names) = cut_optimisation.get_method_hists([inputFile], method, None, None, None, None, None, None, 40, "", weight)
    testBGHist, trainBGHist, testSignalHist, trainSignalHist, method, name = testBGHists[inx], trainBGHists[inx], testSignalHists[inx], trainSignalHists[inx], methods[inx], names[inx]
    legend = TLegend(0.7, 0.7, 0.9, 0.9)
    
    ST = trainSignalHist.Integral() + testSignalHist.Integral()
    BT = trainBGHist.Integral() + testBGHist.Integral()

    trainSignalHist.Scale(1./ST)
    testSignalHist.Scale(1./ST)
    testBGHist.Scale(1./BT)
    trainBGHist.Scale(1./BT)
    
    maxY = max(trainSignalHist.GetMaximum(), testSignalHist.GetMaximum(), testBGHist.GetMaximum(), trainBGHist.GetMaximum())
    
    cpBlue = utils.colorPalette[2]
    cpRed = utils.colorPalette[6]

    trainBGHist.SetTitle(name)
    trainBGHist.GetXaxis().SetTitle("BDT Output")
    trainBGHist.GetYaxis().SetTitle("Arbitrary Units")
    trainBGHist.SetMaximum(maxY + 0.02)
    
    canvas.SetLogy()

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
    trainSignalHist.Draw("SAME HIST")
    
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
    canvas.Update()
    canvas.SaveAs(outputFile)


if __name__ == "__main__":
    plot_rocs()
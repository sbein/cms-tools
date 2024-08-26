#!/usr/bin/env python3

from ROOT import *
from glob import glob
from sys import exit
import argparse
import sys
import os
import re
from datetime import datetime
import math

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes"))
import utils
import analysis_ntuples

gROOT.SetBatch(True)
gStyle.SetOptStat(0)

gSystem.Load('LumiSectMap_C')
from ROOT import LumiSectMap

#ROOT.UseTTFonts = True
#gEnv.Print()

#lumi = 5746.370
#weight = lumi / utils.LUMINOSITY

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Plot signal region significances')
parser.add_argument('-o', '--output_file', nargs=1, help='Output Filename', required=False)
#parser.add_argument('-s', '--single', dest='single', help='Single', action='store_true')
#parser.add_argument('-c', '--cut', nargs=1, help='Cut', required=False)
#parser.add_argument('-obs', '--obs', nargs=1, help='Obs', required=False)
args = parser.parse_args()

output_file = None

histograms_file = "./sig_bg_histograms.root"
#histograms_file = "./met.root"
s
signals = [
    "mu100_dm4p30",
    "mu100_dm3p28",
    "mu100_dm2p51",
    "mu100_dm1p47",
    "mu100_dm1p13"
]

sam = False

if args.output_file:
    output_file = "signal_region_significance_" + args.output_file[0]
else:
    output_file = "signal_region_significance"


output_dir = "./signal_region_plots"
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

######## END OF CMDLINE ARGUMENTS ########

def main():
    print("Start: " + datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    
    print("Opening histograms file " + histograms_file)
    histograms = TFile(histograms_file, 'read')
    
    for lepNum in [1, 2]:
        for lep in ["Muons", "Electrons"]:
            
            orthOpt = [True, False] if (lepNum == 2 and lep == "Muons") else [False]
            for orth in orthOpt:
                histname = "bg_" + ("1t" if lepNum == 1 else "2l") + "_" + ("orth_" if orth else "") + lep
                print("Getting", histname) 
                bg_hist = histograms.Get(histname)
            
                maximum = bg_hist.GetMaximum()
            
                signal_histograms = []
                for signal in signals:
                
                
                    #"bg_2l_" + ("orth_" if orth else "") + lep + "_" + jetiso
                
                    histname = signal + "_" + ("1t" if lepNum == 1 else "2l") + "_" + ("orth_" if orth else "") + lep
                    print("Getting", histname) 
                    hist = histograms.Get(histname)
                    maximum = max(maximum, hist.GetMaximum())
                    signal_histograms.append(hist)
            
                bg_hist.SetMaximum(maximum)
            
                c1 = TCanvas("c1", "c1", 800, 800)
                c1.cd()
        
                legend = TLegend(0.65, 0.70, 0.87, 0.875)
                legend.SetBorderSize(0)
                legend.SetTextFont(42)
                legend.SetTextSize(0.02)
            
                cpRed = utils.colorPalette[7]
                utils.histoStyler(bg_hist)
                bg_hist.SetTitle("")
                bg_hist.GetXaxis().SetTitle("BDT Output")
                bg_hist.GetYaxis().SetTitle("Number of events")
                #bg_hist.GetYaxis().SetTitleOffset(1.4)
                #bg_hist.GetXaxis().SetLabelSize(0.055)
                #trainBGHist.SetMaximum(maxY + 0.02)
                utils.formatHist(bg_hist, cpRed, 0.35, True)
                # fillC = TColor.GetColor(cpRed["fillColor"])
    #             lineC = TColor.GetColor(cpRed["lineColor"])
    #             bg_hist.SetFillStyle(0)
    #             bg_hist.SetFillColorAlpha(fillC, 0.35)
    #             bg_hist.SetLineColor(lineC)
    #             bg_hist.SetLineWidth(1)
    #             bg_hist.SetOption("HIST")
        
                bg_hist.Draw("HIST")
                
                #print("BinWidth", bg_hist.GetBinWidth())
                # print("*********GetNbinsX", bg_hist.GetNbinsX())
#                 for ibin in range(1, bg_hist.GetNbinsX()):
#                     print("BinWidth", bg_hist.GetBinWidth(ibin))
#                     print("GetBinLowEdge", bg_hist.GetBinLowEdge(ibin))

                legend.AddEntry(bg_hist, "Background", 'F')
            
                for i in range(len(signals)):
                    utils.formatHist(signal_histograms[i], utils.signalCp[i], 0.8)
                    legend.AddEntry(signal_histograms[i], signals[i], 'l')
                    signal_histograms[i].Draw("hist same")
            
            
                legend.Draw("SAME")
            
                c1.Print(output_dir + "/signal_background_" + ("1t" if lepNum == 1 else "2l") + "_" + ("orth_" if orth else "") + lep + ".pdf")
                
                ############# DRAW SIGNIFICANCES ##############
                
                categories = 10
                cut_values = []
                binMax = -1
                
                for category in range(categories):
                
                    significance_histograms = []
                
                    for i in range(len(signals)):
                        significance_histogram = signal_histograms[i].Clone()
                        significance_histogram.Reset()
                        
                        endPoint = signal_histograms[i].GetNbinsX() if binMax == -1 else binMax
                        print("endPoint", endPoint)
                        for ibin in range(1, endPoint):
                            print("calculating for bin", ibin)
                            sig = utils.calcSignificanceCutCount(signal_histograms[i], bg_hist, ibin, binMax-1 if binMax > 0 else -1)
                            print("sig", sig)
                            significance_histogram.SetBinContent(ibin, sig)
                        significance_histograms.append(significance_histogram)
                
                    c1 = TCanvas("c1", "c1", 800, 800)
                    c1.cd()
        
                    legend = TLegend(0.15, 0.70, 0.55, 0.875)
                    legend.SetBorderSize(0)
                    legend.SetTextFont(42)
                    legend.SetTextSize(0.02)
                
                    maximum = 0
                    for i in range(len(signals)):
                        maximum = max(significance_histograms[i].GetMaximum(), maximum)
                    significance_histograms[0].SetMaximum(maximum + 1)
                    utils.histoStyler(significance_histograms[0])
                    significance_histograms[0].SetTitle("")
                    significance_histograms[0].GetXaxis().SetTitle("BDT Output")
                    significance_histograms[0].GetYaxis().SetTitle("Significance")
                
            
                    for i in range(len(signals)):
                        utils.formatHist(significance_histograms[i], utils.signalCp[i], 0.8)
                        legend.AddEntry(significance_histograms[i], signals[i], 'l')
                        if i == 0:
                            significance_histograms[i].Draw("hist")
                        else:
                            significance_histograms[i].Draw("hist same")
                
                    binMax = significance_histograms[1].GetMaximumBin()
                    maxValue = significance_histograms[1].GetXaxis().GetBinCenter(binMax)
                    
                    print("binMax", binMax, "maxValue", "{:0.2f}".format(maxValue))
                    
                    cut_values.append("{:0.2f}".format(maxValue))
                
                    sigLine = TLine(maxValue, 0, maxValue, maximum + 1)
                    sigLine.Draw("SAME")
                    sigLine.SetLineColor(kRed)
                    sigLine.SetLineWidth(2)
                
                    tl = TLatex()
                    tl.SetTextFont(42)
                    tl.SetTextSize(0.04)
                    tl.DrawLatex(maxValue + 0.05, maximum + 0.5,  "{:0.2f}".format(maxValue))
                    
                    legend.Draw("SAME")
            
                    c1.Print(output_dir + "/sr" + str(category + 1) + "_significance_" + ("1t" if lepNum == 1 else "2l") + "_" + ("orth_" if orth else "") + lep + ".pdf")
                
                print("===========")
                print(("1t" if lepNum == 1 else "2l") + "_" + ("orth_" if orth else "") + lep)
                print(cut_values)  
    exit(0)
main()

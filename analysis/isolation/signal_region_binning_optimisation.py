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
import analysis_selections
import plotutils

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
#parser.add_argument('-o', '--output_file', nargs=1, help='Output Filename', required=False)
#parser.add_argument('-s', '--single', dest='single', help='Single', action='store_true')
#parser.add_argument('-c', '--cut', nargs=1, help='Cut', required=False)
#parser.add_argument('-obs', '--obs', nargs=1, help='Obs', required=False)
args = parser.parse_args()

output_file = None



lepNum = 2
wanted_year = "2016"
wanted_lepton = "Electrons"
wanted_lepton = "Muons"

lepNum = 1
wanted_year = "2016"


wanted_lepton = "Electrons"
wanted_lepton = "Muons"

category = "leptons"


if lepNum == 1:
    category = "tracks"


# output_dir = "./signal_region_plots_2016_with_phase1"
# if lepNum == 1:
#     output_dir = "./signal_region_tracks_plots"
# 
# if phase1_2017:
#     output_dir = "./signal_region_plots_0_75_2017"
#     if lepNum == 1:
#         output_dir = "./signal_region_tracks_plots_2017"


histograms_file = "../scripts/sig_bg_histograms_data_driven_" + wanted_year + "_" + category + "_uniform_binning_new.root"
output_dir = "./signal_region_plots_" + wanted_year + "_" + category + "_" + wanted_lepton + "_data_driven_fixed"

if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

# if lepNum == 1:
#     histograms_file = "../scripts/sig_bg_histograms_for_track_category.root"
# else:
#     #histograms_file = "./sig_bg_histograms_for_jet_iso_scanCorrJetNoMultIso_no_tautau_after_mht_with_data.root"
#     histograms_file = "./sig_bg_histograms_for_jet_iso_scanCorrJetNoMultIso_with_tautau_after_mht_with_data.root"
#     histograms_file = "./sig_bg_histograms_for_jet_iso_scanCorrJetNoMultIso_with_tautau_2016_with_phase1.root"


# signals = [
#     "mu100_dm4p30",
#     "mu100_dm3p28",
#     "mu100_dm2p51",
#     "mu100_dm1p47",
#     "mu100_dm1p13"
# ]
# 
# phase1_2017 = False
# 
# if phase1_2017:
#     signals = [
#         "mChipm100GeV_dm2p259GeV",
#         "mChipm100GeV_dm1p759GeV",
#         "mChipm100GeV_dm1p259GeV",
#         "mChipm100GeV_dm0p759GeV",
#         "mChipm100GeV_dm0p559GeV"
#     ]
#     histograms_file = "./sig_bg_histograms_for_jet_iso_scanCorrJetNoMultIso_with_tautau_2017.root"

signals = [
    "mChipm100GeV_dm2p26GeV",
    "mChipm100GeV_dm1p76GeV",
    "mChipm100GeV_dm1p26GeV",
    "mChipm100GeV_dm0p96GeV",
    "mChipm100GeV_dm0p76GeV",
    "mChipm100GeV_dm0p56GeV"
]

if wanted_year != "2016":
    signals = [
        "mChipm100GeV_dm2p259GeV",
        "mChipm100GeV_dm1p759GeV",
        "mChipm100GeV_dm1p259GeV",
        "mChipm100GeV_dm0p959GeV",
        "mChipm100GeV_dm0p759GeV",
        "mChipm100GeV_dm0p559GeV"
    ]

index_to_optimise = 2

# index_to_optimise = 1
# ===========
# 2l_Muons
# ['-1.00', '-1.00', '-0.05', '0.00', '0.05', '0.20', '0.25', '0.35', '0.45', '0.60']
# ===========
# 2l_Electrons
# ['-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '0.10', '0.20', '0.30']
# index_to_optimise = 2
# ===========
# 2l_Muons
# ['-0.25', '-0.20', '0.05', '0.20', '0.25', '0.30', '0.35', '0.40', '0.45', '0.55']
# ===========
# 2l_Electrons
# ['-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '0.10', '0.20', '0.30']
# index_to_optimise = 3
# ===========
# 2l_Muons
# ['-1.00', '-1.00', '-1.00', '-0.45', '0.00', '0.15', '0.20', '0.25', '0.35', '0.45']
# ===========
# 2l_Electrons
# ['-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '0.15']
# index_to_optimise = 4
# ===========
# 2l_Muons
# ['-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-0.05', '0.35', '0.40', '0.50']
# ===========
# 2l_Electrons
# ['-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00']

#### 2017 version ######
# 2l_Muons
# ['-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '0.10', '0.30', '0.40', '0.45']
# ===========
# 2l_Electrons
# ['-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00']



#jetiso = analysis_selections.jetIsos


#29/10 data driven values

# 2016
# ===========
# 2l_orth_Muons
# ['-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-0.15', '0.35', '0.45']
# ===========
# 2l_Muons
# ['-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-0.15', '0.35', '0.45']


# 2017
# 2l_orth_Muons
# ['-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '0.10', '0.30', '0.45']
# ===========
# 2l_Muons
# ['-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '0.10', '0.30', '0.50']

# 2018

# ===========
# 2l_orth_Muons
# ['-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '0.00', '0.25', '0.30', '0.40']
# ===========
# 2l_Muons
# ['-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '0.00', '0.25', '0.30', '0.40']

######## END OF CMDLINE ARGUMENTS ########

def main():
    print("Start: " + datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    
    print("Opening histograms file " + histograms_file)
    
    plotting = plotutils.Plotting()
    currStyle = plotting.setStyle()
    
    cut_values = {}
    
    histograms = TFile(histograms_file, 'read')
    
    for lep in [wanted_lepton]:
        
        orthOpt = [True, False] if (lepNum == 2 and lep == "Muons") else [False]
        for orth in orthOpt:
            
            #if orth:
            #    continue
            #"bg_2l_" + ("orth_" if orth else "") + lep + "_" + jetiso[lep]
            #histname = "bg_" + ("1t" if lepNum == 1 else "2l") + "_" + ("orth_" if orth else "") + lep + "_" + jetiso[lep]
            histname = "bg_" + ("1t" if lepNum == 1 else "2l") + "_" + lep + ("_orth" if orth else "")
            histname = "bg" + ("1t" if lepNum == 1 else "2l") + lep + ("Orth" if orth else "") + ("ChargeSymmetric" if lepNum == 1 else "")
            print("Getting", histname) 
            bg_hist = histograms.Get(histname)
        
            maximum = bg_hist.GetMaximum()
        
            signal_histograms = []
            for signal in signals:
                
                #histname = signal + "_" + ("1t" if lepNum == 1 else "2l") + "_" + ("orth_" if orth else "") + lep + "_" + jetiso[lep]
                histname = signal + "_" + ("1t" if lepNum == 1 else "2l") + "_" + lep + ("_orth" if orth else "") # + "_" + jetiso[lep]
                histname = signal + ("1t" if lepNum == 1 else "2l") + lep + ("Orth" if orth else "") # + "_" + jetiso[lep]
                print("Getting", histname) 
                hist = histograms.Get(histname)
                maximum = max(maximum, hist.GetMaximum())
                signal_histograms.append(hist)
        
            bg_hist.SetMaximum(maximum)
        
            c1 = plotting.createCanvas("c1")
            c1.cd()
    
            legend = TLegend(0.65, 0.70, 0.87, 0.875)
            legend.SetBorderSize(0)
            legend.SetTextFont(42)
            legend.SetTextSize(0.02)
        
            cpRed = plotutils.defaultColorPalette[1]
            print(cpRed)
            #utils.histoStyler(bg_hist)
            bg_hist.UseCurrentStyle()
            bg_hist.SetTitle("")
            bg_hist.GetXaxis().SetTitle("BDT Output")
            bg_hist.GetYaxis().SetTitle("Number of events")
            #bg_hist.GetYaxis().SetTitleOffset(1.4)
            #bg_hist.GetXaxis().SetLabelSize(0.055)
            #trainBGHist.SetMaximum(maxY + 0.02)
            
            plotutils.setHistColorFillLine(bg_hist, cpRed, 0.35, True)
            #utils.formatHist(bg_hist, cpRed, 0.35, True)
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
                signal_histograms[i].UseCurrentStyle()
                plotutils.setHistColorFillLine(signal_histograms[i], plotutils.signalCp[i])
                legend.AddEntry(signal_histograms[i], signals[i], 'l')
                signal_histograms[i].Draw("hist same")
        
        
            legend.Draw("SAME")
        
            c1.Print(output_dir + "/signal_background_" + ("1t" if lepNum == 1 else "2l") + "_" + ("orth_" if orth else "") + lep + ".pdf")
            
            ############# DRAW SIGNIFICANCES ##############
            
            categories = 10
            cut_values[lep+ ("_orth" if orth else "")] = []
            binMax = -1
            
            for category in range(categories):
            
                significance_histograms = []
            
                for i in range(len(signals)):
                    significance_histogram = signal_histograms[i].Clone()
                    significance_histogram.Reset()
                    significance_histogram.UseCurrentStyle()
                    
                    endPoint = signal_histograms[i].GetNbinsX() if binMax == -1 else binMax
                    print("endPoint", endPoint)
                    for ibin in range(1, endPoint):
                        print("calculating for bin", ibin)
                        sig = utils.calcSignificanceCutCount(signal_histograms[i], bg_hist, ibin, binMax-1 if binMax > 0 else -1)
                        print("sig", sig)
                        significance_histogram.SetBinContent(ibin, sig)
                    significance_histograms.append(significance_histogram)
            
                c1 = plotting.createCanvas("c1")
                c1.cd()
    
                legend = TLegend(0.2, 0.70, 0.6, 0.875)
                legend.SetBorderSize(0)
                legend.SetFillStyle(0)
                legend.SetTextFont(42)
                #legend.SetTextSize(0.02)
            
                maximum = 0
                for i in range(len(signals)):
                    maximum = max(significance_histograms[i].GetMaximum(), maximum)
                significance_histograms[0].SetMaximum(maximum + 1)
                significance_histograms[0].UseCurrentStyle()
                #utils.histoStyler(significance_histograms[0])
                significance_histograms[0].SetTitle("")
                significance_histograms[0].GetXaxis().SetTitle("BDT Output")
                significance_histograms[0].GetYaxis().SetTitle("Significance")
            
        
                for i in range(len(signals)):
                    plotutils.setHistColorFillLine(significance_histograms[i], plotutils.signalCp[i], 1)
                    #utils.formatHist(significance_histograms[i], utils.signalCp[i], 0.8)
                    legend.AddEntry(significance_histograms[i], signals[i], 'l')
                    if i == 0:
                        significance_histograms[i].Draw("hist")
                    else:
                        significance_histograms[i].Draw("hist same")
            
                binMax = significance_histograms[index_to_optimise].GetMaximumBin()
                maxValue = significance_histograms[index_to_optimise].GetXaxis().GetBinLowEdge(binMax)
                
                print("binMax", binMax, "maxValue", "{:0.2f}".format(maxValue))
                
                cut_values[lep+ ("_orth" if orth else "")].append("{:0.2f}".format(maxValue))
            
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
    for lep in [wanted_lepton]:
        
        orthOpt = [True, False] if (lepNum == 2 and lep == "Muons") else [False]
        for orth in orthOpt:
            
            #if orth:
            #    continue        
            print("===========")
            print(("1t" if lepNum == 1 else "2l") + "_" + ("orth_" if orth else "") + lep)
            print(list(reversed(cut_values[lep+ ("_orth" if orth else "")])))  

main()

#!/usr/bin/env python

from ROOT import *
from glob import glob
from sys import exit
import argparse
import sys
import os
import re

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes"))
import utils
import analysis_ntuples
import analysis_tools
import cut_optimisation
import plotutils
import analysis_selections

gROOT.SetBatch(True)
gStyle.SetOptStat(0)

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Plot observealbes for tracks.')
parser.add_argument('-i', '--input', nargs=1, help='Input Range', required=False)
parser.add_argument('-m', '--method', nargs=1, help='Method', required=False)
parser.add_argument('-o', '--output_file', nargs=1, help='Output Filename', required=False)
parser.add_argument('-w', '--weight', dest='weight', help='Plot With Weight', action='store_true')
parser.add_argument('-n', '--normalise', dest='normalise', help='Normalise', action='store_true')
args = parser.parse_args()


output_file = None
method = ""
weight = args.weight
normalise = args.normalise
input = "/afs/desy.de/user/n/nissanuv/nfs/2lx1x2x1/cut_optimisation/tmva/dilepton_bdt/low"
if args.output_file:
    output_file = args.output_file[0]
if args.input:
    input = args.input[0]
if args.method:
    method = args.method[0]

######## END OF CMDLINE ARGUMENTS ########


phase = "Phase 0"
phase = "Phase 1"


category = "Tracks"
category = "Event_Dilepton"
category = "Event_Ex_Track"


lepton = "Muons"
lepton = "Electrons"



postfix_to_plot = ""
#postfix_to_plot = "_new_skimming"

track_muon_2016_input = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/lepton_track/cut_optimisation/tmva/Muons"
track_muon_phase1_input = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/lepton_track_phase1/cut_optimisation/tmva/Muons"

track_electrons_2016_input = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/lepton_track/cut_optimisation/tmva/Electrons"
track_electrons_phase1_input = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/lepton_track_phase1/cut_optimisation/tmva/Electrons"

event_dilepton_muon_2016_input = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/cut_optimisation/tmva/dilepton_bdt/recoMuons" +  analysis_selections.jetIsos["Muons"]
event_dilepton_muon_phase1_input = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/cut_optimisation/tmva/dilepton_bdt_phase1/recoMuons" +  analysis_selections.jetIsos["Muons"]

event_ex_track_muon_2016_input = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/cut_optimisation/tmva/dilepton_bdt/exTrackMuons" +  analysis_selections.jetIsos["Muons"]
event_ex_track_muon_phase1_input = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/cut_optimisation/tmva/dilepton_bdt_phase1/exTrackMuons" +  analysis_selections.jetIsos["Muons"]

event_ex_track_electron_2016_input = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/cut_optimisation/tmva/dilepton_bdt/exTrackElectrons" +  analysis_selections.jetIsos["Electrons"]
event_ex_track_electron_phase1_input = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/cut_optimisation/tmva/dilepton_bdt_phase1/exTrackElectrons" +  analysis_selections.jetIsos["Electrons"]


#event_dilepton_electron_2016_input = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/cut_optimisation/tmva/dilepton_bdt/recoMuons" +  analysis_selections.jetIsos["Muons"]
#event_dilepton_electron_phase1_input = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/cut_optimisation/tmva/dilepton_bdt_phase1/recoMuons" +  analysis_selections.jetIsos["Muons"]


track_muon_method = "Muons" + analysis_selections.jetIsos["Muons"]
track_electron_method = "Electrons" + analysis_selections.jetIsos["Electrons"]

event_dilepton_muon_method = "recoMuons" + analysis_selections.jetIsos["Muons"]

method = track_muon_method

if lepton == "Electrons":
    method = track_electron_method

stamp_txt = lepton + " " + phase

input = track_muon_2016_input

y_axis_label = category

if lepton == "Electrons":
    input = track_electrons_2016_input
    if category == "Event_Ex_Track":
        input = event_ex_track_electron_2016_input
        method = "exTrackElectrons" + analysis_selections.jetIsos["Electrons"]
        y_axis_label = "Events"
elif lepton == "Muons":
    if category == "Event_Dilepton":
        input = event_dilepton_muon_phase1_input
        method = event_dilepton_muon_method
        y_axis_label = "Events"
    elif category == "Event_Ex_Track":
        input = event_ex_track_muon_2016_input
        method = "exTrackMuons" + analysis_selections.jetIsos["Muons"]
        y_axis_label = "Events"


if phase == "Phase 1":
    if category == "Tracks":
        if lepton == "Muons":
            input = track_muon_phase1_input
        else:
            input = track_electrons_phase1_input
    elif category == "Event_Ex_Track":
        if lepton == "Muons":
            input = event_ex_track_muon_phase1_input
        else:
            input = event_ex_track_electron_phase1_input

if not output_file:
    output_file = "overtraining_" + category + "_" + lepton + "_" + phase.replace(" ", "_") + postfix_to_plot + ".pdf"

print("====================")
print("Running for input: " + input)
print("method", method)
print("category", category)
print("====================")

def main():

    print("Plotting observable")
    c2 = TCanvas("c2")
    plotting = plotutils.Plotting()
    currStyle = plotting.setStyle()
    
    c1 = plotting.createCanvas("c1")
    
    
    
    #c1.SetBottomMargin(0.16)
    #c1.SetLeftMargin(0.18)
    
    
    global method
    global normalise
    
    file = [input]
    c2.cd()
    #(testBGHists, trainBGHists, testSignalHists, trainSignalHists, methods, names) = cut_optimisation.get_bdt_hists(file, None, None, None, None, None, None, 40)
    (testBGHists, trainBGHists, testSignalHists, trainSignalHists, methods, names) = cut_optimisation.get_method_hists(file, method, None, None, None, None, None, None, 40, "", weight)
    #cut_optimisation.get_mlp_hists(file, testBGHists, trainBGHists, testSignalHists, trainSignalHists, methods, names)
    c1.cd()
    
    c1.Print(output_file+"[");
    
    #c1.SetLogy()
    
    legend = TLegend(0.75, 0.70, 0.90, 0.875)
    legend.UseCurrentStyle()
    legend.SetBorderSize(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.05)
    
    for inx in range(len(testBGHists)):
    
        testBGHist, trainBGHist, testSignalHist, trainSignalHist, method, name = testBGHists[inx], trainBGHists[inx], testSignalHists[inx], trainSignalHists[inx], methods[inx], names[inx]
        
        ST = trainSignalHist.Integral() + testSignalHist.Integral()
        BT = trainBGHist.Integral() + testBGHist.Integral()

        if normalise:
            trainSignalHist.Scale(1./ST)
            testSignalHist.Scale(1./ST)
            testBGHist.Scale(1./BT)
            trainBGHist.Scale(1./BT)
            
        maxY = max(trainSignalHist.GetMaximum(), testSignalHist.GetMaximum(), testBGHist.GetMaximum(), trainBGHist.GetMaximum())
        
        cpRed = plotutils.bdtColors[0]
        cpBlue = plotutils.bdtColors[1]
        #utils.histoStyler(trainBGHist)
        trainBGHist.UseCurrentStyle()
        
        trainBGHist.SetTitle("")
        trainBGHist.GetXaxis().SetTitle("BDT Output")
        trainBGHist.GetYaxis().SetTitle(y_axis_label)
        
        #trainBGHist.GetYaxis().SetTitleOffset(1.4)
        #trainBGHist.GetXaxis().SetLabelSize(0.055)
        trainBGHist.SetMaximum(maxY + 1000)
        
        plotutils.setHistColorFillLine(trainBGHist, cpRed)
        
        #fillC = TColor.GetColor(cpRed["fillColor"])
        #lineC = TColor.GetColor(cpRed["lineColor"])
        
        # trainBGHist.SetFillStyle(cpRed["fillStyle"])
#         trainBGHist.SetFillColorAlpha(fillC, 0.35)
#         trainBGHist.SetLineColor(lineC)
#         trainBGHist.SetLineWidth(1)
        trainBGHist.SetOption("HIST")
        
        trainBGHist.Draw("HIST")

        legend.AddEntry(trainBGHist, "B (train)", 'F')

        plotutils.setHistColorFillLine(trainSignalHist, cpBlue)

        # fillC = TColor.GetColor(cpBlue["fillColor"])
#         lineC = TColor.GetColor(cpBlue["lineColor"])
#         trainSignalHist.SetFillStyle(cpBlue["fillStyle"])
#         trainSignalHist.SetFillColorAlpha(fillC, 0.35)
#         trainSignalHist.SetLineColor(lineC)
#         trainSignalHist.SetLineWidth(1)
        trainSignalHist.SetOption("HIST")
        trainSignalHist.Draw("HIST SAME")
        
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
    
        legend.Draw("SAME")

    #utils.stamp_plot()
    plotting.stampPlot(c1, stamp_txt, plotutils.StampStr.SIM, "", True, False)
    #gPad.SetLogy();
    #utils.stampFab("35.9")
    c1.Print(output_file);
    c1.Print(output_file+"]");
    exit(0)

main()



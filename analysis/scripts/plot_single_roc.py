#!/usr/bin/env python

from ROOT import *
from glob import glob
from sys import exit
import argparse
import sys
import os
import re

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib"))
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
args = parser.parse_args()

output_file = None
method = ""
weight = args.weight
input = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/cut_optimisation/tmva/dilepton_bdt/exTrackElectronsCorrJetIso10"
if args.output_file:
    output_file = args.output_file[0]
if args.input:
    input = args.input[0]
if args.method:
    method = args.method[0]

print("input", input)
print("method", method)
######## END OF CMDLINE ARGUMENTS ########

print("Running for input: " + input)

phase = "Phase 1"
phase = "Phase 0"


category = "Tracks"
category = "Event_Dilepton"
category = "Event_Ex_Track"

lepton = "Electrons"
lepton = "Muons"



postfix_to_plot = "_new_training_compare"
postfix_to_plot = ""

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

mva_cut = analysis_selections.track_mva_cut[lepton]

if not output_file:
    output_file = "roc_" + category + "_" + lepton + "_" + phase.replace(" ", "_") + postfix_to_plot + ".pdf"

def main():

    print("Plotting observable")
    c2 = TCanvas("c2")
    plotting = plotutils.Plotting()
    currStyle = plotting.setStyle()
    
    c1 = plotting.createCanvas("c1")

    #memory = []
    
    global method
    
    file = [input]
    c2.cd()
    #(testBGHists, trainBGHists, testSignalHists, trainSignalHists, methods, names) = cut_optimisation.get_bdt_hists(file, None, None, None, None, None, None, 40)
    (testBGHists, trainBGHists, testSignalHists, trainSignalHists, methods, names) = cut_optimisation.get_method_hists(file, method, None, None, None, None, None, None, 40, "", weight)
    
    #get_method_hists(folders, method, gtestBGHists=None, gtrainBGHists=None, gtestSignalHists=None, gtrainSignalHists=None, gmethods=None, gnames=None, bins=10000, condition="", weight=False):
    #file = ["/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/lepton_track/cut_optimisation/tmva_before_removal_of_vars/Muons" ]
    #cut_optimisation.get_method_hists(file, method, testBGHists, trainBGHists, testSignalHists, trainSignalHists, methods, names, 40, "", weight)
    
    #file = ["/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/lepton_track_before_var_fix/cut_optimisation/tmva/Muons" ]
    #cut_optimisation.get_method_hists(file, method, testBGHists, trainBGHists, testSignalHists, trainSignalHists, methods, names, 40, "", weight)
    
    
    #cut_optimisation.get_mlp_hists(file, testBGHists, trainBGHists, testSignalHists, trainSignalHists, methods, names)
    #def get_bdt_hists(folders, testBGHists=None, trainBGHists=None, testSignalHists=None, trainSignalHists=None, methods=None, names=None, bins=10000,  condition=""):
    #    return get_method_hists(folders, "BDT", testBGHists, trainBGHists, testSignalHists, trainSignalHists, methods, names, bins, condition)

    c1.cd()
    
    c1.Print(output_file+"[");
    
    hist = TH1F("hroc", "", 1000, 0, 1)
    hist.UseCurrentStyle()
    hist.SetMinimum(0)
    hist.SetMaximum(1)
    #hist.GetXaxis().SetTitle("#font[12]{#varepsilon_{S}}")
    hist.GetXaxis().SetTitle("#varepsilon_{s}")
    #hist.GetYaxis().SetTitle("background rejection (1 - #font[12]{#varepsilon_{B}})")
    hist.GetYaxis().SetTitle("background rejection (1 - #varepsilon_{b})")
    #utils.histoStyler(hist)
    
    hist.GetYaxis().SetTitleOffset(1.0)
    #hist.GetXaxis().SetLabelSize(0.055)
    hist.Draw()
    
    legend = TLegend(0.18, 0.6, 0.3, 0.7)
    legend.UseCurrentStyle()
    legend.SetBorderSize(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.05)
    legend.SetTextAlign(12)
    
    memory = []
    
    for inx in range(len(testBGHists)):
    
        testBGHist, trainBGHist, testSignalHist, trainSignalHist, method, name = testBGHists[inx], trainBGHists[inx], testSignalHists[inx], trainSignalHists[inx], methods[inx], names[inx]
        h = TGraph()
        memory.append(h)
        S, B, ST, BT = cut_optimisation.getRocWithMvaCut(trainSignalHist, trainBGHist, testSignalHist, testBGHist, mva_cut, h)
        h.SetTitle(name)
        h.SetLineColor(plotutils.rocCurvesColors[inx])
        h.SetLineWidth(1)
        #h.SetMarkerSize(0.2)
        #hbdt.SetFillColor(kRed)
        #if inx == 0:
        h.Draw("same")
        #legend.Draw("same")
        
        
        mvaCutPoint = TGraph()
        memory.append(mvaCutPoint)
        print("x=",S/ST,"y=",1-B/BT)
        mvaCutPoint.SetPoint(0, S/ST, 1-B/BT)
        #mvaCutPoint.SetPoint(0, 0.5, 0.5)
        #color = colors[colorInx]
        #colorInx += 1
        #mvaCutPoint.SetLineColor(kBlack)
        mvaCutPoint.SetMarkerColor(plotutils.rocCurvesColors[inx+1])
        mvaCutPoint.SetMarkerSize(1)
        mvaCutPoint.SetMarkerStyle(20)
        mvaCutPoint.Draw("p same")
        
        legend.AddEntry(mvaCutPoint, "BDT > " + str(mva_cut) + " (#varepsilon_{s}, #varepsilon_{b})=(" + "{:.2f}".format(S/ST) + "," + "{:.2f}".format( B/BT ) + ")", 'p')
    legend.Draw("same")
        
        # tl = TLatex()
#         tl.SetNDC()
#         tl.SetTextSize(0.03) 
#         tl.SetTextFont(42)
#         tl.DrawLatex(0.9, 0.8, "BDT > 0")
#         
    
    #legend.Draw("SAME")
    plotting.stampPlot(c1, stamp_txt, plotutils.StampStr.SIM, "", True, False)
    #utils.stampFab("35.9")
    c1.Print(output_file);
    c1.Print(output_file+"]");
    exit(0)

main()



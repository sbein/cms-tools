#!/usr/bin/env python

from ROOT import *
from glob import glob
from sys import exit
import argparse
import sys
import os
import re

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes"))
import utils
import analysis_ntuples
import analysis_tools

gROOT.SetBatch(True)
gStyle.SetOptStat(0)

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Plot observealbes for tracks.')
parser.add_argument('-i', '--input', nargs=1, help='Input Range', required=False)
parser.add_argument('-o', '--output_file', nargs=1, help='Output Filename', required=True)
args = parser.parse_args()


output_file = None
input = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/sum/higgsino_mu100_dm2p51Chi20Chipm.root"
if args.output_file:
    output_file = args.output_file[0]
if args.input:
    input = args.input[0]
######## END OF CMDLINE ARGUMENTS ########

print("Running for input: " + input)

def main():

    print("Plotting observable")

    c1 = TCanvas("c1", "c1", 800, 800)
    c1.SetBottomMargin(0.16)
    c1.SetLeftMargin(0.16)
    #c1 = utils.mkcanvas()
    #memory = []
    c1.Print(output_file+"[");
    
    #legend = TLegend(.55,.75,.89,.89)
    legend = TLegend(.2,.75,.89,.89)
    legend.SetBorderSize(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.05)
    
    files = [input]
    
    print(files)
    
    sh = utils.UOFlowTH1F("sh", "", 30, 0, 8)
    bh = utils.UOFlowTH1F("bh", "", 30, 0, 8)
    utils.histoStyler(sh)
    utils.histoStyler(bh)
    
    for file in files:
        f = TFile(file)
        c = f.Get('tEvent')
        nentries = c.GetEntries()
        print('Analysing', nentries, "entries")
        for ientry in range(nentries):
            c.GetEntry(ientry)
            if ientry % 1000 == 0:
                print("Processing " + str(ientry) + " weight=" + str(c.Weight))
            if analysis_ntuples.isX1X2X1Process(c):
                genZL, genNonZL = analysis_ntuples.classifyGenZLeptons(c)
                if genZL is None:
                    print("WHAT?!")
                    continue
                nL = c.Electrons.size() + c.Muons.size()
                l1 = None
                l2 = None
                if c.Electrons.size() == 2 and c.Electrons_charge[0] * c.Electrons_charge[1] < 0:
                    l1 = c.Electrons[0]
                    l2 = c.Electrons[1]
                elif c.Muons.size() == 2 and c.Muons_charge[0] * c.Muons_charge[1] < 0:
                    l1 = c.Muons[0]
                    l2 = c.Muons[1]
                if l1 is not None:
                    if l1.Pt() < 5 or l2.Pt() < 5:
                        continue
                    #print(l1, genZL, c)
                    minZ, minCanZ = analysis_ntuples.minDeltaRGenParticles(l1, genZL, c.GenParticles)
                    if minZ > 0.1:
                        #print("NO")
                        continue
                    minZ, minCanZ = analysis_ntuples.minDeltaRGenParticles(l2, genZL, c.GenParticles)
                    if minZ > 0.1:
                        #print("NO")
                        continue
                    sh.Fill((l1 + l2).M(), c.Weight)
                else:
                    ch1 = None
                    if c.Electrons.size() == 1:
                        l1 = c.Electrons[0]
                        ch1 = c.Electrons_charge[0]
                    elif c.Muons.size() == 1:
                        l1 = c.Muons[0]
                        ch1 = c.Muons_charge[0]
                    if not l1:
                        continue
                    if l1.Pt() < 5:
                        continue
                    if not genZL:
                        continue
                    for ti in range(c.tracks.size()):
                        if c.tracks_trkRelIso[ti] > 0.1:
                            continue 

                        t = c.tracks[ti]
                        elecMin = analysis_tools.minDeltaR(t, c.Electrons)
                        muonMin = analysis_tools.minDeltaR(t, c.Muons)
                        if (elecMin is not None and elecMin < 0.1) or (muonMin is not None and muonMin < 0.1):
                            continue
 
                        minZ, minCanZ = analysis_ntuples.minDeltaRGenParticles(t, genZL, c.GenParticles)
                        minNZ, minCanNZ = analysis_ntuples.minDeltaRGenParticles(t, genNonZL, c.GenParticles)
            
                        min = None
                        if minNZ is None or minZ < minNZ:
                            min = minZ
                        else:
                            min = minNZ
        
                        result = ""
        
                        if min > 0.1:
                            result = "MM"
                        elif minNZ is None or minZ < minNZ:
                            if c.tracks_charge[ti] * c.GenParticles_PdgId[minCanZ] < 0:
                                result = "Zl"
                                #print("Found!")
                            else:
                                result = "MM"
                        else:
                            result = "MM"
                        
                        if result == "Zl" and c.tracks_charge[ti] * ch1 < 0:
                            bh.Fill((t + l1).M(), c.Weight)
                            break
            
    
    cpBlue = utils.colorPalette[2]
    cpRed = utils.colorPalette[7]

    #trainBGHist.SetTitle(name)
    bh.GetXaxis().SetTitle("M_{ll} [GeV]")
    bh.GetYaxis().SetTitle("Number of events")
    bh.GetYaxis().SetTitleOffset(1.15)
    #bh.GetXaxis().SetLabelSize(0.04)
    #bh.GetYaxis().SetTitle("Arbitrary Units")

    fillC = TColor.GetColor(cpRed["fillColor"])
    lineC = TColor.GetColor(cpRed["lineColor"])
    #trainBGHist.SetFillStyle(cpRed["fillStyle"])
    bh.SetFillColorAlpha(fillC, 0.35)#.35)
    bh.SetLineColor(lineC)
    bh.SetLineWidth(1)
    bh.SetOption("HIST")
    bh.SetMaximum(900)
    bh.Draw("HIST")

    legend.AddEntry(bh, "One reco one track", 'F')

    fillC = TColor.GetColor(cpBlue["fillColor"])
    lineC = TColor.GetColor(cpBlue["lineColor"])
    #sh.SetFillStyle(cpBlue["fillStyle"])
    sh.SetFillColorAlpha(fillC, 0.35)#.35)
    sh.SetLineColor(lineC)
    sh.SetLineWidth(1)
    sh.SetOption("HIST")
    sh.Draw("HIST SAME")
    
    legend.AddEntry(sh, "Two reconstructed", 'F')    
    
    legend.Draw("SAME")
    gPad.SetLogy();
    utils.stamp_plot()
    #utils.stampFab("35.9")
    c1.Print(output_file);
    c1.Print(output_file+"]");
    exit(0)

main()



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

gROOT.SetBatch(True)
gStyle.SetOptStat(0)

# SIM_GROUP = {
#             "(.*dm2p.*)|(.*dm3p.*)|(.*dm4p.*)" : "low",
#             ".*dm5p.*" : "dm5",
#             ".*dm7p.*" : "dm7",
#             ".*dm9p.*" : "dm9",
#             "(.*dm12p.*)|(.*dm13p.*)" : "high"
# }

SIM_GROUP = {
            "low":"(.*dm2p.*)|(.*dm3p.*)|(.*dm4p.*)",
            "dm5":".*dm5p.*",
            "dm7":".*dm7p.*",
            "dm9":".*dm9p.*",
            "high":"(.*dm12p.*)|(.*dm13p.*)"
}

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Plot observealbes for tracks.')
parser.add_argument('-i', '--input', nargs=1, help='Input Range', required=False)
parser.add_argument('-o', '--output_file', nargs=1, help='Output Filename', required=True)
args = parser.parse_args()
	

output_file = None
input = "high"
if args.output_file:
    output_file = args.output_file[0]
if args.input:
    input = args.input[0]
######## END OF CMDLINE ARGUMENTS ########

signal_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/lepton_track/single/"

print("Running for input: " + input)

def main():

    print("Plotting observable")

    c1 = TCanvas("c1", "c1", 800, 800)
    c1.SetBottomMargin(0.16)
    c1.SetLeftMargin(0.16)
    #c1 = utils.mkcanvas()
    #memory = []
    c1.Print(output_file+"[");
    
    legend = TLegend(.55,.75,.89,.89)
    legend.SetBorderSize(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.05)
    
    files = glob(signal_dir + "/*")
    signal_files_re = re.compile("(" + SIM_GROUP[input] + ")_sig*")
    bg_files_re = re.compile("(" + SIM_GROUP[input] + ")_bg*")
    
    signal_files = [f for f in files if signal_files_re.match(f)]
    bg_files = [f for f in files if bg_files_re.match(f)]
    
    print(signal_files)
    print(bg_files)
    
    sh = utils.UOFlowTH1F("sh", "", 100, 2, 26)
    bh = utils.UOFlowTH1F("bh", "", 100, 2, 26)
    utils.histoStyler(sh)
    utils.histoStyler(bh)
    
    for (fs, hs) in [(signal_files, sh),(bg_files, bh)]:
        for file in fs:
            print("Processing " + file)
            f = TFile(file)
            c = f.Get('tEvent')
            nentries = c.GetEntries()
            print('Analysing', nentries, "entries")
            for ientry in range(nentries):
                if ientry % 1000 == 0:
                    print("Processing " + str(ientry))
                c.GetEntry(ientry)
                hs.Fill(c.lepton.Pt())
    
    cpBlue = utils.colorPalette[2]
    cpRed = utils.colorPalette[7]

    #trainBGHist.SetTitle(name)
    bh.GetXaxis().SetTitle("Pt(l)")
    bh.GetYaxis().SetTitle("Number of tracks")
    bh.GetYaxis().SetTitleOffset(1.15)
    #bh.GetXaxis().SetLabelSize(0.04)
    #bh.GetYaxis().SetTitle("Arbitrary Units")

    fillC = TColor.GetColor(cpRed["fillColor"])
    lineC = TColor.GetColor(cpRed["lineColor"])
    #trainBGHist.SetFillStyle(cpRed["fillStyle"])
    bh.SetFillColorAlpha(fillC, 0.35)#.35)
    bh.SetLineColor(lineC)
    bh.SetLineWidth(1)
    bh.SetMinimum(0.01)
    bh.SetOption("HIST")
    bh.Draw("HIST")

    legend.AddEntry(bh, "Non-Z tracks", 'F')

    fillC = TColor.GetColor(cpBlue["fillColor"])
    lineC = TColor.GetColor(cpBlue["lineColor"])
    #sh.SetFillStyle(cpBlue["fillStyle"])
    sh.SetFillColorAlpha(fillC, 0.35)#.35)
    sh.SetLineColor(lineC)
    sh.SetLineWidth(1)
    sh.SetOption("HIST")
    sh.Draw("HIST SAME")
    
    legend.AddEntry(sh, "Z tracks", 'F')    
    
    legend.Draw("SAME")
    gPad.SetLogy();
    utils.stamp_plot()
    #utils.stampFab("35.9")
    c1.Print(output_file);
    c1.Print(output_file+"]");
    exit(0)

main()



#!/usr/bin/env python

from ROOT import *
from glob import glob
from sys import exit
import argparse
import sys
import numpy as np
import os
import xml.etree.ElementTree as ET

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes"))

from lib import analysis_ntuples
from lib import analysis_tools
from lib import utils
from lib import cut_optimisation

gROOT.SetBatch(True)
gStyle.SetOptStat(0)

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Create skims for x1x2x1 process with BDTs.')
parser.add_argument('-i', '--input_file', nargs=1, help='Input Filename', required=True)
parser.add_argument('-o', '--output_file', nargs=1, help='Output Filename', required=True)
parser.add_argument('-ub', '--univ_bdt', nargs=1, help='Universal BDT Folder', required=True)

args = parser.parse_args()

input_file = None
if args.input_file:
	input_file = args.input_file[0]
output_file = None
if args.output_file:
	output_file = args.output_file[0]
	
univ_bdt = None
if args.univ_bdt:
	univ_bdt = args.univ_bdt[0]
	
######## END OF CMDLINE ARGUMENTS ########

def main():
    iFile = TFile(input_file)
    c = iFile.Get('tEvent')

    h = TH1F("bdt", "bdt", 40, -1, 1)
    (univ_testBGHists, univ_trainBGHists, univ_testSignalHists, univ_trainSignalHists, univ_methods, univ_names) = cut_optimisation.get_bdt_hists([univ_bdt])
    univ_trainSignalHist, univ_trainBGHist, univ_testSignalHist, univ_testBGHist = univ_trainSignalHists[0], univ_trainBGHists[0], univ_testSignalHists[0], univ_testBGHists[0]
    univ_highestZ, univ_highestS, univ_highestB, univ_highestMVA, univ_ST, univ_BT = cut_optimisation.getHighestZ(univ_trainSignalHist, univ_trainBGHist, univ_testSignalHist, univ_testBGHist)

    univ_bdt_weights = univ_bdt + "/dataset/weights/TMVAClassification_BDT.weights.xml"
    univ_bdt_vars = cut_optimisation.getVariablesFromXMLWeightsFile(univ_bdt_weights)
    univ_bdt_vars_map = cut_optimisation.getVariablesMemMap(univ_bdt_vars)
    univ_bdt_specs = cut_optimisation.getSpecSpectatorFromXMLWeightsFile(univ_bdt_weights)
    univ_bdt_specs_map = cut_optimisation.getSpectatorsMemMap(univ_bdt_specs)
    univ_bdt_reader = cut_optimisation.prepareReader(univ_bdt_weights, univ_bdt_vars, univ_bdt_vars_map, univ_bdt_specs, univ_bdt_specs_map)

    print("univ_highestMVA=" + str(univ_highestMVA))

    nentries = c.GetEntries()
    print('Analysing', nentries, "entries")

    total = 0
    passed = 0

    for ientry in range(nentries):
        if ientry % 1000 == 0:
            print("Processing " + str(ientry))
        total += 1
        c.GetEntry(ientry)
        for k, v in univ_bdt_vars_map.items():
            v[0] = eval("c." + k)
        for k, v in univ_bdt_specs_map.items():
            v[0] = eval("c." + k)
        value = univ_bdt_reader.EvaluateMVA("BDT")
        h.Fill(value)
        if value >= univ_highestMVA:
            passed += 1

    print("total=" + str(total))
    print("passed=" + str(passed))

    # Create canvas
    canvas = TCanvas("roc", "roc", 520, 10, 1000, 1000)
    canvas.SetTopMargin(0.5 * canvas.GetTopMargin())
    canvas.SetBottomMargin(1 * canvas.GetBottomMargin())
    canvas.SetLeftMargin(1 * canvas.GetLeftMargin())
    canvas.SetRightMargin(0.5 * canvas.GetRightMargin())

    h.Draw('h')

    canvas.Update()
    canvas.SaveAs(output_file)
	

main()
#!/usr/bin/env python

from ROOT import *
from glob import glob
from sys import exit
import argparse
import sys
import numpy as np
import os

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes"))
from lib import analysis_ntuples
from lib import analysis_tools
from lib import utils
from lib import analysis_observables

gSystem.Load('LumiSectMap_C')
from ROOT import LumiSectMap

gSystem.Load('LeptonCollectionMap_C')
from ROOT import LeptonCollectionMap
from ROOT import LeptonCollectionFilesMap
from ROOT import LeptonCollection

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Create skims for x1x2x1 process.')
parser.add_argument('-i', '--input_file', nargs=1, help='Input Filename', required=True)
parser.add_argument('-o', '--output_file', nargs=1, help='Output Filename', required=True)

args, unknown = parser.parse_known_args()

print(args)


input_file = None
if args.input_file:
    input_file = args.input_file[0].strip()
output_file = None
if args.output_file:
    output_file = args.output_file[0].strip()

def main():
    print("Skimming", input_file, "into", output_file)
    file = TFile(input_file, "read")
    full_tree = file.Get("tEvent")
    nentries = full_tree.GetEntries()
    print("There are", nentries, "in the full tree")
    
    selection_or = []
    
    for iso in utils.leptonIsolationList:
        for cat in utils.leptonIsolationCategories:
            ptRanges = [""]
            if iso == "CorrJetIso":
                ptRanges = utils.leptonCorrJetIsoPtRange
            for ptRange in ptRanges:
                postfixi = [iso + str(ptRange) + cat]
                if iso + str(ptRange) + cat == utils.defaultJetIsoSetting:
                    postfixi = [iso + str(ptRange) + cat, ""]
                for postfix in postfixi:
                    selection_or.append("twoLeptons" + postfix + " == 1")
                    
    selection_string = " || ".join(selection_or)
    print("selection_string=" + selection_string)
    
    new_file = TFile(output_file, "recreate")
    
    new_tree = full_tree.CopyTree(selection_string)
    print("new_tree has", new_tree.GetEntries(), "entries")
    
    new_file.cd()
    new_tree.Write()
    
    hHt = file.Get("hHt")
    new_file.cd()
    hHt.Write()
    
    if file.GetListOfKeys().Contains("lumiSecs"):
        lumiSecs = file.Get("lumiSecs")
        new_file.cd()
        lumiSecs.Write("lumiSecs")

    new_file.Close()
    file.Close()
    
    exit(0)
    
main()
exit(0)
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

gSystem.Load('LeptonCollectionMap_C')
from ROOT import LeptonCollectionMap
from ROOT import LeptonCollection

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Create skims for x1x2x1 process.')
parser.add_argument('-i', '--input_file', nargs=1, help='Input Filename', required=False)
parser.add_argument('-o', '--output_file', nargs=1, help='Output Filename', required=False)
args = parser.parse_args()

print(args)

input_file = None
if args.input_file:
    input_file = args.input_file[0].strip()
output_file = None
if args.output_file:
    output_file = args.output_file[0].strip()
######## END OF CMDLINE ARGUMENTS ########

def main():
    c = TChain('TreeMaker2/PreSelection')
    c.Add(input_file)

    print("Creating " + output_file)
    fnew = TFile(output_file,'recreate')
    
    leptonCollectionMap = LeptonCollectionMap()

    nentries = c.GetEntries()
    print('Analysing', nentries, "entries")

    for ientry in range(nentries):
        if ientry % 1000 == 0:
            print("Processing " + str(ientry))
        c.GetEntry(ientry)
        leptonCollection = LeptonCollection()
        leptonCollection.Electrons = c.Electrons
        leptonCollection.Electrons_charge = c.Electrons_charge
        leptonCollection.Electrons_EnergyCorr = c.Electrons_EnergyCorr
        leptonCollection.Electrons_mediumID = c.Electrons_mediumID
        leptonCollection.Electrons_MiniIso = c.Electrons_MiniIso
        leptonCollection.Electrons_MT2Activity = c.Electrons_MT2Activity
        leptonCollection.Electrons_MTW = c.Electrons_MTW
        leptonCollection.Electrons_passIso = c.Electrons_passIso
        leptonCollection.Electrons_tightID = c.Electrons_tightID
        leptonCollection.Electrons_TrkEnergyCorr = c.Electrons_TrkEnergyCorr
        leptonCollection.Muons = c.Muons
        leptonCollection.Muons_charge = c.Muons_charge
        leptonCollection.Muons_mediumID = c.Muons_mediumID
        leptonCollection.Muons_MiniIso = c.Muons_MiniIso
        leptonCollection.Muons_MT2Activity = c.Muons_MT2Activity
        leptonCollection.Muons_MTW = c.Muons_MTW
        leptonCollection.Muons_passIso = c.Muons_passIso
        leptonCollection.Muons_tightID = c.Muons_tightID
        
        leptonCollectionMap.insert(c.RunNum, c.LumiBlockNum, c.EvtNum, leptonCollection)

    fnew.cd()
    leptonCollectionMap.Write("leptonCollectionMap")
    fnew.Close()

main()

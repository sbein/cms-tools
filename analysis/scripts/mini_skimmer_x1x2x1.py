#!/usr/bin/env python

from ROOT import *
from glob import glob
from sys import exit
import argparse
import sys
import numpy as np
import os
import xml.etree.ElementTree as ET
from math import *

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes"))
from lib import analysis_ntuples
from lib import analysis_tools
from lib import utils
from lib import cut_optimisation

gROOT.SetBatch(True)
gStyle.SetOptStat(0)

gSystem.Load('LumiSectMap_C')
from ROOT import LumiSectMap

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Create skims for x1x2x1 process with BDTs.')
parser.add_argument('-i', '--input_file', nargs=1, help='Input Filename', required=True)
parser.add_argument('-o', '--output_file', nargs=1, help='Output Filename', required=False)
parser.add_argument('-sc', '--same_charge', dest='sc', help='Same Charge', action='store_true')
parser.add_argument('-dy', '--dy', dest='dy', help='Drell-Yan', action='store_true')
parser.add_argument('-sam', '--sam', dest='sam', help='Sam Samples', action='store_true')
parser.add_argument('-s', '--signal', dest='signal', help='Signal', action='store_true')
parser.add_argument('-bg', '--background', dest='bg', help='Background', action='store_true')
parser.add_argument('-skim', '--skim', dest='skim', help='Skim', action='store_true')
parser.add_argument('-data', '--data', dest='data', help='Data', action='store_true')
parser.add_argument('-mini', '--mini', dest='mini', help='Mini', action='store_true')
args = parser.parse_args()


signal = args.signal
bg = args.bg
sc = args.sc

print("SAME CHARGE=", sc)

input_file = None
if args.input_file:
    input_file = args.input_file[0].strip()

if args.output_file:
    output_file = args.output_file[0].strip()
    output_file.strip()

if (bg and signal) or not (bg or signal):
    signal = True
    bg = False


print("output file: |" + output_file + "|")

######## END OF CMDLINE ARGUMENTS ########

def main():
    
    #file = TFile(input_file, "read")
    
    c = TChain('TreeMaker2/PreSelection')
    print("Opening", input_file)
    c.Add(input_file)
    
    #c = file.Get("tEvent")
    nentries = c.GetEntries()
    
    fullInvMass = utils.UOFlowTH1F("fullInvMass", "fullInvMass", 60, 2.5, 3.5)
    singleMuonSingleTrackInvMass = utils.UOFlowTH1F("singleMuonSingleTrackInvMass", "singleMuonSingleTrackInvMass", 60, 2.5, 3.5)
    singleMuonsManyTrackInvMass = utils.UOFlowTH1F("singleMuonsManyTrackInvMass", "singleMuonsManyTrackInvMass", 60, 2.5, 3.5)
    manyMuonsSingleTrackInvMass = utils.UOFlowTH1F("manyMuonsSingleTrackInvMass", "manyMuonsSingleTrackInvMass", 60, 2.5, 3.5)
    
    for ientry in range(nentries):
        if ientry % 100 == 0:
            print("Processing " + str(ientry) + " out of " + str(nentries))
        c.GetEntry(ientry)
        
        # var_MinDeltaPhiMetJets = analysis_ntuples.eventMinDeltaPhiMetJets25Pt2_4Eta(c.Jets, c.MET, c.METPhi)
#         var_MinDeltaPhiMhtJets = analysis_ntuples.eventMinDeltaPhiMhtJets25Pt2_4Eta(c.Jets, c.MHT, c.MHTPhi)
#         if var_MinDeltaPhiMetJets[0] < 0.4: continue
#         if c.MHT < 100: continue
#         if c.MET < 120: continue
        
        noIsoVec = ROOT.std.vector(bool)()
        for i in range(len(c.Muons)):
            noIsoVec.push_back(1)
        
        
        if c.Muons.size() < 2:
            continue
        
        if not analysis_ntuples.hasHighPtJpsiMuon(24, c.Muons, c.Muons_passIso, c.Muons_tightID):
            continue
        
        #print("After")
        
        highPtLepton = c.Muons[0]
        
        foundMuon = False
        foundTrack = False
        inFirstMuonIteration = True
        
        for i in range(len(c.Muons)):
            if i == 0:
                continue
            
            inFirstTrackIterationForMuon = True
            
            if not analysis_ntuples.isleptonPassesJpsiSelection(i, 24, c.Muons, noIsoVec, c.Muons_mediumID, 2, False, c.Muons_tightID):
                continue
            
            for j in range(len(c.tracks)):
                if c.tracks[j].Pt() > 24:
                    continue
                if c.Muons_charge[i] * c.tracks_charge[j] > 0:
                    continue
                if (c.Muons[i] + c.tracks[j]).M() < 2.5 or (c.Muons[i] + c.tracks[j]).M() > 3.5:
                    continue
                
                fullInvMass.Fill((c.Muons[i] + c.tracks[j]).M())
                
                if not foundMuon and not foundTrack:
                    singleMuonSingleTrackInvMass.Fill((c.Muons[i] + c.tracks[j]).M())
                
                foundMuon = True
                foundTrack = True
                
                if inFirstMuonIteration:
                    singleMuonsManyTrackInvMass.Fill((c.Muons[i] + c.tracks[j]).M())
                
                if inFirstTrackIterationForMuon:
                    inFirstTrackIterationForMuon = False
                    manyMuonsSingleTrackInvMass.Fill((c.Muons[i] + c.tracks[j]).M())
                
            if foundMuon:
                inFirstMuonIteration = False
    
    print("Creating file", output_file)
    
    fnew = TFile(output_file,'recreate')
    
    fullInvMass.Write()
    singleMuonSingleTrackInvMass.Write()
    singleMuonsManyTrackInvMass.Write()
    manyMuonsSingleTrackInvMass.Write()
    
    fnew.Close()
    


main()
exit(0)
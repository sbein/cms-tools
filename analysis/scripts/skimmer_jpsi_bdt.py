#!/usr/bin/env python

from ROOT import *
from glob import glob
from sys import exit
import argparse
import sys
import numpy as np
import os
import xml.etree.ElementTree as ET

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
parser.add_argument('-bdt', '--bdt', nargs=1, help='Dilepton BDT Folder', required=True)

parser.add_argument('-s', '--signal', dest='signal', help='Signal', action='store_true')
parser.add_argument('-bg', '--background', dest='bg', help='Background', action='store_true')
parser.add_argument('-data', '--data', dest='data', help='Data', action='store_true')
parser.add_argument('-dy', '--dy', dest='dy', help='Drell-Yan', action='store_true')
parser.add_argument('-sc', '--same_charge', dest='sc', help='Same Charge', action='store_true')
parser.add_argument('-sam', '--sam', dest='sam', help='Sam Samples', action='store_true')
parser.add_argument('-jpsi_muons', '--jpsi_muons', dest='jpsi_muons', help='JPSI Muons Skim', action='store_true')
args = parser.parse_args()

print(args)

signal = args.signal
bg = args.bg

input_file = None
if args.input_file:
    input_file = args.input_file[0].strip()

if (bg and signal) or not (bg or signal):
    signal = True
    bg = False

bdt = None
if args.bdt:
    bdt = args.bdt[0]
    
data = args.data

jpsi_muons = args.jpsi_muons

if jpsi_muons or jpsi_electrons:
    jpsi = True
    print("Got JPSI")
    if jpsi_muons:
        print("MUONS")
    else:
        print("ELECTRONS")

######## END OF CMDLINE ARGUMENTS ########

vars = {}
bdt_vars_maps = {}
bdt_specs_maps = {}
bdt_readers = {}
branches = {}

def main():
    
    if jpsi:
        utils.defaultJetIsoSetting = "NoIso"
    
    iFile = TFile(input_file, "update")
    #hHt = iFile.Get('hHt')
    tree = iFile.Get('tEvent')
    nentries = tree.GetEntries()
    
    # CREATE VARS, BRANCHES, AND BDT READERS
    vars["BDT"] = ROOT.std.vector(double)()
    vars["BtagsDeepMedium"] = np.zeros(1,dtype=int)
    
    if tree.GetBranchStatus("BDT"):
        print("Reseting branch", "BDT")
        branches["BDT"] = tree.GetBranch("BDT")
        branches["BDT"].Reset()
        tree.SetBranchAddress("BDT", vars["BDT"])
    else:
        print("Branching", "BDT")
        branches["BDT"] = tree.Branch("BDT", 'std::vector<double>', vars["BDT"])
        tree.SetBranchAddress("BDT", vars["BDT"])
        
    if tree.GetBranchStatus("BtagsDeepMedium"):
        branch = tree.GetBranch("BtagsDeepMedium")
        branch.Reset()
        branch.SetAddress(vars["BtagsDeepMedium"])
    else:
        branches["BtagsDeepMedium"] = tree.Branch("BtagsDeepMedium",vars["BtagsDeepMedium"],"BtagsDeepMedium/I");
        
    
    bdt_weights = bdt + "/dataset/weights/TMVAClassification_BDT.weights.xml"
    bdt_vars = cut_optimisation.getVariablesFromXMLWeightsFile(bdt_weights)
    print("bdt_vars", bdt_vars)
    bdt_vars_map = cut_optimisation.getVariablesMemMap(bdt_vars)
    print("bdt_vars_map", bdt_vars_map)
    bdt_specs = cut_optimisation.getSpecSpectatorFromXMLWeightsFile(bdt_weights)
    print("bdt_specs", bdt_specs)
    bdt_specs_map = cut_optimisation.getSpectatorsMemMap(bdt_specs)
    print("bdt_specs_map", bdt_specs_map)
    bdt_reader = cut_optimisation.prepareReader(bdt_weights, bdt_vars, bdt_vars_map, bdt_specs, bdt_specs_map)

    bdt_vars_maps["BDT"] = bdt_vars_map
    bdt_specs_maps["BDT"] = bdt_specs_map
    bdt_readers["BDT"] = bdt_reader

    print('Analysing', nentries, "entries")
    
    iFile.cd()

    for ientry in range(nentries):
        if ientry % 1000 == 0:
            print("Processing " + str(ientry) + " out of " + str(nentries))
        tree.GetEntry(ientry)
        
        c = tree
        
        vars["BDT"] = ROOT.std.vector(double)()
        
        nj, btagsDeepMedium, ljet = analysis_ntuples.eventNumberOfJets25Pt2_4Eta_DeepMedium(c.Jets, c.Jets_bJetTagDeepCSVBvsAll)
        if nj is None or btagsDeepMedium is None:
            btagsDeepMedium = 0
        vars["BtagsDeepMedium"][0] = btagsDeepMedium
        
        
        for i in range(c.invMass.size()):
                
            tagMuonIdx = c.tagMuon[i]
            probeTrackIdx = c.probeTrack[i]
            
            tagMuon = c.Muons[tagMuonIdx]
            probeTrack = c.tracks[probeTrackIdx]
            
            if not (probeTrack.Pt() < 3 and abs(probeTrack.Eta()) >= 1.2 and abs(probeTrack.Eta()) <= 2.4):
                vars["BDT"].push_back(1)
            else:
                for k, v in bdt_vars_maps["BDT"].items():
                    #print("********")
                    if analysis_ntuples.commonFlatObs.get(k) is not None:
                        v[0] = eval("tree." + k)
                    elif analysis_ntuples.muonsObs.get(k) is not None:
                        if analysis_ntuples.muonsObs.get(k) == "bool":
                            v[0] = bool(eval("tree." + k)[tagMuonIdx])
                        else:
                            #print("eval(tree." + k + ")", eval("tree." + k + "[" + str(tagMuonIdx) + "]"), tagMuonIdx)
                            v[0] = eval("tree." + k)[tagMuonIdx]
                    elif utils.commonObservablesDTypesList.get(k) is not None:
                        v[0] = eval("tree." + k)[i]
                    elif "tagMuon" in k:
                        #print("eval(" + k + ")", eval(k))
                        v[0]  = eval(k)
                    else:
                        print("WTF", k)
                        exit(1)
                bdt_score = bdt_readers["BDT"].EvaluateMVA("BDT")
                #print(bdt_specs_maps["BDT"])
                #print("bdt_score", bdt_score)
                vars["BDT"].push_back(bdt_score)
            
        tree.SetBranchAddress("BDT", vars["BDT"])
        branches["BDT"].Fill()
        branches["BtagsDeepMedium"].Fill()
       
    tree.Write("tEvent",TObject.kOverwrite)
        
    print("DONE SKIMMING")
    iFile.Close()

main()
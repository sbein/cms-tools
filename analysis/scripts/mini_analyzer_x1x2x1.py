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
parser.add_argument('-tb', '--track_bdt', nargs=1, help='Track BDT Folder', required=True)

parser.add_argument('-s', '--signal', dest='signal', help='Signal', action='store_true')
parser.add_argument('-bg', '--background', dest='bg', help='Background', action='store_true')
parser.add_argument('-sc', '--same_charge', dest='sc', help='Same Charge', action='store_true')
parser.add_argument('-dy', '--dy', dest='dy', help='Drell-Yan', action='store_true')
parser.add_argument('-sam', '--sam', dest='sam', help='Sam Samples', action='store_true')
args = parser.parse_args()


signal = args.signal
bg = args.bg
sc = args.sc

print("SAME CHARGE=", sc)

input_file = None
if args.input_file:
    input_file = args.input_file[0].strip()

if (bg and signal) or not (bg or signal):
    signal = True
    bg = False

track_bdt = None
if args.track_bdt:
    track_bdt = args.track_bdt[0]

######## END OF CMDLINE ARGUMENTS ########

def main():
    
    file = TFile(input_file, "update")
    
    c = file.Get("tEvent")
    nentries = c.GetEntriesFast()
    
    for ientry in range(nentries):
        if ientry % 100 == 0:
            print("Processing " + str(ientry) + " out of " + str(nentries))
        c.GetEntry(ientry)
        
        var_MinDeltaPhiMetJets = analysis_ntuples.eventMinDeltaPhiMetJets25Pt2_4Eta(c.Jets, c.MET, c.METPhi)
        var_MinDeltaPhiMhtJets = analysis_ntuples.eventMinDeltaPhiMhtJets25Pt2_4Eta(c.Jets, c.MHT, c.MHTPhi)
        if var_MinDeltaPhiMetJets[0] < 0.4: continue
        if c.MHT < 100: continue
        if c.MET < 120: continue
        
        nj, btagsDeepMedium, ljet = analysis_ntuples.eventNumberOfJets25Pt2_4Eta_DeepMedium(c.Jets, c.Jets_bJetTagDeepCSVBvsAll)
        
        var_LeadingJet = c.Jets[ljet]
        
        electronsCalcObs = {}
        muonsCalcObs = {}
        
        for i in range(c.Electrons.size()):
            electronsCalcObs["Electrons_deltaRLJ"].push_back(c.Electrons[i].DeltaR(var_LeadingJet))
            
        for i in range(c.Muons.size()):
            muonsCalcObs["Muons_deltaRLJ"].push_back(c.Muons[i].DeltaR(var_LeadingJet))
        
        var_Jets_muonCorrected = ROOT.std.vector(TLorentzVector)(var_Jets)
        var_Jets_electronCorrected = ROOT.std.vector(TLorentzVector)(var_Jets)
        
        non_iso_jet_electrons = [ i for i in range(c.Electrons.size())) if analysis_ntuples.electronPassesKinematicSelection(i, c.Electrons, electronsCalcObs["Electrons_deltaRLJ"]) and electronsCalcObs["Electrons_minDeltaRJets"][i] >= 0 and electronsCalcObs["Electrons_minDeltaRJets"][i] < 0.4 ]
        non_iso_jet_muons = [ i for i in range(c.Muons.size())) if analysis_ntuples.muonPassesLooseSelection(i, muonsObs["Muons"], muonsObs["Muons_mediumID"], muonsCalcObs["Muons_deltaRLJ"])and muonsCalcObs["Muons_minDeltaRJets"][i] >= 0 and muonsCalcObs["Muons_minDeltaRJets"][i] < 0.4 ]
        
        for i in non_iso_jet_electrons:
            for j in range(len(var_Jets_electronCorrected)):
                if var_Jets_electronCorrected[j].DeltaR(electronsObs["Electrons"][i]) < 0.4:
                    var_Jets_electronCorrected[j] -= electronsObs["Electrons"][i]
        for i in non_iso_jet_muons:
            for j in range(len(var_Jets_muonCorrected)):
                if var_Jets_muonCorrected[j].DeltaR(muonsObs["Muons"][i]) < 0.4:
                    var_Jets_muonCorrected[j] -= muonsObs["Muons"][i]
        
        isoJets = {"electron" : {"obs" : "Electrons"}, "muon" : {"obs" : "Muons"}}
        
        for lep in isoJets:
            
            leptonsVecName = isoJets[lep]["obs"]
            leptonsVec = eval("c." + leptonsVecName)
            
            for i in range(leptonsVec.size()):
                min, minCan = analysis_ntuples.minDeltaLepLeps(leptonsVec[i], eval("var_Jets_" + lep + "Corrected"))
                if min is None:
                    eval(leptonsVecName.lower() + "CalcObs")[leptonsVecName  +  "_correctedMinDeltaRJets"].push_back(-1)
                    eval(leptonsVecName.lower() + "CalcObs")[leptonsVecName  +  "_correctedClosestJet"].push_back(-1)
                    for ptRange in utils.leptonCorrJetIsoPtRange:
                        leptonsCorrJetVars[isoJets[lep]["obs"] + "_passCorrJetIso" + str(ptRange)].push_back(True)
                else:
                    eval(leptonsVecName.lower() + "CalcObs")[leptonsVecName  +  "_correctedMinDeltaRJets"].push_back(min)
                    eval(leptonsVecName.lower() + "CalcObs")[leptonsVecName  +  "_correctedClosestJet"].push_back(minCan)
                    
                    for ptRange in utils.leptonCorrJetIsoPtRange:
    
                        min, minCan = analysis_ntuples.minDeltaLepLeps(leptonsVec[i], isoJets[lep][str(ptRange)])
                        if min is None or min > 0.4:
                            leptonsCorrJetVars[isoJets[lep]["obs"] + "_passCorrJetIso" + str(ptRange)].push_back(True)
                        else:
                            leptonsCorrJetVars[isoJets[lep]["obs"] + "_passCorrJetIso" + str(ptRange)].push_back(False)
         
        
        leptons, leptonsIdx, leptonsCharge, leptonFlavour, same_sign = analysis_ntuples.getTwoLeptonsAfterSelection(c.Electrons, leptonsCorrJetVars["Electrons_pass" + iso + str(ptRange)], electronsCalcObs["Electrons_deltaRLJ"], electronsObs["Electrons_charge"], muonsObs["Muons"], leptonsCorrJetVars["Muons_pass" + iso + str(ptRange)], muonsObs["Muons_mediumID"], muonsCalcObs["Muons_deltaRLJ"], muonsObs["Muons_charge"], utils.leptonIsolationCategories[cat]["muonPt"], utils.leptonIsolationCategories[cat]["lowPtTightMuons"], muonsObs["Muons_tightID"])

main()
exit(0)
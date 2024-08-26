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
args = parser.parse_args()


input_file = None
if args.input_file:
    input_file = args.input_file[0].strip()

######## END OF CMDLINE ARGUMENTS ########

branches = {}

def main():
    
    file = TFile(input_file, "update")
    
    tEvent = file.Get("tEvent")
    nentries = tEvent.GetEntries()
    
    electronsCalcObs = {}
    for electronsCalcOb in analysis_ntuples.electronsCalcObs:
        electronsCalcObs[electronsCalcOb] = ROOT.std.vector(eval(analysis_ntuples.electronsCalcObs[electronsCalcOb]))()
    
    muonsCalcObs = {}
    for muonsCalcOb in analysis_ntuples.muonsCalcObs:
        muonsCalcObs[muonsCalcOb] = ROOT.std.vector(eval(analysis_ntuples.muonsCalcObs[muonsCalcOb]))()
        
    leptonsCorrJetVars = {}
    
    for lep in ["Muons", "Electrons"]:
        for CorrJetObs in utils.leptonIsolationList:
            ptRanges = [""]
            if CorrJetObs == "CorrJetIso":
                ptRanges = utils.leptonCorrJetIsoPtRange
            for ptRange in ptRanges:
                leptonsCorrJetVars[lep + "_pass" + CorrJetObs + str(ptRange)] = ROOT.std.vector(eval(utils.leptonsCorrJetVecList[CorrJetObs]))()
    
    for lep in ["Muons", "Electrons"]:
        for CorrJetObs in utils.leptonIsolationList:
            ptRanges = [""]
            if CorrJetObs == "CorrJetIso":
                 ptRanges = utils.leptonCorrJetIsoPtRange
            for ptRange in ptRanges:
                branchName = lep + "_pass" +  CorrJetObs + str(ptRange)
                if tEvent.GetBranchStatus(branchName):
                    print("Reseting branch", branchName)
                    branches[branchName] = tEvent.GetBranch(branchName)
                    branches[branchName].Reset()
                    tEvent.SetBranchAddress(branchName, leptonsCorrJetVars[branchName])
                    #branches[DTypeObs + postfix].SetAddress(exTrackVars[DTypeObs + postfix])
                else:
                    print("Branching", branchName)
                    branches[branchName] = tEvent.Branch(branchName, 'std::vector<' + utils.leptonsCorrJetVecList[CorrJetObs] + '>', leptonsCorrJetVars[branchName])
                    tEvent.SetBranchAddress(branchName, leptonsCorrJetVars[branchName])
    
    for ientry in range(nentries):
        if ientry % 100 == 0:
            print("Processing " + str(ientry) + " out of " + str(nentries))
        tEvent.GetEntry(ientry)
        
        ### JET ISOLATION ####
        
        for muonsCalcOb in analysis_ntuples.muonsCalcObs:
            muonsCalcObs[muonsCalcOb] = ROOT.std.vector(eval(analysis_ntuples.muonsCalcObs[muonsCalcOb]))()
        
        electronsCalcObs = {}
        for electronsCalcOb in analysis_ntuples.electronsCalcObs:
            electronsCalcObs[electronsCalcOb] = ROOT.std.vector(eval(analysis_ntuples.electronsCalcObs[electronsCalcOb]))()
            
        for i in range(tEvent.Muons.size()):
            muonsCalcObs["Muons_deltaRLJ"].push_back(-1)
        for i in range(tEvent.Electrons.size()):
            electronsCalcObs["Electrons_deltaRLJ"].push_back(-1)
        
        for lep in ["Muons", "Electrons"]:
            for CorrJetObs in utils.leptonIsolationList:
                if CorrJetObs == "CorrJetIso":
                    for ptRange in utils.leptonCorrJetIsoPtRange:
                        leptonsCorrJetVars[lep + "_pass" + CorrJetObs + str(ptRange)] = ROOT.std.vector(eval(utils.leptonsCorrJetVecList[CorrJetObs]))()
                else:
                    leptonsCorrJetVars[lep + "_pass" + CorrJetObs] = ROOT.std.vector(eval(utils.leptonsCorrJetVecList[CorrJetObs]))()
        
        isoJets = {"electron" : {"obs" : "Electrons"}, "muon" : {"obs" : "Muons"}}
        for lepIso in utils.leptonIsolationList:
            for lep in isoJets:
                if lepIso == "CorrJetIso":
                    continue
                elif lepIso == "NonJetIso":
                    isoJets[lep][lepIso] = [ tEvent.Jets[j] for j in range(len(tEvent.Jets)) if tEvent.Jets[j].Pt() > 25 ]
        
        for lep in isoJets:

            leptonsVecName = isoJets[lep]["obs"]
            #print(leptonsVecName)
            leptonsVec = eval("tEvent." + leptonsVecName)
            
            for i in range(leptonsVec.size()):
                leptonsCorrJetVars[isoJets[lep]["obs"] + "_passNoIso"].push_back(True)
                min, minCan = analysis_ntuples.minDeltaLepLeps(leptonsVec[i], tEvent.Jets)
                if min is None:
                    eval(leptonsVecName.lower() + "CalcObs")[leptonsVecName  + "_minDeltaRJets"].push_back(-1)
                    eval(leptonsVecName.lower() + "CalcObs")[leptonsVecName  + "_closestJet"].push_back(-1)
                    #leptonsCorrJetVars[isoJets[lep]["obs"] + "_passJetIso"].push_back(True)
                    #leptonsCorrJetVars[isoJets[lep]["obs"] + "_passNonJetIso"].push_back(True)
                else:
                    eval(leptonsVecName.lower() + "CalcObs")[leptonsVecName  + "_minDeltaRJets"].push_back(min)
                    eval(leptonsVecName.lower() + "CalcObs")[leptonsVecName  + "_closestJet"].push_back(minCan)
        
                    # min, minCan = analysis_ntuples.minDeltaLepLeps(leptonsVec[i], isoJets[lep]["JetIso"])
#                     if min is None or min > 0.4:
#                         leptonsCorrJetVars[isoJets[lep]["obs"] + "_passJetIso"].push_back(True)
#                     else:
#                         leptonsCorrJetVars[isoJets[lep]["obs"] + "_passJetIso"].push_back(False)
                    #min, minCan = analysis_ntuples.minDeltaLepLeps(leptonsVec[i], tEvent.Jets)
                    #if min is None or min > 0.4:
                    #    leptonsCorrJetVars[isoJets[lep]["obs"] + "_passNonJetIso"].push_back(True)
                    #else:
                    #    leptonsCorrJetVars[isoJets[lep]["obs"] + "_passNonJetIso"].push_back(False)
        
        var_Jets_muonCorrected = ROOT.std.vector(TLorentzVector)(tEvent.Jets)
        var_Jets_electronCorrected = ROOT.std.vector(TLorentzVector)(tEvent.Jets)
        #print(len(tEvent.Muons), tEvent.Muons.size())
        
        non_iso_jet_electrons = [ i for i in range(len(tEvent.Electrons)) if electronsCalcObs["Electrons_minDeltaRJets"][i] >= 0 and electronsCalcObs["Electrons_minDeltaRJets"][i] < 0.4 ]
        non_iso_jet_muons = [ i for i in range(len(tEvent.Muons)) if analysis_ntuples.muonPassesJetIsoSelection(i, tEvent.Muons, tEvent.Muons_mediumID) and muonsCalcObs["Muons_minDeltaRJets"][i] >= 0 and muonsCalcObs["Muons_minDeltaRJets"][i] < 0.4 ]
        
        #non_iso_jet_electrons = [ i for i in range(len(electronsObs["Electrons"])) if electronsCalcObs["Electrons_minDeltaRJets"][i] >= 0 and electronsCalcObs["Electrons_minDeltaRJets"][i] < 0.4 ]
        #non_iso_jet_muons = [ i for i in range(len(muonsObs["Muons"])) if analysis_ntuples.muonPassesJetIsoSelection(i, muonsObs["Muons"], muonsObs["Muons_mediumID"]) and muonsCalcObs["Muons_minDeltaRJets"][i] >= 0 and muonsCalcObs["Muons_minDeltaRJets"][i] < 0.4 ]
        #non_iso_jet_tracks = [ i for i in range(len(c.tracks)) if abs(c.tracks[i].Eta()) < 2.4 and c.tracks_trkRelIso[i] < 0.1 and c.tracks_dxyVtx[i] < 0.02 and c.tracks_dzVtx[i] < 0.05 and tracksCalcObs["tracks_minDeltaRJets"][i] >= 0 and tracksCalcObs["tracks_minDeltaRJets"][i] < 0.4]
        
        for i in non_iso_jet_electrons:
            for j in range(len(var_Jets_electronCorrected)):
                if var_Jets_electronCorrected[j].DeltaR(tEvent.Electrons[i]) < 0.4:
                    var_Jets_electronCorrected[j] -= tEvent.Electrons[i]
        for i in non_iso_jet_muons:
            for j in range(len(var_Jets_muonCorrected)):
                if var_Jets_muonCorrected[j].DeltaR(tEvent.Muons[i]) < 0.4:
                    var_Jets_muonCorrected[j] -= tEvent.Muons[i]
        
        for lepIso in utils.leptonIsolationList:
            for lep in isoJets:
                if lepIso != "CorrJetIso":
                    continue
                for ptRange in utils.leptonCorrJetIsoPtRange:
                    isoJets[lep][str(ptRange)] = [eval("var_Jets_" + lep + "Corrected")[j] for j in range(len(eval("var_Jets_" + lep + "Corrected"))) if tEvent.Jets_multiplicity[j] >=10 or (eval("var_Jets_" + lep + "Corrected")[j].E() > 0 and eval("var_Jets_" + lep + "Corrected")[j].Pt() > ptRange)]
          
        for lep in isoJets:
             
            leptonsVecName = isoJets[lep]["obs"]
            leptonsVec = eval("tEvent." + leptonsVecName)
            
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
      
        
        for lep in ["Muons", "Electrons"]:
            for CorrJetObs in utils.leptonIsolationList:
                if CorrJetObs == "CorrJetIso":
                    for ptRange in utils.leptonCorrJetIsoPtRange:
                        tEvent.SetBranchAddress(lep + "_pass" + CorrJetObs + str(ptRange), leptonsCorrJetVars[lep + "_pass" + CorrJetObs + str(ptRange)])
                else:
                    #print(lep + "_pass" + CorrJetObs, leptonsCorrJetVars[lep + "_pass" + CorrJetObs])
                    tEvent.SetBranchAddress(lep + "_pass" + CorrJetObs, leptonsCorrJetVars[lep + "_pass" + CorrJetObs])
        
        #### END OF JET ISOLATION
        
        tEvent.Fill()
    
    tEvent.Write("tEvent",TObject.kOverwrite)
    
    file.Close()

main()
exit(0)
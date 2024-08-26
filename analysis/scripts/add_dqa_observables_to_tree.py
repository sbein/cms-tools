#!/usr/bin/env python3

from ROOT import *
from glob import glob
from sys import exit
import numpy as np
import argparse
import sys
import os

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes"))
from lib import analysis_ntuples
from lib import analysis_tools
from lib import utils
from lib import analysis_observables

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Weight skims for x1x2x1 process.')
parser.add_argument('-i', '--input_file', nargs=1, help='Input File', required=True)
parser.add_argument('-f', '--force', dest='force', help='Force Update', action='store_true')
#parser.add_argument('-data', '--data', dest='data', help='data', action='store_true')
#parser.add_argument('-sam', '--sam', dest='sam', help='Sam Samples', action='store_true')
args = parser.parse_args()

input_file = args.input_file[0]
force = args.force

force = True
######## END OF CMDLINE ARGUMENTS ########


#### FIX WRONG BTAGS COUNTING ###

# check if data:
phase = 0
data_period = ""
is_signal = False
is_data = False
is_fastsim = False

for label in ["Run2016", "Run2017", "Run2018", "Summer16", "Fall17", "Autumn18", "RunIISummer16MiniAODv3"]:
    if label in input_file:
        data_period = label
        if "Run201" in label:
            is_data = True
        if label == "Run2016" or label == "Summer16" or label == "RunIISummer16MiniAODv3":
            phase = 0
        elif label == "Run2017" or label == "Run2018" or label == "Fall17" or label == "Autumn18":
            phase = 1
     
if data_period == "RunIISummer16MiniAODv3":
    data_period = "Summer16"
    
print("Signal: %s, phase: %s" % (is_signal, phase))

blockhem = False
partiallyblockhem = False
if "Run2018B" in input_file:
    partiallyblockhem = True
if "Run2018C" in input_file or "Run2018D" in input_file:
    blockhem = True

if data_period != "":
    print("data_period: %s, phase: %s" % (data_period, phase))
else:
    print("Can't determine data/MC era!")
    if "/bg/skim/" in input_file:
        data_period = "Summer16"
        phase = 0
    else:
        data_period = "Fall17"
        phase = 1

if "/signal/" in input_file:
    is_fastsim = True
    if "/skim/" in input_file:
        data_period = "Summer16"
        phase = 0
    elif "/skim_phase1_2018/":
        data_period = "Run2018"
        phase = 1
        

print("is_fastsim", is_fastsim, "data_period", data_period, "phase", phase)

# adjust some variables:
if data_period == "Run2016" or data_period == "Summer16":
    analysis_ntuples.BTAG_DEEP_CSV_MEDIUM  = analysis_ntuples.BTAG_DEEP_CSV_MEDIUM_2016
if data_period == "Run2017" or data_period == "Fall17":
    analysis_ntuples.BTAG_DEEP_CSV_MEDIUM  = analysis_ntuples.BTAG_DEEP_CSV_MEDIUM_2017
if data_period == "Run2018" or data_period == "Autumn18":
    analysis_ntuples.BTAG_DEEP_CSV_MEDIUM  = analysis_ntuples.BTAG_DEEP_CSV_MEDIUM_2018

print("Current value for btags", analysis_ntuples.BTAG_DEEP_CSV_MEDIUM)


newObservableStrs  = {"BTagsDeepMedium" : "int",
                      "prefireWeight" : "float",
                      "hemFailureVetoElectrons" : "bool",
                      "hemFailureVetoJets" : "bool",
                      "hemFailureVetoMuons" : "bool",
                      "hemFailureVetoTracks" : "bool",
                      "passesUniversalSelection" : "bool",
                     }

if is_data:
    newObservableStrs["Weight"] = "float"

prefireFile = TFile(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/L1prefiring_jet_2017BtoF.root"))
prefireHistMap = prefireFile.Get("L1prefiring_jet_2017BtoF")

fileList = [input_file]

for filename in fileList:
    if os.path.isdir(filename): continue
    print("processing file " + filename)
    f = TFile(filename, "update")
    
    t = f.Get("tEvent")
    
    shouldSkipTree = False
    rewriteTree = False

    nentries = t.GetEntries();
    
    obsMem = {}
    branches = {}
    
    # HEM FAILURE
    blockhem = False
    partiallyblockhem = False
    if "Run2018B" in filename:
        partiallyblockhem = True
    if "Run2018C" in filename or "Run2018D" in filename:
        blockhem = True
    
    print('Analysing', nentries, "entries")
    
    for ientry in range(nentries):
        if ientry % 1000 == 0:
            print("Processing " + str(ientry) + " out of " + str(nentries))
        t.GetEntry(ientry)
        
        for newObservableStr in newObservableStrs:
                            
            obsStr = newObservableStr
    
            if obsMem.get(obsStr) is None:
                obsMem[newObservableStr] = np.zeros(1,dtype=eval(newObservableStrs[newObservableStr]))

                if t.GetBranchStatus(obsStr):
                    print("Restting branch", obsStr)
                    branch = t.GetBranch(obsStr)
                    branch.Reset()
                    branch.SetAddress(obsMem[obsStr])
                    branches[obsStr] = branch
                else:
                    branch = t.Branch(obsStr,obsMem[obsStr],obsStr+"/" + utils.typeTranslation[newObservableStrs[newObservableStr]]);
                    branches[obsStr] = branch
            
            if newObservableStr == "BTagsDeepMedium":
                nj, btagsDeepMedium, ljet = analysis_ntuples.eventNumberOfJets30Pt2_4Eta_DeepMedium(t.Jets, t.Jets_bJetTagDeepCSVBvsAll)
                #print(btagsDeepMedium)
                obsMem["BTagsDeepMedium"][0] = btagsDeepMedium
            elif newObservableStr == "prefireWeight":
                prefireWeight = 1.0
                for j in t.Jets:
                    if j.Pt() > 40 and abs(j.Eta()) > 1.75 and abs(j.Eta()) < 3.5:
                        eff = prefireHistMap.GetBinContent(prefireHistMap.FindFixBin(j.Eta(),j.Pt()))
                        #if eff != 0:
                        #    print("Found a weight!", eff)
                        prefireWeight *= (1-eff)
                #if prefireWeight != 1:
                #    print("prefireWeight", prefireWeight)
                obsMem["prefireWeight"][0] = prefireWeight
                
                
            elif newObservableStr == "passesUniversalSelection":    
                obsMem["passesUniversalSelection"][0] = 1
                if is_fastsim:
                    obsMem["passesUniversalSelection"][0] = analysis_ntuples.passesUniversalSelectionFastSim(t, t.MET, t.METPhi)
                else:
                    if not is_data:
                        obsMem["passesUniversalSelection"][0] = analysis_ntuples.passesUniversalSelection(t, t.MET, t.METPhi)
                    elif is_data:
                        obsMem["passesUniversalSelection"][0] = analysis_ntuples.passesUniversalDataSelection(t, t.MET, t.METPhi)
            elif newObservableStr == "hemFailureVetoElectrons":
                obsMem["hemFailureVetoElectrons"][0] = 1
                if is_fastsim or blockhem or (partiallyblockhem and t.RunNum>=319077):
                    for i, electron in enumerate(t.Electrons):
                        if analysis_ntuples.electronPassesTightSelection(i, t.Electrons, t.Electrons_passNoIso, t.Electrons_deltaRLJ):
                            if -3.0 < electron.Eta() and electron.Eta() < -1.4 and -1.57 < electron.Phi() and electron.Phi() < -0.87:
                                obsMem["hemFailureVetoElectrons"][0] = 0
                                print("hem veto electron")
            elif newObservableStr == "hemFailureVetoMuons":
                obsMem["hemFailureVetoMuons"][0] = 1
                if is_fastsim or blockhem or (partiallyblockhem and t.RunNum>=319077):
                    for i, muon in enumerate(t.Muons):
                        if analysis_ntuples.muonPassesTightSelection(i, t.Muons, t.Muons_mediumID, t.Muons_passNoIso, t.Muons_deltaRLJ):
                            if -3.0 < muon.Eta() and muon.Eta() < -1.4 and -1.57 < muon.Phi() and muon.Phi() < -0.87:
                                obsMem["hemFailureVetoMuons"][0] = 0
                                print("hem veto muon")
            elif newObservableStr == "hemFailureVetoJets": 
                obsMem["hemFailureVetoJets"][0] = 1
                if is_fastsim or blockhem or (partiallyblockhem and t.RunNum>=319077):
                    for i, jet in enumerate(t.Jets):
                        if jet.Pt() > 30 and -3.2 < jet.Eta() and jet.Eta() < -1.2 and -1.77 < jet.Phi() and jet.Phi() < -0.67:
                            mhtvec = TLorentzVector()
                            mhtvec.SetPtEtaPhiE(t.MHT, 0, t.MHTPhi, t.MHT)
                            deltaPhiJetMht = abs(jet.DeltaPhi(mhtvec))
                            if deltaPhiJetMht < 0.5:
                                obsMem["hemFailureVetoJets"][0] = 0
                                print("hem veto jet")
            elif newObservableStr == "hemFailureVetoTracks":
                obsMem["hemFailureVetoTracks"][0] = 1
                if is_fastsim or blockhem or (partiallyblockhem and t.RunNum>=319077):
                    for ti, track in enumerate(t.tracks):
                        if track.Pt() > 10:
                            continue
                        if abs(track.Eta()) > 2.4:
                            continue
                        if t.tracks_trkRelIso[ti] > 0.1:
                            continue 
                        if t.tracks_dxyVtx[ti] > 0.02:
                            continue
                        if t.tracks_dzVtx[ti] > 0.02:
                            continue
                        analysis_muons = [t.Muons[mi] for mi, muon in enumerate(t.Muons) if analysis_ntuples.muonPassesTightSelection(mi, t.Muons, t.Muons_mediumID, t.Muons_passNoIso, t.Muons_deltaRLJ)]
                        minimum, minCan = analysis_ntuples.minDeltaLepLeps(track, analysis_muons)
                        if minimum is None or minimum > 0.01:
                            minimum, minCan = analysis_ntuples.minDeltaLepLeps(track, t.Electrons)
                            if minimum is None or minimum > 0.01:
                                if -3.0 < track.Eta() and track.Eta() < -1.4 and -1.57 < track.Phi() and track.Phi() < -0.87:
                                    obsMem["hemFailureVetoTracks"][0] = 0
                                    print("hem veto track")
            elif newObservableStr == "Weight":
                obsMem["Weight"][0] = 1
            
            branches[obsStr].Fill()
        
        continue
   
    t.Write("tEvent",TObject.kOverwrite)
    print("Done")
    f.Close()


    

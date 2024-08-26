#!/usr/bin/env python3

from ROOT import *
from glob import glob
from sys import exit
import argparse
import sys
import numpy as np
import os
import xml.etree.ElementTree as ET
from math import *
import cppyy

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes"))
from lib import analysis_ntuples
from lib import analysis_tools
from lib import utils
from lib import cut_optimisation
from lib import analysis_observables
from lib import analysis_selections

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
parser.add_argument('-phase1', '--phase1', dest='phase1', help='Phase1 Samples', action='store_true')
parser.add_argument('-phase1_2018', '--phase1_2018', dest='phase1_2018', help='Phase1 2018 Samples', action='store_true')
parser.add_argument('-jpsi_muons', '--jpsi_muons', dest='jpsi_muons', help='JPSI Muons Skim', action='store_true')
args = parser.parse_args()


signal = args.signal
bg = args.bg
sc = args.sc

jpsi_muons = args.jpsi_muons

if args.sam:
    signal = True

print("SAME CHARGE=", sc)

jpsi = False

if jpsi_muons:
    jpsi = True
    print("Got JPSI")
    if jpsi_muons:
        print("MUONS")
    else:
        print("ELECTRONS")

input_file = None
if args.input_file:
    input_file = args.input_file[0].strip()

# if (bg and signal) or not (bg or signal):
#     signal = True
#     bg = False

track_bdt = None
if args.track_bdt:
    track_bdt = args.track_bdt[0]

######## END OF CMDLINE ARGUMENTS ########

exTrackVars = {}
track_bdt_vars_maps = {}
track_bdt_specs_maps = {}
track_bdt_readers = {}
branches = {}

filledEvents = 0
filledBlankEvents = 0

def fillInNonTrackInfo(c, postfix, prefix):
    global filledEvents
    global filledBlankEvents
    if prefix == "" and postfix == analysis_selections.jetIsos["Muons"]:
        filledEvents += 1
        filledBlankEvents += 1
    for stringObs in analysis_observables.exclusiveTrackObservablesStringList:
        exTrackVars[prefix + stringObs + postfix] = cppyy.gbl.std.string("")
        #print("*")
        #print(branches[stringObs + postfix])
        #print("**")
        #print(exTrackVars[stringObs + postfix])
        #branches[stringObs + postfix].ResetAddress()
        c.SetBranchAddress(prefix + stringObs + postfix, exTrackVars[prefix + stringObs + postfix])
        #branches[stringObs + postfix].SetAddress(exTrackVars[stringObs + postfix])
        #print("**")
        branches[prefix + stringObs + postfix].Fill()
        #print("***")
    for DTypeObs in analysis_observables.commonObservablesDTypesList:
        exTrackVars[prefix + "exTrack_" + DTypeObs + postfix][0] = -1
        #print("****")
        branches[prefix + "exTrack_" + DTypeObs + postfix].Fill()
        #print("*****")
    for DTypeObs in analysis_observables.exclusiveTrackObservablesDTypesList:
        if DTypeObs == "exclusiveTrack" or DTypeObs == "trackZ":
            exTrackVars[prefix + DTypeObs + postfix][0] = 0
            #print("******")
        else:
            exTrackVars[prefix + DTypeObs + postfix][0] = -1
            #print("******")
        branches[prefix + DTypeObs + postfix].Fill()         
        #print("*******")
    for CTypeObs in analysis_observables.exclusiveTrackObservablesClassList:
        exTrackVars[prefix + CTypeObs + postfix] = eval(analysis_observables.exclusiveTrackObservablesClassList[CTypeObs])()
        #print("********")
        c.SetBranchAddress(prefix + CTypeObs + postfix, exTrackVars[prefix + CTypeObs + postfix])
        #branches[CTypeObs + postfix].SetAddress(exTrackVars[CTypeObs + postfix])
        #print("*********")
        branches[prefix + CTypeObs + postfix].Fill()
        #print("**********")

def main():
    
    if jpsi:
        utils.defaultJetIsoSetting = "NoIso"
    
    file = TFile(input_file, "update")
    
    c = file.Get("tEvent")
    nentries = c.GetEntries()
    
    # CREATE VARS, BRANCHES, AND BDT READERS
    
    for iso in utils.leptonIsolationList:
        for cat in utils.leptonIsolationCategories:
            ptRanges = [""]
            drCuts  = [""]

            if iso in ["CorrJetIso", "CorrJetNoMultIso"]:
                ptRanges = utils.leptonCorrJetIsoPtRange
                drCuts = utils.leptonCorrJetIsoDrCuts
            for ptRange in ptRanges:
                for drCut in drCuts:
                    cuts = ""
                    if len(str(ptRange)) > 0:
                        cuts = str(ptRange) + "Dr" + str(drCut)
                    
                    postfixi = [iso + cuts + cat]
                    
                    if iso + cuts + cat == utils.defaultJetIsoSetting:
                        postfixi = [iso + cuts + cat, ""]
                
                    for postfix in postfixi:
                        
                        if postfix not in [analysis_selections.jetIsos["Muons"], analysis_selections.jetIsos["Electrons"]]:
                            continue
                        
                        for sameCharge in [False, True]:
                            prefix = "sc_" if sameCharge else ""
                            for stringObs in analysis_observables.exclusiveTrackObservablesStringList:
                                exTrackVars[prefix + stringObs + postfix] = cppyy.gbl.std.string("")
                                if c.GetBranchStatus(prefix + stringObs + postfix):
                                    print("Reseting branch", prefix + stringObs + postfix)
                                    branches[prefix + stringObs + postfix] = c.GetBranch(prefix + stringObs + postfix)
                                    branches[prefix + stringObs + postfix].Reset()
                                    c.SetBranchAddress(prefix + stringObs + postfix, exTrackVars[prefix + stringObs + postfix])
                                else:
                                    print("Branching", prefix + stringObs + postfix)
                                    branches[prefix + stringObs + postfix] = c.Branch(prefix + stringObs + postfix, 'std::string', exTrackVars[prefix + stringObs + postfix])
                                    c.SetBranchAddress(prefix + stringObs + postfix, exTrackVars[prefix + stringObs + postfix])
                            for DTypeObs in analysis_observables.commonObservablesDTypesList:
                                exTrackVars[prefix + "exTrack_" + DTypeObs + postfix] = np.zeros(1,dtype=analysis_observables.commonObservablesDTypesList[DTypeObs])
                                if c.GetBranchStatus(prefix + "exTrack_" + DTypeObs + postfix):
                                    print("Reseting branch", prefix + "exTrack_" + DTypeObs + postfix)
                                    branches[prefix + "exTrack_" + DTypeObs + postfix] = c.GetBranch(prefix + "exTrack_" + DTypeObs + postfix)
                                    branches[prefix + "exTrack_" + DTypeObs + postfix].Reset()
                                    c.SetBranchAddress(prefix + "exTrack_" + DTypeObs + postfix, exTrackVars[prefix + "exTrack_" + DTypeObs + postfix])
                                    #branches["exTrack_" + DTypeObs + postfix].SetAddress(exTrackVars["exTrack_" + DTypeObs + postfix])
                                else:
                                    print("Branching", prefix + "exTrack_" + DTypeObs + postfix)
                                    branches[prefix + "exTrack_" + DTypeObs + postfix] = c.Branch(prefix + "exTrack_" + DTypeObs + postfix, exTrackVars[prefix + stringObs + postfix], prefix + "exTrack_" + DTypeObs + postfix + "/" + utils.typeTranslation[analysis_observables.commonObservablesDTypesList[DTypeObs]])
                                    c.SetBranchAddress(prefix + "exTrack_" + DTypeObs + postfix, exTrackVars[prefix + "exTrack_" + DTypeObs + postfix])
                            for DTypeObs in analysis_observables.exclusiveTrackObservablesDTypesList:
                                exTrackVars[prefix + DTypeObs + postfix] = np.zeros(1,dtype=analysis_observables.exclusiveTrackObservablesDTypesList[DTypeObs])
                                if c.GetBranchStatus(prefix + DTypeObs + postfix):
                                    print("Reseting branch", prefix + DTypeObs + postfix)
                                    branches[prefix + DTypeObs + postfix] = c.GetBranch(prefix + DTypeObs + postfix)
                                    branches[prefix + DTypeObs + postfix].Reset()
                                    c.SetBranchAddress(prefix + DTypeObs + postfix, exTrackVars[prefix + DTypeObs + postfix])
                                    #branches[DTypeObs + postfix].SetAddress(exTrackVars[DTypeObs + postfix])
                                else:
                                    print("Branching", prefix + DTypeObs + postfix)
                                    branches[prefix + DTypeObs + postfix] = c.Branch(prefix + DTypeObs + postfix, exTrackVars[prefix + DTypeObs + postfix], prefix + DTypeObs + postfix + "/" + utils.typeTranslation[analysis_observables.exclusiveTrackObservablesDTypesList[DTypeObs]])
                                    c.SetBranchAddress(prefix + DTypeObs + postfix, exTrackVars[prefix + DTypeObs + postfix])
                            for CTypeObs in analysis_observables.exclusiveTrackObservablesClassList:
                                exTrackVars[prefix + CTypeObs + postfix] = eval(analysis_observables.exclusiveTrackObservablesClassList[CTypeObs])()
                                if c.GetBranchStatus(prefix + CTypeObs + postfix):
                                    print("Reseting branch", prefix + CTypeObs + postfix)
                                    branches[prefix + CTypeObs + postfix] = c.GetBranch(prefix + CTypeObs + postfix)
                                    branches[prefix + CTypeObs + postfix].Reset()
                                    c.SetBranchAddress(prefix + CTypeObs + postfix, exTrackVars[prefix + CTypeObs + postfix])
                                else:
                                    print("Branching", prefix + CTypeObs + postfix)
                                    branches[prefix + CTypeObs + postfix] = c.Branch(prefix + CTypeObs + postfix, analysis_observables.exclusiveTrackObservablesClassList[CTypeObs], exTrackVars[prefix + CTypeObs + postfix])
                                    c.SetBranchAddress(prefix + CTypeObs + postfix, exTrackVars[prefix + CTypeObs + postfix])
                    if not jpsi:
                        for lep in ["Muons", "Electrons"]:
                            
                            if iso + cuts + cat != analysis_selections.jetIsos[lep]:
                            #if iso + cuts + cat not in [analysis_selections.jetIsos["Muons"], analysis_selections.jetIsos["Electrons"]]:
                                continue
                            
                            track_bdt_weights = track_bdt + "/" + lep + "/dataset/weights/TMVAClassification_" + lep + iso + cuts + cat + ".weights.xml"
                            track_bdt_vars = cut_optimisation.getVariablesFromXMLWeightsFile(track_bdt_weights)
                            track_bdt_vars_map = cut_optimisation.getVariablesMemMap(track_bdt_vars)
                            track_bdt_specs = cut_optimisation.getSpecSpectatorFromXMLWeightsFile(track_bdt_weights)
                            track_bdt_specs_map = cut_optimisation.getSpectatorsMemMap(track_bdt_specs)
                            track_bdt_reader = cut_optimisation.prepareReader(track_bdt_weights, track_bdt_vars, track_bdt_vars_map, track_bdt_specs, track_bdt_specs_map)

                            track_bdt_vars_maps[lep + iso + cuts + cat] = track_bdt_vars_map
                            track_bdt_specs_maps[lep + iso + cuts + cat] = track_bdt_specs_map
                            track_bdt_readers[lep + iso + cuts + cat] = track_bdt_reader

    print('Analysing', nentries, "entries")

    afterMonoLepton = 0
    afterUniversalBdt = 0
    afterMonoTrack = 0
    afterAtLeastOneTrack = 0

    totalTracks = 0
    totalSurvivedTracks = 0
    eventsWithGreaterThanOneOppSignTracks = 0
    noSurvivingTracks = 0
    
    file.cd()
    generalEvents = 0
    for ientry in range(nentries):
        if ientry % 100 == 0:
            print("Processing " + str(ientry) + " out of " + str(nentries))
        c.GetEntry(ientry)
        #continue
        
        genZL, genNonZL = None, None
        if signal:
            genZL, genNonZL = analysis_ntuples.classifyGenZLeptons(c)
        
        for iso in utils.leptonIsolationList:
            for cat in utils.leptonIsolationCategories:
                ptRanges = [""]
                drCuts  = [""]

                if iso in ["CorrJetIso", "CorrJetNoMultIso"]:
                    ptRanges = utils.leptonCorrJetIsoPtRange
                    drCuts = utils.leptonCorrJetIsoDrCuts
                for ptRange in ptRanges:
                    for drCut in drCuts:
                        cuts = ""
                        if len(str(ptRange)) > 0:
                            cuts = str(ptRange) + "Dr" + str(drCut)

                        postfixi = [iso + cuts + cat]

                        if iso + cuts + cat == utils.defaultJetIsoSetting:
                            postfixi = [iso + cuts + cat, ""]
                    
                        for postfix in postfixi:
                            
                            if postfix not in [analysis_selections.jetIsos["Muons"], analysis_selections.jetIsos["Electrons"]]:
                                continue
                            if postfix == analysis_selections.jetIsos["Muons"]:
                                generalEvents += 1
                            for sameCharge in [False, True]:
                            
                                prefix = "sc_" if sameCharge else ""
                            
                                exTrackVars[prefix + "exclusiveTrack" + postfix][0] = 0
                                exTrackVars[prefix + "trackZ" + postfix][0] = 0
                        
                                ll, lepIdx, leptonCharge, leptonFlavour, t, ti = None, None, None, None, None, None
                        
                                if jpsi:
                                    ll, lepIdx, t, ti = analysis_ntuples.getSingleJPsiLeptonAfterSelection(24, 24, c.Muons, getattr(c, "Muons_pass" + iso + cuts), c.Muons_mediumID, c.Muons_charge, c.tracks, c.tracks_charge, utils.leptonIsolationCategories[cat]["muonPt"], utils.leptonIsolationCategories[cat]["lowPtTightMuons"], c.Muons_tightID, c.Muons_passIso)
                                else:
                                    ll, lepIdx, leptonCharge, leptonFlavour = analysis_ntuples.getSingleLeptonAfterSelection(c.Electrons, getattr(c, "Electrons_pass" + iso + cuts), c.Electrons_deltaRLJ, c.Electrons_charge, c.Muons, getattr(c, "Muons_pass" + iso + cuts), c.Muons_mediumID, c.Muons_deltaRLJ, c.Muons_charge, utils.leptonIsolationCategories[cat]["muonPt"], utils.leptonIsolationCategories[cat]["lowPtTightMuons"], c.Muons_tightID)
        
                                if ll is None:
                                    # NOT TWO TRACKS
                                    #print("**** BEFORE FILL ***" )
                                    fillInNonTrackInfo(c, postfix, prefix)
                                    #print("**** AFTER FILL ***")
                                    continue
                        
                                if jpsi:
                                    leptonFlavour = "Muons"
                                    leptonCharge = c.Muons_charge[lepIdx]
                        
                                if leptonCharge == 0:
                                    print("WHAT?! leptonCharge=0")
                                
                                if postfix != analysis_selections.jetIsos[leptonFlavour]:
                                    fillInNonTrackInfo(c, postfix, prefix)
                                    continue
                                
                                exTrackVars[prefix + "lepton_charge" + postfix][0] = leptonCharge
                                exTrackVars[prefix + "exclusiveTrackLeptonFlavour" + postfix] = cppyy.gbl.std.string(leptonFlavour)
    
                                afterMonoLepton += 1
                    
                                exTrackVars[prefix + "secondTrackBDT" + postfix][0] = -1
        
                                metvec = TLorentzVector()
                                metvec.SetPtEtaPhiE(c.MET, 0, c.METPhi, c.MET)
                                
                                mhtvec = TLorentzVector()
                                mhtvec.SetPtEtaPhiE(c.MHT, 0, c.MHTPhi, c.MHT)
                        
                                highestOppositeTrackScore = None
                                secondTrackScore = None
                                secondTrack = None
                                oppositeChargeTrack = None
                                ntracks = 0
                        
                                if not jpsi:
                                    for ti in range(c.tracks.size()):
                                        t = c.tracks[ti]
                                        if t.Pt() > 10:
                                            continue
                                        if abs(t.Eta()) > 2.4:
                                            continue
                                        tcharge = c.tracks_charge[ti]
                                        #Try lowering to 0!!
            
                                        if c.tracks_trkRelIso[ti] > 0.1:
                                            continue 
                                        if c.tracks_dxyVtx[ti] > 0.02:
                                            continue
                                        if c.tracks_dzVtx[ti] > 0.02:
                                            continue
                                        if sameCharge:
                                            if tcharge * leptonCharge < 0:
                                                continue
                                        else:
                                            if tcharge * leptonCharge > 0:
                                                continue
                                        
                                        if (t + ll).M() < 0:
                                            continue
                                        
                                        deltaRLL = abs(t.DeltaR(ll))
                                        if deltaRLL < 0.01:
                                            continue
                                        totalTracks +=1
                                        ntracks += 1
                        
                                        track_bdt_vars_maps[leptonFlavour + iso + cuts + cat]["deltaEtaLJ"][0] = abs(t.Eta() - c.LeadingJet.Eta())
                                        track_bdt_vars_maps[leptonFlavour + iso + cuts + cat]["deltaRLJ"][0] = abs(t.DeltaR(c.LeadingJet))
                                        #track_bdt_vars_maps[leptonFlavour + iso + cuts + cat]["track.Phi()"][0] = t.Phi()
                                        #track_bdt_vars_maps[leptonFlavour + iso + cuts + cat]["track.Pt()"][0] = t.Pt()
                                        track_bdt_vars_maps[leptonFlavour + iso + cuts + cat]["abs(track.Eta())"][0] = abs(t.Eta())
            
            
                                        track_bdt_vars_maps[leptonFlavour + iso + cuts + cat]["deltaEtaLL"][0] = abs(t.Eta()-ll.Eta()) 
                                        track_bdt_vars_maps[leptonFlavour + iso + cuts + cat]["abs(deltaPhiLL)"][0] = abs(t.DeltaPhi(ll))
                                        track_bdt_vars_maps[leptonFlavour + iso + cuts + cat]["deltaRLL"][0] = abs(t.DeltaR(ll))
                                        #track_bdt_vars_maps[leptonFlavour + iso + cuts + cat]["mtt"][0] = analysis_tools.MT2(c.MET, c.METPhi, t)
                                        #track_bdt_vars_map["deltaRMet"][0] = abs(t.DeltaR(metvec))
                                        track_bdt_vars_maps[leptonFlavour + iso + cuts + cat]["deltaPhiMht"][0] = abs(t.DeltaPhi(mhtvec))
            
                                        track_bdt_vars_maps[leptonFlavour + iso + cuts + cat]["abs(lepton.Eta())"][0] = abs(ll.Eta())
                                        #track_bdt_vars_maps[leptonFlavour + iso + cuts + cat]["lepton.Phi()"][0] = ll.Phi()
                                        track_bdt_vars_maps[leptonFlavour + iso + cuts + cat]["lepton.Pt()"][0] = ll.Pt()
                                        track_bdt_vars_maps[leptonFlavour + iso + cuts + cat]["invMass"][0] = (t + ll).M()
            
            
                                        #for trackVar in ['dxyVtx', 'dzVtx','trkMiniRelIso', 'trkRelIso']:
                                        #    val = eval("c.tracks_" + trackVar + "[" + str(ti) + "]")
                                        #    if val == 0:
                                        #        val = 0.000000000000001
                                        #    track_bdt_vars_maps[leptonFlavour + iso + cuts + cat]["log(" + trackVar + ")"][0] = log(val)
            
                                        track_tmva_value = track_bdt_readers[leptonFlavour + iso + cuts + cat].EvaluateMVA("BDT")
            
                                        if  highestOppositeTrackScore is None or highestOppositeTrackScore < track_tmva_value:
                                            if highestOppositeTrackScore is not None:
                                                secondTrackScore = highestOppositeTrackScore
                                                exTrackVars[prefix + "secondTrackBDT" + postfix][0] = exTrackVars[prefix + "trackBDT" + postfix][0]
                                                secondTrack = oppositeChargeTrack
                                            highestOppositeTrackScore = track_tmva_value
                                            exTrackVars[prefix + "trackBDT" + postfix][0] = track_tmva_value
                                            oppositeChargeTrack = ti
                                else:
                                    highestOppositeTrackScore = 1
                                    secondTrackScore = 1
                                    secondTrack = None
                                    oppositeChargeTrack = ti
                                    ntracks = 0
                            
                            
                                if highestOppositeTrackScore is None:
                                    fillInNonTrackInfo(c, postfix, prefix)
                                    #print("2")
                                    continue
                                #print("REAL ONE")
                                afterAtLeastOneTrack += 1
                                afterMonoTrack += 1
                    
                                exTrackVars[prefix + "exclusiveTrack" + postfix][0] = 1
                    
                                exTrackVars[prefix + "ti" + postfix][0] = oppositeChargeTrack
                                if secondTrack is not None:
                                    exTrackVars[prefix + "sti" + postfix][0] = secondTrack
                                else:
                                    exTrackVars[prefix + "sti" + postfix][0] = -1
                                if signal:
                                    if genZL is None:
                                        exTrackVars[prefix + "trackZ" + postfix][0] = 0
                                    else:
                                        l = c.tracks[oppositeChargeTrack]
                                        minZ, minCanZ = analysis_ntuples.minDeltaRGenParticles(l, genZL, c.GenParticles)
                                        minNZ, minCanNZ = analysis_ntuples.minDeltaRGenParticles(l, genNonZL, c.GenParticles)
                                        min = 0
                                        if minNZ is None or minZ < minNZ:
                                            min = minZ
                                        else:
                                            min = minNZ
                            
                                        if min < 0.01 and (minNZ is None or minZ < minNZ):
                                            if c.tracks_charge[ti] * c.GenParticles_PdgId[minCanZ] < 0 and (abs(c.GenParticles_PdgId[minCanZ]) == 11 or abs(c.GenParticles_PdgId[minCanZ]) == 13):
                                                exTrackVars[prefix + "trackZ" + postfix][0] = 1
        
                                l1 = None
                                l2 = None
                                if ll.Pt() > c.tracks[oppositeChargeTrack].Pt():
                                    l1 = ll
                                    l2 = c.tracks[oppositeChargeTrack]
                                else:
                                    l1 = c.tracks[oppositeChargeTrack]
                                    l2 = ll
                    
                                exTrackVars[prefix + "l1" + postfix] = l1
                                exTrackVars[prefix + "l2" + postfix] = l2
                                exTrackVars[prefix + "lepton" + postfix] = ll
                                exTrackVars[prefix + "track" + postfix] = c.tracks[oppositeChargeTrack]
                                exTrackVars[prefix + "leptonIdx" + postfix][0] = lepIdx
                    
                                if secondTrack is not None:
                                    exTrackVars[prefix + "secondTrack" + postfix] = c.tracks[secondTrack]
                                else:
                                    exTrackVars[prefix + "secondTrack" + postfix] = TLorentzVector()
                    
                                exTrackVars[prefix + "exTrack_invMass" + postfix][0] = (l1 + l2).M()
                                exTrackVars[prefix + "exTrack_dileptonPt" + postfix][0] = abs((l1 + l2).Pt())
                                exTrackVars[prefix + "exTrack_deltaPhi" + postfix][0] =  abs(l1.DeltaPhi(l2))
                                exTrackVars[prefix + "exTrack_deltaEta" + postfix][0] = abs(l1.Eta() - l2.Eta())
                                exTrackVars[prefix + "exTrack_deltaR" + postfix][0] = abs(l1.DeltaR(l2))
                                exTrackVars[prefix + "NTracks" + postfix][0] = ntracks

                                exTrackVars[prefix + "exTrack_pt3" + postfix][0] = analysis_tools.pt3(l1.Pt(),l1.Phi(),l2.Pt(),l2.Phi(),c.MET,c.METPhi)

                                exTrackVars[prefix + "exTrack_mt1" + postfix][0] = analysis_tools.MT2(c.MET, c.METPhi, l1)
                                exTrackVars[prefix + "exTrack_mt2" + postfix][0] = analysis_tools.MT2(c.MET, c.METPhi, l2)

                                exTrackVars[prefix + "mtt" + postfix][0] = analysis_tools.MT2(c.MET, c.METPhi, c.tracks[oppositeChargeTrack])
                                exTrackVars[prefix + "mtl" + postfix][0] = analysis_tools.MT2(c.MET, c.METPhi, ll)
                        
                                exTrackVars[prefix + "exTrack_mtautau" + postfix][0] = analysis_tools.Mtautau(metvec, l1, l2)
                    
                                exTrackVars[prefix + "exTrack_deltaEtaLeadingJetDilepton" + postfix][0] = abs((l1 + l2).Eta() - c.LeadingJet.Eta())
                                exTrackVars[prefix + "exTrack_deltaPhiLeadingJetDilepton" + postfix][0] = abs((l1 + l2).DeltaPhi(c.LeadingJet))
                    
                                exTrackVars[prefix + "exTrack_dilepHt" + postfix][0] = analysis_ntuples.htJet30Leps(c.Jets, [l1,l2])
                    
                                exTrackVars[prefix + "deltaPhiMetTrack" + postfix][0] = abs(c.tracks[oppositeChargeTrack].DeltaPhi(metvec))
                                exTrackVars[prefix + "deltaPhiMetLepton" + postfix][0] = abs(ll.DeltaPhi(metvec))
                                
                                exTrackVars[prefix + "deltaPhiMhtTrack" + postfix][0] = abs(c.tracks[oppositeChargeTrack].DeltaPhi(mhtvec))
                                exTrackVars[prefix + "deltaPhiMhtLepton" + postfix][0] = abs(ll.DeltaPhi(mhtvec))
                                global filledEvents
                                if prefix == "" and postfix == analysis_selections.jetIsos["Muons"]:
                                    filledEvents += 1
                                #print("HERE!!!")
                                for stringObs in analysis_observables.exclusiveTrackObservablesStringList:
                                    c.SetBranchAddress(prefix + stringObs + postfix, exTrackVars[prefix + stringObs + postfix])
                                    #branches[stringObs + postfix].SetAddress(exTrackVars[stringObs + postfix])
                                    branches[prefix + stringObs + postfix].Fill()
                                for DTypeObs in analysis_observables.commonObservablesDTypesList:
                                    branches[prefix + "exTrack_" + DTypeObs + postfix].Fill()
                                for DTypeObs in analysis_observables.exclusiveTrackObservablesDTypesList:
                                    branches[prefix + DTypeObs + postfix].Fill()         
                                for CTypeObs in analysis_observables.exclusiveTrackObservablesClassList:
                                    c.SetBranchAddress(prefix + CTypeObs + postfix, exTrackVars[prefix + CTypeObs + postfix])
                                    #branches[CTypeObs + postfix].SetAddress(exTrackVars[CTypeObs + postfix])
                                    branches[prefix + CTypeObs + postfix].Fill()
                            #print("AFTER!!!")

    c.Write("tEvent",TObject.kOverwrite)
    
    file.Close()

    print("nentries=" + str(nentries))
    print("totalTracks=" + str(totalTracks))
    print("totalSurvivedTracks=" + str(totalSurvivedTracks))
    print("eventsWithGreaterThanOneOppSignTracks=" + str(eventsWithGreaterThanOneOppSignTracks))
    print("noSurvivingTracks=" + str(noSurvivingTracks))
    print("afterAtLeastOneTrack=" + str(afterAtLeastOneTrack))
    print("afterMonoLepton=" + str(afterMonoLepton))
    print("afterUniversalBdt=" + str(afterUniversalBdt))
    print("afterMonoTrack=" + str(afterMonoTrack))
    print("filledEvents=" + str(filledEvents))
    print("filledBlankEvents=" + str(filledBlankEvents))
    print("generalEvents=" + str(generalEvents))
    
    

main()
#!/usr/bin/env python

from ROOT import *
from glob import glob
from math import *
from sys import exit
from array import array
import argparse
import sys
import numpy as np
import os

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools"))
#sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes"))

from lib import utils
from lib import analysis_ntuples
from lib import analysis_tools
from lib import analysis_selections

# gSystem.Load('LumiSectMap_C')
# from ROOT import LumiSectMap
# 
# gSystem.Load('LeptonCollectionMap_C')
# from ROOT import LeptonCollectionMap
# from ROOT import LeptonCollectionFilesMap
# from ROOT import LeptonCollection

gROOT.SetBatch(1)

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Split tracks into signal and background trees.')
parser.add_argument('-i', '--input_file', nargs=1, help='Input Filename', required=True)
parser.add_argument('-o', '--output_file', nargs=1, help='Output Filename', required=False)
args = parser.parse_args()

input_file = None
output_file = None
if args.input_file:
    input_file = args.input_file[0]
if args.output_file:
    output_file = args.output_file[0]

######## END OF CMDLINE ARGUMENTS ########

def main():

    tracksVars = (
        {"name":"dxyVtx", "type":"D"},
        {"name":"dzVtx", "type":"D"},
        {"name":"chi2perNdof", "type":"D"},
        {"name":"trkMiniRelIso", "type":"D"},
        {"name":"trkRelIso", "type":"D"},
    )

    otherVars = (
        {"name":"track", "type2":'TLorentzVector'},
        {"name":"deltaEtaLL", "type":"D"},
        {"name":"deltaPhiLL", "type":"D"},
        {"name":"deltaEtaLJ", "type":"D"},
        {"name":"deltaRLL", "type":"D"},
        {"name":"deltaRLJ", "type":"D"},
        {"name":"mtt", "type":"D"},
        {"name":"deltaPhiMet", "type":"D"},
        {"name":"deltaPhiMht", "type":"D"},
        {"name":"lepton", "type2":"TLorentzVector"},
        {"name":"invMass", "type":"D"},
    )

    vars = otherVars + tracksVars

    varsDict = {}
    for i,v in enumerate(vars):
        varsDict[v["name"]] = i

    utils.addMemToTreeVarsDef(vars)
    
    signalTrees = {}
    bgTrees = {}
    
    
    for iso in utils.leptonIsolationList:
        for cat in utils.leptonIsolationCategories:
            
            ptRanges = [""]
            drCuts = [""]
            if iso in ["CorrJetIso", "CorrJetNoMultIso"]:
                ptRanges = utils.leptonCorrJetIsoPtRange
                drCuts = utils.leptonCorrJetIsoDrCuts
            for ptRange in ptRanges:
                for drCut in drCuts:
                    cuts = ""
                    if len(str(ptRange)) > 0:
                        cuts = str(ptRange) + "Dr" + str(drCut)
                    postfix = iso + cuts + cat
                    save_file = False
                    for lep in ["Electrons", "Muons"]:
                        if postfix != analysis_selections.jetIsos[lep]:
                            continue
                        save_file = True
                        signalTrees[lep + postfix] = TTree(lep + postfix, lep + postfix)
                        utils.barchTreeFromVarsDef(signalTrees[lep + postfix], vars)
                    if not save_file:
                        continue
                    bgTrees[postfix] = TTree(postfix, postfix)
                    utils.barchTreeFromVarsDef(bgTrees[postfix], vars)

    c = TChain('tEvent')
    print("Going to open the file")
    print(input_file)
    c.Add(input_file)

    nentries = c.GetEntries()
    print('Analysing', nentries, "entries")
    afterAtLeastOneReco = 0
    notCorrect = 0
    noReco = 0
    clean = 0
    sigTrack = 0
    for ientry in range(nentries):
        if ientry % 5000 == 0:
            print("Processing " + str(ientry))
        c.GetEntry(ientry)
        #No exclusive track category
        #if c.category == 0:
        #    continue
        rightProcess = analysis_ntuples.isX1X2X1Process(c)
        if not rightProcess:
            #print("No")
            notCorrect += 1
            continue
        
        #print("Size Reco=")
        #print(str(len(c.Electrons) + len(c.Muons)))
        #if c.Electrons.size() + c.Muons.size() < 1:
            #print("No reco")
        #    noReco += 1
        #    continue
        #afterAtLeastOneReco += 1
        genZL, genNonZL = analysis_ntuples.classifyGenZLeptons(c)
        if genZL is None or len(genZL) == 0:
            #print("genZL is None")
            continue
        #if len(genNonZL) == 0:
            #print("genNonZL is None")
        if len(genZL) != 2:
            print("What:", len(genZL))
        
        for iso in utils.leptonIsolationList:
            for cat in utils.leptonIsolationCategories:
                ptRanges = [""]
                drCuts = [""]
                if iso in ["CorrJetIso", "CorrJetNoMultIso"]:
                    ptRanges = utils.leptonCorrJetIsoPtRange
                    drCuts = utils.leptonCorrJetIsoDrCuts
                for ptRange in ptRanges:
                    for drCut in drCuts:
                        
                        cuts = ""
                        if len(str(ptRange)) > 0:
                            cuts = str(ptRange) + "Dr" + str(drCut)
                        postfix = iso + cuts + cat
                        
                        if postfix not in  [analysis_selections.jetIsos["Muons"], analysis_selections.jetIsos["Electrons"]]:
                            continue
                        
                        ll, leptonIdx, leptonCharge, leptonFlavour = analysis_ntuples.getSingleLeptonAfterSelection(c.Electrons, getattr(c, "Electrons_pass" + postfix), c.Electrons_deltaRLJ, c.Electrons_charge, c.Muons, getattr(c, "Muons_pass" + postfix), c.Muons_mediumID, c.Muons_deltaRLJ, c.Muons_charge, utils.leptonIsolationCategories[cat]["muonPt"], utils.leptonIsolationCategories[cat]["lowPtTightMuons"], c.Muons_tightID)
                        
                        if ll is None:
                            leptons, leptonsIdx, leptonsCharge, leptonFlavour, same_sign, isoCr, isoCrMinDr = analysis_ntuples.getTwoLeptonsAfterSelection(c.Electrons, getattr(c, "Electrons_pass" + postfix), c.Electrons_deltaRLJ, c.Electrons_charge, c.Muons, getattr(c, "Muons_pass" + postfix), c.Muons_mediumID, c.Muons_deltaRLJ, c.Muons_charge, utils.leptonIsolationCategories[cat]["muonPt"], utils.leptonIsolationCategories[cat]["lowPtTightMuons"], c.Muons_tightID, False)
                            if isoCr > 0: 
                                continue
                            #if same_sign:
                            #    continue
                            if leptons is not None:
                                ll = leptons[0]
                        
                        if ll is None:
                            continue
                        #if leptonFlavour != getattr(c, "leptonFlavour" + iso + str(ptRange)):
                        #    continue
                    
                        metvec = TLorentzVector()
                        metvec.SetPtEtaPhiE(c.MET, 0, c.METPhi, c.MET)
                        mhtvec = TLorentzVector()
                        mhtvec.SetPtEtaPhiE(c.MHT, 0, c.MHTPhi, c.MHT)
        
                        appEvent = False
        
                        for ti in range(c.tracks.size()):
                            t = c.tracks[ti]
                            if c.tracks_trkRelIso[ti] > 0.1:
                                continue 
                            if c.tracks_dxyVtx[ti] > 0.02:
                                continue
                            if c.tracks_dzVtx[ti] > 0.02:
                                continue            
            
                            #llMin = analysis_tools.minDeltaR(t, [ll])
            
                            #if (llMin is not None and llMin < 0.01):
                            #    continue
                            
                            if abs(t.DeltaR(ll)) < 0.01:
                                continue
                            
                            clean += 1
                            minZ, minCanZ = analysis_ntuples.minDeltaRGenParticles(t, genZL, c.GenParticles)
                            minNZ, minCanNZ = analysis_ntuples.minDeltaRGenParticles(t, genNonZL, c.GenParticles)
        
                            #if minNZ is None:
                            #	print("minNZ is None for " + str(genNonZL))
            
                            min = None
                            if minNZ is None or minZ < minNZ:
                                min = minZ
                            else:
                                min = minNZ
        
                            result = ""
                        
                            genFlavour = ""
        
                            if min > 0.1:
                                result = "MM"
                            elif minNZ is None or minZ < minNZ:
                                if c.tracks_charge[ti] * c.GenParticles_PdgId[minCanZ] < 0 and (abs(c.GenParticles_PdgId[minCanZ]) == 11 or abs(c.GenParticles_PdgId[minCanZ]) == 13):
                                    genFlavour = "Electrons"
                                    if abs(c.GenParticles_PdgId[minCanZ]) == 13:
                                        genFlavour = "Muons"
                                    result = "Zl"
                                    #print("Found!")
                                else:
                                    result = "MM"
                            else:
                                result = "MM"
        
                            vars[varsDict["track"]]["var"] = t
                            for j, v in enumerate(tracksVars):
                                i = len(otherVars) + j
                                vars[i]["var"][0] = eval("c.tracks_" + vars[i]["name"] + "[" + str(ti) + "]")
                            if ll is not None:
                                vars[varsDict["deltaEtaLL"]]["var"][0] = abs(t.Eta()-ll.Eta()) 
                                vars[varsDict["deltaRLL"]]["var"][0] = abs(t.DeltaR(ll))
                                vars[varsDict["invMass"]]["var"][0] = (ll + t).M()
                                vars[varsDict["deltaPhiLL"]]["var"][0] = t.DeltaPhi(ll)
                                if (ll + t).M() < 0:
                                    print("Negative invMass continue", (ll + t).M())
                                    continue
                            else:
                                ll = TLorentzVector()
                                vars[varsDict["deltaEtaLL"]]["var"][0] = -1 
                                vars[varsDict["deltaRLL"]]["var"][0] = -1
                                vars[varsDict["invMass"]]["var"][0] = -1
                                vars[varsDict["deltaPhiLL"]]["var"][0] = -1
                            vars[varsDict["deltaEtaLJ"]]["var"][0] = abs(t.Eta() - c.LeadingJet.Eta())
                            vars[varsDict["deltaRLJ"]]["var"][0] = abs(t.DeltaR(c.LeadingJet))
                            vars[varsDict["mtt"]]["var"][0] = analysis_tools.MT2(c.MET, c.METPhi, t)
                            vars[varsDict["deltaPhiMet"]]["var"][0] = abs(t.DeltaPhi(metvec))
                            vars[varsDict["deltaPhiMht"]]["var"][0] = abs(t.DeltaPhi(mhtvec))
                            vars[varsDict["lepton"]]["var"] = ll
                        
                            tree = None
                            if result == "Zl":
                                
                                if postfix != analysis_selections.jetIsos[genFlavour]:
                                    continue
                                
                                tree = signalTrees[genFlavour + postfix]
                                
                                sigTrack += 1
                                #print("Pt=" + str(vars[varsDict["track"]]["var"].Pt()))
                            else:
                                
                                tree = bgTrees[postfix]
        
                            tree.SetBranchAddress('track', vars[varsDict["track"]]["var"])
                            tree.SetBranchAddress('lepton', vars[varsDict["lepton"]]["var"])
                            tree.Fill()

    print("notCorrect=" + str(notCorrect))
    print("afterAtLeastOneReco=" + str(afterAtLeastOneReco))
    print("clean=" + str(clean))
    print("noReco=" + str(noReco))
    print("sigTrack=" + str(sigTrack))

    fnew = TFile(output_file + "_sig.root",'recreate')
    for lep in ["Electrons", "Muons"]:
        for iso in utils.leptonIsolationList:
            for cat in utils.leptonIsolationCategories:
                ptRanges = [""]
                drCuts = [""]
                if iso in ["CorrJetIso", "CorrJetNoMultIso"]:
                    ptRanges = utils.leptonCorrJetIsoPtRange
                    drCuts = utils.leptonCorrJetIsoDrCuts
                for ptRange in ptRanges:
                    for drCut in drCuts:
                        cuts = ""
                        if len(str(ptRange)) > 0:
                            cuts = str(ptRange) + "Dr" + str(drCut)
                        postfix = iso + cuts + cat
                        
                        if postfix != analysis_selections.jetIsos[lep]:
                            continue
                        
                        signalTrees[lep + postfix].Write()
                    
    fnew.Close()

    fnew = TFile(output_file + "_bg.root",'recreate')
    for iso in utils.leptonIsolationList:
        for cat in utils.leptonIsolationCategories:
            ptRanges = [""]
            drCuts = [""]
            if iso in ["CorrJetIso", "CorrJetNoMultIso"]:
                ptRanges = utils.leptonCorrJetIsoPtRange
                drCuts = utils.leptonCorrJetIsoDrCuts
            for ptRange in ptRanges:
                for drCut in drCuts:
                    cuts = ""
                    if len(str(ptRange)) > 0:
                        cuts = str(ptRange) + "Dr" + str(drCut)
                    postfix = iso + cuts + cat
                    if postfix not in  [analysis_selections.jetIsos["Muons"], analysis_selections.jetIsos["Electrons"]]:
                        continue
                    bgTrees[postfix].Write()
    fnew.Close()
    
    print("Done writing")
        
main()
exit(0)




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
from lib import analysis_observables
from lib import analysis_tools
from lib import utils

gSystem.Load('LumiSectMap_C')
from ROOT import LumiSectMap

gSystem.Load('LeptonCollectionMap_C')
from ROOT import LeptonCollectionMap
from ROOT import LeptonCollectionFilesMap
from ROOT import LeptonCollection

parser = argparse.ArgumentParser(description='Create skims for x1x2x1 process.')
parser.add_argument('-i', '--input_file', nargs=1, help='Input Filename', required=False)
parser.add_argument('-o', '--output_file', nargs=1, help='Output Filename', required=False)
parser.add_argument('-s', '--signal', dest='signal', help='Signal', action='store_true')
parser.add_argument('-bg', '--background', dest='bg', help='Background', action='store_true')
parser.add_argument('-data', '--data', dest='data', help='Data', action='store_true')
parser.add_argument('-master', '--master', dest='master', help='Master', action='store_true')
parser.add_argument('-sam', '--sam', dest='sam', help='Sam Samples', action='store_true')
parser.add_argument('-skim', '--skim', dest='skim', help='Skim', action='store_true')
parser.add_argument('-z_peak', '--z_peak', dest='z_peak', help='Skim', action='store_true')
parser.add_argument('-jpsi_single_electron', '--jpsi_single_electron', dest='single_electron', help='Single Electron Stream', action='store_true')
args = parser.parse_args()

input_file = None
if args.input_file:
    input_file = args.input_file[0].strip()
output_file = None
if args.output_file:
    output_file = args.output_file[0].strip()

signal = args.signal
bg = args.bg
data = args.data
sam = args.sam
z_peak = args.z_peak 
single_electron = args.single_electron

if (bg and signal):
    signal = True
    bg = False

replace_lepton_collection = True
if signal:
    replace_lepton_collection = False

######## END OF CMDLINE ARGUMENTS ########

calcDiObsDef = {
    "invMass" : "double",
    "dileptonPt" : "double",
    "deltaPhi" : "double",
    "deltaEta" : "double",
    "deltaR" : "double",
    "tagMuon" : "int",
    "probeTrack" : "int",
    "tracks_mi" : "int",
    "tracks_ei" : "int",
    "Muons_ti" : "int",
    "tagJpsi" : "int",
    "probeJpsi" : "int",
    "tagZ" : "int",
    "probeZ" : "int"
}

extraObsDef = {
    "passedSingleMuPack" : "bool",
    "passedSingleElectronPack" : "bool"
}


def main():

    import os
    from lib import utils
    
    #### COMMON FLAT OBS ####
    
    extraObs = {}
    for extraOb in extraObsDef:
        extraObs[extraOb] = np.zeros(1,dtype=eval(extraObsDef[extraOb]))
    
    flatObs = {}
    for flatOb in analysis_observables.commonFlatObs:
        flatObs[flatOb] = np.zeros(1,dtype=eval(analysis_observables.commonFlatObs[flatOb]))
    
    bgFlatObs = {}
    for bgFlatOb in analysis_observables.bgFlatObs:
        bgFlatObs[bgFlatOb] = np.zeros(1,dtype=eval(analysis_observables.bgFlatObs[bgFlatOb]))
    
    filtersObs = {}
    for filtersOb in analysis_observables.filtersObs:
        filtersObs[filtersOb] = np.zeros(1,dtype=eval(analysis_observables.filtersObs[filtersOb]))
    
    #### TRACKS ####
    trackObs = {}
    
    for tracksOb in analysis_observables.tracksObs:
        trackObs[tracksOb] = ROOT.std.vector(eval(analysis_observables.tracksObs[tracksOb]))()
    
    # pionsObs = {}
#     for pionsOb in analysis_ntuples.pionsObs:
#         pionsObs[pionsOb] = ROOT.std.vector(eval(analysis_ntuples.pionsObs[pionsOb]))()
#         
#     photonObs = {}
#     for photonOb in analysis_ntuples.photonObs:
#         photonObs[photonOb] = ROOT.std.vector(eval(analysis_ntuples.photonObs[photonOb]))()
#     
    ### LEPTONS ###
    
    electronsObs = {}
    for electronsOb in analysis_observables.electronsObs:
        electronsObs[electronsOb] = ROOT.std.vector(eval(analysis_observables.electronsObs[electronsOb]))()

    muonsObs = {}
    for muonsOb in analysis_observables.muonsObs:
        muonsObs[muonsOb] = ROOT.std.vector(eval(analysis_observables.muonsObs[muonsOb]))()
    
    
    electronsCalcObs = {}
    for electronsCalcOb in analysis_observables.electronsCalcObs:
        electronsCalcObs[electronsCalcOb] = ROOT.std.vector(eval(analysis_observables.electronsCalcObs[electronsCalcOb]))()

    muonsCalcObs = {}
    for muonsCalcOb in analysis_observables.muonsCalcObs:
        muonsCalcObs[muonsCalcOb] = ROOT.std.vector(eval(analysis_observables.muonsCalcObs[muonsCalcOb]))()

        
    origMuonsObs = {}
    for muonsOb in analysis_observables.origMuonsObs:
        origMuonsObs[muonsOb] = ROOT.std.vector(eval(analysis_observables.origMuonsObs[muonsOb]))()
        
    ### GEN PARTICLES ###

    genParticlesObs = {}
    for genParticlesOb in analysis_observables.genParticlesObs:
        genParticlesObs[genParticlesOb] = ROOT.std.vector(eval(analysis_observables.genParticlesObs[genParticlesOb]))()
    
    ### JETS ###
    
    jetsObs = {}
    for jetsOb in analysis_observables.jetsObs:
        jetsObs[jetsOb] = ROOT.std.vector(eval(analysis_observables.jetsObs[jetsOb]))()
    
    ### TRIGGER ###
    
    triggerObs = {}
    for triggerOb in analysis_observables.triggerObs:
        triggerObs[triggerOb] = ROOT.std.vector(eval(analysis_observables.triggerObs[triggerOb]))()
    
    
    calcDiObs = {}
    for calcDiOb in calcDiObsDef:
        calcDiObs[calcDiOb] = ROOT.std.vector(eval(calcDiObsDef[calcDiOb]))()
  
    #### BRANCH ####
    
    tEvent = TTree('tEvent','tEvent')
    
    for extraOb in extraObsDef:
        #extraObs[extraOb] = np.zeros(1,dtype=eval(extraObsDef[extraOb]))
        tEvent.Branch(extraOb, extraObs[extraOb],extraOb + "/" + utils.typeTranslation[extraObsDef[extraOb]])
    
    for flatOb in analysis_observables.commonFlatObs:
        print("tEvent.Branch(" + flatOb + "," +  "flatObs[flatOb]" + "," + flatOb + "/" + utils.typeTranslation[analysis_observables.commonFlatObs[flatOb]] + ")")
        tEvent.Branch(flatOb, flatObs[flatOb],flatOb + "/" + utils.typeTranslation[analysis_observables.commonFlatObs[flatOb]])
    
    if bg:
        for bgFlatOb in analysis_observables.bgFlatObs:
            tEvent.Branch(bgFlatOb, bgFlatObs[bgFlatOb],bgFlatOb + "/" + utils.typeTranslation[analysis_observables.bgFlatObs[bgFlatOb]])
    
    for filtersOb in analysis_observables.filtersObs:
        tEvent.Branch(filtersOb, filtersObs[filtersOb],filtersOb + "/" + utils.typeTranslation[analysis_observables.filtersObs[filtersOb]])
    
    for tracksOb in analysis_observables.tracksObs:
        tEvent.Branch(tracksOb, 'std::vector<' + analysis_observables.tracksObs[tracksOb] + '>', trackObs[tracksOb])
    
    # for pionsOb in analysis_ntuples.pionsObs:
#         tEvent.Branch(pionsOb, 'std::vector<' + analysis_ntuples.pionsObs[pionsOb] + '>', pionsObs[pionsOb])
#         
#     for photonOb in analysis_ntuples.photonObs:
#         tEvent.Branch(photonOb, 'std::vector<' + analysis_ntuples.photonObs[photonOb] + '>', photonObs[photonOb])
#     
    for electronsOb in analysis_observables.electronsObs:
        tEvent.Branch(electronsOb, 'std::vector<' + analysis_observables.electronsObs[electronsOb] + '>', electronsObs[electronsOb])
    
    for muonsOb in analysis_observables.muonsObs:
        tEvent.Branch(muonsOb, 'std::vector<' + analysis_observables.muonsObs[muonsOb] + '>', muonsObs[muonsOb])
    
    for muonsOb in analysis_observables.origMuonsObs:
        tEvent.Branch(muonsOb, 'std::vector<' + analysis_observables.origMuonsObs[muonsOb] + '>', origMuonsObs[muonsOb])
    
    if not data:
        for genParticlesOb in analysis_observables.genParticlesObs:
            tEvent.Branch(genParticlesOb, 'std::vector<' + analysis_observables.genParticlesObs[genParticlesOb] + '>', genParticlesObs[genParticlesOb])
    
    for jetsOb in analysis_observables.jetsObs:
        tEvent.Branch(jetsOb, 'std::vector<' + analysis_observables.jetsObs[jetsOb] + '>', jetsObs[jetsOb])
    
    for triggerOb in analysis_observables.triggerObs:
        tEvent.Branch(triggerOb, 'std::vector<' + analysis_observables.triggerObs[triggerOb] + '>', triggerObs[triggerOb])
    
    for calcDiOb in calcDiObsDef:
        tEvent.Branch(calcDiOb, 'std::vector<' + calcDiObsDef[calcDiOb] + '>', calcDiObs[calcDiOb])
    
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
                print("tEvent.Branch(" + lep + "_pass" + CorrJetObs + str(ptRange), 'std::vector<' + str(utils.leptonsCorrJetVecList[CorrJetObs]) + '>', leptonsCorrJetVars[lep + "_pass" + CorrJetObs + str(ptRange)], ")")
                tEvent.Branch(lep + "_pass" +  CorrJetObs + str(ptRange), 'std::vector<' + utils.leptonsCorrJetVecList[CorrJetObs] + '>', leptonsCorrJetVars[lep + "_pass" + CorrJetObs + str(ptRange)])
    
    
    #### END OF TREE PREP ####
    
    baseFileName = os.path.basename(input_file)
    
    c = TChain('TreeMaker2/PreSelection')
    print("Opening", input_file)
    c.Add(input_file)
    #c = chain.CloneTree()
    #chain = None
    print("Creating " + output_file)
    fnew = TFile(output_file,'recreate')
    print("Created.")

    hHt = TH1F('hHt','hHt',1,0,1)
    hHtAfterMadHt = TH1F('hHtAfterMadHt','hHtAfterMadHt',1,0,1)
    
    lumiSecs = LumiSectMap()
    
    currLeptonCollectionMap = None
    currLeptonCollectionFileMapFile = None
    
    nentries = c.GetEntries()
    print('Analysing', nentries, "entries")
    
    print("Starting Loop")
    
    passedEvents = 0
    passedJPsi = 0
    
    for ientry in range(nentries):
        if ientry % 1000 == 0:
            print("Processing " + str(ientry))
        c.GetEntry(ientry)
        
        ### MADHT ###
        rightProcess = True
        if bg:
            rightProcess = utils.madHtCheck(baseFileName, c.madHT)
        elif data:
            lumiSecs.insert(c.RunNum, c.LumiBlockNum)

        hHt.Fill(c.HT)

        if not rightProcess:
            continue
        
        if c.tracks.size() < 1:
            continue
        
        if single_electron:
            highPtJpsiElectron = analysis_ntuples.hasHighPtJpsiElectron(27, c.Electrons)
            if highPtJpsiElectron is None:
                continue
        else:
            highPtJpsiMuon = analysis_ntuples.hasHighPtJpsiMuon(24, c.Muons, c.Muons_passIso, c.Muons_tightID)
            if highPtJpsiMuon is None:
                continue

        # print("c.tracks[0].X()", c.tracks[0].X(), "c.tracks[0].Y()", c.tracks[0].Y(), "c.tracks[0].Z()", c.tracks[0].Z(), "c.tracks[0].M()", c.tracks[0].M())
#         print("c.tracks[0].Pt()", c.tracks[0].Pt(), "c.tracks[0].Eta()", c.tracks[0].Eta(), "c.tracks[0].Phi()", c.tracks[0].Phi())
#         new = TLorentzVector()
#         new.SetXYZM(c.tracks[0].X(), c.tracks[0].Y(), c.tracks[0].Z(), 0.1057)
#         
#         print("new.X()", new.X(), "new.Y()", new.Y(), "new.Z()", new.Z(), "new.M()", new.M())
#         print("new.Pt()", new.Pt(), "new.Eta()", new.Eta(), "new.Phi()", new.Phi())
#         
#         exit(0)
#         
#         c.tracks[0]
        
        passedEvents += 1
        
        hHtAfterMadHt.Fill(c.HT)
        
        #### FILL IN ####
        
        for flatOb in flatObs:
            flatObs[flatOb][0] = getattr(c, flatOb)
        
        if bg:
            for bgFlatOb in analysis_observables.bgFlatObs:
                bgFlatObs[bgFlatOb][0] = getattr(c, bgFlatOb)
        
        for filtersOb in filtersObs:
            filtersObs[filtersOb][0] = getattr(c, filtersOb)
        
        for tracksOb in analysis_observables.tracksObs:
            trackObs[tracksOb] = getattr(c, tracksOb)
        
        # for pionsOb in analysis_ntuples.pionsObs:
#             pionsObs[pionsOb] = getattr(c, pionsOb)
#         
#         for photonOb in analysis_ntuples.photonObs:
#             photonObs[photonOb] = getattr(c, photonOb
    
        origMuonsObs["Muons_orig"] = c.Muons
        
        #### GET LOW LEPTONS ####
        
        takeLeptonsFrom = None
        
        #replace_lepton_collection = False
        
        if replace_lepton_collection:
            if currLeptonCollectionMap is None or not currLeptonCollectionMap.contains(c.RunNum, c.LumiBlockNum, c.EvtNum):
                print("NEED NEW LEPTON COLLECTION...")
                if currLeptonCollectionMap is not None:
                    currLeptonCollectionMap.Delete()
                    currLeptonCollectionMap = None
                currLeptonCollection = None
                currLeptonCollectionFileMapFile = utils.getLeptonCollectionFileMapFile(baseFileName)
                if currLeptonCollectionFileMapFile is None:
                    print("FATAL: could not open LeptonCollectionFileMapFile")
                    exit(1)
                print("currLeptonCollectionFileMapFile", currLeptonCollectionFileMapFile)
                currLeptonCollectionFileMap = utils.getLeptonCollectionFileMap(currLeptonCollectionFileMapFile, c.RunNum, c.LumiBlockNum, c.EvtNum)
                print("Got currLeptonCollectionFileMap")
                if currLeptonCollectionFileMap is None:
                    print("FATAL: could not find file map. continuing...")
                    exit(1) 
                currLeptonCollectionFileName = currLeptonCollectionFileMap.get(c.RunNum, c.LumiBlockNum, c.EvtNum)
                currLeptonCollectionFileMap.Delete()
                currLeptonCollectionFileMap = None
                print("currLeptonCollectionFileName=", currLeptonCollectionFileName)
                
                currLeptonCollectionMap = utils.getLeptonCollection(currLeptonCollectionFileName)
                print("currLeptonCollectionMap=", currLeptonCollectionMap)
                currLeptonCollectionFileMapFile.Close()
            
            if currLeptonCollectionMap is None:
                print("FATAL: could not find lepton map for ",c.RunNum, c.LumiBlockNum, c.EvtNum, " continuing...")
                exit(1)
            
            takeLeptonsFrom = currLeptonCollectionMap.get(c.RunNum, c.LumiBlockNum, c.EvtNum)
        else:
            takeLeptonsFrom = c
        
        for electronsOb in analysis_observables.electronsObs:
            electronsObs[electronsOb] = getattr(takeLeptonsFrom, electronsOb)
        
        for muonsOb in analysis_observables.muonsObs:
            muonsObs[muonsOb] = getattr(takeLeptonsFrom, muonsOb)
        
        if not data:
        
            for genParticlesOb in analysis_observables.genParticlesObs:
                genParticlesObs[genParticlesOb] = getattr(c, genParticlesOb)
        
        for jetsOb in analysis_observables.jetsObs:
            jetsObs[jetsOb] = getattr(c, jetsOb)
        
        for triggerOb in analysis_observables.triggerObs:
            triggerObs[triggerOb] = getattr(c, triggerOb)
        
        #### SET ADDRESS ####
        
        for tracksOb in analysis_observables.tracksObs:
            tEvent.SetBranchAddress(tracksOb, trackObs[tracksOb])
        
        # for pionsOb in analysis_ntuples.pionsObs:
#             tEvent.SetBranchAddress(pionsOb, pionsObs[pionsOb])
#         
#         for photonOb in analysis_ntuples.photonObs:
#             tEvent.SetBranchAddress(photonOb, photonObs[photonOb])
#         
        for electronsOb in analysis_observables.electronsObs:
            tEvent.SetBranchAddress(electronsOb, electronsObs[electronsOb])
        
        for muonsOb in analysis_observables.muonsObs:
            tEvent.SetBranchAddress(muonsOb, muonsObs[muonsOb])
        
        for muonsOb in analysis_observables.origMuonsObs:
            tEvent.SetBranchAddress(muonsOb, origMuonsObs[muonsOb])
        
        if not data:
            for genParticlesOb in analysis_observables.genParticlesObs:
                tEvent.SetBranchAddress(genParticlesOb, genParticlesObs[genParticlesOb])
        
        for jetsOb in analysis_observables.jetsObs:
            tEvent.SetBranchAddress(jetsOb, jetsObs[jetsOb])
        
        for triggerOb in analysis_observables.triggerObs:
            tEvent.SetBranchAddress(triggerOb, triggerObs[triggerOb])
        
        ### JPSI STUFF ###
        
        for calcDiOb in calcDiObsDef:
            calcDiObs[calcDiOb] = ROOT.std.vector(eval(calcDiObsDef[calcDiOb]))()
        
        foundJpsi = False
        
        for i in range(len(muonsObs["Muons"])):
            if not analysis_ntuples.isleptonPassesJpsiTagSelection(i, 5, muonsObs["Muons"], muonsObs["Muons_passIso"], muonsObs["Muons_mediumID"]):
                continue
            for j in range(len(trackObs["tracks"])):
                if z_peak:
                    if not analysis_ntuples.isTrackPassesProbeJpsiSelection(i, j, 2, 25, muonsObs["Muons"], muonsObs["Muons_charge"], trackObs["tracks"], trackObs["tracks_charge"], 60, 120):
                        continue
                elif not analysis_ntuples.isTrackPassesProbeJpsiSelection(i, j, 2, 25, muonsObs["Muons"], muonsObs["Muons_charge"], trackObs["tracks"], trackObs["tracks_charge"]):
                    continue
                
                foundJpsi = True
                
                #print("foundJpsi!!!")
                
                calcDiObs["tagMuon"].push_back(i)
                calcDiObs["probeTrack"].push_back(j)
                
                mTrack = TLorentzVector()
                track = trackObs["tracks"][j]
                mTrack.SetXYZM(track.X(), track.Y(), track.Z(), 0.1057)
                muon = muonsObs["Muons"][i]
                
                invMass = (mTrack + muon).M()
                #print("From outside: invMass", invMass)
                #print("---")
                
                calcDiObs["invMass"].push_back(invMass)
                calcDiObs["dileptonPt"].push_back(abs((mTrack + muon).Pt()))
                calcDiObs["deltaPhi"].push_back(abs(mTrack.DeltaPhi(muon)))
                calcDiObs["deltaEta"].push_back(abs(mTrack.Eta() - muon.Eta()))
                calcDiObs["deltaR"].push_back(abs(mTrack.DeltaR(muon)))
                
                if not data:
                    min, minCan = analysis_ntuples.minDeltaLepLeps(muon, c.GenParticles)
                    if min is None or min > 0.01:
                        calcDiObs["tagJpsi"].push_back(0)
                    else:
                        pdgId = c.GenParticles_ParentId[minCan]
                        if pdgId == 443:
                            calcDiObs["tagJpsi"].push_back(1)
                        else:
                            calcDiObs["tagJpsi"].push_back(0)
                        if pdgId == 23:
                            calcDiObs["tagZ"].push_back(1)
                        else:
                            calcDiObs["tagZ"].push_back(0)
                
                    min, minCan = analysis_ntuples.minDeltaLepLeps(track, c.GenParticles)
                    if min is None or min > 0.01:
                        calcDiObs["probeJpsi"].push_back(0)
                    else:
                        pdgId = c.GenParticles_ParentId[minCan]
                        if pdgId == 443:
                            calcDiObs["probeJpsi"].push_back(1)
                        else:
                            calcDiObs["probeJpsi"].push_back(0)
                        if pdgId == 23:
                            calcDiObs["probeZ"].push_back(1)
                        else:
                            calcDiObs["probeZ"].push_back(0)
                

        if not foundJpsi:
            continue
        
        passedJPsi += 1
        
        #print("passedJPsi", passedJPsi)
        
        for i in range(len(trackObs["tracks"])):
            t = trackObs["tracks"][i]
            
            min, minCan = analysis_ntuples.minDeltaLepLeps(trackObs["tracks"][i], electronsObs["Electrons"])
            if min is None or min > 0.01 or electronsObs["Electrons_charge"][minCan] * trackObs["tracks_charge"][i] < 0:
                calcDiObs["tracks_ei"].push_back(-1)
            else:
                calcDiObs["tracks_ei"].push_back(minCan)
            
            min, minCan = analysis_ntuples.minDeltaLepLeps(trackObs["tracks"][i], muonsObs["Muons"])
            if min is None or min > 0.01 or muonsObs["Muons_charge"][minCan] * trackObs["tracks_charge"][i] < 0:
                calcDiObs["tracks_mi"].push_back(-1)
            else:
                calcDiObs["tracks_mi"].push_back(minCan)
        
        for i in range(muonsObs["Muons"].size()):
            min, minCan = analysis_ntuples.minDeltaLepLeps(muonsObs["Muons"][i], trackObs["tracks"])
            if min is None or min > 0.01 or trackObs["tracks_charge"][minCan] * muonsObs["Muons_charge"][i] < 0:
                calcDiObs["Muons_ti"].push_back(-1)
            else:
                calcDiObs["Muons_ti"].push_back(minCan)
        
        for calcDiOb in calcDiObsDef:
            #print("tEvent.SetBranchAddress(" + calcDiOb + ", " + str(calcDiObs[calcDiOb]) + ")")
            tEvent.SetBranchAddress(calcDiOb, calcDiObs[calcDiOb])
        
        if data:
            ## Whatever
            extraObs["passedSingleMuPack"][0] = analysis_ntuples.passTrig(c, "SingleMuon")
            extraObs["passedSingleElectronPack"][0] = analysis_ntuples.passTrig(c, "SingleElectron")
        else:
            extraObs["passedSingleMuPack"][0] = True
            extraObs["passedSingleElectronPack"][0] = True
        
        ### JET ISOLATION ####
        
        for electronsCalcOb in analysis_observables.electronsCalcObs:
            electronsCalcObs[electronsCalcOb] = ROOT.std.vector(eval(analysis_observables.electronsCalcObs[electronsCalcOb]))()
        
        for muonsCalcOb in analysis_observables.muonsCalcObs:
            muonsCalcObs[muonsCalcOb] = ROOT.std.vector(eval(analysis_observables.muonsCalcObs[muonsCalcOb]))()
        
        for i in range(electronsObs["Electrons"].size()):
            #electronsCalcObs["Electrons_deltaRLJ"].push_back(electronsObs["Electrons"][i].DeltaR(var_LeadingJet))
            electronsCalcObs["Electrons_deltaRLJ"].push_back(-1)
           # electronsCalcObs["Electrons_deltaPhiLJ"].push_back(abs(electronsObs["Electrons"][i].DeltaPhi(var_LeadingJet)))
           # electronsCalcObs["Electrons_deltaEtaLJ"].push_back(abs(electronsObs["Electrons"][i].Eta() - var_LeadingJet.Eta()))
            min, minCan = analysis_ntuples.minDeltaLepLeps(electronsObs["Electrons"][i], trackObs["tracks"])
            if min is None or min > 0.01 or trackObs["tracks_charge"][minCan] * electronsObs["Electrons_charge"][i] < 0:
                electronsCalcObs["Electrons_ti"].push_back(-1)
            else:
                electronsCalcObs["Electrons_ti"].push_back(minCan)
            
        for i in range(muonsObs["Muons"].size()):
            #muonsCalcObs["Muons_deltaRLJ"].push_back(muonsObs["Muons"][i].DeltaR(var_LeadingJet))
            muonsCalcObs["Muons_deltaRLJ"].push_back(-1)
           # muonsCalcObs["Muons_deltaPhiLJ"].push_back(abs(muonsObs["Muons"][i].DeltaPhi(var_LeadingJet)))
           # muonsCalcObs["Muons_deltaEtaLJ"].push_back(abs(muonsObs["Muons"][i].Eta() - var_LeadingJet.Eta()))
            min, minCan = analysis_ntuples.minDeltaLepLeps(muonsObs["Muons"][i], trackObs["tracks"])
            if min is None or min > 0.01 or trackObs["tracks_charge"][minCan] * muonsObs["Muons_charge"][i] < 0:
                muonsCalcObs["Muons_ti"].push_back(-1)
            else:
                muonsCalcObs["Muons_ti"].push_back(minCan)
        
        
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
                    isoJets[lep][lepIso] = [ c.Jets[j] for j in range(len(c.Jets)) ]# if c.Jets[j].Pt() > 25 ]
        
        for lep in isoJets:

            leptonsVecName = isoJets[lep]["obs"]
            leptonsVec = eval(leptonsVecName.lower() + "Obs")[leptonsVecName]
            
            for i in range(leptonsVec.size()):
                leptonsCorrJetVars[isoJets[lep]["obs"] + "_passNoIso"].push_back(True)
                min, minCan = analysis_ntuples.minDeltaLepLeps(leptonsVec[i], c.Jets)
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
                    #min, minCan = analysis_ntuples.minDeltaLepLeps(leptonsVec[i], c.Jets)
                    #if min is None or min > 0.4:
                    #    leptonsCorrJetVars[isoJets[lep]["obs"] + "_passNonJetIso"].push_back(True)
                    #else:
                    #    leptonsCorrJetVars[isoJets[lep]["obs"] + "_passNonJetIso"].push_back(False)
        
        var_Jets_muonCorrected = ROOT.std.vector(TLorentzVector)(c.Jets)
        var_Jets_electronCorrected = ROOT.std.vector(TLorentzVector)(c.Jets)
        
        non_iso_jet_electrons = [ i for i in range(len(electronsObs["Electrons"])) if electronsCalcObs["Electrons_minDeltaRJets"][i] >= 0 and electronsCalcObs["Electrons_minDeltaRJets"][i] < 0.4 ]
        non_iso_jet_muons = [ i for i in range(len(muonsObs["Muons"])) if analysis_ntuples.muonPassesJetIsoSelection(i, muonsObs["Muons"], muonsObs["Muons_mediumID"]) and muonsCalcObs["Muons_minDeltaRJets"][i] >= 0 and muonsCalcObs["Muons_minDeltaRJets"][i] < 0.4 ]
        
        for i in non_iso_jet_electrons:
            for j in range(len(var_Jets_electronCorrected)):
                if var_Jets_electronCorrected[j].DeltaR(electronsObs["Electrons"][i]) < 0.4:
                    var_Jets_electronCorrected[j] -= electronsObs["Electrons"][i]
        for i in non_iso_jet_muons:
            for j in range(len(var_Jets_muonCorrected)):
                if var_Jets_muonCorrected[j].DeltaR(muonsObs["Muons"][i]) < 0.4:
                    var_Jets_muonCorrected[j] -= muonsObs["Muons"][i]
        
        for lepIso in utils.leptonIsolationList:
            for lep in isoJets:
                if lepIso != "CorrJetIso":
                    continue
                for ptRange in utils.leptonCorrJetIsoPtRange:
                    isoJets[lep][str(ptRange)] = [eval("var_Jets_" + lep + "Corrected")[j] for j in range(len(eval("var_Jets_" + lep + "Corrected"))) if c.Jets_multiplicity[j] >=10 or (eval("var_Jets_" + lep + "Corrected")[j].E() > 0 and eval("var_Jets_" + lep + "Corrected")[j].Pt() > ptRange)]
          
        for lep in isoJets:
             
            leptonsVecName = isoJets[lep]["obs"]
            leptonsVec = eval(leptonsVecName.lower() + "Obs")[leptonsVecName]
            
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
    
    fnew.cd()
    
    tEvent.Write()
    hHt.Write()
    hHtAfterMadHt.Write()
    if data:
        lumiSecs.Write("lumiSecs")
    print('just created', fnew.GetName())
    print("passedEvents", passedEvents)
    print("passedJPsi", passedJPsi)
    fnew.Close()
        
        
main()


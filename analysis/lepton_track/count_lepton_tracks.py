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
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes"))
from lib import histograms
from lib import cuts
from lib import analysis_ntuples
from lib import analysis_tools
from lib import utils
from lib import cut_optimisation

gROOT.SetBatch(1)

gSystem.Load('LumiSectMap_C')
from ROOT import LumiSectMap

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Plot Track Observeables.')
parser.add_argument('-i', '--input_file', nargs=1, help='Input Filename', required=False)
parser.add_argument('-o', '--output_file', nargs=1, help='Output Filename', required=False)
parser.add_argument('-log', '--log', dest='log', help='Log Scale', action='store_true')
parser.add_argument('-mm', '--mm', dest='mm', help='Miss match only', action='store_true')
parser.add_argument('-rm', '--rm', dest='rm', help='Remove matched tracks', action='store_true')
args = parser.parse_args()

input_file = None
output_file = None
track_bdt = None
if args.input_file:
    input_file = args.input_file[0]
else:
    #input_file = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/sum/higgsino_mu100_dm7p39Chi20Chipm.root"
    input_file = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/sum/higgsino_mu100_dm2p51Chi20Chipm.root"
    #input_file = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_signal_bdt/single/higgsino_mu100_dm7p39Chi20Chipm.root"
    #input_file = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_signal_bdt/single/higgsino_mu100_dm12p84Chi20Chipm.root"
    
    #input_file = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_signal_bdt/single/higgsino_mu100_dm2p51Chi20Chipm.root"
    input_file = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_signal_bdt_no_bdt_cut/single/higgsino_mu100_dm2p51Chi20Chipm.root"
    input_file = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_signal_bdt/single/higgsino_mu100_dm1p13Chi20Chipm.root"
    input_file = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_nlp/sum/higgsino_mu100_dm3p28Chi20Chipm.root"
    
    track_bdt = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/lepton_track/cut_optimisation/tmva/dm1"
    #input_file = "/afs/desy.de/user/n/nissanuv/nfs/old_leptons_x1x2x1/signal/skim_dilepton_signal_bdt/single/higgsino_mu100_dm2p51Chi20Chipm.root"
    
    
if args.output_file:
    output_file = args.output_file[0]
else:
    output_file = "tracks.pdf"
logScale = args.log
mm = args.mm
rm = args.rm

mm = True
rm = True

######## END OF CMDLINE ARGUMENTS ########

lepTypes = ["Zl", "NZl", "MM"]

if mm:
    lepTypes = ["Zl", "MM"]

# def minRecDeltaR(l, c):
#     min = None
#     for v in [e for e in c.Electrons] + [m for m in c.Muons]:
#         deltaR = abs(v.DeltaR(l))
#         if min is None or deltaR < min:
#             min = deltaR
#     return min

def track_DeltaR_LJ(c, t, ti):
    nj, btagsDeepMedium, ljet = analysis_ntuples.eventNumberOfJets25Pt2_4Eta_DeepMedium(c.Jets, c.Jets_bJetTagDeepCSVBvsAll)
    return abs(t.DeltaR(c.Jets[ljet]))

def track_DeltaEta_LJ(c, t, ti):
    nj, btagsDeepMedium, ljet = analysis_ntuples.eventNumberOfJets25Pt2_4Eta_DeepMedium(c.Jets, c.Jets_bJetTagDeepCSVBvsAll)
    return abs(t.Eta() - c.Jets[ljet].Eta())

def track_DeltaR_LL(c, t, ti):
    #ll, leptonIdx, leptonCharge, leptonFlavour = analysis_ntuples.getSingleLeptonAfterSelection(electronsObs["Electrons"], leptonsCorrJetVars["Electrons_pass" + iso + str(ptRange)], electronsCalcObs["Electrons_deltaRLJ"], electronsObs["Electrons_charge"], muonsObs["Muons"], leptonsCorrJetVars["Muons_pass" + iso + str(ptRange)], muonsObs["Muons_mediumID"], muonsCalcObs["Muons_deltaRLJ"], muonsObs["Muons_charge"], utils.leptonIsolationCategories[cat]["muonPt"], utils.leptonIsolationCategories[cat]["lowPtTightMuons"], muonsObs["Muons_tightID"])
    ll, leptonIdx, leptonCharge, leptonFlavour = analysis_ntuples.getSingleLeptonAfterSelection(c.Electrons, c.Electrons_passCorrJetIso10, c.Electrons_deltaRLJ, c.Electrons_charge, c.Muons, c.Muons_passCorrJetIso10, c.Muons_mediumID, c.Muons_deltaRLJ, c.Muons_charge)
    #ll = analysis_ntuples.leadingLepton(c)
    if ll is None:
        return 0
    return abs(t.DeltaR(ll))

def track_DeltaEta_LL(c, t, ti):
    ll, leptonIdx, leptonCharge, leptonFlavour = analysis_ntuples.getSingleLeptonAfterSelection(c.Electrons, c.Electrons_passCorrJetIso10, c.Electrons_deltaRLJ, c.Electrons_charge, c.Muons, c.Muons_passCorrJetIso10, c.Muons_mediumID, c.Muons_deltaRLJ, c.Muons_charge)
    if ll is None:
        return 0
    return abs(t.Eta()-ll.Eta())

def mtt(c, t, ti):
    return analysis_tools.MT2(c.Met, c.METPhi, t)

def deltaRMetTrack(c, t, ti):
    metvec = TLorentzVector()
    metvec.SetPtEtaPhiE(c.Met, 0, c.METPhi, c.Met)
    return abs(t.DeltaR(metvec))

def deltaPhiMetTrack(c, t, ti):
    metvec = TLorentzVector()
    metvec.SetPtEtaPhiE(c.Met, 0, c.METPhi, c.Met)
    return abs(t.DeltaPhi(metvec))

def eta(c, ti):
    return abs(c.tracks[ti].Eta()) < 2.4

def pt(c, ti):
    return abs(c.tracks[ti].Pt()) > 2.5

def dz(c, ti):
    return abs(c.tracks_dzVtx[ti]) < 0.035

def dxy(c, ti):
    return abs(c.tracks_dxyVtx[ti]) < 0.05

def deltaEtaLL(c, ti):
    return track_DeltaEta_LL(c, c.tracks[ti], ti) < 1

def deltaEtaLJ(c, ti):
    return track_DeltaEta_LJ(c, c.tracks[ti], ti) < 3.8

def deltaRLJ(c, ti):
    return track_DeltaR_LJ(c, c.tracks[ti], ti) > 1.8

def deltaRLL(c, ti):
	return track_DeltaR_LL(c, c.tracks[ti], ti) < 1.1

def trackBDT(c, ti):
    return c.trackBDT>0.2

def trackBDTOnly(c, ti):
    return c.trackBDT>0.16

def trackBDTLow(c, ti):
    return c.trackBDT>-0.2

# (track_testBGHists, track_trainBGHists, track_testSignalHists, track_trainSignalHists, track_methods, track_names) = cut_optimisation.get_bdt_hists([track_bdt])
# track_trainSignalHist, track_trainBGHist, track_testSignalHist, track_testBGHist = track_trainSignalHists[0], track_trainBGHists[0], track_testSignalHists[0], track_testBGHists[0]
# track_highestZ, track_highestS, track_highestB, track_highestMVA, track_ST, track_BT = cut_optimisation.getHighestZ(track_trainSignalHist, track_trainBGHist, track_testSignalHist, track_testBGHist)
# 
# track_bdt_weights = track_bdt + "/dataset/weights/TMVAClassification_BDT.weights.xml"
# track_bdt_vars = cut_optimisation.getVariablesFromXMLWeightsFile(track_bdt_weights)
# track_bdt_vars_map = cut_optimisation.getVariablesMemMap(track_bdt_vars)
# 
# track_bdt_weights = track_bdt + "/dataset/weights/TMVAClassification_BDT.weights.xml"
# track_bdt_vars = cut_optimisation.getVariablesFromXMLWeightsFile(track_bdt_weights)
# track_bdt_vars_map = cut_optimisation.getVariablesMemMap(track_bdt_vars)
# track_bdt_specs = cut_optimisation.getSpecSpectatorFromXMLWeightsFile(track_bdt_vars)
# track_bdt_specs_map = cut_optimisation.getSpectatorsMemMap(track_bdt_vars)
# track_bdt_reader = cut_optimisation.prepareReader(track_bdt_weights, track_bdt_vars, track_bdt_vars_map, track_bdt_specs, track_bdt_specs_map)

def allTrackBDT(c, t, ti):
    ll, leptonIdx, leptonCharge, leptonFlavour = analysis_ntuples.getSingleLeptonAfterSelection(c.Electrons, c.Electrons_passCorrJetIso10, c.Electrons_deltaRLJ, c.Electrons_charge, c.Muons, c.Muons_passCorrJetIso10, c.Muons_mediumID, c.Muons_deltaRLJ, c.Muons_charge)
    t = c.tracks[ti]
    metvec = TLorentzVector()
    metvec.SetPtEtaPhiE(c.Met, 0, c.METPhi, c.Met)
    track_bdt_vars_map["deltaEtaLJ"][0] = abs(t.Eta() - c.LeadingJet.Eta())
    track_bdt_vars_map["deltaRLJ"][0] = abs(t.DeltaR(c.LeadingJet))
    track_bdt_vars_map["track.Phi()"][0] = t.Phi()
    track_bdt_vars_map["track.Pt()"][0] = t.Pt()
    track_bdt_vars_map["track.Eta()"][0] = t.Eta()
    
    
    track_bdt_vars_map["deltaEtaLL"][0] = abs(t.Eta()-ll.Eta()) 
    track_bdt_vars_map["deltaRLL"][0] = abs(t.DeltaR(ll))
    track_bdt_vars_map["mtt"][0] = analysis_tools.MT2(c.Met, c.METPhi, t)
    #track_bdt_vars_map["deltaRMet"][0] = abs(t.DeltaR(metvec))
    track_bdt_vars_map["deltaPhiMet"][0] = abs(t.DeltaPhi(metvec))
            
    track_bdt_vars_map["lepton.Eta()"][0] = ll.Eta()
    track_bdt_vars_map["lepton.Phi()"][0] = ll.Phi()
    track_bdt_vars_map["lepton.Pt()"][0] = ll.Pt()
    track_bdt_vars_map["invMass"][0] = (t + ll).M()
    
    for trackVar in ['dxyVtx', 'dzVtx','trkMiniRelIso','trkRelIso']:#, 'trkMiniRelIso', 'trkRelIso']:
        track_bdt_vars_map[trackVar][0] = eval("c.tracks_" + trackVar + "[" + str(ti) + "]")
    
    return track_bdt_reader.EvaluateMVA("BDT")

def passedCut(cut, c, ti):
    for func in cut["funcs"]:
        if not func(c, ti):
            return False
    return True


def main():
    
#     c = TChain('tEvent')
#     print("Going to open the file")
#     print(input_file)
#     c.Add(input_file)
    c= None
    c = TChain('tEvent')
    print("Opening file", input_file)
    c.Add(input_file)
    #c.Add('/nfs/dust/cms/user/beinsam/CommonNtuples/MC_BSM/CompressedHiggsino/M1M2Scan/ntuple_sidecar/higgsino_mu100_dm7.39Chi20Chipm.root')

    nentries = c.GetEntries()
    print('Analysing', nentries, "entries")

    histograms = {}
    memory = []

    objs = ["Gen", "Rec", "Track"]
    funcs = ["Pt", "Phi", "Eta"]
    lepTrackHists = ["LepTypePerRecoBin"]
    lepTrackHistsTitle = ["Lep Type Per Reco Bin"]
    lepTrackHistsMaxX = [5]
    lepTrackHistsBins = [5]

    trackHists = ["Track_DeltaR_LJ", "Track_DeltaEta_LJ", "Track_DeltaR_LL", "Track_DeltaEta_LL", "deltaRMetTrack", "deltaPhiMetTrack", "mtt", "allTrackBDT"]
    trackHists = ["Track_DeltaR_LJ", "Track_DeltaEta_LJ", "Track_DeltaR_LL", "Track_DeltaEta_LL", "deltaRMetTrack", "deltaPhiMetTrack", "mtt"]
    trackHistsFuncs = [track_DeltaR_LJ, track_DeltaEta_LJ, track_DeltaR_LL, track_DeltaEta_LL, deltaRMetTrack, deltaPhiMetTrack, mtt, allTrackBDT]
    trackHistsFuncs = [track_DeltaR_LJ, track_DeltaEta_LJ, track_DeltaR_LL, track_DeltaEta_LL, deltaRMetTrack, deltaPhiMetTrack, mtt]
    trackHistsTitle = ["Delta R Track Leading Jet", "Delta Eta Track Leading Jet", "Delta R Track Leading Lepton", "Delta Eta Track Leading Lepton", "deltaRMetTrack", "deltaPhiMetTrack", "mtt", "allTrackBDT"]
    trackHistsTitle = ["Delta R Track Leading Jet", "Delta Eta Track Leading Jet", "Delta R Track Leading Lepton", "Delta Eta Track Leading Lepton", "deltaRMetTrack", "deltaPhiMetTrack", "mtt"]
    trackHistsMinX = [0,0,0,0,0,0,0,-1]
    trackHistsMaxX = [5,5,5,5,4,4,100,1]
    trackHistsBins = [50,50,50,50,50,50,50,50]

    trackHistsNoType = ["Track_NumIso",  "NM_Track_NumIso"]
    trackHistsTitleNoType = ["Number of Isolated Tracks",  "Number of Non Matched Tracks"]
    trackHistsMaxXNoType = [20, 20]
    trackHistsBinsNoType = [20, 20]

    h2DHists = ["NM_Track_NumIso_Per_Reco", "NM_ZL_Track_NumIso_Per_Reco"]
    h2DHistsTitle = ["Number of Non Matched Tracks Per Reco Bin", "Number of Non Matched Zl Tracks Per Reco Bin"]
    h2DHistsXBins = [5,5]
    h2DHistsXMin = [0,0]
    h2DHistsXMax = [5,5]
    h2DHistsYBins = [5,5]
    h2DHistsYMin = [0,0]
    h2DHistsYMax = [5,5]
    
    maxX = [15, 3.5, 3.5]

    tracksFuncs = ["tracks_trkRelIso", "tracks_chi2perNdof", "tracks_dxyVtx", "tracks_dzVtx", "tracks_trackQualityHighPurity"]
    
    tracksMinX = [-15, 0, 0, -15, -15, 0]
    tracksMaxX = [1, 4, 0.1, 1, 1, 1]
    tracksLogScale = [True, False, True, True, False]

    binNum = 50
    
    eventHistsNoType = ["GenTrackLepMll", "TrackLepMll", "TrackGenLepMll", "GenMll"]
    eventHistsNoTypeTitle = ["GenTrackLepMll", "TrackLepMll", "TrackGenLepMll", "GenMll"]
    eventHistsNoTypeMinX = [0,0,0,0]
    eventHistsNoTypeMaxX = [30,30,30,30]
    eventHistsNoTypeBins = [50,50,50,50]
    
#     eventHists = ["trackBDT", "secondTrackBDT", "TrackLepMllTypes"]
#     eventHistsTitle = ["trackBDT", "secondTrackBDT", "TrackLepMllTypes"]
#     eventHistsMinX = [0,-1,0]
#     eventHistsMaxX = [0.4,1,30]
#     eventHistsBins = [50,50,50]
    
    cuts = [{"name":"", "title": "No Cuts", "funcs":[]},
 #            {"name": "trackBDT", "title": "trackBDT", "funcs":[trackBDT]},
#             {"name": "trackBDTLow", "title": "trackBDTLow", "funcs":[trackBDTLow]},
#             {"name": "trackBDTOnly", "title": "trackBDTOnly", "funcs":[trackBDTOnly]},
            #{"name": "deltaRLL", "title": "deltaRLL", "funcs":[deltaRLL]},
        ]
        #{"name":"Eta_deltaEtaLL", "title": "Eta < 2.6, deltaEtaLL < 1", "funcs":[eta, deltaEtaLL]},
#         {"name":"Eta_deltaEtaLL_deltaEtaLJ", "title": "Eta < 2.6, deltaEtaLL < 1, deltaEtaLJ < 3.8", "funcs":[eta, deltaEtaLL, deltaEtaLJ]},
#         {"name":"Pt_Eta_dxy_dz", "title": "Eta < 2.6, Pt > 2.5, dxy < 0.05, dz < 0.06", "funcs":[eta, pt, dxy, dz]},
#         {"name":"Pt_Eta_dxy_dz_deltaEtaLL", "title": "Eta < 2.6, Pt > 2.5, dxy < 0.05, dz < 0.06, deltaEtaLL < 1", "funcs":[eta, pt, dxy, dz, deltaEtaLL]},
#         {"name":"Pt_Eta_dxy_dz_deltaEtaLL_deltaEtaLJ", "title": "Eta < 2.6, Pt > 2.5, dxy < 0.05, dz < 0.06, deltaEtaLL < 1, deltaEtaLJ < 3.8", "funcs":[eta, pt, dxy, dz, deltaEtaLL, deltaEtaLJ]},
#         {"name":"Pt_Eta_dxy_dz_deltaEtaLL_deltaRLJ", "title": "Eta < 2.6, Pt > 2.5, dxy < 0.05, dz < 0.06, deltaEtaLL < 1, deltaRLJ > 1.8", "funcs":[eta, pt, dxy, dz, deltaEtaLL, deltaRLJ]},
#         {"name":"Pt_Eta_dxy_dz_deltaEtaLL_deltaRLJ_deltaRLL", "title": "Eta < 2.6, Pt > 2.5, dxy < 0.05, dz < 0.06, deltaEtaLL < 1, deltaRLJ > 1.8, deltaRLL < 1.1", "funcs":[eta, pt, dxy, dz, deltaEtaLL, deltaRLJ, deltaRLL]}]
#     
    # for lepType in lepTypes:
#         for h, hist in enumerate(eventHists):
#             for cut in cuts:
#                 tname = hist + "_" + lepType + "_" +  cut["name"]
#                 histograms[tname] = utils.UOFlowTH1F(tname, eventHistsTitle[h], eventHistsBins[h], eventHistsMinX[h], eventHistsMaxX[h])
#     
    for h, hist in enumerate(eventHistsNoType):
        for cut in cuts:
            tname = hist + "_" +  cut["name"]
            histograms[tname] = utils.UOFlowTH1F(tname, eventHistsNoTypeTitle[h], eventHistsNoTypeBins[h], eventHistsNoTypeMinX[h], eventHistsNoTypeMaxX[h])

    for obj in objs:
        for lepType in lepTypes:
            if not mm and obj == "Gen" and lepType == "MM":
                continue
            for h, hists in enumerate([funcs,lepTrackHists]):
                if h == 1 and obj == "Gen":
                    continue
                for i, func in enumerate(hists):
                    name = obj + "_" + lepType + "_" + func
                    if obj == "Track":
                        for cut in cuts:
                            tname = name + "_" + cut["name"]
                            if h == 1:
                                histograms[tname] = utils.UOFlowTH1F(tname, lepTrackHistsTitle[i] + " - " + obj, lepTrackHistsBins[i], 0, lepTrackHistsMaxX[i])
                            else:
                                histograms[tname] = utils.UOFlowTH1F(tname, obj + " " + func, binNum, 0, maxX[i])
                    else:
                        if h == 1:
                            histograms[name] = utils.UOFlowTH1F(name, lepTrackHistsTitle[i] + " - " + obj, lepTrackHistsBins[i], 0, lepTrackHistsMaxX[i])
                        else:
                            histograms[name] = utils.UOFlowTH1F(name, obj + " " + func, binNum, 0, maxX[i])
                                    
    for i, trackHist in enumerate(trackHists):
        for lepType in lepTypes:
            for cut in cuts:
                tname = trackHist + "_" + lepType + "_" + cut["name"]
                histograms[tname] = utils.UOFlowTH1F(tname, trackHistsTitle[i], trackHistsBins[i], trackHistsMinX[i], trackHistsMaxX[i])

    for i, trackHist in enumerate(trackHistsNoType):
        for cut in cuts:
            tname = trackHist + "_" + cut["name"]
            histograms[tname] = utils.UOFlowTH1F(tname, trackHistsTitleNoType[i], trackHistsBinsNoType[i], 0, trackHistsMaxXNoType[i])		

            
    histograms["Lepton_minDealZ"] = utils.UOFlowTH1F("Lepton_minDealZ", "Lepton Min Delta Z", binNum, 0, 0.02)
    histograms["Reco_Num"] = utils.UOFlowTH1F("Reco_Num", "Number of Reco Leptons", 5, 0, 5)

    histograms["Track_minDealZ"] = utils.UOFlowTH1F("Track_minDealZ", "Track Min Delta Z", binNum, 0, 0.2)
    histograms["Track_RelIso"] = utils.UOFlowTH1F("Track_RelIso", "Track RelIso for Delta Z < 0.1", binNum, 0, 0.01)

    for i, hist in enumerate(h2DHists):
        for cut in cuts:
            name = hist + "_" + cut["name"]
            histograms[name] = TH2I(name, h2DHistsTitle[i], h2DHistsXBins[i], h2DHistsXMin[i], h2DHistsXMax[i], h2DHistsYBins[i], h2DHistsYMin[i], h2DHistsYMax[i])

    for i, func in enumerate(tracksFuncs):
        for lepType in lepTypes:
            for cut in cuts:
                name = func + "_" + lepType + "_" + cut["name"]
                if func == "tracks_trackQualityHighPurity":
                    histograms[name] = utils.UOFlowTH1F(name, func, 2, 0, tracksMaxX[i])
                else:
                    histograms[name] = utils.UOFlowTH1F(name, func, binNum, tracksMinX[i], tracksMaxX[i])

    for k, h in histograms.items():
        h.Sumw2()
        h.SetStats(0)
        h.SetMinimum(0.001)
    
    notCorrect = 0
    genFlavour = "Muons"
    genFlavourBefore = 0
    genFlavourAfter = 0
    for ientry in range(nentries):
        if ientry % 5000 == 0:
            print("Processing " + str(ientry))
        c.GetEntry(ientry)
        
        if c.category == 0:
            continue
        
        if c.genFlavour != genFlavour:
            continue
        
        rightProcess = analysis_ntuples.isX1X2X1Process(c)
        if not rightProcess:
            print("No")
            notCorrect += 1
            continue
        
        ll, leptonIdx, leptonCharge, leptonFlavour = analysis_ntuples.getSingleLeptonAfterSelection(c.Electrons, c.Electrons_passCorrJetIso10, c.Electrons_deltaRLJ, c.Electrons_charge, c.Muons, c.Muons_passCorrJetIso10, c.Muons_mediumID, c.Muons_deltaRLJ, c.Muons_charge)
        
        #if ll is None or leptonFlavour != genFlavour:
            #print(ll)
            #print(leptonFlavour, genFlavour)
        #    continue
        if ll is None:
            leptons, leptonsIdx, leptonsCharge, leptonFlavour, same_sign = analysis_ntuples.getTwoLeptonsAfterSelection(c.Electrons, c.Electrons_passCorrJetIso10, c.Electrons_deltaRLJ, c.Electrons_charge, c.Muons, c.Muons_passCorrJetIso10, c.Muons_mediumID, c.Muons_deltaRLJ, c.Muons_charge)
            #if same_sign:
            #    continue
            if leptons is not None:
                ll = leptons[0]
        
        genFlavourBefore += 1
        
        if leptonFlavour != genFlavour:
            print(leptonFlavour, genFlavour)
            continue
        
        genFlavourAfter += 1
        
        
        #recoNum = c.Electrons.size() + c.Muons.size()
        recoNum = 1
        #if recoNum != 1:
        #    continue
            
        #nj, btags, ljet = analysis_ntuples.numberOfJets25Pt2_4Eta_Loose(c)
        #if ljet is None:
        #    continue
    
        genZL, genNonZL = analysis_ntuples.classifyGenZLeptons(c)
        if genZL is None:
            continue
        for li in genZL:
            for func in funcs:
                histograms["Gen_Zl_" + func].Fill(abs(getattr(c.GenParticles[li], func)()))
        for li in genNonZL:
            for func in funcs:
                if mm:
                    histograms["Gen_MM_" + func].Fill(abs(getattr(c.GenParticles[li], func)()))
                else:
                    histograms["Gen_NZl_" + func].Fill(abs(getattr(c.GenParticles[li], func)()))
        histograms["Reco_Num"].Fill(recoNum)
    
    
        for lepVal in [[leptonFlavour, leptonCharge]]:#["Electrons", -11], ["Muons", -13]:
            lepFlavour = lepVal[0]
            lepCharge = lepVal[1]
            pdgid = -11 if leptonFlavour == "Electrons" else -13
            leps = [ll]#getattr(c, lepFlavour)
            for li in range(len(leps)):
                l = leps[li]
                minZ, minCanZ = analysis_ntuples.minDeltaRGenParticles(l, genZL, c.GenParticles)
                minNZ, minCanNZ = analysis_ntuples.minDeltaRGenParticles(l, genNonZL, c.GenParticles)
                min = 0
                if minNZ is None or minZ < minNZ:
                    min = minZ
                else:
                    min = minNZ
                histograms["Lepton_minDealZ"].Fill(min)
                if min > 0.01:
                    #print("No Match")
                    for h, hists in enumerate([funcs,lepTrackHists]):
                        for func in hists:
                            if h == 0:
                                histograms["Rec_MM_" + func].Fill(abs(getattr(l, func)()))
                            elif h == 1:
                                histograms["Rec_MM_" + func].Fill(recoNum)
                    continue
                name = ""
                if minNZ is None or minZ < minNZ:
                    #print("E Z min: " + str(minZ))
                    if c.GenParticles_PdgId[minCanZ] == pdgid * lepCharge:#getattr(c, lepFlavour + "_charge")[li]:
                        name = "Rec_Zl_"
                    else:
                        name = "Rec_MM_"
                else:
                    if c.GenParticles_PdgId[minCanNZ] == pdgid * lepCharge:#getattr(c, lepFlavour + "_charge")[li]:
                        if mm:
                            name = "Rec_MM_"
                        else:
                            name = "Rec_NZl_"
                    else:
                        name = "Rec_MM_"
                for h, hists in enumerate([funcs,lepTrackHists]):
                    for func in hists:
                        if h == 0:
                            histograms[name + func].Fill(abs(getattr(l, func)()))
                        elif h == 1:
                            histograms[name + func].Fill(recoNum)
    
        numIsoTracks = [0] * len(cuts)
        numMMIsoTracks = [0] * len(cuts)
        numMMZlIsoTracks = [0] * len(cuts)
        
        for cut in cuts:
            histograms["GenMll_" + cut["name"]].Fill((c.GenParticles[genZL[0]] + c.GenParticles[genZL[1]]).M())
        #histograms["TrackLepMll"].Fill((ll + c.track).M())
        
        filledOnce = False
        #print("=====")
        for ti in range(c.tracks.size()):
            t = c.tracks[ti]
            
            # if c.track != t:
#                 continue
#             
#             if c.tracks_trkRelIso[ti] > 0.1:
#                 continue 
#             if c.tracks_dxyVtx[ti] > 0.02:
#                 continue
#             if c.tracks_dzVtx[ti] > 0.05:
#                 continue
            
            minRecR = ll.DeltaR(t)

            t = c.tracks[ti]
            tcharge = c.tracks_charge[ti]
            
            if tcharge * leptonCharge > 0:
                continue
            
            if rm and minRecR < 0.01:
                continue
        
            #if abs(t.Eta()) > 0.1:
            #	continue
            minZ, minCanZ = analysis_ntuples.minDeltaRGenParticles(t, genZL, c.GenParticles)
            minNZ, minCanNZ = analysis_ntuples.minDeltaRGenParticles(t, genNonZL, c.GenParticles)
            
            
        
            min = 0
            if minNZ is None or minZ < minNZ:
                min = minZ
            else:
                min = minNZ
            #print("*********")
            #print("Min=" + str(min))
            histograms["Track_minDealZ"].Fill(min)
            if min <= 0.1:
                histograms["Track_RelIso"].Fill(c.tracks_trkRelIso[ti])

            result = ""
        
            if min > 0.01:
                result = "MM"
            elif minNZ is None or minZ < minNZ:
                if c.tracks_charge[ti] * c.GenParticles_PdgId[minCanZ] < 0:
                    result = "Zl"
                    if c.tracks_charge[ti] * leptonCharge < 0:
                        #Opposite charge! Good!
                        for i, cut in enumerate(cuts):
                            #print("Checking cut " + cut["name"])
                            if not passedCut(cut, c, ti):
                                #print("not passed")
                                continue
                            histograms["GenTrackLepMll_" + cut["name"]].Fill((c.tracks[ti] + ll).M())
                else:
                    result = "MM"
            else:
                if c.tracks_charge[ti] * c.GenParticles_PdgId[minCanNZ] < 0:
                    if mm:
                        result = "MM"
                    else:
                        result = "NZl"
                else:
                    result = "MM"
            #if result == "Zl":
            #	print("min=", min, " iso:", c.tracks_trkRelIso[ti])
            
            #if c.track == t:
                #if c.trackBDT < 0.1:
                #    continue
                    
                #if track_DeltaR_LL(c, c.tracks[ti], ti) > 0.9:
                #    continue
                # for i, cut in enumerate(cuts):
#                     if len(cut["name"]) > 0:
#                         #print("Checking cut " + cut["name"])
#                         if not passedCut(cut, c, ti):
#                             #print("not passed")
#                             continue
#                 
#                     if filledOnce:
#                         print("WHAT?!?")
#                         filledOnce = True
#                     histograms["trackBDT" + "_" + result + "_" + cut["name"]].Fill(c.trackBDT)
#                     histograms["TrackLepMllTypes" + "_" + result + "_" + cut["name"]].Fill(c.invMass)
#                     histograms["TrackLepMll" + "_" + cut["name"]].Fill(c.invMass)
# 
#                     if c.tracks_charge[ti] * c.GenParticles_PdgId[genZL[0]] < 0:
#                         #SAME CHARGE - TAKE THE OTHER ONE
#                         histograms["TrackGenLepMll" + "_" + cut["name"]].Fill((t + c.GenParticles[genZL[1]]).M())
#                     else:
#                         histograms["TrackGenLepMll" + "_" + cut["name"]].Fill((t + c.GenParticles[genZL[0]]).M())
            # print("c.secondTrack.Pt()=", c.secondTrack.Pt())
#             print("t.Pt()", t.Pt())
#             print("---")
            # if t == c.secondTrack:
#                 print("SECOND TRACK")
#                 for i, cut in enumerate(cuts):
#                     if len(cut["name"]) > 0:
#                         #print("Checking cut " + cut["name"])
#                         if not passedCut(cut, c, ti):
#                             #print("not passed")
#                             continue
#                     histograms["secondTrackBDT" + "_" + result + "_" + cut["name"]].Fill(c.secondTrackBDT)
                
            
            
            for i, cut in enumerate(cuts):
                if len(cut["name"]) > 0:
                    #print("Checking cut " + cut["name"])
                    if not passedCut(cut, c, ti):
                        #print("not passed")
                        continue
            
                numIsoTracks[i] += 1
                
                # track_bdt_vars_map["deltaEtaLJ"][0] = abs(t.Eta() - c.LeadingJet.Eta())
#                 track_bdt_vars_map["deltaRLJ"][0] = abs(t.DeltaR(c.LeadingJet))
#                 track_bdt_vars_map["track.Phi()"][0] = t.Phi()
#                 track_bdt_vars_map["track.Pt()"][0] = t.Pt()
#                 track_bdt_vars_map["track.Eta()"][0] = t.Eta()
#             
#             
#                 track_bdt_vars_map["deltaEtaLL"][0] = abs(t.Eta()-ll.Eta()) 
#                 track_bdt_vars_map["deltaRLL"][0] = abs(t.DeltaR(ll))
#                 track_bdt_vars_map["mtt"][0] = analysis_tools.MT2(c.Met, c.METPhi, t)
#                 track_bdt_vars_map["deltaRMet"][0] = abs(t.DeltaR(metvec))
#                 track_bdt_vars_map["deltaPhiMet"][0] = abs(t.DeltaPhi(metvec))
#             
#                 for trackVar in ['dxyVtx', 'dzVtx','trkMiniRelIso','trkRelIso']:#, 'trkMiniRelIso', 'trkRelIso']:
#                     track_bdt_vars_map[trackVar][0] = eval("c.tracks_" + trackVar + "[" + str(ti) + "]")
#             
#                 track_tmva_value = track_bdt_reader.EvaluateMVA("BDT")
#                 
#                 histograms["allTrackBDT_" + result + "_" + cut["name"]].Fill(track_tmva_value)
            
                if minRecR is None or minRecR > 0.1:
                    numMMIsoTracks[i] += 1
                    if result == "Zl":
                        numMMZlIsoTracks[i] +=1
            
                for h, hists in enumerate([funcs,lepTrackHists]):
                    for func in hists:
                        name = "Track_" + result + "_" + func + "_" + cut["name"]
                        if h == 0:
                            histograms[name].Fill(abs(getattr(t, func)()))
                        elif h == 1:
                            histograms[name].Fill(recoNum)
                for i, trackHist in enumerate(trackHists):
                    name = trackHist + "_" + result + "_" + cut["name"]
                    if trackHistsFuncs[i] is not None:
                        histograms[name].Fill(trackHistsFuncs[i](c, t, ti))
                for j, func in enumerate(tracksFuncs):
                    name = func + "_" + result + "_" + cut["name"]
                    if func == "tracks_trackQualityHighPurity":
                        val = getattr(c, func)[ti]
                        if val:
                            val = 1
                        else:
                            val = 0
                        histograms[name].Fill(val)
                    else:
                        #print(func)
                        if tracksLogScale[j] and abs(getattr(c, func)[ti]) != 0.0:
                            histograms[name].Fill(log(abs(getattr(c, func)[ti]), 10))
                        else:
                            histograms[name].Fill(abs(getattr(c, func)[ti]))
        for i, cut in enumerate(cuts):
            histograms["Track_NumIso_" + cut["name"]].Fill(numIsoTracks[i])
            histograms["NM_Track_NumIso_" + cut["name"]].Fill(numMMIsoTracks[i])
            histograms["NM_Track_NumIso_Per_Reco_" + cut["name"]].Fill(recoNum, numMMIsoTracks[i])
            if numMMIsoTracks[i] == numMMZlIsoTracks[i]:
                histograms["NM_ZL_Track_NumIso_Per_Reco_" + cut["name"]].Fill(recoNum, numMMZlIsoTracks[i])

    print("Not Correct Procs=" + str(notCorrect))
    print("genFlavourBefore", genFlavourBefore, "genFlavourAfter", genFlavourAfter)

    hNM = histograms["NM_Track_NumIso_Per_Reco_" + cuts[-1]["name"]]
    xNMAxis = hNM.GetXaxis()
    yNMAxis = hNM.GetYaxis()
    binNMX = xNMAxis.FindBin(1)
    binNMY = yNMAxis.FindBin(1)

    hZL = histograms["NM_ZL_Track_NumIso_Per_Reco_" + cuts[-1]["name"]]
    xZLAxis = hZL.GetXaxis()
    yZLAxis = hZL.GetYaxis()
    binZLX = xZLAxis.FindBin(1)
    binZLY = yZLAxis.FindBin(1)

    print("Number of 1,1 bins NM_Track_NumIso_Per_Reco=" + str(hNM.GetBinContent(binNMX,binNMY) ) + " NM_ZL_Track_NumIso_Per_Reco=" + str(hZL.GetBinContent(binZLX,binZLY)) )

    c1 = TCanvas("c1")

    titlePad = TPad("titlePad", "",0.0,0.93,1.0,1.0)
    histPad = TPad("histPad", "",0.0,0.0,1.0,0.93)

    titlePad.Draw()
    t = TPaveText(0.0,0.93,1.0,1.0,"NB")
    t.SetFillStyle(0)
    t.SetLineColor(0)
    t.SetTextFont(40);
    t.Draw()

    histPad.Draw()
    histPad.Divide(3,2)
    OUTPUT_FILE = output_file or "./count_lepton_tracks.pdf"
    c1.Print(OUTPUT_FILE + "[");

    for cut in cuts:

        t.Clear()
        t.AddText(cut["title"])
        t.Draw();
        titlePad.Update()
        pId = 1
        needToDraw = False
        drawSame = False
        for h, hists in enumerate([funcs,lepTrackHists]):
            for func in hists:
                for obj in objs:
                    #print("***")
                    #print(cut["name"], obj, func)
                    if len(cut["name"]) > 0 and obj != "Track":
                        #print("Breaking")
                        continue
                    if h == 1 and obj == "Gen":
                        continue
                    maxY = 0
                    for lepType in lepTypes:
                        if obj == "Gen" and lepType == "MM":
                            continue
                        name = obj + "_" + lepType + "_" + func
                        if obj == "Track":
                            name += "_" + cut["name"]
                        h =  histograms[name]
                        maxY = max(maxY, h.GetMaximum())
    
                    drawSame = False
                    pad = histPad.cd(pId)
                    needToDraw = True
                    legend = TLegend(.69,.7,.85,.89)
                    memory.append(legend)
                    cP = 0
                    for lepType in lepTypes:
                        if obj == "Gen" and lepType == "MM":
                            continue
                        name = obj + "_" + lepType + "_" + func
                        if obj == "Track":
                            name += "_" + cut["name"]
                        print(name)
                        h =  histograms[name]
                        utils.formatHist(h, utils.colorPalette[cP], 0.35, True)
                        cP += 1
                        h.SetMaximum(maxY)
                        legend.AddEntry(h, lepType, 'F')
                        if drawSame:
                            h.Draw("HIST SAME")
                        else:
                            drawSame = True
                            #utils.setLabels(h, histDef)
                            h.Draw("HIST")
        
                    legend.Draw("SAME")
                    if logScale:
                        pad.SetLogy()
                    c1.Update()
                    pId += 1
    
                    if pId > 6:
                        pId = 1
                        c1.Print(OUTPUT_FILE);
                        needToDraw = False;

        if len(cut["name"]) == 0:
            for name in ["Lepton_minDealZ", "Track_minDealZ", "Track_RelIso", "Reco_Num"]:
                needToDraw = True
                pad = histPad.cd(pId)
                h =  histograms[name]
                utils.formatHist(h, utils.colorPalette[cP], 0.35, True)
                h.Draw("HIST")
                if logScale:
                    pad.SetLogy()
                c1.Update()
                pId += 1
                if pId > 6:
                    pId = 1
                    c1.Print(OUTPUT_FILE);
                    needToDraw = False
            
            # for name in eventHists:
#                 drawSame = False
#                 pad = histPad.cd(pId)
#                 needToDraw = True
#                 legend = TLegend(.69,.7,.85,.89)
#                 memory.append(legend)
#                 cP = 0
#                 
#                 maxY = 0
#                 for lepType in lepTypes:
#                     tname = name + "_" + lepType
#                     h = histograms[tname]
#                     maxY = max(maxY, h.GetMaximum())
#                 
#                 for lepType in lepTypes:
#                     tname = name + "_" + lepType
#                     h = histograms[tname]
#                     utils.formatHist(h, utils.colorPalette[cP])
#                     cP += 1
#                     h.SetMaximum(maxY)
#                     legend.AddEntry(h, lepType, 'F')
#                     if drawSame:
#                         h.Draw("HIST SAME")
#                     else:
#                         drawSame = True
#                         #utils.setLabels(h, histDef)
#                         h.Draw("HIST")
#                 legend.Draw("SAME")
#                 if logScale:
#                     pad.SetLogy()
#                 c1.Update()		
#                 pId += 1
# 
#                 if pId > 6:
#                     pId = 1
#                     c1.Print(OUTPUT_FILE);
#                     needToDraw = False;
                
        for i, trackHist in enumerate(trackHistsNoType + eventHistsNoType):
                name = trackHist + "_" + cut["name"]
                needToDraw = True
                pad = histPad.cd(pId)
                h =  histograms[name]
                utils.formatHist(h, utils.colorPalette[cP], 0.35, True)
                h.Draw("HIST")
                if logScale:
                    pad.SetLogy()
                c1.Update()		
                pId += 1
                if pId > 6:
                    pId = 1
                    c1.Print(OUTPUT_FILE);
                    needToDraw = False
    
        for hist in h2DHists:
            name = hist + "_" + cut["name"]
            needToDraw = True
            pad = histPad.cd(pId)
            h =  histograms[name]
            h.Draw("TEXT")
            c1.Update()		
            pId += 1
            if pId > 6:
                pId = 1
                c1.Print(OUTPUT_FILE);
                needToDraw = False

        for func in tracksFuncs + trackHists :#+ eventHists:
            maxY = 0
            for lepType in lepTypes:
                name = func + "_" + lepType + "_" + cut["name"]
                h =  histograms[name]
                maxY = max(maxY, h.GetMaximum())
            drawSame = False
            pad = histPad.cd(pId)
            needToDraw = True
            legend = TLegend(.69,.7,.80,.89)
            memory.append(legend)
            cP = 0
            for lepType in lepTypes:
                name = func + "_" + lepType + "_" + cut["name"]
                print(name)
                h =  histograms[name]
                utils.formatHist(h, utils.colorPalette[cP], 0.35, True)
                cP += 1
                h.SetMaximum(maxY)
                legend.AddEntry(h, lepType, 'F')
                if drawSame:
                    h.Draw("HIST SAME")
                else:
                    drawSame = True
                    #utils.setLabels(h, histDef)
                    h.Draw("HIST")
    
            legend.Draw("SAME")
            if logScale:
                pad.SetLogy()
            c1.Update()
            pId += 1

            if pId > 6:
                pId = 1
                c1.Print(OUTPUT_FILE);
                needToDraw = False;
    
        
        if needToDraw:
            for id in range(pId, 7):
                print("Clearing pad " + str(id))
                pad = histPad.cd(id)
                pad.Clear()
            c1.Print(OUTPUT_FILE);

    c1.Print(OUTPUT_FILE+"]");

main()

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
parser.add_argument('-o', '--output_file', nargs=1, help='Output Filename', required=True)
parser.add_argument('-ub', '--univ_bdt', nargs=1, help='Universal BDT Folder', required=True)
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
output_file = None
if args.output_file:
    output_file = args.output_file[0].strip()

if (bg and signal) or not (bg or signal):
    signal = True
    bg = False

univ_bdt = None
track_bdt = None
if args.univ_bdt:
    univ_bdt = args.univ_bdt[0]
if args.track_bdt:
    track_bdt = args.track_bdt[0]

######## END OF CMDLINE ARGUMENTS ########

tracksVars = (
        {"name":"dxyVtx", "type":"double"},
        {"name":"dzVtx", "type":"double"},
        {"name":"chi2perNdof", "type":"double"},
        {"name":"trkMiniRelIso", "type":"double"},
        {"name":"trkRelIso", "type":"double"},
        {"name":"charge", "type":"int"},
        {"name":"trackJetIso", "type":"double"},
        {"name":"trackQualityHighPurity", "type":"bool"},
        #{"name":"trackLeptonIso", "type":"double"}
        )

def main():
    iFile = TFile(input_file)
    #hHt = iFile.Get('hHt')
    c = iFile.Get('tEvent')

    tree = c.CloneTree(0)
    tree.SetDirectory(0)

    var_univBDT = np.zeros(1,dtype=float)
    tree.Branch('univBDT', var_univBDT,'univBDT/D')
    var_trackBDT = np.zeros(1,dtype=float)
    tree.Branch('trackBDT', var_trackBDT,'trackBDT/D')
    
    var_secondTrackBDT = np.zeros(1,dtype=float)
    tree.Branch('secondTrackBDT', var_secondTrackBDT,'secondTrackBDT/D')

    var_l1 = TLorentzVector()
    var_l2 = TLorentzVector()
    
    var_lepton = TLorentzVector()
    var_track = TLorentzVector()
    var_secondTrack = TLorentzVector()
    
    var_leptonFlavour = ROOT.std.string()

    tree.Branch('l1', 'TLorentzVector', var_l1)
    tree.Branch('l2', 'TLorentzVector', var_l2)
    
    tree.Branch('lepton', 'TLorentzVector', var_lepton)
    tree.Branch('track', 'TLorentzVector', var_track)
    tree.Branch('secondTrack', 'TLorentzVector', var_secondTrack)
    
    var_ti = np.zeros(1,dtype=int)
    tree.Branch('ti', var_ti,'ti/I')
    
    var_sti = np.zeros(1,dtype=int)
    tree.Branch('sti', var_sti,'sti/I')

    var_invMass = np.zeros(1,dtype=float)
    var_dileptonPt = np.zeros(1,dtype=float)
    var_deltaPhi = np.zeros(1,dtype=float)
    var_deltaEta = np.zeros(1,dtype=float)
    var_deltaR = np.zeros(1,dtype=float)
    var_pt3 = np.zeros(1,dtype=float)
    var_mtautau = np.zeros(1,dtype=float)
    var_mt1 = np.zeros(1,dtype=float)
    var_mt2 = np.zeros(1,dtype=float)
    var_mtt = np.zeros(1,dtype=float)
    var_mtl = np.zeros(1,dtype=float)
    var_DeltaEtaLeadingJetDilepton = np.zeros(1,dtype=float)
    var_DeltaPhiLeadingJetDilepton = np.zeros(1,dtype=float)
    var_dilepHt = np.zeros(1,dtype=float)
    var_NTracks = np.zeros(1,dtype=int)
    var_leptonCharge = np.zeros(1,dtype=int)
    var_deltaRMetTrack = np.zeros(1,dtype=float)
    var_deltaRMetLepton = np.zeros(1,dtype=float)
    var_deltaPhiMetTrack = np.zeros(1,dtype=float)
    var_deltaPhiMetLepton = np.zeros(1,dtype=float)


    tree.Branch('leptonCharge', var_leptonCharge, 'leptonCharge/I')
    #tree.Branch('leptonFlavour', var_leptonFlavour,'leptonCharge/C')
    tree.Branch('leptonFlavour', 'std::string', var_leptonFlavour)
    
    tree.Branch('invMass', var_invMass,'invMass/D')
    tree.Branch('dileptonPt', var_dileptonPt,'dileptonPt/D')
    tree.Branch('deltaPhi', var_deltaPhi,'deltaPhi/D')
    tree.Branch('deltaEta', var_deltaEta,'deltaEta/D')
    tree.Branch('deltaR', var_deltaR,'deltaR/D')
    tree.Branch('pt3', var_pt3,'pt3/D')
    tree.Branch('mtautau', var_mtautau,'mtautau/D')
    tree.Branch('mt1', var_mt1,'mt1/D')
    tree.Branch('mt2', var_mt2,'mt2/D')
    tree.Branch('mtt', var_mtt,'mtt/D')
    tree.Branch('mtl', var_mtl,'mtl/D')
    tree.Branch('DeltaEtaLeadingJetDilepton', var_DeltaEtaLeadingJetDilepton,'DeltaEtaLeadingJetDilepton/D')
    tree.Branch('DeltaPhiLeadingJetDilepton', var_DeltaPhiLeadingJetDilepton,'DeltaPhiLeadingJetDilepton/D')
    tree.Branch('dilepHt', var_dilepHt,'dilepHt/D')
    tree.Branch('NTracks', var_NTracks,'NTracks/I')
    
    tree.Branch('deltaRMetTrack', var_deltaRMetTrack, 'deltaRMetTrack/D')
    tree.Branch('deltaRMetLepton', var_deltaRMetLepton, 'deltaRMetLepton/D')
    tree.Branch('deltaPhiMetTrack', var_deltaPhiMetTrack, 'deltaPhiMetTrack/D')
    tree.Branch('deltaPhiMetLepton', var_deltaPhiMetLepton, 'deltaPhiMetLepton/D')

    nentries = c.GetEntries()
    print('Analysing', nentries, "entries")

    # (univ_testBGHists, univ_trainBGHists, univ_testSignalHists, univ_trainSignalHists, univ_methods, univ_names) = cut_optimisation.get_bdt_hists([univ_bdt])
#     univ_trainSignalHist, univ_trainBGHist, univ_testSignalHist, univ_testBGHist = univ_trainSignalHists[0], univ_trainBGHists[0], univ_testSignalHists[0], univ_testBGHists[0]
#     univ_highestZ, univ_highestS, univ_highestB, univ_highestMVA, univ_ST, univ_BT = cut_optimisation.getHighestZ(univ_trainSignalHist, univ_trainBGHist, univ_testSignalHist, univ_testBGHist)
# 
#     univ_bdt_weights = univ_bdt + "/dataset/weights/TMVAClassification_BDT.weights.xml"
#     univ_bdt_vars = cut_optimisation.getVariablesFromXMLWeightsFile(univ_bdt_weights)
#     univ_bdt_vars_map = cut_optimisation.getVariablesMemMap(univ_bdt_vars)
#     univ_bdt_reader = cut_optimisation.prepareReader(univ_bdt_weights, univ_bdt_vars, univ_bdt_vars_map)


    (track_testBGHists, track_trainBGHists, track_testSignalHists, track_trainSignalHists, track_methods, track_names) = cut_optimisation.get_bdt_hists([track_bdt])
    track_trainSignalHist, track_trainBGHist, track_testSignalHist, track_testBGHist = track_trainSignalHists[0], track_trainBGHists[0], track_testSignalHists[0], track_testBGHists[0]
    track_highestZ, track_highestS, track_highestB, track_highestMVA, track_ST, track_BT = cut_optimisation.getHighestZ(track_trainSignalHist, track_trainBGHist, track_testSignalHist, track_testBGHist)

    track_bdt_weights = track_bdt + "/dataset/weights/TMVAClassification_BDT.weights.xml"
    track_bdt_vars = cut_optimisation.getVariablesFromXMLWeightsFile(track_bdt_weights)
    track_bdt_vars_map = cut_optimisation.getVariablesMemMap(track_bdt_vars)
    track_bdt_specs = cut_optimisation.getSpecSpectatorFromXMLWeightsFile(track_bdt_vars)
    track_bdt_specs_map = cut_optimisation.getSpectatorsMemMap(track_bdt_vars)
    track_bdt_reader = cut_optimisation.prepareReader(track_bdt_weights, track_bdt_vars, track_bdt_vars_map, track_bdt_specs, track_bdt_specs_map)

    print(track_bdt_vars_map)

#     print("-------------------")
# 
#     print("univ_highestZ=" + str(univ_highestZ))
#     print("univ_highestS=" + str(univ_highestS))
#     print("univ_highestB=" + str(univ_highestB))
#     print("univ_highestMVA=" + str(univ_highestMVA))
#     print("univ_ST=" + str(univ_ST))
#     print("univ_BT=" + str(univ_BT))

    print("-------------------")

    print("track_highestZ=" + str(track_highestZ))
    print("track_highestS=" + str(track_highestS))
    print("track_highestB=" + str(track_highestB))
    print("track_highestMVA=" + str(track_highestMVA))
    print("track_ST=" + str(track_ST))
    print("track_BT=" + str(track_BT))

    print("-------------------")

    afterMonoLepton = 0
    afterUniversalBdt = 0
    afterMonoTrack = 0
    afterAtLeastOneTrack = 0

    totalTracks = 0
    totalSurvivedTracks = 0
    eventsWithGreaterThanOneOppSignTracks = 0
    noSurvivingTracks = 0

    for ientry in range(nentries):
        if ientry % 1000 == 0:
            print("Processing " + str(ientry))
        c.GetEntry(ientry)
        
        if c.MaxCsv25 > 0.7:
            continue
        
        ll, leptonCharge, leptonFlavour = analysis_ntuples.getSingleLeptonAfterSelection(c, c.LeadingJet)
        
        if ll is None:
            continue
        if leptonCharge == 0:
            print("WHAT?! leptonCharge=0")
        var_leptonCharge[0] = leptonCharge
        var_leptonFlavour = ROOT.std.string(leptonFlavour)
    
        afterMonoLepton += 1
    
        # for k, v in univ_bdt_vars_map.items():
#             v[0] = eval("c." + k)
        univ_tmva_value = 0#univ_bdt_reader.EvaluateMVA("BDT")
        var_univBDT[0] = univ_tmva_value
        #if univ_tmva_value < univ_highestMVA:
        #	continue
    
        afterUniversalBdt += 1
        
        var_secondTrackBDT[0] = -1
        
        metvec = TLorentzVector()
        metvec.SetPtEtaPhiE(c.Met, 0, c.METPhi, c.Met)
        
        highestOppositeTrackScore = None
        secondTrackScore = None
        secondTrack = None
        oppositeChargeTrack = None
        ntracks = 0
        for ti in range(c.tracks.size()):
            t = c.tracks[ti]
            tcharge = c.tracks_charge[ti]
            #Try lowering to 0!!
            
            if c.tracks_trkRelIso[ti] > 0.1:
                continue 
            if c.tracks_dxyVtx[ti] > 0.02:
                continue
            if c.tracks_dzVtx[ti] > 0.05:
                continue
            
            if sc:
                if tcharge * leptonCharge < 0:
                    continue
            else:
                if tcharge * leptonCharge > 0:
                    continue
            
            totalTracks +=1
        
            deltaRLL = abs(t.DeltaR(ll))
            if deltaRLL < 0.01:
                continue
            ntracks += 1
        
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
            
            track_tmva_value = track_bdt_reader.EvaluateMVA("BDT")
            
            if  highestOppositeTrackScore is None or highestOppositeTrackScore < track_tmva_value:
                if highestOppositeTrackScore is not None:
                    secondTrackScore = highestOppositeTrackScore
                    var_secondTrackBDT[0] = var_trackBDT[0]
                    secondTrack = oppositeChargeTrack
                highestOppositeTrackScore = track_tmva_value
                var_trackBDT[0] = track_tmva_value
                oppositeChargeTrack = ti

        #print("-------------")
        #print("Total Tracks=" + str(c.tracks.size()))
        #print("Passed Tracks=" + str(len(survivedTracks)))
    
        #print("survivedTracks=" + str(len(survivedTracks)))
    
#         if len(survivedTracks) == 0:
#             noSurvivingTracks += 1
#             continue
        if highestOppositeTrackScore is None or highestOppositeTrackScore<0:
            continue
        afterAtLeastOneTrack += 1
        #numberOfOppositeChargeTracks = 0
    
    
        #for i in survivedTracks:
        #    if c.tracks_charge[i] * leptonCharge < 0:
        #        numberOfOppositeChargeTracks +=1
        #        oppositeChargeTrack = i
    
        #if numberOfOppositeChargeTracks > 1:
        #    eventsWithGreaterThanOneOppSignTracks += 1
        
        #if numberOfOppositeChargeTracks != 1:
        #    continue
    
        #print("Track charge=" + str(c.tracks_charge[survivedTracks[0]]))
        #print("Lepton charge=" + str(leptonCharge))
    
        #if c.tracks_charge[survivedTracks[0]] * leptonCharge > 0:
        #	continue
    
        afterMonoTrack += 1
        
        var_ti[0] = oppositeChargeTrack
        if secondTrack is not None:
            var_sti[0] = secondTrack
        else:
            var_sti[0] = -1
        
        # tracksMem = {}
#         tracksMem["tracks"] = ROOT.std.vector(TLorentzVector)()
#         tracksMem["tracks"].push_back(c.tracks[oppositeChargeTrack])
#         tree.SetBranchAddress('tracks', tracksMem["tracks"])

        # for v in tracksVars:
#             tracksMem[v["name"]] = eval("ROOT.std.vector(" + v["type"] + ")()")
#             #print(eval("c.tracks_" + v["name"] + "[survivedTracks[0]]"))
#             tracksMem[v["name"]].push_back(eval(v["type"] + "(c.tracks_" + v["name"] + "[oppositeChargeTrack])"))
#             tree.SetBranchAddress('tracks_' + v["name"], tracksMem[v["name"]])
#     
    
        l1 = None
        l2 = None
        if ll.Pt() > c.tracks[oppositeChargeTrack].Pt():
            l1 = ll
            l2 = c.tracks[oppositeChargeTrack]
        else:
            l1 = c.tracks[oppositeChargeTrack]
            l2 = ll
    
        var_l1 = l1
        var_l2 = l2
        var_lepton = ll
        var_track = c.tracks[oppositeChargeTrack]
        
        if secondTrack is not None:
            var_secondTrack = c.tracks[secondTrack]
        else:
            var_secondTrack = TLorentzVector()
    
        tree.SetBranchAddress('l1', var_l1)
        tree.SetBranchAddress('l2', var_l2)
        tree.SetBranchAddress('lepton', var_lepton)
        tree.SetBranchAddress('track', var_track)
        tree.SetBranchAddress('secondTrack', var_secondTrack)
        tree.SetBranchAddress('leptonFlavour', var_leptonFlavour)
    
        var_invMass[0] = (l1 + l2).M()
        var_dileptonPt[0] = abs((l1 + l2).Pt())
        var_deltaPhi[0] = abs(l1.DeltaPhi(l2))
        var_deltaEta[0] = abs(l1.Eta() - l2.Eta())
        var_deltaR[0] = abs(l1.DeltaR(l2))
        var_NTracks[0] = ntracks

        var_pt3[0] = analysis_tools.pt3(l1.Pt(),l1.Phi(),l2.Pt(),l2.Phi(),c.Met,c.METPhi)

        pt = TLorentzVector()
        pt.SetPtEtaPhiE(c.Met,0,c.METPhi,c.Met)

        var_mt1[0] = analysis_tools.MT2(c.Met, c.METPhi, l1)
        var_mt2[0] = analysis_tools.MT2(c.Met, c.METPhi, l2)

        var_mtt[0] = analysis_tools.MT2(c.Met, c.METPhi, c.tracks[oppositeChargeTrack])
        var_mtl[0] = analysis_tools.MT2(c.Met, c.METPhi, ll)

        var_mtautau[0] = analysis_tools.Mtautau(pt, l1, l2)
    
        var_DeltaEtaLeadingJetDilepton[0] = abs((l1 + l2).Eta() - c.LeadingJet.Eta())
        var_DeltaPhiLeadingJetDilepton[0] = abs((l1 + l2).DeltaPhi(c.LeadingJet))
    
        var_dilepHt[0] = analysis_ntuples.htJet25Leps(c.Jets, [l1,l2])
        
        var_deltaRMetTrack[0] = abs(c.tracks[oppositeChargeTrack].DeltaR(pt))
        var_deltaPhiMetTrack[0] = abs(c.tracks[oppositeChargeTrack].DeltaPhi(pt))
        var_deltaRMetLepton[0] = abs(ll.DeltaR(pt))
        var_deltaPhiMetLepton[0] = abs(ll.DeltaPhi(pt))

        tree.Fill()
    
    
    if iFile.GetListOfKeys().Contains("lumiSecs") or tree.GetEntries() != 0:
        fnew = TFile(output_file,'recreate')
        tree.Write()
        if iFile.GetListOfKeys().Contains("lumiSecs"):
            lumiSecs = iFile.Get("lumiSecs")
            lumiSecs.Write("lumiSecs")
        #hHt.Write()
        fnew.Close()
    else:
        print("*** RESULT EMPTY")
    iFile.Close()

    print("nentries=" + str(nentries))
    print("totalTracks=" + str(totalTracks))
    print("totalSurvivedTracks=" + str(totalSurvivedTracks))
    print("eventsWithGreaterThanOneOppSignTracks=" + str(eventsWithGreaterThanOneOppSignTracks))
    print("noSurvivingTracks=" + str(noSurvivingTracks))
    print("afterAtLeastOneTrack=" + str(afterAtLeastOneTrack))
    print("afterMonoLepton=" + str(afterMonoLepton))
    print("afterUniversalBdt=" + str(afterUniversalBdt))
    print("afterMonoTrack=" + str(afterMonoTrack))

main()
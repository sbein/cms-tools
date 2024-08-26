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
parser.add_argument('-bdt', '--bdt', nargs=1, help='Dilepton BDT Folder', required=True)

parser.add_argument('-s', '--signal', dest='signal', help='Signal', action='store_true')
parser.add_argument('-bg', '--background', dest='bg', help='Background', action='store_true')
parser.add_argument('-data', '--data', dest='data', help='Data', action='store_true')
parser.add_argument('-tl', '--tl', dest='two_leptons', help='Two Leptons', action='store_true')
parser.add_argument('-dy', '--dy', dest='dy', help='Drell-Yan', action='store_true')
parser.add_argument('-sc', '--same_charge', dest='sc', help='Same Charge', action='store_true')
parser.add_argument('-sam', '--sam', dest='sam', help='Sam Samples', action='store_true')
args = parser.parse_args()

print(args)

signal = args.signal
bg = args.bg

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
if args.bdt:
    univ_bdt = args.bdt[0]
    
two_leptons = args.two_leptons
data = args.data

######## END OF CMDLINE ARGUMENTS ########


def main():
    iFile = TFile(input_file)
    #hHt = iFile.Get('hHt')
    c = iFile.Get('tEvent')
    
    triggerFileName = os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/susy-trig-plots.root")
    print("Opening trigger file: " + triggerFileName)
    
    triggerFile = TFile(triggerFileName, "read")
    
    tEffhMetMhtRealXMet2016 = analysis_ntuples.getTrigEffGraph(triggerFile, 'tEffhMetMhtRealXMet;1')
    tEffhMetMhtRealXMet2017 = analysis_ntuples.getTrigEffGraph(triggerFile, 'tEffhMetMhtRealXMet;2')
    tEffhMetMhtRealXMet2018 = analysis_ntuples.getTrigEffGraph(triggerFile, 'tEffhMetMhtRealXMet;3')
    
    tEffhMetMhtRealXMht2016 = analysis_ntuples.getTrigEffGraph(triggerFile, 'tEffhMetMhtRealXMht;1')
    tEffhMetMhtRealXMht2017 = analysis_ntuples.getTrigEffGraph(triggerFile, 'tEffhMetMhtRealXMht;2')
    tEffhMetMhtRealXMht2018 = analysis_ntuples.getTrigEffGraph(triggerFile, 'tEffhMetMhtRealXMht;3')
    
    tree = c.CloneTree(0)
    tree.SetDirectory(0)
    var_dilepBDT = np.zeros(1,dtype=float)
    
    var_leptons_ParentPdgId = ROOT.std.vector(int)()
    var_leptonParentPdgId = np.zeros(1,dtype=int)
    var_trackParentPdgId = np.zeros(1,dtype=int)
    
    var_trackParentPdgId = np.zeros(1,dtype=int)
    
    var_tEffhMetMhtRealXMet2016 = np.zeros(1,dtype=float)
    var_tEffhMetMhtRealXMet2017 = np.zeros(1,dtype=float)
    var_tEffhMetMhtRealXMet2018 = np.zeros(1,dtype=float)
    
    var_tEffhMetMhtRealXMht2016 = np.zeros(1,dtype=float)
    var_tEffhMetMhtRealXMht2017 = np.zeros(1,dtype=float)
    var_tEffhMetMhtRealXMht2018 = np.zeros(1,dtype=float)
    
    var_passedMhtMet6pack = np.zeros(1,dtype=bool)
    
    var_tautau = np.zeros(1,dtype=bool)
    var_rr = np.zeros(1,dtype=bool)
    var_rf = np.zeros(1,dtype=bool)
    var_ff = np.zeros(1,dtype=bool)
    var_sc = np.zeros(1,dtype=bool)
    var_n_body = np.zeros(1,dtype=bool)
    var_tc = np.zeros(1,dtype=bool)
    var_other = np.zeros(1,dtype=bool)
    
    var_omega = np.zeros(1,dtype=bool)
    var_rho_0 = np.zeros(1,dtype=bool)
    var_eta = np.zeros(1,dtype=bool)
    var_phi = np.zeros(1,dtype=bool)
    var_eta_prime = np.zeros(1,dtype=bool)
    var_j_psi = np.zeros(1,dtype=bool)
    var_upsilon_1 = np.zeros(1,dtype=bool)
    var_upsilon_2 = np.zeros(1,dtype=bool)

    tree.Branch('dilepBDT', var_dilepBDT,'dilepBDT/D')
    
    tree.Branch('tEffhMetMhtRealXMet2016', var_tEffhMetMhtRealXMet2016,'tEffhMetMhtRealXMet2016/D')
    tree.Branch('tEffhMetMhtRealXMet2017', var_tEffhMetMhtRealXMet2017,'tEffhMetMhtRealXMet2017/D')
    tree.Branch('tEffhMetMhtRealXMet2018', var_tEffhMetMhtRealXMet2018,'tEffhMetMhtRealXMet2018/D')
    
    tree.Branch('tEffhMetMhtRealXMht2016', var_tEffhMetMhtRealXMht2016,'tEffhMetMhtRealXMht2016/D')
    tree.Branch('tEffhMetMhtRealXMht2017', var_tEffhMetMhtRealXMht2017,'tEffhMetMhtRealXMht2017/D')
    tree.Branch('tEffhMetMhtRealXMht2018', var_tEffhMetMhtRealXMht2018,'tEffhMetMhtRealXMht2018/D')
    
    tree.Branch('passedMhtMet6pack', var_passedMhtMet6pack,'passedMhtMet6pack/b')
    
    
    if not data:
        if two_leptons:
            print("TWO_LEPTONS!")
            tree.Branch('leptons_ParentPdgId', 'std::vector<int>', var_leptons_ParentPdgId)
            
            if bg:
                tree.Branch('tautau', var_tautau,'tautau/b')
                tree.Branch('rr', var_rr,'rr/b')
                tree.Branch('rf', var_rf,'rf/b')
                tree.Branch('ff', var_ff,'ff/b')
                tree.Branch('sc', var_sc,'sc/b')
                tree.Branch('n_body', var_n_body,'n_body/b')
                tree.Branch('tc', var_tc,'tc/b')
                tree.Branch('other', var_other,'other/b')
                
                tree.Branch('omega', var_omega,'omega/b')
                tree.Branch('rho_0', var_rho_0,'rho_0/b')
                tree.Branch('eta', var_eta,'eta/b')
                tree.Branch('phi', var_phi,'phi/b')
                tree.Branch('eta_prime', var_eta_prime,'eta_prime/b')
                tree.Branch('j_psi', var_j_psi,'j_psi/b')
                tree.Branch('upsilon_1', var_upsilon_1,'upsilon_1/b')
                tree.Branch('upsilon_2', var_upsilon_2,'upsilon_2/b')
        else:
            tree.Branch('leptonParentPdgId', var_leptonParentPdgId, 'leptonParentPdgId/I')
            tree.Branch('trackParentPdgId', var_trackParentPdgId, 'trackParentPdgId/I')
    

    nentries = c.GetEntries()
    print('Analysing', nentries, "entries")

    (univ_testBGHists, univ_trainBGHists, univ_testSignalHists, univ_trainSignalHists, univ_methods, univ_names) = cut_optimisation.get_bdt_hists([univ_bdt])
    univ_trainSignalHist, univ_trainBGHist, univ_testSignalHist, univ_testBGHist = univ_trainSignalHists[0], univ_trainBGHists[0], univ_testSignalHists[0], univ_testBGHists[0]
    univ_highestZ, univ_highestS, univ_highestB, univ_highestMVA, univ_ST, univ_BT = cut_optimisation.getHighestZ(univ_trainSignalHist, univ_trainBGHist, univ_testSignalHist, univ_testBGHist)

    univ_bdt_weights = univ_bdt + "/dataset/weights/TMVAClassification_BDT.weights.xml"
    univ_bdt_vars = cut_optimisation.getVariablesFromXMLWeightsFile(univ_bdt_weights)
    univ_bdt_vars_map = cut_optimisation.getVariablesMemMap(univ_bdt_vars)
    univ_bdt_specs = cut_optimisation.getSpecSpectatorFromXMLWeightsFile(univ_bdt_weights)
    univ_bdt_specs_map = cut_optimisation.getSpectatorsMemMap(univ_bdt_specs)
    print(univ_bdt_vars)
    print(univ_bdt_vars_map)
    print(univ_bdt_specs)
    print(univ_bdt_specs_map)
    univ_bdt_reader = cut_optimisation.prepareReader(univ_bdt_weights, univ_bdt_vars, univ_bdt_vars_map, univ_bdt_specs, univ_bdt_specs_map)

    print("-------------------")

    print("univ_highestZ=" + str(univ_highestZ))
    print("univ_highestS=" + str(univ_highestS))
    print("univ_highestB=" + str(univ_highestB))
    print("univ_highestMVA=" + str(univ_highestMVA))
    print("univ_ST=" + str(univ_ST))
    print("univ_BT=" + str(univ_BT))

    print("-------------------")

    for ientry in range(nentries):
        if ientry % 1000 == 0:
            print("Processing " + str(ientry) + " out of " + str(nentries))
        c.GetEntry(ientry)
    
        for k, v in univ_bdt_vars_map.items():
            v[0] = eval("c." + k)
        dilep_tmva_value = univ_bdt_reader.EvaluateMVA("BDT")
        # Selection
        #if dilep_tmva_value < -0.3 or c.Met < 200 or c.univBDT < -0.4 or c.tracks[0].Pt() < 3 or c.tracks[0].Pt() > 15 or c.tracks_dzVtx[0] > 0.1 or c.tracks_dxyVtx[0] > 0.1 or abs(c.tracks[0].Eta()) > 2.4:
        #if dilep_tmva_value < -0.3 or c.Met < 200 or c.univBDT < -0.4 or c.tracks[0].Pt() < 3 or c.tracks[0].Pt() > 15 or abs(c.tracks[0].Eta()) > 2.4:
        #    continue
        #if c.Mht < 200:
        #    continue
        var_dilepBDT[0] = dilep_tmva_value
        
        if not data:
            gens = [i for i in range(c.GenParticles.size())]
            #print("c.GenParticles.size() ", c.GenParticles.size(), gens)
            if two_leptons:
                if bg:
                    var_tautau[0] = False
                    var_rr[0] = False
                    var_rf[0] = False
                    var_ff[0] = False
                    var_sc[0] = False
                    var_n_body[0] = False
                    var_tc[0] = False
                    var_other[0] = False
                    
                    var_omega[0] = False
                    var_rho_0[0] = False
                    var_eta[0] = False
                    var_phi[0] = False
                    var_eta_prime[0] = False
                    var_j_psi[0] = False
                    var_upsilon_1[0] = False
                    var_upsilon_2[0] = False
                var_leptons_ParentPdgId = ROOT.std.vector(int)()
                lepCans = []
                numRealLeptons = 0
                
                for i in range(c.leptons.size()):
                    lepton = c.leptons[i]
                    min, minCan = analysis_ntuples.minDeltaRGenParticles(lepton, gens, c.GenParticles)
                    pdgId = c.GenParticles_ParentId[minCan]
                    if min > 0.01:
                        #print("BAD GEN!!! ", min)
                        pdgId = 0
                    else:
                        if ((abs(c.GenParticles_PdgId[minCan]) == 13 and c.leptonFlavour == "Muons") or (abs(c.GenParticles_PdgId[minCan]) == 11 and c.leptonFlavour == "Electrons")) and c.leptons_charge[i] * c.GenParticles_PdgId[minCan] < 0:
                            numRealLeptons += 1
                            lepCans.append(minCan)
                        else:
                            #print("BAD GEN MATCH! ")
                            pdgId = 0
                        # parentIdx = c.GenParticles_ParentIdx[minCan]
#                         if c.GenParticles_PdgId[parentIdx] != pdgId:
#                             print("WHAT?!?! ******** c.GenParticles_PdgId[parentIdx]", c.GenParticles_PdgId[parentIdx], "pdgId", pdgId, "parentIdx", parentIdx)
#                             print("c.GenParticles_ParentId[minCan]", c.GenParticles_ParentId[minCan], "c.GenParticles_PdgId[parentIdx]", c.GenParticles_PdgId[parentIdx])
                    var_leptons_ParentPdgId.push_back(pdgId)
                tree.SetBranchAddress('leptons_ParentPdgId', var_leptons_ParentPdgId)
                if bg:
                    if numRealLeptons == 0:
                        var_ff[0] = True
                    elif numRealLeptons == 1:
                        var_rf[0] = True
                    else:
                        var_rr[0] = True
                        if abs(var_leptons_ParentPdgId[0]) == abs(var_leptons_ParentPdgId[1]) == 15:
                            var_tautau[0] = True
                        
                        parentIdx = c.GenParticles_ParentIdx[lepCans[0]]
                        parentIdx2 = c.GenParticles_ParentIdx[lepCans[1]]
                        if parentIdx == -1 and parentIdx2 == -1:
                            var_other[0] = True
                            if abs(var_leptons_ParentPdgId[0]) == abs(var_leptons_ParentPdgId[1]) == 223:
                                var_omega[0] = True
                            elif abs(var_leptons_ParentPdgId[0]) == abs(var_leptons_ParentPdgId[1]) == 113:
                                var_rho_0[0] = True
                            elif abs(var_leptons_ParentPdgId[0]) == abs(var_leptons_ParentPdgId[1]) == 221:
                                var_eta[0] = True
                            elif abs(var_leptons_ParentPdgId[0]) == abs(var_leptons_ParentPdgId[1]) == 333:
                                var_phi[0] = True
                            elif abs(var_leptons_ParentPdgId[0]) == abs(var_leptons_ParentPdgId[1]) == 331:
                                var_eta_prime[0] = True
                            elif abs(var_leptons_ParentPdgId[0]) == abs(var_leptons_ParentPdgId[1]) == 443:
                                var_j_psi[0] = True
                            elif abs(var_leptons_ParentPdgId[0]) == abs(var_leptons_ParentPdgId[1]) == 553:
                                var_upsilon_1[0] = True
                            elif abs(var_leptons_ParentPdgId[0]) == abs(var_leptons_ParentPdgId[1]) == 100553:
                                var_upsilon_2[0] = True
                        else:
                            if c.GenParticles_ParentIdx[lepCans[0]] == c.GenParticles_ParentIdx[lepCans[1]]:
                                numOfParentChildren = 0
                                for i in range(c.GenParticles.size()):
                                    if c.GenParticles_Status[i] == 1 and c.GenParticles_ParentIdx[i] == parentIdx:
                                        numOfParentChildren += 1
                                #print("numOfParentChildren=", numOfParentChildren, "var_leptons_ParentPdgId[0]", var_leptons_ParentPdgId[0], "c.GenParticles_PdgId[parentIdx]", c.GenParticles_PdgId[parentIdx], "c.GenParticles_PdgId[parentIdx2]", c.GenParticles_PdgId[parentIdx2])
                                #print(lepCans)
                                if numOfParentChildren == 2:
                                    var_sc[0] = True
                                    if abs(c.GenParticles_PdgId[parentIdx]) == 223:
                                        var_omega[0] = True
                                    elif abs(c.GenParticles_PdgId[parentIdx]) == 113:
                                        var_rho_0[0] = True
                                    elif abs(c.GenParticles_PdgId[parentIdx]) == 221:
                                        var_eta[0] = True
                                    elif abs(c.GenParticles_PdgId[parentIdx]) == 333:
                                        var_phi[0] = True
                                    elif abs(c.GenParticles_PdgId[parentIdx]) == 331:
                                        var_eta_prime[0] = True
                                    elif abs(c.GenParticles_PdgId[parentIdx]) == 443:
                                        var_j_psi[0] = True
                                    elif abs(c.GenParticles_PdgId[parentIdx]) == 553:
                                        var_upsilon_1[0] = True
                                    elif abs(c.GenParticles_PdgId[parentIdx]) == 100553:
                                        var_upsilon_2[0] = True
                                else:
                                    var_n_body[0] = True
                            else:
                                var_tc[0] = True
            else:
                min, minCan = analysis_ntuples.minDeltaRGenParticles(c.lepton, gens, c.GenParticles)
                #print(min, m inCan)
                pdgId = c.GenParticles_ParentId[minCan]
                if min > 0.05:
                 #   print("BAD GEN LEPTON!!!")
                    pdgId = 0
                #else:
                #    print("GOOD LEPTON ", pdgId)
                var_leptonParentPdgId[0] = pdgId
                min, minCan = analysis_ntuples.minDeltaRGenParticles(c.track, gens, c.GenParticles)
                pdgId = c.GenParticles_ParentId[minCan]
                if min > 0.05:
                    #print("BAD GEN TRACK!!!")
                    pdgId = 0
                #else:
                #    print("GOOD TRACK ", pdgId)
                var_trackParentPdgId[0] = pdgId
        if not data:            
            var_tEffhMetMhtRealXMet2016[0] = tEffhMetMhtRealXMet2016.Eval(c.Met)
            var_tEffhMetMhtRealXMet2017[0] = tEffhMetMhtRealXMet2017.Eval(c.Met)
            var_tEffhMetMhtRealXMet2018[0] = tEffhMetMhtRealXMet2018.Eval(c.Met)
    
            var_tEffhMetMhtRealXMht2016[0] = tEffhMetMhtRealXMht2016.Eval(c.Mht)
            var_tEffhMetMhtRealXMht2017[0] = tEffhMetMhtRealXMht2017.Eval(c.Mht)
            var_tEffhMetMhtRealXMht2018[0] = tEffhMetMhtRealXMht2018.Eval(c.Mht)
            
            var_passedMhtMet6pack[0] = True
            
            #if c.Met < 200:
            #    print("HERE:", var_tEffhMetMhtRealXMet2016[0])
        else:
            print("ELSE!!")
            var_tEffhMetMhtRealXMet2016[0] = 1
            var_tEffhMetMhtRealXMet2017[0] = 1
            var_tEffhMetMhtRealXMet2018[0] = 1
    
            var_tEffhMetMhtRealXMht2016[0] = 1
            var_tEffhMetMhtRealXMht2017[0] = 1
            var_tEffhMetMhtRealXMht2018[0] = 1
            
            var_passedMhtMet6pack[0] = analysis_ntuples.passTrig(c, "MhtMet6pack")
        
        tree.Fill()
        
    print("DONE SKIMMING")
    if iFile.GetListOfKeys().Contains("lumiSecs") or tree.GetEntries() != 0:
        fnew = TFile(output_file,'recreate')
        tree.Write()
        print("Done writing tree...")
        if iFile.GetListOfKeys().Contains("lumiSecs"):
            lumiSecs = iFile.Get("lumiSecs")
            lumiSecs.Write("lumiSecs")
        #hHt.Write()
        fnew.Close()
    else:
        print("*** RESULT EMPTY")
    iFile.Close()

main()
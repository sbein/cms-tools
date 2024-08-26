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
from lib import analysis_tools
from lib import utils

gSystem.Load('LumiSectMap_C')
from ROOT import LumiSectMap

gSystem.Load('LeptonCollectionMap_C')
from ROOT import LeptonCollectionMap
from ROOT import LeptonCollectionFilesMap
from ROOT import LeptonCollection

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Create skims for x1x2x1 process.')
parser.add_argument('-i', '--input_file', nargs=1, help='Input Filename', required=False)
parser.add_argument('-o', '--output_file', nargs=1, help='Output Filename', required=False)
parser.add_argument('-madHTgt', '--madHTgt', nargs=1, help='madHT lower bound', required=False)
parser.add_argument('-madHTlt', '--madHTlt', nargs=1, help='madHT uppper bound', required=False)

parser.add_argument('-s', '--signal', dest='signal', help='Signal', action='store_true')
parser.add_argument('-bg', '--background', dest='bg', help='Background', action='store_true')
parser.add_argument('-skim', '--skim', dest='skim', help='Skim', action='store_true')
parser.add_argument('-data', '--data', dest='data', help='Data', action='store_true')
parser.add_argument('-dy', '--dy', dest='dy', help='Drell-Yan', action='store_true')
parser.add_argument('-sam', '--sam', dest='sam', help='Sam Samples', action='store_true')
parser.add_argument('-sc', '--sc', dest='sc', help='Same Charge', action='store_true')
parser.add_argument('-nlp', '--no_lepton_selection', dest='no_lepton_selection', help='No Lepton Selection Skim', action='store_true')
args = parser.parse_args()

print(args)

madHTgt = None
madHTlt = None
if args.madHTgt:
    madHTgt = int(args.madHTgt[0])
    print("Got madHT lower bound of " + str(madHTgt))
if args.madHTlt:
    madHTlt = int(args.madHTlt[0])
    print("Got madHT upper bound of " + str(madHTlt))


signal = args.signal
bg = args.bg
data = args.data
dy = args.dy
sam = args.sam
sc = args.sc
no_lepton_selection = args.no_lepton_selection

if dy:
    print("Got Drell-Yan")
    #exit(0)
if sc:
    print("SAME SIGN!")
if no_lepton_selection:
    print("NO LEPTON SELECTION!")

input_file = None
if args.input_file:
    input_file = args.input_file[0].strip()
output_file = None
if args.output_file:
    output_file = args.output_file[0].strip()

if (bg and signal):
    signal = True
    bg = False

replace_lepton_collection = True
if signal:
    replace_lepton_collection = False
    
def getDyMuons(c):
    muons = [i for i in range(len(c.Muons)) if c.Muons[i].Pt() >= 15 and bool(c.Muons_mediumID[i]) and bool(c.Muons_passIso[i]) and abs(c.Muons[i].Eta()) <= 2.4]
    
    if len(muons) != 2:
        return None, None
        
    if c.Muons[muons[0]].Pt() < 30:
        return None, None
    
    if c.Muons_charge[muons[0]] * c.Muons_charge[muons[1]] > 0:
        return None, None
    
    invMass = (c.Muons[muons[0]] + c.Muons[muons[1]]).M()
    if not abs(invMass-91.19)<10: return None, None
    
    return muons, invMass

######## END OF CMDLINE ARGUMENTS ########
def main():
    
    import os
    from lib import utils
    
    var_RunNum = np.zeros(1,dtype=int)
    var_LumiBlockNum = np.zeros(1,dtype=int)
    var_EvtNum = np.zeros(1,dtype=long)
    
    var_Met = np.zeros(1,dtype=float)
    var_METPhi = np.zeros(1,dtype=float)
    var_CrossSection = np.zeros(1,dtype=float)
    var_BranchingRatio = np.zeros(1,dtype=float)
    var_NJets = np.zeros(1,dtype=int)
    var_BTagsLoose = np.zeros(1,dtype=int)
    var_BTagsMedium = np.zeros(1,dtype=int)
    var_BTagsDeepLoose = np.zeros(1,dtype=int)
    var_BTagsDeepMedium = np.zeros(1,dtype=int)
    var_Ht = np.zeros(1,dtype=float)
    var_MHTPhi = np.zeros(1,dtype=float)
    var_madHT = np.zeros(1,dtype=float)
    var_Mht = np.zeros(1,dtype=float)
    var_MetDHt = np.zeros(1,dtype=float)
    var_Mt2 = np.zeros(1,dtype=float)
    var_Electrons = ROOT.std.vector(TLorentzVector)()
    var_Electrons_charge = ROOT.std.vector(int)()
    var_Electrons_mediumID = ROOT.std.vector(bool)()
    var_Electrons_passIso = ROOT.std.vector(bool)()
    var_Electrons_tightID = ROOT.std.vector(bool)()
    var_Electrons_EnergyCorr = ROOT.std.vector(double)()
    var_Electrons_MiniIso = ROOT.std.vector(double)()
    var_Electrons_MT2Activity = ROOT.std.vector(double)()
    var_Electrons_MTW = ROOT.std.vector(double)()
    var_Electrons_TrkEnergyCorr = ROOT.std.vector(double)()
    
    var_Electrons_isZ = ROOT.std.vector(bool)()
    var_Electrons_deltaRLJ = ROOT.std.vector(double)()
    var_Electrons_deltaPhiLJ = ROOT.std.vector(double)()
    var_Electrons_deltaEtaLJ = ROOT.std.vector(double)()
    var_Electrons_matchGen = ROOT.std.vector(bool)()
    var_Electrons_minDeltaRJets = ROOT.std.vector(double)()
    var_Electrons_closestJet = ROOT.std.vector(int)()
    
    var_Electrons_correctedMinDeltaRJets = ROOT.std.vector(double)()
    var_Electrons_correctedClosestJet = ROOT.std.vector(int)()
    
    var_Muons = ROOT.std.vector(TLorentzVector)()
    var_Muons_charge = ROOT.std.vector(int)()
    var_Muons_mediumID = ROOT.std.vector(bool)()
    var_Muons_passIso = ROOT.std.vector(bool)()
    var_Muons_tightID = ROOT.std.vector(bool)()
    var_Muons_MiniIso = ROOT.std.vector(double)()
    var_Muons_MT2Activity = ROOT.std.vector(double)()
    var_Muons_MTW = ROOT.std.vector(double)()
    
    var_Muons_isZ = ROOT.std.vector(bool)()
    var_Muons_deltaRLJ = ROOT.std.vector(double)()
    var_Muons_deltaPhiLJ = ROOT.std.vector(double)()
    var_Muons_deltaEtaLJ = ROOT.std.vector(double)()
    var_Muons_matchGen = ROOT.std.vector(bool)()
    var_Muons_minDeltaRJets = ROOT.std.vector(double)()
    var_Muons_closestJet = ROOT.std.vector(int)()

    
    var_Muons_correctedMinDeltaRJets = ROOT.std.vector(double)()
    var_Muons_correctedClosestJet = ROOT.std.vector(int)()
    
    var_vetoElectronsPassIso = np.zeros(1,dtype=bool)
    var_vetoElectronsMediumID = np.zeros(1,dtype=bool)
    var_vetoElectronsTightID = np.zeros(1,dtype=bool)
    
    var_vetoMuonsPassIso = np.zeros(1,dtype=bool)
    var_vetoMuonsMediumID = np.zeros(1,dtype=bool)
    var_vetoMuonsTightID = np.zeros(1,dtype=bool)
    
    var_DYMuons = ROOT.std.vector(TLorentzVector)()
    var_DYMuonsSum = TLorentzVector()
    var_DYMuonsInvMass = np.zeros(1,dtype=float)
    var_DYMuons_charge = ROOT.std.vector(int)()
    var_DYMuons_mediumID = ROOT.std.vector(bool)()
    var_DYMuons_passIso = ROOT.std.vector(bool)()
    var_DYMuons_tightID = ROOT.std.vector(bool)()
    var_DYMuons_MiniIso = ROOT.std.vector(double)()
    var_DYMuons_MT2Activity = ROOT.std.vector(double)()
    var_DYMuons_MTW = ROOT.std.vector(double)()
    
    var_GenParticles = ROOT.std.vector(TLorentzVector)()
    var_GenParticles_ParentId = ROOT.std.vector(int)()
    var_GenParticles_ParentIdx = ROOT.std.vector(int)()
    var_GenParticles_PdgId = ROOT.std.vector(int)()
    var_GenParticles_Status = ROOT.std.vector(int)()
    var_LeadingJetPt = np.zeros(1,dtype=float)
    var_NL = np.zeros(1,dtype=int)
    var_NLGen = np.zeros(1,dtype=int)
    var_NLGenZ = np.zeros(1,dtype=int)
    var_puWeight = np.zeros(1,dtype=float)

    var_Jets = ROOT.std.vector(TLorentzVector)()
    var_Jets_bDiscriminatorCSV = ROOT.std.vector(double)()
    var_Jets_bJetTagDeepCSVBvsAll = ROOT.std.vector(double)()
    var_Jets_electronEnergyFraction = ROOT.std.vector(double)()
    var_Jets_muonEnergyFraction = ROOT.std.vector(double)()
    var_Jets_muonMultiplicity = ROOT.std.vector(int)()
    var_Jets_multiplicity = ROOT.std.vector(int)()
    var_Jets_electronMultiplicity = ROOT.std.vector(int)()
    var_Jets_muonCorrected = ROOT.std.vector(TLorentzVector)()
    var_Jets_electronCorrected = ROOT.std.vector(TLorentzVector)()
    
    var_LeadingJetPartonFlavor = np.zeros(1,dtype=int)
    var_LeadingJetQgLikelihood = np.zeros(1,dtype=float)
    var_LeadingJetMinDeltaRMuons = np.zeros(1,dtype=float)
    var_LeadingJetMinDeltaRElectrons = np.zeros(1,dtype=float)
    
    var_MinDeltaPhiMetJets = np.zeros(1,dtype=float)
    var_MinDeltaPhiMhtJets = np.zeros(1,dtype=float)
    
    var_MinCsv30 = np.zeros(1,dtype=float)
    var_MinCsv25 = np.zeros(1,dtype=float)
    var_MaxCsv30 = np.zeros(1,dtype=float)
    var_MaxCsv25 = np.zeros(1,dtype=float)
    
    var_MinDeepCsv30 = np.zeros(1,dtype=float)
    var_MinDeepCsv25 = np.zeros(1,dtype=float)
    var_MaxDeepCsv30 = np.zeros(1,dtype=float)
    var_MaxDeepCsv25 = np.zeros(1,dtype=float)
    #### TRACKS ####

    var_tracks          = ROOT.std.vector(TLorentzVector)()
    var_tracks_charge   = ROOT.std.vector(int)()
    var_tracks_chi2perNdof = ROOT.std.vector(double)()
    var_tracks_dxyVtx   = ROOT.std.vector(double)()
    var_tracks_dzVtx    = ROOT.std.vector(double)()
    var_tracks_trackJetIso = ROOT.std.vector(double)()
    #var_tracks_trackLeptonIso = ROOT.std.vector(double)()
    var_tracks_trkMiniRelIso = ROOT.std.vector(double)()
    var_tracks_trkRelIso = ROOT.std.vector(double)()
    var_tracks_trackQualityHighPurity = ROOT.std.vector(bool)()
    
    var_genFlavour      = ROOT.std.string()
    
    var_category = np.zeros(1,dtype=bool)
    
    leptonsCorrJetVars = {}
    
    for lep in ["Muons", "Electrons"]:
        for CorrJetObs in utils.leptonIsolationList:
            if CorrJetObs == "CorrJetIso":
                for ptRange in utils.leptonCorrJetIsoPtRange:
                    leptonsCorrJetVars[lep + "_pass" + CorrJetObs + str(ptRange)] = ROOT.std.vector(eval(utils.leptonsCorrJetVecList[CorrJetObs]))()
            else:
                leptonsCorrJetVars[lep + "_pass" + CorrJetObs] = ROOT.std.vector(eval(utils.leptonsCorrJetVecList[CorrJetObs]))()
    
    print(leptonsCorrJetVars)
    
    # DILEPTON OBSERVABLES
    
    dileptonVars = {}
    
    for iso in utils.leptonIsolationList:
        for cat in utils.leptonIsolationCategories:
            ptRanges = [""]
            if iso == "CorrJetIso":
                ptRanges = utils.leptonCorrJetIsoPtRange
            for ptRange in ptRanges:
                for vecObs in utils.dileptonObservablesVecList:
                    dileptonVars[vecObs + iso + str(ptRange) + cat] = ROOT.std.vector(eval(utils.dileptonObservablesVecList[vecObs]))()
                for stringObs in utils.dileptonObservablesStringList:
                    dileptonVars[stringObs + iso + str(ptRange) + cat] = ROOT.std.string("")
                for DTypeObs in utils.dileptonObservablesDTypesList:
                    dileptonVars[DTypeObs + iso + str(ptRange) + cat] = np.zeros(1,dtype=utils.dileptonObservablesDTypesList[DTypeObs])

    print(dileptonVars)
       
    var_LeadingJet = TLorentzVector()
        
    # TRIGGER
    var_triggerNames     = ROOT.std.vector(ROOT.std.string)()
    var_triggerPass      = ROOT.std.vector(int)()
    var_triggerPrescales = ROOT.std.vector(int)()
    var_triggerVersion   = ROOT.std.vector(int)()

    tEvent = TTree('tEvent','tEvent')
    
    tEvent.Branch('RunNum', var_RunNum,'RunNum/I')
    tEvent.Branch('LumiBlockNum', var_LumiBlockNum,'LumiBlockNum/I')
    tEvent.Branch('EvtNum', var_EvtNum,'EvtNum/L')
    
    tEvent.Branch('Met', var_Met,'Met/D')
    tEvent.Branch('METPhi', var_METPhi,'METPhi/D')
    tEvent.Branch('CrossSection', var_CrossSection,'CrossSection/D')
    tEvent.Branch('BranchingRatio', var_BranchingRatio,'BranchingRatio/D')
    tEvent.Branch('NJets', var_NJets,'NJets/I')
    tEvent.Branch('BTagsLoose', var_BTagsLoose,'BTagsLoose/I')
    tEvent.Branch('BTagsMedium', var_BTagsMedium,'BTagsMedium/I')
    tEvent.Branch('BTagsDeepLoose', var_BTagsDeepLoose,'BTagsDeepLoose/I')
    tEvent.Branch('BTagsDeepMedium', var_BTagsDeepMedium,'BTagsDeepMedium/I')
    
    tEvent.Branch('NL', var_NL,'NL/I')
    tEvent.Branch('NLGen', var_NLGen,'NLGen/I')
    tEvent.Branch('NLGenZ', var_NLGenZ,'NLGenZ/I')
    tEvent.Branch('Ht', var_Ht,'Ht/D')
    tEvent.Branch('madHT', var_madHT,'madHT/D')
    tEvent.Branch('Mht', var_Mht,'Mht/D')
    tEvent.Branch('MHTPhi', var_MHTPhi,'MHTPhi/D')
    tEvent.Branch('MetDHt', var_MetDHt,'MetDHt/D')
    #tEvent.Branch('MetDHt2', var_MetDHt2,'MetDHt2/D')
    tEvent.Branch('Mt2', var_Mt2,'Mt2/D')
    tEvent.Branch('puWeight', var_puWeight,'puWeight/D')
    

    tEvent.Branch('Electrons', 'std::vector<TLorentzVector>', var_Electrons)
    tEvent.Branch('Electrons_charge', 'std::vector<int>', var_Electrons_charge)
    
    tEvent.Branch('Electrons_EnergyCorr', 'std::vector<double>', var_Electrons_EnergyCorr)
    tEvent.Branch('Electrons_MiniIso', 'std::vector<double>', var_Electrons_MiniIso)
    tEvent.Branch('Electrons_MT2Activity', 'std::vector<double>', var_Electrons_MT2Activity)
    tEvent.Branch('Electrons_MTW', 'std::vector<double>', var_Electrons_MTW)
    tEvent.Branch('Electrons_TrkEnergyCorr', 'std::vector<double>', var_Electrons_TrkEnergyCorr)
    
    tEvent.Branch('Electrons_mediumID', 'std::vector<bool>', var_Electrons_mediumID)
    tEvent.Branch('Electrons_passIso', 'std::vector<bool>', var_Electrons_passIso)
    tEvent.Branch('Electrons_tightID', 'std::vector<bool>', var_Electrons_tightID)
    
    tEvent.Branch('Electrons_deltaRLJ', 'std::vector<double>', var_Electrons_deltaRLJ)
    tEvent.Branch('Electrons_deltaPhiLJ', 'std::vector<double>', var_Electrons_deltaPhiLJ)
    tEvent.Branch('Electrons_deltaEtaLJ', 'std::vector<double>', var_Electrons_deltaEtaLJ)
    
    tEvent.Branch('Electrons_matchGen', 'std::vector<bool>', var_Electrons_matchGen)    
    
    tEvent.Branch('Electrons_minDeltaRJets', 'std::vector<double>', var_Electrons_minDeltaRJets)
    tEvent.Branch('Electrons_closestJet', 'std::vector<int>', var_Electrons_closestJet)

    tEvent.Branch('Electrons_correctedMinDeltaRJets', 'std::vector<double>', var_Electrons_correctedMinDeltaRJets)
    tEvent.Branch('Electrons_correctedClosestJet', 'std::vector<int>', var_Electrons_correctedClosestJet)
    
    tEvent.Branch('Muons', 'std::vector<TLorentzVector>', var_Muons)
    tEvent.Branch('Muons_charge', 'std::vector<int>', var_Muons_charge)
    tEvent.Branch('Muons_mediumID', 'std::vector<bool>', var_Muons_mediumID)
    tEvent.Branch('Muons_passIso', 'std::vector<bool>', var_Muons_passIso)
    tEvent.Branch('Muons_tightID', 'std::vector<bool>', var_Muons_tightID)
    
    tEvent.Branch('Muons_MiniIso', 'std::vector<double>', var_Muons_MiniIso)
    tEvent.Branch('Muons_MT2Activity', 'std::vector<double>', var_Muons_MT2Activity)
    tEvent.Branch('Muons_MTW', 'std::vector<double>', var_Muons_MTW)
    
    tEvent.Branch('Muons_deltaRLJ', 'std::vector<double>', var_Muons_deltaRLJ)
    tEvent.Branch('Muons_deltaPhiLJ', 'std::vector<double>', var_Muons_deltaPhiLJ)
    tEvent.Branch('Muons_deltaEtaLJ', 'std::vector<double>', var_Muons_deltaEtaLJ)
    
    tEvent.Branch('Muons_matchGen', 'std::vector<bool>', var_Muons_matchGen)
    
    tEvent.Branch('Muons_minDeltaRJets', 'std::vector<double>', var_Muons_minDeltaRJets)
    tEvent.Branch('Muons_closestJet', 'std::vector<int>', var_Muons_closestJet)
    
    tEvent.Branch('Muons_correctedMinDeltaRJets', 'std::vector<double>', var_Muons_correctedMinDeltaRJets)
    tEvent.Branch('Muons_correctedClosestJet', 'std::vector<int>', var_Muons_correctedClosestJet)

    tEvent.Branch('vetoElectronsPassIso', var_vetoElectronsPassIso,'vetoElectronsPassIso/O')
    #tEvent.Branch('vetoElectronsPassJetIso', var_vetoElectronsPassJetIso,'vetoElectronsPassJetIso/O')
    tEvent.Branch('vetoElectronsMediumID', var_vetoElectronsMediumID,'vetoElectronsMediumID/O')
    tEvent.Branch('vetoElectronsTightID', var_vetoElectronsTightID,'vetoElectronsTightID/O')
    
    tEvent.Branch('vetoMuonsPassIso', var_vetoMuonsPassIso,'vetoMuonsPassIso/O')
    #tEvent.Branch('vetoMuonsPassJetIso', var_vetoMuonsPassJetIso,'vetoMuonsPassJetIso/O')
    tEvent.Branch('vetoMuonsMediumID', var_vetoMuonsMediumID,'vetoMuonsMediumID/O')
    tEvent.Branch('vetoMuonsTightID', var_vetoMuonsTightID,'vetoMuonsTightID/O')
    
    if signal:
        tEvent.Branch('Electrons_isZ', 'std::vector<bool>', var_Electrons_isZ)
        tEvent.Branch('Muons_isZ', 'std::vector<bool>', var_Muons_isZ)
        tEvent.Branch('genFlavour', 'std::string', var_genFlavour)
    if dy:
        tEvent.Branch('DYMuons', 'std::vector<TLorentzVector>', var_DYMuons)
        tEvent.Branch('DYMuons_charge', 'std::vector<int>', var_DYMuons_charge)
        tEvent.Branch('DYMuons_mediumID', 'std::vector<bool>', var_DYMuons_mediumID)
        tEvent.Branch('DYMuons_passIso', 'std::vector<bool>', var_DYMuons_passIso)
        tEvent.Branch('DYMuons_tightID', 'std::vector<bool>', var_DYMuons_tightID)
        tEvent.Branch('DYMuons_MiniIso', 'std::vector<double>', var_DYMuons_MiniIso)
        tEvent.Branch('DYMuons_MT2Activity', 'std::vector<double>', var_DYMuons_MT2Activity)
        tEvent.Branch('DYMuons_MTW', 'std::vector<double>', var_DYMuons_MTW)
        tEvent.Branch('DYMuonsSum', 'TLorentzVector', var_DYMuonsSum)
        tEvent.Branch('DYMuonsInvMass', var_DYMuonsInvMass,'DYMuonsInvMass/D')
    
    tEvent.Branch('GenParticles', 'std::vector<TLorentzVector>', var_GenParticles)
    tEvent.Branch('GenParticles_ParentId', 'std::vector<int>', var_GenParticles_ParentId)
    tEvent.Branch('GenParticles_ParentIdx', 'std::vector<int>', var_GenParticles_ParentIdx)
    tEvent.Branch('GenParticles_PdgId', 'std::vector<int>', var_GenParticles_PdgId)
    tEvent.Branch('GenParticles_Status', 'std::vector<int>', var_GenParticles_Status)

    tEvent.Branch('Jets', 'std::vector<TLorentzVector>', var_Jets)
    tEvent.Branch('Jets_bDiscriminatorCSV', 'std::vector<double>', var_Jets_bDiscriminatorCSV)
    tEvent.Branch('Jets_bJetTagDeepCSVBvsAll', 'std::vector<double>', var_Jets_bJetTagDeepCSVBvsAll)
    
    tEvent.Branch('Jets_electronEnergyFraction', 'std::vector<double>', var_Jets_electronEnergyFraction)
    tEvent.Branch('Jets_muonEnergyFraction', 'std::vector<double>', var_Jets_muonEnergyFraction)
    
    tEvent.Branch('Jets_muonMultiplicity', 'std::vector<int>', var_Jets_muonMultiplicity)
    tEvent.Branch('Jets_multiplicity', 'std::vector<int>', var_Jets_multiplicity)
    tEvent.Branch('Jets_electronMultiplicity', 'std::vector<int>', var_Jets_electronMultiplicity)
    
    tEvent.Branch('Jets_muonCorrected', 'std::vector<TLorentzVector>', var_Jets_muonCorrected)
    tEvent.Branch('Jets_electronCorrected', 'std::vector<TLorentzVector>', var_Jets_electronCorrected)

    tEvent.Branch('LeadingJetPartonFlavor', var_LeadingJetPartonFlavor,'LeadingJetPartonFlavor/I')
    tEvent.Branch('LeadingJetQgLikelihood', var_LeadingJetQgLikelihood,'LeadingJetQgLikelihood/D')
    tEvent.Branch('LeadingJetMinDeltaRMuons', var_LeadingJetMinDeltaRMuons,'LeadingJetMinDeltaRMuons/D')
    tEvent.Branch('LeadingJetMinDeltaRElectrons', var_LeadingJetMinDeltaRElectrons,'LeadingJetMinDeltaRElectrons/D')
    
    tEvent.Branch('MinDeltaPhiMetJets', var_MinDeltaPhiMetJets,'MinDeltaPhiMetJets/D')
    tEvent.Branch('MinDeltaPhiMhtJets', var_MinDeltaPhiMhtJets,'MinDeltaPhiMhtJets/D')
    tEvent.Branch('LeadingJetPt', var_LeadingJetPt,'LeadingJetPt/D')
      
    for lep in ["Muons", "Electrons"]:
        for CorrJetObs in utils.leptonIsolationList:
            ptRanges = [""]
            if CorrJetObs == "CorrJetIso":
                 ptRanges = utils.leptonCorrJetIsoPtRange
            for ptRange in ptRanges:
                print("tEvent.Branch(" + lep + "_pass" + CorrJetObs + str(ptRange), 'std::vector<' + str(utils.leptonsCorrJetVecList[CorrJetObs]) + '>', leptonsCorrJetVars[lep + "_pass" + CorrJetObs + str(ptRange)], ")")
                tEvent.Branch(lep + "_pass" +  CorrJetObs + str(ptRange), 'std::vector<' + utils.leptonsCorrJetVecList[CorrJetObs] + '>', leptonsCorrJetVars[lep + "_pass" + CorrJetObs + str(ptRange)])
            
    ###### Tracks #######
    tEvent.Branch('tracks', 'std::vector<TLorentzVector>', var_tracks)
    tEvent.Branch('tracks_charge', 'std::vector<int>', var_tracks_charge)
    tEvent.Branch('tracks_chi2perNdof', 'std::vector<double>', var_tracks_chi2perNdof)
    tEvent.Branch('tracks_dxyVtx', 'std::vector<double>', var_tracks_dxyVtx)
    tEvent.Branch('tracks_dzVtx', 'std::vector<double>', var_tracks_dzVtx)
    tEvent.Branch('tracks_trackJetIso', 'std::vector<double>', var_tracks_trackJetIso)
    #tEvent.Branch('tracks_trackLeptonIso', 'std::vector<double>', var_tracks_trackLeptonIso)
    tEvent.Branch('tracks_trkMiniRelIso', 'std::vector<double>', var_tracks_trkMiniRelIso)
    tEvent.Branch('tracks_trkRelIso', 'std::vector<double>', var_tracks_trkRelIso)
    tEvent.Branch('tracks_trackQualityHighPurity', 'std::vector<bool>', var_tracks_trackQualityHighPurity)
    
    tEvent.Branch('LeadingJet', 'TLorentzVector', var_LeadingJet)
    
    tEvent.Branch('MinCsv30', var_MinCsv30,'MinCsv30/D')
    tEvent.Branch('MinCsv25', var_MinCsv25,'MinCsv25/D')
    tEvent.Branch('MaxCsv30', var_MaxCsv30,'MaxCsv30/D')
    tEvent.Branch('MaxCsv25', var_MaxCsv25,'MaxCsv25/D')
    
    tEvent.Branch('MinDeepCsv30', var_MinDeepCsv30,'MinDeepCsv30/D')
    tEvent.Branch('MinDeepCsv25', var_MinDeepCsv25,'MinDeepCsv25/D')
    tEvent.Branch('MaxDeepCsv30', var_MaxDeepCsv30,'MaxDeepCsv30/D')
    tEvent.Branch('MaxDeepCsv25', var_MaxDeepCsv25,'MaxDeepCsv25/D')
    
    tEvent.Branch('category', var_category,'vetoMuonsTightID/O')
    
    for iso in utils.leptonIsolationList:
        for cat in utils.leptonIsolationCategories:
            ptRanges = [""]
            if iso == "CorrJetIso":
                ptRanges = utils.leptonCorrJetIsoPtRange
            for ptRange in ptRanges:
                for vecObs in utils.dileptonObservablesVecList:
                    print("tEvent.Branch(" + vecObs + iso + str(ptRange) + cat, 'std::vector<' + utils.dileptonObservablesVecList[vecObs] + '>', dileptonVars[vecObs + iso + str(ptRange) + cat], ")")
                    tEvent.Branch(vecObs + iso + str(ptRange) + cat, 'std::vector<' + utils.dileptonObservablesVecList[vecObs] + '>', dileptonVars[vecObs + iso + str(ptRange) + cat])
                for stringObs in utils.dileptonObservablesStringList:
                    print("tEvent.Branch(" + stringObs + iso + str(ptRange) + cat, 'std::string', dileptonVars[stringObs + iso + str(ptRange) + cat],")")
                    tEvent.Branch(stringObs + iso + str(ptRange) + cat, 'std::string', dileptonVars[stringObs + iso + str(ptRange) + cat])
                for DTypeObs in utils.dileptonObservablesDTypesList:
                    print("tEvent.Branch(" + DTypeObs + iso + str(ptRange) + cat, dileptonVars[DTypeObs + iso + str(ptRange) + cat],DTypeObs + iso + str(ptRange) + cat + "/" + utils.typeTranslation[utils.dileptonObservablesDTypesList[DTypeObs]], ")")
                    tEvent.Branch(DTypeObs + iso + str(ptRange) + cat, dileptonVars[DTypeObs + iso + str(ptRange) + cat],DTypeObs + iso + str(ptRange) + cat + "/" + utils.typeTranslation[utils.dileptonObservablesDTypesList[DTypeObs]])
    if not signal:
        tEvent.Branch('TriggerNames', 'std::vector<string>', var_triggerNames)
        tEvent.Branch('TriggerPass', 'std::vector<int>', var_triggerPass)
        tEvent.Branch('TriggerPrescales', 'std::vector<int>', var_triggerPrescales)
        tEvent.Branch('TriggerVersion', 'std::vector<int>', var_triggerVersion)

    chain = TChain('TreeMaker2/PreSelection')
    print("Opening", input_file)
    chain.Add(input_file)
    c = chain.CloneTree()
    chain = None
    print("Creating " + output_file)
    fnew = TFile(output_file,'recreate')
    print("Created.")

    hHt = TH1F('hHt','hHt',100,0,3000)
    hHtWeighted = TH1F('hHtWeighted','hHtWeighted',100,0,3000)
    hHtAfterMadHt = TH1F('hHtAfterMadHt','hHtAfterMadHt',100,0,3000)
    hHt.Sumw2()
    
    lumiSecs = LumiSectMap()
    
    nentries = c.GetEntries()
    print('Analysing', nentries, "entries")

    count = 0
    afterPreselection = 0
    afterMET = 0
    afterNj = 0
    afterLeptons = 0
    nLMap = {}
    nLGenMap = {}
    nLGenMapZ = {}
    baseFileName = os.path.basename(input_file)
    crossSection = 1
    if signal:
        if sam:
            chiM = os.path.basename(input_file).split("_")[2]
            print("Got chiM=" + chiM)
            crossSection = utils.samCrossSections.get(chiM)
            print("Cross Section is", crossSection)
        else:
            filename = (os.path.basename(input_file).split("Chi20Chipm")[0]).replace("p", ".")
            crossSection = utils.getCrossSection(filename)
        if crossSection is None:
            if utils.crossSections.get(filename) is not None:
                crossSection = utils.crossSections.get(filename)
            else:
                crossSection = 1.21547
    elif bg and "DYJetsToLL_M-5to50_" in input_file:
        fileBasename = os.path.basename(input_file).split(".root")[0].split("RunIISummer16MiniAODv3.")[1].split("_TuneCUETP8M1")[0]
        print("Checking DY CS for", fileBasename)
        cs = utils.dyCrossSections.get(fileBasename)
        print("Got cs", cs)
    
    currLeptonCollectionMap = None
    currLeptonCollectionFileMapFile = None
    
    print("Starting Loop")
    for ientry in range(nentries):
        if ientry % 1000 == 0:
            print("Processing " + str(ientry))
        c.GetEntry(ientry)

        ### MADHT ###
        rightProcess = True
    
        if signal and not sam:
            rightProcess = analysis_ntuples.isX1X2X1Process(c)
        elif bg:
            if "DYJetsToLL_M-5to50_" not in input_file:
                crossSection = c.CrossSection
            rightProcess = utils.madHtCheck(baseFileName, c.madHT)
        elif data:
            lumiSecs.insert(c.RunNum, c.LumiBlockNum)

        hHt.Fill(c.HT)
        #print("crossSection=" + str(crossSection))
        hHtWeighted.Fill(c.HT, crossSection)

        if not rightProcess:
            continue
        
#         if madHTgt is not None and c.madHT < madHTgt:
#             print("Skipping because got madHTgt of", madHTgt, "but value is", c.madHT )
#             continue
#         elif if madHTlt is not None and c.madHT > madHTlt:
#             print("Skipping because got madHTlt of", madHTlt, "but value is", c.madHT )
#             continue
            
        count += 1
        if not data:
            hHtAfterMadHt.Fill(c.madHT)
        
        nL = c.Electrons.size() + c.Muons.size()
        nT = c.tracks.size()
    
        #### GEN LEVEL STUFF ####
        nLGen = 0
        nLGenZ = 0
        nX20 = 0
        branching_ratio = 1
        if not data:
            partSize = c.GenParticles.size()
            for ipart in range(partSize):
                if c.GenParticles_Status[ipart] == 1 and (abs(c.GenParticles_PdgId[ipart]) == 11 or abs(c.GenParticles_PdgId[ipart]) == 13):
                    nLGen += 1
                    if c.GenParticles_ParentId[ipart] == 1000023 or c.GenParticles_ParentId[ipart] == 23:
                        nLGenZ += 1
                if abs(c.GenParticles_PdgId[ipart]) == 1000023:
                    nX20 += 1
                
            
            if nLMap.get(nL) is not None:
                nLMap[nL] += 1
            else:
                nLMap[nL] = 1
            if nLGenMap.get(nLGen) is not None:
                nLGenMap[nLGen] += 1
            else:
                nLGenMap[nLGen] = 1
            if nLGenMapZ.get(nLGenZ) is not None:
                nLGenMapZ[nLGenZ] += 1
            else:
                nLGenMapZ[nLGenZ] = 1
            
            if nX20 > 0:
                #print("nX20", nX20, "nLGenZ", nLGenZ)
                if nX20 == 1 and nLGenZ == 2:
                    branching_ratio *= 0.2
                elif nX20 == 2 and nLGenZ == 4:
                    branching_ratio *= 0.04
                elif nX20 == 1 and nLGenZ == 0:
                    branching_ratio *= 1.8
                    #print("******", branching_ratio)
                elif nX20 == 2 and nLGenZ == 0:
                    branching_ratio *= 3.24
                    
        #### END OF GEN LEVEL STUFF ####
        
        var_BranchingRatio[0] = branching_ratio
        # if branching_ratio == 1.8:
#             print("YEY")
#         
        # if nX20 > 0:
#             if nX20 * 2 != nLGenZ:
#                 print("WTF", nX20, nLGenZ)
        
        # nX20 = 0
#         nX10 = 0
#         nX1pm = 0
#         susy = 0
#         susy_map = {}
#         susy_status = {}
#         partSize = c.GenParticles.size()
#         for ipart in range(partSize):
#             
#             if abs(c.GenParticles_PdgId[ipart]) == 1000023:
#                 nX20 += 1
#             if abs(c.GenParticles_PdgId[ipart]) == 1000022:
#                 nX10 += 1
#             if abs(c.GenParticles_PdgId[ipart]) == 1000024:
#                 nX1pm += 1
#             if  analysis_tools.isSusy(abs(c.GenParticles_PdgId[ipart])):
#                 susy += 1
#                 if susy_map.get(abs(c.GenParticles_PdgId[ipart])) is not None:
#                     susy_map[abs(c.GenParticles_PdgId[ipart])] +=1
#                     susy_status[abs(c.GenParticles_PdgId[ipart])].append(abs(c.GenParticles_Status[ipart]))
#                 else:
#                     susy_map[abs(c.GenParticles_PdgId[ipart])] = 1
#                     susy_status[abs(c.GenParticles_PdgId[ipart])] = []
#                     susy_status[abs(c.GenParticles_PdgId[ipart])].append(abs(c.GenParticles_Status[ipart]))
#         print(susy)
#         print(susy_map)
#         print(susy_status)
        
        
        
        #continue
#         if nX20>1:
#             print("MORE THAN 1!")
#         if nX20<1:
#             print("LESS THAN 1!", nX1pm, nX10)
#         if  nX1pm !=1:
#             print("nX1pm not 1", nX1pm, nX10)
#         if nX1pm == 0 and nX20 == 0 and nX10 == 0:
#             print("ALL 0!")
#         print("============")
#         continue
    
        var_NLGen[0] = nLGen
        var_NLGenZ[0] = nLGenZ
    
        #### PRECUTS ###
        if not signal:
            if not analysis_ntuples.passed2016BTrigger(c, data): continue
        
        MET = c.MET
        METPhi = c.METPhi
        MHT = c.MHT
        HT = c.HT
        MHTPhi = c.MHTPhi
        
        jets = c.Jets
        jets_bDiscriminatorCSV = c.Jets_bDiscriminatorCSV
        jets_bJetTagDeepCSVBvsAll = c.Jets_bJetTagDeepCSVBvsAll
        jets_electronEnergyFraction = c.Jets_electronEnergyFraction
        jets_muonEnergyFraction = c.Jets_muonEnergyFraction
        
        jets_muonMultiplicity = c.Jets_muonMultiplicity
        jets_multiplicity = c.Jets_multiplicity
        jets_electronMultiplicity = c.Jets_electronMultiplicity
        
        
        jets_partonFlavor = c.Jets_partonFlavor
        jets_qgLikelihood = c.Jets_qgLikelihood
        
        var_tracks = c.tracks
        var_tracks_charge = c.tracks_charge
        var_tracks_chi2perNdof = c.tracks_chi2perNdof
        var_tracks_dxyVtx = c.tracks_dxyVtx
        var_tracks_dzVtx = c.tracks_dzVtx
        var_tracks_trackJetIso = c.tracks_trackJetIso
        #var_tracks_trackLeptonIso = c.tracks_trackLeptonIso
        var_tracks_trkMiniRelIso = c.tracks_trkMiniRelIso
        var_tracks_trkRelIso = c.tracks_trkRelIso
        var_tracks_trackQualityHighPurity = c.tracks_trackQualityHighPurity
        
        muons = []
        if dy:
           
            muons, invMass = getDyMuons(c)
            if muons is None:
                continue
            
            metVec = TLorentzVector()
            metVec.SetPtEtaPhiE(MET,0,METPhi,MET)
            
            metVec += c.Muons[muons[0]]
            metVec += c.Muons[muons[1]]
            
            MET = abs(metVec.Pt())
            
            if MET > 3000:
                print("HERE WE GO!!!")
                print("c.MET=", c.MET, "metVec=", metVec.Pt(), "MET=", MET)
                print("c.Muons[muons[0]].Pt()=", c.Muons[muons[0]].Pt(), "c.Muons[muons[1]].Pt()=", c.Muons[muons[1]].Pt())
                print("-------")
            
            METPhi = metVec.Phi()
            
            jetsHt = [i for i in range(len(c.Jets)) if c.Jets[i].Pt() >= 30 and abs(c.Jets[i].Eta()) <= 2.4 and abs(c.Muons[muons[0]].DeltaR(c.Jets[i])) > 0.1 and abs(c.Muons[muons[1]].DeltaR(c.Jets[i])) > 0.1]
            jetsMht = [i for i in range(len(c.Jets)) if c.Jets[i].Pt() >= 30 and abs(c.Jets[i].Eta()) <= 5 and abs(c.Muons[muons[0]].DeltaR(c.Jets[i])) > 0.1 and abs(c.Muons[muons[1]].DeltaR(c.Jets[i])) > 0.1]
            
            #print("jetsHt=", jetsHt)
            #print("jetsMht=", jetsMht)
            
            HT = 0
            for i in jetsHt:
                HT += c.Jets[i].Pt()
            MhtVec = TLorentzVector()
            metVec.SetPtEtaPhiE(0,0,0,0)
            for i in jetsMht:
                MhtVec -= c.Jets[i]
            MHT = MhtVec.Pt()
            MHTPhi = MhtVec.Phi()
            
            jets = ROOT.std.vector(TLorentzVector)()
            jets_bDiscriminatorCSV = ROOT.std.vector(double)()
            jets_bJetTagDeepCSVBvsAll = ROOT.std.vector(double)()
            
            jets_electronEnergyFraction = ROOT.std.vector(double)()
            jets_muonEnergyFraction = ROOT.std.vector(double)()
            
            jets_muonMultiplicity = ROOT.std.vector(int)()
            jets_multiplicity = ROOT.std.vector(int)()
            jets_electronMultiplicity = ROOT.std.vector(int)()
            
            jets_partonFlavor = ROOT.std.vector(int)()
            jets_qgLikelihood = ROOT.std.vector(double)()
            
            for i in range(c.Jets.size()):
                if abs(c.Muons[muons[0]].DeltaR(c.Jets[i])) > 0.1 and abs(c.Muons[muons[1]].DeltaR(c.Jets[i])) > 0.1:
                    jets.push_back(c.Jets[i])
                    jets_bDiscriminatorCSV.push_back(c.Jets_bDiscriminatorCSV[i])
                    jets_bJetTagDeepCSVBvsAll.push_back(c.Jets_bJetTagDeepCSVBvsAll[i])
                    jets_electronEnergyFraction.push_back(c.Jets_electronEnergyFraction[i])
                    jets_muonEnergyFraction.push_back(c.Jets_muonEnergyFraction[i])
                    jets_partonFlavor.push_back(c.Jets_partonFlavor[i])
                    jets_qgLikelihood.push_back(c.Jets_qgLikelihood[i])
                    jets_muonMultiplicity.push_back(c.Jets_muonMultiplicity[i])
                    jets_multiplicity.push_back(c.Jets_multiplicity[i])
                    jets_electronMultiplicity.push_back(c.Jets_electronMultiplicity[i])
            
            var_tracks          = ROOT.std.vector(TLorentzVector)()
            var_tracks_charge   = ROOT.std.vector(int)()
            var_tracks_chi2perNdof = ROOT.std.vector(double)()
            var_tracks_dxyVtx   = ROOT.std.vector(double)()
            var_tracks_dzVtx    = ROOT.std.vector(double)()
            var_tracks_trackJetIso = ROOT.std.vector(double)()
            var_tracks_trkMiniRelIso = ROOT.std.vector(double)()
            var_tracks_trkRelIso = ROOT.std.vector(double)()
            var_tracks_trackQualityHighPurity = ROOT.std.vector(bool)()
            
            for i in range(c.tracks.size()):
                if abs(c.Muons[muons[0]].DeltaR(c.tracks[i])) > 0.01 and abs(c.Muons[muons[1]].DeltaR(c.tracks[i])) > 0.01:
                    var_tracks.push_back(c.tracks[i])
                    var_tracks_charge.push_back(c.tracks_charge[i])
                    var_tracks_chi2perNdof.push_back(c.tracks_chi2perNdof[i])
                    var_tracks_dxyVtx.push_back(c.tracks_dxyVtx[i])
                    var_tracks_dzVtx.push_back(c.tracks_dzVtx[i])
                    var_tracks_trackJetIso.push_back(c.tracks_trackJetIso[i])
                    var_tracks_trkMiniRelIso.push_back(c.tracks_trkMiniRelIso[i])
                    var_tracks_trkRelIso.push_back(c.tracks_trkRelIso[i])
                    var_tracks_trackQualityHighPurity.push_back(bool(c.tracks_trackQualityHighPurity[i]))
        
        nj, btagsLoose, ljet = analysis_ntuples.eventNumberOfJets25Pt2_4Eta_Loose(jets, jets_bDiscriminatorCSV)
        nj, btagsMedium, ljet = analysis_ntuples.eventNumberOfJets25Pt2_4Eta_Medium(jets, jets_bDiscriminatorCSV)
        nj, btagsDeepLoose, ljet = analysis_ntuples.eventNumberOfJets25Pt2_4Eta_DeepLoose(jets, jets_bJetTagDeepCSVBvsAll)
        nj, btagsDeepMedium, ljet = analysis_ntuples.eventNumberOfJets25Pt2_4Eta_DeepMedium(jets, jets_bJetTagDeepCSVBvsAll)
        
        if ljet is None:
            #print("No ljet:",ljet )
            continue
            
        if no_lepton_selection and btagsDeepMedium > 0:
            continue
        
        afterNj += 1
        
        #if not duoLepton: continue
        var_MinDeltaPhiMetJets[0] = analysis_ntuples.eventMinDeltaPhiMetJets25Pt2_4Eta(jets, MET, METPhi)
        var_MinDeltaPhiMhtJets[0] = analysis_ntuples.eventMinDeltaPhiMhtJets25Pt2_4Eta(jets, MHT, MHTPhi)
        #if not dy:
        if var_MinDeltaPhiMetJets[0] < 0.4: continue
        if MHT < 100: continue
        if MET < 120: continue
        #Keep 2 b-tags for two-leptons
        # if two_leptons:
#             if btags > 2: continue
#         else:
#             if btags > 0: continue
                
        ## END PRECUTS##
        
        afterMET += 1
        #if btags > 0: continue
        
        #if nj < 1: continue
        
        #nj, btags, ljet = analysis_ntuples.numberOfJets25Pt2_4Eta_Loose(c)
        
        var_RunNum[0] = c.RunNum
        var_LumiBlockNum[0] = c.LumiBlockNum
        var_EvtNum[0] = c.EvtNum

        var_Met[0] = MET
        var_METPhi[0] = METPhi
        var_Mht[0] = MHT
        var_MHTPhi[0] = MHTPhi
        var_Ht[0] = HT
        var_Mt2[0] = c.MT2
        var_CrossSection[0] = crossSection
        var_NJets[0] = nj
        var_BTagsLoose[0] = btagsLoose
        var_BTagsMedium[0] = btagsMedium
        var_BTagsDeepLoose[0] = btagsDeepLoose
        var_BTagsDeepMedium[0] = btagsDeepMedium
        
        var_LeadingJetPt[0] = jets[ljet].Pt()
        var_LeadingJet = jets[ljet]

        var_MinCsv30[0], var_MaxCsv30[0] = analysis_ntuples.minMaxCsv(jets, jets_bDiscriminatorCSV, 30)
        var_MinCsv25[0], var_MaxCsv25[0] = analysis_ntuples.minMaxCsv(jets, jets_bDiscriminatorCSV, 25)
        
        var_MinDeepCsv30[0], var_MaxDeepCsv30[0] = analysis_ntuples.minMaxCsv(jets, jets_bJetTagDeepCSVBvsAll, 30)
        var_MinDeepCsv25[0], var_MaxDeepCsv25[0] = analysis_ntuples.minMaxCsv(jets, jets_bJetTagDeepCSVBvsAll, 25)
        
        #if var_MaxCsv25[0] > 0.7:
        #    continue
        
        afterPreselection += 1
        
        if not data:
            var_puWeight[0] = c.puWeight
            var_madHT[0] = c.madHT
        else:
            var_puWeight[0] = 1
            var_madHT[0] = 1
        
        takeLeptonsFrom = None
        
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
            # takeLeptonsFrom["Electrons"] = c.Electrons
#             takeLeptonsFrom["Electrons_charge"] = c.Electrons_charge
#             takeLeptonsFrom["Electrons_mediumID"] = c.Electrons_mediumID
#             takeLeptonsFrom["Electrons_passIso"] = c.Electrons_passIso
#             takeLeptonsFrom["Electrons_tightID"] = c.Electrons_tightID
#             takeLeptonsFrom["Electrons_EnergyCorr"] = c.Electrons_EnergyCorr
#             takeLeptonsFrom["Electrons_MiniIso"] = c.Electrons_MiniIso
#             takeLeptonsFrom["Electrons_MT2Activity"] = c.Electrons_MT2Activity
#             takeLeptonsFrom["Electrons_MTW"] = c.Electrons_MTW
#             takeLeptonsFrom["Electrons_TrkEnergyCorr"] = c.Electrons_TrkEnergyCorr
#         
#             takeLeptonsFrom["Muons"] = c.Muons
#             takeLeptonsFrom["Muons_charge"] = c.Muons_charge
#             takeLeptonsFrom["Muons_mediumID"] = c.Muons_mediumID
#             takeLeptonsFrom["Muons_passIso"] = c.Muons_passIso
#             takeLeptonsFrom["Muons_tightID"] = c.Muons_tightID
#             takeLeptonsFrom["Muons_MiniIso"] = c.Muons_MiniIso
#             takeLeptonsFrom["Muons_MT2Activity"] = c.Muons_MT2Activity
#             takeLeptonsFrom["Muons_MTW"] = c.Muons_MTW
             
        if dy:
            #print("muons=", muons)
            muons, invMass = getDyMuons(takeLeptonsFrom)
            if muons is None:
                print("WHAT IS GOING ON?")
            
            var_DYMuons = ROOT.std.vector(TLorentzVector)()
            var_DYMuons_charge = ROOT.std.vector(int)()
            var_DYMuons_mediumID = ROOT.std.vector(bool)()
            var_DYMuons_passIso = ROOT.std.vector(bool)()
            var_DYMuons_tightID = ROOT.std.vector(bool)()
            var_DYMuons_MiniIso = ROOT.std.vector(double)()
            var_DYMuons_MT2Activity = ROOT.std.vector(double)()
            var_DYMuons_MTW = ROOT.std.vector(double)()
            
            var_DYMuons.push_back(takeLeptonsFrom.Muons[muons[0]])
            var_DYMuons.push_back(takeLeptonsFrom.Muons[muons[1]])
            
            var_DYMuonsSum = takeLeptonsFrom.Muons[muons[0]] + takeLeptonsFrom.Muons[muons[1]]
            var_DYMuonsInvMass[0] = var_DYMuonsSum.M()
            
            var_DYMuons_charge.push_back(takeLeptonsFrom.Muons_charge[muons[0]])
            var_DYMuons_charge.push_back(takeLeptonsFrom.Muons_charge[muons[1]])
            
            var_DYMuons_mediumID.push_back(bool(takeLeptonsFrom.Muons_mediumID[muons[0]]))
            var_DYMuons_mediumID.push_back(bool(takeLeptonsFrom.Muons_mediumID[muons[1]]))
            
            var_DYMuons_passIso.push_back(bool(takeLeptonsFrom.Muons_passIso[muons[0]]))
            var_DYMuons_passIso.push_back(bool(takeLeptonsFrom.Muons_passIso[muons[1]]))
            
            var_DYMuons_tightID.push_back(bool(takeLeptonsFrom.Muons_tightID[muons[0]]))
            var_DYMuons_tightID.push_back(bool(takeLeptonsFrom.Muons_tightID[muons[1]]))
            
            var_DYMuons_MiniIso.push_back(takeLeptonsFrom.Muons_MiniIso[muons[0]])
            var_DYMuons_MiniIso.push_back(takeLeptonsFrom.Muons_MiniIso[muons[1]])
            
            var_DYMuons_MT2Activity.push_back(takeLeptonsFrom.Muons_MT2Activity[muons[0]])
            var_DYMuons_MT2Activity.push_back(takeLeptonsFrom.Muons_MT2Activity[muons[1]])
            
            var_DYMuons_MTW.push_back(takeLeptonsFrom.Muons_MTW[muons[0]])
            var_DYMuons_MTW.push_back(takeLeptonsFrom.Muons_MTW[muons[1]])
            
            var_Muons = ROOT.std.vector(TLorentzVector)()
            var_Muons_charge = ROOT.std.vector(int)()
            var_Muons_mediumID = ROOT.std.vector(bool)()
            var_Muons_passIso = ROOT.std.vector(bool)()
            var_Muons_tightID = ROOT.std.vector(bool)()
            var_Muons_MiniIso = ROOT.std.vector(double)()
            var_Muons_MT2Activity = ROOT.std.vector(double)()
            var_Muons_MTW = ROOT.std.vector(double)()
            
            for i in range(takeLeptonsFrom.Muons.size()):
                if i != muons[0] and i != muons[1]:
                    var_Muons.push_back(takeLeptonsFrom.Muons[i])
                    var_Muons_charge.push_back(takeLeptonsFrom.Muons_charge[i])
                    var_Muons_mediumID.push_back(bool(takeLeptonsFrom.Muons_mediumID[i]))
                    var_Muons_passIso.push_back(bool(takeLeptonsFrom.Muons_passIso[i]))
                    var_Muons_tightID.push_back(bool(takeLeptonsFrom.Muons_tightID[i]))
                    var_Muons_MiniIso.push_back(takeLeptonsFrom.Muons_MiniIso[i])
                    var_Muons_MT2Activity.push_back(takeLeptonsFrom.Muons_MT2Activity[i])
                    var_Muons_MTW.push_back(takeLeptonsFrom.Muons_MTW[i])
            
            takeLeptonsFrom.Muons = var_Muons
            takeLeptonsFrom.Muons_charge = var_Muons_charge
            takeLeptonsFrom.Muons_mediumID = var_Muons_mediumID
            takeLeptonsFrom.Muons_passIso = var_Muons_passIso
            takeLeptonsFrom.Muons_tightID = var_Muons_tightID
            takeLeptonsFrom.Muons_MiniIso = var_Muons_MiniIso
            takeLeptonsFrom.Muons_MT2Activity = var_Muons_MT2Activity
            takeLeptonsFrom.Muons_MTW = var_Muons_MTW
        
        var_Electrons = takeLeptonsFrom.Electrons
        var_Electrons_charge= takeLeptonsFrom.Electrons_charge
        var_Electrons_mediumID = takeLeptonsFrom.Electrons_mediumID
        var_Electrons_passIso = takeLeptonsFrom.Electrons_passIso
        var_Electrons_tightID = takeLeptonsFrom.Electrons_tightID
        var_Electrons_EnergyCorr = takeLeptonsFrom.Electrons_EnergyCorr
        var_Electrons_MiniIso = takeLeptonsFrom.Electrons_MiniIso
        var_Electrons_MT2Activity = takeLeptonsFrom.Electrons_MT2Activity
        var_Electrons_MTW = takeLeptonsFrom.Electrons_MTW
        var_Electrons_TrkEnergyCorr = takeLeptonsFrom.Electrons_TrkEnergyCorr
        
        var_Muons = takeLeptonsFrom.Muons
        var_Muons_charge = takeLeptonsFrom.Muons_charge
        var_Muons_mediumID = takeLeptonsFrom.Muons_mediumID
        var_Muons_passIso = takeLeptonsFrom.Muons_passIso
        var_Muons_tightID = takeLeptonsFrom.Muons_tightID
        var_Muons_MiniIso = takeLeptonsFrom.Muons_MiniIso
        var_Muons_MT2Activity = takeLeptonsFrom.Muons_MT2Activity
        var_Muons_MTW = takeLeptonsFrom.Muons_MTW
        
        var_Jets = jets
        var_Jets_bDiscriminatorCSV = jets_bDiscriminatorCSV
        var_Jets_bJetTagDeepCSVBvsAll = jets_bJetTagDeepCSVBvsAll
        var_Jets_electronEnergyFraction = jets_electronEnergyFraction
        var_Jets_muonEnergyFraction = jets_muonEnergyFraction
        
        
        var_Jets_muonMultiplicity = jets_muonMultiplicity
        var_Jets_multiplicity = jets_multiplicity
        var_Jets_electronMultiplicity = jets_electronMultiplicity
        
        # var_Jets_minDeltaRElectrons = ROOT.std.vector(double)()
#         var_Jets_minDeltaRMuons = ROOT.std.vector(double)()

        # loose_electrons = [ var_Electrons[i] for i in range(var_Electrons.size()) if analysis_ntuples.electronPassesLooseSelection(i, var_Electrons, var_Electrons_passIso) ]
#         medium_muons = [ var_Muons[i] for i in range(var_Muons.size()) if analysis_ntuples.muonPassesLooseSelection(i, var_Muons, var_Muons_mediumID) ]
#         
#         for i in range(var_Jets.size()):
#             jet = var_Jets[i]
#             min, minCan = analysis_ntuples.minDeltaLepLeps(var_Jets[i], loose_electrons)
#             var_Jets_minDeltaRElectrons.push_back(min if min is not None else -1)
#             min, minCan = analysis_ntuples.minDeltaLepLeps(var_Jets[i], medium_muons)
#             var_Jets_minDeltaRMuons.push_back(min if min is not None else -1)
        
        var_NL[0] = nL
        
        if data:
            var_GenParticles = ROOT.std.vector(TLorentzVector)()
            var_GenParticles_ParentId = ROOT.std.vector(int)()
            var_GenParticles_ParentIdx = ROOT.std.vector(int)()
            var_GenParticles_PdgId = ROOT.std.vector(int)()
            var_GenParticles_Status = ROOT.std.vector(int)()
        else:
            var_GenParticles = c.GenParticles
            var_GenParticles_ParentId = c.GenParticles_ParentId
            var_GenParticles_ParentIdx = c.GenParticles_ParentIdx
            var_GenParticles_PdgId = c.GenParticles_PdgId
            var_GenParticles_Status = c.GenParticles_Status
        
        if not signal:
            var_triggerNames = c.TriggerNames
            var_triggerPass = c.TriggerPass
            var_triggerPrescales = c.TriggerPrescales
            var_triggerVersion = c.TriggerVersion
    
        tEvent.SetBranchAddress('Electrons', var_Electrons)
        tEvent.SetBranchAddress('Electrons_charge', var_Electrons_charge)
        tEvent.SetBranchAddress('Muons', var_Muons)
        tEvent.SetBranchAddress('Muons_charge', var_Muons_charge)
        
        tEvent.SetBranchAddress('Electrons_mediumID', var_Electrons_mediumID)
        tEvent.SetBranchAddress('Electrons_passIso', var_Electrons_passIso)
        tEvent.SetBranchAddress('Electrons_tightID', var_Electrons_tightID)
        
        tEvent.SetBranchAddress('Electrons_EnergyCorr', var_Electrons_EnergyCorr)
        tEvent.SetBranchAddress('Electrons_MiniIso', var_Electrons_MiniIso)
        tEvent.SetBranchAddress('Electrons_MT2Activity', var_Electrons_MT2Activity)
        tEvent.SetBranchAddress('Electrons_MTW', var_Electrons_MTW)
        tEvent.SetBranchAddress('Electrons_TrkEnergyCorr', var_Electrons_TrkEnergyCorr)
        
        
        tEvent.SetBranchAddress('Muons_mediumID', var_Muons_mediumID)
        tEvent.SetBranchAddress('Muons_passIso', var_Muons_passIso)
        tEvent.SetBranchAddress('Muons_tightID', var_Muons_tightID)
        
        tEvent.SetBranchAddress('Muons_MiniIso', var_Muons_MiniIso)
        tEvent.SetBranchAddress('Muons_MT2Activity', var_Muons_MT2Activity)
        tEvent.SetBranchAddress('Muons_MTW', var_Muons_MTW)
        
        var_Electrons_deltaRLJ = ROOT.std.vector(double)()
        var_Electrons_deltaPhiLJ = ROOT.std.vector(double)()
        var_Electrons_deltaEtaLJ = ROOT.std.vector(double)()
    
        var_Muons_deltaRLJ = ROOT.std.vector(double)()
        var_Muons_deltaPhiLJ = ROOT.std.vector(double)()
        var_Muons_deltaEtaLJ = ROOT.std.vector(double)()
        
        for i in range(var_Electrons.size()):
            var_Electrons_deltaRLJ.push_back(var_Electrons[i].DeltaR(var_LeadingJet))
            var_Electrons_deltaPhiLJ.push_back(abs(var_Electrons[i].DeltaPhi(var_LeadingJet)))
            var_Electrons_deltaEtaLJ.push_back(abs(var_Electrons[i].Eta() - var_LeadingJet.Eta()))
            
        for i in range(var_Muons.size()):
            var_Muons_deltaRLJ.push_back(var_Muons[i].DeltaR(var_LeadingJet))
            var_Muons_deltaPhiLJ.push_back(abs(var_Muons[i].DeltaPhi(var_LeadingJet)))
            var_Muons_deltaEtaLJ.push_back(abs(var_Muons[i].Eta() - var_LeadingJet.Eta()))
        
        var_Electrons_matchGen = ROOT.std.vector(bool)()
        var_Muons_matchGen = ROOT.std.vector(bool)()
        
        if not data:
            genElectrons = [ var_GenParticles[i] for i in range(var_GenParticles.size()) if abs(var_GenParticles_PdgId[i]) == 11 ]
            genElectronsIdx = [ i for i in range(var_GenParticles.size()) if abs(var_GenParticles_PdgId[i]) == 11 ]
            genMuons = [ var_GenParticles[i] for i in range(var_GenParticles.size()) if abs(var_GenParticles_PdgId[i]) == 13]
            genMuonsIdx = [ i for i in range(var_GenParticles.size()) if abs(var_GenParticles_PdgId[i]) == 13]
            for i in range(var_Electrons.size()):
                signedGenElectrons = [ genElectrons[j] for j in range(len(genElectrons)) if var_GenParticles_PdgId[genElectronsIdx[j]] == -11 *  var_Electrons_charge[i] ]
                min, minCan = analysis_ntuples.minDeltaLepLeps(var_Electrons[i], signedGenElectrons)
                if min is None or min > 0.01:
                    var_Electrons_matchGen.push_back(False)
                else:
                    var_Electrons_matchGen.push_back(True)
            for i in range(var_Muons.size()):
                signedGenMuons = [ genMuons[j] for j in range(len(genMuons)) if var_GenParticles_PdgId[genMuonsIdx[j]] == -13 *  var_Muons_charge[i] ]
                min, minCan = analysis_ntuples.minDeltaLepLeps(var_Muons[i], signedGenMuons)
                if min is None or min > 0.01:
                    var_Muons_matchGen.push_back(False)
                else:
                    var_Muons_matchGen.push_back(True)
        
        tEvent.SetBranchAddress('Electrons_matchGen', var_Electrons_matchGen)
        tEvent.SetBranchAddress('Muons_matchGen', var_Muons_matchGen)
        
        tEvent.SetBranchAddress('Electrons_deltaRLJ', var_Electrons_deltaRLJ)
        tEvent.SetBranchAddress('Electrons_deltaPhiLJ', var_Electrons_deltaPhiLJ)
        tEvent.SetBranchAddress('Electrons_deltaEtaLJ', var_Electrons_deltaEtaLJ)
        
        tEvent.SetBranchAddress('Muons_deltaRLJ', var_Muons_deltaRLJ)
        tEvent.SetBranchAddress('Muons_deltaPhiLJ', var_Muons_deltaPhiLJ)
        tEvent.SetBranchAddress('Muons_deltaEtaLJ', var_Muons_deltaEtaLJ)
        
        var_Electrons_minDeltaRJets = ROOT.std.vector(double)()
        var_Electrons_closestJet = ROOT.std.vector(int)()
        var_Muons_minDeltaRJets = ROOT.std.vector(double)()
        var_Muons_closestJet = ROOT.std.vector(int)()
        
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
                elif lepIso == "JetIso":
                    isoJets[lep][lepIso] =  [var_Jets[j] for j in range(len(var_Jets)) if var_Jets_multiplicity[j] >=10 or eval("var_Jets_" + lep + "EnergyFraction")[j] <= (0.3 if lep == "electron" else 0.1)]
                elif lepIso == "NonJetIso":
                    isoJets[lep][lepIso] = var_Jets
        
        for lep in isoJets:
            
            leptonsVecName = "var_" + isoJets[lep]["obs"]
            leptonsVec = eval(leptonsVecName)
            
            for i in range(leptonsVec.size()):
                min, minCan = analysis_ntuples.minDeltaLepLeps(leptonsVec[i], var_Jets)
                if min is None:
                    eval(leptonsVecName + "_minDeltaRJets").push_back(-1)
                    eval(leptonsVecName + "_closestJet").push_back(-1)
                    leptonsCorrJetVars[isoJets[lep]["obs"] + "_passJetIso"].push_back(True)
                    leptonsCorrJetVars[isoJets[lep]["obs"] + "_passNonJetIso"].push_back(True)
                else:
                    eval(leptonsVecName + "_minDeltaRJets").push_back(min)
                    eval(leptonsVecName + "_closestJet").push_back(minCan)
        
                    min, minCan = analysis_ntuples.minDeltaLepLeps(leptonsVec[i], isoJets[lep]["JetIso"])
                    if min is None or min > 0.4:
                        leptonsCorrJetVars[isoJets[lep]["obs"] + "_passJetIso"].push_back(True)
                    else:
                        leptonsCorrJetVars[isoJets[lep]["obs"] + "_passJetIso"].push_back(False)
                    min, minCan = analysis_ntuples.minDeltaLepLeps(leptonsVec[i], var_Jets)
                    if min is None or min > 0.4:
                        leptonsCorrJetVars[isoJets[lep]["obs"] + "_passNonJetIso"].push_back(True)
                    else:
                        leptonsCorrJetVars[isoJets[lep]["obs"] + "_passNonJetIso"].push_back(False)
        
        var_Jets_muonCorrected = ROOT.std.vector(TLorentzVector)(var_Jets)
        var_Jets_electronCorrected = ROOT.std.vector(TLorentzVector)(var_Jets)
        
        non_iso_jet_electrons = [ i for i in range(len(var_Electrons)) if analysis_ntuples.electronPassesKinematicSelection(i, var_Electrons, var_Electrons_deltaRLJ) and var_Electrons_minDeltaRJets[i] >= 0 and var_Electrons_minDeltaRJets[i] < 0.4 ]
        non_iso_jet_muons = [ i for i in range(len(var_Muons)) if analysis_ntuples.muonPassesLooseSelection(i, var_Muons, var_Muons_mediumID, var_Muons_deltaRLJ)and var_Muons_minDeltaRJets[i] >= 0 and var_Muons_minDeltaRJets[i] < 0.4 ]
        
        for i in non_iso_jet_electrons:
            for j in range(len(var_Jets_electronCorrected)):
                if var_Jets_electronCorrected[j].DeltaR(var_Electrons[i]) < 0.4:
                    var_Jets_electronCorrected[j] -= var_Electrons[i]
        for i in non_iso_jet_muons:
            for j in range(len(var_Jets_muonCorrected)):
                if var_Jets_muonCorrected[j].DeltaR(var_Muons[i]) < 0.4:
                    var_Jets_muonCorrected[j] -= var_Muons[i]
        
        for lepIso in utils.leptonIsolationList:
            for lep in isoJets:
                if lepIso != "CorrJetIso":
                    continue
                for ptRange in utils.leptonCorrJetIsoPtRange:
                    isoJets[lep][str(ptRange)] = [eval("var_Jets_" + lep + "Corrected")[j] for j in range(len(eval("var_Jets_" + lep + "Corrected"))) if var_Jets_multiplicity[j] >=10 or (eval("var_Jets_" + lep + "Corrected")[j].E() > 0 and eval("var_Jets_" + lep + "Corrected")[j].Pt() > ptRange)]
        
        var_Electrons_correctedMinDeltaRJets = ROOT.std.vector(double)()
        var_Electrons_correctedClosestJet = ROOT.std.vector(int)()
        
        var_Muons_correctedMinDeltaRJets = ROOT.std.vector(double)()
        var_Muons_correctedClosestJet = ROOT.std.vector(int)()
          
        for lep in isoJets:
             
            leptonsVecName = "var_" + isoJets[lep]["obs"]
            leptonsVec = eval(leptonsVecName)
            
            for i in range(leptonsVec.size()):
                min, minCan = analysis_ntuples.minDeltaLepLeps(leptonsVec[i], eval("var_Jets_" + lep + "Corrected"))
                if min is None:
                    eval(leptonsVecName + "_correctedMinDeltaRJets").push_back(-1)
                    eval(leptonsVecName + "_correctedClosestJet").push_back(-1)
                    for ptRange in utils.leptonCorrJetIsoPtRange:
                        leptonsCorrJetVars[isoJets[lep]["obs"] + "_passCorrJetIso" + str(ptRange)].push_back(True)
                else:
                    eval(leptonsVecName + "_correctedMinDeltaRJets").push_back(min)
                    eval(leptonsVecName + "_correctedClosestJet").push_back(minCan)
                    
                    for ptRange in utils.leptonCorrJetIsoPtRange:
    
                        min, minCan = analysis_ntuples.minDeltaLepLeps(leptonsVec[i], isoJets[lep][str(ptRange)])
                        if min is None or min > 0.4:
                            leptonsCorrJetVars[isoJets[lep]["obs"] + "_passCorrJetIso" + str(ptRange)].push_back(True)
                        else:
                            leptonsCorrJetVars[isoJets[lep]["obs"] + "_passCorrJetIso" + str(ptRange)].push_back(False)
        
        tEvent.SetBranchAddress('Electrons_minDeltaRJets', var_Electrons_minDeltaRJets)
        tEvent.SetBranchAddress('Electrons_closestJet', var_Electrons_closestJet)

        tEvent.SetBranchAddress('Muons_minDeltaRJets', var_Muons_minDeltaRJets)
        tEvent.SetBranchAddress('Muons_closestJet', var_Muons_closestJet)

        tEvent.SetBranchAddress('Electrons_correctedMinDeltaRJets', var_Electrons_correctedMinDeltaRJets)
        tEvent.SetBranchAddress('Electrons_correctedClosestJet', var_Electrons_correctedClosestJet)

        tEvent.SetBranchAddress('Muons_correctedMinDeltaRJets', var_Muons_correctedMinDeltaRJets)
        tEvent.SetBranchAddress('Muons_correctedClosestJet', var_Muons_correctedClosestJet)
         
        for lep in ["Muons", "Electrons"]:
            for CorrJetObs in utils.leptonIsolationList:
                if CorrJetObs == "CorrJetIso":
                    for ptRange in utils.leptonCorrJetIsoPtRange:
                        tEvent.SetBranchAddress(lep + "_pass" + CorrJetObs + str(ptRange), leptonsCorrJetVars[lep + "_pass" + CorrJetObs + str(ptRange)])
                else:
                    #print(lep + "_pass" + CorrJetObs, leptonsCorrJetVars[lep + "_pass" + CorrJetObs])
                    tEvent.SetBranchAddress(lep + "_pass" + CorrJetObs, leptonsCorrJetVars[lep + "_pass" + CorrJetObs])
        
        tight_electrons = [ var_Electrons[i] for i in range(len(var_Electrons)) if analysis_ntuples.electronPassesTightSelection(i, var_Electrons, leptonsCorrJetVars["Electrons_passJetIso"], var_Electrons_deltaRLJ) ]
        tight_muons = [ var_Muons[i] for i in range(len(var_Muons)) if analysis_ntuples.muonPassesTightSelection(i, var_Muons, var_Muons_mediumID, leptonsCorrJetVars["Muons_passJetIso"], var_Muons_deltaRLJ) ]
        
        min, minCan = analysis_ntuples.minDeltaLepLeps(var_Jets[ljet], tight_electrons)
        if minCan is None:
            var_LeadingJetMinDeltaRElectrons[0] = -1
        else:
            var_LeadingJetMinDeltaRElectrons[0] = min
            
        min, minCan = analysis_ntuples.minDeltaLepLeps(var_Jets[ljet], tight_muons)
        if minCan is None:
            var_LeadingJetMinDeltaRMuons[0] = -1
        else:
            var_LeadingJetMinDeltaRMuons[0] = min
        
        for vecObs in utils.dileptonObservablesVecList:
            for iso in utils.leptonIsolationList:
                for cat in utils.leptonIsolationCategories:
                    if iso == "CorrJetIso":
                        for ptRange in utils.leptonCorrJetIsoPtRange:
                            dileptonVars[vecObs + iso + str(ptRange) + cat] = ROOT.std.vector(eval(utils.dileptonObservablesVecList[vecObs]))()
                    else:
                        dileptonVars[vecObs + iso + cat] = ROOT.std.vector(eval(utils.dileptonObservablesVecList[vecObs]))()
      
        foundTwoLeptons = False
        foundSingleLepton = False
        
        var_category[0] = 0
            
        for iso in utils.leptonIsolationList:
            for cat in utils.leptonIsolationCategories:
                ptRanges = [""]
                if iso == "CorrJetIso":
                    ptRanges = utils.leptonCorrJetIsoPtRange

                for ptRange in ptRanges:
                    
                    leptons, leptonsIdx, leptonsCharge, leptonFlavour = analysis_ntuples.getTwoLeptonsAfterSelection(var_Electrons, leptonsCorrJetVars["Electrons_pass" + iso + str(ptRange)], var_Electrons_deltaRLJ, var_Electrons_charge, var_Muons, leptonsCorrJetVars["Muons_pass" + iso + str(ptRange)], var_Muons_mediumID, var_Muons_deltaRLJ, var_Muons_charge, sc, utils.leptonIsolationCategories[cat]["muonPt"], utils.leptonIsolationCategories[cat]["lowPtTightMuons"], var_Muons_tightID)
                    
                    if leptons is None:
                        for DTypeObs in utils.dileptonObservablesDTypesList:
                            if DTypeObs == "twoLeptons":
                                dileptonVars[DTypeObs + iso + str(ptRange) + cat][0] = 0
                            else:
                                dileptonVars[DTypeObs + iso + str(ptRange) + cat][0] = -1
                            
                        ll, leptonIdx, leptonCharge, leptonFlavour = analysis_ntuples.getSingleLeptonAfterSelection(var_Electrons, leptonsCorrJetVars["Electrons_pass" + iso + str(ptRange)], var_Electrons_deltaRLJ, var_Electrons_charge, var_Muons, leptonsCorrJetVars["Muons_pass" + iso + str(ptRange)], var_Muons_mediumID, var_Muons_deltaRLJ, var_Muons_charge, utils.leptonIsolationCategories[cat]["muonPt"], utils.leptonIsolationCategories[cat]["lowPtTightMuons"], var_Muons_tightID)
                
                        if ll is not None:
                            if nT > 0 and var_BTagsLoose[0] == 0 or var_BTagsMedium[0] == 0 or var_BTagsDeepLoose[0] == 0 or var_BTagsDeepMedium[0] == 0:
                                var_category[0] = 1
                                foundSingleLepton = True
                    elif var_BTagsLoose[0] < 3 and var_BTagsMedium[0] < 3 and var_BTagsDeepLoose[0] < 3 and var_BTagsDeepMedium[0] < 3:
                        foundTwoLeptons = True  
                        
                        dileptonVars["leptons" + iso + str(ptRange) + cat].push_back(leptons[0])
                        dileptonVars["leptons" + iso + str(ptRange) + cat].push_back(leptons[1])
                        
                        dileptonVars["leptonsIdx" + iso + str(ptRange) + cat].push_back(leptonsIdx[0])
                        dileptonVars["leptonsIdx" + iso + str(ptRange) + cat].push_back(leptonsIdx[1])
                        
                        dileptonVars["leptons_charge" + iso + str(ptRange) + cat].push_back(leptonsCharge[0])
                        dileptonVars["leptons_charge" + iso + str(ptRange) + cat].push_back(leptonsCharge[1])
                        
                        dileptonVars["leptonFlavour" + iso + str(ptRange) + cat] = ROOT.std.string(leptonFlavour)
                        

                        dileptonVars["twoLeptons" + iso + str(ptRange) + cat][0] = 1
                        
                        pt = TLorentzVector()
                        pt.SetPtEtaPhiE(MET,0,METPhi,MET)
                        
                        dileptonVars["invMass" + iso + str(ptRange) + cat][0] =  (leptons[0] + leptons[1]).M()
                        dileptonVars["dileptonPt" + iso + str(ptRange) + cat][0] = abs((leptons[0] + leptons[1]).Pt())
                        dileptonVars["deltaPhi" + iso + str(ptRange) + cat][0] = abs(leptons[0].DeltaPhi(leptons[1]))
                        dileptonVars["deltaEta" + iso + str(ptRange) + cat][0] = abs(leptons[0].Eta() - leptons[1].Eta())
                        dileptonVars["deltaR" + iso + str(ptRange) + cat][0] = abs(leptons[0].DeltaR(leptons[1]))
                        dileptonVars["pt3" + iso + str(ptRange) + cat][0] = analysis_tools.pt3(leptons[0].Pt(),leptons[0].Phi(),leptons[1].Pt(),leptons[1].Phi(),MET,METPhi)
                        dileptonVars["mt1" + iso + str(ptRange) + cat][0] = analysis_tools.MT2(MET, METPhi, leptons[0])
                        dileptonVars["mt2" + iso + str(ptRange) + cat][0] = analysis_tools.MT2(MET, METPhi, leptons[1])
                        dileptonVars["mtautau" + iso + str(ptRange) + cat][0] = analysis_tools.Mtautau(pt, leptons[0], leptons[1])
                        dileptonVars["deltaEtaLeadingJetDilepton" + iso + str(ptRange) + cat][0] = abs((leptons[0] + leptons[1]).Eta() - jets[ljet].Eta())
                        dileptonVars["deltaPhiLeadingJetDilepton" + iso + str(ptRange) + cat][0] = abs((leptons[0] + leptons[1]).DeltaPhi(jets[ljet]))
                        dileptonVars["dilepHt" + iso + str(ptRange) + cat][0] = analysis_ntuples.htJet25Leps(jets, leptons)
                        dileptonVars["deltaPhiMetLepton1" + iso + str(ptRange) + cat][0] = abs(leptons[0].DeltaPhi(pt))
                        dileptonVars["deltaPhiMetLepton2" + iso + str(ptRange) + cat][0] = abs(leptons[1].DeltaPhi(pt))

                    for vecObs in utils.dileptonObservablesVecList:
                        #print("tEvent.Branch(" + vecObs + iso + str(ptRange) + cat, 'std::vector<' + utils.dileptonObservablesVecList[vecObs] + '>', dileptonVars[vecObs + iso + str(ptRange) + cat], ")")
                        tEvent.SetBranchAddress(vecObs + iso + str(ptRange) + cat, dileptonVars[vecObs + iso + str(ptRange) + cat])
                    for stringObs in utils.dileptonObservablesStringList:
                        #print("tEvent.Branch(" + stringObs + iso + str(ptRange) + cat, 'std::string', dileptonVars[stringObs + iso + str(ptRange) + cat],")")
                        tEvent.SetBranchAddress(stringObs + iso + str(ptRange) + cat, dileptonVars[stringObs + iso + str(ptRange) + cat])
        
        if not no_lepton_selection and not foundTwoLeptons and not foundSingleLepton:
            continue

        afterLeptons += 1
        
        var_vetoElectronsPassIso[0] = 0 if len([ i for i in range(len(var_Electrons)) if var_Electrons[i].Pt() > 25 and  bool(var_Electrons_passIso[i]) ]) == 0 else 1
        #var_vetoElectronsPassJetIso[0] = 0 if len([ i for i in range(len(var_Electrons)) if var_Electrons[i].Pt() > 25 and  bool(var_Electrons_passJetIso[i]) ]) == 0 else 1
        var_vetoElectronsMediumID[0] = 0 if len([ i for i in range(len(var_Electrons)) if var_Electrons[i].Pt() > 25 and  bool(var_Electrons_mediumID[i]) ]) == 0 else 1
        var_vetoElectronsTightID[0] = 0 if len([ i for i in range(len(var_Electrons)) if var_Electrons[i].Pt() > 25 and  bool(var_Electrons_tightID[i]) ]) == 0 else 1
        
        var_vetoMuonsPassIso[0] = 0 if len([ i for i in range(len(var_Muons)) if var_Muons[i].Pt() > 25 and  bool(var_Muons_passIso[i]) ]) == 0 else 1
        #var_vetoMuonsPassJetIso[0] = 0 if len([ i for i in range(len(var_Muons)) if var_Muons[i].Pt() > 25 and  bool(var_Muons_passJetIso[i]) ]) == 0 else 1
        var_vetoMuonsMediumID[0] = 0 if len([ i for i in range(len(var_Muons)) if var_Muons[i].Pt() > 25 and  bool(var_Muons_mediumID[i]) ]) == 0 else 1
        var_vetoMuonsTightID[0] = 0 if len([ i for i in range(len(var_Muons)) if var_Muons[i].Pt() > 25 and  bool(var_Muons_tightID[i]) ]) == 0 else 1
        
        if dy:
            
            tEvent.SetBranchAddress('DYMuons', var_DYMuons)
            tEvent.SetBranchAddress('DYMuons_charge', var_DYMuons_charge)
            tEvent.SetBranchAddress('DYMuonsSum', var_DYMuonsSum)
            
            tEvent.SetBranchAddress('DYMuons_mediumID', var_DYMuons_mediumID)
            tEvent.SetBranchAddress('DYMuons_passIso', var_DYMuons_passIso)
            tEvent.SetBranchAddress('DYMuons_tightID', var_DYMuons_tightID)
        
            tEvent.SetBranchAddress('DYMuons_MiniIso', var_DYMuons_MiniIso)
            tEvent.SetBranchAddress('DYMuons_MT2Activity', var_DYMuons_MT2Activity)
            tEvent.SetBranchAddress('DYMuons_MTW', var_DYMuons_MTW)

        tEvent.SetBranchAddress('GenParticles', var_GenParticles)
        tEvent.SetBranchAddress('GenParticles_ParentId', var_GenParticles_ParentId)
        tEvent.SetBranchAddress('GenParticles_Status', var_GenParticles_Status)
        tEvent.SetBranchAddress('GenParticles_ParentIdx', var_GenParticles_ParentIdx)
        tEvent.SetBranchAddress('GenParticles_PdgId', var_GenParticles_PdgId)
        tEvent.SetBranchAddress('Jets', var_Jets)
        tEvent.SetBranchAddress('Jets_bDiscriminatorCSV', var_Jets_bDiscriminatorCSV)
        tEvent.SetBranchAddress('Jets_bJetTagDeepCSVBvsAll', var_Jets_bJetTagDeepCSVBvsAll)
        tEvent.SetBranchAddress('Jets_electronEnergyFraction', var_Jets_electronEnergyFraction)
        tEvent.SetBranchAddress('Jets_muonEnergyFraction', var_Jets_muonEnergyFraction)
        #tEvent.SetBranchAddress('Jets_minDeltaRElectrons', var_Jets_minDeltaRElectrons)
        #tEvent.SetBranchAddress('Jets_minDeltaRMuons', var_Jets_minDeltaRMuons)
        tEvent.SetBranchAddress('Jets_muonMultiplicity', var_Jets_muonMultiplicity)
        tEvent.SetBranchAddress('Jets_multiplicity', var_Jets_multiplicity)
        tEvent.SetBranchAddress('Jets_electronMultiplicity', var_Jets_electronMultiplicity)
        
        tEvent.SetBranchAddress('Jets_muonCorrected', var_Jets_muonCorrected)
        tEvent.SetBranchAddress('Jets_electronCorrected', var_Jets_electronCorrected)

        tEvent.SetBranchAddress('tracks', var_tracks)
        tEvent.SetBranchAddress('tracks_charge', var_tracks_charge)
        tEvent.SetBranchAddress('tracks_chi2perNdof', var_tracks_chi2perNdof)
        tEvent.SetBranchAddress('tracks_dxyVtx', var_tracks_dxyVtx)
        tEvent.SetBranchAddress('tracks_dzVtx', var_tracks_dzVtx)
        tEvent.SetBranchAddress('tracks_trackJetIso', var_tracks_trackJetIso)
        #tEvent.SetBranchAddress('tracks_trackLeptonIso', var_tracks_trackLeptonIso)
        tEvent.SetBranchAddress('tracks_trkMiniRelIso', var_tracks_trkMiniRelIso)
        tEvent.SetBranchAddress('tracks_trkRelIso', var_tracks_trkRelIso)
        tEvent.SetBranchAddress('tracks_trackQualityHighPurity', var_tracks_trackQualityHighPurity)
        
        tEvent.SetBranchAddress('LeadingJet', var_LeadingJet)
        
        if signal:
            var_Electrons_isZ = ROOT.std.vector(bool)()
            var_Muons_isZ = ROOT.std.vector(bool)()
            
            genZL, genNonZL = analysis_ntuples.classifyGenZLeptons(c)
            
            if genZL is None:
                var_genFlavour = ROOT.std.string("")
                for i in range(var_Electrons.size()):
                    var_Electrons_isZ.push_back(False)
                for i in range(var_Muons.size()):
                    var_Muons_isZ.push_back(False)
            else:
                if abs(c.GenParticles_PdgId[genZL[0]]) == 11:
                    var_genFlavour = ROOT.std.string("Electrons")
                    for i in range(var_Electrons.size()):
                        var_Electrons_isZ.push_back(analysis_ntuples.isLeptonMatchedGen(c.GenParticles, c.GenParticles_PdgId, genZL, genNonZL, i, var_Electrons, var_Electrons_charge, -11))
                    for i in range(c.Muons.size()):
                        var_Muons_isZ.push_back(False)
                else:
                    var_genFlavour = ROOT.std.string("Muons")
                    for i in range(c.Muons.size()):
                        var_Muons_isZ.push_back(analysis_ntuples.isLeptonMatchedGen(c.GenParticles, c.GenParticles_PdgId, genZL, genNonZL, i, var_Muons, var_Muons_charge, -13))
                    for i in range(c.Electrons.size()):
                        var_Electrons_isZ.push_back(False)
                        
            tEvent.SetBranchAddress('genFlavour', var_genFlavour)
            tEvent.SetBranchAddress('Electrons_isZ', var_Electrons_isZ)
            tEvent.SetBranchAddress('Muons_isZ', var_Muons_isZ)
        
        if not signal:
            tEvent.SetBranchAddress('TriggerNames', var_triggerNames)
            tEvent.SetBranchAddress('TriggerPass', var_triggerPass)
            tEvent.SetBranchAddress('TriggerPrescales', var_triggerPrescales)
            tEvent.SetBranchAddress('TriggerVersion', var_triggerVersion)

            
        metDHt = 9999999
        if HT != 0:
            metDHt = MET / HT

        var_MetDHt[0] = metDHt
        var_LeadingJetPartonFlavor[0] = jets_partonFlavor[ljet]
        var_LeadingJetQgLikelihood[0] = jets_qgLikelihood[ljet]
    
        tEvent.Fill()

    fnew.cd()
    tEvent.Write()
    print('just created', fnew.GetName())
    print("Total: " + str(nentries))
    print("Right Process: " + str(count))
    print("After MET: " + str(afterMET))
    print("After NJ: " + str(afterNj))
    print("After Preselection: " + str(afterPreselection))
    print("After Leptons: " + str(afterLeptons))
    print("nL:")
    print(nLMap)
    print("nLGen:")
    print(nLGenMap)
    print("nLGenZ:")
    print(nLGenMapZ)

    hHt.Write()
    hHtWeighted.Write()
    hHtAfterMadHt.Write()
    
    if data:
        lumiSecs.Write("lumiSecs") 
    
    fnew.Close()

main()

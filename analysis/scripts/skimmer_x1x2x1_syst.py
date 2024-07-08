#!/usr/bin/env python3.8

from ROOT import *
from glob import glob
from sys import exit
import argparse
import sys
import numpy as np
import os
import cppyy

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes"))
from lib import analysis_ntuples
from lib import analysis_tools
from lib import utils
from lib import analysis_observables

gSystem.Load('LumiSectMap_C')
from ROOT import LumiSectMap

gSystem.Load('LeptonCollectionMap_C')
from ROOT import LeptonCollectionMap
from ROOT import LeptonCollectionFilesMap
from ROOT import LeptonCollection

#for systematics:
with open(os.environ['CMSSW_BASE']+'/src/cms-tools/analysis/tools/lib_systematics.py') as f:
    exec(f.read())
readerBtag = prepareReaderBtagSF()

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Create skims for x1x2x1 process.')
parser.add_argument('-i', '--input_file', nargs=1, help='Input Filename', required=False)
parser.add_argument('-o', '--output_dir', nargs=1, help='Output directory', required=False)
parser.add_argument('-madHTgt', '--madHTgt', nargs=1, help='madHT lower bound', required=False)
parser.add_argument('-madHTlt', '--madHTlt', nargs=1, help='madHT uppper bound', required=False)

parser.add_argument('-s', '--signal', dest='signal', help='Signal', action='store_true')
parser.add_argument('-bg', '--background', dest='bg', help='Background', action='store_true')
parser.add_argument('-skim', '--skim', dest='skim', help='Skim', action='store_true')
parser.add_argument('-data', '--data', dest='data', help='Data', action='store_true')
parser.add_argument('-dy', '--dy', dest='dy', help='Drell-Yan', action='store_true')
parser.add_argument('-sam', '--sam', dest='sam', help='Sam Samples', action='store_true')
parser.add_argument('-nlp', '--no_lepton_selection', dest='no_lepton_selection', help='No Lepton Selection Skim', action='store_true')
parser.add_argument('-jpsi_muons', '--jpsi_muons', dest='jpsi_muons', help='JPSI Muons Skim', action='store_true')
parser.add_argument('-jpsi_electrons', '--jpsi_electrons', dest='jpsi_electrons', help='JPSI Electrons Skim', action='store_true')
parser.add_argument('-testing', '--testing', dest='testing', help='testing', action='store_true')
parser.add_argument('-phase1', '--phase1', dest='phase1', help='phase1', action='store_true')
parser.add_argument('-phase1_2018', '--phase1_2018', dest='phase1_2018', help='phase1_2018', action='store_true')
parser.add_argument('-jecup', '--jecup', dest='jecup', help='jec-up variation', action='store_true')
parser.add_argument('-jecdown', '--jecdown', dest='jecdown', help='jec-down variation', action='store_true')

args = parser.parse_args()

print(args)
    
def getDyMuons(c):
    #print "getDyMuons"
    muons = [i for i in range(len(c.Muons)) if c.Muons[i].Pt() >= 20 and bool(c.Muons_mediumID[i]) and bool(c.Muons_passIso[i]) and abs(c.Muons[i].Eta()) <= 2.4]
    
    if len(muons) != 2:
        return None, None
        
    if c.Muons[muons[0]].Pt() < 30:
        return None, None
    
    if c.Muons_charge[muons[0]] * c.Muons_charge[muons[1]] > 0:
        return None, None
    
    invMass = (c.Muons[muons[0]] + c.Muons[muons[1]]).M()
    if not abs(invMass-91.19)<10: return None, None
    
    return muons, invMass

def getWMuon(c):
    muons = [i for i in range(len(c.Muons)) if c.Muons[i].Pt() >= 20 and bool(c.Muons_mediumID[i]) and bool(c.Muons_passIso[i]) and abs(c.Muons[i].Eta()) <= 2.4]
    if len(muons) != 1:
        return None
    if c.Muons[muons[0]].Pt() < 30:
        return None
    return muons
    
    
######## END OF CMDLINE ARGUMENTS ########

commonBranches = {
        "passedMhtMet6pack" :  "bool",
        "passedSingleMuPack" :  "bool",
        "passed2016BFilter" : "bool",
        "passesUniversalSelection" : "bool",
        "FastSimWeightPR31285To36122" : "float",
        "TrgEffNom" : "float",
        "TrgEffUp" : "float",
        "TrgEffDown" : "float",
        "IsrNom" : "float",
        "IsrUp" : "float",
        "IsrDown" : "float",
        "BTagNom" : "float",
        "BTagUp" : "float",
        "BTagDown" : "float",                
        "PuNom" : "float",
        "PuUp" : "float",
        "PuDown" : "float",
        "ElSfNom" : "float",
        "ElSfUp" : "float",
        "ElSfDown" : "float",                
        "MuSfNom" : "float",
        "MuSfUp" : "float",
        "MuSfDown" : "float"                  
}

def main():
    
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
    no_lepton_selection = args.no_lepton_selection
    jpsi_muons = args.jpsi_muons
    jpsi_electrons = args.jpsi_electrons
    jpsi = False
    testing = args.testing
    phase1 = args.phase1 or args.phase1_2018
    jecup = args.jecup; jecdown = args.jecdown
    
    if args.phase1: year = '2017'
    elif args.phase1_2018: year = '2018'
    else: year = '2016'
    eleReco, eleIdiso, eleIdFastFull, muIdiso, muIdFastFull = getRecoIdisoFastfullLeptonSFhistos(year)
    
    if signal and phase1:
        sam = True
    
    if dy:
        print("Got Drell-Yan")
        #exit(0)
    if no_lepton_selection:
        print("NO LEPTON SELECTION!")

    if jpsi_muons or jpsi_electrons:
        jpsi = True
        print("Got JPSI")
        if jpsi_muons:
            print("MUONS")
        else:
            print("ELECTRONS")

    if not signal:
        analysis_observables.commonFlatObs.update(analysis_observables.filtersObs)

    input_file = None
    if args.input_file:
        input_file = args.input_file[0].strip()
    output_dir = None
    if args.output_dir:
        output_dir = args.output_dir[0].strip()

    if (bg and signal):
        signal = True
        bg = False

    replace_lepton_collection = True
    if signal:
        replace_lepton_collection = False
    
    import os
    from lib import utils
    
    if jpsi:
        utils.defaultJetIsoSetting = "NoIso"
    
    # if no_lepton_selection:
#         utils.defaultJetIsoSetting = "NoIso"
# 
#         utils.leptonIsolationList = [ "NoIso" ]
#         utils.leptonIsolationCrList = [  ]
#         utils.leptonIsolationIncList = utils.leptonIsolationList + utils.leptonIsolationCrList
#     
    
    
    #triggerFileName = os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/susy-trig-plots.root")
    triggerFileName = os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/susy-trig-plots_amag.root")#SB
    print("Opening trigger file: " + triggerFileName)
    
    triggerFile = TFile(triggerFileName, "read")
    
    if phase1:#SB
        #in this block replacing Yuval's function analysis_ntuples.getTrigEffGraph
        #lumi16 = 36.5#not needed here
        lumi17 = 41.5
        lumi18 = 59.0
        te17 = triggerFile.Get('tEffhMetMhtRealXMht;2')
        hpass17 = te17.GetPassedHistogram().Clone('hpass')
        htotal17 = te17.GetTotalHistogram().Clone('htotal')
        te18 = triggerFile.Get('tEffhMetMhtRealXMht;3')
        hpass18 = te17.GetPassedHistogram().Clone('hpass')
        htotal18 = te17.GetTotalHistogram().Clone('htotal')
        hpass17.Scale(lumi17); hpass18.Scale(lumi18); 
        htotal17.Scale(lumi17); htotal18.Scale(lumi18);
        hpass = hpass17.Clone()
        hpass.Add(hpass18)
        htotal = hpass17.Clone()
        htotal.Add(htotal18)        
        tetrig = TEfficiency(hpass, htotal)
    else:
        te16 = triggerFile.Get('tEffhMetMhtRealXMht;1')
        tetrig = te16
        #tetrig = analysis_ntuples.getTrigEffGraph(triggerFile, 'tEffhMetMhtRealXMht;1')        
    
    triggerFile.Close()
    
    flatObs = {}
    for flatOb in analysis_observables.commonFlatObs:
        flatObs[flatOb] = np.zeros(1,dtype=eval(analysis_observables.commonFlatObs[flatOb]))
        
    commonRecalcFlatObs = {}
    for commonRecalcFlatOb in analysis_observables.commonRecalcFlatObs:
        commonRecalcFlatObs[commonRecalcFlatOb] = np.zeros(1,dtype=eval(analysis_observables.commonRecalcFlatObs[commonRecalcFlatOb]))
    
    commonOrigRecalcFlatObs = {}
    for commonRecalcFlatOb in analysis_observables.commonRecalcFlatObs:
        commonOrigRecalcFlatObs[commonRecalcFlatOb] = np.zeros(1,dtype=eval(analysis_observables.commonRecalcFlatObs[commonRecalcFlatOb]))
    
    
    commonCalcFlatObs = {}
    for commonCalcFlatOb in analysis_observables.commonCalcFlatObs:
        commonCalcFlatObs[commonCalcFlatOb] = np.zeros(1,dtype=eval(analysis_observables.commonCalcFlatObs[commonCalcFlatOb]))
    
    vetosFlatObs = {}
    for vetosFlatOb in analysis_observables.vetosFlatObs:
        vetosFlatObs[vetosFlatOb] = np.zeros(1,dtype=eval(analysis_observables.vetosFlatObs[vetosFlatOb]))

     ### JETS ###
    
    jetsObs = {}
    for jetsOb in analysis_observables.jetsObs:
        jetsObs[jetsOb] = cppyy.gbl.std.vector(eval(analysis_observables.jetsObs[jetsOb]))()

    
    jetsCalcObs = {}
    for jetsCalcOb in analysis_observables.jetsCalcObs:
        jetsCalcObs[jetsCalcOb] = cppyy.gbl.std.vector(eval(analysis_observables.jetsCalcObs[jetsCalcOb]))()

    #### TRACKS ####
    tracksObs = {}
    
    for tracksOb in analysis_observables.tracksObs:
        tracksObs[tracksOb] = cppyy.gbl.std.vector(eval(analysis_observables.tracksObs[tracksOb]))()
        
    tracksCalcObs = {}
    for tracksCalcOb in analysis_observables.tracksCalcObs:
        tracksCalcObs[tracksCalcOb] = cppyy.gbl.std.vector(eval(analysis_observables.tracksCalcObs[tracksCalcOb]))()
    
    pionsObs = {}
    for pionsOb in analysis_observables.pionsObs:
        pionsObs[pionsOb] = cppyy.gbl.std.vector(eval(analysis_observables.pionsObs[pionsOb]))()
        
    photonObs = {}
    for photonOb in analysis_observables.photonObs:
        photonObs[photonOb] = cppyy.gbl.std.vector(eval(analysis_observables.photonObs[photonOb]))()
    
    ### LEPTONS ###
    
    electronsObs = {}
    for electronsOb in analysis_observables.electronsObs:
        electronsObs[electronsOb] = cppyy.gbl.std.vector(eval(analysis_observables.electronsObs[electronsOb]))()

    electronsCalcObs = {}
    for electronsCalcOb in analysis_observables.electronsCalcObs:
        electronsCalcObs[electronsCalcOb] = cppyy.gbl.std.vector(eval(analysis_observables.electronsCalcObs[electronsCalcOb]))()

    muonsObs = {}
    for muonsOb in analysis_observables.muonsObs:
        muonsObs[muonsOb] = cppyy.gbl.std.vector(eval(analysis_observables.muonsObs[muonsOb]))()

    muonsCalcObs = {}
    for muonsCalcOb in analysis_observables.muonsCalcObs:
        muonsCalcObs[muonsCalcOb] = cppyy.gbl.std.vector(eval(analysis_observables.muonsCalcObs[muonsCalcOb]))()
        
    
    ### DY LEPTONS ###

    dyMuonsObs = {}
    for muonsOb in analysis_observables.muonsObs:
        dyMuonsObs[muonsOb] = cppyy.gbl.std.vector(eval(analysis_observables.muonsObs[muonsOb]))()

    dyMuonsFlatObs = {}
    for dyMuonsFlatOb in analysis_observables.dyMuonsFlatObs:
        dyMuonsFlatObs[dyMuonsFlatOb] = np.zeros(1,dtype=analysis_observables.dyMuonsFlatObs[dyMuonsFlatOb])
    
    dyMuonsClassObs = {}
    for dyMuonsClassOb in analysis_observables.dyMuonsClassObs:
        dyMuonsClassObs[dyMuonsClassOb] = eval(analysis_observables.dyMuonsClassObs[dyMuonsClassOb])()

    
    ### GEN PARTICLES ###

    genParticlesObs = {}
    for genParticlesOb in analysis_observables.genParticlesObs:
        genParticlesObs[genParticlesOb] = cppyy.gbl.std.vector(eval(analysis_observables.genParticlesObs[genParticlesOb]))()
    
    commonObservablesStringObs = {}
    for commonObservablesStringOb in analysis_observables.commonObservablesStringList:
        commonObservablesStringObs[commonObservablesStringOb] = cppyy.gbl.std.string()
    
    genVecObs = {}
    for genVecOb in analysis_observables.genObservablesVecList:
        genVecObs[genVecOb] = cppyy.gbl.std.vector(eval(analysis_observables.genObservablesVecList[genVecOb]))()
    
    genCalcObs = {}
    for DTypeOb in analysis_observables.commonObservablesDTypesList:
        genCalcObs[DTypeOb] = np.zeros(1,dtype=analysis_observables.commonObservablesDTypesList[DTypeOb])
    
    leptonsCorrJetVars = {}
    
    for lep in ["Muons", "Electrons", "tracks"]:
        for CorrJetObs in utils.leptonIsolationIncList:
            ptRanges = [""]
            drCuts = [""]
            if CorrJetObs in ["CorrJetIso", "CorrJetD3Iso", "CorrJetNoMultIso", "CorrJetNoMultD3Iso"]:
                ptRanges = utils.leptonCorrJetIsoPtRange
                drCuts = utils.leptonCorrJetIsoDrCuts
            for ptRange in ptRanges:
                for drCut in drCuts:
                    cuts = ""
                    if len(str(ptRange)) > 0:
                        cuts = str(ptRange) + "Dr" + str(drCut)
                    leptonsCorrJetVars[lep + "_pass" + CorrJetObs + cuts] = cppyy.gbl.std.vector(eval(utils.leptonsCorrJetVecList[CorrJetObs]))()
                    # This is not saved to the root files
                    leptonsCorrJetVars[lep + "_minDr" + CorrJetObs + cuts] = cppyy.gbl.std.vector(double)()
    
    # DILEPTON OBSERVABLES
    
    dileptonVars = {}
    
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
                    postfixi = [iso + cuts + cat]
                    if iso + cuts + cat == utils.defaultJetIsoSetting:
                        postfixi = [iso + cuts + cat, ""]
                    for postfix in postfixi:
                        for vecObs in analysis_observables.dileptonObservablesVecList:
                            dileptonVars[vecObs + postfix] = cppyy.gbl.std.vector(eval(analysis_observables.dileptonObservablesVecList[vecObs]))()
                        for stringObs in analysis_observables.dileptonObservablesStringList:
                            dileptonVars[stringObs + postfix] = cppyy.gbl.std.string("")
                        for DTypeObs in analysis_observables.dileptonObservablesDTypesList:
                            dileptonVars[DTypeObs + postfix] = np.zeros(1,dtype=analysis_observables.dileptonObservablesDTypesList[DTypeObs])

    #print dileptonVars
       
    var_LeadingJet = TLorentzVector()
    
    ### TRIGGER ###
    
    triggerObs = {}
    for triggerOb in analysis_observables.triggerObs:
        triggerObs[triggerOb] = cppyy.gbl.std.vector(eval(analysis_observables.triggerObs[triggerOb]))()

    tEvent = TTree('tEvent','tEvent')
    
    for flatOb in analysis_observables.commonFlatObs:
        print("tEvent.Branch(" + flatOb + "," +  "flatObs[flatOb]" + "," + flatOb + "/" + utils.typeTranslation[analysis_observables.commonFlatObs[flatOb]] + ")")
        tEvent.Branch(flatOb, flatObs[flatOb],flatOb + "/" + utils.typeTranslation[analysis_observables.commonFlatObs[flatOb]])
    
    for flatOb in analysis_observables.commonRecalcFlatObs:
        print("tEvent.Branch(" + flatOb + "," +  "commonRecalcFlatObs[flatOb]" + "," + flatOb + "/" + utils.typeTranslation[analysis_observables.commonRecalcFlatObs[flatOb]] + ")")
        tEvent.Branch(flatOb, commonRecalcFlatObs[flatOb],flatOb + "/" + utils.typeTranslation[analysis_observables.commonRecalcFlatObs[flatOb]])
    
    for flatOb in analysis_observables.commonRecalcFlatObs:
        print("tEvent.Branch(Orig" + flatOb + "," +  "commonRecalcFlatObs[flatOb]" + "," + "Orig" + flatOb + "/" + utils.typeTranslation[analysis_observables.commonRecalcFlatObs[flatOb]] + ")")
        tEvent.Branch("Orig" +flatOb, commonOrigRecalcFlatObs[flatOb],"Orig" + flatOb + "/" + utils.typeTranslation[analysis_observables.commonRecalcFlatObs[flatOb]])
    
    
    for commonCalcFlatOb in analysis_observables.commonCalcFlatObs:
        print("tEvent.Branch(" + commonCalcFlatOb  + "," + "commonCalcFlatObs[commonCalcFlatOb]" + "," + commonCalcFlatOb + "/" + utils.typeTranslation[analysis_observables.commonCalcFlatObs[commonCalcFlatOb]] + ")")
        tEvent.Branch(commonCalcFlatOb, commonCalcFlatObs[commonCalcFlatOb],commonCalcFlatOb + "/" + utils.typeTranslation[analysis_observables.commonCalcFlatObs[commonCalcFlatOb]])
    
    for vetosFlatOb in analysis_observables.vetosFlatObs:
        tEvent.Branch(vetosFlatOb, vetosFlatObs[vetosFlatOb],vetosFlatOb + "/" + utils.typeTranslation[analysis_observables.vetosFlatObs[vetosFlatOb]])
    
    for jetsOb in analysis_observables.jetsObs:
        tEvent.Branch(jetsOb, 'std::vector<' + analysis_observables.jetsObs[jetsOb] + '>', jetsObs[jetsOb])
    
    for jetsCalcOb in analysis_observables.jetsCalcObs:
        tEvent.Branch(jetsCalcOb, 'std::vector<' + analysis_observables.jetsCalcObs[jetsCalcOb] + '>', jetsCalcObs[jetsCalcOb])
    
    if not data:
        for genParticlesOb in analysis_observables.genParticlesObs:
            tEvent.Branch(genParticlesOb, 'std::vector<' + analysis_observables.genParticlesObs[genParticlesOb] + '>', genParticlesObs[genParticlesOb])
        ## Signal Gen Stuff
        if signal:
            for genVecOb in analysis_observables.genObservablesVecList:
                tEvent.Branch(genVecOb, 'std::vector<' + analysis_observables.genObservablesVecList[genVecOb] + '>', genVecObs[genVecOb])
            
            for DTypeOb in analysis_observables.commonObservablesDTypesList:
                tEvent.Branch("gen_" + DTypeOb, genCalcObs[DTypeOb],"gen_" + DTypeOb + "/" + utils.typeTranslation[analysis_observables.commonObservablesDTypesList[DTypeOb]])
    
    for commonObservablesStringOb in analysis_observables.commonObservablesStringList:
        tEvent.Branch(commonObservablesStringOb, 'std::string', commonObservablesStringObs[commonObservablesStringOb])
    
    for lep in ["Muons", "Electrons", "tracks"]:
        for CorrJetObs in utils.leptonIsolationIncList:
            ptRanges = [""]
            drCuts = [""]
            if CorrJetObs in ["CorrJetIso", "CorrJetD3Iso", "CorrJetNoMultIso", "CorrJetNoMultD3Iso"]:
                ptRanges = utils.leptonCorrJetIsoPtRange
                drCuts = utils.leptonCorrJetIsoDrCuts
            for ptRange in ptRanges:
                for drCut in drCuts:
                    cuts = str(ptRange)
                    if len(str(ptRange)) > 0:
                        cuts = str(ptRange) + "Dr" + str(drCut)
                    print("tEvent.Branch(" + lep + "_pass" + CorrJetObs + cuts, 'std::vector<' + str(utils.leptonsCorrJetVecList[CorrJetObs]) + '>', leptonsCorrJetVars[lep + "_pass" + CorrJetObs + cuts], ")")
                    tEvent.Branch(lep + "_pass" +  CorrJetObs + cuts, 'std::vector<' + utils.leptonsCorrJetVecList[CorrJetObs] + '>', leptonsCorrJetVars[lep + "_pass" + CorrJetObs + cuts])
            
    ###### Tracks #######
    
    for tracksOb in analysis_observables.tracksObs:
        tEvent.Branch(tracksOb, 'std::vector<' + analysis_observables.tracksObs[tracksOb] + '>', tracksObs[tracksOb])
    
    for tracksCalcOb in analysis_observables.tracksCalcObs:
        tEvent.Branch(tracksCalcOb, 'std::vector<' + analysis_observables.tracksCalcObs[tracksCalcOb] + '>', tracksCalcObs[tracksCalcOb])
    
    for pionsOb in analysis_observables.pionsObs:
        tEvent.Branch(pionsOb, 'std::vector<' + analysis_observables.pionsObs[pionsOb] + '>', pionsObs[pionsOb])
        
    for photonOb in analysis_observables.photonObs:
        tEvent.Branch(photonOb, 'std::vector<' + analysis_observables.photonObs[photonOb] + '>', photonObs[photonOb])
    
    for electronsOb in analysis_observables.electronsObs:
        tEvent.Branch(electronsOb, 'std::vector<' + analysis_observables.electronsObs[electronsOb] + '>', electronsObs[electronsOb])
    
    for electronsCalcOb in analysis_observables.electronsCalcObs:
        tEvent.Branch(electronsCalcOb, 'std::vector<' + analysis_observables.electronsCalcObs[electronsCalcOb] + '>', electronsCalcObs[electronsCalcOb])
    
    for muonsOb in analysis_observables.muonsObs:
        tEvent.Branch(muonsOb, 'std::vector<' + analysis_observables.muonsObs[muonsOb] + '>', muonsObs[muonsOb])
    
    for muonsCalcOb in analysis_observables.muonsCalcObs:
        tEvent.Branch(muonsCalcOb, 'std::vector<' + analysis_observables.muonsCalcObs[muonsCalcOb] + '>', muonsCalcObs[muonsCalcOb])
        
        
    if dy:
        for muonsOb in analysis_observables.muonsObs:
            tEvent.Branch("DY" + muonsOb, 'std::vector<' + analysis_observables.muonsObs[muonsOb] + '>', dyMuonsObs[muonsOb])
        
        for dyMuonsFlatOb in analysis_observables.dyMuonsFlatObs:
            tEvent.Branch(dyMuonsFlatOb, dyMuonsFlatObs[dyMuonsFlatOb],dyMuonsFlatOb + "/" + utils.typeTranslation[analysis_observables.dyMuonsFlatObs[dyMuonsFlatOb]])
    
        for dyMuonsClassOb in analysis_observables.dyMuonsClassObs:
            tEvent.Branch(dyMuonsClassOb, analysis_observables.dyMuonsClassObs[dyMuonsClassOb], dyMuonsClassObs[dyMuonsClassOb])


    tEvent.Branch('LeadingJet', 'TLorentzVector', var_LeadingJet)
    
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
                    postfixi = [iso + cuts + cat]
                    if iso + cuts + cat == utils.defaultJetIsoSetting:
                        postfixi = [iso + cuts + cat, ""]
                    for postfix in postfixi:
                        for vecObs in analysis_observables.dileptonObservablesVecList:
                            print("tEvent.Branch(" + vecObs + postfix, 'std::vector<' + analysis_observables.dileptonObservablesVecList[vecObs] + '>', dileptonVars[vecObs + postfix], ")")
                            tEvent.Branch(vecObs + postfix, 'std::vector<' + analysis_observables.dileptonObservablesVecList[vecObs] + '>', dileptonVars[vecObs + postfix])
                        for stringObs in analysis_observables.dileptonObservablesStringList:
                            print("tEvent.Branch(" + stringObs + postfix, 'std::string', dileptonVars[stringObs + postfix],")")
                            tEvent.Branch(stringObs + postfix, 'std::string', dileptonVars[stringObs + postfix])
                        for DTypeObs in analysis_observables.dileptonObservablesDTypesList:
                            print("tEvent.Branch(" + DTypeObs + postfix, dileptonVars[DTypeObs + postfix],DTypeObs + postfix + "/" + utils.typeTranslation[analysis_observables.dileptonObservablesDTypesList[DTypeObs]], ")")
                            tEvent.Branch(DTypeObs + postfix, dileptonVars[DTypeObs + postfix],DTypeObs + postfix + "/" + utils.typeTranslation[analysis_observables.dileptonObservablesDTypesList[DTypeObs]])
                        
    if not signal:
        for triggerOb in analysis_observables.triggerObs:
            tEvent.Branch(triggerOb, 'std::vector<' + analysis_observables.triggerObs[triggerOb] + '>', triggerObs[triggerOb])
    
    vars = {}
    
    for commonBranch in commonBranches:
        vars[commonBranch] = np.zeros(1,dtype=commonBranches[commonBranch])
        tEvent.Branch(commonBranch, vars[commonBranch], commonBranch + "/" + utils.typeTranslation[commonBranches[commonBranch]])
    
    
    c = TChain('TreeMaker2/PreSelection')
    print("Opening", input_file)
    lil_input = input_file.split('/')[-1]
    c.Add(input_file)
    #c = c.CloneTree()
    #chain = None
    fname = output_dir+lil_input
    if jecup: fname = fname.replace('.root','_JecUp.root')
    if jecdown: fname = fname.replace('.root','_JecDown.root') 
    print("Creating " + fname)
    fnew = TFile(fname,'recreate')
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
        print('sam', sam)
        if sam:
            if phase1:
                print('working with input_file', input_file)
                chiM = os.path.basename(input_file).split("_")[3]
            else:
                chiM = os.path.basename(input_file).split("_")[2]
            crossSection = utils.samCrossSections.get(chiM)
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
        crossSection = utils.dyCrossSections.get(fileBasename)
        print("Got cs", crossSection)
    elif bg and "Summer16ForYuval.WZTo3LNu_mllmin01" in input_file:
        crossSection = 62.78
        replace_lepton_collection = False
        print("It's Summer16ForYuval.WZTo3LNu_mllmin01!!!")
    
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
            if "DYJetsToLL_M-5to50_" not in input_file and "Summer16ForYuval.WZTo3LNu_mllmin01" not in input_file:
                crossSection = c.CrossSection
            rightProcess = utils.madHtCheck(baseFileName, c.madHT)
        elif data:
            lumiSecs.insert(c.RunNum, c.LumiBlockNum)

        hHt.Fill(c.HT)
        #print "crossSection=" + str(crossSection)
        hHtWeighted.Fill(c.HT, crossSection)

        if not rightProcess:
            continue
            
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
        if signal:
            if sam:
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
                    #print "nX20", nX20, "nLGenZ", nLGenZ
                    if nX20 == 1 and nLGenZ == 2:
                        branching_ratio *= 0.2
                    elif nX20 == 2 and nLGenZ == 4:
                        branching_ratio *= 0.04
                    elif nX20 == 1 and nLGenZ == 0:
                        branching_ratio *= 1.8
                        #print "******", branching_ratio
                    elif nX20 == 2 and nLGenZ == 0:
                        branching_ratio *= 3.24
            else:
                branching_ratio = 0.1
                    
        #### END OF GEN LEVEL STUFF ####
        
        #var_BranchingRatio[0] = branching_ratio
        commonCalcFlatObs["BranchingRatio"][0] = branching_ratio
        commonCalcFlatObs["NLGen"][0] = nLGen
        commonCalcFlatObs["NLGenZ"][0] = nLGenZ
    
        #### PRECUTS ###
        if not signal:
            vars["passed2016BFilter"][0] = analysis_ntuples.passed2016BFilter(c, data)
        else:
            vars["passed2016BFilter"][0] = True
        
        for tracksOb in analysis_observables.tracksObs:
            tracksObs[tracksOb] = getattr(c, tracksOb)
        
        for pionsOb in analysis_observables.pionsObs:
            pionsObs[pionsOb] = getattr(c, pionsOb)
        
        for photonOb in analysis_observables.photonObs:
            photonObs[photonOb] = getattr(c, photonOb)
        
        for jetsOb in analysis_observables.jetsObs:
            jetsObs[jetsOb] = getattr(c, jetsOb)
        
        HT=0
        MHTvec = TLorentzVector()
        if len(jetsObs["Jets"])>3:
            if not jetsObs["Jets"][3].Pt()==c.Jets[3].Pt():
                print(ientry, 'different jets', jetsObs["Jets"][3].Pt(), c.Jets[3].Pt())
        for ijet, jet in enumerate(jetsObs["Jets"]):
            if jecup:  jet*=1.0/(1-c.Jets_jecUnc[ijet])
            if jecdown: jet*=1.0/(1+c.Jets_jecUnc[ijet])
            if not jet.Pt()>30: continue
            if not abs(jet.Eta())<5.0: continue
            MHTvec-=jet
            if not abs(jet.Eta())<2.4: continue
            HT+=jet.Pt()
        
        MET = c.MET
        METPhi = c.METPhi
        MHT = MHTvec.Pt()
        MHTPhi = MHTvec.Phi()        
        #HT = c.HT

        for flatOb in commonRecalcFlatObs:
            commonRecalcFlatObs[flatOb][0] = getattr(c, flatOb)
            commonOrigRecalcFlatObs[flatOb][0] = getattr(c, flatOb)
        commonRecalcFlatObs['MHT'][0] = MHT
        commonRecalcFlatObs['MHTPhi'][0] = MHTPhi
        commonRecalcFlatObs['HT'][0] = HT        
        
        muons = []
        if dy:
           
            muons, invMass = getDyMuons(c)
            if muons is None:
                muons = getWMuon(c)
                if muons is None:
                    continue
                invMass = -1
            
            metVector = TLorentzVector()
            metVector.SetPtEtaPhiE(c.MET,0,c.METPhi,c.MET)
            
            for i in range(len(muons)):
               metVector += c.Muons[muons[i]]
            #print(abs(metVector.Pt()), metVector.Phi())
            MET = abs(metVector.Pt())    
            METPhi = metVector.Phi()
            
            thejets = c.Jets
            for ijet, jet in enumerate(thejets):
                if jecup: jet*=1.0/(1-c.Jets_jecUnc[ijet])
                if jecdown: jet*=1.0/(1+c.Jets_jecUnc[ijet])
            jetsHt = [i for i in range(len(thejets)) if thejets[i].Pt() >= 30 and abs(thejets[i].Eta()) <= 2.4 and all(abs(c.Muons[j].DeltaR(thejets[i])) > 0.1 for j in muons)]
            jetsMht = [i for i in range(len(thejets)) if thejets[i].Pt() >= 30 and abs(thejets[i].Eta()) <= 5 and all(abs(c.Muons[j].DeltaR(thejets[i])) > 0.1 for j in muons)]
    
            #print "jetsHt=", jetsHt, "len(thejets)", len(thejets)
            #print "jetsMht=", jetsMht
            
            HT = 0
            for i in jetsHt:
                HT += thejets[i].Pt()
            MhtVec = TLorentzVector()
            MhtVec.SetPtEtaPhiE(0,0,0,0)
            for i in jetsMht:
                MhtVec -= thejets[i]
            MHT = MhtVec.Pt()
            MHTPhi = MhtVec.Phi()
           
            for flatOb in commonRecalcFlatObs:
                commonRecalcFlatObs[flatOb][0] = eval(flatOb)
        
            # CLEAN JETS FROM THE DY MUONS
            for jetsOb in analysis_observables.jetsObs:
                jetsObs[jetsOb] = cppyy.gbl.std.vector(eval(analysis_observables.jetsObs[jetsOb]))()

            for i in range(thejets.size()):
                if all(abs(c.Muons[j].DeltaR(thejets[i])) > 0.1 for j in muons):
                    for jetsOb in analysis_observables.jetsObs:
                        jetsObs[jetsOb].push_back(getattr(c, jetsOb)[i])
        
            # CLEAN TRACKS FROM THE DY MUONS
        
            for tracksOb in analysis_observables.tracksObs:
                tracksObs[tracksOb] = cppyy.gbl.std.vector(eval(analysis_observables.tracksObs[tracksOb]))()
        
            for i in range(c.tracks.size()):
                if all(abs(c.Muons[j].DeltaR(c.tracks[i])) > 0.01 for j in muons):
                    for tracksOb in analysis_observables.tracksObs:
                        if analysis_observables.tracksObs[tracksOb] == "bool":
                            tracksObs[tracksOb].push_back(bool(getattr(c, tracksOb)[i]))
                        else:
                            tracksObs[tracksOb].push_back(getattr(c, tracksOb)[i])
        
        nj, btagsLoose, ljet = analysis_ntuples.eventNumberOfJets30Pt2_4Eta_Loose(jetsObs["Jets"], jetsObs["Jets_bDiscriminatorCSV"])
        nj, btagsMedium, ljet = analysis_ntuples.eventNumberOfJets30Pt2_4Eta_Medium(jetsObs["Jets"], jetsObs["Jets_bDiscriminatorCSV"])
        nj, btagsDeepLoose, ljet = analysis_ntuples.eventNumberOfJets30Pt2_4Eta_DeepLoose(jetsObs["Jets"], jetsObs["Jets_bJetTagDeepCSVBvsAll"])
        nj, btagsDeepMedium, ljet = analysis_ntuples.eventNumberOfJets30Pt2_4Eta_DeepMedium(jetsObs["Jets"], jetsObs["Jets_bJetTagDeepCSVBvsAll"])
        
        if ljet is None and not jpsi:
            #print "No ljet:",ljet 
            continue
            
        #if no_lepton_selection and btagsDeepMedium > 0:
        #    continue
        
        afterNj += 1
        
        #if not duoLepton: continue
        commonCalcFlatObs["MinDeltaPhiMetJets"][0] = analysis_ntuples.eventMinDeltaPhiMetJets30Pt2_4Eta(jetsObs["Jets"], MET, METPhi)
        commonCalcFlatObs["MinDeltaPhiMhtJets"][0] = analysis_ntuples.eventMinDeltaPhiMhtJets30Pt2_4Eta(jetsObs["Jets"], MHT, MHTPhi)
        if not dy and not jpsi and not no_lepton_selection:
            #if commonCalcFlatObs["MinDeltaPhiMetJets"][0] < 0.4: continue
            #if MHT < 140: continue
            #if MET < 140: continue
            
            if MHT < 100: continue
            #if MET < 140: continue
            
        #Keep 2 b-tags for two-leptons
        # if two_leptons:
#             if btags > 2: continue
#         else:
#             if btags > 0: continue
                
        ## END PRECUTS##
        
        afterMET += 1
        #if btags > 0: continue
        
        #if nj < 1: continue
        
        #nj, btags, ljet = analysis_ntuples.numberOfJets30Pt2_4Eta_Loose(c)
        
        for flatOb in flatObs:
            flatObs[flatOb][0] = getattr(c, flatOb)
    
        commonCalcFlatObs["CrossSection"][0] = crossSection
        commonCalcFlatObs["NJets"][0] = nj
        commonCalcFlatObs["BTagsLoose"][0] = btagsLoose
        commonCalcFlatObs["BTagsMedium"][0] = btagsMedium
        commonCalcFlatObs["BTagsDeepLoose"][0] = btagsDeepLoose
        commonCalcFlatObs["BTagsDeepMedium"][0] = btagsDeepMedium
        
        if ljet is None:
            commonCalcFlatObs["LeadingJetPt"][0] = -1
            var_LeadingJet = TLorentzVector()
        else:
            commonCalcFlatObs["LeadingJetPt"][0] = jetsObs["Jets"][ljet].Pt()
            var_LeadingJet = jetsObs["Jets"][ljet]

        commonCalcFlatObs["MinCsv30"][0], commonCalcFlatObs["MaxCsv30"][0] = analysis_ntuples.minMaxCsv(jetsObs["Jets"], jetsObs["Jets_bDiscriminatorCSV"], 30)
        commonCalcFlatObs["MinCsv25"][0], commonCalcFlatObs["MaxCsv25"][0] = analysis_ntuples.minMaxCsv(jetsObs["Jets"], jetsObs["Jets_bDiscriminatorCSV"], 25)
        
        commonCalcFlatObs["MinDeepCsv30"][0], commonCalcFlatObs["MaxDeepCsv30"][0] = analysis_ntuples.minMaxCsv(jetsObs["Jets"], jetsObs["Jets_bJetTagDeepCSVBvsAll"], 30)
        commonCalcFlatObs["MinDeepCsv25"][0], commonCalcFlatObs["MaxDeepCsv25"][0] = analysis_ntuples.minMaxCsv(jetsObs["Jets"], jetsObs["Jets_bJetTagDeepCSVBvsAll"], 25)
        
        #if var_MaxCsv25[0] > 0.7:
        #    continue
        
        afterPreselection += 1
        
        if not data:
            commonCalcFlatObs["puWeight"][0] = c.puWeight
            commonCalcFlatObs["madHT"][0] = c.madHT
        else:
            commonCalcFlatObs["puWeight"][0] = 1
            commonCalcFlatObs["madHT"][0] = 1
        
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
        
        if dy:
            #print "In DY section"
            #print "muons=", muons
            muons, invMass = getDyMuons(takeLeptonsFrom)
            if muons is None:
                muons = getWMuon(takeLeptonsFrom)
                if muons is None:
                    continue
                invMass = -1
            if muons is None:
                print("WHAT IS GOING ON?")
            
            for muonsOb in analysis_observables.muonsObs:
                dyMuonsObs[muonsOb] = cppyy.gbl.std.vector(eval(analysis_observables.muonsObs[muonsOb]))()

            for dyMuonsFlatOb in analysis_observables.dyMuonsFlatObs:
                dyMuonsFlatObs[dyMuonsFlatOb] = np.zeros(1,dtype=analysis_observables.dyMuonsFlatObs[dyMuonsFlatOb])
    
            for dyMuonsClassOb in analysis_observables.dyMuonsClassObs:
                dyMuonsClassObs[dyMuonsClassOb] = eval(analysis_observables.dyMuonsClassObs[dyMuonsClassOb])()
            
            for muonsOb in analysis_observables.muonsObs:
                if analysis_observables.muonsObs[muonsOb] == "bool":
                    for j in range(len(muons)):
                        dyMuonsObs[muonsOb].push_back(bool(getattr(takeLeptonsFrom, muonsOb)[muons[j]]))
                else:
                    for j in range(len(muons)):
                        dyMuonsObs[muonsOb].push_back(getattr(takeLeptonsFrom, muonsOb)[muons[j]])
            
            if len(muons) == 2:
                dyMuonsClassObs["DYMuonsSum"] = takeLeptonsFrom.Muons[muons[0]] + takeLeptonsFrom.Muons[muons[1]]
            else:
                dyMuonsClassObs["DYMuonsSum"] = takeLeptonsFrom.Muons[muons[0]]
            #print "invMass=", invMass
            dyMuonsFlatObs["DYMuonsInvMass"][0] = invMass
            
            for muonsOb in analysis_observables.muonsObs:
                muonsObs[muonsOb] = cppyy.gbl.std.vector(eval(analysis_observables.muonsObs[muonsOb]))()
            
            for i in range(takeLeptonsFrom.Muons.size()):
                if all(i != j for j in muons):
                    for muonsOb in analysis_observables.muonsObs:
                        if analysis_observables.muonsObs[muonsOb] == "bool":
                            muonsObs[muonsOb].push_back(bool(getattr(takeLeptonsFrom, muonsOb)[i]))
                        else:
                            muonsObs[muonsOb].push_back(getattr(takeLeptonsFrom, muonsOb)[i])
        else:
            for muonsOb in analysis_observables.muonsObs:
                muonsObs[muonsOb] = getattr(takeLeptonsFrom, muonsOb)
        
        for electronsOb in analysis_observables.electronsObs:
                electronsObs[electronsOb] = getattr(takeLeptonsFrom, electronsOb)
        
        commonCalcFlatObs["NL"][0] = nL
        
        if data:
            var_GenParticles = cppyy.gbl.std.vector(TLorentzVector)()
            var_GenParticles_ParentId = cppyy.gbl.std.vector(int)()
            var_GenParticles_ParentIdx = cppyy.gbl.std.vector(int)()
            var_GenParticles_PdgId = cppyy.gbl.std.vector(int)()
            var_GenParticles_Status = cppyy.gbl.std.vector(int)()
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
        
        for electronsCalcOb in analysis_observables.electronsCalcObs:
            electronsCalcObs[electronsCalcOb] = cppyy.gbl.std.vector(eval(analysis_observables.electronsCalcObs[electronsCalcOb]))()
        
        for muonsCalcOb in analysis_observables.muonsCalcObs:
            muonsCalcObs[muonsCalcOb] = cppyy.gbl.std.vector(eval(analysis_observables.muonsCalcObs[muonsCalcOb]))()
        
        for tracksCalcOb in analysis_observables.tracksCalcObs:
            tracksCalcObs[tracksCalcOb] = cppyy.gbl.std.vector(eval(analysis_observables.tracksCalcObs[tracksCalcOb]))()
        
        for i in range(electronsObs["Electrons"].size()):
            electronsCalcObs["Electrons_deltaRLJ"].push_back(electronsObs["Electrons"][i].DeltaR(var_LeadingJet))
            electronsCalcObs["Electrons_deltaPhiLJ"].push_back(abs(electronsObs["Electrons"][i].DeltaPhi(var_LeadingJet)))
            electronsCalcObs["Electrons_deltaEtaLJ"].push_back(abs(electronsObs["Electrons"][i].Eta() - var_LeadingJet.Eta()))
            mini, minCan = analysis_ntuples.minDeltaLepLeps(electronsObs["Electrons"][i], tracksObs["tracks"])
            if mini is None or mini > 0.01 or tracksObs["tracks_charge"][minCan] * electronsObs["Electrons_charge"][i] < 0:
                electronsCalcObs["Electrons_ti"].push_back(-1)
            else:
                electronsCalcObs["Electrons_ti"].push_back(minCan)
            
        for i in range(muonsObs["Muons"].size()):
            muonsCalcObs["Muons_deltaRLJ"].push_back(muonsObs["Muons"][i].DeltaR(var_LeadingJet))
            muonsCalcObs["Muons_deltaPhiLJ"].push_back(abs(muonsObs["Muons"][i].DeltaPhi(var_LeadingJet)))
            muonsCalcObs["Muons_deltaEtaLJ"].push_back(abs(muonsObs["Muons"][i].Eta() - var_LeadingJet.Eta()))
            mini, minCan = analysis_ntuples.minDeltaLepLeps(muonsObs["Muons"][i], tracksObs["tracks"])
            if mini is None or mini > 0.01 or tracksObs["tracks_charge"][minCan] * muonsObs["Muons_charge"][i] < 0:
                muonsCalcObs["Muons_ti"].push_back(-1)
            else:
                muonsCalcObs["Muons_ti"].push_back(minCan)
        
        for i in range(tracksObs["tracks"].size()):
            tracksCalcObs["tracks_deltaRLJ"].push_back(tracksObs["tracks"][i].DeltaR(var_LeadingJet))
            tracksCalcObs["tracks_deltaPhiLJ"].push_back(abs(tracksObs["tracks"][i].DeltaPhi(var_LeadingJet)))
            tracksCalcObs["tracks_deltaEtaLJ"].push_back(abs(tracksObs["tracks"][i].Eta() - var_LeadingJet.Eta()))
        
        if not data:
            genElectrons = [ var_GenParticles[i] for i in range(var_GenParticles.size()) if abs(var_GenParticles_PdgId[i]) == 11 ]
            genElectronsIdx = [ i for i in range(var_GenParticles.size()) if abs(var_GenParticles_PdgId[i]) == 11 ]
            genMuons = [ var_GenParticles[i] for i in range(var_GenParticles.size()) if abs(var_GenParticles_PdgId[i]) == 13]
            genMuonsIdx = [ i for i in range(var_GenParticles.size()) if abs(var_GenParticles_PdgId[i]) == 13]
            for i in range(electronsObs["Electrons"].size()):
                signedGenElectrons = [ genElectrons[j] for j in range(len(genElectrons)) if var_GenParticles_PdgId[genElectronsIdx[j]] == -11 *  electronsObs["Electrons_charge"][i] ]
                mini, minCan = analysis_ntuples.minDeltaLepLeps(electronsObs["Electrons"][i], signedGenElectrons)
                if mini is None or mini > 0.01:
                    electronsCalcObs["Electrons_matchGen"].push_back(False)
                else:
                    electronsCalcObs["Electrons_matchGen"].push_back(True)
            for i in range(muonsObs["Muons"].size()):
                signedGenMuons = [ genMuons[j] for j in range(len(genMuons)) if var_GenParticles_PdgId[genMuonsIdx[j]] == -13 *  muonsObs["Muons_charge"][i] ]
                mini,minCan = analysis_ntuples.minDeltaLepLeps(muonsObs["Muons"][i], signedGenMuons)
                if mini is None or mini > 0.01:
                    muonsCalcObs["Muons_matchGen"].push_back(False)
                else:
                    muonsCalcObs["Muons_matchGen"].push_back(True)
            for i in range(tracksObs["tracks"].size()):
                signedGenElectrons = [ genElectrons[j] for j in range(len(genElectrons)) if var_GenParticles_PdgId[genElectronsIdx[j]] == -11 *  tracksObs["tracks_charge"][i] ]
                signedGenMuons = [ genMuons[j] for j in range(len(genMuons)) if var_GenParticles_PdgId[genMuonsIdx[j]] == -13 *  tracksObs["tracks_charge"][i] ]
                mini, minCan = analysis_ntuples.minDeltaLepLeps(tracksObs["tracks"][i], signedGenMuons)
                if mini is None or mini > 0.01:
                    mini, minCan = analysis_ntuples.minDeltaLepLeps(tracksObs["tracks"][i], signedGenElectrons)
                    if mini is None or mini > 0.01:
                        muonsCalcObs["Muons_matchGen"].push_back(False)
                    else:
                        muonsCalcObs["Muons_matchGen"].push_back(True)
                else:
                    muonsCalcObs["Muons_matchGen"].push_back(True)
        
        for lep in ["Muons", "Electrons", "tracks"]:
            for CorrJetObs in utils.leptonIsolationIncList:
                ptRanges = [""]
                drCuts = [""]
                if CorrJetObs in ["CorrJetIso", "CorrJetD3Iso", "CorrJetNoMultIso", "CorrJetNoMultD3Iso"]:
                    ptRanges = utils.leptonCorrJetIsoPtRange
                    drCuts = utils.leptonCorrJetIsoDrCuts
                for ptRange in ptRanges:
                    for drCut in drCuts:
                        cuts = ""
                        if len(str(ptRange)) > 0:
                            cuts = str(ptRange) + "Dr" + str(drCut)
                        leptonsCorrJetVars[lep + "_pass" + CorrJetObs + cuts] = cppyy.gbl.std.vector(eval(utils.leptonsCorrJetVecList[CorrJetObs]))()
                        # This is not saved to the root files
                        leptonsCorrJetVars[lep + "_minDr" + CorrJetObs + cuts] = cppyy.gbl.std.vector(double)()
        
        isoJets = {"electron" : {"obs" : "Electrons"}, "muon" : {"obs" : "Muons"}, "track" : {"obs" : "tracks"}}
        isoJetsIdx = {"electron" : {"obs" : "Electrons"}, "muon" : {"obs" : "Muons"}, "track" : {"obs" : "tracks"}}
        for lepIso in utils.leptonIsolationList:
            for lep in isoJets:
                if lepIso in ["CorrJetIso", "CorrJetNoMultIso"]:
                    continue
                elif lepIso == "JetIso":
                    #isoJets[lep][lepIso] =  [var_Jets[j] for j in range(len(var_Jets)) if var_Jets[j].Pt() > 25 and (var_Jets_multiplicity[j] >=10 or eval("var_Jets_" + lep + "EnergyFraction")[j] <= (0.3 if lep == "electron" else 0.1))]
                    isoJets[lep][lepIso] =  [ jetsObs["Jets"][j] for j in range(len(jetsObs["Jets"])) if jetsObs["Jets"][j].Pt() > 15 ]
                    isoJets[lep]["JetD3Iso"] =  [ jetsObs["Jets"][j] for j in range(len(jetsObs["Jets"])) if jetsObs["Jets"][j].Pt() < 30 and  jetsObs["Jets"][j].Pt() > 15 ]
                #elif lepIso == "NonJetIso":
                #    isoJets[lep][lepIso] = [ jetsObs["Jets"][j] for j in range(len(jetsObs["Jets"])) ]# if var_Jets[j].Pt() > 25 ]
        
        for lep in isoJets:

            leptonsVecName = isoJets[lep]["obs"]
            leptonsVec = eval(leptonsVecName.lower() + "Obs")[leptonsVecName]
            
            for i in range(leptonsVec.size()):
                leptonsCorrJetVars[isoJets[lep]["obs"] + "_passNoIso"].push_back(True)
                mini, minCan = analysis_ntuples.minDeltaLepLeps(leptonsVec[i], jetsObs["Jets"])
                if mini is None:
                    eval(leptonsVecName.lower() + "CalcObs")[leptonsVecName  + "_minDeltaRJets"].push_back(-1)
                    eval(leptonsVecName.lower() + "CalcObs")[leptonsVecName  + "_closestJet"].push_back(-1)
                else:
                    eval(leptonsVecName.lower() + "CalcObs")[leptonsVecName  + "_minDeltaRJets"].push_back(mini)
                    eval(leptonsVecName.lower() + "CalcObs")[leptonsVecName  + "_closestJet"].push_back(minCan)
                
        
        jetsCalcObs["Jets_muonCorrected"] = cppyy.gbl.std.vector(TLorentzVector)(jetsObs["Jets"])
        jetsCalcObs["Jets_electronCorrected"] = cppyy.gbl.std.vector(TLorentzVector)(jetsObs["Jets"])
        jetsCalcObs["Jets_trackCorrected"] = cppyy.gbl.std.vector(TLorentzVector)(jetsObs["Jets"])
        
        #non_iso_jet_electrons = [ i for i in range(len(electronsObs["Electrons"])) if analysis_ntuples.electronPassesKinematicSelection(i, electronsObs["Electrons"], electronsCalcObs["Electrons_deltaRLJ"]) and electronsCalcObs["Electrons_minDeltaRJets"][i] >= 0 and electronsCalcObs["Electrons_minDeltaRJets"][i] < 0.4 ]
        #non_iso_jet_muons = [ i for i in range(len(muonsObs["Muons"])) if analysis_ntuples.muonPassesLooseSelection(i, muonsObs["Muons"], muonsObs["Muons_mediumID"], muonsCalcObs["Muons_deltaRLJ"])and muonsCalcObs["Muons_minDeltaRJets"][i] >= 0 and muonsCalcObs["Muons_minDeltaRJets"][i] < 0.4 ]
        
        # REVIEW CR HERE -> Should be 0.3?
        # changing this definition. We no longer ignore high-Pt leptons, and we no longer look at the leading jet
        non_iso_jet_electrons = [ i for i in range(len(electronsObs["Electrons"])) if electronsCalcObs["Electrons_minDeltaRJets"][i] >= 0 and electronsCalcObs["Electrons_minDeltaRJets"][i] < 0.4 ]
        non_iso_jet_muons = [ i for i in range(len(muonsObs["Muons"])) if analysis_ntuples.muonPassesJetIsoSelection(i, muonsObs["Muons"], muonsObs["Muons_mediumID"]) and muonsCalcObs["Muons_minDeltaRJets"][i] >= 0 and muonsCalcObs["Muons_minDeltaRJets"][i] < 0.4 ]
        non_iso_jet_tracks = [ i for i in range(len(tracksObs["tracks"])) if abs(tracksObs["tracks"][i].Eta()) < 2.4 and tracksObs["tracks_trkRelIso"][i] < 0.1 and tracksObs["tracks_dxyVtx"][i] < 0.02 and tracksObs["tracks_dzVtx"][i] < 0.05 and tracksCalcObs["tracks_minDeltaRJets"][i] >= 0 and tracksCalcObs["tracks_minDeltaRJets"][i] < 0.4]
        
        for i in non_iso_jet_electrons:
            for j in range(jetsCalcObs["Jets_electronCorrected"].size()):
                if jetsCalcObs["Jets_electronCorrected"][j].DeltaR(electronsObs["Electrons"][i]) < 0.4:
                    jetsCalcObs["Jets_electronCorrected"][j] -= electronsObs["Electrons"][i]
        for i in non_iso_jet_muons:
            for j in range(jetsCalcObs["Jets_muonCorrected"].size()):
                if jetsCalcObs["Jets_muonCorrected"][j].DeltaR(muonsObs["Muons"][i]) < 0.4:
                    jetsCalcObs["Jets_muonCorrected"][j] -= muonsObs["Muons"][i]
        for i in non_iso_jet_tracks:
            for j in range(jetsCalcObs["Jets_trackCorrected"].size()):
                if jetsCalcObs["Jets_trackCorrected"][j].DeltaR(tracksObs["tracks"][i]) < 0.4:
                    jetsCalcObs["Jets_trackCorrected"][j] -= tracksObs["tracks"][i]
        
        for lepIso in utils.leptonIsolationList:
            for lep in isoJets:
                if lepIso not in ["CorrJetIso", "CorrJetNoMultIso"]:
                    continue
                for ptRange in utils.leptonCorrJetIsoPtRange:
                    if lepIso == "CorrJetIso":
                        isoJets[lep][lepIso+str(ptRange)] = [jetsCalcObs["Jets_" + lep + "Corrected"][j] for j in range(len(jetsCalcObs["Jets_" + lep + "Corrected"])) if jetsObs["Jets_multiplicity"][j] >=10 or (jetsCalcObs["Jets_" + lep + "Corrected"][j].E() > 0 and jetsCalcObs["Jets_" + lep + "Corrected"][j].Pt() > ptRange)]
                        isoJetsIdx[lep][lepIso+str(ptRange)] = [j for j in range(len(jetsCalcObs["Jets_" + lep + "Corrected"])) if jetsObs["Jets_multiplicity"][j] >=10 or (jetsCalcObs["Jets_" + lep + "Corrected"][j].E() > 0 and jetsCalcObs["Jets_" + lep + "Corrected"][j].Pt() > ptRange)]
                    elif lepIso == "CorrJetNoMultIso":
                        isoJets[lep][lepIso+str(ptRange)] = [jetsCalcObs["Jets_" + lep + "Corrected"][j] for j in range(len(jetsCalcObs["Jets_" + lep + "Corrected"])) if (jetsCalcObs["Jets_" + lep + "Corrected"][j].E() > 0 and jetsCalcObs["Jets_" + lep + "Corrected"][j].Pt() > ptRange)]
                        isoJetsIdx[lep][lepIso+str(ptRange)] = [j for j in range(len(jetsCalcObs["Jets_" + lep + "Corrected"])) if (jetsCalcObs["Jets_" + lep + "Corrected"][j].E() > 0 and jetsCalcObs["Jets_" + lep + "Corrected"][j].Pt() > ptRange)]
                        
        for lep in isoJets:
             
            leptonsVecName = isoJets[lep]["obs"]
            leptonsVec = eval(leptonsVecName.lower() + "Obs")[leptonsVecName]
            
            for i in range(leptonsVec.size()):
                mini, minCan = analysis_ntuples.minDeltaLepLeps(leptonsVec[i], jetsCalcObs["Jets_" + lep + "Corrected"])
                if mini is None:
                    eval(leptonsVecName.lower() + "CalcObs")[leptonsVecName  +  "_correctedMinDeltaRJets"].push_back(-1)
                    eval(leptonsVecName.lower() + "CalcObs")[leptonsVecName  +  "_correctedClosestJet"].push_back(-1)
                    for ptRange in utils.leptonCorrJetIsoPtRange:
                        for drCut in utils.leptonCorrJetIsoDrCuts:
                            cuts = str(ptRange) + "Dr" + str(drCut)
                            print("***We don't have any JET?")
                            #leptonsCorrJetVars[isoJets[lep]["obs"] + "_passCorrJetIso" + cuts].push_back(True)
                            leptonsCorrJetVars[isoJets[lep]["obs"] + "_passCorrJetNoMultIso" + cuts].push_back(True)
                            #leptonsCorrJetVars[isoJets[lep]["obs"] + "_passCorrJetD3Iso" + cuts].push_back(False)
                            leptonsCorrJetVars[isoJets[lep]["obs"] + "_passCorrJetNoMultD3Iso" + cuts].push_back(False)
                else:
                    eval(leptonsVecName.lower() + "CalcObs")[leptonsVecName  +  "_correctedMinDeltaRJets"].push_back(mini)
                    eval(leptonsVecName.lower() + "CalcObs")[leptonsVecName  +  "_correctedClosestJet"].push_back(minCan)
                    
                    for lepIso in ["CorrJetNoMultIso"]:#["CorrJetIso", "CorrJetNoMultIso"]:
                        d3Iso = "CorrJetD3Iso" if lepIso == "CorrJetIso" else "CorrJetNoMultD3Iso"
                        for ptRange in utils.leptonCorrJetIsoPtRange:
                        
                            mini, minCan = analysis_ntuples.minDeltaLepLeps(leptonsVec[i], isoJets[lep][lepIso+str(ptRange)])
                        
                            for drCut in utils.leptonCorrJetIsoDrCuts:
                            
                                cuts = str(ptRange) + "Dr" + str(drCut)
                            
                                if mini is None or mini > drCut:
                                    leptonsCorrJetVars[isoJets[lep]["obs"] + "_pass" + lepIso + cuts].push_back(True)
                                else:
                                    leptonsCorrJetVars[isoJets[lep]["obs"] + "_pass" + lepIso + cuts].push_back(False)
                                ### REVIEW CR
                                if mini is not None and mini < drCut and jetsObs["Jets"][isoJetsIdx[lep][lepIso+str(ptRange)][minCan]].Pt() < 30: #and mini >= 0.2
                                    leptonsCorrJetVars[isoJets[lep]["obs"] + "_pass"+ d3Iso + cuts].push_back(True)
                                    leptonsCorrJetVars[isoJets[lep]["obs"] + "_minDr" + d3Iso + cuts].push_back(mini)
                                else:
                                    leptonsCorrJetVars[isoJets[lep]["obs"] + "_pass"+ d3Iso + cuts].push_back(False)
                                    leptonsCorrJetVars[isoJets[lep]["obs"] + "_minDr"+ d3Iso + cuts].push_back(-1)
        
        for lep in ["Muons", "Electrons", "tracks"]:
            for CorrJetObs in utils.leptonIsolationIncList:
                if CorrJetObs in ["CorrJetIso", "CorrJetD3Iso", "CorrJetNoMultIso", "CorrJetNoMultD3Iso"]:
                    for ptRange in utils.leptonCorrJetIsoPtRange:
                        for drCut in utils.leptonCorrJetIsoDrCuts:
                            cuts = str(ptRange) + "Dr" + str(drCut)
                            tEvent.SetBranchAddress(lep + "_pass" + CorrJetObs + cuts, leptonsCorrJetVars[lep + "_pass" + CorrJetObs + cuts])
                else:
                    #print lep + "_pass" + CorrJetObs, leptonsCorrJetVars[lep + "_pass" + CorrJetObs]
                    tEvent.SetBranchAddress(lep + "_pass" + CorrJetObs, leptonsCorrJetVars[lep + "_pass" + CorrJetObs])
        
        tight_electrons = [ electronsObs["Electrons"][i] for i in range(len(electronsObs["Electrons"])) if analysis_ntuples.electronPassesTightSelection(i, electronsObs["Electrons"], leptonsCorrJetVars["Electrons_pass" + utils.defaultJetIsoSetting], electronsCalcObs["Electrons_deltaRLJ"]) ]
        tight_muons = [ muonsObs["Muons"][i] for i in range(len(muonsObs["Muons"])) if analysis_ntuples.muonPassesTightSelection(i, muonsObs["Muons"], muonsObs["Muons_mediumID"], leptonsCorrJetVars["Muons_pass" + utils.defaultJetIsoSetting], muonsCalcObs["Muons_deltaRLJ"]) ]
        
        mini, minCan = analysis_ntuples.minDeltaLepLeps(var_LeadingJet, tight_electrons)
        if minCan is None:
            commonCalcFlatObs["LeadingJetMinDeltaRElectrons"][0] = -1
        else:
            commonCalcFlatObs["LeadingJetMinDeltaRElectrons"][0] = mini
            
        mini, minCan = analysis_ntuples.minDeltaLepLeps(var_LeadingJet, tight_muons)
        if minCan is None:
            commonCalcFlatObs["LeadingJetMinDeltaRMuons"][0] = -1
        else:
            commonCalcFlatObs["LeadingJetMinDeltaRMuons"][0] = mini
        
        for vecObs in analysis_observables.dileptonObservablesVecList:
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
                            postfixi = [iso + cuts + cat]
                            if iso + cuts + cat == utils.defaultJetIsoSetting:
                                postfixi = [iso + cuts + cat, ""]
                            for postfix in postfixi:
                                dileptonVars[vecObs + postfix] = cppyy.gbl.std.vector(eval(analysis_observables.dileptonObservablesVecList[vecObs]))()
                                if postfix == utils.defaultJetIsoSetting:
                                    dileptonVars[vecObs] = cppyy.gbl.std.vector(eval(analysis_observables.dileptonObservablesVecList[vecObs]))()
                            
        foundTwoLeptons = False
        foundSingleLepton = False
        
        commonCalcFlatObs["category"][0] = 0
            
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
                        postfixi = [iso + cuts + cat]
                
                        if iso + cuts + cat == utils.defaultJetIsoSetting:
                            postfixi = [iso + cuts + cat, ""]
                
                        #print "default=", utils.defaultJetIsoSetting
                        #print iso + str(ptRange) + cat, postfixi
                
                        for DTypeObs in analysis_observables.dileptonObservablesDTypesList:
                            for postfix in postfixi:
                                if analysis_observables.dileptonObservablesDTypesList[DTypeObs] == "bool":
                                    dileptonVars[DTypeObs + postfix][0] = 0
                                else:
                                    dileptonVars[DTypeObs + postfix][0] = -1
                
                        leptonsNum = analysis_ntuples.countLeptonsAfterSelection(electronsObs["Electrons"], leptonsCorrJetVars["Electrons_pass" + iso + cuts], electronsCalcObs["Electrons_deltaRLJ"], electronsObs["Electrons_charge"], muonsObs["Muons"], leptonsCorrJetVars["Muons_pass" + iso + cuts], muonsObs["Muons_mediumID"], muonsCalcObs["Muons_deltaRLJ"], muonsObs["Muons_charge"], utils.leptonIsolationCategories[cat]["muonPt"], utils.leptonIsolationCategories[cat]["lowPtTightMuons"], muonsObs["Muons_tightID"])
                        for postfix in postfixi:
                            dileptonVars["NSelectionLeptons" + postfix][0] = leptonsNum
                            dileptonVars["vetoElectrons" + postfix][0] = 0 if len([ i for i in range(electronsObs["Electrons"].size()) if electronsObs["Electrons"][i].Pt() > 15 and bool(leptonsCorrJetVars["Electrons_pass" + iso + cuts][i]) ]) == 0 else 1
                            dileptonVars["vetoMuons" + postfix][0] = 0 if len([ i for i in range(muonsObs["Muons"].size()) if muonsObs["Muons"][i].Pt() > 15 and  bool(leptonsCorrJetVars["Muons_pass" + iso + cuts][i]) ]) == 0 else 1
                
                        leptons, leptonsIdx, leptonsCharge, leptonFlavour, same_sign, isoCr, isoCrMinDr = None, None, None, None, None, 0, -1
                
                        if jpsi_muons:
                            leptonFlavour = "Muons"
                            same_sign = False
                            leptons, leptonsIdx, leptonsCharge = analysis_ntuples.getTwoJPsiLeptonsAfterSelection(24, 24, muonsObs["Muons"], leptonsCorrJetVars["Muons_pass" + iso + cuts], muonsObs["Muons_mediumID"], muonsObs["Muons_charge"], utils.leptonIsolationCategories[cat]["muonPt"], utils.leptonIsolationCategories[cat]["lowPtTightMuons"], muonsObs["Muons_tightID"], muonsObs["Muons_passIso"])
                            #print ientry
                            #print ientry, leptons, leptonsIdx, leptonsCharge
                        else:
                            # need to see how to make it work for noiso too.....
                            #print(leptonsCorrJetVars)
                            if iso == "CorrJetIso":
                                leptons, leptonsIdx, leptonsCharge, leptonFlavour, same_sign, isoCr, isoCrMinDr = analysis_ntuples.getTwoLeptonsAfterSelection(electronsObs["Electrons"], leptonsCorrJetVars["Electrons_pass" + iso + cuts], electronsCalcObs["Electrons_deltaRLJ"], electronsObs["Electrons_charge"], muonsObs["Muons"], leptonsCorrJetVars["Muons_pass" + iso + cuts], muonsObs["Muons_mediumID"], muonsCalcObs["Muons_deltaRLJ"], muonsObs["Muons_charge"], utils.leptonIsolationCategories[cat]["muonPt"], utils.leptonIsolationCategories[cat]["lowPtTightMuons"], muonsObs["Muons_tightID"], True, leptonsCorrJetVars["Electrons_passCorrJetD3Iso" + cuts], leptonsCorrJetVars["Muons_passCorrJetD3Iso" + cuts], leptonsCorrJetVars["Electrons_minDrCorrJetD3Iso" + cuts], leptonsCorrJetVars["Muons_minDrCorrJetD3Iso" + cuts])
                            elif iso == "CorrJetNoMultIso":
                                leptons, leptonsIdx, leptonsCharge, leptonFlavour, same_sign, isoCr, isoCrMinDr = analysis_ntuples.getTwoLeptonsAfterSelection(electronsObs["Electrons"], leptonsCorrJetVars["Electrons_pass" + iso + cuts], electronsCalcObs["Electrons_deltaRLJ"], electronsObs["Electrons_charge"], muonsObs["Muons"], leptonsCorrJetVars["Muons_pass" + iso + cuts], muonsObs["Muons_mediumID"], muonsCalcObs["Muons_deltaRLJ"], muonsObs["Muons_charge"], utils.leptonIsolationCategories[cat]["muonPt"], utils.leptonIsolationCategories[cat]["lowPtTightMuons"], muonsObs["Muons_tightID"], True, leptonsCorrJetVars["Electrons_passCorrJetNoMultD3Iso" + cuts], leptonsCorrJetVars["Muons_passCorrJetNoMultD3Iso" + cuts], leptonsCorrJetVars["Electrons_minDrCorrJetNoMultD3Iso" + cuts], leptonsCorrJetVars["Muons_minDrCorrJetNoMultD3Iso" + cuts])
                            elif iso == "JetIso":
                                leptons, leptonsIdx, leptonsCharge, leptonFlavour, same_sign, isoCr, isoCrMinDr = analysis_ntuples.getTwoLeptonsAfterSelection(electronsObs["Electrons"], leptonsCorrJetVars["Electrons_pass" + iso + cuts], electronsCalcObs["Electrons_deltaRLJ"], electronsObs["Electrons_charge"], muonsObs["Muons"], leptonsCorrJetVars["Muons_pass" + iso + cuts], muonsObs["Muons_mediumID"], muonsCalcObs["Muons_deltaRLJ"], muonsObs["Muons_charge"], utils.leptonIsolationCategories[cat]["muonPt"], utils.leptonIsolationCategories[cat]["lowPtTightMuons"], muonsObs["Muons_tightID"], True, leptonsCorrJetVars["Electrons_passJetD3Iso"], leptonsCorrJetVars["Muons_passJetD3Iso"], leptonsCorrJetVars["Electrons_minDrJetD3Iso"], leptonsCorrJetVars["Muons_minDrJetD3Iso"])
                            else:
                                leptons, leptonsIdx, leptonsCharge, leptonFlavour, same_sign, isoCr, isoCrMinDr = analysis_ntuples.getTwoLeptonsAfterSelection(electronsObs["Electrons"], leptonsCorrJetVars["Electrons_pass" + iso + cuts], electronsCalcObs["Electrons_deltaRLJ"], electronsObs["Electrons_charge"], muonsObs["Muons"], leptonsCorrJetVars["Muons_pass" + iso + cuts], muonsObs["Muons_mediumID"], muonsCalcObs["Muons_deltaRLJ"], muonsObs["Muons_charge"], utils.leptonIsolationCategories[cat]["muonPt"], utils.leptonIsolationCategories[cat]["lowPtTightMuons"], muonsObs["Muons_tightID"])
                
                        if leptons is None:
                            if jpsi_muons:
                                ll, leptonIdx, t, ti = analysis_ntuples.getSingleJPsiLeptonAfterSelection(24, 24, muonsObs["Muons"], leptonsCorrJetVars["Muons_pass" + iso + cuts], muonsObs["Muons_mediumID"], muonsObs["Muons_charge"], tracksObs["tracks"], tracksObs["tracks_charge"], utils.leptonIsolationCategories[cat]["muonPt"], utils.leptonIsolationCategories[cat]["lowPtTightMuons"], muonsObs["Muons_tightID"], muonsObs["Muons_passIso"])
                            else:
                                ll, leptonIdx, leptonCharge, leptonFlavour = analysis_ntuples.getSingleLeptonAfterSelection(electronsObs["Electrons"], leptonsCorrJetVars["Electrons_pass" + iso + cuts], electronsCalcObs["Electrons_deltaRLJ"], electronsObs["Electrons_charge"], muonsObs["Muons"], leptonsCorrJetVars["Muons_pass" + iso + cuts], muonsObs["Muons_mediumID"], muonsCalcObs["Muons_deltaRLJ"], muonsObs["Muons_charge"], utils.leptonIsolationCategories[cat]["muonPt"], utils.leptonIsolationCategories[cat]["lowPtTightMuons"], muonsObs["Muons_tightID"])
            
                            if ll is not None:
                                if nT > 0 and (jpsi_muons or commonCalcFlatObs["BTagsLoose"][0] == 0 or commonCalcFlatObs["BTagsMedium"][0] == 0 or commonCalcFlatObs["BTagsDeepLoose"][0] == 0 or commonCalcFlatObs["BTagsDeepMedium"][0] == 0):
                                    commonCalcFlatObs["category"][0] = 1
                                    foundSingleLepton = True
                        #if leptons is not None and (jpsi_muons or commonCalcFlatObs["BTagsLoose"][0] < 3 or commonCalcFlatObs["BTagsMedium"][0] < 3 or commonCalcFlatObs["BTagsDeepLoose"][0] < 3 or commonCalcFlatObs["BTagsDeepMedium"][0] < 3):
                        if leptons is not None and (jpsi_muons or commonCalcFlatObs["BTagsLoose"][0] == 0 or commonCalcFlatObs["BTagsMedium"][0] == 0 or commonCalcFlatObs["BTagsDeepLoose"][0] == 0 or commonCalcFlatObs["BTagsDeepMedium"][0] == 0):
                
                            #print var_BTagsLoose[0], var_BTagsMedium[0], var_BTagsDeepLoose[0], var_BTagsDeepMedium[0]
                
                            foundTwoLeptons = True
                            #print "foundTwoLeptons!!!", ientry
                            #print ientry, leptons, leptonsIdx, leptonsCharge, leptonFlavour, same_sign
                    
                            pt = TLorentzVector()
                            pt.SetPtEtaPhiE(MET,0,METPhi,MET)
                            
                            mhtvec = TLorentzVector()
                            mhtvec.SetPtEtaPhiE(MHT,0,MHTPhi,MHT)
                    
                            for postfix in postfixi:
                    
                                #print ientry, postfix, leptons, leptonsIdx, leptonsCharge, leptonFlavour, same_sign
                        
                                dileptonVars["isoCr" + postfix][0] = isoCr
                                dileptonVars["isoCrMinDr" + postfix][0] = isoCrMinDr
                    
                                dileptonVars["leptons" + postfix].push_back(leptons[0].Clone())
                                dileptonVars["leptons" + postfix].push_back(leptons[1].Clone())
                    
                                dileptonVars["leptonsIdx" + postfix].push_back(leptonsIdx[0])
                                dileptonVars["leptonsIdx" + postfix].push_back(leptonsIdx[1])
                    
                                dileptonVars["leptons_charge" + postfix].push_back(leptonsCharge[0])
                                dileptonVars["leptons_charge" + postfix].push_back(leptonsCharge[1])
                        
                                if leptonFlavour is None:
                                    print("Wow, something is weird")
                                    print(leptons, leptonsIdx, leptonsCharge, leptonFlavour, same_sign, isoCr)
                        
                                dileptonVars["leptonFlavour" + postfix] = cppyy.gbl.std.string(leptonFlavour)
                    
                                dileptonVars["twoLeptons" + postfix][0] = 1
                    
                                dileptonVars["sameSign" + postfix][0] = 1 if same_sign else 0
                    
                                dileptonVars["invMass" + postfix][0] =  (leptons[0] + leptons[1]).M()
                                dileptonVars["dileptonPt" + postfix][0] = abs((leptons[0] + leptons[1]).Pt())
                                dileptonVars["deltaPhi" + postfix][0] = abs(leptons[0].DeltaPhi(leptons[1]))
                                dileptonVars["deltaEta" + postfix][0] = abs(leptons[0].Eta() - leptons[1].Eta())
                                dileptonVars["deltaR" + postfix][0] = abs(leptons[0].DeltaR(leptons[1]))
                                dileptonVars["pt3" + postfix][0] = analysis_tools.pt3(leptons[0].Pt(),leptons[0].Phi(),leptons[1].Pt(),leptons[1].Phi(),MET,METPhi)
                                dileptonVars["mt1" + postfix][0] = analysis_tools.MT2(MET, METPhi, leptons[0])
                                dileptonVars["mt2" + postfix][0] = analysis_tools.MT2(MET, METPhi, leptons[1])
                                dileptonVars["mth1" + postfix][0] = analysis_tools.MT2(MHT, MHTPhi, leptons[0])
                                dileptonVars["mth2" + postfix][0] = analysis_tools.MT2(MHT, MHTPhi, leptons[1])
                        
                                #if leptons[0].Pt() < 1 or leptons[1].Pt() < 1:
                                #    print "FUCK!"
                                #    exit(0)
                        
                                #print postfix
                                #print ientry
                                dileptonVars["mtautau" + postfix][0] = analysis_tools.Mtautau(pt, leptons[0], leptons[1])
                                dileptonVars["nmtautau" + postfix][0] = analysis_tools.Mtautau2(pt, leptons[0], leptons[1])
                                dileptonVars["deltaEtaLeadingJetDilepton" + postfix][0] = abs((leptons[0] + leptons[1]).Eta() - var_LeadingJet.Eta())
                                dileptonVars["deltaPhiLeadingJetDilepton" + postfix][0] = abs((leptons[0] + leptons[1]).DeltaPhi(var_LeadingJet))
                                dileptonVars["dilepHt" + postfix][0] = analysis_ntuples.htJet30Leps(jetsObs["Jets"], leptons)
                                dileptonVars["deltaPhiMetLepton1" + postfix][0] = abs(leptons[0].DeltaPhi(pt))
                                dileptonVars["deltaPhiMetLepton2" + postfix][0] = abs(leptons[1].DeltaPhi(pt))
                                
                                dileptonVars["deltaPhiMhtLepton1" + postfix][0] = abs(leptons[0].DeltaPhi(mhtvec))
                                dileptonVars["deltaPhiMhtLepton2" + postfix][0] = abs(leptons[1].DeltaPhi(mhtvec))
                        
                                if not data:
                                    gens = [i for i in range(var_GenParticles.size())]
                                    lepCans = []
                                    numRealLeptons = 0
    
                                    for i in range(len(leptons)):
                                        lepton = leptons[i]
                                        mini, minCan = analysis_ntuples.minDeltaRGenParticles(lepton, gens, var_GenParticles)
                                        pdgId = var_GenParticles_ParentId[minCan]
                                        if mini > 0.01:
                                            #print "BAD GEN!!! ", min
                                            pdgId = 0
                                        else:
                                            if ((abs(var_GenParticles_PdgId[minCan]) == 13 and leptonFlavour == "Muons") or (abs(var_GenParticles_PdgId[minCan]) == 11 and leptonFlavour == "Electrons")) and leptonsCharge[i] * var_GenParticles_PdgId[minCan] < 0:
                                                numRealLeptons += 1
                                                lepCans.append(minCan)
                                            else:
                                                #print "BAD GEN MATCH! "
                                                pdgId = 0
                                            dileptonVars["leptons_ParentPdgId" + postfix].push_back(pdgId)

                                    if bg:
                                        if numRealLeptons == 0:
                                            dileptonVars["ff" + postfix][0] = True
                                        elif numRealLeptons == 1:
                                            dileptonVars["rf" + postfix][0] = True
                                        else:
                                            dileptonVars["rr" + postfix][0] = True
                                            if abs(dileptonVars["leptons_ParentPdgId" + postfix][0]) == abs(dileptonVars["leptons_ParentPdgId" + postfix][1]) == 15:
                                                dileptonVars["tautau" + postfix][0] = True
            
                                            parentIdx = var_GenParticles_ParentIdx[lepCans[0]]
                                            parentIdx2 = var_GenParticles_ParentIdx[lepCans[1]]
                                            if parentIdx == -1 and parentIdx2 == -1:
                                                dileptonVars["other" + postfix][0] = True
                                                if abs(dileptonVars["leptons_ParentPdgId" + postfix][0]) == abs(dileptonVars["leptons_ParentPdgId" + postfix][1]) == 223:
                                                    dileptonVars["omega" + postfix][0] = True
                                                elif abs(dileptonVars["leptons_ParentPdgId" + postfix][0]) == abs(dileptonVars["leptons_ParentPdgId" + postfix][1]) == 113:
                                                    dileptonVars["rho_0" + postfix][0] = True
                                                elif abs(dileptonVars["leptons_ParentPdgId" + postfix][0]) == abs(dileptonVars["leptons_ParentPdgId" + postfix][1]) == 221:
                                                    dileptonVars["eta" + postfix][0] = True
                                                elif abs(dileptonVars["leptons_ParentPdgId" + postfix][0]) == abs(dileptonVars["leptons_ParentPdgId" + postfix][1]) == 333:
                                                    dileptonVars["phi" + postfix][0] = True
                                                elif abs(dileptonVars["leptons_ParentPdgId" + postfix][0]) == abs(dileptonVars["leptons_ParentPdgId" + postfix][1]) == 331:
                                                    dileptonVars["eta_prime" + postfix][0] = True
                                                elif abs(dileptonVars["leptons_ParentPdgId" + postfix][0]) == abs(dileptonVars["leptons_ParentPdgId" + postfix][1]) == 443:
                                                    dileptonVars["j_psi" + postfix][0] = True
                                                elif abs(dileptonVars["leptons_ParentPdgId" + postfix][0]) == abs(dileptonVars["leptons_ParentPdgId" + postfix][1]) == 553:
                                                    dileptonVars["upsilon_1" + postfix][0] = True
                                                elif abs(dileptonVars["leptons_ParentPdgId" + postfix][0]) == abs(dileptonVars["leptons_ParentPdgId" + postfix][1]) == 100553:
                                                    dileptonVars["upsilon_2" + postfix][0] = True
                                            else:
                                                if var_GenParticles_ParentIdx[lepCans[0]] == var_GenParticles_ParentIdx[lepCans[1]]:
                                                    numOfParentChildren = 0
                                                    for i in range(var_GenParticles.size()):
                                                        if var_GenParticles_Status[i] == 1 and var_GenParticles_ParentIdx[i] == parentIdx:
                                                            numOfParentChildren += 1
                                                    #print "numOfParentChildren=", numOfParentChildren, "var_leptons_ParentPdgId[0]", var_leptons_ParentPdgId[0], "var_GenParticles_PdgId[parentIdx]", var_GenParticles_PdgId[parentIdx], "var_GenParticles_PdgId[parentIdx2]", var_GenParticles_PdgId[parentIdx2]
                                                    #print lepCans
                                                    if numOfParentChildren == 2:
                                                        dileptonVars["sc" + postfix][0] = True
                                                        if abs(var_GenParticles_PdgId[parentIdx]) == 223:
                                                            dileptonVars["omega" + postfix][0] = True
                                                        elif abs(var_GenParticles_PdgId[parentIdx]) == 113:
                                                            dileptonVars["rho_0" + postfix][0] = True
                                                        elif abs(var_GenParticles_PdgId[parentIdx]) == 221:
                                                            dileptonVars["eta" + postfix][0] = True
                                                        elif abs(var_GenParticles_PdgId[parentIdx]) == 333:
                                                            dileptonVars["phi" + postfix][0] = True
                                                        elif abs(var_GenParticles_PdgId[parentIdx]) == 331:
                                                            dileptonVars["eta_prime" + postfix][0] = True
                                                        elif abs(var_GenParticles_PdgId[parentIdx]) == 443:
                                                            dileptonVars["j_psi" + postfix][0] = True
                                                        elif abs(var_GenParticles_PdgId[parentIdx]) == 553:
                                                            dileptonVars["upsilon_1" + postfix][0] = True
                                                        elif abs(var_GenParticles_PdgId[parentIdx]) == 100553:
                                                            dileptonVars["upsilon_2" + postfix][0] = True
                                                    else:
                                                        dileptonVars["n_body" + postfix][0] = True
                                                else:
                                                    dileptonVars["tc" + postfix][0] = True
                            
                        for postfix in postfixi:
                            for vecObs in analysis_observables.dileptonObservablesVecList:
                                #print "tEvent.SetBranchAddress(" + vecObs + postfix +","+ str(dileptonVars[vecObs + postfix]) + ")"
                                tEvent.SetBranchAddress(vecObs + postfix, dileptonVars[vecObs + postfix])
                            for stringObs in analysis_observables.dileptonObservablesStringList:
                                #print "tEvent.SetBranchAddress(" + stringObs + postfix +","+ str(dileptonVars[stringObs + postfix]) + ")"
                                tEvent.SetBranchAddress(stringObs + postfix, dileptonVars[stringObs + postfix])
        
        if not foundTwoLeptons and dy:
            continue
        
        if not no_lepton_selection and not foundTwoLeptons and not foundSingleLepton:
            continue

        afterLeptons += 1
        
        for i in range(len(tracksObs["tracks"])):
            t = tracksObs["tracks"][i]
            
            mini, minCan = analysis_ntuples.minDeltaLepLeps(tracksObs["tracks"][i], electronsObs["Electrons"])
            if mini is None or mini > 0.01 or electronsObs["Electrons_charge"][minCan] * tracksObs["tracks_charge"][i] < 0:
                tracksCalcObs["tracks_ei"].push_back(-1)
            else:
                tracksCalcObs["tracks_ei"].push_back(minCan)
            
            mini, minCan = analysis_ntuples.minDeltaLepLeps(tracksObs["tracks"][i], muonsObs["Muons"])
            if mini is None or mini > 0.01 or muonsObs["Muons_charge"][minCan] * tracksObs["tracks_charge"][i] < 0:
                tracksCalcObs["tracks_mi"].push_back(-1)
            else:
                tracksCalcObs["tracks_mi"].push_back(minCan)
        
        
        vetosFlatObs["vetoElectronsPassIso"][0] = 0 if len([ i for i in range(electronsObs["Electrons"].size()) if electronsObs["Electrons"][i].Pt() > 15 and  bool(electronsObs["Electrons_passIso"][i]) ]) == 0 else 1
        #var_vetoElectronsPassJetIso[0] = 0 if len([ i for i in range(len(var_Electrons)) if var_Electrons[i].Pt() > 25 and  bool(var_Electrons_passJetIso[i]) ]) == 0 else 1
        vetosFlatObs["vetoElectronsMediumID"][0] = 0 if len([ i for i in range(electronsObs["Electrons"].size()) if electronsObs["Electrons"][i].Pt() > 15 and  bool(electronsObs["Electrons_mediumID"][i]) ]) == 0 else 1
        vetosFlatObs["vetoElectronsTightID"][0] = 0 if len([ i for i in range(electronsObs["Electrons"].size()) if electronsObs["Electrons"][i].Pt() > 15 and  bool(electronsObs["Electrons_tightID"][i]) ]) == 0 else 1
        
        #vetosFlatObs["vetoElectronsJetIso"][0] = 0 if len([ i for i in range(electronsObs["Electrons"].size()) if electronsObs["Electrons"][i].Pt() > 25 and  bool(electronsObs["Electrons_tightID"][i]) ]) == 0 else 1
        
        vetosFlatObs["vetoMuonsPassIso"][0] = 0 if len([ i for i in range(muonsObs["Muons"].size()) if muonsObs["Muons"][i].Pt() > 15 and  bool(muonsObs["Muons_passIso"][i]) ]) == 0 else 1
        #var_vetoMuonsPassJetIso[0] = 0 if len([ i for i in range(len(var_Muons)) if var_Muons[i].Pt() > 25 and  bool(var_Muons_passJetIso[i]) ]) == 0 else 1
        vetosFlatObs["vetoMuonsMediumID"][0] = 0 if len([ i for i in range(muonsObs["Muons"].size()) if muonsObs["Muons"][i].Pt() > 15 and  bool(muonsObs["Muons_mediumID"][i]) ]) == 0 else 1
        vetosFlatObs["vetoMuonsTightID"][0] = 0 if len([ i for i in range(muonsObs["Muons"].size()) if muonsObs["Muons"][i].Pt() > 15 and  bool(muonsObs["Muons_tightID"][i]) ]) == 0 else 1        
        
        for jetsOb in analysis_observables.jetsObs:
            tEvent.SetBranchAddress(jetsOb, jetsObs[jetsOb])
        
        for jetsCalcOb in analysis_observables.jetsCalcObs:
            tEvent.SetBranchAddress(jetsCalcOb, jetsCalcObs[jetsCalcOb])
        
        if not data:
            for genParticlesOb in analysis_observables.genParticlesObs:
                genParticlesObs[genParticlesOb] = getattr(c, genParticlesOb)
            for genParticlesOb in analysis_observables.genParticlesObs:
                tEvent.SetBranchAddress(genParticlesOb, genParticlesObs[genParticlesOb])
    
        for commonObservablesStringOb in analysis_observables.commonObservablesStringList:
            tEvent.SetBranchAddress(commonObservablesStringOb, commonObservablesStringObs[commonObservablesStringOb])
   
        for tracksOb in analysis_observables.tracksObs:
            tEvent.SetBranchAddress(tracksOb, tracksObs[tracksOb])
        
        for tracksCalcOb in analysis_observables.tracksCalcObs:
            tEvent.SetBranchAddress(tracksCalcOb, tracksCalcObs[tracksCalcOb])
        
        for pionsOb in analysis_observables.pionsObs:
            tEvent.SetBranchAddress(pionsOb, pionsObs[pionsOb])
        
        for photonOb in analysis_observables.photonObs:
            tEvent.SetBranchAddress(photonOb, photonObs[photonOb])
        
        for electronsOb in analysis_observables.electronsObs:
            tEvent.SetBranchAddress(electronsOb, electronsObs[electronsOb])
        
        for electronsCalcOb in analysis_observables.electronsCalcObs:
            tEvent.SetBranchAddress(electronsCalcOb, electronsCalcObs[electronsCalcOb])
        
        for muonsOb in analysis_observables.muonsObs:
            tEvent.SetBranchAddress(muonsOb, muonsObs[muonsOb])
        
        for muonsCalcOb in analysis_observables.muonsCalcObs:
            tEvent.SetBranchAddress(muonsCalcOb, muonsCalcObs[muonsCalcOb])
        
        if dy:
            for muonsOb in analysis_observables.muonsObs:
                tEvent.SetBranchAddress("DY" + muonsOb, dyMuonsObs[muonsOb])

            for dyMuonsClassOb in analysis_observables.dyMuonsClassObs:
                tEvent.SetBranchAddress(dyMuonsClassOb, dyMuonsClassObs[dyMuonsClassOb])
         
        tEvent.SetBranchAddress('LeadingJet', var_LeadingJet)
        
        if signal:
            electronsCalcObs["Electrons_isZ"] = cppyy.gbl.std.vector(bool)()
            muonsCalcObs["Muons_isZ"] = cppyy.gbl.std.vector(bool)()
            commonObservablesStringObs["genFlavour"] = cppyy.gbl.std.string("")
            
            genVecObs["genLeptonsIdx"] = cppyy.gbl.std.vector(int)()
            
            genZL, genNonZL = analysis_ntuples.classifyGenZLeptons(c)
            #print len(genZL)
            
            if genZL is None:
                commonObservablesStringObs["genFlavour"] = cppyy.gbl.std.string("")
                #print "****"
                #print commonObservablesStringObs["genFlavour"]
                for i in range(electronsObs["Electrons"].size()):
                    electronsCalcObs["Electrons_isZ"].push_back(False)
                for i in range(muonsObs["Muons"].size()):
                    muonsCalcObs["Muons_isZ"].push_back(False)
                for i in range(tracksObs["tracks"].size()):
                    tracksCalcObs["tracks_isZ"].push_back(False)
                
                for ob in genCalcObs:
                    genCalcObs[ob][0] = -1
            else:
                
                if  c.GenParticles[genZL[0]].Pt() > c.GenParticles[genZL[1]].Pt():
                    genVecObs["genLeptonsIdx"].push_back(genZL[0])
                    genVecObs["genLeptonsIdx"].push_back(genZL[1])
                    g1 = c.GenParticles[genZL[0]]
                    g2 = c.GenParticles[genZL[1]]
                else:
                    genVecObs["genLeptonsIdx"].push_back(genZL[1])
                    genVecObs["genLeptonsIdx"].push_back(genZL[0])
                    g2 = c.GenParticles[genZL[0]]
                    g1 = c.GenParticles[genZL[1]]
                
                pt = TLorentzVector()
                pt.SetPtEtaPhiE(MET,0,METPhi,MET)
                
                genCalcObs["invMass"][0] = (g1 + g2).M()
                genCalcObs["dileptonPt"][0] = abs((g1 + g2).Pt())
                genCalcObs["deltaPhi"][0] = abs(g1.DeltaPhi(g2))
                genCalcObs["deltaEta"][0] = abs(g1.Eta() - g2.Eta())
                genCalcObs["deltaR"][0] = abs(g1.DeltaR(g2))
                genCalcObs["pt3"][0] = analysis_tools.pt3(g1.Pt(),g1.Phi(),g2.Pt(),g2.Phi(),MET,METPhi)
                genCalcObs["mt1"][0] = analysis_tools.MT2(MET, METPhi, g1)
                genCalcObs["mt2"][0] = analysis_tools.MT2(MET, METPhi, g2)
                genCalcObs["mth1"][0] = analysis_tools.MT2(MHT, MHTPhi, g1)
                genCalcObs["mth2"][0] = analysis_tools.MT2(MHT, MHTPhi, g2)
                genCalcObs["mtautau"][0] = analysis_tools.Mtautau(pt, g1, g2)
                genCalcObs["nmtautau"][0] = analysis_tools.Mtautau(pt, g1, g2)
                genCalcObs["deltaEtaLeadingJetDilepton"][0] = abs((g1 + g2).Eta() - var_LeadingJet.Eta())
                genCalcObs["deltaPhiLeadingJetDilepton"][0] = abs((g1 + g2).DeltaPhi(var_LeadingJet))
                genCalcObs["dilepHt"][0] = analysis_ntuples.htJet30Leps(jetsObs["Jets"], [g1,g2])
                #genCalcObs["deltaPhiMetLepton1"][0] = abs(g1.DeltaPhi(pt))
                #genCalcObs["deltaPhiMetLepton2"][0] = abs(g2.DeltaPhi(pt))
                
                if abs(c.GenParticles_PdgId[genZL[0]]) == 11:
                    commonObservablesStringObs["genFlavour"] = cppyy.gbl.std.string("Electrons")
                    for i in range(electronsObs["Electrons"].size()):
                        electronsCalcObs["Electrons_isZ"].push_back(analysis_ntuples.isLeptonMatchedGen(c.GenParticles, c.GenParticles_PdgId, genZL, genNonZL, i, electronsObs["Electrons"], electronsObs["Electrons_charge"], -11))
                    for i in range(muonsObs["Muons"].size()):
                        muonsCalcObs["Muons_isZ"].push_back(False)
                else:
                    commonObservablesStringObs["genFlavour"] = cppyy.gbl.std.string("Muons")
                    for i in range(muonsObs["Muons"].size()):
                        muonsCalcObs["Muons_isZ"].push_back(analysis_ntuples.isLeptonMatchedGen(c.GenParticles, c.GenParticles_PdgId, genZL, genNonZL, i, muonsObs["Muons"], muonsObs["Muons_charge"], -13))
                    for i in range(electronsObs["Electrons"].size()):
                        electronsCalcObs["Electrons_isZ"].push_back(False)
                for i in range(tracksObs["tracks"].size()):
                    tracksCalcObs["tracks_isZ"].push_back(analysis_ntuples.isLeptonMatchedGen(c.GenParticles, c.GenParticles_PdgId, genZL, genNonZL, i, tracksObs["tracks"], tracksObs["tracks_charge"], 0))
            
            tEvent.SetBranchAddress('genFlavour', commonObservablesStringObs["genFlavour"])
            tEvent.SetBranchAddress('Electrons_isZ', electronsCalcObs["Electrons_isZ"])
            tEvent.SetBranchAddress('Muons_isZ', muonsCalcObs["Muons_isZ"])
            
            for genVecOb in analysis_observables.genObservablesVecList:
                tEvent.SetBranchAddress(genVecOb, genVecObs[genVecOb])
        
        if not signal:
            for triggerOb in analysis_observables.triggerObs:
                tEvent.SetBranchAddress(triggerOb, triggerObs[triggerOb])
            
        metDHt = 9999999
        if c.HT != 0:
            metDHt = MET / c.HT
        
        commonCalcFlatObs["MetDHt"][0] = metDHt
        
        if not ljet:
            commonCalcFlatObs["LeadingJetPartonFlavor"][0] = -1
            commonCalcFlatObs["LeadingJetQgLikelihood"][0] = -1
        else:
            commonCalcFlatObs["LeadingJetPartonFlavor"][0] = jetsObs["Jets_partonFlavor"][ljet]
            commonCalcFlatObs["LeadingJetQgLikelihood"][0] = jetsObs["Jets_qgLikelihood"][ljet]
        
        
        if not data:    
            if signal and sam and not phase1:
                vars["FastSimWeightPR31285To36122"][0] = c.FastSimWeightPR31285To36122 
                #SB needed for pMSSM
                #SB going to switch to new ntuples where this is no longer needed
            else:
                vars["FastSimWeightPR31285To36122"][0] = 1
            
            vars["passedMhtMet6pack"][0] = True
            vars["passedSingleMuPack"][0] = True
            vars["passesUniversalSelection"][0] = True
            tbin = tetrig.FindFixBin(MHT)
            vars["TrgEffNom"][0] = tetrig.GetEfficiency(tbin)
            vars["TrgEffUp"][0] = vars["TrgEffNom"][0]+tetrig.GetEfficiencyErrorUp(tbin)
            vars["TrgEffDown"][0] = vars["TrgEffNom"][0]-tetrig.GetEfficiencyErrorLow(tbin)
            vars["IsrNom"][0], vars["IsrUp"][0], vars["IsrDown"][0] =  get_isr_weight(c)#SB
            sfbtagnom = get_btag_weight(c,nSigmaBtagSF=0,nSigmaBtagFastSimSF=0,isFastSim=1,readerBtag=readerBtag)#SB
            sfbtagup = get_btag_weight(c,nSigmaBtagSF=1,nSigmaBtagFastSimSF=0,isFastSim=1,readerBtag=readerBtag)#SB
            sfbtagdown = get_btag_weight(c,nSigmaBtagSF=-1,nSigmaBtagFastSimSF=0,isFastSim=1,readerBtag=readerBtag)#SB
            vars["BTagNom"][0], vars["BTagUp"][0], vars["BTagDown"][0] =  sfbtagnom, sfbtagup, sfbtagdown#SB
            vars["PuNom"][0], vars["PuUp"][0], vars["PuDown"][0] =  c.puWeight, c.puSysUp, c.puSysDown#SB
            
            vars["ElSfNom"][0], vars["ElSfUp"][0], vars["ElSfDown"][0] = 1, 1, 1
            vars["MuSfNom"][0], vars["MuSfUp"][0], vars["MuSfDown"][0] = 1, 1, 1            
            if muonsObs["Muons"].size()>1:
                lepsfnom = 1.0
                lepsfup = 1.0 
                lepsfdown = 1.0
                for imu in range(2):
                    print('reaching into Is', muIdiso.GetName)
                    xax = muIdiso.GetXaxis()
                    leppt, lepeta = max(xax.GetBinLowEdge(1)+0.000001, muonsObs["Muons"][imu].Pt()), abs(muonsObs["Muons"][imu].Eta())
                    binpt = min(xax.FindBin(leppt), xax.GetNbins())
                    yax = muIdiso.GetYaxis()
                    bineta = min(yax.FindBin(lepeta), yax.GetNbins())
                    lepsfnom*=muIdiso.GetBinContent(binpt, bineta)
                    lepsfup*=(muIdiso.GetBinContent(binpt, bineta)+muIdiso.GetBinError(binpt, bineta))
                    lepsfdown*=(muIdiso.GetBinContent(binpt, bineta)-muIdiso.GetBinError(binpt, bineta))                    
                    xax = muIdFastFull.GetXaxis()
                    leppt, lepeta = max(xax.GetBinLowEdge(1)+0.000001, muonsObs["Muons"][imu].Pt()), abs(muonsObs["Muons"][imu].Eta())
                    binpt = min(xax.FindBin(leppt), xax.GetNbins())
                    yax = muIdFastFull.GetYaxis()
                    bineta = min(yax.FindBin(lepeta), yax.GetNbins())
                    lepsfnom*=muIdFastFull.GetBinContent(binpt, bineta)
                    lepsfup*=(muIdFastFull.GetBinContent(binpt, bineta)+muIdFastFull.GetBinError(binpt, bineta))
                    lepsfdown*=(muIdFastFull.GetBinContent(binpt, bineta)-muIdFastFull.GetBinError(binpt, bineta))                    
                vars["MuSfNom"][0]  = lepsfnom
                vars["MuSfUp"][0]  = lepsfup
                vars["MuSfDown"][0]  = lepsfdown                                
                print('harnassing a muon with pt', leppt, 'sf=', lepsfnom, '+/-', lepsfup-lepsfnom, '/', lepsfnom-lepsfdown)  
                            
            elif electronsObs["Electrons"].size()>1: 
                lepsfnom = 1.0
                lepsfup = 1.0
                lepsfdown = 1.0                                
                for iel in range(2):
                    xax = eleReco.GetXaxis()                
                    yax = eleReco.GetYaxis()                    
                    leppt, lepeta = max(yax.GetBinLowEdge(1)+0.000001, electronsObs["Electrons"][iel].Pt()), abs(electronsObs["Electrons"][iel].Eta())
                    binpt = min(yax.FindBin(leppt), yax.GetNbins())
                    bineta = min(xax.FindBin(lepeta), xax.GetNbins())
                    lepsfnom*=eleReco.GetBinContent(bineta, binpt)
                    lepsfup*=(eleReco.GetBinContent(bineta, binpt)+eleReco.GetBinError(bineta, binpt))
                    lepsfdown*=(eleReco.GetBinContent(bineta, binpt)-eleReco.GetBinError(bineta, binpt))                    
                    yax = eleIdiso.GetYaxis()
                    xax = eleIdiso.GetXaxis()  
                    leppt, lepeta = max(yax.GetBinLowEdge(1)+0.000001, electronsObs["Electrons"][iel].Pt()), abs(electronsObs["Electrons"][iel].Eta())                  
                    binpt = min(yax.FindBin(leppt), yax.GetNbins())
                    bineta = min(xax.FindBin(lepeta), xax.GetNbins())
                    lepsfnom*=eleIdiso.GetBinContent(bineta, binpt)
                    lepsfup*=(eleIdiso.GetBinContent(bineta, binpt)+eleIdiso.GetBinError(bineta, binpt))
                    lepsfdown*=(eleIdiso.GetBinContent(bineta, binpt)-eleIdiso.GetBinError(bineta, binpt))                                        
                    yax = eleIdFastFull.GetYaxis()
                    xax = eleIdFastFull.GetXaxis()
                    leppt, lepeta = max(yax.GetBinLowEdge(1)+0.000001, electronsObs["Electrons"][iel].Pt()), abs(electronsObs["Electrons"][iel].Eta())                                      
                    binpt = min(yax.FindBin(leppt), yax.GetNbins())
                    bineta = min(xax.FindBin(lepeta), xax.GetNbins())
                    lepsfnom*=eleIdFastFull.GetBinContent(bineta, binpt)
                    lepsfup*=(eleIdFastFull.GetBinContent(bineta, binpt)+eleIdFastFull.GetBinError(bineta, binpt))
                    lepsfdown*=(eleIdFastFull.GetBinContent(bineta, binpt)-eleIdFastFull.GetBinError(bineta, binpt))                    
                vars["ElSfNom"][0] = lepsfnom
                vars["ElSfUp"][0] = lepsfup
                vars["ElSfDown"][0] = lepsfdown                                
                print('harnassing an electron with pt', leppt, 'sf=', lepsf)              
            
        else:
            vars["FastSimWeightPR31285To36122"][0] = 1
            vars["passedMhtMet6pack"][0] = analysis_ntuples.passTrig(c, "MhtMet6pack")
            vars["passedSingleMuPack"][0] = analysis_ntuples.passTrig(c, "SingleMuon")
            vars["passesUniversalSelection"][0] = analysis_ntuples.passesUniversalSelection(c, MET, METPhi)
            vars["TrgEffNom"][0], vars["TrgEffUp"][0], vars["TrgEffDown"][0] = 1, 1, 1#SB
            vars["IsrNom"][0], vars["IsrUp"][0], vars["IsrDown"][0] = 1, 1, 1#SB
            vars["BTagNom"][0], vars["BTagUp"][0], vars["BTagDown"][0] = 1, 1, 1#SB            
            vars["PuNom"][0], vars["PuUp"][0], vars["PuDown"][0] = 1, 1, 1#SB
            vars["ElSf"][0], vars["MuSf"][0] = 1, 1#SB
            
        #print("tEvent.Fill()")
        #print("c.RunNum,", c.RunNum,"c.LumiBlockNum,", c.LumiBlockNum, "c.EvtNum", c.EvtNum)
        tEvent.Fill()

    fnew.cd()
    tEvent.Write()

    hHt.Write('hHt')
    hHtWeighted.Write('hHtWeighted')
    hHtAfterMadHt.Write('hHtAfterMadHt')
    
    if data:
        lumiSecs.Write("lumiSecs") 
    print('we are here', os.getcwd())
    print('just created', fnew.GetName())
    fnew.Close()

main()
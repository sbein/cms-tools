#!/usr/bin/env python

from ROOT import *
from glob import glob
from sys import exit
from array import array
import argparse
import sys
import os

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools"))
from lib import utils
from lib import analysis_selections

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Run TMVA.')
parser.add_argument('-i', '--input', nargs='*', help='Signal Files', required=True)
parser.add_argument('-o', '--output_file', nargs=1, help='Output Filename', required=True)
parser.add_argument('-bg', '--bg', nargs='*', help='Input Background Files', required=True)
parser.add_argument('-nn', '--no_norm', dest='no_norm', help='No renormalization of weights', action='store_true')
parser.add_argument('-all', '--all', dest='all', help='All methods', action='store_true')
parser.add_argument('-lep', '--lep', nargs=1, help='lepton', required=True)
args = parser.parse_args()

input_files = args.input
bg_files = args.bg

output_file_name = None
if args.output_file:
    output_file_name = args.output_file[0]
else:
    output_file_name = "tmva_output.root"

no_norm = args.no_norm
all = args.all
lep = args.lep[0]


print("No norm=" + str(no_norm))
print("All=" + str(all))
print("Lep=" + lep)

######## END OF CMDLINE ARGUMENTS ########

dir = os.path.dirname(output_file_name)
print("Changing directory to", dir)
os.chdir(dir)

#output_file_name_object = os.path.splitext(output_file_name)[0] + "Object.root"


gROOT.SetBatch(1)
TMVA.Tools.Instance()
outputFile = TFile(output_file_name,'RECREATE')
#outputFileObject = TFile(output_file_name_object,'RECREATE')
factory = TMVA.Factory("TMVAClassification", outputFile,
                            ":".join([
                                "!V",
                                "!Silent",
                                "Color",
                                "DrawProgressBar",
                                "Transformations=I;D;P;G,D",
                                "AnalysisType=Classification"]
                                     ))

dataloaders = {}

#for lep in ["Electrons", "Muons"]:
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
                if iso + cuts + cat != analysis_selections.jetIsos[lep]:
                    continue
                dataloaders[lep + iso + cuts + cat] = TMVA.DataLoader("dataset")
                
bgFiles = []
bTrees = []
sFiles = []
sTrees = []

for input_file in input_files:
    print("Opening File " + input_file)
    fsignal = TFile(input_file)
    sFiles.append(fsignal)
    #for lep in ["Electrons", "Muons"]:
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
                    #print("Checking " + iso + cuts + cat)
                    if iso + cuts + cat != analysis_selections.jetIsos[lep]:
                        continue
                    sTree = fsignal.Get(lep + iso + cuts + cat)
                    if sTree.GetEntries() == 0:
                        print("Emtpy. Skipping")
                        continue
                    sTrees.append(sTree)
                    dataloaders[lep + iso + cuts + cat].AddSignalTree(sTree, 1)
                    
for bg_file in bg_files:
    if "QCD" in bg_file:
        print("Skipping QCD", bg_file)
        #exit(0)
        continue
    fbackground = TFile(bg_file)
    bgFiles.append(fbackground)
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
                    #for lep in ["Electrons", "Muons"]:
                    if iso + cuts + cat != analysis_selections.jetIsos[lep]:
                        continue
                    bTree = fbackground.Get(iso + cuts + cat)
                    if bTree.GetEntries() == 0:
                        print("Emtpy. Skipping")
                        continue
                    if len(bTrees) == 0 or bTree != bTrees[-1]:
                        bTrees.append(bTree)
                    #for lep in ["Electrons", "Muons"]:
                    dataloaders[lep + iso + cuts + cat].AddBackgroundTree(bTree, 1)

# cuts defining the signal and background sample
preselectionCut = TCut("")
preselectionLeptonCut = TCut("deltaEtaLL > -1")

#for lep in ["Electrons", "Muons"]:
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
                if iso + cuts + cat != analysis_selections.jetIsos[lep]:
                        continue
                postfix = iso + cuts + cat
                dataloader = dataloaders[lep + postfix]
            
                # Variables
                dataloader.AddVariable('abs(track.Eta())', 'F')
                
                #dataloader.AddVariable('track.Phi()', 'F')
                #dataloader.AddVariable('log(dxyVtx)', 'F')
                #dataloader.AddVariable('log(dzVtx)', 'F')
                #dataloader.AddVariable('log(trkMiniRelIso)', 'F')
                #dataloader.AddVariable('log(trkRelIso)', 'F')
            
                dataloader.AddVariable('deltaEtaLJ', 'F')
                dataloader.AddVariable('deltaRLJ', 'F')

                ## FULL
                dataloader.AddVariable('deltaEtaLL', 'F')
                dataloader.AddVariable('abs(deltaPhiLL)', 'F')
                
                dataloader.AddVariable('deltaRLL', 'F')
                
                #dataloader.AddVariable('deltaRMet', 'F')
                dataloader.AddVariable('deltaPhiMht', 'F')
                dataloader.AddVariable('abs(lepton.Eta())', 'F')
                #dataloader.AddVariable('lepton.Phi()', 'F')
                dataloader.AddVariable('lepton.Pt()', 'F')
                dataloader.AddVariable('invMass', 'F')

                #no significance
                #dataloader.AddVariable('track.Pt()', 'F')
                #dataloader.AddVariable('mtt', 'F')
                if no_norm:
                    dataloader.PrepareTrainingAndTestTree(preselectionLeptonCut, "SplitMode=random:!V:NormMode=None")
                else:
                    dataloader.PrepareTrainingAndTestTree(preselectionLeptonCut, "SplitMode=random:!V")
                factory.BookMethod(dataloader, TMVA.Types.kBDT, lep + postfix, "NTrees=200:MaxDepth=3")
#factory.BookMethod(dataloader, TMVA.Types.kBDT, "BDT2","NTrees=2000:nEventsMin=2000:MaxDepth=4:BoostType=AdaBoost:AdaBoostBeta=0.6:UseRandomisedTrees=True:UseNVars=6:nCuts=2000:PruneMethod=CostComplexity:PruneStrength=-1")
#if all:
#    factory.BookMethod(dataloader, TMVA.Types.kMLP, "MLP", "H:!V:NeuronType=tanh:VarTransform=N:NCycles=600:HiddenLayers=N+5:TestRate=5:!UseRegulator" )
#factory.BookMethod(dataloader, TMVA.Types.kMLP, "MLP_ANN", "" );
factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()
outputFile.Close()







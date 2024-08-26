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

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Run TMVA.')
parser.add_argument('-i', '--input', nargs='*', help='Signal Files', required=True)
parser.add_argument('-o', '--output_file', nargs=1, help='Output Filename', required=True)
parser.add_argument('-bg', '--bg', nargs=1, help='Input Background Directory', required=False)
parser.add_argument('-nn', '--no_norm', dest='no_norm', help='No renormalization of weights', action='store_true')
parser.add_argument('-all', '--all', dest='all', help='All methods', action='store_true')
args = parser.parse_args()

input_files = args.input

output_file_name = None
if args.output_file:
    output_file_name = args.output_file[0]
else:
    output_file_name = "tmva_output.root"
bg_dir = None
if args.bg:
    bg_dir = args.bg[0]

no_norm = args.no_norm
all = args.all

print("No norm=" + str(no_norm))
print("All=" + str(all))

tmp_dir = "/afs/desy.de/user/n/nissanuv/nfs/tmp/"

lepNum = "reco"
lep = "Muons"
iso = "CorrJetIso"
ptRange = 15
cat = "LowPtTight"

######## END OF CMDLINE ARGUMENTS ########

dir = os.path.dirname(output_file_name)
print("Changing directory to", dir)
os.chdir(dir)

gROOT.SetBatch(1)
TMVA.Tools.Instance()
outputFile = TFile(output_file_name,'RECREATE')
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
preselections = {}

bgFiles = []
bTrees = []
sFiles = []
sTrees = []

newFiles = []
newTrees = []

foundCategory = {}

totalEvents = 0
weights = 0

bg_files = glob(bg_dir + "/*")
print(bg_files)

for input_file in input_files:
    print("Opening File " + input_file)
    fsignal = TFile(input_file)
    sFiles.append(fsignal)
    sTree = fsignal.Get("tEvent")
    if sTree.GetEntries() == 0:
        print("Emtpy. Skipping")
        continue
    #for lepNum in ["reco", "exTrack"]:
        #for lep in ["Electrons", "Muons"]:
            #for iso in utils.leptonIsolationList:
                #for cat in utils.leptonIsolationCategories:
                    #ptRanges = [""]
                    #if iso == "CorrJetIso":
                    #    ptRanges = utils.leptonCorrJetIsoPtRange
                    #for ptRange in ptRanges:
    if dataloaders.get(lepNum + lep + iso + str(ptRange) + cat) is None:
        dataloaders[lepNum + lep + iso + str(ptRange) + cat] = TMVA.DataLoader("dataset")
    print("Getting", iso + str(ptRange) + cat)
    preselection = None
    
    if lepNum == "reco":
        preselection = "twoLeptons" + iso + str(ptRange) + cat + " == 1 && BTagsDeepMedium == 0 && leptonFlavour" + iso + str(ptRange) + cat  + " == \"" + lep + "\""
    else:
        preselection = "exclusiveTrack" + iso + str(ptRange) + cat + ' == 1 && BTagsDeepMedium == 0 && exclusiveTrackLeptonFlavour' + iso + str(ptRange) + cat  + " == \"" + lep + "\""
    print("Copying tree", input_file, "with", preselection)
    newFile = TFile(tmp_dir + "signal_" + lepNum + lep + iso + str(ptRange) + cat + ".root", "recreate")
    newTree = sTree.CopyTree(preselection)
    print("Done copying.")
    if newTree.GetEntriesFast() == 0:
        print("Empty tree!!!!")
        newFile.Close()
    else:
        print("Entries copied", newTree.GetEntriesFast())
        newFiles.append(newFile)
        sTrees.append(sTree)
        newTrees.append(newTree)
        foundCategory[lepNum + lep + iso + str(ptRange) + cat] = True
        dataloaders[lepNum + lep + iso + str(ptRange) + cat].AddSignalTree(newTree, 1)

for bg_file in bg_files:
    if "QCD" in bg_file:
        print("Skipping QCD", bg_file)
        #exit(0)
        continue
    if len(bg_file) == 0 or bg_file.isspace():
        continue
    print("Processing", bg_file)
    
    #if "DYJetsToLL_M-50_HT-800to1200" not in bg_file:
    #    continue
    fbackground = TFile(bg_file)
    bTree = fbackground.Get("tEvent")
    bgFiles.append(fbackground)
    #for lepNum in ["reco", "exTrack"]:
        #for lep in ["Electrons", "Muons"]:
        #for lep in ["Muons"]:
        #    for iso in utils.leptonIsolationList:
        #        for cat in utils.leptonIsolationCategories:
        #            ptRanges = [""]
        #            if iso == "CorrJetIso":
        #                ptRanges = utils.leptonCorrJetIsoPtRange
        #            for ptRange in ptRanges:
    bTrees.append(bTree)

    print("Getting", iso + str(ptRange) + cat)
    preselection = None
    
    if lepNum == "reco":
        preselection = "twoLeptons" + iso + str(ptRange) + cat + " == 1 && BTagsDeepMedium == 0 && leptonFlavour" + iso + str(ptRange) + cat  + " == \"" + lep + "\""
    else:
        preselection = "exclusiveTrack" + iso + str(ptRange) + cat + ' == 1 && BTagsDeepMedium == 0 && exclusiveTrackLeptonFlavour' + iso + str(ptRange) + cat  + " == \"" + lep + "\""
    print("Copying tree", bg_file, "with", preselection)
    newFile = TFile(tmp_dir + "bg_" + lepNum + lep + iso + str(ptRange) + cat + ".root", "recreate")
    newTree = bTree.CopyTree(preselection)
    print("Done copying.")
    if newTree.GetEntriesFast() == 0:
        print("Empty tree!!!!")
        newFile.Close()
    else:
        print("Entries copied", newTree.GetEntriesFast())
        newFiles.append(newFile)
        newTrees.append(newTree)
        dataloaders[lepNum + lep + iso + str(ptRange) + cat].AddBackgroundTree(newTree, 1)


#for lepNum in ["reco", "exTrack"]:
        #for lep in ["Electrons", "Muons"]:
#        for lep in ["Muons"]:
#            for iso in utils.leptonIsolationList:
#                for cat in utils.leptonIsolationCategories:
#                    ptRanges = [""]
#                    if iso == "CorrJetIso":
#                        ptRanges = utils.leptonCorrJetIsoPtRange
#                    for ptRange in ptRanges:
                        
prefix = ""
if lepNum == "exTrack":
    prefix = "exTrack_"

dataloader = dataloaders[lepNum + lep + iso + str(ptRange) + cat]

dataloader.AddVariable(prefix + 'deltaPhi' + iso + str(ptRange) + cat, 'F')
dataloader.AddVariable(prefix + 'deltaEta' + iso + str(ptRange) + cat, 'F')
dataloader.AddVariable(prefix + 'deltaR' + iso + str(ptRange) + cat, 'F')
dataloader.AddVariable(prefix + 'pt3' + iso + str(ptRange) + cat, 'F')
dataloader.AddVariable(prefix + 'deltaEtaLeadingJetDilepton' + iso + str(ptRange) + cat, 'F')
dataloader.AddVariable(prefix + 'deltaPhiLeadingJetDilepton' + iso + str(ptRange) + cat, 'F')
dataloader.AddVariable(prefix + 'dilepHt' + iso + str(ptRange) + cat, 'F')
dataloader.AddVariable(prefix + 'invMass' + iso + str(ptRange) + cat, 'F')

dataloader.AddVariable('Ht', 'F')
dataloader.AddVariable('MinDeltaPhiMhtJets', 'F')
dataloader.AddVariable('Mht', 'F')
dataloader.AddVariable('LeadingJetPt', 'F')
dataloader.AddVariable('LeadingJet.Eta()', 'F')
dataloader.AddVariable('NJets', 'I')

preselectionCut = None

if lepNum == "reco":
    
    #preselectionCut = TCut("vetoElectronsTightID == 0 && vetoMuonsPassIso == 0 && BTagsDeepMedium == 0")
    #preselectionCut = TCut("twoLeptons" + iso + str(ptRange) + cat + ' == 1 && BTagsDeepMedium == 0 && leptonFlavour' + iso + str(ptRange) + cat  + ' == "' + lep + '"')
    preselectionCut = TCut("")
    preselections[lepNum + lep + iso + str(ptRange) + cat] = preselectionCut
    
    dataloader.AddVariable('dileptonPt' + iso + str(ptRange) + cat, 'F')
    dataloader.AddVariable('mt1' + iso + str(ptRange) + cat, 'F')
    
#                             dataloader.AddVariable('Alt$(leptons' + iso + str(ptRange) + cat + '[1].Pt(),-1)', 'F')
#                             dataloader.AddVariable('Alt$(leptons' + iso + str(ptRange) + cat + '[0].Eta(),-1)', 'F')
#                             dataloader.AddVariable('Alt$(leptons' + iso + str(ptRange) + cat + '[0].Phi(),-1)', 'F')
#                             
    dataloader.AddVariable('leptons' + iso + str(ptRange) + cat + '[0].Pt()', 'F')
    dataloader.AddVariable('leptons' + iso + str(ptRange) + cat + '[0].Eta()', 'F')
    dataloader.AddVariable('leptons' + iso + str(ptRange) + cat + '[0].Phi()', 'F')
    dataloader.AddVariable('deltaPhiMetLepton1' + iso + str(ptRange) + cat, 'F')
    dataloader.AddVariable('deltaPhiMetLepton2' + iso + str(ptRange) + cat, 'F')
else:
    
    #preselectionCut = TCut("exclusiveTrack" + iso + str(ptRange) + cat + ' == 1 && BTagsDeepMedium == 0 && exclusiveTrackLeptonFlavour' + iso + str(ptRange) + cat  + ' == "' + lep + '"')
    preselectionCut = TCut("")
    preselections[lepNum + lep + iso + str(ptRange) + cat] = preselectionCut

    #dataloader.AddVariable('dileptonPt', 'F')
    #dataloader.AddVariable('mtautau', 'F')
    #dataloader.AddVariable('mtt', 'F')
    dataloader.AddVariable('mtl' + iso + str(ptRange) + cat, 'F')
    dataloader.AddVariable('lepton' + iso + str(ptRange) + cat + '.Pt()', 'F')
    #dataloader.AddVariable('track.Pt()', 'F')
    dataloader.AddVariable('lepton' + iso + str(ptRange) + cat + '.Eta()', 'F')
    dataloader.AddVariable('track' + iso + str(ptRange) + cat + '.Eta()', 'F')
    dataloader.AddVariable('lepton' + iso + str(ptRange) + cat + '.Phi()', 'F')
    dataloader.AddVariable('track' + iso + str(ptRange) + cat + '.Phi()', 'F')
    dataloader.AddVariable('Mt2', 'F')

#new removal
#dataloader.AddVariable('mtautau', 'F')
#dataloader.AddVariable('Mt2', 'F')
#dataloader.AddVariable('mt2', 'F')
#dataloader.AddVariable('LeadingJetQgLikelihood', 'F')
#dataloader.AddVariable('leptons[1].Phi()', 'F')
#dataloader.AddVariable('leptons[1].Eta()', 'F')
#dataloader.AddVariable('MaxCsv25', 'F')

# Spectators
dataloader.AddSpectator('Weight','F')
if no_norm:
    dataloader.PrepareTrainingAndTestTree(preselectionCut, "SplitMode=random:!V:NormMode=None")
else:
    dataloader.PrepareTrainingAndTestTree(preselectionCut, "SplitMode=random:!V")
factory.BookMethod(dataloader, TMVA.Types.kBDT, lepNum + lep + iso + str(ptRange) + cat, "NTrees=120:MaxDepth=3")

factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()
outputFile.Close()




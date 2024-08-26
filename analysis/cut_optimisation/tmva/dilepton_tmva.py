#!/usr/bin/env python

from ROOT import *
from glob import glob
from sys import exit
from array import array
import argparse
import sys
import os
from tempfile import mkdtemp
import shutil

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools"))
from lib import utils
from lib import analysis_observables
from lib import analysis_selections

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Run TMVA.')
parser.add_argument('-i', '--input', nargs='*', help='Signal Files', required=True)
parser.add_argument('-o', '--output_file', nargs=1, help='Output Filename', required=True)
parser.add_argument('-bg', '--bg', nargs=1, help='Input Background Directory', required=False)
parser.add_argument('-nn', '--no_norm', dest='no_norm', help='No renormalization of weights', action='store_true')
parser.add_argument('-all', '--all', dest='all', help='All methods', action='store_true')

parser.add_argument('-lepNum', '--lepNum', nargs=1, help='lepNum', required=True)
parser.add_argument('-lep', '--lep', nargs=1, help='lep', required=True)
parser.add_argument('-iso', '--iso', nargs=1, help='iso', required=True)
parser.add_argument('-ptRange', '--ptRange', nargs='?', help='ptRange', const="", required=False)
parser.add_argument('-cat', '--cat', nargs='?', help='cat', const="", required=False)
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

lepNum = args.lepNum[0]
lep = args.lep[0]
iso = args.iso[0]
if args.ptRange:
    ptRange = args.ptRange
else:
    ptRange = ""
if args.cat:
    cat = args.cat
else:
    cat = ""

print("lepNum", lepNum, "lep", lep, "iso", iso, "ptRange", ptRange, "cat", cat)

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

#bgFiles = []
bTrees = []
#sFiles = []
sTrees = []

newFiles = []
newTrees = []

foundCategory = {}

totalEvents = 0
weights = 0

bg_files = glob(bg_dir + "/*")
print(bg_files)

prefix = ""
if lepNum == "exTrack":
    prefix = "exTrack_"


variablesUsed = []

variablesUsed.append("BTagsDeepMedium")
variablesUsed.append("MinDeltaPhiMhtJets")
variablesUsed.append("Weight")

variablesUsed.append(prefix + 'deltaPhi' + iso + str(ptRange) + cat)
variablesUsed.append(prefix + 'deltaEta' + iso + str(ptRange) + cat)
variablesUsed.append(prefix + 'deltaR' + iso + str(ptRange) + cat)
variablesUsed.append(prefix + 'dilepHt' + iso + str(ptRange) + cat)
variablesUsed.append(prefix + 'invMass' + iso + str(ptRange) + cat)

for obs in analysis_observables.dileptonBDTeventObservables:
    if "LeadingJet." in obs:
        variablesUsed.append("LeadingJet")
    else:
        variablesUsed.append(obs)

preselection = None

if lepNum == "reco":
    #preselection = "twoLeptons" + iso + str(ptRange) + cat + " == 1 && BTagsDeepMedium == 0 && MinDeltaPhiMhtJets > 0.4 && @leptons" + iso + str(ptRange) + cat + ".size() == 2 && leptonFlavour" + iso + str(ptRange) + cat  + " == \"" + lep + "\"" + " && sameSign" + iso + str(ptRange) + cat + " == 0" + " && isoCr" + iso + str(ptRange) + cat + " == 0"
    #preselection = "twoLeptons" + iso + str(ptRange) + cat + " == 1 && BTagsDeepMedium == 0 && MinDeltaPhiMhtJets > 0.4 && leptonFlavour" + iso + str(ptRange) + cat  + " == \"" + lep + "\"" + " && sameSign" + iso + str(ptRange) + cat + " == 0" + " && isoCr" + iso + str(ptRange) + cat + " == 0"
    #Inclusive isocr
    preselection = "twoLeptons" + iso + str(ptRange) + cat + " == 1 && BTagsDeepMedium == 0 && MinDeltaPhiMhtJets > 0.4 && leptonFlavour" + iso + str(ptRange) + cat  + " == \"" + lep + "\"" + " && sameSign" + iso + str(ptRange) + cat + " == 0"
    
    variablesUsed.append("twoLeptons" + iso + str(ptRange) + cat)
    variablesUsed.append("leptonFlavour" + iso + str(ptRange) + cat)
    variablesUsed.append("sameSign" + iso + str(ptRange) + cat)
    variablesUsed.append("isoCr" + iso + str(ptRange) + cat)
    
    variablesUsed.append('dileptonPt' + iso + str(ptRange) + cat)
    variablesUsed.append('mth1' + iso + str(ptRange) + cat)
    
    variablesUsed.append('leptons' + iso + str(ptRange) + cat)

    variablesUsed.append('deltaPhiMhtLepton1' + iso + str(ptRange) + cat)
    variablesUsed.append('deltaPhiMhtLepton2' + iso + str(ptRange) + cat)
    
    variablesUsed.append('nmtautau' + iso + str(ptRange) + cat)
    
else:
    # Before 
    #preselection = "exclusiveTrack" + iso + str(ptRange) + cat + ' == 1 && BTagsDeepMedium == 0 &&  trackBDT' + iso + str(ptRange) + cat  +    ' >= 0 && exclusiveTrackLeptonFlavour' + iso + str(ptRange) + cat  + " == \"" + lep + "\""
    # Making new version without trackBDT precut
    preselection = "exclusiveTrack" + iso + str(ptRange) + cat + ' == 1 && BTagsDeepMedium == 0 &&  trackBDT' + iso + str(ptRange) + cat  +    ' >= 0 && MinDeltaPhiMhtJets > 0.4 && exclusiveTrackLeptonFlavour' + iso + str(ptRange) + cat  + " == \"" + lep + "\""
    variablesUsed.append("exclusiveTrack" + iso + str(ptRange) + cat)
    variablesUsed.append("exclusiveTrackLeptonFlavour" + iso + str(ptRange) + cat)
    variablesUsed.append('mtl' + iso + str(ptRange) + cat)
    variablesUsed.append('lepton' + iso + str(ptRange) + cat)
    variablesUsed.append('track' + iso + str(ptRange) + cat)
    variablesUsed.append('trackBDT' + iso + str(ptRange) + cat)

print("Variables used", variablesUsed )

tmpDir = mkdtemp(prefix="nissanuv", dir="/tmp") + '/'
print("tmpDir=",tmpDir)

#if not os.path.isdir(tmpDir):
#    os.mkdir(tmpDir)

for input_file in input_files:
    print("Opening File " + input_file)
    fsignal = TFile(input_file)
    #sFiles.append(fsignal)
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
     # print("Copying tree", input_file, "with", preselection)
#     newFile = TFile(tmp_dir + "signal_" + lepNum + lep + iso + str(ptRange) + cat + ".root", "recreate")
#     newTree = sTree.CopyTree(preselection)
    
    # if newTree.GetEntriesFast() == 0:
#         print("Empty tree!!!!")
#         newFile.Close()
    #else:
    #print("Entries copied", newTree.GetEntriesFast())
    #newFiles.append(newFile)
    baseFileName = os.path.basename(input_file)
    newfile = TFile(tmpDir + baseFileName, "recreate");
    
    print("old tree has", sTree.GetEntries())
    sTree.SetBranchStatus("*",0);
    for branch in variablesUsed:
        print("Setting branch on", branch)
        sTree.SetBranchStatus(branch,1);
    #newSTree = sTree.CloneTree(0)
    print("Coping tree with preselection", preselection)
    newSTree = sTree.CopyTree(preselection)
    print("new tree has", newSTree.GetEntries())
    
    if newSTree.GetEntries() == 0:
        newfile.Close()
        sTree.Delete()
        fsignal.Close() 
        continue
    
    newfile.cd()
    newSTree.Write("tEvent");
    newfile.Close();
    
    print("Done copying.")
    #sTrees.append(newSTree)
    sTree.Delete()
    fsignal.Close() 
    
    newfile = TFile(tmpDir + baseFileName, "read");
    newFiles.append(newfile)
    sTree = newfile.Get("tEvent")
    newTrees.append(sTree)
    dataloaders[lepNum + lep + iso + str(ptRange) + cat].AddSignalTree(sTree, 1) 

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
    
    baseFileName = os.path.basename(bg_file)
    newfile = TFile(tmpDir + baseFileName, "recreate");
    
    bTree.SetBranchStatus("*",0);
    for branch in variablesUsed:
        bTree.SetBranchStatus(branch,1);
    newBTree = bTree.CopyTree(preselection)
    print("new tree has", newBTree.GetEntries())
    if newBTree.GetEntries() == 0:
        newfile.Close()
        bTree.Delete()
        fbackground.Close() 
        continue
    
    newfile.cd()
    newBTree.Write("tEvent");
    newfile.Close();
    print("Done copying.")
    bTree.Delete()
    fbackground.Close()
    
    newfile = TFile(tmpDir + baseFileName, "read")
    newFiles.append(newfile)
    bTree = newfile.Get("tEvent")
    bTrees.append(bTree)
    dataloaders[lepNum + lep + iso + str(ptRange) + cat].AddBackgroundTree(bTree, 1)

    #bgFiles.append(fbackground)
    
    
    
    
    #for lepNum in ["reco", "exTrack"]:
        #for lep in ["Electrons", "Muons"]:
        #for lep in ["Muons"]:
        #    for iso in utils.leptonIsolationList:
        #        for cat in utils.leptonIsolationCategories:
        #            ptRanges = [""]
        #            if iso == "CorrJetIso":
        #                ptRanges = utils.leptonCorrJetIsoPtRange
        #            for ptRange in ptRanges:
    #bTrees.append(newBTree)

    #print("Getting", iso + str(ptRange) + cat)
    #print("Copying tree", bg_file, "with", preselection)
    #newFile = TFile(tmp_dir + "bg_" + lepNum + lep + iso + str(ptRange) + cat + ".root", "recreate")
    #newTree = bTree.CopyTree(preselection)
    #print("Done copying.")
    #if newTree.GetEntriesFast() == 0:
    #    print("Empty tree!!!!")
    #    newFile.Close()
    #else:
    #    print("Entries copied", newTree.GetEntriesFast())
    #    newFiles.append(newFile)
    #    newTrees.append(newTree)
    


#for lepNum in ["reco", "exTrack"]:
        #for lep in ["Electrons", "Muons"]:
#        for lep in ["Muons"]:
#            for iso in utils.leptonIsolationList:
#                for cat in utils.leptonIsolationCategories:
#                    ptRanges = [""]
#                    if iso == "CorrJetIso":
#                        ptRanges = utils.leptonCorrJetIsoPtRange
#                    for ptRange in ptRanges:

dataloader = dataloaders[lepNum + lep + iso + str(ptRange) + cat]

dataloader.AddVariable(prefix + 'deltaPhi' + iso + str(ptRange) + cat, 'F')
dataloader.AddVariable(prefix + 'deltaEta' + iso + str(ptRange) + cat, 'F')
dataloader.AddVariable(prefix + 'deltaR' + iso + str(ptRange) + cat, 'F')
# REMOVE THIS
#dataloader.AddVariable(prefix + 'pt3' + iso + str(ptRange) + cat, 'F')
#dataloader.AddVariable(prefix + 'deltaEtaLeadingJetDilepton' + iso + str(ptRange) + cat, 'F')
#dataloader.AddVariable(prefix + 'deltaPhiLeadingJetDilepton' + iso + str(ptRange) + cat, 'F')
# ------------
#dataloader.AddVariable(prefix + 'dilepHt' + iso + str(ptRange) + cat, 'F')
dataloader.AddVariable(prefix + 'invMass' + iso + str(ptRange) + cat, 'F')

# moved to dileptonBDTeventObservables
# dataloader.AddVariable('HT', 'F')
# dataloader.AddVariable('MinDeltaPhiMhtJets', 'F')
# dataloader.AddVariable('MHT', 'F')
# dataloader.AddVariable('LeadingJetPt', 'F')
# dataloader.AddVariable('LeadingJet.Eta()', 'F')
# dataloader.AddVariable('NJets', 'I')

for obs in analysis_observables.dileptonBDTeventObservables:
    dataloader.AddVariable(obs, analysis_observables.dileptonBDTeventObservables[obs])
    

preselectionCut = None

if lepNum == "reco":
    
    #preselectionCut = TCut("vetoElectronsTightID == 0 && vetoMuonsPassIso == 0 && BTagsDeepMedium == 0")
    #preselectionCut = TCut("twoLeptons" + iso + str(ptRange) + cat + ' == 1 && BTagsDeepMedium == 0 && leptonFlavour' + iso + str(ptRange) + cat  + ' == "' + lep + '"')
    preselectionCut = TCut(preselection)
    preselections[lepNum + lep + iso + str(ptRange) + cat] = preselectionCut
    dataloader.AddCut(preselection)
    dataloader.AddVariable('dileptonPt' + iso + str(ptRange) + cat, 'F')
    dataloader.AddVariable('mth1' + iso + str(ptRange) + cat, 'F')
    
#                             dataloader.AddVariable('Alt$(leptons' + iso + str(ptRange) + cat + '[1].Pt(),-1)', 'F')
#                             dataloader.AddVariable('Alt$(leptons' + iso + str(ptRange) + cat + '[0].Eta(),-1)', 'F')
#                             dataloader.AddVariable('Alt$(leptons' + iso + str(ptRange) + cat + '[0].Phi(),-1)', 'F')
#                             
    dataloader.AddVariable('leptons' + iso + str(ptRange) + cat + '[0].Pt()', 'F')
    dataloader.AddVariable('leptons' + iso + str(ptRange) + cat + '[1].Pt()', 'F')
    dataloader.AddVariable('leptons' + iso + str(ptRange) + cat + '[0].Eta()', 'F')
    #dataloader.AddVariable('leptons' + iso + str(ptRange) + cat + '[0].Phi()', 'F')
    dataloader.AddVariable('deltaPhiMhtLepton1' + iso + str(ptRange) + cat, 'F')
    dataloader.AddVariable('deltaPhiMhtLepton2' + iso + str(ptRange) + cat, 'F')
    dataloader.AddVariable('nmtautau' + iso + str(ptRange) + cat, 'F')
        
else:
    
    #preselectionCut = TCut("exclusiveTrack" + iso + str(ptRange) + cat + ' == 1 && BTagsDeepMedium == 0 && exclusiveTrackLeptonFlavour' + iso + str(ptRange) + cat  + ' == "' + lep + '"')
    preselectionCut = TCut(preselection)
    preselections[lepNum + lep + iso + str(ptRange) + cat] = preselectionCut

    #dataloader.AddVariable('dileptonPt', 'F')
    #dataloader.AddVariable('mtautau', 'F')
    #dataloader.AddVariable('mtt', 'F')
    dataloader.AddVariable('mtl' + iso + str(ptRange) + cat, 'F')
    dataloader.AddVariable('lepton' + iso + str(ptRange) + cat + '.Pt()', 'F')
    #dataloader.AddVariable('track.Pt()', 'F')
    dataloader.AddVariable('lepton' + iso + str(ptRange) + cat + '.Eta()', 'F')
    dataloader.AddVariable('track' + iso + str(ptRange) + cat + '.Eta()', 'F')
    dataloader.AddVariable('track' + iso + str(ptRange) + cat + '.Pt()', 'F')
    dataloader.AddVariable('lepton' + iso + str(ptRange) + cat + '.Phi()', 'F')
    dataloader.AddVariable('track' + iso + str(ptRange) + cat + '.Phi()', 'F')
    dataloader.AddVariable('trackBDT' + iso + str(ptRange) + cat, 'F')
    #dataloader.AddVariable('Mt2', 'F')

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

print("deleting tmp dir", tmpDir)
shutil.rmtree(tmpDir)
exit(0)



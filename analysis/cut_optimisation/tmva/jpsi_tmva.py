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
parser.add_argument('-bg', '--bg', nargs='*', help='Input Background Files', required=True)
parser.add_argument('-nn', '--no_norm', dest='no_norm', help='No renormalization of weights', action='store_true')
parser.add_argument('-all', '--all', dest='all', help='All methods', action='store_true')
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

print("No norm=" + str(no_norm))
print("All=" + str(all))

	
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

dataloader = TMVA.DataLoader("dataset")
                
bgFiles = []
bTrees = []
sFiles = []
sTrees = []

for input_file in input_files:
    print("Opening File " + input_file)
    fsignal = TFile(input_file)
    sFiles.append(fsignal)
    sTree = fsignal.Get('tEvent')
    if sTree.GetEntries() == 0:
        print("Emtpy. Skipping")
        continue
    sTrees.append(sTree)
    dataloader.AddSignalTree(sTree, 1)
                    
for bg_file in bg_files:
    fbackground = TFile(bg_file)
    bgFiles.append(fbackground)
    bTree = fbackground.Get('tEvent')
    if bTree.GetEntries() == 0:
        print("Emtpy. Skipping")
        continue
    bTrees.append(bTree)
    dataloader.AddBackgroundTree(bTree, 1)

# cuts defining the signal and background sample
preselectionCut = TCut("probeTrack.Pt() < 3 && abs(probeTrack.Eta()) >= 1.2 && abs(probeTrack.Eta()) <= 2.4")

# calcDiObsDef = {
#     "invMass" : "float",
#     "dileptonPt" : "float",
#     "deltaPhi" : "float",
#     "deltaEta" : "float",
#     "deltaR" : "float",
#     "tagJpsi" : "int",
#     "probeJpsi" : "int"   
# }
# 
# tagObsDef = {
#     "Muons_tightID" : "bool",
#     "Muons_passIso" : "bool",
#     "Muons_MiniIso" : "float",
#     "Muons_MT2Activity" : "float",
#     "Muons_MTW" : "float",
# }
# 
# vecObsDef = {
#     "tagMuon" : "TLorentzVector",
#     "probeTrack" : "TLorentzVector"
# }
# 
# commonFlatObs = {
#     "RunNum" : "int",
#     "LumiBlockNum" : "int",
#     "EvtNum" : "float",
#     "MET" : "float",
#     "METPhi" : "float",
#     "MT2" : "float",
#     "HT" : "float",
#     "MHT" : "float",
#     "MHTPhi" : "float",
# }
# 
# flatObs = {}
# for flatOb in analysis_ntuples.commonFlatObs:
#     flatObs[flatOb] = np.zeros(1,dtype=eval(analysis_ntuples.commonFlatObs[flatOb]))

                
# Variables
dataloader.AddVariable('dileptonPt', 'F')

# Check two sceneraios of either/or
dataloader.AddVariable('deltaEta', 'F')
dataloader.AddVariable('deltaPhi', 'F')

dataloader.AddVariable('abs(tagMuon.Eta())', 'F')
dataloader.AddVariable('tagMuon.Phi()', 'F')
dataloader.AddVariable('tagMuon.Pt()', 'F')

#dataloader.AddVariable('Muons_tightID', 'I')
dataloader.AddVariable('Muons_passIso', 'I')
dataloader.AddVariable('Muons_MiniIso', 'F')
dataloader.AddVariable('Muons_MTW', 'F')





# dataloader.AddVariable('deltaR', 'F')
# dataloader.AddVariable('MET', 'F')
# dataloader.AddVariable('METPhi', 'F')
# dataloader.AddVariable('MT2', 'F')
# dataloader.AddVariable('HT', 'F')
# dataloader.AddVariable('MHT', 'F')
# dataloader.AddVariable('MHTPhi', 'F')


#if no_norm:
dataloader.PrepareTrainingAndTestTree(preselectionCut, "SplitMode=random:!V:NormMode=None")
#else:
#    dataloader.PrepareTrainingAndTestTree(preselectionCut, "SplitMode=random:!V")
factory.BookMethod(dataloader, TMVA.Types.kBDT, "BDT", "NTrees=200:MaxDepth=3")
#factory.BookMethod(dataloader, TMVA.Types.kBDT, "BDT2","NTrees=2000:nEventsMin=2000:MaxDepth=4:BoostType=AdaBoost:AdaBoostBeta=0.6:UseRandomisedTrees=True:UseNVars=6:nCuts=2000:PruneMethod=CostComplexity:PruneStrength=-1")
#if all:
#    factory.BookMethod(dataloader, TMVA.Types.kMLP, "MLP", "H:!V:NeuronType=tanh:VarTransform=N:NCycles=600:HiddenLayers=N+5:TestRate=5:!UseRegulator" )
#factory.BookMethod(dataloader, TMVA.Types.kMLP, "MLP_ANN", "" );
factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()
outputFile.Close()







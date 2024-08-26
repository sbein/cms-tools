#!/usr/bin/env python

from ROOT import *
from glob import glob
from sys import exit
from array import array
import argparse
import sys
import os

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Run TMVA.')
parser.add_argument('-i', '--input_file', nargs=1, help='Input Signal Filename', required=True)
parser.add_argument('-o', '--output_file', nargs=1, help='Output Filename', required=True)
parser.add_argument('-bg', '--bg', nargs=1, help='Input Background Directory', required=False)
parser.add_argument('-nn', '--no_norm', dest='no_norm', help='No renormalization of weights', action='store_true')
parser.add_argument('-all', '--all', dest='all', help='All methods', action='store_true')
args = parser.parse_args()


input_file = None
if args.input_file:
	input_file = args.input_file[0]
else:
	input_file = "/afs/desy.de/user/n/nissanuv/work/x1x2x1/signal/skim/sum/type_sum/dm20.root"
output_file_name = None
if args.output_file:
	output_file_name = args.output_file[0]
else:
	output_file_name = "tmva_output.root"
bg_dir = None
if args.bg:
	bg_dir = args.bg[0]
else:
	bg_dir = "/afs/desy.de/user/n/nissanuv/work/x1x2x1/bg/skim/sum/type_sum"
no_norm = args.no_norm
all = args.all

print("No norm=" + str(no_norm))
print("All=" + str(all))

	
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
                                     
dataloader = TMVA.DataLoader("dataset")
dataloader.SetWeightExpression("Weight")
fsignal = TFile(input_file, "update")
sTree = fsignal.Get("tEvent")
dataloader.AddSignalTree(sTree, 1);
bgFiles = []
bTrees = []
bFileNames =  glob(bg_dir + "/*");
for f in bFileNames:
    print("Adding file " + f)
    bFile = TFile(f, "update")
    bgFiles.append(bFile)
    bTree = bFile.Get("tEvent")
    bTrees.append(bTree)
    dataloader.AddBackgroundTree(bTree, 1)

# Variables
#dataloader.AddVariable('NJets', 'I')
dataloader.AddVariable('Ht', 'F')
dataloader.AddVariable('LeadingJetQgLikelihood', 'F')
dataloader.AddVariable('MinDeltaPhiMhtJets', 'F')
dataloader.AddVariable('Mht', 'F')
dataloader.AddVariable('LeadingJetPt', 'F')
dataloader.AddVariable('LeadingJet.Eta()', 'F')

# Spectators
#dataloader.AddSpectator('NL','I')

# cuts defining the signal and background sample
preselectionCut = TCut("")
if no_norm:
	dataloader.PrepareTrainingAndTestTree(preselectionCut, "SplitMode=random:!V:NormMode=None")
else:
	dataloader.PrepareTrainingAndTestTree(preselectionCut, "SplitMode=random:!V")
#
factory.BookMethod(dataloader, TMVA.Types.kBDT, "BDT", "NTrees=200:MaxDepth=4")
if all:
	factory.BookMethod(dataloader, TMVA.Types.kMLP, "MLP", "H:!V:NeuronType=tanh:VarTransform=N:NCycles=600:HiddenLayers=N+5:TestRate=5:!UseRegulator" )
#factory.BookMethod(dataloader, TMVA.Types.kMLP, "MLP_ANN", "" );
factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()
outputFile.Close()







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
#sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes"))

from lib import utils
from lib import analysis_ntuples
from lib import analysis_tools

# gSystem.Load('LumiSectMap_C')
# from ROOT import LumiSectMap
# 
# gSystem.Load('LeptonCollectionMap_C')
# from ROOT import LeptonCollectionMap
# from ROOT import LeptonCollectionFilesMap
# from ROOT import LeptonCollection

gROOT.SetBatch(1)

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Split tracks into signal and background trees.')
parser.add_argument('-i', '--input_file', nargs=1, help='Input Filename', required=True)
parser.add_argument('-o', '--output_file', nargs=1, help='Output Filename', required=False)
args = parser.parse_args()

input_file = None
output_file = None
if args.input_file:
    input_file = args.input_file[0]
if args.output_file:
    output_file = args.output_file[0]

######## END OF CMDLINE ARGUMENTS ########

def main():
    
    calcDiObsDef = {
        "invMass" : "float",
        "dileptonPt" : "float",
        "deltaPhi" : "float",
        "deltaEta" : "float",
        "deltaR" : "float",
        "tagJpsi" : "int",
        "probeJpsi" : "int"   
    }
    
    tagObsDef = {
        "Muons_tightID" : "bool",
        "Muons_passIso" : "bool",
        "Muons_MiniIso" : "float",
        "Muons_MT2Activity" : "float",
        "Muons_MTW" : "float",
    }
    
    vecObsDef = {
        "tagMuon" : "TLorentzVector",
        "probeTrack" : "TLorentzVector"
    }
    
    flatObs = {}
    for flatOb in analysis_ntuples.commonFlatObs:
        flatObs[flatOb] = np.zeros(1,dtype=eval(analysis_ntuples.commonFlatObs[flatOb]))
    
    calcDiObs = {}
    for calcDiOb in calcDiObsDef:
        calcDiObs[calcDiOb] =  np.zeros(1,dtype=eval(calcDiObsDef[calcDiOb]))
    
    tagObs = {}
    for tagOb in tagObsDef:
        tagObs[tagOb] =  np.zeros(1,dtype=eval(tagObsDef[tagOb]))
    
    vecObs = {}
    for vecOb in vecObsDef:
        vecObs[vecOb] = eval(vecObsDef[vecOb])()
    
    signalTree = TTree("sTree", "sTree")
    bgTree = TTree("bTree", "bTree")
    
    for flatOb in analysis_ntuples.commonFlatObs:
        print("tEvent.Branch(" + flatOb + "," +  "flatObs[flatOb]" + "," + flatOb + "/" + utils.typeTranslation[analysis_ntuples.commonFlatObs[flatOb]] + ")")
        signalTree.Branch(flatOb, flatObs[flatOb],flatOb + "/" + utils.typeTranslation[analysis_ntuples.commonFlatObs[flatOb]])
        bgTree.Branch(flatOb, flatObs[flatOb],flatOb + "/" + utils.typeTranslation[analysis_ntuples.commonFlatObs[flatOb]])
    
    for calcDiOb in calcDiObsDef:
        print(calcDiOb, calcDiObs[calcDiOb],calcDiOb + "/" + utils.typeTranslation[calcDiObsDef[calcDiOb]])
        signalTree.Branch(calcDiOb, calcDiObs[calcDiOb],calcDiOb + "/" + utils.typeTranslation[calcDiObsDef[calcDiOb]])
        bgTree.Branch(calcDiOb, calcDiObs[calcDiOb],calcDiOb + "/" + utils.typeTranslation[calcDiObsDef[calcDiOb]])
        
    for tagOb in tagObsDef:
        signalTree.Branch(tagOb, tagObs[tagOb],tagOb + "/" + utils.typeTranslation[tagObsDef[tagOb]])
        bgTree.Branch(tagOb, tagObs[tagOb],tagOb + "/" + utils.typeTranslation[tagObsDef[tagOb]])
    
    for vecOb in vecObsDef:
        signalTree.Branch(vecOb, vecObsDef[vecOb], vecObs[vecOb]) 
        bgTree.Branch(vecOb, vecObsDef[vecOb], vecObs[vecOb]) 
    

    c = TChain('tEvent')
    print("Going to open the file")
    print(input_file)
    c.Add(input_file)

    nentries = c.GetEntries()
    print('Analysing', nentries, "entries")
    for ientry in range(nentries):
        if ientry % 5000 == 0:
            print("Processing " + str(ientry))
        c.GetEntry(ientry)
        
        for flatOb in flatObs:
            flatObs[flatOb][0] = getattr(c, flatOb)
        
        for i in range(c.invMass.size()):
        
            for calcDiOb in calcDiObsDef:
                calcDiObs[calcDiOb][0] = (getattr(c, calcDiOb))[i]
#                 
#                 if c.tagJpsi[i] > 0 or c.probeJpsi[i] > 0:
#                     print(calcDiOb, (getattr(c, calcDiOb))[i], calcDiObs[calcDiOb][0])
        
            tagMuonIdx = c.tagMuon[i]
            probeTrackIdx = c.probeTrack[i]
        
            for tagOb in tagObsDef:
                tagObs[tagOb][0] = (getattr(c, tagOb))[tagMuonIdx]
            
            vecObs["tagMuon"] = c.Muons[tagMuonIdx]
            vecObs["probeTrack"] = c.tracks[probeTrackIdx]
            
            tree = bgTree
                
            if c.tagJpsi[i] > 0 or c.probeJpsi[i] > 0:
                tree = signalTree
            
            
            for vecOb in vecObsDef:
            #print("tEvent.SetBranchAddress(" + calcDiOb + ", " + str(calcDiObs[calcDiOb]) + ")")
                tree.SetBranchAddress(vecOb, vecObs[vecOb])
            
            #bla[0] = 5
        
            tree.Fill()
        
        

    fnew = TFile(output_file + "_sig.root",'recreate')
    signalTree.Write("tEvent")
    fnew.Close()

    fnew = TFile(output_file + "_bg.root",'recreate')
    bgTree.Write("tEvent")
    fnew.Close()
    
    print("Done writing")
        
main()
exit(0)




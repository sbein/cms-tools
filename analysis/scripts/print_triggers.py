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
args = parser.parse_args()

print(args)

input_file = None
if args.input_file:
    input_file = args.input_file[0].strip()

######## END OF CMDLINE ARGUMENTS ########

def main():
    
    import os
    from lib import utils
    
    c = TChain('TreeMaker2/PreSelection')
    print("Opening", input_file)
    c.Add(input_file)
    
    nentries = c.GetEntries()
    print('Analysing', nentries, "entries")
    
    TriggerNamesMap = {}
    TriggerPassMap = {}
    TriggerPrescalesMap = {}
    TriggerVersionMap = {}

    for ientry in range(nentries):
        if ientry % 1000 == 0:
            print("Processing " + str(ientry))
        c.GetEntry(ientry)
        
        TriggerNames = c.TriggerNames
        TriggerPass = c.TriggerPass
        TriggerPrescales = c.TriggerPrescales
        TriggerVersion = c.TriggerVersion
        
        for i in range(TriggerNames.size()):
            if TriggerPass[i] != 1 and TriggerPass[i] != 0 and TriggerPass[i] != -1:
                print("WHAT?", TriggerPass[i])
            # if TriggerPass[i] == 0:
#                 print("0!!!")
#             if TriggerPass[i] == -1:
#                 print("-1!!!")
            
            if TriggerNames[i] in TriggerNamesMap and  TriggerNamesMap[TriggerNames[i]] != i:
                print("CRAZY!!!?", TriggerNames[i], i, TriggerNamesMap[TriggerNames[i]])
            
            if ientry == 0 or (ientry != 0 and TriggerNames[i] not in TriggerNamesMap):
                #print("Adding unseen TriggerName", TriggerNames[i])
                TriggerNamesMap[TriggerNames[i]] = i
            
            if TriggerPass[i] != 1:
                continue
        
            if ientry == 0 or (ientry != 0 and TriggerPass[i] not in TriggerPassMap):
                #print("Adding unseen TriggerPass", TriggerPass[i])
                #TriggerPassMap[TriggerNames[i]] = i
                TriggerPassMap[i] = TriggerNames[i]
        
            if ientry == 0 or (ientry != 0 and TriggerPrescales[i] not in TriggerPrescalesMap):
                #print("Adding unseen TriggerPrescales", TriggerPrescales[i])
                TriggerPrescalesMap[TriggerPrescales[i]] = i
        
            if ientry == 0 or (ientry != 0 and TriggerVersion[i] not in TriggerVersionMap):
                #print("Adding unseen TriggerVersion", TriggerVersion[i])
                TriggerVersionMap[TriggerVersion[i]] = i
        
    print("======================")
    print("TriggerNames:")
    print(TriggerNamesMap)
    print("TriggerPass")
    print(TriggerPassMap)
    print("TriggerPrescales")
    print(TriggerPrescalesMap)
    print("TriggerVersion")
    print(TriggerVersionMap)
    
    for k,v in sorted(TriggerPassMap.items()):
        print(k, v)
        
        #TriggerNames    = (vector<string>*)0x4294930
        #TriggerPass     = (vector<int>*)0x2ac1050
        #TriggerPrescales = (vector<int>*)0x6f69d50
        #TriggerVersion  = (vector<int>*)0x6f79ec0

main()

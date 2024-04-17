#!/usr/bin/env python3.8

from ROOT import *
from glob import glob
import sys
import os
import time

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes"))
import utils

gROOT.SetBatch(True)
gStyle.SetOptStat(0)

gSystem.Load('LumiSectMap_C')
from ROOT import LumiSectMap

####### CMDLINE ARGUMENTS #########

lumiSecs = LumiSectMap()

#data_files = glob("/pnfs/desy.de/cms/tier2/store/user/*/NtupleHub/ProductionRun2v*/Run2016B*MET*")
#data_files = glob("/afs/desy.de/user/n/nissanuv/ntupleHub/SlimmedProduction/Run201[78]*MET*")
#data_files = glob("/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/tmp/*")
#data_files = glob("/afs/desy.de/user/n/nissanuv/ntupleHub/SlimmedProduction/Run2018D*MET*")

#glob_str = "/pnfs/desy.de/cms/tier2/store/user/*/NtupleHub/ProductionRun2v3*/Run2018*MET*"



#print "glob_str", glob_str

#data_files = glob(glob_str)

#f = "/afs/desy.de/user/n/nissanuv/ntupleHub/SlimmedProduction/Run2017C-31Mar2018-v1.MET_445FC981-2B38-E811-826D-AC1F6B1AF080.root"
#print(os.path.getctime(f))
#print(os.path.getmtime(f))

#tstruct = time.localtime(os.path.getctime(f))
#print(tstruct)
#print(f, tstruct.tm_year)
#exit(0)

#data_files = glob("/afs/desy.de/user/n/nissanuv/ntupleHub/SlimmedProduction/Run201[678]*MET*")
data_files = glob("/afs/desy.de/user/n/nissanuv/ntupleHub/SlimmedProduction/Run2017*MET*")

print(len(data_files), "Files")
i=0
    
for f in data_files:
    i+=1
    
    
    #tstruct = time.localtime(os.path.getmtime(f))
    
    
    #if tstruct.tm_year != 2024:
    #    continue
    print(f)
    
    
    #continue

    print("***")
    print(i, "/", len(data_files))
    print("***")
    c = TChain('TreeMaker2/PreSelection')
    #c = TChain('tEvent')
    c.Add(f)
    
    nentries = c.GetEntries()
    print('Analysing', nentries, "entries")
    
    for ientry in range(nentries):
        if ientry % 10000 == 0:
            print("Processing " + str(ientry))
        c.GetEntry(ientry)
        lumiSecs.insert(c.RunNum, c.LumiBlockNum)

lumi = utils.calculateLumiFromLumiSecs(lumiSecs)
print("Luminosity=", lumi)
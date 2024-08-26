#!/usr/bin/env python3

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
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes"))
from lib import histograms
from lib import utils
from lib import cuts
from lib import analysis_ntuples
from lib import analysis_tools

gSystem.Load('LumiSectMap_C')
from ROOT import LumiSectMap

####### CMDLINE ARGUMENTS #########



######## END OF CMDLINE ARGUMENTS ########


files = glob("/pnfs/desy.de/cms/tier2/store/user/ynissan/NtupleHub/SignalNtuples/*")

for f in files:
    output_file = os.path.splitext(os.path.basename(f))[0]
    
    if len(glob("/pnfs/desy.de/cms/tier2/store/user/ynissan/NtupleHub/SignalNtuplesSplit/" + output_file + "*")) > 0:
        print(f, "already existing...")
        continue
    
    chain = TChain('TreeMaker2/PreSelection')
    print("Going to open the file")
    print(f)
    chain.Add(f)
    print("After opening")
    tree = chain.CloneTree(0)

    nentries = chain.GetEntriesFast()
    print('Analysing', nentries, "entries")

    max_per_file = 60000
    filenum = 1
    
    fnewFileName = output_file + "_" + str(filenum) + ".root"
    fnew = TFile("/tmp/" + fnewFileName,'recreate')
    fnew.mkdir("TreeMaker2");
    fnew.cd("TreeMaker2")
    new_entries = False

    for ientry in range(nentries):
        if ientry % 5000 == 0:
            print("Processing " + str(ientry))
        if ientry != 0 and ientry % max_per_file == 0:
            print("Done copying. Writing to file")
            tree.Write('PreSelection')
            print("Done writing to file.")
            tree.Reset()
            fnew.Close()
            
            os.system("gfal-copy " + "/tmp/" + fnewFileName + " srm://dcache-se-cms.desy.de/pnfs/desy.de/cms/tier2/store/user/ynissan/NtupleHub/SignalNtuplesSplit/")
            os.remove("/tmp/" + fnewFileName)
            
            filenum +=1
            fnewFileName = output_file + "_" + str(filenum) + ".root"
            fnew = TFile("/tmp/" + fnewFileName,'recreate')
            fnew.mkdir("TreeMaker2");
            fnew.cd("TreeMaker2")
            new_entries = False
        chain.GetEntry(ientry)
        tree.Fill()
        new_entries = True

    if new_entries:
        print("Done copying. Writing to file")
        tree.Write('PreSelection')
        print("Done writing to file.")
        tree.Reset()
        fnew.Close()
        os.system("gfal-copy " + "/tmp/" + fnewFileName + " srm://dcache-se-cms.desy.de/pnfs/desy.de/cms/tier2/store/user/ynissan/NtupleHub/SignalNtuplesSplit/")
        os.remove("/tmp/" + fnewFileName)



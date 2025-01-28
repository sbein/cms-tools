#!/usr/bin/env python3

from ROOT import *
from glob import glob
from sys import exit
import numpy as np
import argparse
import sys
import os

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes"))
from lib import utils

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Weight skims for x1x2x1 process.')
parser.add_argument('-i', '--input_dir', nargs=1, help='Input Directory', required=True)
parser.add_argument('-f', '--Force', dest='force', help='Force Update', action='store_true')
args = parser.parse_args()

input_dir = args.input_dir[0]
force = args.force
######## END OF CMDLINE ARGUMENTS ########

def main():
    
    triggerFileName = os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/susy-trig-plots.root")
    print("Opening trigger file: " + triggerFileName)
    
    triggerFile = TFile(triggerFileName, "read")
    tEffhMetMhtRealXMet2016 = triggerFile.Get('tEffhMetMhtRealXMet;1')
    tEffhMetMhtRealXMet2017 = triggerFile.Get('tEffhMetMhtRealXMet;2')
    tEffhMetMhtRealXMet2018 = triggerFile.Get('tEffhMetMhtRealXMet;3')
    
    tEffhMetMhtRealXMht2016 = triggerFile.Get('tEffhMetMhtRealXMht;1')
    tEffhMetMhtRealXMht2017 = triggerFile.Get('tEffhMetMhtRealXMht;2')
    tEffhMetMhtRealXMht2018 = triggerFile.Get('tEffhMetMhtRealXMht;3')
    
    tEffhMetMhtRealXMet2016 = triggerFile.Get('tEffhMetMhtRealXMet;1')
    tEffhMetMhtRealXMet2017 = triggerFile.Get('tEffhMetMhtRealXMet;2')
    tEffhMetMhtRealXMet2018 = triggerFile.Get('tEffhMetMhtRealXMet;3')
    
    tEffhMetMhtRealXMht2016 = triggerFile.Get('tEffhMetMhtRealXMht;1')
    tEffhMetMhtRealXMht2017 = triggerFile.Get('tEffhMetMhtRealXMht;2')
    tEffhMetMhtRealXMht2018 = triggerFile.Get('tEffhMetMhtRealXMht;3')
    
    var_EffhMetMhtRealXMht2016 = np.zeros(1,dtype=float)
    
    fileList = glob(input_dir + "/*");
    for f in fileList:
        if os.path.isdir(f): continue
        print("processing file " + f )
        f = TFile(f, "update")
        t = f.Get("tEvent")
        
        if t.GetBranchStatus("tEffhMetMhtRealXMet2016"):
            if not force:
                print("This tree already has efficiencies! Skipping...")
                f.Close()
                continue
        
        t.GetEntry(0)
        
        var_Weight = np.zeros(1,dtype=float)
        var_Weight[0] = weight
        nentries = t.GetEntries();
        if t.GetBranchStatus("Weight"):
            if not force:
                print("This tree is already weighted! Skipping...")
            else:
                branch = t.GetBranch("Weight")
                branch.Reset()
                branch.SetAddress(var_Weight)
                for ientry in range(nentries):
                    branch.Fill()
                t.Write("tEvent",TObject.kOverwrite)
                print("Done")
            f.Close()
            continue
    
        newBranch = t.Branch("Weight",var_Weight,"Weight/D");
        for ientry in range(nentries):
            newBranch.Fill()
        print("Writing Tree")
        t.Write("tEvent",TObject.kOverwrite)
        print("Done")
        f.Close()

main()
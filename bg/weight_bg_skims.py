#!/usr/bin/env python3

from ROOT import *
from glob import glob
from sys import exit
import argparse
import sys
import numpy as np
import os
import cppyy
import itertools
from datetime import datetime

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes"))
from lib import analysis_ntuples
from lib import analysis_tools
from lib import utils
from lib import analysis_observables

parser = argparse.ArgumentParser(description='Sum bg files.')
parser.add_argument('-f', '--force', dest='force', help='Force Update', action='store_true')
parser.add_argument('-phase1', '--phase1', dest='phase1', help='Force Update', action='store_true')
args = parser.parse_args()

force = args.force
phase1 = args.phase1

bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/type_sum"
if phase1:
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_phase1/sum/type_sum"

def main():
    sumTypes = {}
    
    fileList = glob(bg_dir + "/*");
    
    for fileName in fileList:
        print("Summing", os.path.basename(fileName))
        bg_type = "_".join(os.path.basename(fileName).split("_")[0:-1])
        if bg_type not in sumTypes:
            sumTypes[bg_type] = 0
        f = TFile(fileName, "read")
        h = f.Get("hHt")
        sumTypes[bg_type] += h.Integral(-1,99999999)
        f.Close()

    print(sumTypes)
    
    for fileName in fileList:
        print("Summing", os.path.basename(fileName))
        bg_type = "_".join(os.path.basename(fileName).split("_")[0:-1])
        f = TFile(fileName, "update")
        t = f.Get("tEvent")
        t.GetEntry(0)
        numOfEvents = sumTypes[bg_type]
        print("numOfEvents:", numOfEvents)
        cs = t.CrossSection
        print("CrossSection:", cs)
        weight = cs/numOfEvents
        print("weight:", weight)

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
exit(0)

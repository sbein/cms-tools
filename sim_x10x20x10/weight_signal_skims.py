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

parser = argparse.ArgumentParser(description='Sum signal files.')
parser.add_argument('-f', '--force', dest='force', help='Force Update', action='store_true')
parser.add_argument('-sam', '--sam', dest='sam', help='Sam Skims', action='store_true')
parser.add_argument('-nlp', '--nlp', dest='nlp', help='No Lepton Selection', action='store_true')
parser.add_argument('-phase1', '--phase1', dest='phase1', help='Phase 1', action='store_true')
args = parser.parse_args()

force = args.force
sam = args.sam
nlp = args.nlp
phase1 = args.phase1

signal_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/single"

if nlp:
    signal_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_nlp/sum"
elif phase1:
    signal_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_phase1/single"

def main():
    points = {}
    
    fileList = glob(signal_dir + "/*");

    for fileName in fileList:
        point = None
        if sam:
            point = "_".join(os.path.basename(fileName).split("_")[2:4])
        else:
            point = "_".join(os.path.basename(fileName).split("_")[0:3])
        if points.get(point) is None:
            points[point] = 0
        
        f = TFile(fileName, "read")
        print("Summing", os.path.basename(fileName))
        h = f.Get("hHt")
        points[point] += h.Integral(-1,99999999)
        f.Close()
        
    print("\n\n\n")
    print(points)
    print("\n\n\n")
    
    for fileName in fileList:
        print("Weighting", os.path.basename(fileName))
        point = None
        if sam:
            point = "_".join(os.path.basename(fileName).split("_")[2:4])
        else:
            point = "_".join(os.path.basename(fileName).split("_")[0:3])
        f = TFile(fileName, "update")
        t = f.Get("tEvent")
        t.GetEntry(0)
        numOfEvents = points[point]
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

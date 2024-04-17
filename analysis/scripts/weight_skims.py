#!/usr/bin/env python

from ROOT import *
from glob import glob
from sys import exit
import numpy as np
import argparse
import sys
import os
import time

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes"))
from lib import utils

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Weight skims for x1x2x1 process.')
parser.add_argument('-i', '--input_dir', nargs=1, help='Input Directory', required=True)
parser.add_argument('-f', '--force', dest='force', help='Force Update', action='store_true')
parser.add_argument('-data', '--data', dest='data', help='data', action='store_true')
parser.add_argument('-sam', '--sam', dest='sam', help='Sam Samples', action='store_true')
parser.add_argument('-phase1', '--phase1', dest='phase1', help='Sam Samples', action='store_true')
parser.add_argument('-jecup', '--jecup', dest='jecup', help='jec-up variation', action='store_true')
parser.add_argument('-jecdown', '--jecdown', dest='jecdown', help='jec-down variation', action='store_true')
args = parser.parse_args()

input_dir = args.input_dir[0]
force = args.force
sam = args.sam
data = args.data
phase1 = args.phase1
jecup = args.jecup; jecdown = args.jecdown
######## END OF CMDLINE ARGUMENTS ########

if jecup: thing2grab = 'JecUp'
elif jecdown: thing2grab = 'JecDown'
else: 
    if phase1: thing2grab = '1.roo'
    else: thing2grab = 'Tree.roo'

fileList = glob(input_dir + "/*"+thing2grab+"*");
print('fileList', input_dir + "/*"+thing2grab+"*", len(fileList))
for filename in fileList:
    if os.path.isdir(filename): continue
    #tstruct = time.localtime(os.path.getmtime(filename))
    #if tstruct.tm_year != 2024:
    #    print "old file... skipping... " + filename
    #    continue
    print "processing file " + filename
    f = TFile(filename, "update")
    numOfEvents = 0
    if sam and (not phase1):
        point = "_".join(os.path.basename(filename).split("_")[2:4])
        point_files = glob(input_dir + "/*" + point + "*"+thing2grab+"*")
        print "point", point, "has", len(point_files), "files"
        numOfEvents = 20000 * len(point_files)
    else:
        h = f.Get("hHt")
        numOfEvents = h.Integral(-1,99999999)+0.000000000001
    print "Number of event:", numOfEvents

    t = f.Get("tEvent")
    t.GetEntry(0)
    weight = 1
    cs = 1
    if not data:
        cs = t.CrossSection
        print "CrossSection:", cs
        weight = cs/numOfEvents
        print "weight:", weight

    var_Weight = np.zeros(1,dtype=float)
    var_Weight[0] = weight
    nentries = t.GetEntries();
    if t.GetBranchStatus("Weight"):
        if not force:
            print "This tree is already weighted! Skipping..."
        else:
            branch = t.GetBranch("Weight")
            branch.Reset()
            branch.SetAddress(var_Weight)
            for ientry in range(nentries):
                branch.Fill()
            t.Write("tEvent",TObject.kOverwrite)
            print "Done"
        f.Close()
        continue

    newBranch = t.Branch("Weight",var_Weight,"Weight/D");
    for ientry in range(nentries):
        newBranch.Fill()
    print "Writing Tree"
    t.Write("tEvent",TObject.kOverwrite)
    print "Done"
    f.Close()

#!/usr/bin/env python

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

parser = argparse.ArgumentParser(description='Update cross section skims for x1x2x1 process.')
parser.add_argument('-i', '--input_dir', nargs=1, help='Input Directory', required=True)
parser.add_argument('-f', '--Force', dest='force', help='Force Update', action='store_true')
parser.add_argument('-bg', '--background', dest='bg', help='Background', action='store_true')
args = parser.parse_args()

input_dir = args.input_dir[0]
force = args.force
bg = args.bg
######## END OF CMDLINE ARGUMENTS ########
fileList = None
if bg:
    fileList = glob(input_dir + "/*DYJetsToLL_M-5to50_*");
else:
    fileList = glob(input_dir + "/*");
for fileName in fileList:
    if os.path.isdir(fileName): continue
    print("processing file " + fileName )
    f = TFile(fileName, "update")
    h = f.Get("hHt")
    numOfEvents = h.Integral(-1,99999999)+0.000000000001
    print("Number of event:", numOfEvents)

    t = f.Get("tEvent")
    t.GetEntry(0)
    fileBasename = None
    cs = 1
    if bg:
        fileBasename = "_".join(os.path.basename(fileName).split(".root")[0].split("_")[0:3])#.split("RunIISummer16MiniAODv3.")[1].split("_TuneCUETP8M1")[0]
        cs = utils.dyCrossSections.get(fileBasename)
    else:
        fileBasename = (os.path.basename(fileName).split("Chi20Chipm")[0]).replace("p", ".")
        cs = utils.getCrossSection(fileBasename)
    print("Getting cross section for ", fileBasename)
    print("CrossSection:", cs)
    var_CrossSection = np.zeros(1,dtype=float)
    var_CrossSection[0] = cs
    nentries = t.GetEntries();
    if t.GetBranchStatus("CrossSection"):
        branch = t.GetBranch("CrossSection")
        branch.Reset()
        branch.SetAddress(var_CrossSection)
        for ientry in range(nentries):
            branch.Fill()
        t.Write("tEvent",TObject.kOverwrite)
        print("Done")
        f.Close()
        continue
    
    newBranch = t.Branch("CrossSection",var_CrossSection,"CrossSection/D");
    for ientry in range(nentries):
        newBranch.Fill()
    print("Writing Tree")
    t.Write("tEvent",TObject.kOverwrite)
    print("Done")
    f.Close()


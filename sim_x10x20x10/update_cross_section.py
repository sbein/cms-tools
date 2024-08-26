#!/usr/bin/env python3

from ROOT import *
from glob import glob
from sys import exit
import numpy as np
import argparse
import sys
import os

sys.path.append("/afs/desy.de/user/n/nissanuv/cms-tools")
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
    if bg:
        fileBasename = os.path.basename(fileName).split(".root")[0]
        print(fileBasename)
        exit(0)
    else:
        fileBasename = os.path.basename(fileName).split("Chi20Chipm.root")[0]
    print("Getting cross section for ", fileBasename)
    cs = utils.getCrossSection(fileBasename)
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


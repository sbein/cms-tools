#!/usr/bin/env python

from ROOT import *
from glob import glob
from sys import exit
import argparse
import sys
import numpy as np
import os
import xml.etree.ElementTree as ET
from math import *

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes"))
from lib import analysis_ntuples
from lib import analysis_tools
from lib import utils
from lib import cut_optimisation

gROOT.SetBatch(True)
gStyle.SetOptStat(0)

gSystem.Load('LumiSectMap_C')
from ROOT import LumiSectMap

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Create skims for x1x2x1 process with BDTs.')
parser.add_argument('-i', '--input_file', nargs=1, help='Input Filename', required=True)
parser.add_argument('-s', '--signal', dest='signal', help='Signal', action='store_true')
parser.add_argument('-bg', '--background', dest='bg', help='Background', action='store_true')
parser.add_argument('-sc', '--same_charge', dest='sc', help='Same Charge', action='store_true')
parser.add_argument('-dy', '--dy', dest='dy', help='Drell-Yan', action='store_true')
parser.add_argument('-sam', '--sam', dest='sam', help='Sam Samples', action='store_true')
args = parser.parse_args()


signal = args.signal
bg = args.bg
sc = args.sc

print("SAME CHARGE=", sc)

input_file = None
if args.input_file:
    input_file = args.input_file[0].strip()

if (bg and signal) or not (bg or signal):
    signal = True
    bg = False

######## END OF CMDLINE ARGUMENTS ########

def main():
    
    file = TFile(input_file, "read")
    
    c = file.Get("tEvent")
    
    #c = TChain('TreeMaker2/PreSelection')
    print("Opening", input_file)
    #c.Add(input_file)
    
    nentries = c.GetEntries()
    print("File has", nentries, "entries")
    
    for ientry in range(nentries):
        if ientry % 100 == 0:
            print("Processing " + str(ientry) + " out of " + str(nentries))
        c.GetEntry(ientry)
        #analysis_ntuples.printTrigNames(c, "MhtMet6pack")
        analysis_ntuples.printTrigNames(c, "SingleMuon")
        
        
main()
exit(0)
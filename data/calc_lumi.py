#!/usr/bin/env python3.8

from ROOT import *
from glob import glob
from sys import exit
import argparse
import sys
import os
import re
from datetime import datetime

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes"))
import utils

gROOT.SetBatch(True)
gStyle.SetOptStat(0)

gSystem.Load('LumiSectMap_C')
from ROOT import LumiSectMap

#lumi = 5746.370
#weight = lumi / utils.LUMINOSITY

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Calculate Luminosity.')
parser.add_argument('-i', '--input_dir', nargs=1, help='Input Directory', required=False)
parser.add_argument('-j', '--json_file', nargs=1, help='Input JSON File', required=False)
args = parser.parse_args()

input_dir = None
json_file = None

if args.input_dir:
    input_dir = args.input_dir[0]
else:
    input_dir = "/afs/desy.de/user/n/nissanuv/ntupleHub/LeptonCollection"
    input_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim_phase1/sum"
    #input_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim/sum"

if args.json_file:
    json_file = args.json_file[0].strip()

#lumi = utils.get_lumi_from_bril('/tmp/tmp_json_1653484428.json', 'ynissan')
    #os.remove(tmpJsonFile)
#print("Luminosity=", lumi)
#exit(0)

if json_file is not None:
    print("tmpJsonFile", json_file)
    lumi = utils.get_lumi_from_bril(json_file, 'ynissan')
    print("Luminosity=", lumi)
else:
    lumiSecs = LumiSectMap()

    #data_files = glob(input_dir + "/Run201[678]*MET*")
    data_files = glob(input_dir + "/Run201[8]*MET*")
    
    for f in data_files: 
        print(f)
        rootFile = TFile(f)
        if rootFile.GetListOfKeys().Contains("lumiSecs"):
            lumis = rootFile.Get('lumiSecs')
            col = TList()
            col.Add(lumis)
            lumiSecs.Merge(col)
        else:
            print("Bad file", f)
            #os.remove(f)
        rootFile.Close()

    lumi = utils.calculateLumiFromLumiSecs(lumiSecs)
    print("Luminosity=", lumi)
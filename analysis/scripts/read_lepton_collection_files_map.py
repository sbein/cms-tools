#!/usr/bin/env python

from ROOT import *
from glob import glob
from sys import exit
import argparse
import sys
import numpy as np
import os

sys.path.append("/afs/desy.de/user/n/nissanuv/cms-tools")
sys.path.append("/afs/desy.de/user/n/nissanuv/cms-tools/lib/classes")

gSystem.Load('LeptonCollectionMap_C')
from ROOT import LeptonCollectionMap
from ROOT import LeptonCollectionFilesMap
from ROOT import LeptonCollection

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Create skims for x1x2x1 process.')
parser.add_argument('-i', '--input_file', nargs=1, help='Input Filename', required=False)
args = parser.parse_args()

print(args)

input_file = None
if args.input_file:
    input_file = args.input_file[0].strip()
######## END OF CMDLINE ARGUMENTS ########

def main():
    f = TFile(input_file,'read')
    
    leptonCollectionFilesMap = f.Get("leptonCollectionFilesMap")
    print("Size=", leptonCollectionFilesMap.getSize())
    #print(leptonCollectionMap.leptonCollectionMap)
    for a in leptonCollectionFilesMap.leptonCollectionFilesMap:
        print(a.first[0], a.first[1], a.first[2], a.second)
    f.Close()

main()

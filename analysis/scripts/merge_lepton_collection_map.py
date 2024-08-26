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
from ROOT import LeptonCollection

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Create skims for x1x2x1 process.')
parser.add_argument('-i', '--input_file', nargs='+', help='Input Filename', required=False)
parser.add_argument('-o', '--output_file', nargs=1, help='Output Filename', required=False)
parser.add_argument('-f', '--input_file_name', nargs=1, help='Input Filename', required=False)
args = parser.parse_args()

print(args)

input_files = None
#if len(args.input_file) < 2:
#    print("Need at least 2 file")
#    exit(0)
if args.input_file_name:
    input_file_name =  args.input_file_name[0]
    input_file_handle = open(input_file_name, "r")
    lines = input_file_handle.readlines()
    input_file_handle.close()
    input_files = lines[0].split(" ")
else:
    input_files = args.input_file

print("input_files", input_files)

######## END OF CMDLINE ARGUMENTS ########

#SINGLE_OUTPUT = "/pnfs/desy.de/cms/tier2/store/user/ynissan/NtupleHub/LeptonCollection"
SINGLE_OUTPUT = '/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/lc/single'

def main():
    maxMapSize = 30
    mapNum = 1
    
    newFile = TFile(args.output_file[0], "recreate")
    #input_files = glob(SINGLE_OUTPUT + "/Summer16*.QCD_HT500to700_*.root")
    leptonCollectionMap = None
    i = 1
    shouldWrite = True
    for nf in input_files:
        print("Opening ", nf, " ", i, " out of", len(input_files))
        f = TFile(nf,'read')
        leptonCollectionMapN = f.Get("leptonCollectionFilesMap")
        if leptonCollectionMap is None:
            leptonCollectionMap = LeptonCollectionFilesMap()
            #leptonCollectionMap = leptonCollectionMapN
        #else:
        leptonCollectionMap.Merge(leptonCollectionMapN)
        leptonCollectionMapN.IsA().Destructor(leptonCollectionMapN)
        f.Close()
        f.IsA().Destructor(f)
        if i % maxMapSize == 0:
            print("Writing map " + str(mapNum))
            newFile.cd()
            leptonCollectionMap.Write("leptonCollectionFilesMap" + str(mapNum))
            mapNum += 1
            shouldWrite = False
            leptonCollectionMap.IsA().Destructor(leptonCollectionMap)
            leptonCollectionMap = None
        else:
            shouldWrite = True
        i += 1
    if shouldWrite and leptonCollectionMap is not None:
        print("Writing map " + str(mapNum))
        newFile.cd()
        leptonCollectionMap.Write("leptonCollectionFilesMap" + str(mapNum))
    newFile.Close()
main()

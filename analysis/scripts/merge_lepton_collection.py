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

import os

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Create skims for x1x2x1 process.')
parser.add_argument('-i', '--input_file', nargs='+', help='Input Filename', required=True)
parser.add_argument('-o', '--output_dir', nargs=1, help='Output Dir', required=True)
args = parser.parse_args()

print(args)

input_files = None
#if len(args.input_file) < 2:
#    print("Need at least 2 file")
#    exit(0)
input_files = args.input_file
######## END OF CMDLINE ARGUMENTS ########

def main():
    import os
    
    for f in input_files:
        leptonCollectionFilesMap = LeptonCollectionFilesMap()
        file = TFile(f,'read')
        leptonCollectionMap = file.Get("leptonCollectionMap")
        print("Next file", f)
        size = leptonCollectionMap.getSize()
        print("Size=", size)
        #i = 0
        
        basename = os.path.basename(f)
        print("Will insert name", basename)
        for a in leptonCollectionMap.leptonCollectionMap:
            # i += 1
#             if i % 100000 == 0:
#                 print("Processing ", i, " out of", size)
                #break
            leptonCollectionFilesMap.insert(a.first[0], a.first[1], a.first[2], basename)
    
        file.Close()
        out_file = args.output_dir[0] + "/" + basename
        print("Creating " + out_file)
        fnew = TFile(out_file,'recreate')#, '', 0)
        leptonCollectionFilesMap.Write("leptonCollectionFilesMap")
        #tEvent.Write()
        print("Closing File...")
        fnew.Close()

main()

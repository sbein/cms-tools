#!/usr/bin/env python

from ROOT import *
from glob import glob
from math import *
from sys import exit
from array import array
import argparse
import sys
import numpy as np
import os

sys.path.append("/afs/desy.de/user/n/nissanuv/cms-tools")
from lib import histograms
from lib import utils
from lib import cuts
from lib import analysis_ntuples
from lib import analysis_tools

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Clones trees.')
parser.add_argument('-i', '--input_file', nargs=1, help='Input Filename', required=False)
parser.add_argument('-o', '--output_file', nargs=1, help='Output Filename', required=False)
args = parser.parse_args()

input_file = None
if args.input_file:
	input_file = args.input_file[0]
output_file = None
if args.output_file:
	output_file = args.output_file[0]
	
######## END OF CMDLINE ARGUMENTS ########

print("About to clone tree")

chain = TChain('TreeMaker2/PreSelection')
print("Going to open the file")
print(input_file)
chain.Add(input_file)
print("After opening")
tree = chain.CloneTree(0)

nentries = chain.GetEntriesFast()
print('Analysing', nentries, "entries")

max_per_file = 50000
filenum = 1

fnew = TFile(output_file + "_" + str(filenum) + ".root",'recreate')
fnew.mkdir("TreeMaker2");
fnew.cd("TreeMaker2")
new_entries = False

for ientry in range(nentries):
	if ientry % 5000 == 0:
		print("Processing " + str(ientry))
	if ientry != 0 and ientry % max_per_file == 0:
		print("Done copying. Writing to file")
		tree.Write('PreSelection')
		print("Done writing to file.")
		tree.Reset()
		fnew.Close()
		filenum +=1
		fnew = TFile(output_file + "_" + str(filenum) + ".root",'recreate')
		fnew.mkdir("TreeMaker2");
		fnew.cd("TreeMaker2")
		new_entries = False
	chain.GetEntry(ientry)
	tree.Fill()
	new_entries = True

if new_entries:
	print("Done copying. Writing to file")
	tree.Write('PreSelection')
	print("Done writing to file.")
	fnew.Close()

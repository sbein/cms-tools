#!/usr/bin/env python

import os, sys, re
from string import *
from ROOT import *
import argparse
from glob import glob

def error(message):
    print("** %s" % message)
    exit(0)

gSystem.AddDynamicPath("$RGS_PATH/lib")
if gSystem.Load("libRGS") < 0: error("unable to load libRGS")

NAME = "x10x20x10"

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Train RGS for x1x2x1 process.')
parser.add_argument('-s', '--signal', nargs=1, help='Input Signal', required=False)
parser.add_argument('-i', '--input_dir', nargs=1, help='Input Directory', required=False)
parser.add_argument('-c', '--cuts', nargs=1, help='Cuts File', required=False)
parser.add_argument('-f', '--file', nargs=1, help='Train single File', required=False)
parser.add_argument('-m', '--max_cuts', nargs=1, help='Maximum Number Of Cut Points', required=False)
args = parser.parse_args()

if args.signal and args.file:
	error("Can train only a single file")

sigfilename = None
if args.signal:
	sigfilename = args.signal[0]
input_dir = None
if args.input_dir:
	input_dir = args.input_dir[0]
cuts_files = None
if args.cuts:
	cuts_files = args.cuts[0]
train_file = None
if args.file:
	train_file = args.file[0]
maxcuts = -1 # maximum number of cut-points to consider
if args.max_cuts:
	maxcuts = args.max_cuts[0]
######## END OF CMDLINE ARGUMENTS ########

dir = None
cuts_name = None
if input_dir:
	dir = os.path.realpath(input_dir)
	cuts_name = os.path.basename(dir)
else:
	dir = os.path.dirname(os.path.realpath(sys.argv[0]))
	cuts_name = NAME

print(dir)
print(cuts_name)

varfilename  = dir + "/" + "%s.cuts" % cuts_name

if not os.path.exists(varfilename):
	error("unable to open variables file %s" % varfilename)
      
#bkgfiledir = "/afs/desy.de/user/n/nissanuv/work/x1x2x1/bg/skim/sum/type_sum"
#if not os.path.exists(bkgfiledir):
#	error("unable to open background dir %s" % bkgfiledir)

cutdatafilename = cuts_files or sigfilename
print("cutdatafilename" + "=" + cutdatafilename)
start      = 0           # start row 
treename   = "tEvent"    # name of Root tree 
weightname = "Weight"    # name of event weight variable

# One can add an optional selection, which, if true, keeps the event.
selection  = ""
rgs = RGS(cutdatafilename, start, maxcuts, treename, weightname, selection)

start   =  0                   # start row
numrows = -1                   # read all rows

outputFilename = None

if sigfilename:
	outputFilename = "signal"
	rgs.add(sigfilename, start, numrows, "_signal")
if train_file:
	filename = os.path.basename(train_file).split(".")[0].replace("-", "_")
	print("Name: " + filename)
	outputFilename = filename
	rgs.add(train_file, start, numrows, "_" + filename)

# bgFiles = glob(bkgfiledir + "/*.root")
# for bgFile in bgFiles:
# 	filename = os.path.basename(bgFile).split(".")[0].replace("-", "_")
# 	print("Name: " + filename)
# 	rgs.add(bgFile, start, numrows, "_" + filename)

rgs.run(varfilename)
# Write to a root file
resultsfilename= dir + "/single/" + "%s.root" % outputFilename
rgs.save(resultsfilename)
	

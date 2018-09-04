#!/usr/bin/env python

import os, sys, re
from string import *
from ROOT import *
import argparse
from glob import glob

def error(message):
    print "** %s" % message
    exit(0)

gSystem.AddDynamicPath("$RGS_PATH/lib")
if gSystem.Load("libRGS") < 0: error("unable to load libRGS")

NAME = "x10x20x10"

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Train RGS for x1x2x1 process.')
parser.add_argument('-s', '--signal', nargs=1, help='Input Signal', required=False)
parser.add_argument('-i', '--input_dir', nargs=1, help='Input Directory', required=False)
parser.add_argument('-c', '--cuts', nargs=1, help='Cuts File', required=False)
args = parser.parse_args()

sigfilename = None
if args.signal:
	sigfilename = args.signal[0]
else:
	sigfilename = "/afs/desy.de/user/n/nissanuv/work/x1x2x1/signal/skim/sum/type_sum/dm20.root"
input_dir = None
if args.input_dir:
	input_dir = args.input_dir[0]
cuts_files = None
if args.cuts:
	cuts_files = args.cuts[0]
######## END OF CMDLINE ARGUMENTS ########

dir = None
cuts_name = None
if input_dir:
	dir = os.path.realpath(input_dir)
	cuts_name = os.path.basename(dir)
else:
	dir = os.path.dirname(os.path.realpath(sys.argv[0]))
	cuts_name = NAME

print dir
print cuts_name

varfilename  = dir + "/" + "%s.cuts" % cuts_name
resultsfilename= dir + "/" + "%s.root" % cuts_name

if not os.path.exists(varfilename):
	error("unable to open variables file %s" % varfilename)

if not os.path.exists(sigfilename):
	error("unable to open signal file %s" % sigfilename)
      
bkgfiledir = "/afs/desy.de/user/n/nissanuv/work/x1x2x1/bg/skim/sum/type_sum"
if not os.path.exists(bkgfiledir):
	error("unable to open background dir %s" % bkgfiledir)

cutdatafilename = cuts_files or sigfilename
print "cutdatafilename" + "=" + cutdatafilename
start      = 0           # start row 
maxcuts    = -1          # maximum number of cut-points to consider
treename   = "tEvent"    # name of Root tree 
weightname = "Weight"    # name of event weight variable

# One can add an optional selection, which, if true, keeps the event.
selection  = ""
rgs = RGS(cutdatafilename, start, maxcuts, treename, weightname, selection)

start   =  0                   # start row
numrows = -1                   # read all rows
    
rgs.add(sigfilename, start, numrows, "_signal")

bgFiles = glob(bkgfiledir + "/*.root")
for bgFile in bgFiles:
	filename = os.path.basename(bgFile).split(".")[0].replace("-", "_")
	print "Name: " + filename
	rgs.add(bgFile, start, numrows, "_" + filename)

rgs.run(varfilename)
# Write to a root file
rgs.save(resultsfilename)
	
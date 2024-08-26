#!/usr/bin/python

from ROOT import *
from glob import glob
from math import *
from sys import exit
from array import array
from os import system
import argparse
import os
import sys

sys.path.append("/afs/desy.de/user/n/nissanuv/cms-tools")
from lib import utils

# load FWLite C++ libraries
# gSystem.Load("libFWCoreFWLite.so");
# gSystem.Load("libDataFormatsFWLite.so");
# FWLiteEnabler.enable()

# load FWlite python libraries
# from DataFormats.FWLite import Handle, Events
# import FWCore.ParameterSet.Config as cms

BG_OUTPUT = "/afs/desy.de/user/n/nissanuv/cms-tools/bg/output"
#BG_SINGLE_OUTPUT = "/afs/desy.de/user/n/nissanuv/cms-tools/bg/output/single"
BG_SINGLE_OUTPUT = "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v1"
BG_OUTPUT_SUM = BG_OUTPUT + "/sum"
BG_OUTPOUT_TYPE_SUM = BG_OUTPUT_SUM + "/type_sum"
BG_OUTPOUT_PROCESSED = BG_OUTPUT_SUM + "/processed"
BG_OUTPOUT_STACK = BG_OUTPUT_SUM + "/stack"
LUMINOSITY = 35900.

35900/4529783

fileList = glob(BG_SINGLE_OUTPUT + "/Summer16.WJetsToLNu_*");

for f in fileList : 
	cs = 0
	c = TChain("TreeMaker2/PreSelection");
	c.Add(f)
	c.GetEntry(0)
	print(f + " " + str(c.CrossSection))
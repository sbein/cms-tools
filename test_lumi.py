#!/usr/bin/env python

from ROOT import *
from glob import glob
from sys import exit
import argparse
import sys
import numpy as np
import os
import commands

def get_lumi_from_bril(json_file_name, cern_username, retry=False):
    status, out = commands.getstatusoutput('ps axu | grep "itrac5117-v.cern.ch:1012" | grep -v grep')
    if status != 0:
        print("Opening SSH tunnel for brilcalc...")
        os.system("ssh -f -N -L 10121:itrac5117-v.cern.ch:10121 %s@lxplus.cern.ch" % cern_username)
    else:
        print("Existing tunnel for brilcalc found")
    print("Getting lumi for %s..." % json_file_name)
    status, out = commands.getstatusoutput("export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda/bin:$PATH; brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -u /fb -c offsite -i %s > %s.briloutput; grep '|' %s.briloutput | tail -n1" % (json_file_name, '/tmp/tmp', '/tmp/tmp'))
    if status != 0:
        if not retry:
            print("Trying to re-establish the tunnel...")
            os.system("pkill -f itrac5117")
            get_lumi_from_bril(json_file_name, cern_username, retry=True)
        else:
            print("Error while running brilcalc!")
            if cern_username == "ynissan":
                print("Did you set your CERN username with '--cern_username'?")
        lumi = -1
    else:
        print("Output: " + out)
        lumi = float(out.split("|")[-2])
    
    print("lumi:", lumi)
    return lumi

def main():
    get_lumi_from_bril('/nfs/dust/cms/user/singha/LLCh/BACKGROUNDIII/CMSSW_10_1_0/src/DataHists_merged/Run2016_MET_13404.json', 'ynissan')

main()

#!/usr/bin/env python3.8

from ROOT import *
from glob import glob
from sys import exit
import argparse
import sys
import numpy as np
import os
import cppyy
import itertools
from datetime import datetime

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes"))
from lib import analysis_ntuples
from lib import analysis_tools
from lib import utils
from lib import analysis_observables

parser = argparse.ArgumentParser(description='Add observables to trees.')
args = parser.parse_args()



WORK_DIR = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim_phase1"
WORK_DIR = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim"
OUTPUT_SUM = WORK_DIR + "/sum"

OUTPUT_SUM_OUTPUT = WORK_DIR + "/stdout"
OUTPUT_SUM_ERROR = WORK_DIR + "/stderr"

if not os.path.isdir(OUTPUT_SUM_OUTPUT):
    os.mkdir(OUTPUT_SUM_OUTPUT)

if not os.path.isdir(OUTPUT_SUM_ERROR):
    os.mkdir(OUTPUT_SUM_ERROR)

condor_wrapper = utils.TOOLS_BASE_PATH + "/analysis/scripts/condor_wrapper.sh"
add_observable_script = utils.TOOLS_BASE_PATH + "/analysis/scripts/add_dqa_observables_to_tree.py"

print(("Start: " + datetime.now().strftime('%d-%m-%Y %H:%M:%S')))

condor_file="/tmp/condor_submut." + datetime.now().strftime('%d-%m-%Y_%H:%M:%S')
print("condor submit file:", condor_file)

def main():
    
    condor_f = open(condor_file,'w')
    condor_f.write('''
universe = vanilla
should_transfer_files = IF_NEEDED
executable = /bin/bash
notification = Never
''')
    
    print("Adding histograms.")
    fileList = glob(OUTPUT_SUM + "/*_topup_*");
    
    
    for f in fileList:
        filename = ".".join(os.path.basename(f).split(".")[0:2])

        command = add_observable_script + " -i " + f
        print("Perorming:", command)
    
        #system(command)
        condor_f.write("arguments = " + condor_wrapper + " " + command + "\n")
        condor_f.write("error = " + OUTPUT_SUM_ERROR + "/" + filename + "_add_dqa.err" + "\n")
        condor_f.write("output = " + OUTPUT_SUM_OUTPUT + "/" + filename + "_add_dqa.out" + "\n")
        condor_f.write("Queue\n")
            

    condor_f.close()
    system("condor_submit " + condor_file)
main()

exit(0)

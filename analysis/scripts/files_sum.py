#!/usr/bin/env python3

from ROOT import *
from glob import glob
from math import *
from sys import exit
from array import array
from os import system
import argparse
import os
import sys

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes"))
from lib import utils

parser = argparse.ArgumentParser(description='Sum histograms and trees.')
parser.add_argument('-skim', '--skim', dest='skim', help='Work on skim', action='store_true')
parser.add_argument('-bg', '--background', dest='bg', help='Background', action='store_true')
parser.add_argument('-sig', '--signal', dest='sig', help='Signal', action='store_true')
parser.add_argument('-lp', '--lepton_collection', dest='lepton_collection', help='Lepton Collection', action='store_true')
parser.add_argument('-sn', '--signal_ntuples', dest='signal_ntuples', help='Signal Ntuples', action='store_true')
parser.add_argument('-dlc', '--data_lepton_collection', dest='data_lepton_collection', help='Data Lepton Collection', action='store_true')
parser.add_argument('-tl', '--tl', dest='two_leptons', help='Two Leptons', action='store_true')
parser.add_argument('-dy', '--dy', dest='drell_yan', help='Two Leptons', action='store_true')
parser.add_argument('-sc', '--sc', dest='sc', help='Same Charge', action='store_true')
parser.add_argument('-nlp', '--no_lepton_selection', dest='no_lepton_selection', help='No Lepton Selection Skim', action='store_true')
parser.add_argument('-jpsi_electrons', '--jpsi_electrons', dest='jpsi_electrons', help='JPSI Electrons Skim', action='store_true')
parser.add_argument('-jpsi_muons', '--jpsi_muons', dest='jpsi_muons', help='JPSI Muons Skim', action='store_true')
parser.add_argument('-jpsi_muons_single_electron', '--jpsi_muons_single_electron', dest='jpsi_muons_single_electron', help='JPSI Muons Skim', action='store_true')
parser.add_argument('-master', '--master', dest='master', help='Master Skim', action='store_true')
parser.add_argument('-z_peak', '--z_peak', dest='z_peak', help='Z Peak Skim', action='store_true')
parser.add_argument('-slim', '--slim', dest='slim', help='slim', action='store_true')
parser.add_argument('-phase1', '--phase1', dest='phase1', help='phase1', action='store_true')
args = parser.parse_args()

##the double ## comments with SB could be made into a flag for the sam WZ ntuples

skim = args.skim
signal = args.sig
bg = args.bg
lepton_collection = args.lepton_collection
signal_ntuples = args.signal_ntuples
data_lepton_collection = args.data_lepton_collection
two_leptons = args.two_leptons
drell_yan = args.drell_yan
sc = args.sc
no_lepton_selection = args.no_lepton_selection
jpsi_muons = args.jpsi_muons
jpsi_muons_single_electron = args.jpsi_muons_single_electron
master = args.master
z_peak = args.z_peak
slim = args.slim
phase1 = args.phase1

if (bg and signal) or not (bg or signal):
    signal = True
    bg = False

WORK_DIR = None
if bg:
    if skim:
        WORK_DIR = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim"
        if lepton_collection:
            WORK_DIR = "/pnfs/desy.de/cms/tier2/store/user/ynissan/NtupleHub/LeptonCollectionFilesMaps/"
        elif two_leptons:
            if sc:
                WORK_DIR = "/afs/desy.de/user/n/nissanuv/nfs/2lx1x2x1/bg/skim_sc"
            else:
                ##SB##COMMENTWORK_DIR = "/afs/desy.de/user/n/nissanuv/nfs/2lx1x2x1/bg/skim"
                WORK_DIR = "/nfs/dust/cms/user/beinsam/x1x2x1/bg/skim_phase1"
        elif drell_yan:
            WORK_DIR = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_dy"
        elif no_lepton_selection:
            WORK_DIR = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_nlp"
        elif jpsi_muons:
            WORK_DIR = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_muons_jpsi"
        elif jpsi_muons_single_electron:
            WORK_DIR = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_jpsi_single_electron"
        elif master:
            WORK_DIR = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_master" 
        elif z_peak:
            WORK_DIR = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_z" 
        elif slim:
            WORK_DIR = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/slim"
            if phase1:
                ##WORK_DIR = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_phase1/sum/slim"
                WORK_DIR = "/nfs/dust/cms/user/beinsam/x1x2x1/bg/skim_phase1/sum/slim"
    else:
        WORK_DIR = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/hist"
else:
    if skim:
        WORK_DIR = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim"
        
        if lepton_collection:
            WORK_DIR = "/pnfs/desy.de/cms/tier2/store/user/ynissan/NtupleHub/LeptonCollectionFilesMaps/"
    else:
        WORK_DIR = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/"
    

SINGLE_OUTPUT = WORK_DIR + "/single"
OUTPUT_SUM = WORK_DIR + "/sum"
if slim:
    if phase1:
        SINGLE_OUTPUT = WORK_DIR + "/"
        ##SBCOMMENTED#OUTPUT_SUM = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_phase1/sum/slim_sum" 
        OUTPUT_SUM = "/nfs/dust/cms/user/beinsam/x1x2x1/bg/skim_phase1/sum/slim_sum" 
    else:
        SINGLE_OUTPUT = WORK_DIR + "/"
        OUTPUT_SUM = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/slim_sum" 

OUTPOUT_TYPE_SUM = OUTPUT_SUM + "/type_sum"


if lepton_collection:
    OUTPOUT_TYPE_SUM = "/tmp"
    SINGLE_OUTPUT = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/lc/single"
elif signal_ntuples:
    OUTPOUT_TYPE_SUM = "/tmp"
    SINGLE_OUTPUT = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/ntuples/single/"
    WORK_DIR = "/pnfs/desy.de/cms/tier2/store/user/ynissan/NtupleHub/SignalNtuples/"
elif data_lepton_collection:
    OUTPOUT_TYPE_SUM = "/tmp"
    SINGLE_OUTPUT = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/lc/single"
    WORK_DIR = "/pnfs/desy.de/cms/tier2/store/user/ynissan/NtupleHub/LeptonCollectionFilesMaps/"
else:
    if not os.path.isdir(OUTPUT_SUM):
        os.mkdir(OUTPUT_SUM)

    if not os.path.isdir(OUTPOUT_TYPE_SUM):
        os.mkdir(OUTPOUT_TYPE_SUM)

sumTypes = {}

print("Adding histograms.")
fileList = glob(SINGLE_OUTPUT + "/*");

if data_lepton_collection:
    files_glob = fileList
    
    #file = "Run2016_SingleMuon.root"
    file = "Run2016_SingleElectron.root"
    tmp_dir = "/afs/desy.de/user/n/nissanuv/nfs"
    #file = "Run2016_MET.root"
    print("***NUMBER:" + str(len(files_glob)))
    #print(files_glob)
    print("Checking " + WORK_DIR + "/" + os.path.basename(file))
    if os.path.exists(WORK_DIR + "/" + os.path.basename(file)):
        print("File " + WORK_DIR + "/" + os.path.basename(file) + " exists...")
        exit(1)

    command = "./merge_lepton_collection_map.py -o " + tmp_dir + "/" + file + " -i " + SINGLE_OUTPUT + "/*"
    print("Perorming:", command )
    system(command)
    command = "(eval `scram unsetenv -sh`; gfal-copy " + tmp_dir + "/" + file + " " + "srm://dcache-se-cms.desy.de" + WORK_DIR + ")"
    print("Perorming:", command )
    system(command)
    command = "rm " + tmp_dir + "/" + file
    print("Perorming:", command )
    #system(command)
else:
    for f in fileList:
        filename = None
        if bg and not slim:
            filename = os.path.basename(f).split(".")[1]
        else:
            filename = os.path.basename(f).split(".")[0]
        if "MET" in filename:
            continue
        types = filename.split("_")
        type = types[0]
        if signal_ntuples:
            type = types[0] + "_" + types[1] + "_" + types[2]
        if type not in sumTypes:
            sumTypes[type] = {}
        if bg:
            #if type == "DYJetsToLL" or type == "ST":
            #if type == "TT":
            #    sumTypes[type][types[1]] = True
            #else:
            print(types)
            types[2] = types[2].split("AOD")[0]
            sumTypes[type][types[1] + "_" + types[2]] = True
            #else:
            #    sumTypes[type][types[1]] = True

    print(sumTypes )

    for type in sumTypes:
        print(type)
        if bg:
            for typeRange in sumTypes[type]:
                print("-----")
                print(typeRange)
                print("-----")
                #continue
                command = None
                file = ""
                files = ""
                if slim:
                    file = OUTPOUT_TYPE_SUM + "/" + type + "_" + typeRange + ".root"
                    files = SINGLE_OUTPUT + "/" + type + "_*" + typeRange + "*.root"
                    command = "hadd -f " + file + " " + files
                elif "M-5to50" in typeRange:
                    #command = "/afs/desy.de/user/n/nissanuv/cms-tools/analysis/scripts/ahadd.py -f " + OUTPOUT_TYPE_SUM + "/" + type + "_" + typeRange + ".root " + SINGLE_OUTPUT + "/RunIISummer16MiniAODv3." + type + "_*" + typeRange + "*.root"
                    file = OUTPOUT_TYPE_SUM + "/" + type + "_" + typeRange + ".root"
                    if lepton_collection:
                        files = SINGLE_OUTPUT + "/Summer16*." + type + "_*" + typeRange + "*.root"
                    else:
                        files = SINGLE_OUTPUT + "/RunIISummer16MiniAODv3." + type + "_*" + typeRange + "*.root"
                    command = "hadd -f " + file + " " + files
                else:
                    file = OUTPOUT_TYPE_SUM + "/" + type + "_" + typeRange + ".root"
                    files = SINGLE_OUTPUT + "/Summer16*." + type + "_" + typeRange + "*.root"
                    command = "hadd -f " + file + " " + files
                if lepton_collection:
                    #command = "mkdir tmp"
                    #print("Perorming:", command )
                    #system(command)
                    #command = "gfal-copy -f srm://dcache-se-cms.desy.de/" + files + " ./tmp/"
                    #print("Perorming:", command )
                    #system(command)
                    print(files)
                    files_glob = glob(files)
                    print("***NUMBER:" + str(len(files_glob)) + " " + type + "_" + typeRange)
                    #print(files_glob)
                    print("Checking " + WORK_DIR + "/" + os.path.basename(file))
                    if os.path.exists(WORK_DIR + "/" + os.path.basename(file)):
                        print("File " + WORK_DIR + "/" + os.path.basename(file) + " exists...")
                        continue
                
                    command = "./merge_lepton_collection_map.py -o " + file + " -i " + files
                    print("Perorming:", command )
                    system(command)
                    command = "gfal-copy -f " + file + " " + "srm://dcache-se-cms.desy.de" + WORK_DIR
                    print("Perorming:", command )
                    system(command)
                    command = "rm -rf ./tmp"
                    print("Perorming:", command )
                    system(command)
                else:
                    if os.path.exists(file):
                        print("File", file, " exists. Skipping")
                    else:
                        print("Perorming:", command )
                        system(command)
                
        elif signal_ntuples:          
            print("-------")
            command = "hadd -f " + OUTPOUT_TYPE_SUM + "/" + type + "_1.root " + SINGLE_OUTPUT + "/" + type + "_*.root"
            print("Perorming:", command)
            system(command)
            command = "gfal-copy " + OUTPOUT_TYPE_SUM + "/" + type + "_1.root " + " srm://dcache-se-cms.desy.de" + WORK_DIR
            print("Perorming:", command)
            system(command)
            command = "rm " + OUTPOUT_TYPE_SUM + "/" + type + "_1.root "
            print("Perorming:", command)
            system(command)
        else:
            command = "hadd -f " + OUTPOUT_TYPE_SUM + "/" + type + ".root " + SINGLE_OUTPUT + "/" + type + "_*.root"
            print("Perorming:", command )
            #system(command)

exit(0)

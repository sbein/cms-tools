#!/usr/bin/env python

from ROOT import *
from glob import glob
from sys import exit
import argparse
import sys
import os
import re
from datetime import datetime
import math

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes"))
import utils
import analysis_ntuples

gROOT.SetBatch(True)
gStyle.SetOptStat(0)

gSystem.Load('LumiSectMap_C')
from ROOT import LumiSectMap

#lumi = 5746.370
#weight = lumi / utils.LUMINOSITY

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Plot skims for x1x2x1 process with BDTs.')
parser.add_argument('-o', '--output_file', nargs=1, help='Output Filename', required=False)
parser.add_argument('-s', '--single', dest='single', help='Single', action='store_true')
parser.add_argument('-c', '--cut', nargs=1, help='Cut', required=False)
parser.add_argument('-obs', '--obs', nargs=1, help='Obs', required=False)
parser.add_argument('-lep', '--lep', dest='lep', help='Single', action='store_true')
parser.add_argument('-bt', '--bg_retag', dest='bg_retag', help='Background Retagging', action='store_true')
args = parser.parse_args()

bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/type_sum"

bgReTagging = {
    "tautau" : "tautau",
    "sc" : "sc * (!tautau)",
    "tc" : "tc * (!tautau)",
    "fake" : "(rf || ff)",
    "other_sc": "other * (!tautau) * (omega || rho_0 || eta || phi || eta_prime || j_psi || upsilon_1 || upsilon_2)",
    "other_no_sc" : "other * (!tautau) * (!omega) * (!rho_0) * (!eta) * (!phi) * (!eta_prime) * (!j_psi) * (!upsilon_1) * (!upsilon_2)",
    "n_body" : "n_body * (!tautau)"
    
}

bgReTaggingOrder = {
    "tautau" : 0,
    "other_sc": 1,
    "other_no_sc" : 2,
    "sc" : 3,
    "tc" : 4,
    "fake" : 5,
    "n_body" : 6,
}

#orig
#hist_def = { "obs" : "dilepBDT", "minX" : 0.1, "maxX" : 1, "bins" : 30, "cond" : str(utils.LUMINOSITY) + "* passedMhtMet6pack * tEffhMetMhtRealXMht2016 * Weight * ((leptons[1].Pt() <= 3.5 || deltaR <= 0.3) && Mht >= 220 &&  Met >= 200 && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && dilepBDT > 0.1 && BTagsDeepMedium == 0 && vetoElectronsTightID == 0 && vetoMuonsPassJetIso == 0)" }

#{"name":"none", "title": "None", "condition" : "(twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12 && BTagsDeepMedium == 0 && vetoElectrons == 0 && vetoMuons == 0)", "baseline" : "sameSign == 0", "sc" : "sameSign == 1"},
#muons
#hist_def = { "obs" : "dilepBDT", "minX" : 0.1, "maxX" : 1, "bins" : 30, "cond" : str(utils.LUMINOSITY) + "* passedMhtMet6pack * tEffhMetMhtRealXMht2016 * Weight * ((leptons[1].Pt() <= 3.5 || deltaR <= 0.3) && twoLeptons == 1 && @leptons.size() == 2 && sameSign == 0 && MHT >= 220 &&  MET >= 200 && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && dilepBDT > 0.1 && BTagsDeepMedium == 0 && vetoElectrons == 0 && vetoMuons == 0 && leptonFlavour == \"Electrons\")" }
#electrons
hist_def = { "obs" : "dilepBDT", "minX" : 0.1, "maxX" : 1, "bins" : 30, "cond" : str(utils.LUMINOSITY) + "* passedMhtMet6pack * tEffhMetMhtRealXMht2016 * Weight * (twoLeptons == 1 && @leptons.size() == 2 && sameSign == 0 && MHT >= 220 &&  MET >= 200 && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && dilepBDT > 0.1 && BTagsDeepMedium == 0 && vetoElectrons == 0 && vetoMuons == 0 && leptonFlavour == \"Electrons\")" }
#hist_def = { "obs" : "dilepBDT", "minX" : -1, "maxX" : 1, "bins" : 60, "cond" : str(utils.LUMINOSITY) + "* passedMhtMet6pack * tEffhMetMhtRealXMht2016 * Weight * ((leptons[1].Pt() <= 3.5 || deltaR <= 0.3) && (invMass < 10 && invMass > 5) && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81))" }
ignore_bg_files = ["TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root", "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"]

def countBgInFiles(type, rootFiles, counts):
    for f in rootFiles:
        print(f)
        if os.path.basename(f) in ignore_bg_files:
            print("File", f, "in ignore list. Skipping...")
            continue
        rootFile = TFile(f)
        c = rootFile.Get('tEvent')
        #print(c)
        for bgReTagType in bgReTaggingOrder:
            #print(bgReTagType)
            drawString = hist_def["cond"] + " * " + bgReTagging[bgReTagType]
            hist = utils.getHistogramFromTree("tmp", c, hist_def["obs"], hist_def["bins"], hist_def["minX"], hist_def["maxX"], drawString, False)
            #print(hist)
            #print("{:.2f}".format(hist.Integral()))
            if counts[type].get(bgReTagType) is None:
                counts[type][bgReTagType] = 0
            counts[type][bgReTagType] += hist.Integral()
            
            
        rootFile.Close()

def main():
    print("Start: " + datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    
    counts = {}
    
    bg_files = glob(bg_dir + "/*")
    sumTypes = {}
    memory = []

    for f in bg_files: 
        filename = os.path.basename(f).split(".")[0]
        types = filename.split("_")
        type = None
        
        if types[0] == "TTJets":
            type = "_".join(types[0:2])
        elif types[0] == "ST":
            type = "_".join(types[0:3])
        else:
            type = types[0]
        if type not in sumTypes:
            sumTypes[type] = {}
        #sumTypes[types[0]][types[1]] = True

    print(sumTypes)
    
    for type in sumTypes:
        if utils.existsInCoumpoundType(type):
            continue
        print("Summing type", type)
        counts[type] = {}
        rootFiles = glob(bg_dir + "/*" + type + "_*.root")
        countBgInFiles(type, rootFiles, counts)
    
    for cType in utils.compoundTypes:
        print("Creating compound type", cType)
        counts[cType] = {}
        rootFiles = utils.getFilesForCompoundType(cType, bg_dir)
        print(rootFiles)
        countBgInFiles(cType, rootFiles, counts)
        
    print(counts)
    
    sortedBgReTagging = sorted([k for k in bgReTagging], key=lambda a: bgReTaggingOrder[a])
    sortedBgTypes = sorted([k for k in utils.bgOrder], key=lambda a: utils.bgOrder[a])
    
    print("," + ",".join(sortedBgReTagging))
    for bgType in sortedBgTypes:
        #print(bgType)
        print(bgType + "," + ",".join(["{:.2f}".format(counts[bgType][bgRetagType]) for bgRetagType in sortedBgReTagging]))

main()

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

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Slim skims for jet iso scan..')
parser.add_argument('-i', '--input_file', nargs=1, help='Input Filename', required=False)
parser.add_argument('-o', '--output_file', nargs=1, help='Output Filename', required=False)
args = parser.parse_args()

input_file = args.input_file[0]
output_file = args.output_file[0]

print "input_file", input_file
print "output_file", output_file


######## END OF CMDLINE ARGUMENTS ########

variablesUsed = []

variablesUsed.append("BTagsDeepMedium")
variablesUsed.append("MinDeltaPhiMetJets")
variablesUsed.append("MinDeltaPhiMhtJets")
variablesUsed.append("passedMhtMet6pack")
variablesUsed.append("tEffhMetMhtRealXMht2016")
variablesUsed.append("tEffhMetMhtRealXMht2017")
variablesUsed.append("tEffhMetMhtRealXMht2018")
variablesUsed.append("Weight")
variablesUsed.append("BranchingRatio")
variablesUsed.append("MET")
variablesUsed.append("METPhi")
variablesUsed.append("MHT")
variablesUsed.append("vetoElectronsPassIso")
variablesUsed.append("vetoMuonsPassIso")
variablesUsed.append("NJets")
variablesUsed.append("LeadingJetPt")
variablesUsed.append("LeadingJet")
variablesUsed.append("HT")
variablesUsed.append("Weight")
variablesUsed.append("passedMhtMet6pack")
variablesUsed.append("CrossSection")
variablesUsed.append("puWeight")
variablesUsed.append("passesUniversalSelection")

variablesUsed.append("prefireWeight")
variablesUsed.append("hemFailureVetoElectrons")
variablesUsed.append("hemFailureVetoJets")
variablesUsed.append("hemFailureVetoMuons")
variablesUsed.append("hemFailureVetoTracks")

#variablesUsed.append("FastSimWeightPR31285To36122")


variablesUsed.append("passesUniversalSelection")

# basic_histograms_defs = [
#         { "obs" : "invMass%%%", "minX" : 0, "maxX" : 13, "bins" : 6, "blind" : [4,None]},# "customBins"  : [0,2,4,6,10,12] },
#         { "obs" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 6, "blind" : [None,0.1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
#         { "obs" : "dilepBDT%%%_fine", "formula" : "dilepBDT%%%","minX" : -1, "maxX" : 1, "bins" : 15, "blind" : [None,0.1]},
#         { "obs" : "dilepBDT%%%_custom", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 6, "blind" : [None,0.1], "customBins"  : [-1,-0.6,-0.3,0,0.10,0.26,0.34,0.38,0.42,1] },
#         { "obs" : "deltaR%%%", "minX" : 0, "maxX" : 3.5, "bins" : 8},
#         { "obs" : "dilepHt%%%", "minX" : 200, "maxX" : 800, "bins" : 8},
#         { "obs" : "dileptonPt%%%", "minX" : 0, "maxX" : 30, "bins" : 8},
#         { "obs" : "MHT", "minX" : 220, "maxX" : 800, "bins" : 8},
#         { "obs" : "MET", "minX" : 200, "maxX" : 800, "bins" : 8},
#         { "obs" : "MinDeltaPhiMhtJets", "minX" : 0, "maxX" : 3.5, "bins" : 8},
#         { "obs" : "leptons%%%[0].Pt()", "minX" : 0, "maxX" : 20, "bins" : 8},
#         { "obs" : "deltaPhiMetLepton1%%%", "minX" : 0, "maxX" : 3.5, "bins" : 8},
#         { "obs" : "mt1%%%", "minX" : 0, "maxX" : 200, "bins" : 8},
#         { "obs" : "leptons%%%[0].Eta()", "minX" : -2.4, "maxX" : 2.4, "bins" : 8},
#         { "obs" : "NJets", "minX" : 0, "maxX" : 6, "bins" : 6},
#         { "obs" : "deltaPhiMetLepton2%%%", "minX" : 0, "maxX" : 3.5, "bins" : 8},
#         { "obs" : "LeadingJetPt", "minX" : 0, "maxX" : 500, "bins" : 8},
#         { "obs" : "LeadingJet.Eta()", "minX" : -2.4, "maxX" : 2.4, "bins" : 8},
#         { "obs" : "deltaEta%%%", "minX" : 0, "maxX" : 5, "bins" : 8},
#         { "obs" : "HT", "minX" : 0, "maxX" : 500, "bins" : 8},
#         { "obs" : "leptons%%%[0].Phi()", "minX" : 0, "maxX" : 3.5, "bins" : 8},
#      ]
#     
# notautau_cuts = [
#         {"name":"none", "title": "None", "condition" : "(MinDeltaPhiMetJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 200 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
#         {"name":"bdt", "title": "BDT > 0.35", "condition" : "(dilepBDT%%% > 0.35 &&  MinDeltaPhiMetJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 200 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
#     ]

preselection = "MinDeltaPhiMhtJets > 0.4 && MET >= 140 && MHT >= 220 && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && "
twoLeptonsConds = []

for iso in ["CorrJetNoMultIso"]:
    #for iso in utils.leptonIsolationList:
    for cat in utils.leptonIsolationCategories:
        ptRanges = [""]
        drCuts = [""]
        #if iso == "CorrJetNoMultIso":
        #    continue
        if iso in ["CorrJetIso", "CorrJetNoMultIso"]:
            ptRanges = utils.leptonCorrJetIsoPtRange
            drCuts = utils.leptonCorrJetIsoDrCuts
        for ptRange in ptRanges:
            for drCut in drCuts:
                cuts = ""
                if len(str(ptRange)) > 0:
                    cuts = str(ptRange) + "Dr" + str(drCut)
                jetiso = iso + cuts + cat
                variablesUsed.append("leptons" + jetiso)
                variablesUsed.append("deltaR" + jetiso)
                
                variablesUsed.append("deltaPhi" + jetiso)
                
                
                variablesUsed.append("dilepHt" + jetiso)
                variablesUsed.append("dileptonPt" + jetiso)
                variablesUsed.append("deltaPhiMetLepton1" + jetiso)
                variablesUsed.append("deltaPhiMetLepton2" + jetiso)
                variablesUsed.append("deltaPhiMhtLepton1" + jetiso)
                variablesUsed.append("deltaPhiMhtLepton2" + jetiso)
                variablesUsed.append("mt1" + jetiso)
                variablesUsed.append("mth1" + jetiso)
                variablesUsed.append("deltaEta" + jetiso)
                variablesUsed.append("twoLeptons" + jetiso)
                variablesUsed.append("dilepBDT" + jetiso)
                
                #variablesUsed.append("dilepBDTphase1" + jetiso)
                
                variablesUsed.append("leptonFlavour" + jetiso)
                variablesUsed.append("sameSign" + jetiso)
                variablesUsed.append("isoCr" + jetiso)
                variablesUsed.append("invMass" + jetiso)
                variablesUsed.append("mtautau" + jetiso)
                variablesUsed.append("nmtautau" + jetiso)
                variablesUsed.append("tc" + jetiso)
                variablesUsed.append("tautau" + jetiso)
                variablesUsed.append("other" + jetiso)
                variablesUsed.append("omega" + jetiso)
                variablesUsed.append("rho_0" + jetiso)
                variablesUsed.append("eta" + jetiso)
                variablesUsed.append("eta_prime" + jetiso)
                variablesUsed.append("j_psi" + jetiso)
                variablesUsed.append("upsilon_1" + jetiso)
                variablesUsed.append("upsilon_2" + jetiso)
                variablesUsed.append("phi" + jetiso)
                variablesUsed.append("n_body" + jetiso)
                variablesUsed.append("sc" + jetiso)
                variablesUsed.append("rf" + jetiso)
                variablesUsed.append("ff" + jetiso)
                                
                twoLeptonsConds.append("twoLeptons" + jetiso + " == 1")
                

preselection += "(" + " || ".join(twoLeptonsConds) + ")"

print "Preselection:"
print preselection

condor_wrapper = os.path.expandvars("$CMSSW_BASE/src/cms-tools/analysis/scripts/condor_wrapper.sh")

print(("Start: " + datetime.now().strftime('%d-%m-%Y %H:%M:%S')))

condor_file="/tmp/condor_submut." + datetime.now().strftime('%d-%m-%Y_%H:%M:%S')
print("condor submit file:", condor_file)

def main():
    print "Start: " + datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    
    # if not os.path.isdir(output_dir):
#         os.mkdir(output_dir)
    
    #files = glob(input_dir + "/*")
    
    #for filename in files:
    
    print "Opening", input_file
    #baseFileName = os.path.basename(input_file)
    #output_file = output_dir + "/" + baseFileName
    print "output_file", output_file
    
    if os.path.isfile(output_file):
        print "File exits. Skipping", output_file
        exit(0)

    f = TFile(input_file)
    c = f.Get('tEvent')
    if c.GetEntries() == 0:
        print "Emtpy. Skipping"
        f.Close()
        exit(0)

    print "old tree has", c.GetEntries()
    c.SetBranchStatus("*",0);
    for branch in variablesUsed:
        #print "Setting branch on", branch
        c.SetBranchStatus(branch,1)
    newfile = TFile(output_file,'recreate')
    newTree = c.CopyTree(preselection)
    print "new tree has", newTree.GetEntries()
    
    if newTree.GetEntries() == 0:
        print "Resulting tree is empty. Skipping."
        f.Close()
        newTree.Delete()
        newfile.Close()
        os.remove(output_file)
        exit(0)
    
    newfile.cd()
    newTree.Write("tEvent");
    newfile.Close();

    print "Done copying."

    c.Delete()
    f.Close() 
    
    print "End: " + datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    
main()
exit(0)
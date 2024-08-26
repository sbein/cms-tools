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

parser = argparse.ArgumentParser(description='Creates root files for limits and significance.')
parser.add_argument('-o', '--output_file', nargs=1, help='Output Filename', required=False)
#parser.add_argument('-s', '--single', dest='single', help='Single', action='store_true')
#parser.add_argument('-c', '--cut', nargs=1, help='Cut', required=False)
#parser.add_argument('-obs', '--obs', nargs=1, help='Obs', required=False)
args = parser.parse_args()

output_file = None

sam = True

signal_dir = None
bg_dir = None

if sam:
    signal_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_sam/sum"
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/type_sum"
else:
    signal_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_0.4/sum"
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_0.4/sum/type_sum"


if args.output_file:
    output_file = args.output_file[0]
else:
    output_file = "sig_bg_histograms_tmp_noiso.root"

jetIsos = {
    "Electrons": "CorrJetNoMultIso11Dr0.5",
    "Muons" : "CorrJetNoMultIso10Dr0.6",
    #"Muons" : "NoIso"
}


# was 30 originally
bins = 50

######## END OF CMDLINE ARGUMENTS ########

def main():
    print("Start: " + datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    
    fnew = TFile(output_file,'recreate')
    c1 = TCanvas("c1", "c1", 800, 800)
    c1.cd()
    
    print("Getting signals...")
    
    for filename in glob(signal_dir + "/*"):
        print("Opening", filename  )
        if sam:
            deltaM = utils.getPointFromSamFileName(filename)
        else:
            deltaM = utils.getPointFromFileName(filename)  
        
        
        
        print("deltaM=" + deltaM)
        if deltaM != "mChipm140GeV_dm4p28GeV":
            continue
        f = TFile(filename)
        c = f.Get('tEvent')

        for lep in ["Muons", "Electrons"]:
            orth_cond = " && (leptons" + jetIsos[lep] + "[1].Pt() <= 3.5 || deltaR" + jetIsos[lep] + " <= 0.3)"
            c1.cd()
            # prev
            #hist = utils.getHistogramFromTree(deltaM + "_1t_" + lep, c, "exTrack_dilepBDT", 30, -0.6, 0.6, str(utils.LUMINOSITY) + "* passedMhtMet6pack * tEffhMetMhtRealXMht2016 *  Weight * BranchingRatio * (exclusiveTrack == 1 && MHT >= 220 && MET >= 200 && exTrack_invMass < 30 && BTagsDeepMedium == 0 && exTrack_dilepBDT >= 0 && exclusiveTrackLeptonFlavour == \"" + lep + "\")", True)
            # Making new version without trackBDT precut
            # add trackBDT cuts and fix electrons stuff!!!
            hist = utils.getHistogramFromTree(deltaM + "_1t_" + lep, c, "exTrack_dilepBDT" + jetIsos[lep], bins, -1, 1, str(utils.LUMINOSITY) + "* passedMhtMet6pack * tEffhMetMhtRealXMht2016 *  Weight * BranchingRatio * (exclusiveTrack" + jetIsos[lep] + " == 1 && MET >= 140 && MHT >= 220 && exTrack_invMass" + jetIsos[lep] + " < 12 && BTagsDeepMedium == 0 && exclusiveTrackLeptonFlavour" + jetIsos[lep] + " == \"" + lep + "\")", True)
            #hist = utils.getHistogramFromTree(deltaM + "_1t_" + lep, c, "MET", bins, 0, 500, str(utils.LUMINOSITY) + "* passedMhtMet6pack * tEffhMetMhtRealXMht2016 *  Weight * BranchingRatio * (exclusiveTrack" + jetIsos[lep] + " == 1 && MHT >= 220 && exTrack_invMass" + jetIsos[lep] + " < 12 && BTagsDeepMedium == 0 && exclusiveTrackLeptonFlavour" + jetIsos[lep] + " == \"" + lep + "\")", True)
            hist.Sumw2()
            fnew.cd()
            hist.Write()
            orthOpt = [True, False] if lep == "Muons" else [False]
            for orth in orthOpt:
                c1.cd()
                hist = utils.getHistogramFromTree(deltaM + "_2l_" + ("orth_" if orth else "") + lep, c, "dilepBDT" + jetIsos[lep], bins, -1, 1, str(utils.LUMINOSITY) + "* passedMhtMet6pack * tEffhMetMhtRealXMht2016 * Weight * BranchingRatio * (twoLeptons" + jetIsos[lep] + " == 1 " + (orth_cond if orth else "") + " && MET >= 140 && MHT >= 220 && invMass" + jetIsos[lep] + " < 12  && invMass" + jetIsos[lep] + " > 0.4 && !(invMass" + jetIsos[lep] + " > 3 && invMass" + jetIsos[lep] + " < 3.2) && !(invMass" + jetIsos[lep] + " > 0.75 && invMass" + jetIsos[lep] + " < 0.81) && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && leptonFlavour" + jetIsos[lep] + " == \"" + lep + "\" && sameSign" + jetIsos[lep] + " == 0 && isoCr" + jetIsos[lep] + " == 0)", True)
                #hist = utils.getHistogramFromTree(deltaM + "_2l_" + ("orth_" if orth else "") + lep, c, "MET", bins, 0, 500, str(utils.LUMINOSITY) + "* passedMhtMet6pack * tEffhMetMhtRealXMht2016 * Weight * BranchingRatio * (twoLeptons" + jetIsos[lep] + " == 1 " + (orth_cond if orth else "") + " && MHT >= 220 && invMass" + jetIsos[lep] + " < 12  && invMass" + jetIsos[lep] + " > 0.4 && !(invMass" + jetIsos[lep] + " > 3 && invMass" + jetIsos[lep] + " < 3.2) && !(invMass" + jetIsos[lep] + " > 0.75 && invMass" + jetIsos[lep] + " < 0.81) && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && @leptons" + jetIsos[lep] + ".size() == 2 && leptonFlavour" + jetIsos[lep] + " == \"" + lep + "\" && sameSign" + jetIsos[lep] + " == 0 && isoCr" + jetIsos[lep] + " == 0)", True)
                #non-orth
                #hist = utils.getHistogramFromTree(deltaM + "_2l", c, "dilepBDT", 30, -0.6, 0.6, str(utils.LUMINOSITY) + "* passedMhtMet6pack * tEffhMetMhtRealXMht2016 * Weight * BranchingRatio * (MHT >= 220 &&  MET >= 200 && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && dilepBDT > 0.1)", True)
                hist.Sumw2()
                fnew.cd()
                hist.Write()
            
        f.Close()
    
    bg_1t_hist = {}
    bg_2l_hist = {}
    
    print("Getting BG...")
    
    for filename in glob(bg_dir + "/*"):
        break
        print("Opening", filename)
        f = TFile(filename)
        c = f.Get('tEvent')
        
        for lep in ["Muons", "Electrons"]:
            orth_cond = " && (leptons" + jetIsos[lep] + "[1].Pt() <= 3.5 || deltaR" + jetIsos[lep] + " <= 0.3)"
            c1.cd()
            basename = os.path.basename(filename).split(".")[0]
            # prev
            #hist = utils.getHistogramFromTree(basename, c, "exTrack_dilepBDT", 30, -0.6, 0.6, str(utils.LUMINOSITY) + "* passedMhtMet6pack * tEffhMetMhtRealXMht2016 * Weight * (exclusiveTrack == 1 && MHT >= 220 && MET >= 200 && exTrack_invMass < 30 && BTagsDeepMedium == 0  && exTrack_dilepBDT >= 0 && exclusiveTrackLeptonFlavour == \"" + lep + "\")", True)
            # Making new version without trackBDT precut
            hist = utils.getHistogramFromTree("bg_1t_" + lep, c, "exTrack_dilepBDT" + jetIsos[lep], bins, -1, 1, str(utils.LUMINOSITY) + "* passedMhtMet6pack * tEffhMetMhtRealXMht2016 *  Weight * BranchingRatio * (exclusiveTrack" + jetIsos[lep] + " == 1 && MET >= 140 && MHT >= 220 && exTrack_invMass" + jetIsos[lep] + " < 12 && BTagsDeepMedium == 0 && exclusiveTrackLeptonFlavour" + jetIsos[lep] + " == \"" + lep + "\")", True)
            #hist = utils.getHistogramFromTree(basename, c, "MET", bins, 0, 500, str(utils.LUMINOSITY) + "* passedMhtMet6pack * tEffhMetMhtRealXMht2016 *  Weight * BranchingRatio * (exclusiveTrack" + jetIsos[lep] + " == 1 && MHT >= 220 && exTrack_invMass" + jetIsos[lep] + " < 12 && BTagsDeepMedium == 0 && exclusiveTrackLeptonFlavour" + jetIsos[lep] + " == \"" + lep + "\")", True)
            hist.Sumw2()
            if bg_1t_hist.get(lep) is None:
                bg_1t_hist[lep] = hist
            else:
                bg_1t_hist[lep].Add(hist)
            
            orthOpt = [True, False] if lep == "Muons" else [False]
            for orth in orthOpt:
                c1.cd()
                print("2l",lep,orth)
                hist = utils.getHistogramFromTree("bg_2l_" + lep + ("_orth" if orth else ""), c, "dilepBDT" + jetIsos[lep], bins, -1, 1, str(utils.LUMINOSITY) + "* passedMhtMet6pack * tEffhMetMhtRealXMht2016 * Weight * BranchingRatio * (twoLeptons" + jetIsos[lep] + " == 1 "  + (orth_cond if orth else "") +  " && MET >= 140 && MHT >= 220 && invMass" + jetIsos[lep] + " < 12  && invMass" + jetIsos[lep] + " > 0.4 && !(invMass" + jetIsos[lep] + " > 3 && invMass" + jetIsos[lep] + " < 3.2) && !(invMass" + jetIsos[lep] + " > 0.75 && invMass" + jetIsos[lep] + " < 0.81) && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && leptonFlavour" + jetIsos[lep] + " == \"" + lep + "\" && sameSign" + jetIsos[lep] + " == 0 && isoCr" + jetIsos[lep] + " == 0)", True)
                #hist = utils.getHistogramFromTree(basename, c, "MET", bins, 0, 500, str(utils.LUMINOSITY) + "* passedMhtMet6pack * tEffhMetMhtRealXMht2016 * Weight * BranchingRatio * (twoLeptons" + jetIsos[lep] + " == 1 "  + (orth_cond if orth else "") +  " && MHT >= 220 && invMass" + jetIsos[lep] + " < 12  && invMass" + jetIsos[lep] + " > 0.4 && !(invMass" + jetIsos[lep] + " > 3 && invMass" + jetIsos[lep] + " < 3.2) && !(invMass" + jetIsos[lep] + " > 0.75 && invMass" + jetIsos[lep] + " < 0.81) && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && @leptons" + jetIsos[lep] + ".size() == 2 && leptonFlavour" + jetIsos[lep] + " == \"" + lep + "\" && sameSign" + jetIsos[lep] + " == 0 && isoCr" + jetIsos[lep] + " == 0)", True)
                #non-orth
                #hist = utils.getHistogramFromTree(basename, c, "dilepBDT", 30, -0.6, 0.6, str(utils.LUMINOSITY) + "* passedMhtMet6pack * tEffhMetMhtRealXMht2016 * Weight * (MHT >= 220 &&  MET >= 200 && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && dilepBDT > 0.1)", True)
                hist.Sumw2()
                if bg_2l_hist.get(lep + ("_orth" if orth else "")) is None:
                    bg_2l_hist[lep + ("_orth" if orth else "")] = hist
                else:
                    bg_2l_hist[lep + ("_orth" if orth else "")].Add(hist)
        
        f.Close()
    
    fnew.cd()
    for lep in ["Muons", "Electrons"]:
        break
        bg_1t_hist[lep].Write("bg_1t_" + lep)
        orthOpt = [True, False] if lep == "Muons" else [False]
        for orth in orthOpt:
            bg_2l_hist[lep + ("_orth" if orth else "")].Write("bg_2l_" + ("orth_" if orth else "") + lep)
    fnew.Close()
    
    exit(0)
    
main()

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

sam = False

signal_dir = None
bg_dir = None

if sam:
    signal_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_sam/sum"
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/type_sum"
else:
    signal_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/single"
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/type_sum"


bg_slim_file = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/slim_sum.root"
data_slim_file = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim/slim_sum/slim_sum.root"
#bg_slim_file = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/slim_sum_before_inc_isocr.root"

jetIsos = {
    "Electrons": "CorrJetNoMultIso11Dr0.5",
    "Muons" : "CorrJetNoMultIso10Dr0.6"
}


if args.output_file:
    output_file = args.output_file[0]
else:
    output_file = "sig_bg_histograms_for_track_category.root"

bins = 40

signals = [
    "mu100_dm4p30",
    "mu100_dm3p28",
    "mu100_dm2p51",
    "mu100_dm1p47",
    "mu100_dm1p13"
]

######## END OF CMDLINE ARGUMENTS ########

def main():
    print("Start: " + datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    
    fnew = TFile(output_file,'recreate')
    c1 = TCanvas("c1", "c1", 800, 800)
    c1.cd()

    i = 0
    
    print("Getting signals...")
    signal_histograms = {}
    for signal_file in signals:
        signal_files = glob(signal_dir + "/higgsino_" + signal_file + "Chi20Chipm*.root")
        print("=====================================\n\n\n\n\n\n\n\n\n\n\n")
        for filename in signal_files:
            print("Opening", filename  )
            if sam:
                deltaM = utils.getPointFromSamFileName(filename)
            else:
                print(filename)
                deltaM = utils.getPointFromFileName(filename)  
    
            print("deltaM=" + deltaM)
            f = TFile(filename)
            c = f.Get('tEvent')

            for lep in ["Muons", "Electrons"]:
        
                #if lep == "Electrons":
                #    continue
                jetiso = jetIsos[lep]
        
                #if jetiso != "CorrJetIso10.5Dr0.55":
                #    continue
        
                c1.cd()
        
                #1t category
                #hist = utils.getHistogramFromTree(deltaM + "_1t_" + lep + "_" + jetiso, c, "exTrack_dilepBDT" + jetiso, bins, -1, 1, str(utils.LUMINOSITY) + "* passedMhtMet6pack * tEffhMetMhtRealXMht2016 *  Weight * BranchingRatio * (exclusiveTrack" + jetiso + " == 1 && MinDeltaPhiMhtJets > 0.4 && MET >= 140 && MHT >= 220 && exTrack_invMass" + jetiso + " < 12 && BTagsDeepMedium == 0 && exclusiveTrackLeptonFlavour" + jetiso + " == \"" + lep + "\")", True)
        
                # hist.Sumw2()
#                             fnew.cd()
#                             hist.Write()
                cond = str(utils.LUMINOSITY) + " * passesUniversalSelection * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * Weight * BranchingRatio * (MinDeltaPhiMhtJets > 0.4 && MHT >= 220 &&  MET >= 140 && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && exclusiveTrack" + jetiso + " == 1 && exTrack_invMass" + jetiso + " < 12 && exclusiveTrackLeptonFlavour" + jetiso + " == \"" + lep + "\"" + (" && exTrack_deltaR" + jetiso + " > 0.05" if lep == "Electrons" else "") +  " && trackBDT" + jetiso + " > 0)"
               
                hist_name = deltaM + "_1t_" + lep  + "_" + jetiso
                hist = utils.getHistogramFromTree(hist_name, c, "exTrack_dilepBDT" + jetiso, bins, -1, 1, cond, True)
                hist.Sumw2()
                if signal_histograms.get(hist_name) is None:
                    signal_histograms[hist_name] = hist
                else:
                    signal_histograms[hist_name].Add(hist)

            
            f.Close()
    
    bg_1t_hist = {}
    
    print("Getting BG...")
    bg_files = glob(bg_dir + "/*")
    for filename in bg_files:#glob():
        print("=====================================\n\n\n\n\n\n\n\n\n\n\n")
        print("Opening", filename)
        f = TFile(filename)
        c = f.Get('tEvent')
        
        for lep in ["Muons", "Electrons"]:
            
            #if lep == "Electrons":
            #    continue
            

            jetiso = jetIsos[lep]
            
            #if jetiso != "CorrJetIso10.5Dr0.55":
            #    continue

            c1.cd()

                    
            cond = str(utils.LUMINOSITY) + " * passesUniversalSelection * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * Weight * BranchingRatio * (MinDeltaPhiMhtJets > 0.4 && MHT >= 220 &&  MET >= 140 && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && exclusiveTrack" + jetiso + " == 1 && exTrack_invMass" + jetiso + " < 12 && exclusiveTrackLeptonFlavour" + jetiso + " == \"" + lep + "\"" + (" && exTrack_deltaR" + jetiso + " > 0.05" if lep == "Electrons" else "") +  " && trackBDT" + jetiso + " > 0)"
            hist_name = "bg_1t_" + lep + "_" + jetiso
            hist = utils.getHistogramFromTree(hist_name, c, "exTrack_dilepBDT" + jetiso, bins, -1, 1, cond, True)
            hist.Sumw2()
            if bg_1t_hist.get(hist_name) is None:
                bg_1t_hist[hist_name] = hist
            else:
                bg_1t_hist[hist_name].Add(hist)
        f.Close()
    
    
    fnew.cd()
    for hist in signal_histograms:
        signal_histograms[hist].Write()
    for hist in bg_1t_hist:
        bg_1t_hist[hist].Write()
        

    fnew.Close()
    
    exit(0)
    
main()

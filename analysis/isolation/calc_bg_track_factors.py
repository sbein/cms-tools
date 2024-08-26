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
import analysis_selections

gROOT.SetBatch(True)
gStyle.SetOptStat(0)

gSystem.Load('LumiSectMap_C')
from ROOT import LumiSectMap

#lumi = 5746.370
#weight = lumi / utils.LUMINOSITY

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Calculate scale and normalisation factors.')
#parser.add_argument('-o', '--output_file', nargs=1, help='Output Filename', required=False)
#parser.add_argument('-s', '--single', dest='single', help='Single', action='store_true')
#parser.add_argument('-c', '--cut', nargs=1, help='Cut', required=False)
#parser.add_argument('-obs', '--obs', nargs=1, help='Obs', required=False)
args = parser.parse_args()

output_file = None

data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim/sum"

wanted_year = "phase1"
#wanted_year = "2016"

if wanted_year != "2016":
    data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim_phase1/sum"


######## END OF CMDLINE ARGUMENTS ########

def main():
    print("Start: " + datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    
    c1 = TCanvas("c1", "c1", 800, 800)
    c1.cd()
       
    data_1t_hist = {}
    
    pattern = "/*"
    if wanted_year == "2017" or wanted_year == "2018":
        pattern = "/Run" + wanted_year + "*"
    
    print("WANTED YEAR", wanted_year)
    
    data_files = glob(data_dir + pattern)
    i=1
    for filename in data_files:#glob(bg_dir + "/*"):
        print("=====================================")
        print("Analysing file", str(i), "out of", len(data_files))
        #if i > 10:
        #    break
        i+=1
        print("Opening", filename)
        f = TFile(filename)
        c = f.Get('tEvent')
        
        for lep in ["Muons", "Electrons"]:
        #for lep in ["Muons"]:
            for sc in [False, True]:
                
                # base_cond = "(" + data_filters[wanted_year] + "passedMhtMet6pack == 1 && passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && MHT >= 220 &&  MET >= 140 && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)"
#                 sc_cond =  "(" + ("sc_exTrack_deltaR%%% > 0.05 && " if lep == "Electrons" else "") + "sc_exclusiveTrack%%% == 1 && sc_trackBDT%%% > 0 && sc_exTrack_invMass%%% < 12 && sc_exTrack_dilepBDT%%% < 0 && sc_exclusiveTrackLeptonFlavour%%% == \""+lep+"\")"  if sc else "(" + ("exTrack_deltaR%%% > 0.05 && " if lep == "Electrons" else "") + "exclusiveTrack%%% == 1 && trackBDT%%% > 0 && exTrack_invMass%%% < 12  && exTrack_dilepBDT%%% < 0 && exclusiveTrackLeptonFlavour%%% == \""+lep+"\")"
#                 cond = base_cond + " && " + sc_cond
#                 condition = cond.replace("%%%", jetiso[lep])
                
                c1.cd()
                
                
                
                histName = "1t_" + lep + ("_sc" if sc else "")
                print("histName", histName)
                obs = None
                if sc:
                    obs = analysis_selections.exTrackSameSignDilepBDTString[wanted_year] + analysis_selections.jetIsos[lep]
                else:
                    obs = analysis_selections.exTrackDilepBDTString[wanted_year] + analysis_selections.jetIsos[lep]

                #hist = utils.getHistogramFromTree(histName, c, obs, 1, -1, 1, condition, False)
                #hist.Sumw2()
                
                #old_sum = hist.Integral()
                #print("old number", old_sum)
                
                conditions = analysis_selections.ex_track_cr_selections
                if sc:
                    conditions = analysis_selections.sc_ex_track_cr_selections
                if lep == "Electrons":
                    conditions = analysis_selections.ex_track_cr_electrons_selections
                    if sc:
                        conditions = analysis_selections.sc_ex_track_cr_electrons_selections
                
                condition = analysis_selections.getDataString(wanted_year, lep, conditions)
                print("new condition=" + condition)
                hist = utils.getHistogramFromTree(histName, c, obs, 1, -1, 1, condition, False)
                hist.Sumw2()
                new_sum = hist.Integral()
                print("new number", new_sum)
                #print("diff", old_sum-new_sum)
                print("\n\n")
                
                if data_1t_hist.get(histName) is None:
                    data_1t_hist[histName] = hist
                else:
                    data_1t_hist[histName].Add(hist)
                
        f.Close()
    
    print("\n\n\n\n\n")
    print(data_1t_hist)
    print("\n\n\n\n\n")
    for dataHistName in data_1t_hist:
        dataHist = data_1t_hist[dataHistName]
        dataNum = dataHist.GetBinContent(1)
        dataError = dataHist.GetBinError(1)
        print(dataHistName, "dataNum", dataNum, "dataError", dataError)
    
    print("=====================================\n\n\n\n\n\n\n\n\n\n\n")
    
    for lep in ["Muons", "Electrons"]:
    #for lep in ["Muons"]:
        print("\n\n\nsc scale factor - " + lep)
        numHist = data_1t_hist["1t_" + lep]
        denHist = data_1t_hist["1t_" + lep + "_sc"]
        print("num", numHist.GetBinContent(1), "den", denHist.GetBinContent(1))
        numHist.Divide(denHist)
        print("sf", numHist.GetBinContent(1), "err", numHist.GetBinError(1), "rel-err", numHist.GetBinError(1)/numHist.GetBinContent(1))
 
    exit(0)
    
main()

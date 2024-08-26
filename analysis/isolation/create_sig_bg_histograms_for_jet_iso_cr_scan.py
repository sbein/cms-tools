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

phase1_2017 = False

signal_dir = None
bg_dir = None
bg_slim_file = None
data_slim_file = None
eff_field = "tEffhMetMhtRealXMht2016"

bg_slim_file = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/slim_sum_total/slim_sum_total.root"
data_slim_file = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim/slim_sum/slim_sum.root"

if phase1_2017:
    signal_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_phase1/slim_sum"
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_phase1/sum/slim_sum"
    bg_slim_file = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_phase1/sum/slim_sum.root"
    eff_field = "tEffhMetMhtRealXMht2017"
elif sam:
    signal_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_sam/sum"
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/type_sum"
else:
    signal_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim_sum"
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/slim_sum/type_sum"



#bg_slim_file = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/slim_sum_before_inc_isocr.root"

jetiso = None
wanted_iso = "CorrJetNoMultIso"
unwanted_iso = "CorrJetIso"

get_data = False

# wanted_iso = "CorrJetIso"
# unwanted_iso = "CorrJetNoMultIso"

if args.output_file:
    output_file = args.output_file[0]
else:
    output_file = "sig_bg_histograms_for_jet_iso_scan" + wanted_iso + "_with_tautau_after_mht_with_data.root"
    output_file = "sig_bg_histograms_for_jet_iso_scan" + wanted_iso + "_with_tautau_2017.root"
    output_file = "sig_bg_histograms_for_jet_iso_scan" + wanted_iso + "_with_tautau_2016_with_phase1.root"

single_iso_choice = "CorrJetNoMultIso10Dr0.6"

bdt_var = "dilepBDT"
bdt_var = "dilepBDTphase1"

bins = 40

notautau = False

signals = [
    "mu100_dm4p30",
    "mu100_dm3p28",
    "mu100_dm2p51",
    "mu100_dm1p47",
    "mu100_dm1p13"
]

if phase1_2017:
    signals = [
        "mChipm100GeV_dm2p259GeV",
        "mChipm100GeV_dm1p759GeV",
        "mChipm100GeV_dm1p259GeV",
        "mChipm100GeV_dm0p759GeV",
        "mChipm100GeV_dm0p559GeV"
    ]

######## END OF CMDLINE ARGUMENTS ########

def main():
    print("Start: " + datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    
    fnew = TFile(output_file,'recreate')
    c1 = TCanvas("c1", "c1", 800, 800)
    c1.cd()
     
    mtautau_min = 0
    mtautau_max = 160
    
    if get_data:
    
        print("Getting Data...")
        data_files = [data_slim_file]
        for filename in data_files:#glob(bg_dir + "/*"):
        
            print("=====================================\n\n\n\n\n\n\n\n\n\n\n")
            print("Opening", filename)
            f = TFile(filename)
            c = f.Get('tEvent')
        
            for lep in ["Muons", "Electrons"]:
            
                #if lep == "Electrons":
                #    continue
            
                for iso in utils.leptonIsolationList:
                    if iso in [unwanted_iso, "JetIso"]:
                        continue
                    for cat in utils.leptonIsolationCategories:
                        ptRanges = [""]
                        drCuts = [""]
                        if iso == wanted_iso:
                            ptRanges = utils.leptonCorrJetIsoPtRange
                            drCuts = utils.leptonCorrJetIsoDrCuts
                        for ptRange in ptRanges:
                            for drCut in drCuts:
                                cuts = ""
                                if len(str(ptRange)) > 0:
                                    cuts = str(ptRange) + "Dr" + str(drCut)
                                jetiso = iso + cuts + cat
                            
                                #if jetiso != "CorrJetIso10.5Dr0.55":
                                #    continue
                                
                                if len(single_iso_choice) > 0 and jetiso!= single_iso_choice:
                                    continue

                                c1.cd()
                                basename = os.path.basename(filename).split(".")[0]
                                # prev
                                #hist = utils.getHistogramFromTree(basename, c, "exTrack_dilepBDT", 30, -0.6, 0.6, str(utils.LUMINOSITY) + "* passedMhtMet6pack * tEffhMetMhtRealXMht2016 * Weight * (exclusiveTrack == 1 && MHT >= 220 && MET >= 200 && exTrack_invMass < 30 && BTagsDeepMedium == 0  && exTrack_dilepBDT >= 0 && exclusiveTrackLeptonFlavour == \"" + lep + "\")", True)
                                # Making new version without trackBDT precut
                                # 1t category
                                # hist = utils.getHistogramFromTree("bg_1t_" + lep + "_" + jetiso, c, "exTrack_dilepBDT" + jetiso, bins, -1, 1, str(utils.LUMINOSITY) + "* passedMhtMet6pack * tEffhMetMhtRealXMht2016 *  Weight * BranchingRatio * (exclusiveTrack" + jetiso + " == 1 && MinDeltaPhiMhtJets > 0.4 && MET >= 140 && MHT >= 220 && exTrack_invMass" + jetiso + " < 12 && BTagsDeepMedium == 0 && exclusiveTrackLeptonFlavour" + jetiso + " == \"" + lep + "\")", True)
    #                             
    #                             hist.Sumw2()
    #                             if bg_1t_hist.get(lep) is None:
    #                                 bg_1t_hist[lep + "_" + jetiso] = hist
    #                             else:
    #                                 bg_1t_hist[lep + "_" + jetiso].Add(hist)
    #             
                                orthOpt = [True, False] if lep == "Muons" else [False]
                                orth_cond = " && (leptons" + jetiso + "[1].Pt() <= 3.5 || deltaR" + jetiso + " <= 0.3)"
                                isoCrs = [True, False] if iso == wanted_iso else [False]
                                print("isoCrs", isoCrs)
                                for orth in orthOpt:
                                    for isoCr in isoCrs:
                                        c1.cd()
                                    
                                        print("2l",lep,orth,jetiso,isoCr)

                                        #condition = "(passesUniversalSelection * twoLeptons" + jetiso + " == 1 "  + (orth_cond if orth else "") +  " && MinDeltaPhiMhtJets > 0.4 && MET >= 140 && MHT >= 220 && invMass" + jetiso + " < 12  && invMass" + jetiso + " > 0.4 && !(invMass" + jetiso + " > 3 && invMass" + jetiso + " < 3.2) && !(invMass" + jetiso + " > 0.75 && invMass" + jetiso + " < 0.81) && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && leptonFlavour" + jetiso + " == \"" + lep + "\" && sameSign" + jetiso + " == 0 && isoCr" + jetiso + (" >= 1" if isoCr else " == 0") + " && ( nmtautau" + jetiso + " < " + str(mtautau_min) + " || nmtautau"  + jetiso + " > " + str(mtautau_max) + " ) && dilepBDT" + jetiso + " < 0)"
                                        condition = "passesUniversalSelection * passedMhtMet6pack * (twoLeptons" + jetiso + " == 1 "  + (orth_cond if orth else "") +  " && MinDeltaPhiMhtJets > 0.4 && MET >= 140 && MHT >= 220 && invMass" + jetiso + " < 12  && invMass" + jetiso + " > 0.4 && !(invMass" + jetiso + " > 3 && invMass" + jetiso + " < 3.2) && !(invMass" + jetiso + " > 0.75 && invMass" + jetiso + " < 0.81) && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && leptonFlavour" + jetiso + " == \"" + lep + "\" && sameSign" + jetiso + " == 0 " + (("&& isoCr" + jetiso + (" >= 1" if isoCr else " == 0")) if len(cuts) > 0 else "") +  " && ( nmtautau" + jetiso + " < " + str(mtautau_min) + " || nmtautau"  + jetiso + " > " + str(mtautau_max) + " ))"
                                        #condition = "passesUniversalSelection * passedMhtMet6pack * (twoLeptons" + jetiso + " == 1 "  + (orth_cond if orth else "") +  " && MinDeltaPhiMhtJets > 0.4 && MET >= 140 && MHT >= 220 && invMass" + jetiso + " < 12  && invMass" + jetiso + " > 0.4 && !(invMass" + jetiso + " > 3 && invMass" + jetiso + " < 3.2) && !(invMass" + jetiso + " > 0.75 && invMass" + jetiso + " < 0.81) && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && leptonFlavour" + jetiso + " == \"" + lep + "\" && sameSign" + jetiso + " == 0 " + (("&& isoCr" + jetiso + (" >= 1" if isoCr else " == 0")) if len(cuts) > 0 else "") + " &&"
                                        print("condition", condition)
                                        histName = "data_2l_" + lep + ("_orth" if orth else "") + "_" + jetiso + ("_isoCr" if isoCr else "")
                                        print("histName", histName)
                                        hist = utils.getHistogramFromTree(histName, c, bdt_var + jetiso, bins, -1, 1, condition, True)
                                        hist.Sumw2()
                                        fnew.cd()
                                        hist.Write()
            f.Close()
    
    i = 0
    
    print("Getting signals...")
    
    for signal_file in signals:
        filename = signal_dir + "/higgsino_" + signal_file + "Chi20Chipm_1.root"
        
        if phase1_2017:
            filename = signal_dir + "/" + signal_file + "_1.root"
            
        print("=====================================\n\n\n\n\n\n\n\n\n\n\n")
        print("Opening", filename  )
        if sam or phase1_2017:
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
            
            for iso in utils.leptonIsolationList:
                if iso in [unwanted_iso, "JetIso"]:
                    continue
                for cat in utils.leptonIsolationCategories:
                    ptRanges = [""]
                    drCuts = [""]
                    if iso == wanted_iso:
                        ptRanges = utils.leptonCorrJetIsoPtRange
                        drCuts = utils.leptonCorrJetIsoDrCuts
                    for ptRange in ptRanges:
                        #if ptRange < 9:
                        #    continue
                        for drCut in drCuts:
                            cuts = ""
                            if len(str(ptRange)) > 0:
                                cuts = str(ptRange) + "Dr" + str(drCut)
                            jetiso = iso + cuts + cat
                            
                            #if jetiso != "CorrJetIso10.5Dr0.55":
                            #    continue
                            
                            if len(single_iso_choice) > 0 and jetiso!= single_iso_choice:
                                    continue
                            
                            c1.cd()
                            
                            #1t category
                            #hist = utils.getHistogramFromTree(deltaM + "_1t_" + lep + "_" + jetiso, c, "exTrack_dilepBDT" + jetiso, bins, -1, 1, str(utils.LUMINOSITY) + "* passedMhtMet6pack * tEffhMetMhtRealXMht2016 *  Weight * BranchingRatio * (exclusiveTrack" + jetiso + " == 1 && MinDeltaPhiMhtJets > 0.4 && MET >= 140 && MHT >= 220 && exTrack_invMass" + jetiso + " < 12 && BTagsDeepMedium == 0 && exclusiveTrackLeptonFlavour" + jetiso + " == \"" + lep + "\")", True)
                            
                            # hist.Sumw2()
#                             fnew.cd()
#                             hist.Write()
                            
                            orth_cond = " && (leptons" + jetiso + "[1].Pt() <= 3.5 || deltaR" + jetiso + " <= 0.3)"
                            orthOpt = [True, False] if lep == "Muons" else [False]
                            isoCrs = [True, False] if iso == wanted_iso else [False]
                            for orth in orthOpt:
                                for isoCr in isoCrs:
                                    c1.cd()
                                    cond = str(utils.LUMINOSITY) + " * " + eff_field + " * passedMhtMet6pack * Weight * BranchingRatio * (twoLeptons" + jetiso + " == 1 " + (orth_cond if orth else "") + " && MinDeltaPhiMhtJets > 0.4 && MET >= 140 && MHT >= 220 && invMass" + jetiso + " < 12  && invMass" + jetiso + " > 0.4 && !(invMass" + jetiso + " > 3 && invMass" + jetiso + " < 3.2) && !(invMass" + jetiso + " > 0.75 && invMass" + jetiso + " < 0.81) && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && leptonFlavour" + jetiso + " == \"" + lep + "\" && sameSign" + jetiso + " == 0 " + (("&& isoCr" + jetiso + (" >= 1" if isoCr else " == 0")) if len(cuts) > 0 else "") + ((" && !tautau" + jetiso) if notautau else "") + ")"
                                    hist = utils.getHistogramFromTree(deltaM + "_2l_" + ("orth_" if orth else "") + lep + "_" + jetiso + ("_isoCr" if isoCr else ""), c, bdt_var + jetiso, bins, -1, 1, cond, True)
                                    hist.Sumw2()
                                    fnew.cd()
                                    hist.Write()
                                    
                            
        f.Close()
    
    bg_1t_hist = {}
    bg_2l_hist = {}
    
    print("Getting BG...")
    bg_files = [bg_slim_file]
    for filename in bg_files:#glob(bg_dir + "/*"):
        print("=====================================\n\n\n\n\n\n\n\n\n\n\n")
        print("Opening", filename)
        f = TFile(filename)
        c = f.Get('tEvent')
        
        for lep in ["Muons", "Electrons"]:
            
            #if lep == "Electrons":
            #    continue
            
            for iso in utils.leptonIsolationList:
                if iso in [unwanted_iso, "JetIso"]:
                    continue
                for cat in utils.leptonIsolationCategories:
                    ptRanges = [""]
                    drCuts = [""]
                    if iso == wanted_iso:
                        ptRanges = utils.leptonCorrJetIsoPtRange
                        drCuts = utils.leptonCorrJetIsoDrCuts
                    for ptRange in ptRanges:
                        #if ptRange < 9:
                        #    continue
                        for drCut in drCuts:
                            cuts = ""
                            if len(str(ptRange)) > 0:
                                cuts = str(ptRange) + "Dr" + str(drCut)
                            jetiso = iso + cuts + cat
                            
                            #if jetiso != "CorrJetIso10.5Dr0.55":
                            #    continue

                            if len(single_iso_choice) > 0 and jetiso!= single_iso_choice:
                                continue
                            
                            c1.cd()
                            basename = os.path.basename(filename).split(".")[0]
                            # prev
                            #hist = utils.getHistogramFromTree(basename, c, "exTrack_dilepBDT", 30, -0.6, 0.6, str(utils.LUMINOSITY) + "* passedMhtMet6pack * tEffhMetMhtRealXMht2016 * Weight * (exclusiveTrack == 1 && MHT >= 220 && MET >= 200 && exTrack_invMass < 30 && BTagsDeepMedium == 0  && exTrack_dilepBDT >= 0 && exclusiveTrackLeptonFlavour == \"" + lep + "\")", True)
                            # Making new version without trackBDT precut
                            # 1t category
                            # hist = utils.getHistogramFromTree("bg_1t_" + lep + "_" + jetiso, c, "exTrack_dilepBDT" + jetiso, bins, -1, 1, str(utils.LUMINOSITY) + "* passedMhtMet6pack * tEffhMetMhtRealXMht2016 *  Weight * BranchingRatio * (exclusiveTrack" + jetiso + " == 1 && MinDeltaPhiMhtJets > 0.4 && MET >= 140 && MHT >= 220 && exTrack_invMass" + jetiso + " < 12 && BTagsDeepMedium == 0 && exclusiveTrackLeptonFlavour" + jetiso + " == \"" + lep + "\")", True)
#                             
#                             hist.Sumw2()
#                             if bg_1t_hist.get(lep) is None:
#                                 bg_1t_hist[lep + "_" + jetiso] = hist
#                             else:
#                                 bg_1t_hist[lep + "_" + jetiso].Add(hist)
#             
                            orthOpt = [True, False] if lep == "Muons" else [False]
                            orth_cond = " && (leptons" + jetiso + "[1].Pt() <= 3.5 || deltaR" + jetiso + " <= 0.3)"
                            isoCrs = [True, False] if iso == wanted_iso else [False]
                            print("isoCrs", isoCrs)
                            for orth in orthOpt:
                                for isoCr in isoCrs:
                                    c1.cd()
                                    
                                    print("2l",lep,orth,jetiso,isoCr)
                                    hist = utils.getHistogramFromTree("bg_2l_" + lep + ("_orth" if orth else "") + "_" + jetiso + ("_isoCr" if isoCr else ""), c, bdt_var + jetiso, bins, -1, 1, str(utils.LUMINOSITY) + " * " + eff_field + " * passedMhtMet6pack * Weight * BranchingRatio * (twoLeptons" + jetiso + " == 1 "  + (orth_cond if orth else "") +  " && MinDeltaPhiMhtJets > 0.4 && MET >= 140 && MHT >= 220 && invMass" + jetiso + " < 12  && invMass" + jetiso + " > 0.4 && !(invMass" + jetiso + " > 3 && invMass" + jetiso + " < 3.2) && !(invMass" + jetiso + " > 0.75 && invMass" + jetiso + " < 0.81) && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && leptonFlavour" + jetiso + " == \"" + lep + "\" && sameSign" + jetiso + " == 0 " + (("&& isoCr" + jetiso + (" >= 1" if isoCr else " == 0")) if len(cuts) > 0 else "") + ((" && !tautau" + jetiso) if notautau else "") + ")", True)
                                    hist.Sumw2()
                                    if bg_2l_hist.get(lep + ("_orth" if orth else "")) is None:
                                        bg_2l_hist[lep + ("_orth" if orth else "") + "_" + jetiso + ("_isoCr" if isoCr else "")] = hist
                                    else:
                                        bg_2l_hist[lep + ("_orth" if orth else "") + "_" + jetiso + ("_isoCr" if isoCr else "")].Add(hist)
        f.Close()
    
    
    fnew.cd()
    for lep in ["Muons", "Electrons"]:
        #if lep == "Electrons":
        #        continue
        for iso in utils.leptonIsolationList:
            if iso in [unwanted_iso, "JetIso"]:
                continue
            for cat in utils.leptonIsolationCategories:
                ptRanges = [""]
                drCuts = [""]
                if iso == wanted_iso:
                    ptRanges = utils.leptonCorrJetIsoPtRange
                    drCuts = utils.leptonCorrJetIsoDrCuts
                
                for ptRange in ptRanges:
                    #if ptRange < 9:
                    #        continue
                    for drCut in drCuts:
                        cuts = ""
                        if len(str(ptRange)) > 0:
                            cuts = str(ptRange) + "Dr" + str(drCut)
                        jetiso = iso + cuts + cat
                        #if jetiso != "CorrJetIso10.5Dr0.55":
                        #    continue
                        if len(single_iso_choice) > 0 and jetiso!= single_iso_choice:
                            continue
                        #bg_1t_hist[lep + "_" + jetiso].Write("bg_1t_" + lep + "_" + jetiso)
                        orthOpt = [True, False] if lep == "Muons" else [False]
                        isoCrs = [True, False] if iso == wanted_iso else [False]
                        for orth in orthOpt:
                            for isoCr in isoCrs:
                                bg_2l_hist[lep + ("_orth" if orth else "") + "_" + jetiso + ("_isoCr" if isoCr else "")].Write("bg_2l_" + ("orth_" if orth else "") + lep + "_" + jetiso + ("_isoCr" if isoCr else ""))
    fnew.Close()
    print("End: " + datetime.now().strftime('%d-%m-%Y %H:%M:%S'))

    exit(0)
    
main()

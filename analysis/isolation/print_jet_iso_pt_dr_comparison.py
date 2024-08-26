#!/usr/bin/env python

from ROOT import *
from glob import glob
from sys import exit
import argparse
import sys
import os
import re
from datetime import datetime
import cppyy
from ctypes import *

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes"))
import utils

gROOT.SetBatch(True)
gStyle.SetOptStat(0)

signals = [
    #"mu100_dm4p30",
    "mu100_dm3p28",
    #"mu100_dm2p51",
    #"mu100_dm1p47",
    #"mu100_dm1p13"
]

phase1_2017 = False
get_data = True

if phase1_2017:
    signals = [
        #"mChipm100GeV_dm2p259GeV",
        "mChipm100GeV_dm1p759GeV",
        #"mChipm100GeV_dm1p259GeV",
        #"mChipm100GeV_dm0p759GeV",
        #"mChipm100GeV_dm0p559GeV"
    ]


wanted_lepton = "Electrons"
wanted_lepton = "Muons"


wanted_iso = "CorrJetNoMultIso"
unwanted_iso = "CorrJetIso"

# wanted_iso = "CorrJetIso"
# unwanted_iso = "CorrJetNoMultIso"

def main():
    print("Start: " + datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    
    #histogram_file = TFile("sig_bg_histograms_for_jet_iso_scanCorrJetNoMultIso.root", "read")
    #histogram_file = TFile("sig_bg_histograms_for_jet_iso_scanCorrJetNoMultIso_no_tautau.root", "read")
    #histogram_file = TFile("sig_bg_histograms_for_jet_iso_scanCorrJetNoMultIso_no_tautau_after_mht.root", "read")
    histogram_file = TFile("sig_bg_histograms_for_jet_iso_scanCorrJetNoMultIso_no_tautau_after_mht_with_data.root", "read")
    
    #histogram_file = TFile("sig_bg_histograms_for_jet_iso_scanCorrJetNoMultIso_with_tautau_2017.root", "read")
    
    
    significance = {}
    signal_count = {}
    signal_count_cr = {}
    bg_count = {}
    bg_count_cr = {}
    data_count = {}
    data_count_cr = {}
    bg_transfer_factor_histogram = {}
    bg_sc_transfer_factor_histogram = {}
    data_transfer_factor_histogram = {}
    data_sc_transfer_factor_histogram = {}
    transfer_factor = {}
    transfer_factor_error = {}
    transfer_factor_data = {}
    transfer_factor_data_error = {}
    p_value = {}
    
    
    for lep in ["Muons", "Electrons"]:
        
        if lep != wanted_lepton:
            continue
        
        if significance.get(lep) is None:
            significance[lep] = {}
            signal_count[lep] = {}
            signal_count_cr[lep] = {}
            bg_count[lep] = {}
            bg_count_cr[lep] = {}
            data_count[lep] = {}
            data_count_cr[lep] = {}
            bg_transfer_factor_histogram[lep] = {}
            bg_sc_transfer_factor_histogram[lep] = {}
            data_transfer_factor_histogram[lep] = {}
            data_sc_transfer_factor_histogram[lep] = {}
            transfer_factor[lep] = {}
            transfer_factor_error[lep] = {}
            transfer_factor_data[lep] = {}
            transfer_factor_data_error[lep] = {}
            p_value[lep] = {}
        
        for iso in utils.leptonIsolationList:
            if iso in [unwanted_iso, "JetIso"]:
                continue
            for cat in utils.leptonIsolationCategories:
                ptRanges = [""]
                drCuts = [""]
                if iso in ["CorrJetIso", "CorrJetNoMultIso"]:
                    ptRanges = utils.leptonCorrJetIsoPtRange
                    drCuts = utils.leptonCorrJetIsoDrCuts
                for ptRange in ptRanges:
                    for drCut in drCuts:
                        cuts = ""
                        if len(str(ptRange)) > 0:
                            cuts = str(ptRange) + "Dr" + str(drCut)
                        jetiso = iso + cuts + cat
                        
                        if significance[lep].get(jetiso) is None:
                            significance[lep][jetiso] = {}
                            signal_count[lep][jetiso] = {}
                            signal_count_cr[lep][jetiso] = {}
                            bg_count[lep][jetiso] = {}
                            bg_count_cr[lep][jetiso] = {}
                            data_count[lep][jetiso] = {}
                            data_count_cr[lep][jetiso] = {}
                            bg_transfer_factor_histogram[lep][jetiso] = {}
                            bg_sc_transfer_factor_histogram[lep][jetiso] = {}
                            data_transfer_factor_histogram[lep][jetiso] = {}
                            data_sc_transfer_factor_histogram[lep][jetiso] = {}
                            transfer_factor[lep][jetiso] = {}
                            transfer_factor_error[lep][jetiso] = {}
                            transfer_factor_data[lep][jetiso] = {}
                            transfer_factor_data_error[lep][jetiso] = {}
                            p_value[lep][jetiso] = {}
                        
                        orthOpt = [True, False] if lep == "Muons" else [False]
                        isoCrs = [True, False] if iso == wanted_iso else [False]
                        isoCr = False
                        
                        for orth in orthOpt:
                            orthStr = "orth" if orth else "non-orth"
                            if significance[lep][jetiso].get(orthStr) is None:
                                significance[lep][jetiso][orthStr] = {}
                                signal_count[lep][jetiso][orthStr] = {}
                                signal_count_cr[lep][jetiso][orthStr] = {}
                                bg_transfer_factor_histogram[lep][jetiso][orthStr] = {}
                                bg_sc_transfer_factor_histogram[lep][jetiso][orthStr] = {}
                                data_transfer_factor_histogram[lep][jetiso][orthStr] = {}
                                data_sc_transfer_factor_histogram[lep][jetiso][orthStr] = {}
                                transfer_factor[lep][jetiso][orthStr] = {}
                                transfer_factor_error[lep][jetiso][orthStr] = {}
                                transfer_factor_data[lep][jetiso][orthStr] = {}
                                transfer_factor_data_error[lep][jetiso][orthStr] = {}
                                p_value[lep][jetiso][orthStr] = 0
                                #bg_count[lep][jetiso][orthStr] = {}
                            
                            bg_hist_name = "bg_2l_" + ("orth_" if orth else "") + lep + "_" + jetiso
                            bg_hist_name_cr = "bg_2l_" + ("orth_" if orth else "") + lep + "_" + jetiso + "_isoCr"
                            print("Getting", bg_hist_name)
                            bg_hist = histogram_file.Get(bg_hist_name)#.Rebin(5)
                            if iso == wanted_iso:
                                print("Getting", bg_hist_name_cr)
                                bg_hist_cr = histogram_file.Get(bg_hist_name_cr)
                                intError  = c_double()
                                bg_count_cr[lep][jetiso][orthStr] = bg_hist_cr.IntegralAndError(bg_hist_cr.FindBin(-1), bg_hist_cr.FindBin(0),intError)
                                bg_sc_transfer_factor_histogram[lep][jetiso][orthStr] = TH1F(bg_hist_name_cr + "_bg_transfer_factor_histogram", "", 1, 0, 1)
                                bg_sc_transfer_factor_histogram[lep][jetiso][orthStr].Sumw2()
                                bg_sc_transfer_factor_histogram[lep][jetiso][orthStr].SetBinContent(1,bg_count_cr[lep][jetiso][orthStr])
                                bg_sc_transfer_factor_histogram[lep][jetiso][orthStr].SetBinError(1,intError)
                                
                                integral = bg_hist.Integral()
                                bg_hist_copy = bg_hist.Clone()
                                bg_hist_copy.Scale(1./integral)
                                
                                integral = bg_hist_cr.Integral()
                                bg_hist_cr_copy = bg_hist_cr.Clone()
                                bg_hist_cr_copy.Scale(1./integral)
                                
                                p_value[lep][jetiso][orthStr] = bg_hist_copy.Chi2Test(bg_hist_cr_copy, "WW")
                            else:
                                print("What?")
                            intError  = c_double()
                            bg_count[lep][jetiso][orthStr] = bg_hist.IntegralAndError(bg_hist.FindBin(-1), bg_hist.FindBin(0), intError)
                            bg_transfer_factor_histogram[lep][jetiso][orthStr] = TH1F(bg_hist_name + "_bg_transfer_factor_histogram", "", 1, 0, 1)
                            bg_transfer_factor_histogram[lep][jetiso][orthStr].Sumw2()
                            bg_transfer_factor_histogram[lep][jetiso][orthStr].SetBinContent(1,bg_count[lep][jetiso][orthStr])
                            bg_transfer_factor_histogram[lep][jetiso][orthStr].SetBinError(1,intError)
                            if iso == wanted_iso:
                                print("Going to divide",bg_sc_transfer_factor_histogram[lep][jetiso][orthStr])
                                bg_transfer_factor_histogram[lep][jetiso][orthStr].Divide(bg_sc_transfer_factor_histogram[lep][jetiso][orthStr])
                            
                            
                            if get_data:
                            
                                # DATA SCALE FACTORS
                                data_hist_name = "data_2l_" + lep + "_" + ("orth_" if orth else "") + jetiso
                                data_hist_name_cr = "data_2l_" + lep + "_" + ("orth_" if orth else "") + jetiso + "_isoCr"
                                print("Getting", data_hist_name)
                                data_hist = histogram_file.Get(data_hist_name)#.Rebin(5)
                                if iso == wanted_iso:
                                    print("Getting", data_hist_name_cr)
                                    data_hist_cr = histogram_file.Get(data_hist_name_cr)
                                    intError  = c_double()
                                    data_count_cr[lep][jetiso][orthStr] = data_hist_cr.IntegralAndError(data_hist_cr.FindBin(-1), data_hist_cr.FindBin(0),intError)
                                    data_sc_transfer_factor_histogram[lep][jetiso][orthStr] = TH1F(data_hist_name_cr + "_data_transfer_factor_histogram", "", 1, 0, 1)
                                    data_sc_transfer_factor_histogram[lep][jetiso][orthStr].Sumw2()
                                    data_sc_transfer_factor_histogram[lep][jetiso][orthStr].SetBinContent(1,data_count_cr[lep][jetiso][orthStr])
                                    data_sc_transfer_factor_histogram[lep][jetiso][orthStr].SetBinError(1,intError)
                                else:
                                    print("What?")
                                intError  = c_double()
                                data_count[lep][jetiso][orthStr] = data_hist.IntegralAndError(data_hist.FindBin(-1), data_hist.FindBin(0), intError)
                                data_transfer_factor_histogram[lep][jetiso][orthStr] = TH1F(data_hist_name + "_data_transfer_factor_histogram", "", 1, 0, 1)
                                data_transfer_factor_histogram[lep][jetiso][orthStr].Sumw2()
                                data_transfer_factor_histogram[lep][jetiso][orthStr].SetBinContent(1,data_count[lep][jetiso][orthStr])
                                data_transfer_factor_histogram[lep][jetiso][orthStr].SetBinError(1,intError)
                                if iso == wanted_iso:
                                    print("Going to divide",data_sc_transfer_factor_histogram[lep][jetiso][orthStr])
                                    data_transfer_factor_histogram[lep][jetiso][orthStr].Divide(data_sc_transfer_factor_histogram[lep][jetiso][orthStr])
                           
                           
                           
                           
                           
                            for signal in signals:
                                sig_hist_name = signal + "_2l_" + ("orth_" if orth else "") + lep + "_" + jetiso
                                sig_hist = histogram_file.Get(sig_hist_name)#.Rebin(5)
                                print("Getting", sig_hist)
                                sig_hist_name_cr = signal + "_2l_" + ("orth_" if orth else "") + lep + "_" + jetiso + "_isoCr"
                                sig_hist_cr = histogram_file.Get(sig_hist_name_cr)#.Rebin(5)
                                print("Getting", sig_hist_cr)
                                
                                signal_count[lep][jetiso][orthStr][signal] = sig_hist.Integral(sig_hist.FindBin(0), sig_hist.FindBin(1))
                                if iso == wanted_iso:
                                    signal_count_cr[lep][jetiso][orthStr][signal] = sig_hist_cr.Integral(sig_hist_cr.FindBin(0), sig_hist_cr.FindBin(1))
                               
                                #significance[lep][jetiso][orthStr][signal] = utils.calcSignificanceNoAcc(sig_hist, bg_hist, True)
                                
                                
                                if iso != wanted_iso:
                                    continue
                                
                                newSigHist = sig_hist.Rebin(5,"newSigHist")
                                newBgHist = bg_hist_cr.Rebin(5,"newBgHist")
                                transferFactor = bg_transfer_factor_histogram[lep][jetiso][orthStr].GetBinContent(1)
                                transferFactorError = bg_transfer_factor_histogram[lep][jetiso][orthStr].GetBinError(1)
                                significance[lep][jetiso][orthStr][signal] = utils.calcSignificanceTransferFactor(newSigHist, newBgHist, transferFactor, transferFactorError)
                                
                            #for isoCr in isoCrs:
                                
                                #hist = utils.getHistogramFromTree(deltaM + "_2l_" + ("orth_" if orth else "") + lep + "_" + jetiso + ("_isoCr" if isoCr else ""), c, "dilepBDT" + jetiso, bins, -1, 1, str(utils.LUMINOSITY) + "* passedMhtMet6pack * tEffhMetMhtRealXMht2016 * Weight * BranchingRatio * (twoLeptons" + jetiso + " == 1 " + (orth_cond if orth else "") + " && MinDeltaPhiMetJets > 0.4 && MET >= 140 && MHT >= 220 && invMass" + jetiso + " < 12  && invMass" + jetiso + " > 0.4 && !(invMass" + jetiso + " > 3 && invMass" + jetiso + " < 3.2) && !(invMass" + jetiso + " > 0.75 && invMass" + jetiso + " < 0.81) && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && leptonFlavour" + jetiso + " == \"" + lep + "\" && sameSign" + jetiso + " == 0 " + (("&& isoCr" + jetiso + (" >= 1" if isoCr else " == 0")) if len(cuts) > 0 else "") + ")", True)
                                    
                                    
    #fitHist.Integral(fitHist.FindBin(3.0), fitHist.FindBin(3.2))
    
    orthStr = "non-orth"
    signal = "mu100_dm3p28"
    if phase1_2017:
         signal = "mChipm100GeV_dm1p759GeV"
    #signal = "mu100_dm1p47"
    
    print(significance)
    print("=============================================\n\n\n\n")
    print("Significance")
    print("pt/dr," + ",".join([str(dr) for dr in utils.leptonCorrJetIsoDrCuts]))
    for lep in ["Muons", "Electrons"]:
        if lep != wanted_lepton:
            continue
        for iso in utils.leptonIsolationList:
            if iso != wanted_iso:
                continue
            for cat in utils.leptonIsolationCategories:
                ptRanges = [""]
                drCuts = [""]
                if iso in ["CorrJetIso", "CorrJetNoMultIso"]:
                    ptRanges = utils.leptonCorrJetIsoPtRange
                    drCuts = utils.leptonCorrJetIsoDrCuts
                for ptRange in ptRanges:
                    pt_dr_sig = [str(ptRange)]
                    for drCut in drCuts:
                        cuts = ""
                        if len(str(ptRange)) > 0:
                            cuts = str(ptRange) + "Dr" + str(drCut)
                        jetiso = iso + cuts + cat
                        pt_dr_sig.append("{:.2f}".format(significance[lep][jetiso][orthStr][signal]))
                    print(",".join(pt_dr_sig))
    print("\n\n\n\n")
    print("Signal Efficiency")
    print("pt/dr," + ",".join([str(dr) for dr in utils.leptonCorrJetIsoDrCuts]))
    for lep in ["Muons", "Electrons"]:
        if lep != wanted_lepton:
            continue
        for iso in utils.leptonIsolationList:
            if iso != wanted_iso:
                continue
            for cat in utils.leptonIsolationCategories:
                ptRanges = [""]
                drCuts = [""]
                if iso in ["CorrJetIso", "CorrJetNoMultIso"]:
                    ptRanges = utils.leptonCorrJetIsoPtRange
                    drCuts = utils.leptonCorrJetIsoDrCuts
                for ptRange in ptRanges:
                    pt_dr_sig = [str(ptRange)]
                    for drCut in drCuts:
                        cuts = ""
                        if len(str(ptRange)) > 0:
                            cuts = str(ptRange) + "Dr" + str(drCut)
                        jetiso = iso + cuts + cat
                        pt_dr_sig.append("{:.2f}".format(signal_count[lep][jetiso][orthStr][signal]/signal_count[lep]["NoIso"][orthStr][signal]))
                    print(",".join(pt_dr_sig))
    print("\n\n\n\n")
    
    print("Background Efficiency")
    print("pt/dr," + ",".join([str(dr) for dr in utils.leptonCorrJetIsoDrCuts]))
    for lep in ["Muons", "Electrons"]:
        if lep != wanted_lepton:
            continue
        for iso in utils.leptonIsolationList:
            if iso != wanted_iso:
                continue
            for cat in utils.leptonIsolationCategories:
                ptRanges = [""]
                drCuts = [""]
                if iso in ["CorrJetIso", "CorrJetNoMultIso"]:
                    ptRanges = utils.leptonCorrJetIsoPtRange
                    drCuts = utils.leptonCorrJetIsoDrCuts
                for ptRange in ptRanges:
                    pt_dr_sig = [str(ptRange)]
                    for drCut in drCuts:
                        cuts = ""
                        if len(str(ptRange)) > 0:
                            cuts = str(ptRange) + "Dr" + str(drCut)
                        jetiso = iso + cuts + cat
                        pt_dr_sig.append("{:.2f}".format(bg_count[lep][jetiso][orthStr]/bg_count[lep]["NoIso"][orthStr]))
                    print(",".join(pt_dr_sig))
    print("\n\n\n\n")
    
    
    print("Background CR Ratio")
    print("pt/dr," + ",".join([str(dr) for dr in utils.leptonCorrJetIsoDrCuts]))
    for lep in ["Muons", "Electrons"]:
        if lep != wanted_lepton:
            continue
        for iso in utils.leptonIsolationList:
            if iso != wanted_iso:
                continue
            for cat in utils.leptonIsolationCategories:
                ptRanges = [""]
                drCuts = [""]
                if iso in ["CorrJetIso", "CorrJetNoMultIso"]:
                    ptRanges = utils.leptonCorrJetIsoPtRange
                    drCuts = utils.leptonCorrJetIsoDrCuts
                for ptRange in ptRanges:
                    pt_dr_sig = [str(ptRange)]
                    for drCut in drCuts:
                        cuts = ""
                        if len(str(ptRange)) > 0:
                            cuts = str(ptRange) + "Dr" + str(drCut)
                        jetiso = iso + cuts + cat
                        if bg_count[lep][jetiso][orthStr] > 0:
                            pt_dr_sig.append("{:.2f}".format(bg_count_cr[lep][jetiso][orthStr]/bg_count[lep][jetiso][orthStr]))
                        else:
                            pt_dr_sig.append("{:.2f}".format(-1))
                    print(",".join(pt_dr_sig))
    print("\n\n\n\n")
    
    print("Signal Contamination")
    print("pt/dr," + ",".join([str(dr) for dr in utils.leptonCorrJetIsoDrCuts]))
    for lep in ["Muons", "Electrons"]:
        if lep != wanted_lepton:
            continue
        for iso in utils.leptonIsolationList:
            if iso != wanted_iso:
                continue
            for cat in utils.leptonIsolationCategories:
                ptRanges = [""]
                drCuts = [""]
                if iso in ["CorrJetIso", "CorrJetNoMultIso"]:
                    ptRanges = utils.leptonCorrJetIsoPtRange
                    drCuts = utils.leptonCorrJetIsoDrCuts
                for ptRange in ptRanges:
                    pt_dr_sig = [str(ptRange)]
                    for drCut in drCuts:
                        cuts = ""
                        if len(str(ptRange)) > 0:
                            cuts = str(ptRange) + "Dr" + str(drCut)
                        jetiso = iso + cuts + cat
                        if bg_count[lep][jetiso][orthStr] > 0:
                            pt_dr_sig.append("{:.2f}".format(signal_count_cr[lep][jetiso][orthStr][signal]/bg_count[lep][jetiso][orthStr]))
                        else:
                            pt_dr_sig.append("{:.2f}".format(-1))
                    print(",".join(pt_dr_sig))
    print("\n\n\n\n")
    
    print("Signal CR to SR ratio")
    print("pt/dr," + ",".join([str(dr) for dr in utils.leptonCorrJetIsoDrCuts]))
    for lep in ["Muons", "Electrons"]:
        if lep != wanted_lepton:
            continue
        for iso in utils.leptonIsolationList:
            if iso != wanted_iso:
                continue
            for cat in utils.leptonIsolationCategories:
                ptRanges = [""]
                drCuts = [""]
                if iso in ["CorrJetIso", "CorrJetNoMultIso"]:
                    ptRanges = utils.leptonCorrJetIsoPtRange
                    drCuts = utils.leptonCorrJetIsoDrCuts
                for ptRange in ptRanges:
                    pt_dr_sig = [str(ptRange)]
                    for drCut in drCuts:
                        cuts = ""
                        if len(str(ptRange)) > 0:
                            cuts = str(ptRange) + "Dr" + str(drCut)
                        jetiso = iso + cuts + cat
                        if signal_count[lep][jetiso][orthStr][signal] > 0:
                            pt_dr_sig.append("{:.2f}".format(signal_count_cr[lep][jetiso][orthStr][signal]/signal_count[lep][jetiso][orthStr][signal]))
                        else:
                            pt_dr_sig.append("{:.2f}".format(-1))
                    print(",".join(pt_dr_sig))
    print("\n\n\n\n")
    
    
    print("Transfer Factor")
    print("pt/dr," + ",".join([str(dr) for dr in utils.leptonCorrJetIsoDrCuts]))
    for lep in ["Muons", "Electrons"]:
        if lep != wanted_lepton:
            continue
        for iso in utils.leptonIsolationList:
            if iso != wanted_iso:
                continue
            for cat in utils.leptonIsolationCategories:
                ptRanges = [""]
                drCuts = [""]
                if iso in ["CorrJetIso", "CorrJetNoMultIso"]:
                    ptRanges = utils.leptonCorrJetIsoPtRange
                    drCuts = utils.leptonCorrJetIsoDrCuts
                for ptRange in ptRanges:
                    pt_dr_sig = [str(ptRange)]
                    for drCut in drCuts:
                        cuts = ""
                        if len(str(ptRange)) > 0:
                            cuts = str(ptRange) + "Dr" + str(drCut)
                        jetiso = iso + cuts + cat

                        pt_dr_sig.append("{:.2f}".format(bg_transfer_factor_histogram[lep][jetiso][orthStr].GetBinContent(1)))
                    print(",".join(pt_dr_sig))
    print("\n\n\n\n")
    
    print("Transfer Factor Error")
    print("pt/dr," + ",".join([str(dr) for dr in utils.leptonCorrJetIsoDrCuts]))
    for lep in ["Muons", "Electrons"]:
        if lep != wanted_lepton:
            continue
        for iso in utils.leptonIsolationList:
            if iso != wanted_iso:
                continue
            for cat in utils.leptonIsolationCategories:
                ptRanges = [""]
                drCuts = [""]
                if iso in ["CorrJetIso", "CorrJetNoMultIso"]:
                    ptRanges = utils.leptonCorrJetIsoPtRange
                    drCuts = utils.leptonCorrJetIsoDrCuts
                for ptRange in ptRanges:
                    pt_dr_sig = [str(ptRange)]
                    for drCut in drCuts:
                        cuts = ""
                        if len(str(ptRange)) > 0:
                            cuts = str(ptRange) + "Dr" + str(drCut)
                        jetiso = iso + cuts + cat
                        
                        pt_dr_sig.append("{:.2f}".format(bg_transfer_factor_histogram[lep][jetiso][orthStr].GetBinError(1)))
                    print(",".join(pt_dr_sig))
    print("\n\n\n\n")
    
    if get_data:
    
        print("DATA Transfer Factor")
        print("pt/dr," + ",".join([str(dr) for dr in utils.leptonCorrJetIsoDrCuts]))
        for lep in ["Muons", "Electrons"]:
            if lep != wanted_lepton:
                continue
            for iso in utils.leptonIsolationList:
                if iso != wanted_iso:
                    continue
                for cat in utils.leptonIsolationCategories:
                    ptRanges = [""]
                    drCuts = [""]
                    if iso in ["CorrJetIso", "CorrJetNoMultIso"]:
                        ptRanges = utils.leptonCorrJetIsoPtRange
                        drCuts = utils.leptonCorrJetIsoDrCuts
                    for ptRange in ptRanges:
                        pt_dr_sig = [str(ptRange)]
                        for drCut in drCuts:
                            cuts = ""
                            if len(str(ptRange)) > 0:
                                cuts = str(ptRange) + "Dr" + str(drCut)
                            jetiso = iso + cuts + cat
                        
                            pt_dr_sig.append("{:.2f}".format(data_transfer_factor_histogram[lep][jetiso][orthStr].GetBinContent(1)))
                        print(",".join(pt_dr_sig))
        print("\n\n\n\n")
    
    print("P Value")
    print("pt/dr," + ",".join([str(dr) for dr in utils.leptonCorrJetIsoDrCuts]))
    for lep in ["Muons", "Electrons"]:
        if lep != wanted_lepton:
            continue
        for iso in utils.leptonIsolationList:
            if iso != wanted_iso:
                continue
            for cat in utils.leptonIsolationCategories:
                ptRanges = [""]
                drCuts = [""]
                if iso in ["CorrJetIso", "CorrJetNoMultIso"]:
                    ptRanges = utils.leptonCorrJetIsoPtRange
                    drCuts = utils.leptonCorrJetIsoDrCuts
                for ptRange in ptRanges:
                    pt_dr_sig = [str(ptRange)]
                    for drCut in drCuts:
                        cuts = ""
                        if len(str(ptRange)) > 0:
                            cuts = str(ptRange) + "Dr" + str(drCut)
                        jetiso = iso + cuts + cat
                        
                        pt_dr_sig.append("{:.2f}".format(p_value[lep][jetiso][orthStr]))
                    print(",".join(pt_dr_sig))
    print("\n\n\n\n")
    
    histogram_file.Close()
    
    print("\n\n\nEnd: " + datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    exit(0)
main()
exit(0)
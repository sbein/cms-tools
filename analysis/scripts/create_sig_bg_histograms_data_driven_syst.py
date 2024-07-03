#!/usr/bin/env python3.8

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

parser = argparse.ArgumentParser(description='Creates root files for limits and significance.')
parser.add_argument('-o', '--output_file', nargs=1, help='Output Filename', required=False)
parser.add_argument('-phase0', '--phase0', help='Phase 0', action='store_true')
parser.add_argument('-phase1', '--phase1', help='Phase 1', action='store_true')
parser.add_argument('-channel', '--channel')# 'leptons', tracks, all
parser.add_argument('-jecup', '--jecup', dest='jecup', help='jec-up variation', action='store_true')
parser.add_argument('-jecdown', '--jecdown', dest='jecdown', help='jec-down variation', action='store_true')
args = parser.parse_args()
phase1 = args.phase1
phase0 = args.phase0
channel = args.channel
jecup = args.jecup; jecdown = args.jecdown
sam = True

print('phase0', phase0)
print('phase1', phase1)
#choose one of the two
if phase0: wanted_year = "2016"
elif phase1: wanted_year = "phase1"

if jecup: thing2grab = 'JecUp'
elif jecdown: thing2grab = 'JecDown'
else: thing2grab = '1.roo'

#first test:
#systs_weightbased_nuni = ['','']#['','','TrgEff']#the first two are the normalization and Nominal value histograms, respectively!
#systs_weightbased_uni = []#['Isr','Pu']

systs_weightbased_nuni = ['','','TrgEff','MuSF','ElSF']#the first two are the normalization and Nominal value histograms, respectively!
systs_weightbased_uni = ['Isr','Pu','BTag']

if wanted_year=='2016': 
    #synch with Yuval
    #systs_weightbased_nuni = ['','']#['','','TrgEff']
    #systs_weightbased_uni = []#['Isr']
    systs_weightbased_nuni = ['','','TrgEff']
    systs_weightbased_uni = ['Isr']    

systs_weightbased = systs_weightbased_nuni+systs_weightbased_uni
print("WANTED YEAR " + wanted_year)

#choose one of the three
#channel = "all"
#channel = "tracks"
#channel = "leptons"

skip_electrons = True

use_uniform_binning = False
add_systematics = False
seperate_bg_methods = False
use_line_fits_predictions = False
use_line_fits_predictions_tf = False
ignore_tf_errors = False
max_files = -1
no_track_tf = False

final_prediction = True
if final_prediction:
    use_uniform_binning = False
    add_systematics = True
    seperate_bg_methods = True
    use_line_fits_predictions = True
    ignore_tf_errors = True
    no_track_tf = True
    max_files = -1

partial_unblinding = True
partial_unblinding = False###
partial_unblinding_portion = 10

# required_lepton = "Muons"
# jetiso = "CorrJetNoMultIso10Dr0.6"
# 
# required_lepton = "Electrons"
# jetiso = "CorrJetNoMultIso10Dr0.5"


output_file = None

if args.output_file: output_file = args.output_file[0]
else: output_file = "sig_bg_histograms_data_driven_" + wanted_year + "_" + channel + ("_uniform_binning" if use_uniform_binning else "") + ("_partial_unblinding" if partial_unblinding else "") + ".root"

if jecup: output_file = output_file.replace('.root','_JecUp.root')
if jecdown: output_file = output_file.replace('.root','_JecDown.root')    
print("output_file=" + output_file)

useYuvalsSkims = False

if useYuvalsSkims:
     signal_dirs = {
         "2016" : "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_sam/sum",
         "2017" : "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_phase1/sum",
         "2018" : "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_phase1_2018/sum",
     }
     
     if channel == "leptons":
         signal_dirs = {
             "2016" : "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_sam/slim_sum",
             "2017" : "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_phase1/slim_sum",
             "2018" : "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_phase1_2018/slim_sum",
         }    
else:
    signal_dirs = {
        "2016" : "/nfs/dust/cms/user/beinsam/x1x2x1/signal/skim_sam/sum",
        "2017" : "/nfs/dust/cms/user/beinsam/x1x2x1/signal/skim_phase1/sum",
        "2018" : "/nfs/dust/cms/user/beinsam/x1x2x1/signal/skim_phase1_2018/sum",
    }
    if channel == "leptons":
        signal_dirs = {
            "2016" : "/nfs/dust/cms/user/beinsam/x1x2x1/signal/skim_sam/sum",#"/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_sam/slim_sum",
            "2017" : "/nfs/dust/cms/user/beinsam/x1x2x1/signal/skim_phase1/sum",
            "2018" : "/nfs/dust/cms/user/beinsam/x1x2x1/signal/skim_phase1_2018/sum",
        }

bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/slim_sum_total"
data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim/slim_sum"

if channel != "leptons":
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/type_sum"
    data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim/sum"

data_pattern = "*"

if wanted_year != "2016":
    if channel != "leptons":
        bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_phase1/sum/type_sum" ####This could be where the "all" weirdness comes from
        data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim_phase1/sum"
        if wanted_year == "2017":
            data_pattern = "Run2017*"
        elif wanted_year == "2018":
            data_pattern = "Run2018*"
    else:
        bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_phase1/sum/slim_sum_total"####This could be where the "all" weirdness comes from
        if wanted_year == "2017":
            data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim_phase1/slim_2017"
        elif wanted_year == "2018":
            data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim_phase1/slim_2018"
        elif wanted_year == "phase1":
            data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim_phase1/slim_sum"


######## END OF CMDLINE ARGUMENTS ########

def main():
    print("Start: " + datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    
    bg_1t_hist = {}
    bg_2l_hist = {}
    
    data_1t_hist = {}
    data_2l_hist = {}
    
    print('creating file', output_file)
    fnew = TFile(output_file,'recreate')
    
    c1 = TCanvas("c1", "c1", 800, 800)
    c1.cd()
    
    global wanted_year
    
    i=0
    print("Getting DATA DRIVEN BG...")
    data_files = glob(data_dir + "/" + data_pattern)
    for filename in data_files:#skip these backgrounds
        #continue
        #continue #for now, let's skip the backgrounds, I only need the signals
        print("Opening", filename)
        f = TFile(filename)
        c = f.Get('tEvent')
        
        for lep in ["Muons", "Electrons"]:
        
            c1.cd()
            
            if channel != "leptons":
            
                histName = "bg1t" + lep + "ChargeSymmetric"
                if c.GetEntries()==0: continue
                obs = analysis_selections.exTrackSameSignDilepBDTString[wanted_year] + analysis_selections.jetIsos[lep]
                conditions = analysis_selections.sc_ex_track_full_range_selections
                if lep == "Electrons":
                    conditions = analysis_selections.sc_ex_track_full_range_selections_electrons
                weight = analysis_selections.getDataString(wanted_year, lep, conditions)
                hist = None
                if use_uniform_binning:
                    hist = utils.getHistogramFromTree(histName, c, obs, analysis_selections.uniform_binning_number, -1, 1, weight, False)
                else:
                    hist = utils.getHistogramFromTreeCustomBinsX(histName, c, obs, analysis_selections.binning["1t"][wanted_year][lep], weight, False)
                new_sum = hist.Integral()
                print("\n\nnew sum", new_sum)
                #was active# print("new number", new_sum)
                ###print("dif", new_sum-old_sum)
                
                #print("Scaling historgram with", lumi_weight_for_data)
                #hist.Scale(lumi_weight_for_data)
                
                tfHist = None
                tfHistName = histName + "_tfError"
                if not no_track_tf:
                    if ignore_tf_errors:
                        if add_systematics:
                            tfHist = hist.Clone(tfHistName)
                            tfHist.Sumw2()
                            tfHist.SetDirectory(0)
                            utils.scaleHistogram(tfHist, analysis_selections.sfs["tracks"][wanted_year][lep][0] + analysis_selections.sfs["tracks"][wanted_year][lep][1], 0)
                        utils.scaleHistogram(hist, analysis_selections.sfs["tracks"][wanted_year][lep][0], 0)
                    else:
                        utils.scaleHistogram(hist, analysis_selections.sfs["tracks"][wanted_year][lep][0], analysis_selections.sfs["tracks"][wanted_year][lep][1])
                
                if partial_unblinding:
                    utils.scaleHistogram(hist, 1./partial_unblinding_portion, 0)
                
                if bg_1t_hist.get(histName) is None:
                    bg_1t_hist[histName] = hist
                else:
                    bg_1t_hist[histName].Add(hist)
                
                if tfHist is not None:
                    if bg_1t_hist.get(tfHistName) is None:
                        bg_1t_hist[tfHistName] = tfHist
                    else:
                        bg_1t_hist[tfHistName].Add(tfHist)
                
                
                
                
                
                ########### GET UNBLINDED RESULTS ################
                
                if not partial_unblinding:
                    continue
                dataHistName = "data1t" + lep
                
                conditions = analysis_selections.ex_track_full_range_selections
                if lep == "Electrons":
                    conditions = analysis_selections.ex_track_full_range_selections_electrons
                if partial_unblinding:
                    conditions = conditions + ["Entry$ % 10==0"]
                
                weight = analysis_selections.getDataString(wanted_year, lep, conditions)
                
                obs = analysis_selections.exTrackDilepBDTString[wanted_year] + analysis_selections.jetIsos[lep]
                
                if use_uniform_binning:
                    hist = utils.getHistogramFromTree(dataHistName, c, obs, analysis_selections.uniform_binning_number, -1, 1, weight, False)
                else:
                    hist = utils.getHistogramFromTreeCustomBinsX(dataHistName, c, obs, analysis_selections.binning["1t"][wanted_year][lep], weight, False)
                
                if data_1t_hist.get(dataHistName) is None:
                    data_1t_hist[dataHistName] = hist
                else:
                    data_1t_hist[dataHistName].Add(hist)
                
        
            if channel != "tracks":
                if skip_electrons:
                    if lep == "Electrons":
                        continue
                orthOpt = [True, False] if lep == "Muons" else [False]
                #orth_cond = " && (leptons" + analysis_selections.jetIsos[lep] + "[1].Pt() <= 3.5 || deltaR" + analysis_selections.jetIsos[lep] + " <= 0.3)"
                print('orthOpt, lep', orthOpt, lep)
                for orth in orthOpt:
                    sigmaOpt = [True, False] if lep == "Muons" and add_systematics else [False]
                    for sigma in sigmaOpt:
                        c1.cd()
                        print("\n\n2l",lep,"orth",orth,"sigma",sigma)
                        
                        #weight = "(passedMhtMet6pack == 1 && passesUniversalSelection == 1 && twoLeptons%%% == 1 "  + (orth_cond if orth else "") +  " && MinDeltaPhiMhtJets > 0.4 && MET >= 140 && MHT >= 220 && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && leptonFlavour%%% == \"" + lep + "\" && sameSign%%% == 0 && isoCr%%% >= 1 " + (mtautauveto if veto_tautau else "") + ")"
                        #weight = weight.replace("%%%", analysis_selections.jetIsos[lep])
                        histName = "bg2l" + lep + ("Orth" if orth else "") + "Jetty" +  ("_shape" if sigma else "")
                        #print("\n\nhistName=" + histName)
                        #print("old weight="+weight)
                
                
                        #hist = utils.getHistogramFromTreeCustomBinsX(histName, c, "dilepBDT" + analysis_selections.jetIsos[lep], analysis_selections.binning["2l"][lep], weight, False)
                        #hist.Sumw2()
                        #hist.Scale(lumi_weight_for_data)
                        #old_sum = hist.Integral()
                        #print("old number", old_sum)
                
                        conditions = analysis_selections.two_leptons_full_bdt_iso_sb_outside_mtautau_window
                        if orth:
                            conditions = analysis_selections.two_leptons_full_bdt_iso_sb_outside_mtautau_window_sos
                    
                        extra_filters = []
                        if use_line_fits_predictions:
                            if sigma:
                                extra_filters = analysis_selections.extra_filters_2l_sigma_prediction[wanted_year][lep]
                            else:
                                extra_filters = analysis_selections.extra_filters_2l_main_prediction[wanted_year][lep]
                        
                        print("extra_filters", extra_filters)
                        weight = analysis_selections.getDataString(wanted_year, lep, conditions, extra_filters)
                
                        observable = analysis_selections.dilepBDTString[wanted_year] + analysis_selections.jetIsos[lep]
                    
                        hist = None
                        if use_uniform_binning:
                            hist = utils.getHistogramFromTree(histName, c, observable, analysis_selections.uniform_binning_number, -1, 1, weight, False)
                        else:
                            hist = utils.getHistogramFromTreeCustomBinsX(histName, c, observable, analysis_selections.binning["2l"][lep], weight, False)
                        hist.Sumw2() 
                        
                        if partial_unblinding:
                            utils.scaleHistogram(hist, 1./partial_unblinding_portion, 0)
                        
                        
                        #print("\n\nnew weight="+weight)
                        #hist = utils.getHistogramFromTreeCustomBinsX(histName, c, "dilepBDT" + analysis_selections.jetIsos[lep], analysis_selections.binning["2l"][lep], weight, False)
                        #hist.Sumw2()
                        new_sum = hist.Integral()
                        print("\n\nnew number", new_sum)
                        #print("difference", old_sum-new_sum)
                        print("\n\n")
                        
                        tfHist = None
                        tfHistName = histName + "_tfError"
                        if use_line_fits_predictions:
                            sfa = [0,0]
                            if sigma:
                                if use_line_fits_predictions_tf:
                                    sfa = analysis_selections.non_iso_2l_factors_sigma[wanted_year][lep]
                                else:
                                    sfa = analysis_selections.non_iso_2l_factors_base[wanted_year][lep]
                            else:
                                sfa = analysis_selections.non_iso_2l_factors_base[wanted_year][lep]
                            if ignore_tf_errors:
                                # we are not using the scale error anymore....
                                
                                if add_systematics and not sigma:
                                    tfHist = hist.Clone(tfHistName)
                                    tfHist.Sumw2()
                                    tfHist.SetDirectory(0)
                                    utils.scaleHistogram(tfHist, sfa[0] + sfa[1], 0)
                                
                                utils.scaleHistogram(hist, sfa[0], 0)
                            else:
                                utils.scaleHistogram(hist, sfa[0], sfa[1])
                        else:
                            if ignore_tf_errors:
                                # we are not using the scale error anymore....
                                if add_systematics and not sigma:
                                    tfHist = hist.Clone(tfHistName)
                                    tfHist.Sumw2()
                                    tfHist.SetDirectory(0)
                                    utils.scaleHistogram(tfHist, analysis_selections.sfs["leptons"][wanted_year][lep][0] + analysis_selections.sfs["leptons"][wanted_year][lep][1], 0)
                                utils.scaleHistogram(hist, analysis_selections.sfs["leptons"][wanted_year][lep][0], 0)
                            else:
                                utils.scaleHistogram(hist, analysis_selections.sfs["leptons"][wanted_year][lep][0], analysis_selections.sfs["leptons"][wanted_year][lep][1])
                    
                        if bg_2l_hist.get(histName) is None:
                            bg_2l_hist[histName] = hist
                        else:
                            bg_2l_hist[histName].Add(hist)
                        if tfHist is not None:
                            if bg_2l_hist.get(tfHistName) is None:
                                bg_2l_hist[tfHistName] = tfHist
                            else:
                                bg_2l_hist[tfHistName].Add(tfHist)
                    #bg_2l_hist[histName].Draw('hist e')
                    #c1.Update()
                    #pause()            
                    #print('went beyond pause') 
                    
                    
                    ########### GET UNBLINDED RESULTS ################
                
                    if not partial_unblinding:
                        continue
                    
                    histName = "data2l" + lep + ("Orth" if orth else "")
                    
                    conditions = analysis_selections.two_leptons_full_bdt_conditions_outside_mtautau_window
                    if orth:
                        conditions = analysis_selections.two_leptons_full_bdt_conditions_outside_mtautau_window_sos
                    
                    if partial_unblinding:
                        conditions = conditions + ["Entry$ % 10==0"]
                    extra_filters = []
                    if use_line_fits_predictions:
                         extra_filters = analysis_selections.extra_filters_2l_main_prediction[wanted_year][lep]
                    
                    print("extra_filters", extra_filters)
                    weight = analysis_selections.getDataString(wanted_year, lep, conditions, extra_filters)
            
                    observable = analysis_selections.dilepBDTString[wanted_year] + analysis_selections.jetIsos[lep]
                
                    hist = None
                    if use_uniform_binning:
                        hist = utils.getHistogramFromTree(histName, c, observable, analysis_selections.uniform_binning_number, -1, 1, weight, False)
                    else:
                        hist = utils.getHistogramFromTreeCustomBinsX(histName, c, observable, analysis_selections.binning["2l"][lep], weight, False)
                    hist.Sumw2() 
                    
                    if data_2l_hist.get(histName) is None:
                        data_2l_hist[histName] = hist
                    else:
                        data_2l_hist[histName].Add(hist)
        
        f.Close()
        i += 1
        if max_files > 0 and i >= max_files:
            break
    
    print("bg_2l_hist", bg_2l_hist)
    
    if channel != "tracks":
    
        print("Getting Mtautau BG...")
        bg_slim_files = glob(bg_dir + "/*")
        for filename in bg_slim_files:
            #continue ##for now, let's not worry about the mtau tau background either
            print("Opening", filename)
            f = TFile(filename)
            c = f.Get('tEvent')
        
            for lep in ["Muons", "Electrons"]:
                if skip_electrons:
                    if lep == "Electrons":
                        continue
                c1.cd()
                orthOpt = [True, False] if lep == "Muons" else [False]
                orth_cond = " && (leptons%%%[1].Pt() <= 3.5 || deltaR%%% <= 0.3)"
                for orth in orthOpt:
                    c1.cd()
                    print("2l",lep,orth)
                
                    #weight = "{:.2f}".format(analysis_selections.luminosities[wanted_year]*1000) + " * passesUniversalSelection * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * Weight * BranchingRatio * (twoLeptons%%% == 1 " + (orth_cond if orth else "") + " && MinDeltaPhiMhtJets > 0.4 && MET >= 140 && MHT >= 220 && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && leptonFlavour%%% == \"" + lep + "\" && sameSign%%% == 0 && isoCr%%% == 0 && tautau%%%" + (mtautauveto if veto_tautau else "") + " )"
                    #weight = weight.replace("%%%", analysis_selections.jetIsos[lep])
                    histName = "bg2l" + lep + ("Orth" if orth else "")
                    if seperate_bg_methods:
                        histName += "Tautau"
                    #hist = utils.getHistogramFromTreeCustomBinsX(histName, c, "dilepBDT" + analysis_selections.jetIsos[lep], analysis_selections.binning["2l"][lep], weight, False)
                    #hist.Sumw2()
                    
                    #old_sum = hist.Integral()
                    #print("old number", old_sum)
                    
                    
                    conditions = analysis_selections.two_leptons_full_bdt_tautau_outside_mtautau_window_prediction
                    if orth:
                        conditions = analysis_selections.two_leptons_full_bdt_tautau_outside_mtautau_window_prediction_sos
                    weight = analysis_selections.getFullSimString(wanted_year, lep, conditions)
                    
                    observable = analysis_selections.dilepBDTString[wanted_year] + analysis_selections.jetIsos[lep]
                    
                    hist = None
                    if use_uniform_binning:
                        hist = utils.getHistogramFromTree(histName, c, observable, analysis_selections.uniform_binning_number, -1, 1, weight, False)
                    else:
                        hist = utils.getHistogramFromTreeCustomBinsX(histName, c, observable, analysis_selections.binning["2l"][lep], weight, False)
                    hist.Sumw2() 
                    
                    if partial_unblinding:
                        utils.scaleHistogram(hist, 1./partial_unblinding_portion, 0)
                    
                    new_sum = hist.Integral()
                    print("\n\nnew sum", new_sum)
                    #print("difference", old_sum-new_sum)
                    tfHist = None
                    tfHistName = histName + "_tfError"
                    if ignore_tf_errors:
                        if add_systematics:
                            tfHist = hist.Clone(tfHistName)
                            tfHist.Sumw2()
                            tfHist.SetDirectory(0)
                            utils.scaleHistogram(tfHist, analysis_selections.tautau_factors[wanted_year][lep][0]+analysis_selections.tautau_factors[wanted_year][lep][1], 0)
                        utils.scaleHistogram(hist, analysis_selections.tautau_factors[wanted_year][lep][0], 0)
                    else:
                        utils.scaleHistogram(hist, analysis_selections.tautau_factors[wanted_year][lep][0], analysis_selections.tautau_factors[wanted_year][lep][1])
                    if bg_2l_hist.get(histName) is None:
                        print("WTF!! histName", histName)
                        bg_2l_hist[histName] = hist
                    else:
                        bg_2l_hist[histName].Add(hist)
                    
                    if tfHist is not None:
                        if bg_2l_hist.get(tfHistName) is None:
                            print("WTF!! histName", tfHistName)
                            bg_2l_hist[tfHistName] = tfHist
                        else:
                            bg_2l_hist[tfHistName].Add(tfHist)   
            
            f.Close()#skip these backgrounds

    print("Getting signals...")
    
    
    ###this is the one we care about
    signal_hists = {}
    i = 0
    wanted_years = [wanted_year]
    binning_phase = wanted_year
    if wanted_year == "phase1":
        wanted_years = ["2017","2018"]
    print("\n\nwanted_year", wanted_year, "wanted_years", wanted_years)
    for wanted_year in wanted_years:
        signal_dir = signal_dirs[wanted_year]
        print("\nNow for year", wanted_year, "signal_dir", signal_dir)
        for filename in glob(signal_dir + "/*"+thing2grab+"*"):
            #continue
            print("Opening", filename)
            if sam:
                deltaM = utils.getPointFromSamFileName(filename)
            else:
                deltaM = utils.getPointFromFileName(filename)  
            #if deltaM != "mChipm140GeV_dm4p28GeV":
            #    continue
            print("deltaM=" + deltaM, filename)
            f = TFile(filename)
            tree = f.Get('tEvent')



            normsystweight = '*1.0' #this will be the weights that define the unitarity target
            for syst in systs_weightbased_nuni[2:]: normsystweight+='*'+syst+'Nom' 
            nomsystweight = '*1.0'
            for syst in (systs_weightbased)[2:]:    nomsystweight+='*'+syst+'Nom' 
            
            print('tree.GetDirectory()', tree.GetDirectory())
            
            for isyst, syst_weightbased in enumerate(systs_weightbased):
                if isyst in [0,1]: variations = ['Nom']
                else: variations = ['Up','Down']
                for variation in variations:
                    if isyst==0: 
                        systvar = normsystweight.replace(syst_weightbased+'Nom',syst_weightbased+variation)
                    else:
                        systvar = nomsystweight.replace(syst_weightbased+'Nom',syst_weightbased+variation)
                    
                    for lep in ["Muons", "Electrons"]:
                        c1.cd()
                    
                        if channel != "leptons":
                            
                            if variation=='Nom': 
                                if isyst==0: histName = deltaM + "1t" + lep + 'Norm'
                                else: histName = deltaM + "1t" + lep
                            else: histName = deltaM + "1t" + lep +'_'+syst_weightbased+variation
                            
                            
                            obs = analysis_selections.exTrackDilepBDTString[wanted_year] + analysis_selections.jetIsos[lep]
                            
                            
                            conditions = analysis_selections.ex_track_full_range_selections
                            
                            if lep == "Electrons":
                                conditions = analysis_selections.ex_track_full_range_selections_electrons
                            weight = analysis_selections.getFastSimString(wanted_year, lep, conditions)+systvar
                                                    
                            
                            
                                
                            if use_uniform_binning:
                                hist = utils.getHistogramFromTree(histName, tree, obs, analysis_selections.uniform_binning_number, -1, 1, weight, False)
                            else:
                                hist = utils.getHistogramFromTreeCustomBinsX(histName, tree, obs, analysis_selections.binning["1t"][binning_phase][lep], weight, False)
                            new_sum = hist.Integral()
                            print("new_sum", new_sum)
                            if partial_unblinding:
                                utils.scaleHistogram(hist, 1./partial_unblinding_portion, 0)
                            #print("difference", old_sum-new_sum)
                            if signal_hists.get(histName) is None:
                                signal_hists[histName] = hist
                            else:
                                signal_hists[histName].Add(hist)
                        
                        if channel != "tracks":
                            if skip_electrons and lep == "Electrons":
                                #print('skipping tree A3', tree.GetEntries())
                                continue
                            
                            orthOpt = [True, False] if lep == "Muons" else [False]
                            orth_cond = " && (leptons%%%[1].Pt() <= 3.5 || deltaR%%% <= 0.3)"
                            for orth in orthOpt:
                                c1.cd()
                                                         
                                if variation=='Nom': 
                                    if isyst==0: histName = deltaM + "2l" + lep + ("Orth" if orth else "")+'Norm'
                                    else: histName = deltaM + "2l" + lep + ("Orth" if orth else "")
                                else: histName = deltaM + "2l" + lep + ("Orth" if orth else "")+'_'+syst_weightbased+variation
                        
                                conditions = analysis_selections.two_leptons_full_bdt_conditions_outside_mtautau_window
                                if orth:
                                    conditions = analysis_selections.two_leptons_full_bdt_conditions_outside_mtautau_window_sos
                                #weight = analysis_selections.getFastSimString(wanted_year, lep, conditions)
                                weight = analysis_selections.getFastSimString(wanted_year, lep, conditions)+systvar
                                print('lepton weight', weight)
                                #print('really need to handle the universal selection thing')
                        
                                observable = analysis_selections.dilepBDTString[wanted_year] + analysis_selections.jetIsos[lep]
                            
                                hist = None
                                if use_uniform_binning:
                                    hist = utils.getHistogramFromTree(histName, tree, observable, analysis_selections.uniform_binning_number, -1, 1, weight, False)
                                else:
                                    print('hist and tree', histName, tree)
                                    hist = utils.getHistogramFromTreeCustomBinsX(histName, tree, observable, analysis_selections.binning["2l"][lep], weight, False)
                                    
                                hist.Sumw2()
                        
                        
                                #hist = utils.getHistogramFromTreeCustomBinsX(histName, tree, "dilepBDT" + analysis_selections.jetIsos[lep], analysis_selections.binning["2l"][lep], cuts, False)
                                #hist.Sumw2() 
        
                                new_sum = hist.Integral()
                                #print("difference", old_sum-new_sum)
                                #print("\n\n")
                        
                                #non-orth
                                #hist = utils.getHistogramFromTree(deltaM + "_2l", tree, "dilepBDT", 30, -0.6, 0.6, str(utils.LUMINOSITY) + "* passedMhtMet6pack * tEffhMetMhtRealXMht2016 * cuts * BranchingRatio * (MHT >= 220 &&  MET >= 200 && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && dilepBDT > 0.1)", True)
                                
                                if partial_unblinding:
                                    utils.scaleHistogram(hist, 1./partial_unblinding_portion, 0)
                                
                                if signal_hists.get(histName) is None:
                                    signal_hists[histName] = hist
                                else:
                                    signal_hists[histName].Add(hist)
            f.Close()
            i += 1
            if max_files > 0 and i >= max_files:
                break
    fnew.cd()
    print("\n\n\n=======================")
    print("signal_hists", signal_hists)
    print("bg_1t_hist", bg_1t_hist)
    print("bg_2l_hist", bg_2l_hist)
    print("data_1t_hist", data_1t_hist)
    for hist in signal_hists:
        print("Writing histogram signal_hists", hist)
        if 'Norm' in hist: continue
        #some systematic variations should preserve the normalization
        if signal_hists[hist].Integral()>0 and not ('Norm' in hist): 
            normhist = ('_'.join(hist.split('_')[:2])+'Norm').replace('Nom','Norm')
            print ('want to divide', hist, 'by', normhist)
            unitarity_factor = signal_hists[normhist].Integral()/signal_hists[hist].Integral()
            print('unitarity_factor', hist, unitarity_factor)
            signal_hists[hist].Scale(unitarity_factor)
        signal_hists[hist].Write()
    for hist in bg_1t_hist:
        print("Writing histogram bg_1t_hist", hist)
        bg_1t_hist[hist].Write()
    for hist in bg_2l_hist:
        print("Writing bg_2l_hist", hist)
        bg_2l_hist[hist].Write()
    for hist in data_1t_hist:
        print("Writing data_1t_hist", hist)
        data_1t_hist[hist].Write()
    for hist in data_2l_hist:
        print("Writing data_2l_hist", hist)
        data_2l_hist[hist].Write()
    print('just created', fnew.GetName())
    fnew.Close()
    print("End: " + datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    exit(0)
    
main()

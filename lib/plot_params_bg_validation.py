import sys
import os
import copy
import ROOT

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib"))

from plot_params_base import *

#######################################################################################################
############ SAME SIGN VALIDATION FOR CorrJetNoMultIso10_06 WITH/OUT LINE FITS AND WEIGHTS ############
#######################################################################################################

# here was dilepton_muons_bg_isocr_no_retag_CorrJetNoMultIso10_06_invmass
class dilepton_muons_bg_isocr_no_retag_CorrJetNoMultIso10_06_2016_same_sign(BaseParams):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_no_retag_CorrJetNoMultIso10_06_2016_same_sign.root"
    
    save_histrograms_to_file = True
    load_histrograms_from_file = True 
    
    bg_retag = False
    plot_signal = False
    plot_sc = True
    plot_data = False
    plot_overflow = False
    plot_ratio = True
    
    nostack = False
    normalise = True
    normalise_each_bg = False
    plot_error = True
    sc_label = "jet isolation sideband"
    ratio_label = "main"
    sc_ratio_label = "side"
    weightString = {
        #'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * puWeight * BranchingRatio",
        'MET' : "Weight * passesUniversalSelection * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * BranchingRatio",
    }
    
    cuts = [
        #"passedMhtMet6pack * tEffhMetMhtRealXMht2016 * Weight * BranchingRatio * (twoLeptons" + jetiso + " == 1 "  + (orth_cond if orth else "") +  " && MinDeltaPhiMhtJets > 0.4 && MET >= 140 && MHT >= 220 && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign" + jetiso + " == 0 && isoCr" + jetiso + (" >= 1" if isoCr else " == 0") + " && dilepBDT" + jetiso + " < 0 && leptonFlavour" + jetiso + " == \"" + lep + "\" && tautau" + jetiso + " == 0)"
        {"name":"none", "title": "None", "condition" : "(passedMhtMet6pack == 1 && passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 1 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
        #{"name":"loose", "title": "loose", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
        #{"name":"mtautau", "title": "mtautau > 200", "condition" : "(mtautau%%% > 200 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
        #{"name":"nmtautau", "title": "nmtautau < 0 or nmtautau > 160", "condition" : "((nmtautau%%% < 0 || nmtautau%%% > 160) && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
        #{"name":"nmtautau_inside", "title": "0 < nmtautau < 160 && BDT < 0", "condition" : "((nmtautau%%% < 160 && nmtautau%%% > 0) && dilepBDT%%% < 0 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
    ]
    injectJetIsoToCuts(cuts, "CorrJetNoMultIso10Dr0.6")
    
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/slim_sum/type_sum"
    

    histograms_defs = [
        
        { "obs" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 20, "units" : "BDT"},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        { "obs" : "closure_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,0,0.15,0.25,0.35,0.45,0.6,1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        { "obs" : "closure_new_bin_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,0,0.1,0.2,0.3,0.4,0.5,1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        
        
        { "obs" : "closure_dilepBDTphase1_fine%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT output", "bins" : 20},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        { "obs" : "closure_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT output", "customBins"  : [-1,0,0.1,0.2,0.3,0.4,0.5,1], "linearYspace" : 1.6},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        #{ "obs" : "closure_2017_binning_even_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,1]},
        #{ "obs" : "closure_2017_binning_even_tight_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,1]},
        #{ "obs" : "closure_2017_binning_even_wider_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.1,0.2,0.3,0.4,0.45,1]},
        #{ "obs" : "closure_2017_binning_different_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.05,0.15,0.25,0.35,0.45,1]},
        #{ "obs" : "closure_2017_binning_even_wider_tighter_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.1,0.2,0.3,0.4,0.5,1]},
        #{ "obs" : "closure_2017_binning_even_wider_tighter_2_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.1,0.2,0.3,0.4,0.45,0.55,1]},
        #{ "obs" : "closure_2017_binning_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.1,0.3,0.4,0.45,1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        
        
        
        
        #{ "obs" : "closure_newer_bin_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,0,0.1,0.2,0.3,0.4,0.45,0.5,0.55,1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        #{ "obs" : "closure_newest_bin_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,0,0.1,0.2,0.3,0.4,0.45,0.5,1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        
        #{ "obs" : "fine_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 60, "units" : "BDT"},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        #{ "obs" : "coarse_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 6, "blind" : [None,0.1], "units" : "BDT"},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        #{ "obs" : "sideband_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 0, "bins" : 1, "blind" : [None,0.1], "units" : "BDT"},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        #{ "obs" : "custom_dilepBDT%%%", "formula" : "dilepBDT%%%","minX" : -1, "maxX" : 1, "bins" : 6, "units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.15,0.25,0.35,0.45,0.6,1] },
        #{ "obs" : "mtautau%%%", "linearYspace" : 1.5, "minX" : -300, "maxX" : 300, "bins" : 15},
        #{ "obs" : "nmtautau%%%", "linearYspace" : 1.5, "minX" : -300, "maxX" : 300, "bins" : 15},
        #{ "obs" : "coarse_nmtautau%%%", "formula" : "nmtautau%%%", "linearYspace" : 1.5, "minX" : 0, "maxX" : 160, "bins" : 15},
        #{ "obs" : "invMass%%%", "formula" : "invMass%%%", "minX" : 0, "maxX" : 12, "bins" : 6},
        
    ]
    injectJetIsoToHistograms(histograms_defs, "CorrJetNoMultIso10Dr0.6")
    plot_overflow = True
    fit_linear_ratio_plot = True
    calculatedLumi = {
        'MET' : 35.7389543,
    }
    normalise = True
    stamp_scale_factor = True
    
    fit_linear_ratio_plot = True    
    

class dilepton_muons_bg_isocr_no_retag_CorrJetNoMultIso10_06_2016_same_sign_no_norm_sf(dilepton_muons_bg_isocr_no_retag_CorrJetNoMultIso10_06_2016_same_sign):
    normalise = False
    
    transfer_factor = 0.539
    transfer_factor_error = 0
    transfer_factor = 0.477
    save_histrograms_to_file = True
    load_histrograms_from_file = True
    
    fit_linear_ratio_plot = True

class dilepton_muons_bg_isocr_no_retag_CorrJetNoMultIso10_06_2016_same_sign_no_norm_sf_line_weights(dilepton_muons_bg_isocr_no_retag_CorrJetNoMultIso10_06_2016_same_sign_no_norm_sf):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_no_retag_CorrJetNoMultIso10_06_2016_same_sign_no_norm_sf_line_weights.root"
    # weightString = {
#         'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * BranchingRatio * muonsClosureLineFitWeightCorrJetNoMultIso10Dr0.6",
#     }
    load_histrograms_from_file = True 
    
    cuts = [
        {"name":"none", "title": "None", "condition" : "(passedMhtMet6pack == 1 && passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 1 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1", "sc_weights" : "muonsClosureLineFitWeight%%%"},
    ]
    
    injectJetIsoToCuts(cuts, "CorrJetNoMultIso10Dr0.6")
    
    transfer_factor = 0.492
    transfer_factor_error = 0

    
class dilepton_muons_bg_isocr_no_retag_CorrJetNoMultIso10_06_2017_same_sign(dilepton_muons_bg_isocr_no_retag_CorrJetNoMultIso10_06_2016_same_sign):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_no_retag_CorrJetNoMultIso10_06_2017_same_sign.root"
    
    save_histrograms_to_file = True
    load_histrograms_from_file = True 
    
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_phase1/sum/slim_sum/type_sum"
    
    weightString = {
        #'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * puWeight * BranchingRatio",
        'MET' : "Weight * passesUniversalSelection * passedMhtMet6pack * tEffhMetMhtRealXMht2017 * BranchingRatio",
    }
    
    normalise = False
    transfer_factor = 0.810
    transfer_factor_error = 0
    
    histograms_defs = [
        
        
        
        { "obs" : "closure_dilepBDTphase1_fine%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "bins" : 20},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        { "obs" : "closure_dilepBDTphase1%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.1,0.2,0.3,0.5,1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        { "obs" : "closure_2017_binning_even_dilepBDTphase1%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,1]},
        #{ "obs" : "closure_2017_binning_even_tight_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,1]},
        { "obs" : "closure_2017_binning_even_wider_dilepBDTphase1%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.1,0.2,0.3,0.4,0.45,1]},
        #{ "obs" : "closure_2017_binning_even_wider_tighter_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.1,0.2,0.3,0.4,0.5,1]},
        #{ "obs" : "closure_2017_binning_even_wider_tighter_2_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.1,0.2,0.3,0.4,0.45,0.55,1]},
        { "obs" : "closure_2017_binning_dilepBDTphase1%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.1,0.3,0.4,0.45,1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
         
    ]
    injectJetIsoToHistograms(histograms_defs, "CorrJetNoMultIso10Dr0.6")
    
#################################################################################################################
############ DATA SAME SIGN VALIDATION FOR CorrJetNoMultIso10_06 WITH/OUT LINE FITS AND WEIGHTS 2016 ############
#################################################################################################################

class dilepton_muons_data_CorrJetNoMultIso10_06_2016_same_sign_no_norm_sf(dilepton_muons_bg_isocr_no_retag_CorrJetNoMultIso10_06_2016_same_sign_no_norm_sf):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_data_CorrJetNoMultIso10_06_2016_same_sign_no_norm_sf.root"
    
    cuts = [
        {"name":"none", "title": "None", "condition" : "(passedMhtMet6pack == 1 && passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 1 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
        {"name":"sos", "title": "SOS", "condition" : "(passedMhtMet6pack == 1 && passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 1 && (leptons%%%[1].Pt() <= 3.5 || deltaR%%% <= 0.3))", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
    ]
    injectJetIsoToCuts(cuts, "CorrJetNoMultIso10Dr0.6")
    save_histrograms_to_file = True
    load_histrograms_from_file = False
    
    plot_bg = False
    plot_data = True

    data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim/slim_sum"
    glob_data = False
    transfer_factor = 0.643
    transfer_factor_error = 0
    fit_linear_ratio_plot = True
    
    lumi_string_prefix = "[2016]"

class dilepton_muons_data_CorrJetNoMultIso10_06_2016_same_sign_no_norm_sf_line_weights(dilepton_muons_data_CorrJetNoMultIso10_06_2016_same_sign_no_norm_sf):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_data_CorrJetNoMultIso10_06_2016_same_sign_no_norm_sf_line_weights_new.root"
    load_histrograms_from_file = True
    cuts = [
        {"name":"none", "title": "None", "condition" : "(passedMhtMet6pack == 1 && passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 1 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1", "sc_weights" : "muonsClosureLineFitWeight%%%"},
        {"name":"sos", "title": "SOS", "condition" : "(passedMhtMet6pack == 1 && passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 1 && (leptons%%%[1].Pt() <= 3.5 || deltaR%%% <= 0.3))", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1", "sc_weights" : "muonsClosureLineFitWeight%%%"},
    ]
    injectJetIsoToCuts(cuts, "CorrJetNoMultIso10Dr0.6")
    
    weightString = {
        'MET' : "1",
    }
    applyWeightsToData = True
    transfer_factor = 0.656
    transfer_factor = 0.891
    transfer_factor_error = 0

##############################################################################################################
############ SAME SIGN VALIDATION FOR CorrJetNoMultIso10_06 WITH/OUT LINE FITS AND WEIGHTS PHASE1 ############
##############################################################################################################


# It used to inherit from dilepton_muons_bg_isocr_no_retag_CorrJetNoMultIso10_06_invmass
class dilepton_muons_bg_isocr_no_retag_CorrJetNoMultIso10_06_2017_same_sign_phase1(BaseParams):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_no_retag_CorrJetNoMultIso10_06_2017_same_sign_phase1.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = False
    plot_sc = True
    cuts = [
        #"passedMhtMet6pack * tEffhMetMhtRealXMht2016 * Weight * BranchingRatio * (twoLeptons" + jetiso + " == 1 "  + (orth_cond if orth else "") +  " && MinDeltaPhiMhtJets > 0.4 && MET >= 140 && MHT >= 220 && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign" + jetiso + " == 0 && isoCr" + jetiso + (" >= 1" if isoCr else " == 0") + " && dilepBDT" + jetiso + " < 0 && leptonFlavour" + jetiso + " == \"" + lep + "\" && tautau" + jetiso + " == 0)"
        {"name":"none", "title": "None", "condition" : "(passedMhtMet6pack == 1 && passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 1 )", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
        {"name":"sos", "title": "SOS", "condition" : "(passedMhtMet6pack == 1 && passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 1 && (leptons%%%[1].Pt() <= 3.5 || deltaR%%% <= 0.3))", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
        #{"name":"loose", "title": "loose", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
        #{"name":"mtautau", "title": "mtautau > 200", "condition" : "(mtautau%%% > 200 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
        #{"name":"nmtautau", "title": "nmtautau < 0 or nmtautau > 160", "condition" : "((nmtautau%%% < 0 || nmtautau%%% > 160) && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
        #{"name":"nmtautau_inside", "title": "0 < nmtautau < 160 && BDT < 0", "condition" : "((nmtautau%%% < 160 && nmtautau%%% > 0) && dilepBDT%%% < 0 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
    ]
    injectJetIsoToCuts(cuts, "CorrJetNoMultIso10Dr0.6")
    fit_linear_ratio_plot = False
    
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_phase1/sum/slim_sum/type_sum"
    
    weightString = {
        #'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * puWeight * BranchingRatio",
        'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2017 * BranchingRatio",
    }
    
    histograms_defs = [
        
        { "obs" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 20, "units" : "BDT", "linearYspace" : 1.8},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        { "obs" : "closure_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,0,0.1,0.30,0.4,0.45,0.5,1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        { "obs" : "closure_less_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,0,0.1,0.30,0.4,1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        #{ "obs" : "closure_new_bin_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,0,0.1,0.2,0.3,0.4,0.5,1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        #{ "obs" : "closure_newer_bin_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,0,0.1,0.2,0.3,0.4,0.45,0.5,0.55,1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        #{ "obs" : "closure_newest_bin_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,0,0.1,0.2,0.3,0.4,0.45,0.5,1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        
        #{ "obs" : "fine_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 60, "units" : "BDT"},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        #{ "obs" : "coarse_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 6, "blind" : [None,0.1], "units" : "BDT"},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        #{ "obs" : "sideband_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 0, "bins" : 1, "blind" : [None,0.1], "units" : "BDT"},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        #'0.10', '0.30', '0.40', '0.45'
       { "obs" : "custom_dilepBDT%%%", "formula" : "dilepBDT%%%","minX" : -1, "maxX" : 1, "bins" : 6, "units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.30,0.4,0.45,0.5,1] }, 
       { "obs" : "custom_less_dilepBDT%%%", "formula" : "dilepBDT%%%","minX" : -1, "maxX" : 1, "bins" : 6, "units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.30,0.4,1], "linearYspace" : 1.6 }, 
       { "obs" : "custom_less_dilepBDT2%%%", "formula" : "dilepBDT%%%","minX" : -1, "maxX" : 1, "bins" : 6, "units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,1], "linearYspace" : 1.6 }, 
        #{ "obs" : "mtautau%%%", "linearYspace" : 1.5, "minX" : -300, "maxX" : 300, "bins" : 15},
        #{ "obs" : "nmtautau%%%", "linearYspace" : 1.5, "minX" : -300, "maxX" : 300, "bins" : 15},
        #{ "obs" : "coarse_nmtautau%%%", "formula" : "nmtautau%%%", "linearYspace" : 1.5, "minX" : 0, "maxX" : 160, "bins" : 15},
        #{ "obs" : "invMass%%%", "formula" : "invMass%%%", "minX" : 0, "maxX" : 12, "bins" : 6},
        
    ]
    injectJetIsoToHistograms(histograms_defs, "CorrJetNoMultIso10Dr0.6")
    normalise = False
    stamp_scale_factor = False
    transfer_factor = 0.81
    transfer_factor_error = 0
    sc_label = "isolation sideband"
    ratio_label = "main"
    sc_ratio_label = "side"
    plot_ratio = True
    legend_coordinates = {"x1" : .40, "y1" : .7, "x2" : .94, "y2" : .90}
    legend_text_size = 0.08
    legend_columns = 1
    label_text = plotutils.StampStr.PRE

class dilepton_muons_data_isocr_no_retag_CorrJetNoMultIso10_06_invmass_same_sign_2017(dilepton_muons_bg_isocr_no_retag_CorrJetNoMultIso10_06_2017_same_sign_phase1):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_data_isocr_no_retag_CorrJetNoMultIso10_06_invmass_same_sign_2017.root"
    plot_bg = False
    plot_data = True
    plot_signal = False
    save_histrograms_to_file = True
    load_histrograms_from_file = False
    data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim_phase1/slim_2017"
    glob_data = False
    transfer_factor = 0.438
    transfer_factor_error = 0
    calculatedLumi = {
       'MET' : 41.4,
    }
    fit_linear_ratio_plot = False
    lumi_string_prefix = "[2017]"

class dilepton_muons_data_isocr_no_retag_CorrJetNoMultIso10_06_invmass_same_sign_2017F(dilepton_muons_data_isocr_no_retag_CorrJetNoMultIso10_06_invmass_same_sign_2017):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_data_isocr_no_retag_CorrJetNoMultIso10_06_invmass_same_sign_2017F.root"
    data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim_phase1/slim_2017F"
    transfer_factor = 0.381
    transfer_factor_error = 0
    calculatedLumi = {
       'MET' : 13.4,
    }
    calculatedLumi = {
       'MET' : 41.4,
    }
    lumi_string_prefix = "[2017F]"
    calculatedLumi = {
       'MET' : 13.4,
    }
    

class dilepton_muons_data_isocr_no_retag_CorrJetNoMultIso10_06_invmass_same_sign_2017F_prefire(dilepton_muons_data_isocr_no_retag_CorrJetNoMultIso10_06_invmass_same_sign_2017):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_data_isocr_no_retag_CorrJetNoMultIso10_06_invmass_same_sign_2017F_prefire.root"
    load_histrograms_from_file = True
    data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim_phase1/slim_2017F"
    transfer_factor = 0.396
    transfer_factor_error = 0
    weightString = {
        #'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * puWeight * BranchingRatio",
        'MET' : "prefireWeight",
    }
    applyWeightsToData = True
    lumi_string_prefix = "[2017F - with prefire weights]"
    calculatedLumi = {
       'MET' : 13.4,
    }

class dilepton_muons_data_isocr_no_retag_CorrJetNoMultIso10_06_invmass_same_sign_2018A(dilepton_muons_data_isocr_no_retag_CorrJetNoMultIso10_06_invmass_same_sign_2017):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_data_isocr_no_retag_CorrJetNoMultIso10_06_invmass_same_sign_2018A.root"
    load_histrograms_from_file = True
    weightString = {
        #'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * puWeight * BranchingRatio",
        'MET' : "prefireWeight",
    }
    data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim_phase1/slim_2018A"
    transfer_factor = 0.453
    transfer_factor_error = 0
    lumi_string_prefix = "[2018A]"
    calculatedLumi = {
       'MET' : 13.8,
    }

class dilepton_muons_data_isocr_no_retag_CorrJetNoMultIso10_06_invmass_same_sign_2018CD(dilepton_muons_data_isocr_no_retag_CorrJetNoMultIso10_06_invmass_same_sign_2017):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_data_isocr_no_retag_CorrJetNoMultIso10_06_invmass_same_sign_2018CD.root"
    data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim_phase1/slim_2018CD"
    load_histrograms_from_file = True
    
    transfer_factor = 0.498
    transfer_factor_error = 0
    lumi_string_prefix = "[2018CD]"
    calculatedLumi = {
       'MET' : 38.2,
    }

class dilepton_muons_data_isocr_no_retag_CorrJetNoMultIso10_06_invmass_same_sign_2018CD_hem_veto(dilepton_muons_data_isocr_no_retag_CorrJetNoMultIso10_06_invmass_same_sign_2017):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_data_isocr_no_retag_CorrJetNoMultIso10_06_invmass_same_sign_2018CD_hem_veto.root"
    data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim_phase1/slim_2018CD"
    transfer_factor = 0.490
    transfer_factor_error = 0
    load_histrograms_from_file = True
    cuts = [
        #"passedMhtMet6pack * tEffhMetMhtRealXMht2016 * Weight * BranchingRatio * (twoLeptons" + jetiso + " == 1 "  + (orth_cond if orth else "") +  " && MinDeltaPhiMhtJets > 0.4 && MET >= 140 && MHT >= 220 && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign" + jetiso + " == 0 && isoCr" + jetiso + (" >= 1" if isoCr else " == 0") + " && dilepBDT" + jetiso + " < 0 && leptonFlavour" + jetiso + " == \"" + lep + "\" && tautau" + jetiso + " == 0)"
        {"name":"none", "title": "None", "condition" : "(passedMhtMet6pack == 1 && passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 1 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
        {"name":"hem_ej", "title": "HEM e+j", "condition" : "(hemFailureVetoJets == 1 && hemFailureVetoElectrons == 1 && passedMhtMet6pack == 1 && passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 1 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
        {"name":"hem_ejm", "title": "HEM e+j+m", "condition" : "(hemFailureVetoMuons == 1 && hemFailureVetoJets == 1 && hemFailureVetoElectrons == 1 && passedMhtMet6pack == 1 && passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 1 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
        
        #{"name":"loose", "title": "loose", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
        #{"name":"mtautau", "title": "mtautau > 200", "condition" : "(mtautau%%% > 200 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
        #{"name":"nmtautau", "title": "nmtautau < 0 or nmtautau > 160", "condition" : "((nmtautau%%% < 0 || nmtautau%%% > 160) && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
        #{"name":"nmtautau_inside", "title": "0 < nmtautau < 160 && BDT < 0", "condition" : "((nmtautau%%% < 160 && nmtautau%%% > 0) && dilepBDT%%% < 0 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
    ]
    injectJetIsoToCuts(cuts, "CorrJetNoMultIso10Dr0.6")
    lumi_string_prefix = "[2018CD - with HEM veto]"
    calculatedLumi = {
       'MET' : 38.2,
    }
    
class dilepton_muons_data_isocr_no_retag_CorrJetNoMultIso10_06_invmass_same_sign_phase1(dilepton_muons_data_isocr_no_retag_CorrJetNoMultIso10_06_invmass_same_sign_2017):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_data_isocr_no_retag_CorrJetNoMultIso10_06_invmass_same_sign_phase1.root"
    data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim_phase1/slim_sum"
    transfer_factor = 0.527
    transfer_factor_error = 0
    
    save_histrograms_to_file = True
    load_histrograms_from_file = True
    
    stamp_scale_factor = False
    
    lumi_string_prefix = "[Phase 1]"
    calculatedLumi = {
       'MET' : 101.3,
    }

class dilepton_muons_data_isocr_no_retag_CorrJetNoMultIso10_06_invmass_same_sign_phase0(dilepton_muons_data_isocr_no_retag_CorrJetNoMultIso10_06_invmass_same_sign_phase1):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_data_isocr_no_retag_CorrJetNoMultIso10_06_invmass_same_sign_phase0.root"
    data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim/slim_sum"
    transfer_factor = 0.868
    transfer_factor_error = 0
    
    save_histrograms_to_file = True
    load_histrograms_from_file = True
    
    stamp_scale_factor = False
    
    lumi_string_prefix = "[Phase 0]"
    calculatedLumi = {
       'MET' : 36.3
    }
    
    histograms_defs = [
        
        { "obs" : "dilepBDT%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "bins" : 20, "units" : "BDT", "linearYspace" : 1.8},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        { "obs" : "final_binning%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        { "obs" : "closure_dilepBDT%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,0,0.1,0.30,0.4,0.45,0.5,1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        { "obs" : "closure_less_dilepBDT%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,0,0.1,0.30,0.4,1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        #{ "obs" : "closure_new_bin_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,0,0.1,0.2,0.3,0.4,0.5,1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        #{ "obs" : "closure_newer_bin_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,0,0.1,0.2,0.3,0.4,0.45,0.5,0.55,1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        #{ "obs" : "closure_newest_bin_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,0,0.1,0.2,0.3,0.4,0.45,0.5,1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        
        #{ "obs" : "fine_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 60, "units" : "BDT"},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        #{ "obs" : "coarse_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 6, "blind" : [None,0.1], "units" : "BDT"},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        #{ "obs" : "sideband_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 0, "bins" : 1, "blind" : [None,0.1], "units" : "BDT"},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        #'0.10', '0.30', '0.40', '0.45'
       { "obs" : "custom_dilepBDT%%%", "formula" : "dilepBDTphase1%%%","minX" : -1, "maxX" : 1, "bins" : 6, "units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.30,0.4,0.45,0.5,1] }, 
       { "obs" : "custom_less_dilepBDT%%%", "formula" : "dilepBDTphase1%%%","minX" : -1, "maxX" : 1, "bins" : 6, "units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.30,0.4,1], "linearYspace" : 1.6 }, 
       { "obs" : "custom_less_dilepBDT2%%%", "formula" : "dilepBDTphase1%%%","minX" : -1, "maxX" : 1, "bins" : 6, "units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,1], "linearYspace" : 1.6 }, 
        #{ "obs" : "mtautau%%%", "linearYspace" : 1.5, "minX" : -300, "maxX" : 300, "bins" : 15},
        #{ "obs" : "nmtautau%%%", "linearYspace" : 1.5, "minX" : -300, "maxX" : 300, "bins" : 15},
        #{ "obs" : "coarse_nmtautau%%%", "formula" : "nmtautau%%%", "linearYspace" : 1.5, "minX" : 0, "maxX" : 160, "bins" : 15},
        #{ "obs" : "invMass%%%", "formula" : "invMass%%%", "minX" : 0, "maxX" : 12, "bins" : 6},
        
    ]
    injectJetIsoToHistograms(histograms_defs, "CorrJetNoMultIso10Dr0.6")
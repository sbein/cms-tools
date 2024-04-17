import sys
import os
import copy
import ROOT

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib"))

from plot_params_base import *
import analysis_selections

bgReTaggingFull = {
    "tc" : "tc * (!tautau)",
    "tautau" : "tautau",
    "other" : "other * (!tautau) * (!omega) * (!rho_0) * (!eta) * (!phi) * (!eta_prime) * (!j_psi) * (!upsilon_1) * (!upsilon_2)",
    "omega" : "omega",
    "rho" : "rho_0",
    "eta" : "eta",
    "phi" : "phi",
    "etaprime" : "eta_prime",
    "jpsi" : "j_psi",
    "upsilon1" : "upsilon_1",
    "upsilon2" : "upsilon_2",
    "nbody" : "n_body * (!tautau)",
    "scother" : "sc * (!tautau) * (!omega) * (!rho_0) * (!eta) * (!phi) * (!eta_prime) * (!j_psi) * (!upsilon_1) * (!upsilon_2)",
    "fake" : "(rf || ff)",
}

bgReTaggingCollected = {
    "tc" : "tc * (!tautau)",
    "tautau" : "tautau",
    "other" : "other * (!tautau) * (!omega) * (!rho_0) * (!eta) * (!phi) * (!eta_prime) * (!j_psi) * (!upsilon_1) * (!upsilon_2)",
    "resonances" : "(sc || omega || rho_0 || eta || phi || eta_prime || j_psi || upsilon_1 || upsilon_2)",
    "nbody" : "n_body * (!tautau)",
    "fake" : "(rf || ff)",
}

bgReTaggingCollectedNoTauTau = {
    "tc" : "tc * (!tautau)",
    #"tautau" : "tautau",
    "other" : "other * (!tautau) * (!omega) * (!rho_0) * (!eta) * (!phi) * (!eta_prime) * (!j_psi) * (!upsilon_1) * (!upsilon_2)",
    "resonances" : "(sc || omega || rho_0 || eta || phi || eta_prime || j_psi || upsilon_1 || upsilon_2)",
    "nbody" : "n_body * (!tautau)",
    "fake" : "(rf || ff)",
}

bgReTaggingCollectedNoTauTauCorrJetIso = {
    "tc" : "tcCorrJetIso15 * (!tautauCorrJetIso15)",
    #"tautau" : "tautau",
    "other" : "otherCorrJetIso15 * (!tautauCorrJetIso15) * (!omegaCorrJetIso15) * (!rho_0CorrJetIso15) * (!etaCorrJetIso15) * (!phiCorrJetIso15) * (!eta_primeCorrJetIso15) * (!j_psiCorrJetIso15) * (!upsilon_1CorrJetIso15) * (!upsilon_2CorrJetIso15)",
    "resonances" : "(scCorrJetIso15 || omegaCorrJetIso15 || rho_0CorrJetIso15 || etaCorrJetIso15 || phiCorrJetIso15 || eta_primeCorrJetIso15 || j_psiCorrJetIso15 || upsilon_1CorrJetIso15 || upsilon_2CorrJetIso15)",
    "nbody" : "n_bodyCorrJetIso15 * (!tautauCorrJetIso15)",
    "fake" : "(rfCorrJetIso15 || ffCorrJetIso15)",
}

bgReTaggingCollectedNoTauTauCorrJetIso15_04 = {
    "tc" : "tcCorrJetIso15Dr0.4 * (!tautauCorrJetIso15Dr0.4)",
    #"tautau" : "tautau",
    "other" : "otherCorrJetIso15Dr0.4 * (!tautauCorrJetIso15Dr0.4) * (!omegaCorrJetIso15Dr0.4) * (!rho_0CorrJetIso15Dr0.4) * (!etaCorrJetIso15Dr0.4) * (!phiCorrJetIso15Dr0.4) * (!eta_primeCorrJetIso15Dr0.4) * (!j_psiCorrJetIso15Dr0.4) * (!upsilon_1CorrJetIso15Dr0.4) * (!upsilon_2CorrJetIso15Dr0.4)",
    "resonances" : "(scCorrJetIso15Dr0.4 || omegaCorrJetIso15Dr0.4 || rho_0CorrJetIso15Dr0.4 || etaCorrJetIso15Dr0.4 || phiCorrJetIso15Dr0.4 || eta_primeCorrJetIso15Dr0.4 || j_psiCorrJetIso15Dr0.4 || upsilon_1CorrJetIso15Dr0.4 || upsilon_2CorrJetIso15Dr0.4)",
    "nbody" : "n_bodyCorrJetIso15Dr0.4 * (!tautauCorrJetIso15Dr0.4)",
    "fake" : "(rfCorrJetIso15Dr0.4 || ffCorrJetIso15Dr0.4)",
}

bgReTaggingCollectedNoTauTauCorrJetIso11_055 = {
    "tc" : "tcCorrJetIso11Dr0.55 * (!tautauCorrJetIso11Dr0.55)",
    #"tautau" : "tautau",
    "other" : "otherCorrJetIso11Dr0.55 * (!tautauCorrJetIso11Dr0.55) * (!omegaCorrJetIso11Dr0.55) * (!rho_0CorrJetIso11Dr0.55) * (!etaCorrJetIso11Dr0.55) * (!phiCorrJetIso11Dr0.55) * (!eta_primeCorrJetIso11Dr0.55) * (!j_psiCorrJetIso11Dr0.55) * (!upsilon_1CorrJetIso11Dr0.55) * (!upsilon_2CorrJetIso11Dr0.55)",
    "resonances" : "(scCorrJetIso11Dr0.55 || omegaCorrJetIso11Dr0.55 || rho_0CorrJetIso11Dr0.55 || etaCorrJetIso11Dr0.55 || phiCorrJetIso11Dr0.55 || eta_primeCorrJetIso11Dr0.55 || j_psiCorrJetIso11Dr0.55 || upsilon_1CorrJetIso11Dr0.55 || upsilon_2CorrJetIso11Dr0.55)",
    "nbody" : "n_bodyCorrJetIso11Dr0.55 * (!tautauCorrJetIso11Dr0.55)",
    "fake" : "(rfCorrJetIso11Dr0.55 || ffCorrJetIso11Dr0.55)",
}

bgReTaggingCollectedCorrJetIso11_055 = {
    "tautau" : "tautauCorrJetIso11Dr0.55",
    "other" : "!tautauCorrJetIso11Dr0.55"
}


bgReTaggingCollectedCorrJetIso15 = {
    "tc" : "tcCorrJetIso15 * (!tautauCorrJetIso15)",
    "tautau" : "tautauCorrJetIso15",
    "other" : "otherCorrJetIso15 * (!tautauCorrJetIso15) * (!omegaCorrJetIso15) * (!rho_0CorrJetIso15) * (!etaCorrJetIso15) * (!phiCorrJetIso15) * (!eta_primeCorrJetIso15) * (!j_psiCorrJetIso15) * (!upsilon_1CorrJetIso15) * (!upsilon_2CorrJetIso15)",
    "resonances" : "(scCorrJetIso15 || omegaCorrJetIso15 || rho_0CorrJetIso15 || etaCorrJetIso15 || phiCorrJetIso15 || eta_primeCorrJetIso15 || j_psiCorrJetIso15 || upsilon_1CorrJetIso15 || upsilon_2CorrJetIso15)",
    "nbody" : "n_bodyCorrJetIso15 * (!tautauCorrJetIso15)",
    "fake" : "(rfCorrJetIso15 || ffCorrJetIso15)",
}

bgReTaggingCollectedNoTauTauCorrJetIso10 = {
    "tc" : "tcCorrJetIso10 * (!tautauCorrJetIso10)",
    #"tautau" : "tautau",
    "other" : "otherCorrJetIso10 * (!tautauCorrJetIso10) * (!omegaCorrJetIso10) * (!rho_0CorrJetIso10) * (!etaCorrJetIso10) * (!phiCorrJetIso10) * (!eta_primeCorrJetIso10) * (!j_psiCorrJetIso10) * (!upsilon_1CorrJetIso10) * (!upsilon_2CorrJetIso10)",
    "resonances" : "(scCorrJetIso10 || omegaCorrJetIso10 || rho_0CorrJetIso10 || etaCorrJetIso10 || phiCorrJetIso10 || eta_primeCorrJetIso10 || j_psiCorrJetIso10 || upsilon_1CorrJetIso10 || upsilon_2CorrJetIso10)",
    "nbody" : "n_bodyCorrJetIso10 * (!tautauCorrJetIso10)",
    "fake" : "(rfCorrJetIso10 || ffCorrJetIso10)",
}

bgReTaggingCollectedCorrJetIso10 = {
    "tc" : "tcCorrJetIso10 * (!tautauCorrJetIso10)",
    "tautau" : "tautauCorrJetIso10",
    "other" : "otherCorrJetIso10 * (!tautauCorrJetIso10) * (!omegaCorrJetIso10) * (!rho_0CorrJetIso10) * (!etaCorrJetIso10) * (!phiCorrJetIso10) * (!eta_primeCorrJetIso10) * (!j_psiCorrJetIso10) * (!upsilon_1CorrJetIso10) * (!upsilon_2CorrJetIso10)",
    "resonances" : "(scCorrJetIso10 || omegaCorrJetIso10 || rho_0CorrJetIso10 || etaCorrJetIso10 || phiCorrJetIso10 || eta_primeCorrJetIso10 || j_psiCorrJetIso10 || upsilon_1CorrJetIso10 || upsilon_2CorrJetIso10)",
    "nbody" : "n_bodyCorrJetIso10 * (!tautauCorrJetIso10)",
    "fake" : "(rfCorrJetIso10 || ffCorrJetIso10)",
}

bgReTaggingResonances = {
    #"tc" : "tc * (!tautau)",
    #"tautau" : "tautau",
    #"other" : "other * (!tautau) * (!omega) * (!rho_0) * (!eta) * (!phi) * (!eta_prime) * (!j_psi) * (!upsilon_1) * (!upsilon_2)",
    "omega" : "omega",
    "rho" : "rho_0",
    "eta" : "eta",
    "phi" : "phi",
    "etaprime" : "eta_prime",
    "jpsi" : "j_psi",
    "upsilon1" : "upsilon_1",
    "upsilon2" : "upsilon_2",
    "nbody" : "n_body * (!tautau)",
    "scother" : "sc * (!tautau) * (!omega) * (!rho_0) * (!eta) * (!phi) * (!eta_prime) * (!j_psi) * (!upsilon_1) * (!upsilon_2)",
    #"fake" : "(rf || ff)",
}

bgReTaggingOrderFull = {
    "resonances" : -3,
    "tautau" : -2,
    "other" : -1,
    "omega" : 0,
    "rho" : 1,
    "eta" : 2,
    "phi" : 3,
    "etaprime" : 4,
    "jpsi" : 5,
    "upsilon1" : 6,
    "upsilon2" : 7,
    "tc" : 8,
    "nbody" : 9,
    "scother" : 10,
    "fake" : 11
}

bgReTaggingNamesFull = {
    "resonances" : "resonances",
    "tautau" : "#tau#tau",
    "other" : "no information",
    "omega" : "#omega",
    "rho" : "#rho",
    "eta" : "#eta",
    "phi" : "#phi",
    "etaprime" : "#eta^{}'",
    "jpsi" : "J/#psi",
    "upsilon1" : "#Upsilon(1s)",
    "upsilon2" : "#Upsilon(2s)",
    "tc" : "no common parent",
    "nbody" : "n-body",
    "scother" : "other resonances",
    "fake" : "fake"
}

basic_histograms_defs = [
        { "obs" : "invMass%%%", "minX" : 0, "maxX" : 13, "bins" : 6, "blind" : [4,None], "units" : "M_{ll} [GeV]"},# "customBins"  : [0,2,4,6,10,12] },
        { "obs" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 6, "blind" : [None,0.1], "units" : "BDT"},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        { "obs" : "dilepBDT%%%_mid", "formula" : "dilepBDT%%%","minX" : -1, "maxX" : 1, "bins" : 12, "blind" : [None,0.1], "units" : "BDT", "linearYspace" : 1.5},
        { "obs" : "dilepBDT%%%_fine", "formula" : "dilepBDT%%%","minX" : -1, "maxX" : 1, "bins" : 24, "blind" : [None,0.1], "units" : "BDT"},
        #{ "obs" : "dilepBDT%%%_custom", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 6, "blind" : [None,0.1], "customBins"  : [-1,-0.6,-0.3,0,0.10,0.26,0.34,0.38,0.42,1] },
        { "obs" : "deltaR%%%", "minX" : 0, "maxX" : 3.5, "bins" : 8, "units" : "\Delta_{}R"},
        { "obs" : "dilepHt%%%", "minX" : 200, "maxX" : 800, "bins" : 8},
        { "obs" : "dileptonPt%%%", "minX" : 0, "maxX" : 30, "bins" : 8, "units" : "p_T(ll) [GeV]"},
        { "obs" : "MHT", "minX" : 220, "maxX" : 800, "bins" : 8},
        { "obs" : "MET", "minX" : 200, "maxX" : 800, "bins" : 8},
        { "obs" : "MinDeltaPhiMhtJets", "minX" : 0, "maxX" : 3.5, "bins" : 8, "units" : "Min\Delta_{}\phi(H_{T}^{Miss}, Jets)"},
        { "obs" : "leptons%%%[0].Pt()", "minX" : 0, "maxX" : 20, "bins" : 8, "units" : "p_{T}(l_{1}) [GeV]"},
        { "obs" : "deltaPhiMetLepton1%%%", "minX" : 0, "maxX" : 3.5, "bins" : 8, "units" : "\Delta\phi(H_{T}^{Miss},l_{1})"},
        { "obs" : "mt1%%%", "minX" : 0, "maxX" : 200, "bins" : 8, "units" : "m_{T}(l_{1}) [GeV]"},
        { "obs" : "leptons%%%[0].Eta()", "minX" : -2.4, "maxX" : 2.4, "bins" : 8},
        { "obs" : "NJets", "minX" : 0, "maxX" : 6, "bins" : 6},
        { "obs" : "deltaPhiMetLepton2%%%", "minX" : 0, "maxX" : 3.5, "bins" : 8, "units" : "\Delta\phi(H_{T}^{Miss},l_{2})"},
        { "obs" : "LeadingJetPt", "minX" : 0, "maxX" : 500, "bins" : 8},
        { "obs" : "LeadingJet.Eta()", "minX" : -2.4, "maxX" : 2.4, "bins" : 8},
        { "obs" : "deltaEta%%%", "minX" : 0, "maxX" : 5, "bins" : 8, "units" : "\Delta_{}\eta"},
        { "obs" : "HT", "minX" : 0, "maxX" : 500, "bins" : 8},
        { "obs" : "leptons%%%[0].Phi()", "minX" : 0, "maxX" : 3.5, "bins" : 8},
     ]
    
notautau_cuts = [
        {"name":"none", "title": "None", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
        {"name":"mtautau", "title": "mtautau > 200", "condition" : "(mtautau%%% > 200 & MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
    ]

class dilepton_muons_bg_isocr_no_retag(BaseParams):
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/slim_sum/type_sum"
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = False 
    bg_retag = False
    plot_signal = False
    plot_sc = True
    plot_data = False
    plot_overflow = False
    plot_ratio = True
    blind_data = True
    subtract_same_charge = False
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

class dilepton_muons_bg_isocr_no_retag_CorrJetIso10_06(dilepton_muons_bg_isocr_no_retag):
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/slim_sum/type_sum"
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_no_retag_CorrJetIso10_06.root"
    cuts = copy.deepcopy(notautau_cuts)
    injectJetIsoToCuts(cuts, "CorrJetIso10Dr0.6")
    histograms_defs = copy.deepcopy(basic_histograms_defs)
    injectJetIsoToHistograms(histograms_defs, "CorrJetIso10Dr0.6")
    
    
class dilepton_muons_bg_isocr_no_retag_CorrJetIso10_06_no_norm(dilepton_muons_bg_isocr_no_retag_CorrJetIso10_06):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_no_retag_CorrJetIso10_06.root"
    normalise = False

class dilepton_muons_bg_isocr_no_retag_CorrJetIso10_5_55(dilepton_muons_bg_isocr_no_retag):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_no_retag_CorrJetIso10_5_55.root"
    cuts = copy.deepcopy(notautau_cuts)
    injectJetIsoToCuts(cuts, "CorrJetIso10.5Dr0.55")
    histograms_defs = copy.deepcopy(basic_histograms_defs)
    injectJetIsoToHistograms(histograms_defs, "CorrJetIso10.5Dr0.55")
    save_histrograms_to_file = True
    load_histrograms_from_file = True 

class dilepton_muons_bg_isocr_no_retag_CorrJetIso10_5_55_bdt_only(dilepton_muons_bg_isocr_no_retag_CorrJetIso10_5_55):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_no_retag_CorrJetIso10_5_55_bdt_only.root"
    
    save_histrograms_to_file = True
    load_histrograms_from_file = True 
    
    cuts = [
        {"name":"none", "title": "None", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
        {"name":"loose", "title": "loose", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
        #{"name":"mtautau", "title": "mtautau > 200", "condition" : "(mtautau%%% > 200 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
        {"name":"nmtautau", "title": "nmtautau < 0 or nmtautau > 160", "condition" : "((nmtautau%%% < 0 || nmtautau%%% > 160) && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
        {"name":"nmtautau_inside", "title": "0 < nmtautau < 160 && BDT < 0", "condition" : "((nmtautau%%% < 160 && nmtautau%%% > 0) && dilepBDT%%% < 0 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
    ]
    injectJetIsoToCuts(cuts, "CorrJetIso10.5Dr0.55")

    histograms_defs = [
        
        { "obs" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 20, "blind" : [None,0.1], "units" : "BDT"},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        { "obs" : "coarse_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 4, "blind" : [None,0.1], "units" : "BDT"},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        { "obs" : "sideband_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 0, "bins" : 1, "blind" : [None,0.1], "units" : "BDT"},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        { "obs" : "custom_dilepBDT%%%", "formula" : "dilepBDT%%%","minX" : -1, "maxX" : 1, "bins" : 6, "units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,1] },
        { "obs" : "mtautau%%%", "linearYspace" : 1.5, "minX" : -300, "maxX" : 300, "bins" : 15},
        { "obs" : "nmtautau%%%", "linearYspace" : 1.5, "minX" : -300, "maxX" : 300, "bins" : 15},
        { "obs" : "coarse_nmtautau%%%", "formula" : "nmtautau%%%", "linearYspace" : 1.5, "minX" : 0, "maxX" : 160, "bins" : 15},
        
    ]
    injectJetIsoToHistograms(histograms_defs, "CorrJetIso10.5Dr0.55")
    plot_overflow = True

####################################################################################################
############ CLOSURE PLOT SCAN FOR CorrJetNoMultIso10_06 WITH/OUT LINE FITS AND WEIGHTS ############
####################################################################################################

# index_to_optimise = 1
# ===========
# 2l_Muons
# ['-1.00', '-1.00', '-0.05', '0.00', '0.05', '0.20', '0.25', '0.35', '0.45', '0.60']
# ===========
# 2l_Electrons
# ['-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '0.10', '0.20', '0.30']
# index_to_optimise = 2
# ===========
# 2l_Muons
# ['-0.25', '-0.20', '0.05', '0.20', '0.25', '0.30', '0.35', '0.40', '0.45', '0.55']
# ===========
# 2l_Electrons
# ['-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '0.10', '0.20', '0.30']
# index_to_optimise = 3
# ===========
# 2l_Muons
# ['-1.00', '-1.00', '-1.00', '-0.45', '0.00', '0.15', '0.20', '0.25', '0.35', '0.45']
# ===========
# 2l_Electrons
# ['-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '0.15']
# index_to_optimise = 4
# ===========
# 2l_Muons
# ['-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-0.05', '0.35', '0.40', '0.50']
# ===========
# 2l_Electrons
# ['-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00', '-1.00']

class dilepton_muons_bg_isocr_no_retag_CorrJetNoMultIso10_06_2016(dilepton_muons_bg_isocr_no_retag_CorrJetIso10_5_55):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_no_retag_CorrJetIso10_06_2016_check.root"
    
    save_histrograms_to_file = True
    load_histrograms_from_file = False 
    
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/slim_sum/type_sum"
    
    cuts = [
        {"name":"none", "title": "None", "condition" : "(passedMhtMet6pack == 1 && passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
        #{"name":"loose", "title": "loose", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
        #{"name":"mtautau", "title": "mtautau > 200", "condition" : "(mtautau%%% > 200 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
        #{"name":"nmtautau", "title": "nmtautau < 0 or nmtautau > 160", "condition" : "((nmtautau%%% < 0 || nmtautau%%% > 160) && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
        #{"name":"nmtautau_inside", "title": "0 < nmtautau < 160 && BDT < 0", "condition" : "((nmtautau%%% < 160 && nmtautau%%% > 0) && dilepBDT%%% < 0 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
    ]
    injectJetIsoToCuts(cuts, "CorrJetNoMultIso10Dr0.6")

    histograms_defs = [
        
        { "obs" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 20, "units" : "BDT"},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        { "obs" : "closure_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,0,0.15,0.25,0.35,0.45,0.6,1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        { "obs" : "closure_new_bin_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,0,0.1,0.2,0.3,0.4,0.5,1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        
        { "obs" : "closure_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.1,0.2,0.3,0.4,0.5,1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },

        { "obs" : "closure_2017_binning_even_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,1]},
        #{ "obs" : "closure_2017_binning_even_tight_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,1]},
        { "obs" : "closure_2017_binning_even_wider_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.1,0.2,0.3,0.4,0.45,1]},
        { "obs" : "closure_2017_binning_different_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.05,0.15,0.25,0.35,0.45,1]},
        #{ "obs" : "closure_2017_binning_even_wider_tighter_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.1,0.2,0.3,0.4,0.5,1]},
        #{ "obs" : "closure_2017_binning_even_wider_tighter_2_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.1,0.2,0.3,0.4,0.45,0.55,1]},
        { "obs" : "closure_2017_binning_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.1,0.3,0.4,0.45,1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        
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

class dilepton_muons_bg_isocr_no_retag_CorrJetNoMultIso10_06_2016_no_norm_sf(dilepton_muons_bg_isocr_no_retag_CorrJetNoMultIso10_06_2016):
    normalise = False
    transfer_factor = 0.576
    transfer_factor_error = 0.05
    transfer_factor_error = 0.0
    
    transfer_factor = 0.618
    
    save_histrograms_to_file = True
    load_histrograms_from_file = False
    calculatedLumi = {
        'MET' : 35.7389543,
    }
    fit_linear_ratio_plot = True

    
class dilepton_muons_bg_isocr_no_retag_CorrJetNoMultIso10_06_2016_no_norm_sf_line_fit_line_weights(dilepton_muons_bg_isocr_no_retag_CorrJetNoMultIso10_06_2016_no_norm_sf):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_no_retag_CorrJetNoMultIso10_06_2016_no_norm_sf_line_fit_line_weights.root"
    
    cuts = [
        {"name":"none", "title": "None", "condition" : "(passedMhtMet6pack == 1 && passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1", "sc_weights" : "muonsClosureLineFitWeight%%%"},
    ]
    injectJetIsoToCuts(cuts, "CorrJetNoMultIso10Dr0.6")
    save_histrograms_to_file = True
    load_histrograms_from_file = True
    transfer_factor = 0.629


class dilepton_muons_bg_isocr_no_retag_CorrJetNoMultIso10_06_2017(dilepton_muons_bg_isocr_no_retag_CorrJetNoMultIso10_06_2016):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_no_retag_CorrJetNoMultIso10_06_2017.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = True  
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_phase1/sum/slim_sum/type_sum"
    weightString = {
        'MET' : "Weight * passesUniversalSelection * passedMhtMet6pack * tEffhMetMhtRealXMht2017 * BranchingRatio",
    }
    
    histograms_defs = [
        
        { "obs" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 20, "units" : "BDT output", "linearYspace" : 1.6},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        #{ "obs" : "closure_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,0,0.15,0.25,0.35,0.45,0.6,1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        #{ "obs" : "closure_new_bin_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,0,0.1,0.2,0.3,0.4,0.5,1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        
        { "obs" : "closure_dilepBDTphase1%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT output", "linearYspace" : 1.6, "customBins"  : [-1,0,0.1,0.2,0.3,0.4,0.5,1], "ratio1max" : 2.5}
        #{ "obs" : "closure_2017_binning_even_dilepBDTphase1%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,1]},
        #{ "obs" : "closure_2017_binning_even_tight_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,1]},
        #{ "obs" : "closure_2017_binning_even_wider_dilepBDTphase1%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.1,0.2,0.3,0.4,0.45,1]},
        #{ "obs" : "closure_2017_binning_reversed_dilepBDTphase1%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.05,0.15,0.25,0.35,0.45,1]},
        #{ "obs" : "closure_2017_binning_even_wider_tighter_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.1,0.2,0.3,0.4,0.5,1]},
        #{ "obs" : "closure_2017_binning_even_wider_tighter_2_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.1,0.2,0.3,0.4,0.45,0.55,1]},
        #{ "obs" : "closure_2017_binning_dilepBDTphase1%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.1,0.3,0.4,0.45,1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        
        
    ]
    injectJetIsoToHistograms(histograms_defs, "CorrJetNoMultIso10Dr0.6")
    fit_linear_ratio_plot = True
    calculatedLumi = {
        'MET' : analysis_selections.luminosities["2017"],
    }
    normalise = False
    
    transfer_factor = 0.588
    transfer_factor_error = 0
    label_text = plotutils.StampStr.SIM
    stamp_scale_factor = False

class dilepton_muons_bg_isocr_no_retag_CorrJetNoMultIso10_06_2017_no_norm_sf_line_fit_line_weights(dilepton_muons_bg_isocr_no_retag_CorrJetNoMultIso10_06_2017):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_no_retag_CorrJetNoMultIso10_06_2017_no_norm_sf_line_fit_line_weights.root"
    
    cuts = [
        {"name":"none", "title": "None", "condition" : "(passedMhtMet6pack == 1 && passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1", "sc_weights" : "muonsClosureLineFitWeight%%%"},
    ]
    injectJetIsoToCuts(cuts, "CorrJetNoMultIso10Dr0.6")
    save_histrograms_to_file = True
    load_histrograms_from_file = True
    transfer_factor = 0.547

class dilepton_muons_bg_isocr_no_retag_CorrJetNoMultIso10_06_2018(dilepton_muons_bg_isocr_no_retag_CorrJetNoMultIso10_06_2016):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_no_retag_CorrJetNoMultIso10_06_2018.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = True 
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_phase1/sum/slim_sum/type_sum"
    weightString = {
        'MET' : "Weight * passesUniversalSelection * passedMhtMet6pack * tEffhMetMhtRealXMht2018 * BranchingRatio * hemFailureVetoElectrons * hemFailureVetoJets * hemFailureVetoMuons",
    }
    
    histograms_defs = [
        
        { "obs" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 20, "units" : "BDT"},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        #{ "obs" : "closure_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,0,0.15,0.25,0.35,0.45,0.6,1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        #{ "obs" : "closure_new_bin_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,0,0.1,0.2,0.3,0.4,0.5,1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        
        { "obs" : "closure_dilepBDTphase1%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.1,0.2,0.3,0.5,1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        { "obs" : "closure_2017_binning_even_dilepBDTphase1%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,1]},
        #{ "obs" : "closure_2017_binning_even_tight_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,1]},
        { "obs" : "closure_2017_binning_even_wider_dilepBDTphase1%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.1,0.2,0.3,0.4,0.45,1]},
        #{ "obs" : "closure_2017_binning_even_wider_tighter_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.1,0.2,0.3,0.4,0.5,1]},
        #{ "obs" : "closure_2017_binning_even_wider_tighter_2_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.1,0.2,0.3,0.4,0.45,0.55,1]},
        { "obs" : "closure_2017_binning_dilepBDTphase1%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,0,0.1,0.3,0.4,0.45,1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        
        
    ]
    injectJetIsoToHistograms(histograms_defs, "CorrJetNoMultIso10Dr0.6")
    fit_linear_ratio_plot = True
    calculatedLumi = {
        'MET' : analysis_selections.luminosities["2018"],
    }
    normalise = False
    
    transfer_factor = 0.588
    transfer_factor_error = 0
    
###############################################################
############ CLOSURE PLOT SCAN FOR ALL ISO OPTIONS ############
###############################################################

class dilepton_muons_bg_isocr_no_retag_scan(dilepton_muons_bg_isocr_no_retag_CorrJetIso10_5_55):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_no_retag_scan2.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = False 
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/slim_sum/type_sum"
    cuts = [
        {"name":"none", "title": "None", "condition" : "1", "baseline" : "1", "sc" : "1"},
        #{"name":"bdt", "title": "BDT > 0.35", "condition" : "(dilepBDT%%% > 0.35 &&  MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 200 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
    ]
    histograms_defs = [
    
    ]
    
    for iso in utils.leptonIsolationList:
        for cat in utils.leptonIsolationCategories:
            ptRanges = [""]
            drCuts = [""]
            #if iso == "CorrJetIso":
            if iso == "CorrJetNoMultIso":
                ptRanges = utils.leptonCorrJetIsoPtRange
                drCuts = utils.leptonCorrJetIsoDrCuts
            else:
                continue
            for ptRange in ptRanges:
                if ptRange < 9:
                    continue
                for drCut in drCuts:
                    jetIso = ""
                    if len(str(ptRange)) > 0:
                        jetIso = iso + str(ptRange) + "Dr" + str(drCut) + cat
                    else:
                        continue
                    #for obs in ["invMass", "dilepBDT"]:
                    for obs in ["dilepBDT", "dilepBDT_fine", "dilepBDT_custom"]:
                    #for obs in ["dilepBDT_fine"]:
                        #{ "obs" : "invMassCorrJetIso15Dr0.4", "minX" : 0, "maxX" : 13, "bins" : 6, "blind" : [4,None]}
                        hist_def = { "obs" : obs + "%%%", "formula" : "dilepBDT%%%" if "dilepBDT" in obs else (obs + "%%%"), "linearYspace" : 1.5, "minX" : 0 if obs == "invMass" else -1, "maxX" : 13 if obs == "invMass" else 1, "bins" : 40 if obs == "dilepBDT_fine" else 20, "blind" : [None, 0], "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.45,0.5,0.55,1] if obs == "dilepBDT_custom" else None,  "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"}
                        #print(hist_def["obs"],jetIso)
                        #print(hist_def["obs"].replace("%%%", jetIso))
                        #print(hist_def["obs"])
                        hist_def["obs"] = hist_def["obs"].replace("%%%", jetIso)
                        hist_def["formula"] = hist_def["formula"].replace("%%%", jetIso)
                        #print(hist_def["obs"])
                        #exit(0)
                        hist_def["condition"] = hist_def["condition"].replace("%%%", jetIso)
                        hist_def["baseline"] = hist_def["baseline"].replace("%%%", jetIso)
                        hist_def["sc"] = hist_def["sc"].replace("%%%", jetIso)
                        histograms_defs.append(hist_def)

class dilepton_muons_bg_isocr_no_retag_scan_with_phase1_bdt(dilepton_muons_bg_isocr_no_retag_scan):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_no_retag_scan_with_phase1_bdt.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = False 
    
    histograms_defs = [
    
    ]
    
    for iso in utils.leptonIsolationList:
        for cat in utils.leptonIsolationCategories:
            ptRanges = [""]
            drCuts = [""]
            #if iso == "CorrJetIso":
            if iso == "CorrJetNoMultIso":
                ptRanges = utils.leptonCorrJetIsoPtRange
                drCuts = utils.leptonCorrJetIsoDrCuts
            else:
                continue
            for ptRange in ptRanges:
                if ptRange < 9:
                    continue
                if ptRange > 11:
                    continue
                for drCut in drCuts:
                    jetIso = ""
                    if len(str(ptRange)) > 0:
                        jetIso = iso + str(ptRange) + "Dr" + str(drCut) + cat
                    else:
                        continue
                    #for obs in ["invMass", "dilepBDT"]:
                    for obs in ["dilepBDT", "dilepBDT_fine", "dilepBDT_custom", "dilepBDTphase1", "dilepBDTphase1_fine", "dilepBDTphase1_custom"]:
                    #for obs in ["dilepBDT_fine"]:
                        #{ "obs" : "invMassCorrJetIso15Dr0.4", "minX" : 0, "maxX" : 13, "bins" : 6, "blind" : [4,None]}
                        hist_def = { "obs" : obs + "%%%", "formula" : "dilepBDTphase1%%%" if "phase1" in obs else "dilepBDT%%%", "linearYspace" : 1.5, "minX" : 0 if obs == "invMass" else -1, "maxX" : 13 if obs == "invMass" else 1, "bins" : 40 if (obs == "dilepBDT_fine" or obs == "dilepBDTphase1_fine") else 20, "blind" : [None, 0], "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.45,0.5,0.55,1] if (obs == "dilepBDT_custom" or obs == "dilepBDTphase1_custom") else None,  "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"}
                        #print(hist_def["obs"],jetIso)
                        #print(hist_def["obs"].replace("%%%", jetIso))
                        #print(hist_def["obs"])
                        hist_def["obs"] = hist_def["obs"].replace("%%%", jetIso)
                        hist_def["formula"] = hist_def["formula"].replace("%%%", jetIso)
                        #print(hist_def["obs"])
                        #exit(0)
                        hist_def["condition"] = hist_def["condition"].replace("%%%", jetIso)
                        hist_def["baseline"] = hist_def["baseline"].replace("%%%", jetIso)
                        hist_def["sc"] = hist_def["sc"].replace("%%%", jetIso)
                        histograms_defs.append(hist_def)

class dilepton_muons_bg_isocr_no_retag_scan_phase1(dilepton_muons_bg_isocr_no_retag_scan):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_no_retag_scan_phase1_new_training3.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = True 
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_phase1/sum/slim_sum/type_sum"
    weightString = {
        'MET' : "Weight * passesUniversalSelection * passedMhtMet6pack * tEffhMetMhtRealXMht2017 * BranchingRatio",
    }

class dilepton_electrons_bg_isocr_no_retag_scan_with_phase1_bdt(dilepton_muons_bg_isocr_no_retag_scan):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_electrons_bg_isocr_no_retag_scan_with_phase1_bdt.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = False 

    histograms_defs = [
    
    ]
    
    for iso in utils.leptonIsolationList:
        for cat in utils.leptonIsolationCategories:
            ptRanges = [""]
            drCuts = [""]
            if iso == "CorrJetNoMultIso":
                ptRanges = utils.leptonCorrJetIsoPtRange
                drCuts = utils.leptonCorrJetIsoDrCuts
            else:
                continue
            for ptRange in ptRanges:
                if ptRange < 9:
                    continue
                if ptRange > 11:
                    continue
                for drCut in drCuts:
                    jetIso = ""
                    if len(str(ptRange)) > 0:
                        jetIso = iso + str(ptRange) + "Dr" + str(drCut) + cat
                    else:
                        continue
                    #for obs in ["invMass", "dilepBDT"]:
                    for obs in ["dilepBDT", "dilepBDT_fine", "dilepBDT_custom", "dilepBDTphase1", "dilepBDTphase1_fine", "dilepBDTphase1_custom"]:
                    #for obs in ["dilepBDT_fine"]:
                        #{ "obs" : "invMassCorrJetIso15Dr0.4", "minX" : 0, "maxX" : 13, "bins" : 6, "blind" : [4,None]}
                        hist_def = { "obs" : obs + "%%%", "formula" : "dilepBDTphase1%%%" if "phase1" in obs else "dilepBDT%%%", "linearYspace" : 1.5, "minX" : 0 if obs == "invMass" else -1, "maxX" : 13 if obs == "invMass" else 1, "bins" : 40 if (obs == "dilepBDT_fine" or obs == "dilepBDTphase1_fine") else 20, "blind" : [None, 0], "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.45,0.5,0.55,1] if (obs == "dilepBDT_custom" or obs == "dilepBDTphase1_custom") else None,  "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Electrons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"}
                        #print(hist_def["obs"],jetIso)
                        #print(hist_def["obs"].replace("%%%", jetIso))
                        #print(hist_def["obs"])
                        hist_def["obs"] = hist_def["obs"].replace("%%%", jetIso)
                        hist_def["formula"] = hist_def["formula"].replace("%%%", jetIso)
                        #print(hist_def["obs"])
                        #exit(0)
                        hist_def["condition"] = hist_def["condition"].replace("%%%", jetIso)
                        hist_def["baseline"] = hist_def["baseline"].replace("%%%", jetIso)
                        hist_def["sc"] = hist_def["sc"].replace("%%%", jetIso)
                        histograms_defs.append(hist_def)

class dilepton_electrons_bg_isocr_no_retag_scan_phase1(dilepton_muons_bg_isocr_no_retag_scan):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_electrons_bg_isocr_no_retag_scan_phase1.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = True 
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_phase1/sum/slim_sum/type_sum"
    weightString = {
        'MET' : "Weight * passesUniversalSelection * passedMhtMet6pack * tEffhMetMhtRealXMht2017 * BranchingRatio",
    }
    
    
    histograms_defs = [
    
    ]
    
    for iso in utils.leptonIsolationList:
        for cat in utils.leptonIsolationCategories:
            ptRanges = [""]
            drCuts = [""]
            if iso == "CorrJetNoMultIso":
                ptRanges = utils.leptonCorrJetIsoPtRange
                drCuts = utils.leptonCorrJetIsoDrCuts
            else:
                continue
            for ptRange in ptRanges:
                if ptRange < 9:
                    continue
                if ptRange > 11:
                    continue
                for drCut in drCuts:
                    jetIso = ""
                    if len(str(ptRange)) > 0:
                        jetIso = iso + str(ptRange) + "Dr" + str(drCut) + cat
                    else:
                        continue
                    #for obs in ["invMass", "dilepBDT"]:
                    for obs in ["dilepBDT", "dilepBDT_fine", "dilepBDT_custom"]:
                    #for obs in ["dilepBDT_fine"]:
                        #{ "obs" : "invMassCorrJetIso15Dr0.4", "minX" : 0, "maxX" : 13, "bins" : 6, "blind" : [4,None]}
                        hist_def = { "obs" : obs + "%%%", "formula" : "dilepBDT%%%", "linearYspace" : 1.5, "minX" : 0 if obs == "invMass" else -1, "maxX" : 13 if obs == "invMass" else 1, "bins" : 40 if (obs == "dilepBDT_fine" or obs == "dilepBDTphase1_fine") else 20, "blind" : [None, 0], "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.45,0.5,0.55,1] if (obs == "dilepBDT_custom" or obs == "dilepBDTphase1_custom") else None,  "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Electrons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"}
                        #print(hist_def["obs"],jetIso)
                        #print(hist_def["obs"].replace("%%%", jetIso))
                        #print(hist_def["obs"])
                        hist_def["obs"] = hist_def["obs"].replace("%%%", jetIso)
                        hist_def["formula"] = hist_def["formula"].replace("%%%", jetIso)
                        #print(hist_def["obs"])
                        #exit(0)
                        hist_def["condition"] = hist_def["condition"].replace("%%%", jetIso)
                        hist_def["baseline"] = hist_def["baseline"].replace("%%%", jetIso)
                        hist_def["sc"] = hist_def["sc"].replace("%%%", jetIso)
                        histograms_defs.append(hist_def)

signals = [
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim/higgsino_mu100_dm1p13Chi20Chipm.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim/higgsino_mu100_dm1p47Chi20Chipm.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim/higgsino_mu100_dm1p92Chi20Chipm.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim/higgsino_mu100_dm3p28Chi20Chipm.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim/higgsino_mu100_dm4p30Chi20Chipm.root"
              ]

signalNames = [
    "\Delta_{}M 1.13 Gev",
    "\Delta_{}M 1.47 Gev",
    "\Delta_{}M 1.9 Gev",
    "\Delta_{}M 3.2 Gev",
    "\Delta_{}M 4.3 Gev",
]

class dilepton_muons_bg_isocr_no_retag_scan_full_met_range_optimised_bins_tautau(dilepton_muons_bg_isocr_no_retag_CorrJetIso10_5_55):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_no_retag_scan_full_met_range_optimised_bins_tautau.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = True 
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/slim_sum_full_met_range/type_sum"
    cuts = [
        {"name":"none", "title": "None", "condition" : "1", "baseline" : "1", "sc" : "1"},
        #{"name":"bdt", "title": "BDT > 0.35", "condition" : "(dilepBDT%%% > 0.35 &&  MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 200 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
    ]
    histograms_defs = [
    #    { "obs" : "invMass%%%", "minX" : 0, "maxX" : 13, "bins" : 6, "blind" : [4,None]},# "customBins"  : [0,2,4,6,10,12] },
    #    { "obs" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 6, "blind" : [None,0.1]}
    ]
    
    for iso in utils.leptonIsolationList:
        for cat in utils.leptonIsolationCategories:
            ptRanges = [""]
            drCuts = [""]
            if iso == "CorrJetIso":
                ptRanges = utils.leptonCorrJetIsoPtRange
                drCuts = utils.leptonCorrJetIsoDrCuts
            else:
                continue
            for ptRange in ptRanges:
                for drCut in drCuts:
                    jetIso = ""
                    if len(str(ptRange)) > 0:
                        jetIso = iso + str(ptRange) + "Dr" + str(drCut) + cat
                    else:
                        continue
                    #for obs in ["invMass", "dilepBDT"]:
                    for obs in ["dilepBDT"]:
                        hist_def = { "obs" : obs + "%%%", "minX" : 0 if obs == "invMass" else -1, "maxX" : 13 if obs == "invMass" else 1, "customBins"  : [-1,-0.6,-0.4,-0.2,0,0.1, 0.18, 0.22, 0.38, 0.42, 0.46,1], "blind" : [None, 0],  "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 200 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"}
                        #hist_def = { "obs" : obs + "%%%", "minX" : 0 if obs == "invMass" else -1, "maxX" : 13 if obs == "invMass" else 1, "bins"  : 6, "blind" : [None, 0],  "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 200 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"}
                        #print(hist_def["obs"],jetIso)
                        #print(hist_def["obs"].replace("%%%", jetIso))
                        #print(hist_def["obs"])
                        hist_def["obs"] = hist_def["obs"].replace("%%%", jetIso)
                        #print(hist_def["obs"])
                        #exit(0)
                        hist_def["condition"] = hist_def["condition"].replace("%%%", jetIso)
                        hist_def["baseline"] = hist_def["baseline"].replace("%%%", jetIso)
                        hist_def["sc"] = hist_def["sc"].replace("%%%", jetIso)
                        histograms_defs.append(hist_def)

class dilepton_muons_bg_isocr_no_retag_scan_full_met_range_optimised_bins_full(dilepton_muons_bg_isocr_no_retag_CorrJetIso10_5_55):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_no_retag_scan_full_met_range_optimised_bins_full.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = True 
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/slim_sum_full_met_range/type_sum"
    cuts = [
        {"name":"none", "title": "None", "condition" : "1", "baseline" : "1", "sc" : "1"},
        #{"name":"bdt", "title": "BDT > 0.35", "condition" : "(dilepBDT%%% > 0.35 &&  MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 200 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
    ]
    histograms_defs = [
    #    { "obs" : "invMass%%%", "minX" : 0, "maxX" : 13, "bins" : 6, "blind" : [4,None]},# "customBins"  : [0,2,4,6,10,12] },
    #    { "obs" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 6, "blind" : [None,0.1]}
    ]
    
    for iso in utils.leptonIsolationList:
        for cat in utils.leptonIsolationCategories:
            ptRanges = [""]
            drCuts = [""]
            if iso == "CorrJetIso":
                ptRanges = utils.leptonCorrJetIsoPtRange
                drCuts = utils.leptonCorrJetIsoDrCuts
            else:
                continue
            for ptRange in ptRanges:
                for drCut in drCuts:
                    jetIso = ""
                    if len(str(ptRange)) > 0:
                        jetIso = iso + str(ptRange) + "Dr" + str(drCut) + cat
                    else:
                        continue
                    #for obs in ["invMass", "dilepBDT"]:
                    for obs in ["dilepBDT"]:
                        hist_def = { "obs" : obs + "%%%", "minX" : 0 if obs == "invMass" else -1, "maxX" : 13 if obs == "invMass" else 1, "customBins"  : [-1,-0.6,-0.4,-0.2,0,0.1, 0.18, 0.22, 0.38, 0.42, 0.46,1], "blind" : [None, 0],  "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 200 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"}
                        #hist_def = { "obs" : obs + "%%%", "minX" : 0 if obs == "invMass" else -1, "maxX" : 13 if obs == "invMass" else 1, "bins"  : 6, "blind" : [None, 0],  "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 200 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"}
                        #print(hist_def["obs"],jetIso)
                        #print(hist_def["obs"].replace("%%%", jetIso))
                        #print(hist_def["obs"])
                        hist_def["obs"] = hist_def["obs"].replace("%%%", jetIso)
                        #print(hist_def["obs"])
                        #exit(0)
                        hist_def["condition"] = hist_def["condition"].replace("%%%", jetIso)
                        hist_def["baseline"] = hist_def["baseline"].replace("%%%", jetIso)
                        hist_def["sc"] = hist_def["sc"].replace("%%%", jetIso)
                        histograms_defs.append(hist_def)
    
class dilepton_muons_bg_isocr(dilepton_muons_bg_isocr_no_retag):
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/type_sum"
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr.root"
    
    bg_retag = True
    
    save_histrograms_to_file = True
    load_histrograms_from_file = False 
    
    # bgReTagging = {
#         "veto" : "(isoCr == 0)",
#         "isoCr" : "(isoCr >= 1)",
#     }
#     
#     bgReTaggingOrder = {
#         "veto" : 0,
#         "isoCr" : 1,
#     }
#     bgReTaggingNames = {
#         "veto" : "veto",
#         "isoCr" : "Jet Iso #Delta_{}R CR",
#     }
    
    bgReTagging = bgReTaggingCollected
    bgReTaggingOrder = bgReTaggingOrderFull
    bgReTaggingNames = bgReTaggingNamesFull
    
    cuts = [
        #{"name":"none", "title": "None", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0", "sc" : "sameSign == 0 && isoCr >= 1"},
        #{"name":"isocr1", "title": "isoCr == 1", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0", "sc" : "sameSign == 0 && isoCr == 1"},
        {"name":"mindr01", "title": "MinDr >= 0.1 && isoCr == 1", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0", "sc" : "sameSign == 0 && isoCr == 1 && isoCrMinDr >= 0.1"},
        {"name":"mindr02", "title": "MinDr >= 0.2 && isoCr == 1", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0", "sc" : "sameSign == 0 && isoCr == 1 && isoCrMinDr >= 0.2"},
        #{"name": "bdt", "title": "bdt >= 0.1", "condition" : "(dilepBDT >= 0.1 && BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0", "sc" : "sameSign == 0 && isoCr >= 1"},
        #{"name":"no-tautau", "title": "No tautau", "condition" : "(!tautau && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && !(invMass > 3 && invMass < 3.2) && invMass < 12  && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0", "sc" : "sameSign == 1"},
        #{"name":"bdt", "title": "BDT>0.1", "condition" : "(dilepBDT > 0.1 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && !(invMass > 3 && invMass < 3.2) && invMass < 12 && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0", "sc" : "sameSign == 1"},
        #{"name":"bdt-no-tautau", "title": "BDT>0.1 && No tautau", "condition" : "(!tautau && dilepBDT > 0.1 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && !(invMass > 3 && invMass < 3.2) && invMass < 12 && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0", "sc" : "sameSign == 1"},
        
        #{"name":"low-met", "title": "Low Met", "condition" : "(twoLeptons == 1 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0", "sc" : "sameSign == 1"},
        #{"name":"non-orth", "title": "Non Orth", "condition" : "(twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && dilepBDT > 0.1)", "baseline" : "sameSign == 0", "sc" : "sameSign == 1"},
        #{"name":"orth", "title": "Orth", "condition" : "(twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && dilepBDT > 0.1 && (leptons[1].Pt() <= 3.5 || deltaR <= 0.3))", "baseline" : "sameSign == 0", "sc" : "sameSign == 1"},
    ]
    
    
    plot_custom_ratio = 0
    #customRatios = [  [["veto"],["isoCr"]]  ]
    
    plot_signal = False
    plot_sc = True
    plot_data = False
    plot_overflow = False
    plot_ratio = True
    
    blind_data = True
    subtract_same_charge = False
    nostack = False
    
    histograms_defs = [
        { "obs" : "invMass", "minX" : 0, "maxX" : 13, "bins" : 6, "blind" : [4,None]},# "customBins"  : [0,2,4,6,10,12] },
        { "obs" : "dilepBDT", "minX" : -1, "maxX" : 1, "bins" : 6, "blind" : [None,0.1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        #{ "obs" : "isoCrMinDr", "minX" : 0, "maxX" : 0.4, "bins" : 8},
        { "obs" : "deltaR", "minX" : 0, "maxX" : 3.5, "bins" : 8},
        { "obs" : "dilepHt", "minX" : 200, "maxX" : 800, "bins" : 8},
        { "obs" : "dileptonPt", "minX" : 0, "maxX" : 30, "bins" : 8},
        { "obs" : "MHT", "minX" : 220, "maxX" : 800, "bins" : 8},
        { "obs" : "MinDeltaPhiMhtJets", "minX" : 0, "maxX" : 3.5, "bins" : 8},
        { "obs" : "leptons[0].Pt()", "minX" : 0, "maxX" : 20, "bins" : 8},
        { "obs" : "deltaPhiMetLepton1", "minX" : 0, "maxX" : 3.5, "bins" : 8},
        { "obs" : "mt1", "minX" : 0, "maxX" : 200, "bins" : 8},
        { "obs" : "leptons[0].Eta()", "minX" : -2.4, "maxX" : 2.4, "bins" : 8},
        { "obs" : "NJets", "minX" : 0, "maxX" : 6, "bins" : 6},
        { "obs" : "deltaPhiMetLepton2", "minX" : 0, "maxX" : 3.5, "bins" : 8},
        { "obs" : "LeadingJetPt", "minX" : 0, "maxX" : 500, "bins" : 8},
        { "obs" : "LeadingJet.Eta()", "minX" : -2.4, "maxX" : 2.4, "bins" : 8},
        { "obs" : "deltaEta", "minX" : 0, "maxX" : 5, "bins" : 8},
        { "obs" : "HT", "minX" : 0, "maxX" : 500, "bins" : 8},
        { "obs" : "leptons[0].Phi()", "minX" : 0, "maxX" : 3.5, "bins" : 8},
    ]
    
    normalise = True
    normalise_each_bg = False
    plot_error = True
    sc_label = "Jet Iso #Delta_{}R CR"
    sc_ratio_label = "cr"

class dilepton_muons_bg_isocr_min_dr(dilepton_muons_bg_isocr):
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/type_sum"
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_min_dr.root"
    
    histograms_defs = [
        { "obs" : "isoCrMinDr", "minX" : 0, "maxX" : 0.4, "bins" : 8}
    ]
    cuts = [
        {"name":"none", "title": "None", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr >= 1", "sc" : "sameSign == 0 && isoCr >= 1"},
    ]
    plot_sc = False
    plot_ratio = False
    normalise = False

class dilepton_muons_bg_isocr_notautau(dilepton_muons_bg_isocr):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_notautau.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = False
    bgReTagging = bgReTaggingCollectedNoTauTau
    cuts = [
        {"name":"none", "title": "None", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0 && !tautau", "sc" : "sameSign == 0 && isoCr >= 1 && !tautau"},
        {"name":"isocr1", "title": "isoCr == 1", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0 && !tautau", "sc" : "sameSign == 0 && isoCr == 1  && !tautau"},
        {"name":"mindr01", "title": "MinDr >= 0.1 && isoCr == 1", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0 && !tautau", "sc" : "sameSign == 0 && isoCr == 1 && !tautau && isoCrMinDr >= 0.1"},
        {"name":"mindr02", "title": "MinDr >= 0.2 && isoCr == 1", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0 && !tautau", "sc" : "sameSign == 0 && isoCr == 1 && !tautau && isoCrMinDr >= 0.2"},
        {"name":"isocr011", "title": "MinDr >= 0.1 && isoCr >= 1", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0 && !tautau", "sc" : "sameSign == 0 && isoCr >= 1 && !tautau && isoCrMinDr >= 0.1"},
        {"name":"isocr02", "title": "MinDr >= 0.2 && isoCr >= 1", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0 && !tautau", "sc" : "sameSign == 0 && isoCr >= 1 && !tautau && isoCrMinDr >= 0.2"},
        #{"name":"nj", "title": "NJ >= 2", "condition" : "(NJets >= 2 && BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0 && !tautau", "sc" : "sameSign == 0 && isoCr >= 1 && !tautau"},
        #{"name": "bdt", "title": "bdt >= 0.1", "condition" : "(dilepBDT >= 0.1 && BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0 && !tautau", "sc" : "sameSign == 0 && isoCr >= 1 && !tautau"},
        
        #{"name":"none", "title": "None", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0 && !tautau", "sc" : "sameSign == 0 && isoCr >= 1 && !tautau"},
    ]

class dilepton_muons_bg_isocr_notautau_corrjetiso(dilepton_muons_bg_isocr_notautau):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_notautau_corrjetiso.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = False
    bgReTagging = bgReTaggingCollectedNoTauTauCorrJetIso
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_0.4/sum/type_sum"
    cuts = [
        {"name":"none", "title": "None", "condition" : "(BTagsDeepMedium == 0 && twoLeptonsCorrJetIso15 == 1 && MHT >= 220 &&  MET >= 200 && @leptonsCorrJetIso15.size() == 2 && leptonFlavourCorrJetIso15 == \"Muons\" && invMassCorrJetIso15 < 12  && invMassCorrJetIso15 > 0.4 && !(invMassCorrJetIso15 > 3 && invMassCorrJetIso15 < 3.2) && !(invMassCorrJetIso15 > 0.75 && invMassCorrJetIso15 < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSignCorrJetIso15 == 0 && isoCrCorrJetIso15 == 0 && !tautauCorrJetIso15", "sc" : "sameSignCorrJetIso15 == 0 && isoCrCorrJetIso15 >= 1 && !tautauCorrJetIso15"},
        {"name":"isocr1", "title": "isoCr == 1", "condition" : "(BTagsDeepMedium == 0 && twoLeptonsCorrJetIso15 == 1 && MHT >= 220 &&  MET >= 200 && @leptonsCorrJetIso15.size() == 2 && leptonFlavourCorrJetIso15 == \"Muons\" && invMassCorrJetIso15 < 12  && invMassCorrJetIso15 > 0.4 && !(invMassCorrJetIso15 > 3 && invMassCorrJetIso15 < 3.2) && !(invMassCorrJetIso15 > 0.75 && invMassCorrJetIso15 < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSignCorrJetIso15 == 0 && isoCrCorrJetIso15 == 0 && !tautauCorrJetIso15", "sc" : "sameSignCorrJetIso15 == 0 && isoCrCorrJetIso15 == 1 && !tautauCorrJetIso15"},
        {"name":"mindr01", "title": "MinDr >= 0.1 && isoCr == 1", "condition" : "(BTagsDeepMedium == 0 && twoLeptonsCorrJetIso15 == 1 && MHT >= 220 &&  MET >= 200 && @leptonsCorrJetIso15.size() == 2 && leptonFlavourCorrJetIso15 == \"Muons\" && invMassCorrJetIso15 < 12  && invMassCorrJetIso15 > 0.4 && !(invMassCorrJetIso15 > 3 && invMassCorrJetIso15 < 3.2) && !(invMassCorrJetIso15 > 0.75 && invMassCorrJetIso15 < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSignCorrJetIso15 == 0 && isoCrCorrJetIso15 == 0 && !tautauCorrJetIso15", "sc" : "sameSignCorrJetIso15 == 0 && isoCrCorrJetIso15 == 1 && !tautauCorrJetIso15 && isoCrMinDrCorrJetIso15 >= 0.1"},
        {"name":"mindr02", "title": "MinDr >= 0.2 && isoCr == 1", "condition" : "(BTagsDeepMedium == 0 && twoLeptonsCorrJetIso15 == 1 && MHT >= 220 &&  MET >= 200 && @leptonsCorrJetIso15.size() == 2 && leptonFlavourCorrJetIso15 == \"Muons\" && invMassCorrJetIso15 < 12  && invMassCorrJetIso15 > 0.4 && !(invMassCorrJetIso15 > 3 && invMassCorrJetIso15 < 3.2) && !(invMassCorrJetIso15 > 0.75 && invMassCorrJetIso15 < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSignCorrJetIso15 == 0 && isoCrCorrJetIso15 == 0 && !tautauCorrJetIso15", "sc" : "sameSignCorrJetIso15 == 0 && isoCrCorrJetIso15 == 1 && !tautauCorrJetIso15 && isoCrMinDrCorrJetIso15 >= 0.2"},
        {"name":"isocr011", "title": "MinDr >= 0.1 && isoCr >= 1", "condition" : "(BTagsDeepMedium == 0 && twoLeptonsCorrJetIso15 == 1 && MHT >= 220 &&  MET >= 200 && @leptonsCorrJetIso15.size() == 2 && leptonFlavourCorrJetIso15 == \"Muons\" && invMassCorrJetIso15 < 12  && invMassCorrJetIso15 > 0.4 && !(invMassCorrJetIso15 > 3 && invMassCorrJetIso15 < 3.2) && !(invMassCorrJetIso15 > 0.75 && invMassCorrJetIso15 < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSignCorrJetIso15 == 0 && isoCrCorrJetIso15 == 0 && !tautauCorrJetIso15", "sc" : "sameSignCorrJetIso15 == 0 && isoCrCorrJetIso15 >= 1 && !tautauCorrJetIso15 && isoCrMinDrCorrJetIso15 >= 0.1"},
        {"name":"isocr02", "title": "MinDr >= 0.2 && isoCr >= 1", "condition" : "(BTagsDeepMedium == 0 && twoLeptonsCorrJetIso15 == 1 && MHT >= 220 &&  MET >= 200 && @leptonsCorrJetIso15.size() == 2 && leptonFlavourCorrJetIso15 == \"Muons\" && invMassCorrJetIso15 < 12  && invMassCorrJetIso15 > 0.4 && !(invMassCorrJetIso15 > 3 && invMassCorrJetIso15 < 3.2) && !(invMassCorrJetIso15 > 0.75 && invMassCorrJetIso15 < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSignCorrJetIso15 == 0 && isoCrCorrJetIso15 == 0 && !tautauCorrJetIso15", "sc" : "sameSignCorrJetIso15 == 0 && isoCrCorrJetIso15 >= 1 && !tautauCorrJetIso15 && isoCrMinDrCorrJetIso15 >= 0.2"},
        #{"name":"nj", "title": "NJ >= 2", "condition" : "(NJets >= 2 && BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0 && !tautau", "sc" : "sameSign == 0 && isoCr >= 1 && !tautau"},
        #{"name": "bdt", "title": "bdt >= 0.1", "condition" : "(dilepBDT >= 0.1 && BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0 && !tautau", "sc" : "sameSign == 0 && isoCr >= 1 && !tautau"},
        
        #{"name":"none", "title": "None", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0 && !tautau", "sc" : "sameSign == 0 && isoCr >= 1 && !tautau"},
    ]
    
    histograms_defs = [
        { "obs" : "invMassCorrJetIso15", "minX" : 0, "maxX" : 13, "bins" : 6, "blind" : [4,None]},# "customBins"  : [0,2,4,6,10,12] },
        { "obs" : "dilepBDTCorrJetIso15", "minX" : -1, "maxX" : 1, "bins" : 6, "blind" : [None,0.1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        { "obs" : "isoCrMinDrCorrJetIso15", "minX" : 0, "maxX" : 0.4, "bins" : 8},
        { "obs" : "deltaRCorrJetIso15", "minX" : 0, "maxX" : 3.5, "bins" : 8},
        { "obs" : "dilepHtCorrJetIso15", "minX" : 200, "maxX" : 800, "bins" : 8},
        { "obs" : "dileptonPtCorrJetIso15", "minX" : 0, "maxX" : 30, "bins" : 8},
        { "obs" : "MHT", "minX" : 220, "maxX" : 800, "bins" : 8},
        { "obs" : "MinDeltaPhiMhtJets", "minX" : 0, "maxX" : 3.5, "bins" : 8},
        { "obs" : "leptonsCorrJetIso15[0].Pt()", "minX" : 0, "maxX" : 20, "bins" : 8},
        { "obs" : "deltaPhiMetLepton1CorrJetIso15", "minX" : 0, "maxX" : 3.5, "bins" : 8},
        { "obs" : "mt1CorrJetIso15", "minX" : 0, "maxX" : 200, "bins" : 8},
        { "obs" : "leptonsCorrJetIso15[0].Eta()", "minX" : -2.4, "maxX" : 2.4, "bins" : 8},
        { "obs" : "NJets", "minX" : 0, "maxX" : 6, "bins" : 6},
        { "obs" : "deltaPhiMetLepton2CorrJetIso15", "minX" : 0, "maxX" : 3.5, "bins" : 8},
        { "obs" : "LeadingJetPt", "minX" : 0, "maxX" : 500, "bins" : 8},
        { "obs" : "LeadingJet.Eta()", "minX" : -2.4, "maxX" : 2.4, "bins" : 8},
        { "obs" : "deltaEtaCorrJetIso15", "minX" : 0, "maxX" : 5, "bins" : 8},
        { "obs" : "HT", "minX" : 0, "maxX" : 500, "bins" : 8},
        { "obs" : "leptonsCorrJetIso15[0].Phi()", "minX" : 0, "maxX" : 3.5, "bins" : 8},
    ]


class dilepton_muons_bg_isocr_notautau_corrjetiso_15_04(dilepton_muons_bg_isocr_notautau_corrjetiso):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_notautau_corrjetiso_15_04.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = False
    bgReTagging = bgReTaggingCollectedNoTauTauCorrJetIso15_04
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/slim_sum/type_sum"
    cuts = [
        {"name":"none", "title": "None", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptonsCorrJetIso15Dr0.4 == 1 && MHT >= 220 &&  MET >= 200 && leptonFlavourCorrJetIso15Dr0.4 == \"Muons\" && invMassCorrJetIso15Dr0.4 < 12  && invMassCorrJetIso15Dr0.4 > 0.4 && !(invMassCorrJetIso15Dr0.4 > 3 && invMassCorrJetIso15Dr0.4 < 3.2) && !(invMassCorrJetIso15Dr0.4 > 0.75 && invMassCorrJetIso15Dr0.4 < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSignCorrJetIso15Dr0.4 == 0 && isoCrCorrJetIso15Dr0.4 == 0 && !tautauCorrJetIso15Dr0.4", "sc" : "sameSignCorrJetIso15Dr0.4 == 0 && isoCrCorrJetIso15Dr0.4 >= 1 && !tautauCorrJetIso15Dr0.4"},
    ]
    
    histograms_defs = [
        { "obs" : "invMassCorrJetIso15Dr0.4", "minX" : 0, "maxX" : 13, "bins" : 6, "blind" : [4,None]},# "customBins"  : [0,2,4,6,10,12] },
        { "obs" : "dilepBDTCorrJetIso15Dr0.4", "minX" : -1, "maxX" : 1, "bins" : 6, "blind" : [None,0.1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        { "obs" : "dilepBDTCorrJetIso15Dr0.4_fine", "formula": "dilepBDTCorrJetIso15Dr0.4", "minX" : -1, "maxX" : 1, "bins" : 15, "blind" : [None,0.1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        # { "obs" : "isoCrMinDrCorrJetIso15Dr0.4", "minX" : 0, "maxX" : 0.4, "bins" : 8},
#         { "obs" : "deltaRCorrJetIso15Dr0.4", "minX" : 0, "maxX" : 3.5, "bins" : 8},
#         { "obs" : "dilepHtCorrJetIso15Dr0.4", "minX" : 200, "maxX" : 800, "bins" : 8},
#         { "obs" : "dileptonPtCorrJetIso15Dr0.4", "minX" : 0, "maxX" : 30, "bins" : 8},
#         { "obs" : "MHT", "minX" : 220, "maxX" : 800, "bins" : 8},
#         { "obs" : "MinDeltaPhiMhtJets", "minX" : 0, "maxX" : 3.5, "bins" : 8},
#         { "obs" : "leptonsCorrJetIso15Dr0.4[0].Pt()", "minX" : 0, "maxX" : 20, "bins" : 8},
#         { "obs" : "deltaPhiMetLepton1CorrJetIso15Dr0.4", "minX" : 0, "maxX" : 3.5, "bins" : 8},
#         { "obs" : "mt1CorrJetIso15Dr0.4", "minX" : 0, "maxX" : 200, "bins" : 8},
#         { "obs" : "leptonsCorrJetIso15Dr0.4[0].Eta()", "minX" : -2.4, "maxX" : 2.4, "bins" : 8},
#         { "obs" : "NJets", "minX" : 0, "maxX" : 6, "bins" : 6},
#         { "obs" : "deltaPhiMetLepton2CorrJetIso15Dr0.4", "minX" : 0, "maxX" : 3.5, "bins" : 8},
#         { "obs" : "LeadingJetPt", "minX" : 0, "maxX" : 500, "bins" : 8},
#         { "obs" : "LeadingJet.Eta()", "minX" : -2.4, "maxX" : 2.4, "bins" : 8},
#         { "obs" : "deltaEtaCorrJetIso15Dr0.4", "minX" : 0, "maxX" : 5, "bins" : 8},
#         { "obs" : "HT", "minX" : 0, "maxX" : 500, "bins" : 8},
#         { "obs" : "leptonsCorrJetIso15Dr0.4[0].Phi()", "minX" : 0, "maxX" : 3.5, "bins" : 8},
    ]

class dilepton_muons_bg_isocr_notautau_corrjetiso_15_04_no_retag(dilepton_muons_bg_isocr_notautau_corrjetiso_15_04):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_notautau_corrjetiso_15_04_no_retag.root"
    bg_retag = False

class dilepton_muons_bg_isocr_notautau_corrjetiso_11_055(dilepton_muons_bg_isocr_notautau_corrjetiso_15_04):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_notautau_corrjetiso_11_055.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = False
    bgReTagging = bgReTaggingCollectedNoTauTauCorrJetIso11_055
    bg_retag = False
    #bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/slim"
    cuts = [
        {"name":"none", "title": "None", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptonsCorrJetIso11Dr0.55 == 1 && MHT >= 220 &&  MET >= 200 && leptonFlavourCorrJetIso11Dr0.55 == \"Muons\" && invMassCorrJetIso11Dr0.55 < 12  && invMassCorrJetIso11Dr0.55 > 0.4 && !(invMassCorrJetIso11Dr0.55 > 3 && invMassCorrJetIso11Dr0.55 < 3.2) && !(invMassCorrJetIso11Dr0.55 > 0.75 && invMassCorrJetIso11Dr0.55 < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSignCorrJetIso11Dr0.55 == 0 && isoCrCorrJetIso11Dr0.55 == 0 && !tautauCorrJetIso11Dr0.55", "sc" : "sameSignCorrJetIso11Dr0.55 == 0 && isoCrCorrJetIso11Dr0.55 >= 1 && !tautauCorrJetIso11Dr0.55"},
    ]
    
    histograms_defs = [
        { "obs" : "invMassCorrJetIso11Dr0.55", "minX" : 0, "maxX" : 13, "bins" : 6, "blind" : [4,None]},# "customBins"  : [0,2,4,6,10,12] },
        { "obs" : "dilepBDTCorrJetIso11Dr0.55", "minX" : -1, "maxX" : 1, "bins" : 6, "blind" : [None,0.1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        { "obs" : "dilepBDTCorrJetIso11Dr0.55_fine", "formula" : "dilepBDTCorrJetIso11Dr0.55","minX" : -1, "maxX" : 1, "bins" : 15, "blind" : [None,0.1]},
        { "obs" : "dilepBDTCorrJetIso11Dr0.55_custom", "formula" : "dilepBDTCorrJetIso11Dr0.55", "minX" : -1, "maxX" : 1, "bins" : 6, "blind" : [None,0.1], "customBins"  : [-1,-0.6,-0.3,0,0.10,0.26,0.34,0.38,0.42,1] },
        # { "obs" : "isoCrMinDrCorrJetIso15Dr0.4", "minX" : 0, "maxX" : 0.4, "bins" : 8},
        { "obs" : "deltaRCorrJetIso11Dr0.55", "minX" : 0, "maxX" : 3.5, "bins" : 8},
        { "obs" : "dilepHtCorrJetIso11Dr0.55", "minX" : 200, "maxX" : 800, "bins" : 8},
        { "obs" : "dileptonPtCorrJetIso11Dr0.55", "minX" : 0, "maxX" : 30, "bins" : 8},
        { "obs" : "MHT", "minX" : 220, "maxX" : 800, "bins" : 8},
        { "obs" : "MinDeltaPhiMhtJets", "minX" : 0, "maxX" : 3.5, "bins" : 8},
        { "obs" : "leptonsCorrJetIso11Dr0.55[0].Pt()", "minX" : 0, "maxX" : 20, "bins" : 8},
        { "obs" : "deltaPhiMetLepton1CorrJetIso11Dr0.55", "minX" : 0, "maxX" : 3.5, "bins" : 8},
        { "obs" : "mt1CorrJetIso11Dr0.55", "minX" : 0, "maxX" : 200, "bins" : 8},
        { "obs" : "leptonsCorrJetIso11Dr0.55[0].Eta()", "minX" : -2.4, "maxX" : 2.4, "bins" : 8},
        { "obs" : "NJets", "minX" : 0, "maxX" : 6, "bins" : 6},
        { "obs" : "deltaPhiMetLepton2CorrJetIso11Dr0.55", "minX" : 0, "maxX" : 3.5, "bins" : 8},
        { "obs" : "LeadingJetPt", "minX" : 0, "maxX" : 500, "bins" : 8},
        { "obs" : "LeadingJet.Eta()", "minX" : -2.4, "maxX" : 2.4, "bins" : 8},
        { "obs" : "deltaEtaCorrJetIso11Dr0.55", "minX" : 0, "maxX" : 5, "bins" : 8},
        { "obs" : "HT", "minX" : 0, "maxX" : 500, "bins" : 8},
        { "obs" : "leptonsCorrJetIso11Dr0.55[0].Phi()", "minX" : 0, "maxX" : 3.5, "bins" : 8},
    ]

class dilepton_muons_bg_isocr_notautau_corrjetiso_10_06(dilepton_muons_bg_isocr_notautau_corrjetiso_11_055):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_notautau_corrjetiso_10_06.root"
    cuts = [
        {"name":"none", "title": "None", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptonsCorrJetIso10Dr0.6 == 1 && MHT >= 220 &&  MET >= 200 && leptonFlavourCorrJetIso10Dr0.6 == \"Muons\" && invMassCorrJetIso10Dr0.6 < 12  && invMassCorrJetIso10Dr0.6 > 0.4 && !(invMassCorrJetIso10Dr0.6 > 3 && invMassCorrJetIso10Dr0.6 < 3.2) && !(invMassCorrJetIso10Dr0.6 > 0.75 && invMassCorrJetIso10Dr0.6 < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSignCorrJetIso10Dr0.6 == 0 && isoCrCorrJetIso10Dr0.6 == 0 && !tautauCorrJetIso10Dr0.6", "sc" : "sameSignCorrJetIso10Dr0.6 == 0 && isoCrCorrJetIso10Dr0.6 >= 1 && !tautauCorrJetIso10Dr0.6"},
    ]
    
    histograms_defs = [
        { "obs" : "invMassCorrJetIso10Dr0.6", "minX" : 0, "maxX" : 13, "bins" : 6, "blind" : [4,None]},# "customBins"  : [0,2,4,6,10,12] },
        { "obs" : "dilepBDTCorrJetIso10Dr0.6", "minX" : -1, "maxX" : 1, "bins" : 6, "blind" : [None,0.1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        { "obs" : "dilepBDTCorrJetIso10Dr0.6_fine", "formula" : "dilepBDTCorrJetIso10Dr0.6","minX" : -1, "maxX" : 1, "bins" : 15, "blind" : [None,0.1]},
        { "obs" : "dilepBDTCorrJetIso10Dr0.6_custom", "formula" : "dilepBDTCorrJetIso10Dr0.6", "minX" : -1, "maxX" : 1, "bins" : 6, "blind" : [None,0.1], "customBins"  : [-1,-0.6,-0.3,0,0.10,0.26,0.34,0.38,0.42,1] },
        { "obs" : "deltaRCorrJetIso10Dr0.6", "minX" : 0, "maxX" : 3.5, "bins" : 8},
        { "obs" : "dilepHtCorrJetIso10Dr0.6", "minX" : 200, "maxX" : 800, "bins" : 8},
        { "obs" : "dileptonPtCorrJetIso10Dr0.6", "minX" : 0, "maxX" : 30, "bins" : 8},
        { "obs" : "MHT", "minX" : 220, "maxX" : 800, "bins" : 8},
        { "obs" : "MET", "minX" : 200, "maxX" : 800, "bins" : 8},
        { "obs" : "MinDeltaPhiMhtJets", "minX" : 0, "maxX" : 3.5, "bins" : 8},
        { "obs" : "leptonsCorrJetIso10Dr0.6[0].Pt()", "minX" : 0, "maxX" : 20, "bins" : 8},
        { "obs" : "deltaPhiMetLepton1CorrJetIso10Dr0.6", "minX" : 0, "maxX" : 3.5, "bins" : 8},
        { "obs" : "mt1CorrJetIso10Dr0.6", "minX" : 0, "maxX" : 200, "bins" : 8},
        { "obs" : "leptonsCorrJetIso10Dr0.6[0].Eta()", "minX" : -2.4, "maxX" : 2.4, "bins" : 8},
        { "obs" : "NJets", "minX" : 0, "maxX" : 6, "bins" : 6},
        { "obs" : "deltaPhiMetLepton2CorrJetIso10Dr0.6", "minX" : 0, "maxX" : 3.5, "bins" : 8},
        { "obs" : "LeadingJetPt", "minX" : 0, "maxX" : 500, "bins" : 8},
        { "obs" : "LeadingJet.Eta()", "minX" : -2.4, "maxX" : 2.4, "bins" : 8},
        { "obs" : "deltaEtaCorrJetIso10Dr0.6", "minX" : 0, "maxX" : 5, "bins" : 8},
        { "obs" : "HT", "minX" : 0, "maxX" : 500, "bins" : 8},
        { "obs" : "leptonsCorrJetIso10Dr0.6[0].Phi()", "minX" : 0, "maxX" : 3.5, "bins" : 8},
     ]

class dilepton_muons_bg_isocr_notautau_corrjetiso_11_055_custom_bins(dilepton_muons_bg_isocr_notautau_corrjetiso_11_055):
    histograms_defs = [
        #{ "obs" : "invMassCorrJetIso11Dr0.55", "minX" : 0, "maxX" : 13, "bins" : 6, "blind" : [4,None], "customBins"  :  },
        { "obs" : "dilepBDTCorrJetIso11Dr0.55", "minX" : -1, "maxX" : 1, "bins" : 6, "blind" : [None,0.1], "customBins"  : [-1,-0.6,-0.3,0,0.02,0.10,0.26,0.34,0.38,0.42,1] },
    ]

class dilepton_muons_bg_isocr_notautau_corrjetiso_11_055_custom_bins_collected(dilepton_muons_bg_isocr_notautau_corrjetiso_11_055_custom_bins):
    bgReTagging = bgReTaggingCollectedCorrJetIso11_055
    cuts = [
        {"name":"none", "title": "None", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptonsCorrJetIso11Dr0.55 == 1 && MHT >= 220 &&  MET >= 200 && MinDeltaPhiMhtJets > 0.4 && leptonFlavourCorrJetIso11Dr0.55 == \"Muons\" && invMassCorrJetIso11Dr0.55 < 12  && invMassCorrJetIso11Dr0.55 > 0.4 && !(invMassCorrJetIso11Dr0.55 > 3 && invMassCorrJetIso11Dr0.55 < 3.2) && !(invMassCorrJetIso11Dr0.55 > 0.75 && invMassCorrJetIso11Dr0.55 < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSignCorrJetIso11Dr0.55 == 0 && isoCrCorrJetIso11Dr0.55 == 0", "sc" : "sameSignCorrJetIso11Dr0.55 == 0 && isoCrCorrJetIso11Dr0.55 >= 1"},
    ]

class dilepton_muons_bg_isocr_notautau_corrjetiso_no_norm(dilepton_muons_bg_isocr_notautau_corrjetiso):
    load_histrograms_from_file = True
    normalise = False

class dilepton_muons_bg_isocr_inclusive_corrjetiso(dilepton_muons_bg_isocr_notautau_corrjetiso):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_inclusive_corrjetiso.root"
    bgReTagging = bgReTaggingCollectedCorrJetIso15
    cuts = [
        {"name":"none", "title": "None", "condition" : "(BTagsDeepMedium == 0 && twoLeptonsCorrJetIso15 == 1 && MHT >= 220 &&  MET >= 200 && @leptonsCorrJetIso15.size() == 2 && leptonFlavourCorrJetIso15 == \"Muons\" && invMassCorrJetIso15 < 12  && invMassCorrJetIso15 > 0.4 && !(invMassCorrJetIso15 > 3 && invMassCorrJetIso15 < 3.2) && !(invMassCorrJetIso15 > 0.75 && invMassCorrJetIso15 < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSignCorrJetIso15 == 0 && isoCrCorrJetIso15 == 0", "sc" : "sameSignCorrJetIso15 == 0 && isoCrCorrJetIso15 >= 1"},
        #{"name":"isocr1", "title": "isoCr == 1", "condition" : "(BTagsDeepMedium == 0 && twoLeptonsCorrJetIso15 == 1 && MHT >= 220 &&  MET >= 200 && @leptonsCorrJetIso15.size() == 2 && leptonFlavourCorrJetIso15 == \"Muons\" && invMassCorrJetIso15 < 12  && invMassCorrJetIso15 > 0.4 && !(invMassCorrJetIso15 > 3 && invMassCorrJetIso15 < 3.2) && !(invMassCorrJetIso15 > 0.75 && invMassCorrJetIso15 < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSignCorrJetIso15 == 0 && isoCrCorrJetIso15 == 0 && !tautauCorrJetIso15", "sc" : "sameSignCorrJetIso15 == 0 && isoCrCorrJetIso15 == 1"},
        #{"name":"mindr01", "title": "MinDr >= 0.1 && isoCr == 1", "condition" : "(BTagsDeepMedium == 0 && twoLeptonsCorrJetIso15 == 1 && MHT >= 220 &&  MET >= 200 && @leptonsCorrJetIso15.size() == 2 && leptonFlavourCorrJetIso15 == \"Muons\" && invMassCorrJetIso15 < 12  && invMassCorrJetIso15 > 0.4 && !(invMassCorrJetIso15 > 3 && invMassCorrJetIso15 < 3.2) && !(invMassCorrJetIso15 > 0.75 && invMassCorrJetIso15 < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSignCorrJetIso15 == 0 && isoCrCorrJetIso15 == 0 && !tautauCorrJetIso15", "sc" : "sameSignCorrJetIso15 == 0 && isoCrCorrJetIso15 == 1 && isoCrMinDrCorrJetIso15 >= 0.1"},
        #{"name":"mindr02", "title": "MinDr >= 0.2 && isoCr == 1", "condition" : "(BTagsDeepMedium == 0 && twoLeptonsCorrJetIso15 == 1 && MHT >= 220 &&  MET >= 200 && @leptonsCorrJetIso15.size() == 2 && leptonFlavourCorrJetIso15 == \"Muons\" && invMassCorrJetIso15 < 12  && invMassCorrJetIso15 > 0.4 && !(invMassCorrJetIso15 > 3 && invMassCorrJetIso15 < 3.2) && !(invMassCorrJetIso15 > 0.75 && invMassCorrJetIso15 < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSignCorrJetIso15 == 0 && isoCrCorrJetIso15 == 0 && !tautauCorrJetIso15", "sc" : "sameSignCorrJetIso15 == 0 && isoCrCorrJetIso15 == 1 && isoCrMinDrCorrJetIso15 >= 0.2"},
        #{"name":"isocr011", "title": "MinDr >= 0.1 && isoCr >= 1", "condition" : "(BTagsDeepMedium == 0 && twoLeptonsCorrJetIso15 == 1 && MHT >= 220 &&  MET >= 200 && @leptonsCorrJetIso15.size() == 2 && leptonFlavourCorrJetIso15 == \"Muons\" && invMassCorrJetIso15 < 12  && invMassCorrJetIso15 > 0.4 && !(invMassCorrJetIso15 > 3 && invMassCorrJetIso15 < 3.2) && !(invMassCorrJetIso15 > 0.75 && invMassCorrJetIso15 < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSignCorrJetIso15 == 0 && isoCrCorrJetIso15 == 0 && !tautauCorrJetIso15", "sc" : "sameSignCorrJetIso15 == 0 && isoCrCorrJetIso15 >= 1 && isoCrMinDrCorrJetIso15 >= 0.1"},
        #{"name":"isocr02", "title": "MinDr >= 0.2 && isoCr >= 1", "condition" : "(BTagsDeepMedium == 0 && twoLeptonsCorrJetIso15 == 1 && MHT >= 220 &&  MET >= 200 && @leptonsCorrJetIso15.size() == 2 && leptonFlavourCorrJetIso15 == \"Muons\" && invMassCorrJetIso15 < 12  && invMassCorrJetIso15 > 0.4 && !(invMassCorrJetIso15 > 3 && invMassCorrJetIso15 < 3.2) && !(invMassCorrJetIso15 > 0.75 && invMassCorrJetIso15 < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSignCorrJetIso15 == 0 && isoCrCorrJetIso15 == 0 && !tautauCorrJetIso15", "sc" : "sameSignCorrJetIso15 == 0 && isoCrCorrJetIso15 >= 1 && isoCrMinDrCorrJetIso15 >= 0.2"},
        #{"name":"nj", "title": "NJ >= 2", "condition" : "(NJets >= 2 && BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0 && !tautau", "sc" : "sameSign == 0 && isoCr >= 1 && !tautau"},
        #{"name": "bdt", "title": "bdt >= 0.1", "condition" : "(dilepBDT >= 0.1 && BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0 && !tautau", "sc" : "sameSign == 0 && isoCr >= 1 && !tautau"},
        
        #{"name":"none", "title": "None", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0 && !tautau", "sc" : "sameSign == 0 && isoCr >= 1 && !tautau"},
    ]

class dilepton_muons_bg_isocr_inclusive_corrjetiso_no_norm(dilepton_muons_bg_isocr_inclusive_corrjetiso):
    normalise = False
    load_histrograms_from_file = True

class dilepton_muons_bg_isocr_tautau_corrjetiso15(dilepton_muons_bg_isocr_inclusive_corrjetiso):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_tautau_corrjetiso15.root"
    choose_bg_categories_list = ["tautau"]
    choose_bg_categories = True
    cuts = [
        #{"name":"none", "title": "None", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0", "sc" : "sameSign == 0 && isoCr >= 1 && " + dilepton_muons_bg_isocr.bgReTagging["tautau"]},
        {"name":"none", "title": "None", "condition" : "(BTagsDeepMedium == 0 && twoLeptonsCorrJetIso15 == 1 && MHT >= 220 &&  MET >= 200 && @leptonsCorrJetIso15.size() == 2 && leptonFlavourCorrJetIso15 == \"Muons\" && invMassCorrJetIso15 < 12  && invMassCorrJetIso15 > 0.4 && !(invMassCorrJetIso15 > 3 && invMassCorrJetIso15 < 3.2) && !(invMassCorrJetIso15 > 0.75 && invMassCorrJetIso15 < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSignCorrJetIso15 == 0 && isoCrCorrJetIso15 == 0", "sc" : "sameSignCorrJetIso15 == 0 && isoCrCorrJetIso15 >= 1 && " + dilepton_muons_bg_isocr_inclusive_corrjetiso.bgReTagging["tautau"] + " == 1"},
    ]

class dilepton_muons_bg_isocr_tautau_corrjetiso15_no_norm(dilepton_muons_bg_isocr_tautau_corrjetiso15):
    normalise = False
    load_histrograms_from_file = True

class dilepton_muons_bg_isocr_notautau_corrjetiso_15_0_6(dilepton_muons_bg_isocr_notautau_corrjetiso):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_notautau_corrjetiso_15_0_6.root"
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/type_sum"

class dilepton_muons_bg_isocr_notautau_corrjetiso_15_0_6_no_norm(dilepton_muons_bg_isocr_notautau_corrjetiso_15_0_6):
    normalise = False
    load_histrograms_from_file = True

class dilepton_muons_bg_isocr_notautau_corrjetiso_10(dilepton_muons_bg_isocr_notautau_corrjetiso):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_notautau_corrjetiso_10.root"
    bgReTagging = bgReTaggingCollectedNoTauTauCorrJetIso10
    cuts = [
        {"name":"none", "title": "None", "condition" : "(BTagsDeepMedium == 0 && twoLeptonsCorrJetIso10 == 1 && MHT >= 220 &&  MET >= 200 && @leptonsCorrJetIso10.size() == 2 && leptonFlavourCorrJetIso10 == \"Muons\" && invMassCorrJetIso10 < 12  && invMassCorrJetIso10 > 0.4 && !(invMassCorrJetIso10 > 3 && invMassCorrJetIso10 < 3.2) && !(invMassCorrJetIso10 > 0.75 && invMassCorrJetIso10 < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSignCorrJetIso10 == 0 && isoCrCorrJetIso10 == 0 && !tautauCorrJetIso10", "sc" : "sameSignCorrJetIso10 == 0 && isoCrCorrJetIso10 >= 1 && !tautauCorrJetIso10"},
        {"name":"isocr1", "title": "isoCr == 1", "condition" : "(BTagsDeepMedium == 0 && twoLeptonsCorrJetIso10 == 1 && MHT >= 220 &&  MET >= 200 && @leptonsCorrJetIso10.size() == 2 && leptonFlavourCorrJetIso10 == \"Muons\" && invMassCorrJetIso10 < 12  && invMassCorrJetIso10 > 0.4 && !(invMassCorrJetIso10 > 3 && invMassCorrJetIso10 < 3.2) && !(invMassCorrJetIso10 > 0.75 && invMassCorrJetIso10 < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSignCorrJetIso10 == 0 && isoCrCorrJetIso10 == 0 && !tautauCorrJetIso10", "sc" : "sameSignCorrJetIso10 == 0 && isoCrCorrJetIso10 == 1 && !tautauCorrJetIso10"},
        {"name":"mindr01", "title": "MinDr >= 0.1 && isoCr == 1", "condition" : "(BTagsDeepMedium == 0 && twoLeptonsCorrJetIso10 == 1 && MHT >= 220 &&  MET >= 200 && @leptonsCorrJetIso10.size() == 2 && leptonFlavourCorrJetIso10 == \"Muons\" && invMassCorrJetIso10 < 12  && invMassCorrJetIso10 > 0.4 && !(invMassCorrJetIso10 > 3 && invMassCorrJetIso10 < 3.2) && !(invMassCorrJetIso10 > 0.75 && invMassCorrJetIso10 < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSignCorrJetIso10 == 0 && isoCrCorrJetIso10 == 0 && !tautauCorrJetIso10", "sc" : "sameSignCorrJetIso10 == 0 && isoCrCorrJetIso10 == 1 && !tautauCorrJetIso10 && isoCrMinDrCorrJetIso10 >= 0.1"},
        {"name":"mindr02", "title": "MinDr >= 0.2 && isoCr == 1", "condition" : "(BTagsDeepMedium == 0 && twoLeptonsCorrJetIso10 == 1 && MHT >= 220 &&  MET >= 200 && @leptonsCorrJetIso10.size() == 2 && leptonFlavourCorrJetIso10 == \"Muons\" && invMassCorrJetIso10 < 12  && invMassCorrJetIso10 > 0.4 && !(invMassCorrJetIso10 > 3 && invMassCorrJetIso10 < 3.2) && !(invMassCorrJetIso10 > 0.75 && invMassCorrJetIso10 < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSignCorrJetIso10 == 0 && isoCrCorrJetIso10 == 0 && !tautauCorrJetIso10", "sc" : "sameSignCorrJetIso10 == 0 && isoCrCorrJetIso10 == 1 && !tautauCorrJetIso10 && isoCrMinDrCorrJetIso10 >= 0.2"},
        {"name":"isocr011", "title": "MinDr >= 0.1 && isoCr >= 1", "condition" : "(BTagsDeepMedium == 0 && twoLeptonsCorrJetIso10 == 1 && MHT >= 220 &&  MET >= 200 && @leptonsCorrJetIso10.size() == 2 && leptonFlavourCorrJetIso10 == \"Muons\" && invMassCorrJetIso10 < 12  && invMassCorrJetIso10 > 0.4 && !(invMassCorrJetIso10 > 3 && invMassCorrJetIso10 < 3.2) && !(invMassCorrJetIso10 > 0.75 && invMassCorrJetIso10 < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSignCorrJetIso10 == 0 && isoCrCorrJetIso10 == 0 && !tautauCorrJetIso10", "sc" : "sameSignCorrJetIso10 == 0 && isoCrCorrJetIso10 >= 1 && !tautauCorrJetIso10 && isoCrMinDrCorrJetIso10 >= 0.1"},
        {"name":"isocr02", "title": "MinDr >= 0.2 && isoCr >= 1", "condition" : "(BTagsDeepMedium == 0 && twoLeptonsCorrJetIso10 == 1 && MHT >= 220 &&  MET >= 200 && @leptonsCorrJetIso10.size() == 2 && leptonFlavourCorrJetIso10 == \"Muons\" && invMassCorrJetIso10 < 12  && invMassCorrJetIso10 > 0.4 && !(invMassCorrJetIso10 > 3 && invMassCorrJetIso10 < 3.2) && !(invMassCorrJetIso10 > 0.75 && invMassCorrJetIso10 < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSignCorrJetIso10 == 0 && isoCrCorrJetIso10 == 0 && !tautauCorrJetIso10", "sc" : "sameSignCorrJetIso10 == 0 && isoCrCorrJetIso10 >= 1 && !tautauCorrJetIso10 && isoCrMinDrCorrJetIso10 >= 0.2"},
        #{"name":"nj", "title": "NJ >= 2", "condition" : "(NJets >= 2 && BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0 && !tautau", "sc" : "sameSign == 0 && isoCr >= 1 && !tautau"},
        #{"name": "bdt", "title": "bdt >= 0.1", "condition" : "(dilepBDT >= 0.1 && BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0 && !tautau", "sc" : "sameSign == 0 && isoCr >= 1 && !tautau"},
        
        #{"name":"none", "title": "None", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0 && !tautau", "sc" : "sameSign == 0 && isoCr >= 1 && !tautau"},
    ]
    histograms_defs = [
        { "obs" : "invMassCorrJetIso10", "minX" : 0, "maxX" : 13, "bins" : 6, "blind" : [4,None]},# "customBins"  : [0,2,4,6,10,12] },
        { "obs" : "dilepBDTCorrJetIso10", "minX" : -1, "maxX" : 1, "bins" : 6, "blind" : [None,0.1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        { "obs" : "isoCrMinDrCorrJetIso10", "minX" : 0, "maxX" : 0.4, "bins" : 8},
        { "obs" : "deltaRCorrJetIso10", "minX" : 0, "maxX" : 3.5, "bins" : 8},
        { "obs" : "dilepHtCorrJetIso10", "minX" : 200, "maxX" : 800, "bins" : 8},
        { "obs" : "dileptonPtCorrJetIso10", "minX" : 0, "maxX" : 30, "bins" : 8},
        { "obs" : "MHT", "minX" : 220, "maxX" : 800, "bins" : 8},
        { "obs" : "MinDeltaPhiMhtJets", "minX" : 0, "maxX" : 3.5, "bins" : 8},
        { "obs" : "leptonsCorrJetIso10[0].Pt()", "minX" : 0, "maxX" : 20, "bins" : 8},
        { "obs" : "deltaPhiMetLepton1CorrJetIso10", "minX" : 0, "maxX" : 3.5, "bins" : 8},
        { "obs" : "mt1CorrJetIso10", "minX" : 0, "maxX" : 200, "bins" : 8},
        { "obs" : "leptonsCorrJetIso10[0].Eta()", "minX" : -2.4, "maxX" : 2.4, "bins" : 8},
        { "obs" : "NJets", "minX" : 0, "maxX" : 6, "bins" : 6},
        { "obs" : "deltaPhiMetLepton2CorrJetIso10", "minX" : 0, "maxX" : 3.5, "bins" : 8},
        { "obs" : "LeadingJetPt", "minX" : 0, "maxX" : 500, "bins" : 8},
        { "obs" : "LeadingJet.Eta()", "minX" : -2.4, "maxX" : 2.4, "bins" : 8},
        { "obs" : "deltaEtaCorrJetIso10", "minX" : 0, "maxX" : 5, "bins" : 8},
        { "obs" : "HT", "minX" : 0, "maxX" : 500, "bins" : 8},
        { "obs" : "leptonsCorrJetIso10[0].Phi()", "minX" : 0, "maxX" : 3.5, "bins" : 8},
    ]

class dilepton_muons_bg_isocr_notautau_corrjetiso_10_no_norm(dilepton_muons_bg_isocr_notautau_corrjetiso_10):
    normalise = False
    load_histrograms_from_file = True

class dilepton_muons_bg_isocr_inclusive_corrjetiso_10(dilepton_muons_bg_isocr_notautau_corrjetiso_10):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_inclusive_corrjetiso_10.root"
    bgReTagging = bgReTaggingCollectedCorrJetIso10
    cuts = [
        {"name":"none", "title": "None", "condition" : "(BTagsDeepMedium == 0 && twoLeptonsCorrJetIso10 == 1 && MHT >= 220 &&  MET >= 200 && @leptonsCorrJetIso10.size() == 2 && leptonFlavourCorrJetIso10 == \"Muons\" && invMassCorrJetIso10 < 12  && invMassCorrJetIso10 > 0.4 && !(invMassCorrJetIso10 > 3 && invMassCorrJetIso10 < 3.2) && !(invMassCorrJetIso10 > 0.75 && invMassCorrJetIso10 < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSignCorrJetIso10 == 0 && isoCrCorrJetIso10 == 0", "sc" : "sameSignCorrJetIso10 == 0 && isoCrCorrJetIso10 >= 1"},
    ]

class dilepton_muons_bg_isocr_notautau_corrjetiso_10_0_6(dilepton_muons_bg_isocr_notautau_corrjetiso_10):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_notautau_corrjetiso_10_0_6.root"
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/type_sum"

class dilepton_muons_bg_isocr_notautau_corrjetiso_mindr(dilepton_muons_bg_isocr_notautau_corrjetiso):
    cuts = [
        {"name":"none", "title": "None", "condition" : "(BTagsDeepMedium == 0 && twoLeptonsCorrJetIso15 == 1 && MHT >= 220 &&  MET >= 200 && @leptonsCorrJetIso15.size() == 2 && leptonFlavourCorrJetIso15 == \"Muons\" && invMassCorrJetIso15 < 12  && invMassCorrJetIso15 > 0.4 && !(invMassCorrJetIso15 > 3 && invMassCorrJetIso15 < 3.2) && !(invMassCorrJetIso15 > 0.75 && invMassCorrJetIso15 < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSignCorrJetIso15 == 0 && isoCrCorrJetIso15 > 0 && !tautauCorrJetIso15", "sc" : "sameSignCorrJetIso15 == 0 && isoCrCorrJetIso15 >= 1 && !tautauCorrJetIso15"},
    ]
    histograms_defs = [
        { "obs" : "isoCrMinDrCorrJetIso15", "minX" : 0, "maxX" : 0.4, "bins" : 8},
    ]
    plot_sc = False
    plot_ratio = False
    normalise = False

class dilepton_muons_bg_isocr_notautau_corrjetiso_10_0_6_no_norm(dilepton_muons_bg_isocr_notautau_corrjetiso_10_0_6):
    normalise = False
    load_histrograms_from_file = True

class dilepton_muons_bg_isocr_notautau_working_02_corrjetiso(dilepton_muons_bg_isocr):
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_dr_0.2_working/sum/type_sum"
    bgReTagging = bgReTaggingCollectedNoTauTauCorrJetIso
    cuts = [
        {"name":"none", "title": "None", "condition" : "(BTagsDeepMedium == 0 && twoLeptonsCorrJetIso15 == 1 && MHT >= 220 &&  MET >= 200 && @leptonsCorrJetIso15.size() == 2 && leptonFlavourCorrJetIso15 == \"Muons\" && invMassCorrJetIso15 < 12  && invMassCorrJetIso15 > 0.4 && !(invMassCorrJetIso15 > 3 && invMassCorrJetIso15 < 3.2) && !(invMassCorrJetIso15 > 0.75 && invMassCorrJetIso15 < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSignCorrJetIso15 == 0 && isoCrCorrJetIso15 == 0 && !tautauCorrJetIso15", "sc" : "sameSignCorrJetIso15 == 0 && isoCrCorrJetIso15 >= 1 && !tautauCorrJetIso15"},
        {"name":"isocr1", "title": "isoCr == 1", "condition" : "(BTagsDeepMedium == 0 && twoLeptonsCorrJetIso15 == 1 && MHT >= 220 &&  MET >= 200 && @leptonsCorrJetIso15.size() == 2 && leptonFlavourCorrJetIso15 == \"Muons\" && invMassCorrJetIso15 < 12  && invMassCorrJetIso15 > 0.4 && !(invMassCorrJetIso15 > 3 && invMassCorrJetIso15 < 3.2) && !(invMassCorrJetIso15 > 0.75 && invMassCorrJetIso15 < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSignCorrJetIso15 == 0 && isoCrCorrJetIso15 == 0 && !tautauCorrJetIso15", "sc" : "sameSignCorrJetIso15 == 0 && isoCrCorrJetIso15 == 1 && !tautauCorrJetIso15"},
        #{"name":"isocr1", "title": "isoCr == 1", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0", "sc" : "sameSign == 0 && isoCr == 1  && !tautau"},
        #{"name":"mindr01", "title": "MinDr >= 0.1 && isoCr == 1", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0", "sc" : "sameSign == 0 && isoCr == 1 && isoCrMinDr >= 0.1"},
        #{"name":"mindr02", "title": "MinDr >= 0.2 && isoCr == 1", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0", "sc" : "sameSign == 0 && isoCr == 1 && isoCrMinDr >= 0.2"},
        
        #{"name":"isocr02", "title": "MinDr >= 0.1", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0 && !tautau", "sc" : "sameSign == 0 && isoCr >= 1 && !tautau && isoCrMinDr >= 0.1"},
        #{"name":"isocr02", "title": "MinDr >= 0.2", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0 && !tautau", "sc" : "sameSign == 0 && isoCr >= 1 && !tautau && isoCrMinDr >= 0.2"},
        #{"name":"nj", "title": "NJ >= 2", "condition" : "(NJets >= 2 && BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0 && !tautau", "sc" : "sameSign == 0 && isoCr >= 1 && !tautau"},
        #{"name": "bdt", "title": "bdt >= 0.1", "condition" : "(dilepBDT >= 0.1 && BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0 && !tautau", "sc" : "sameSign == 0 && isoCr >= 1 && !tautau"},
        
        #{"name":"none", "title": "None", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0 && !tautau", "sc" : "sameSign == 0 && isoCr >= 1 && !tautau"},
    ]
    histograms_defs = [
        { "obs" : "invMassCorrJetIso15", "minX" : 0, "maxX" : 13, "bins" : 6, "blind" : [4,None]},# "customBins"  : [0,2,4,6,10,12] },
        { "obs" : "dilepBDTCorrJetIso15", "minX" : -1, "maxX" : 1, "bins" : 6, "blind" : [None,0.1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        #{ "obs" : "isoCrMinDr", "minX" : 0, "maxX" : 0.4, "bins" : 8},
        { "obs" : "deltaRCorrJetIso15", "minX" : 0, "maxX" : 3.5, "bins" : 8},
        { "obs" : "dilepHtCorrJetIso15", "minX" : 200, "maxX" : 800, "bins" : 8},
        { "obs" : "dileptonPtCorrJetIso15", "minX" : 0, "maxX" : 30, "bins" : 8},
        { "obs" : "MHT", "minX" : 220, "maxX" : 800, "bins" : 8},
        { "obs" : "MinDeltaPhiMhtJets", "minX" : 0, "maxX" : 3.5, "bins" : 8},
        { "obs" : "leptonsCorrJetIso15[0].Pt()", "minX" : 0, "maxX" : 20, "bins" : 8},
        { "obs" : "deltaPhiMetLepton1CorrJetIso15", "minX" : 0, "maxX" : 3.5, "bins" : 8},
        { "obs" : "mt1CorrJetIso15", "minX" : 0, "maxX" : 200, "bins" : 8},
        { "obs" : "leptonsCorrJetIso15[0].Eta()", "minX" : -2.4, "maxX" : 2.4, "bins" : 8},
        { "obs" : "NJets", "minX" : 0, "maxX" : 6, "bins" : 6},
        { "obs" : "deltaPhiMetLepton2CorrJetIso15", "minX" : 0, "maxX" : 3.5, "bins" : 8},
        { "obs" : "LeadingJetPt", "minX" : 0, "maxX" : 500, "bins" : 8},
        { "obs" : "LeadingJet.Eta()", "minX" : -2.4, "maxX" : 2.4, "bins" : 8},
        { "obs" : "deltaEtaCorrJetIso15", "minX" : 0, "maxX" : 5, "bins" : 8},
        { "obs" : "HT", "minX" : 0, "maxX" : 500, "bins" : 8},
        { "obs" : "leptonsCorrJetIso15[0].Phi()", "minX" : 0, "maxX" : 3.5, "bins" : 8},
    ]

class dilepton_muons_bg_isocr_res(dilepton_muons_bg_isocr):
    choose_bg_categories = True
    choose_bg_files_for_sc = True
    choose_bg_categories_list = ["resonances"]
    cuts = [
        {"name":"none", "title": "None", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0", "sc" : "sameSign == 0 && isoCr >= 1 && " + dilepton_muons_bg_isocr.bgReTagging["resonances"]},
        {"name":"isocr", "title": "MinDr >= 0.2", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0 && !tautau", "sc" : "sameSign == 0 && isoCr >= 1 && isoCrMinDr >= 0.2 && " + dilepton_muons_bg_isocr.bgReTagging["resonances"]},
        #{"name":"nj", "title": "NJ >= 2", "condition" : "(NJets >= 2 && BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0", "sc" : "sameSign == 0 && isoCr >= 1 && " + dilepton_muons_bg_isocr.bgReTagging["resonances"]},
        #{"name": "bdt", "title": "bdt >= 0.1", "condition" : "(dilepBDT >= 0.1 && BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0", "sc" : "sameSign == 0 && isoCr >= 1 && " + dilepton_muons_bg_isocr.bgReTagging["resonances"]},
    ]

class dilepton_muons_bg_isocr_tc(dilepton_muons_bg_isocr_res):
    choose_bg_categories_list = ["tc"]
    cuts = [
        {"name":"none", "title": "None", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0", "sc" : "sameSign == 0 && isoCr >= 1 && " + dilepton_muons_bg_isocr.bgReTagging["tc"]},
        {"name":"isocr", "title": "MinDr >= 0.2", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0 && !tautau", "sc" : "sameSign == 0 && isoCr >= 1 && isoCrMinDr >= 0.2 && " + dilepton_muons_bg_isocr.bgReTagging["tc"]},
        {"name":"nj", "title": "NJ >= 2", "condition" : "(NJets >= 2 && BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0", "sc" : "sameSign == 0 && isoCr >= 1 && " + dilepton_muons_bg_isocr.bgReTagging["tc"]},
        {"name": "bdt", "title": "bdt >= 0.1", "condition" : "(dilepBDT >= 0.1 && BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0", "sc" : "sameSign == 0 && isoCr >= 1 && " + dilepton_muons_bg_isocr.bgReTagging["tc"]},
    ]

class dilepton_muons_bg_isocr_tautau(dilepton_muons_bg_isocr_tc):
    choose_bg_categories_list = ["tautau"]
    cuts = [
        {"name":"none", "title": "None", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0", "sc" : "sameSign == 0 && isoCr >= 1 && " + dilepton_muons_bg_isocr.bgReTagging["tautau"]},
        {"name":"isocr", "title": "MinDr >= 0.2", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0 && !tautau", "sc" : "sameSign == 0 && isoCr >= 1 && isoCrMinDr >= 0.2 && " + dilepton_muons_bg_isocr.bgReTagging["tautau"]},
        #{"name":"nj", "title": "NJ >= 2", "condition" : "(NJets >= 2 && BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0", "sc" : "sameSign == 0 && isoCr >= 1 && " + dilepton_muons_bg_isocr.bgReTagging["tautau"]},
        #{"name": "bdt", "title": "bdt >= 0.1", "condition" : "(dilepBDT >= 0.1 && BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0", "sc" : "sameSign == 0 && isoCr >= 1 && " + dilepton_muons_bg_isocr.bgReTagging["tautau"]},
    ]

class dilepton_muons_bg_isocr_other(dilepton_muons_bg_isocr_tc):
    choose_bg_categories_list = ["other"]
    cuts = [
        {"name":"none", "title": "None", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0", "sc" : "sameSign == 0 && isoCr >= 1 && " + dilepton_muons_bg_isocr.bgReTagging["other"]},
        {"name":"isocr", "title": "MinDr >= 0.2", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0 && !tautau", "sc" : "sameSign == 0 && isoCr >= 1 && isoCrMinDr >= 0.2 && " + dilepton_muons_bg_isocr.bgReTagging["other"]},
        #{"name":"nj", "title": "NJ >= 2", "condition" : "(NJets >= 2 && BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0", "sc" : "sameSign == 0 && isoCr >= 1 && " + dilepton_muons_bg_isocr.bgReTagging["other"]},
        #{"name": "bdt", "title": "bdt >= 0.1", "condition" : "(dilepBDT >= 0.1 && BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0", "sc" : "sameSign == 0 && isoCr >= 1 && " + dilepton_muons_bg_isocr.bgReTagging["other"]},
    ]

class dilepton_muons_bg_isocr_nbody(dilepton_muons_bg_isocr_tc):
    choose_bg_categories_list = ["nbody"]
    cuts = [
        {"name":"none", "title": "None", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0", "sc" : "sameSign == 0 && isoCr >= 1 && " + dilepton_muons_bg_isocr.bgReTagging["nbody"]},
        {"name":"isocr", "title": "MinDr >= 0.2", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0 && !tautau", "sc" : "sameSign == 0 && isoCr >= 1 && isoCrMinDr >= 0.2 && " + dilepton_muons_bg_isocr.bgReTagging["nbody"]},
        #{"name":"nj", "title": "NJ >= 2", "condition" : "(NJets >= 2 && BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0", "sc" : "sameSign == 0 && isoCr >= 1 && " + dilepton_muons_bg_isocr.bgReTagging["nbody"]},
        #{"name": "bdt", "title": "bdt >= 0.1", "condition" : "(dilepBDT >= 0.1 && BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0", "sc" : "sameSign == 0 && isoCr >= 1 && " + dilepton_muons_bg_isocr.bgReTagging["nbody"]},
    ]

class dilepton_muons_bg_isocr_fake(dilepton_muons_bg_isocr_tc):
    choose_bg_categories_list = ["fake"]
    cuts = [
        {"name":"none", "title": "None", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0", "sc" : "sameSign == 0 && isoCr >= 1 && " + dilepton_muons_bg_isocr.bgReTagging["fake"]},
        {"name":"isocr", "title": "MinDr >= 0.2", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0 && !tautau", "sc" : "sameSign == 0 && isoCr >= 1 && isoCrMinDr >= 0.2 && " + dilepton_muons_bg_isocr.bgReTagging["fake"]},
        #{"name":"nj", "title": "NJ >= 2", "condition" : "(NJets >= 2 && BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0", "sc" : "sameSign == 0 && isoCr >= 1 && " + dilepton_muons_bg_isocr.bgReTagging["fake"]},
        #{"name": "bdt", "title": "bdt >= 0.1", "condition" : "(dilepBDT >= 0.1 && BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0", "sc" : "sameSign == 0 && isoCr >= 1 && " + dilepton_muons_bg_isocr.bgReTagging["fake"]},
    ]

#dilepton_muons_bg_isocr_sm dilepton_muons_bg_isocr_sm_wjets dilepton_muons_bg_isocr_sm_ttjets dilepton_muons_bg_isocr_sm_dy dilepton_muons_bg_isocr_sm_zjets dilepton_muons_bg_isocr_sm_rare dilepton_muons_bg_isocr_sm_diboson

class dilepton_muons_bg_isocr_sm(dilepton_muons_bg_isocr):
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_0.4/sum/type_sum"
    load_histrograms_from_file = False
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_sm.root"
    cuts = [
        {"name":"none", "title": "None", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0", "sc" : "sameSign == 0 && isoCr >= 1"},
        {"name":"mindr", "title": "MinDr >= 0.2", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0", "sc" : "sameSign == 0 && isoCr >= 1 && isoCrMinDr >= 0.2"},
        #{"name":"nj", "title": "NJ >= 2", "condition" : "(NJets >= 2 && BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0", "sc" : "sameSign == 0 && isoCr >= 1"},
        #{"name": "bdt", "title": "bdt >= 0.1", "condition" : "(dilepBDT >= 0.1 && BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0", "sc" : "sameSign == 0 && isoCr >= 1"},
    ]
    plot_sc = True
    plot_custom_ratio = False
    customRatios = []
    plot_ratio = True
    normalise = True
    normalise_each_bg = False
    bg_retag = False
    nostack = False
    sc_label = "Jet Iso #Delta_{}R CR"
    sc_ratio_label = "cr"

class dilepton_muons_bg_isocr_sm_corrjetiso_15(dilepton_muons_bg_isocr_sm):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_sm_corrjetiso_15.root"
    cuts = [
        {"name":"none", "title": "None", "condition" : "(BTagsDeepMedium == 0 && twoLeptonsCorrJetIso15 == 1 && MHT >= 220 &&  MET >= 200 && @leptonsCorrJetIso15.size() == 2 && leptonFlavourCorrJetIso15 == \"Muons\" && invMassCorrJetIso15 < 12  && invMassCorrJetIso15 > 0.4 && !(invMassCorrJetIso15 > 3 && invMassCorrJetIso15 < 3.2) && !(invMassCorrJetIso15 > 0.75 && invMassCorrJetIso15 < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSignCorrJetIso15 == 0 && isoCrCorrJetIso15 == 0 && !tautauCorrJetIso15", "sc" : "sameSignCorrJetIso15 == 0 && isoCrCorrJetIso15 >= 1 && !tautauCorrJetIso15"},
    ]
    histograms_defs = [
        { "obs" : "invMassCorrJetIso15", "minX" : 0, "maxX" : 13, "bins" : 6, "blind" : [4,None]},# "customBins"  : [0,2,4,6,10,12] },
        { "obs" : "dilepBDTCorrJetIso15", "minX" : -1, "maxX" : 1, "bins" : 6, "blind" : [None,0.1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
        { "obs" : "isoCrMinDrCorrJetIso15", "minX" : 0, "maxX" : 0.4, "bins" : 8},
        { "obs" : "deltaRCorrJetIso15", "minX" : 0, "maxX" : 3.5, "bins" : 8},
        { "obs" : "dilepHtCorrJetIso15", "minX" : 200, "maxX" : 800, "bins" : 8},
        { "obs" : "dileptonPtCorrJetIso15", "minX" : 0, "maxX" : 30, "bins" : 8},
        { "obs" : "MHT", "minX" : 220, "maxX" : 800, "bins" : 8},
        { "obs" : "MinDeltaPhiMhtJets", "minX" : 0, "maxX" : 3.5, "bins" : 8},
        { "obs" : "leptonsCorrJetIso15[0].Pt()", "minX" : 0, "maxX" : 20, "bins" : 8},
        { "obs" : "deltaPhiMetLepton1CorrJetIso15", "minX" : 0, "maxX" : 3.5, "bins" : 8},
        { "obs" : "mt1CorrJetIso15", "minX" : 0, "maxX" : 200, "bins" : 8},
        { "obs" : "leptonsCorrJetIso15[0].Eta()", "minX" : -2.4, "maxX" : 2.4, "bins" : 8},
        { "obs" : "NJets", "minX" : 0, "maxX" : 6, "bins" : 6},
        { "obs" : "deltaPhiMetLepton2CorrJetIso15", "minX" : 0, "maxX" : 3.5, "bins" : 8},
        { "obs" : "LeadingJetPt", "minX" : 0, "maxX" : 500, "bins" : 8},
        { "obs" : "LeadingJet.Eta()", "minX" : -2.4, "maxX" : 2.4, "bins" : 8},
        { "obs" : "deltaEtaCorrJetIso15", "minX" : 0, "maxX" : 5, "bins" : 8},
        { "obs" : "HT", "minX" : 0, "maxX" : 500, "bins" : 8},
        { "obs" : "leptonsCorrJetIso15[0].Phi()", "minX" : 0, "maxX" : 3.5, "bins" : 8},
    ]
    
class dilepton_muons_bg_isocr_sm_mindr(dilepton_muons_bg_isocr_sm):
    plot_sc = False
    plot_ratio = False
    cuts = [
        #{"name":"none", "title": "None", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0", "sc" : "sameSign == 0 && isoCr >= 1"},
        {"name":"none", "title": "None", "condition" : "(BTagsDeepMedium == 0 && MHT >= 220 &&  MET >= 200 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "", "sc" : "sameSign == 0 && isoCr >= 1"},
        #{"name":"mindr", "title": "MinDr >= 0.2", "condition" : "(BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0", "sc" : "sameSign == 0 && isoCr >= 1 && isoCrMinDr >= 0.2"},
        #{"name":"nj", "title": "NJ >= 2", "condition" : "(NJets >= 2 && BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0", "sc" : "sameSign == 0 && isoCr >= 1"},
        #{"name": "bdt", "title": "bdt >= 0.1", "condition" : "(dilepBDT >= 0.1 && BTagsDeepMedium == 0 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0 && isoCr == 0", "sc" : "sameSign == 0 && isoCr >= 1"},
    ]
    histograms_defs = [
        { "obs" : "Muons_minDeltaRJets", "minX" : 0, "maxX" : 3, "bins" : 30, "blind" : [4,None], "condition" : "Muons_passCorrJetIso15 == 1 && Jets[Muons_closestJet].Pt() > 15 && Jets[Muons_closestJet].Pt() < 30"},# "customBins"  : [0,2,4,6,10,12] },
        { "obs" : "Muons_minDeltaRJets_cr", "formula": "Muons_minDeltaRJets" ,"minX" : 0, "maxX" : 3, "bins" : 30, "blind" : [4,None], "condition" : "Muons_passCorrJetIso15 == 0 && Jets[Muons_closestJet].Pt() > 15 && Jets[Muons_closestJet].Pt() < 30"},# "customBins"  : [0,2,4,6,10,12] },
    ]
    normalise = False
    

class dilepton_muons_bg_isocr_sm_wjets(dilepton_muons_bg_isocr_sm):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_sm_wjets.root"
    choose_bg_files = True
    choose_bg_files_list = ["WJetsToLNu"]
    
class dilepton_muons_bg_isocr_sm_ttjets(dilepton_muons_bg_isocr_sm_wjets):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_sm_ttjets.root"
    choose_bg_files_list = ["TTJets"]
    
class dilepton_muons_bg_isocr_sm_dy(dilepton_muons_bg_isocr_sm_wjets):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_sm_dy.root"
    choose_bg_files_list = ["DYJetsToLL"]

class dilepton_muons_bg_isocr_sm_zjets(dilepton_muons_bg_isocr_sm_wjets):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_sm_zjets.root"
    choose_bg_files_list = ["ZJetsToNuNu"]

class dilepton_muons_bg_isocr_sm_rare(dilepton_muons_bg_isocr_sm_wjets):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_sm_rare.root"
    choose_bg_files_list = ["Rare"]

class dilepton_muons_bg_isocr_sm_diboson(dilepton_muons_bg_isocr_sm_wjets):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_sm_diboson.root"
    choose_bg_files_list = ["DiBoson"]


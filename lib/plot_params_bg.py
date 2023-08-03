import sys
import os
from ROOT import *

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib"))

from plot_params_base import *
import plotutils
import analysis_selections

bgReTaggingFull = {
    "tc" : "tc%%% * (!tautau%%%)",
    "tautau" : "tautau%%%",
    "other" : "other%%% * (!tautau%%%) * (!omega%%%) * (!rho_0%%%) * (!eta%%%) * (!phi%%%) * (!eta_prime%%%) * (!j_psi%%%) * (!upsilon_1%%%) * (!upsilon_2%%%)",
    "omega" : "omega%%%",
    "rho" : "rho_0%%%",
    "eta" : "eta%%%",
    "phi" : "phi%%%",
    "etaprime" : "eta_prime%%%",
    "jpsi" : "j_psi%%%",
    "upsilon1" : "upsilon_1%%%",
    "upsilon2" : "upsilon_2%%%",
    "nbody" : "n_body%%% * (!tautau%%%)",
    "scother" : "sc%%% * (!tautau%%%) * (!omega%%%) * (!rho_0%%%) * (!eta%%%) * (!phi%%%) * (!eta_prime%%%) * (!j_psi%%%) * (!upsilon_1%%%) * (!upsilon_2%%%)",
    "fake" : "(rf%%% || ff%%%)",
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
    "other" : "other * (!tautau) * (!omega) * (!rho_0) * (!eta) * (!phi) * (!eta_prime) * (!j_psi) * (!upsilon_1) * (!upsilon_2)",
    "resonances" : "(sc || omega || rho_0 || eta || phi || eta_prime || j_psi || upsilon_1 || upsilon_2)",
    "nbody" : "n_body * (!tautau)",
    "fake" : "(rf || ff)",
}

bgReTaggingResonances = {
    #"tc" : "tc%%% * (!tautau%%%)",
    #"tautau" : "tautau%%%",
    #"other" : "other%%% * (!tautau%%%) * (!omega%%%) * (!rho_0%%%) * (!eta%%%) * (!phi%%%) * (!eta_prime%%%) * (!j_psi%%%) * (!upsilon_1%%%) * (!upsilon_2%%%)",
    "omega" : "omega%%%",
    "rho" : "rho_0%%%",
    "eta" : "eta%%%",
    "phi" : "phi%%%",
    "etaprime" : "eta_prime%%%",
    "jpsi" : "j_psi%%%",
    "upsilon1" : "upsilon_1%%%",
    "upsilon2" : "upsilon_2%%%",
    "nbody" : "n_body%%% * (!tautau%%%)",
    "scother" : "sc%%% * (!tautau%%%) * (!omega%%%) * (!rho_0%%%) * (!eta%%%) * (!phi%%%) * (!eta_prime%%%) * (!j_psi%%%) * (!upsilon_1%%%) * (!upsilon_2%%%)",
    #"fake" : "(rf%%% || ff%%%)",
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

# invMass veto
# invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81)

# FULL ZOO

class full_zoo(BaseParams):
    
    weightString = {
        'MET' : "Weight",
    }
    ignore_bg_files = ["TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root", "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root", "QCD"]
    histrograms_file = BaseParams.histograms_root_files_dir + "/full_zoo.root"
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/slim_sum/type_sum"
    save_histrograms_to_file = True
    load_histrograms_from_file = False 
    
    plot_signal = False
    
    plot_log_x = True
    plot_real_log_x = True
    plot_overflow = False
    
    jetIso = analysis_selections.jetIsos["Muons"]
    jetIso = "NoIso"
    
    calculatedLumi = {
        'MET' : analysis_selections.recommended_luminosities["2016"],
    }

    weightString = {
        'MET' : analysis_selections.full_sim_weights["2016"],
    }
    baseConditionsArr = [analysis_selections.common_preselection, analysis_selections.two_leptons_condition]
    #baseConditions = analysis_selections.injectValues(" && ".join(baseConditionsArr), "2016", "Muons")
    baseConditions = " && ".join(baseConditionsArr).replace("%%%", jetIso).replace("$$$", "Muons")

    
    cuts = [
        {"name":"none", "title": "None", "condition" : baseConditions, "baseline" : analysis_selections.two_leptons_opposite_sign, "sc" : analysis_selections.two_leptons_same_sign },
        #{"name":"bdt", "title": "BDT>0.1", "condition" : "(dilepBDT > 0.1 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12 && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0", "sc" : "sameSign == 1"},
    ]
    
    injectJetIsoToCuts(cuts, jetIso)
    
    histograms_defs = [
        { "obs" : "invMass%%%", "minX" : 0.1, "maxX" : 6, "bins" : 100 },
        #{ "obs" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 6 },
    ]
    
    injectJetIsoToHistograms(histograms_defs, jetIso)  
    
    bg_retag = True
    
    bgReTagging = bgReTaggingResonances
    injectJetIsoToMapValues(bgReTagging, jetIso)
    bgReTaggingOrder = bgReTaggingOrderFull
    bgReTaggingNames = bgReTaggingNamesFull
    plot_error = True

class sm_zoo(full_zoo):
    bg_retag = False

class zoo_all_even_bins(full_zoo):
    cuts = [
        {"name":"none", "title": "None", "condition" : "(twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12 && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0", "sc" : "sameSign == 1"},
    ]

class test_class(full_zoo):
    cuts = [
        {"name":"none", "title": "None", "condition" : "(twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12)", "baseline" : "sameSign == 0", "sc" : "sameSign == 1"},
    ]
    histograms_defs = [
        { "obs" : "invMass", "minX" : 0.1, "maxX" : 2, "bins" : 100, "blind" : [4,None] },
    ]
    bgReTagging = bgReTaggingResonances

class zoo(full_zoo):
    bgReTagging = bgReTaggingResonances

class zoo_all_electrons(full_zoo):
    cuts = [
        {"name":"none", "title": "None", "condition" : "(twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Electrons\" && invMass < 12 && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0", "sc" : "sameSign == 1"},
    ]

class zoo_electrons(zoo_all_electrons):
    bgReTagging = bgReTaggingResonances
    
class zoo_all_low_met(full_zoo):
    cuts = [
        {"name":"none", "title": "None", "condition" : "(twoLeptons == 1 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && BTagsDeepMedium == 0)", "baseline" : "sameSign == 0", "sc" : "sameSign == 1"},
        #{"name":"low-met", "title": "Low Met", "condition" : "(twoLeptons == 1 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0", "sc" : "sameSign == 1"},
        #{"name":"non-orth", "title": "Non Orth", "condition" : "(twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && dilepBDT > 0.1)", "baseline" : "sameSign == 0", "sc" : "sameSign == 1"},
        #{"name":"orth", "title": "Orth", "condition" : "(twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && dilepBDT > 0.1 && (leptons[1].Pt() <= 3.5 || deltaR <= 0.3))", "baseline" : "sameSign == 0", "sc" : "sameSign == 1"},
    ]
class zoo_all_low_met_all(full_zoo):
    cuts = [
        {"name":"none", "title": "None", "condition" : "(twoLeptons == 1 && @leptons.size() == 2 && invMass < 12  && BTagsDeepMedium == 0)", "baseline" : "sameSign == 0", "sc" : "sameSign == 1"},
        #{"name":"low-met", "title": "Low Met", "condition" : "(twoLeptons == 1 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0", "sc" : "sameSign == 1"},
        #{"name":"non-orth", "title": "Non Orth", "condition" : "(twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && dilepBDT > 0.1)", "baseline" : "sameSign == 0", "sc" : "sameSign == 1"},
        #{"name":"orth", "title": "Orth", "condition" : "(twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && dilepBDT > 0.1 && (leptons[1].Pt() <= 3.5 || deltaR <= 0.3))", "baseline" : "sameSign == 0", "sc" : "sameSign == 1"},
    ]


# zoo removal
#invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81)

class dilepton_muons_bg(BaseParams):
    signal_dir = signals
    signal_names = signalNames
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/type_sum"
    data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim/sum/"
    cuts = [
        {"name":"none", "title": "None", "condition" : "(twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0", "sc" : "sameSign == 1"},
        {"name":"no-tautau", "title": "No tautau", "condition" : "(!tautau && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0", "sc" : "sameSign == 1"},
        {"name":"bdt", "title": "BDT>0.1", "condition" : "(dilepBDT > 0.1 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12 && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0", "sc" : "sameSign == 1"},
        {"name":"bdt-no-tautau", "title": "BDT>0.1 && No tautau", "condition" : "(!tautau && dilepBDT > 0.1 && twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12 && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0", "sc" : "sameSign == 1"},
        #{"name":"low-met", "title": "Low Met", "condition" : "(twoLeptons == 1 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "sameSign == 0", "sc" : "sameSign == 1"},
        #{"name":"non-orth", "title": "Non Orth", "condition" : "(twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && dilepBDT > 0.1)", "baseline" : "sameSign == 0", "sc" : "sameSign == 1"},
        #{"name":"orth", "title": "Orth", "condition" : "(twoLeptons == 1 && MHT >= 220 &&  MET >= 200 && @leptons.size() == 2 && leptonFlavour == \"Muons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && dilepBDT > 0.1 && (leptons[1].Pt() <= 3.5 || deltaR <= 0.3))", "baseline" : "sameSign == 0", "sc" : "sameSign == 1"},
    ]
    
    #(twoLeptons == 1 && (leptons[1].Pt() <= 3.5 || deltaR <= 0.3) && MHT >= 220 &&  MET >= 200 && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && dilepBDT > 0.1 && BTagsDeepMedium == 0 && vetoElectronsPassIsoTightID == 0 && vetoMuonsPassIsoPassIso == 0 && @leptons.size() == 2 && leptonFlavour == \"" + lep + "\" && sameSign == 0)", True)
    histograms_defs = [
        { "obs" : "invMass", "minX" : 0, "maxX" : 13, "bins" : 6, "blind" : [4,None]},# "customBins"  : [0,2,3.0,3.2,4,6,10,12] },#, "scale" : "width"
        { "obs" : "dilepBDT", "minX" : -1, "maxX" : 1, "bins" : 6, "blind" : [None,0.1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
    ]
    
    weightString = {
        'MET' : "Weight"# * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * puWeight",
    }
    
    #calculatedLumi = {
    #    'MET' : 35.778598358,
    #}
    
    plot_sc = True
    plot_data = False
    plot_overflow = False
    plot_ratio = True
    plot_signal = False
    
    blind_data = True
    
    save_histrograms_to_file = True
    load_histrograms_from_file = False
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg.root"

class dilepton_muons_bg_scale(dilepton_muons_bg):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_scale.root"
    histograms_defs = [
        { "obs" : "invMass", "minX" : 0, "maxX" : 13, "bins" : 6, "blind" : [4,None], "customBins"  : [0,2,3.0,3.2,4,6,10,12], "scale" : "width"},
        { "obs" : "dilepBDT", "minX" : -1, "maxX" : 1, "bins" : 6, "blind" : [None,0.1], "customBins"  : [-1,-0.4,0,0.1,0.2,1], "scale" : "width" },
    ]
    y_title = "Events / GeV"

class dilepton_muons_bg_coarse(dilepton_muons_bg):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_fine.root"
    histograms_defs = [
        { "obs" : "invMass", "minX" : 0, "maxX" : 13, "bins" : 6, "blind" : [4,None]},# "customBins"  : [0,2,3.05,3.15,4,6,10,12] },
        { "obs" : "dilepBDT", "minX" : -1, "maxX" : 1, "bins" : 6, "blind" : [None,0.1]},# "customBins"  : [-1,-0.4,0,0.1,0.2,1] },
    ]

class dilepton_muons_bg_coarse_retag(dilepton_muons_bg_coarse):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_coarse_retag.root"
    bg_retag = True
    
    bgReTagging = bgReTaggingFull
    bgReTaggingOrder = bgReTaggingOrderFull
    bgReTaggingNames = bgReTaggingNamesFull

class track_muon_sc_comparison(BaseParams):
    histrograms_file = BaseParams.histograms_root_files_dir + "/track_muon_sc_comparison.root"
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/type_sum"
    save_histrograms_to_file = True
    load_histrograms_from_file = False 
    baseConditions = analysis_selections.injectValues(analysis_selections.ex_track_cond, "2016", "Muons")
    scConditions = analysis_selections.injectValues(analysis_selections.sc_ex_track_cond, "2016", "Muons")
    cuts = [
        {"name":"none", "title": "None", "condition" : analysis_selections.common_preselection, "baseline" : baseConditions, "sc" : scConditions },
        #{"name":"sr", "title": "sr", "condition" : "(MHT >= 220 &&  MET >= 200 && BTagsDeepMedium == 0 )", "baseline" : "exclusiveTrack == 1 && trackBDT > 0 && exTrack_invMass < 30 && exclusiveTrackLeptonFlavour == \"Muons\" && exTrack_dilepBDT > 0.1", "sc" : "sc_exclusiveTrack == 1 && sc_trackBDT > 0 && sc_exTrack_invMass < 30 && sc_exclusiveTrackLeptonFlavour == \"Muons\"" }
    ]
    #injectJetIsoToCuts(cuts, "CorrJetNoMultIso10Dr0.6")
    
    histograms_defs = [
        { "obs" : "exTrack_dilepBDT%%%", "units" : "BDT", "minX" : -1, "maxX" : 1, "bins" : 30,  "sc_obs" : "sc_exTrack_dilepBDT%%%", "linearYspace" : 1.9, "lumiStringPrefix" : "Muons Phase 0"},
        { "obs" : "exTrack_dilepBDT_bins%%%", "formula": "exTrack_dilepBDT%%%", "units" : "BDT", "minX" : -1, "maxX" : 1, "bins" : 30,  "sc_obs" : "sc_exTrack_dilepBDT%%%", "linearYspace" : 1.9, "lumiStringPrefix" : "Muons Phase 0", "customBins"  : [-1,0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,1]},
    ]
    
    injectJetIsoToHistograms(histograms_defs, analysis_selections.jetIsos["Muons"])  
    
    weightString = {
        'MET' : analysis_selections.full_sim_weights["2016"],
    }
    
    calculatedLumi = {
        'MET' : analysis_selections.recommended_luminosities["2016"],
    }
    
    plot_data = False
    plot_sc = True
    plot_ratio = True
    plot_signal = False
    plot_error = True
    sc_color = kOrange + 1
    label_text = plotutils.StampStr.SIM
    ratio_label = "oc"
    stamp_scale_factor = True
    
    legend_coordinates = {"x1" : .40, "y1" : .60, "x2" : .92, "y2" : .89}

class track_muon_sc_comparison_phase1(track_muon_sc_comparison):
    histrograms_file = BaseParams.histograms_root_files_dir + "/track_muon_sc_comparison_phase1_new_training.root"
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_phase1/sum/type_sum"
    weightString = {
        'MET' : analysis_selections.full_sim_weights["phase1"],
    }
    
    calculatedLumi = {
        'MET' : analysis_selections.recommended_luminosities["phase1"],
    }
    
    histograms_defs = [
        { "obs" : "exTrack_dilepBDT%%%", "units" : "BDT", "minX" : -1, "maxX" : 1, "bins" : 30,  "sc_obs" : "sc_exTrack_dilepBDT%%%", "linearYspace" : 1.5, "lumiStringPrefix" : "Muons Phase 1"},
    ]
    
    injectJetIsoToHistograms(histograms_defs, analysis_selections.jetIsos["Muons"])  
    y_title_offset = 0.9

class track_electron_sc_comparison(track_muon_sc_comparison):
    histrograms_file = BaseParams.histograms_root_files_dir + "/track_electron_sc_comparison.root"
    baseConditions = analysis_selections.injectValues(analysis_selections.ex_track_cond + " && " + analysis_selections.ex_track_electrons_filter, "2016", "Electrons")
    scConditions = analysis_selections.injectValues(analysis_selections.sc_ex_track_cond + " && " + analysis_selections.sc_ex_track_electrons_filter , "2016", "Electrons")
    cuts = [
        {"name":"none", "title": "None", "condition" : analysis_selections.common_preselection, "baseline" : baseConditions, "sc" : scConditions },
        #{"name":"sr", "title": "sr", "condition" : "(MHT >= 220 &&  MET >= 200 && BTagsDeepMedium == 0 )", "baseline" : "exclusiveTrack == 1 && trackBDT > 0 && exTrack_invMass < 30 && exclusiveTrackLeptonFlavour == \"Muons\" && exTrack_dilepBDT > 0.1", "sc" : "sc_exclusiveTrack == 1 && sc_trackBDT > 0 && sc_exTrack_invMass < 30 && sc_exclusiveTrackLeptonFlavour == \"Muons\"" }
    ]
    
    histograms_defs = [
        { "obs" : "exTrack_dilepBDT%%%", "units" : "BDT", "minX" : -1, "maxX" : 1, "bins" : 30,  "sc_obs" : "sc_exTrack_dilepBDT%%%", "linearYspace" : 1.5, "lumiStringPrefix" : "Electrons Phase 0"},
    ]
    
    injectJetIsoToHistograms(histograms_defs, analysis_selections.jetIsos["Electrons"]) 
    
    save_histrograms_to_file = True
    load_histrograms_from_file = True 

class track_electron_sc_comparison_phase1(track_muon_sc_comparison_phase1):
    histrograms_file = BaseParams.histograms_root_files_dir + "/track_electron_sc_comparison_phase1_new_training.root"
    baseConditions = analysis_selections.injectValues(analysis_selections.ex_track_cond + " && " + analysis_selections.ex_track_electrons_filter, "2016", "Electrons")
    scConditions = analysis_selections.injectValues(analysis_selections.sc_ex_track_cond + " && " + analysis_selections.sc_ex_track_electrons_filter , "2016", "Electrons")
    cuts = [
        {"name":"none", "title": "None", "condition" : analysis_selections.common_preselection, "baseline" : baseConditions, "sc" : scConditions },
        #{"name":"sr", "title": "sr", "condition" : "(MHT >= 220 &&  MET >= 200 && BTagsDeepMedium == 0 )", "baseline" : "exclusiveTrack == 1 && trackBDT > 0 && exTrack_invMass < 30 && exclusiveTrackLeptonFlavour == \"Muons\" && exTrack_dilepBDT > 0.1", "sc" : "sc_exclusiveTrack == 1 && sc_trackBDT > 0 && sc_exTrack_invMass < 30 && sc_exclusiveTrackLeptonFlavour == \"Muons\"" }
    ]
    histograms_defs = [
        { "obs" : "exTrack_dilepBDT%%%", "units" : "BDT", "minX" : -1, "maxX" : 1, "bins" : 30,  "sc_obs" : "sc_exTrack_dilepBDT%%%", "linearYspace" : 1.6, "lumiStringPrefix" : "Electrons Phase 1"},
    ]
    
    injectJetIsoToHistograms(histograms_defs, analysis_selections.jetIsos["Electrons"]) 
    save_histrograms_to_file = True
    load_histrograms_from_file = True 

# We don't really need to scan this category - because we use the 2 Muons category to decide this one out.
class track_muon_sc_comparison_scan_muons(BaseParams):
    histrograms_file = BaseParams.histograms_root_files_dir + "/track_muon_sc_comparison_scan_muons.root"
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/type_sum"
    save_histrograms_to_file = True
    load_histrograms_from_file = True 
    
    # cuts = [
#         {"name":"none", "title": "None", "condition" : "(MinDeltaPhiMhtJets > 0.4 && MHT >= 220 &&  MET >= 140 && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "exclusiveTrack%%% == 1 && trackBDT%%% > 0 && exTrack_invMass%%% < 12 && exclusiveTrackLeptonFlavour%%% == \"Muons\"", "sc" : "sc_exclusiveTrack%%% == 1 && sc_trackBDT%%% > 0 && sc_exTrack_invMass%%% < 12 && sc_exclusiveTrackLeptonFlavour%%% == \"Muons\"" },
#         #{"name":"sr", "title": "sr", "condition" : "(MHT >= 220 &&  MET >= 200 && BTagsDeepMedium == 0 )", "baseline" : "exclusiveTrack == 1 && trackBDT > 0 && exTrack_invMass < 30 && exclusiveTrackLeptonFlavour == \"Muons\" && exTrack_dilepBDT > 0.1", "sc" : "sc_exclusiveTrack == 1 && sc_trackBDT > 0 && sc_exTrack_invMass < 30 && sc_exclusiveTrackLeptonFlavour == \"Muons\"" }
#     ]
#     injectJetIsoToCuts(cuts, "CorrJetIso10.5Dr0.55")
#     
#     histograms_defs = [
#         { "obs" : "exTrack_dilepBDT%%%", "units" : "BDT", "minX" : -1, "maxX" : 1, "bins" : 30, "blind" : [None,0.1], "sc_obs" : "sc_exTrack_dilepBDT%%%", "linearYspace" : 1.5},
#     ]
#     
#     injectJetIsoToHistograms(histograms_defs, "CorrJetIso10.5Dr0.55")  
    
    weightString = {
        'MET' : "Weight * passesUniversalSelection * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * BranchingRatio",
    }
    
    plot_data = False
    plot_sc = True
    plot_ratio = True
    plot_signal = False
    sc_color = kOrange + 1
    label_text = plotutils.StampStr.SIMWIP
    
    
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
                        hist_def = { "obs" : obs + "%%%", "formula" : "exTrack_dilepBDT%%%" if "dilepBDT" in obs else (obs + "%%%"), "sc_obs" : "sc_exTrack_dilepBDT%%%", "linearYspace" : 1.5, "minX" : 0 if obs == "invMass" else -1, "maxX" : 13 if obs == "invMass" else 1, "bins" : 40 if obs == "dilepBDT_fine" else 20, "blind" : [None, 0], "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,1] if obs == "dilepBDT_custom" else None,  "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && MHT >= 220 &&  MET >= 140 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "exclusiveTrack%%% == 1 && trackBDT%%% > 0 && exTrack_invMass%%% < 12 && exclusiveTrackLeptonFlavour%%% == \"Muons\"", "sc" : "sc_exclusiveTrack%%% == 1 && sc_trackBDT%%% > 0 && sc_exTrack_invMass%%% < 12 && sc_exclusiveTrackLeptonFlavour%%% == \"Muons\""}
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


class dimuon_background_tautau_vs_bdt(BaseParams):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dimuon_background_tautau_vs_bdt.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = True 
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/slim_sum_total"
    plot_bg = True
    plot_data = False
    plot_signal = False
    jetIso = "CorrJetNoMultIso10Dr0.6"
    solid_bg = True
    cuts = [
        {"name":"none", "title": "None", "condition" : "(passedMhtMet6pack == 1 && passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && isoCr%%% == 0 && tautau%%%)"},
        #{"name":"tautau", "title": "no tautau", "condition" : "(passedMhtMet6pack == 1 && passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && (nmtautau%%% > 150 || nmtautau%%% < 50))"},
        #{"name":"orth", "title": "orth", "condition" : "(passedMhtMet6pack == 1 && passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && (leptons%%%[1].Pt() <= 3.5 || deltaR%%% <= 0.3))"},
    ]
    injectJetIsoToCuts(cuts, jetIso)
    histograms_defs = [     
        #{ "obs" : "dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,1], "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
        { "obs" : "tautau", "formula" : "nmtautau%%%:dilepBDT%%%", "minX" : -1, "maxX" : 1, "minY" : -100, "maxY" : 200, "units" : "BDT", "bins" : 50, "binsY" : 50, "2D" : True, "plotStr" : "colz"},
    ]
    injectJetIsoToHistograms(histograms_defs, jetIso)
    weightString = {
        #'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * puWeight * BranchingRatio",
        'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * BranchingRatio * passesUniversalSelection",
    }
    calculatedLumi = {
        #'MET' : 35.712736198,
        'MET' : 35.7389543
    }

signals = [
              #"/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim/higgsino_mu100_dm1p13Chi20Chipm.root",
              #"/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim/higgsino_mu100_dm1p47Chi20Chipm.root",
              #"/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim/higgsino_mu100_dm1p92Chi20Chipm.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim_sum/higgsino_mu100_dm3p28Chi20Chipm_1.root",
              #"/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim/higgsino_mu100_dm4p30Chi20Chipm.root"
              ]

signalNames = [
    # "\Delta_{}M 1.13 Gev",
#     "\Delta_{}M 1.47 Gev",
#     "\Delta_{}M 1.9 Gev",
    "\Delta_{}M 3.2 Gev",
    #"\Delta_{}M 4.3 Gev",
]


class dimuon_background_tautau_vs_bdt_signal(dimuon_background_tautau_vs_bdt):
    jetIso = "CorrJetNoMultIso10Dr0.6"
    cuts = [
        {"name":"none", "title": "None", "condition" : "(passedMhtMet6pack == 1 && passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && isoCr%%% == 0)"},
        #{"name":"tautau", "title": "no tautau", "condition" : "(passedMhtMet6pack == 1 && passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && (nmtautau%%% > 150 || nmtautau%%% < 50))"},
        #{"name":"orth", "title": "orth", "condition" : "(passedMhtMet6pack == 1 && passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && (leptons%%%[1].Pt() <= 3.5 || deltaR%%% <= 0.3))"},
    ]
    injectJetIsoToCuts(cuts, jetIso)
    histrograms_file = BaseParams.histograms_root_files_dir + "/dimuon_background_tautau_vs_bdt_signal.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = False 
    plot_bg = False
    plot_signal = True
    signal_dir = signals
    signal_names = signalNames

########### DATA DRIVEN ESTIMATIONS ########### 

class dimuon_background_estimation_non_isolated_and_tautau_2016(BaseParams):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dimuon_background_estimation_non_isolated_and_tautau_2016.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = True
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/slim_sum_total"
    data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim/slim_sum/"
    
    plot_error = True
    plot_data = False
    plot_data_for_bg_estimation = True
    
    plot_signal = False
    blind_data = False
    bg_retag = True
    
    jetIsoStr = ""
    
    jetIso = analysis_selections.jetIsos["Muons"]
    
    cuts = [
        {"name":"none", "title": "None", "condition" : "(passedMhtMet6pack == 1 && passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0)"},
        {"name":"tautau", "title": "no tautau [40,130]", "condition" : "(passedMhtMet6pack == 1 && passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && (nmtautau%%% > 130 || nmtautau%%% < 40))"},
        {"name":"orth", "title": "orth", "condition" : "(passedMhtMet6pack == 1 && passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && (leptons%%%[1].Pt() <= 3.5 || deltaR%%% <= 0.3))"},
        #{"name":"orth-notautau", "title": "orth-notautau [50,150]", "condition" : "(passedMhtMet6pack == 1 && passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && (leptons%%%[1].Pt() <= 3.5 || deltaR%%% <= 0.3) && (nmtautau%%% > 150 || nmtautau%%% < 50) )"},
        {"name":"orth-notautau1", "title": "orth-notautau [40,130]", "condition" : "(passedMhtMet6pack == 1 && passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && (leptons%%%[1].Pt() <= 3.5 || deltaR%%% <= 0.3) && (nmtautau%%% > 130 || nmtautau%%% < 40) )"},
        #{"name":"orth-notautau2", "title": "orth-notautau2 [0,160]", "condition" : "(passedMhtMet6pack == 1 && passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && (leptons%%%[1].Pt() <= 3.5 || deltaR%%% <= 0.3) && (nmtautau%%% > 160 || nmtautau%%% < 0) )"},
    ]
    injectJetIsoToCuts(cuts, jetIso)

    # histograms_defs = [     
#         #{ "obs" : "dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,1], "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
#         #{ "obs" : "tautau", "formula" : "nmtautau%%%:dilepBDT%%%", "minX" : -1, "maxX" : 1, "minY" : -100, "mixY" : 200, "units" : "BDT", "bins" : 50, "binsY" : 50, "2D" : True},
#         { "obs" : "dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.05,0.15,0.25,0.35,0.45,0.6,1], "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
#         #{ "obs" : "new_bin_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,1], "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
#         { "obs" : "newer_bin_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.45,0.5,0.55,1], "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
#         { "obs" : "newest_bin_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.45,0.5,1], "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
#         { "obs" : "fine_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 40, "units" : "BDT", "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}}
#     ]
    
    
    
    histograms_defs = [     
        #{ "obs" : "dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,1], "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
        #{ "obs" : "tautau", "formula" : "nmtautau%%%:dilepBDT%%%", "minX" : -1, "maxX" : 1, "minY" : -100, "mixY" : 200, "units" : "BDT", "bins" : 50, "binsY" : 50, "2D" : True},
        #{ "obs" : "dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.05,0.15,0.25,0.35,0.45,0.6,1], "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
        #{ "obs" : "dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.05,0.15,0.25,0.35,0.45,0.6,1], "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
        #{ "obs" : "new_bin_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,1], "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
        #{ "obs" : "newer_bin_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.45,0.5,0.55,1], "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
        #{ "obs" : "newer_bin_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.45,0.5,0.55,1], "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
        
        #{ "obs" : "newest_bin_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.45,0.5,1], "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
        #{ "obs" : "newest_bin_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.45,0.5,1], "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
        #{ "obs" : "newestest_bin_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.45,1], "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
        
        { "obs" : "newestestest_bin_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT output", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,1], "legendCol" : 1, "legendCoor" : {"x1" : .63, "y1" : .68, "x2" : .99, "y2" : .89}, "linearYspace" : 1.6, "logYspace" : 3000 },
        #{ "obs" : "fine_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 40, "units" : "BDT", "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
        { "obs" : "fine_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "bins" : 40, "units" : "BDT phase1", "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}}
    ]
    injectJetIsoToHistograms(histograms_defs, jetIso)
    
    weightString = {
        #'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * puWeight * BranchingRatio",
        'MET' : "Weight * tEffhMetMhtRealXMht2016 * BranchingRatio",
    }
    
    calculatedLumi = {
        'MET' : analysis_selections.luminosities["2016"]
    }
    
    bgReTaggingFactors = {
        "tautau" : analysis_selections.tautau_factors["2016"]["Muons"],
        "non-iso" : analysis_selections.non_iso_2l_factors["2016"]["Muons"]
    }
    
    bgReTagging = {
        "tautau" : "tautau%%% && isoCr%%% == 0",
        "non-iso" : "isoCr%%% >= 1"
    }
    
    injectJetIsoToMapValues(bgReTagging, jetIso)
    
    bgReTaggingUseSources = True
    
    bgReTaggingOrder = {
        "tautau" : 1,
        "non-iso" : 2
    }
    bgReTaggingNames = {
        "tautau" : "#tau#tau",
        "non-iso" : "jetty"
    }
    bgReTaggingSources = {
        "tautau" : "bg",
        "non-iso" : "data"
    }
    
    #bgReTaggingFactors = {
    #    "tautau" : [1.44864,0.46772],
    #    "non-iso" : [0.4604,0.06955]
    #}
    y_title_offset = 0.8
    
    colorPalette = [
        { "name" : "yellow", "fillColor" : TColor.GetColor("#ffd700"), "lineColor" : kBlack, "fillStyle" : 1001, "markerColor" : 5,  "markerStyle" : kOpenCircle},
        { "name" : "blue", "fillColor" : TColor.GetColor("#0057b7"), "lineColor" : kBlack, "fillStyle" : 1001, "markerColor" : 38,  "markerStyle" : kOpenCross },
    ]
    log_minimum = 0.01
    
    label_text = plotutils.StampStr.PRE

class dimuon_background_estimation_non_isolated_and_tautau_2017(dimuon_background_estimation_non_isolated_and_tautau_2016):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dimuon_background_estimation_non_isolated_and_tautau_2017.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = True
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_phase1/sum/slim_sum_total"
    data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim_phase1/slim_2017/"
    
    weightString = {
        #'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * puWeight * BranchingRatio",
        'MET' : "Weight * tEffhMetMhtRealXMht2017 * BranchingRatio",
    }
    
    calculatedLumi = {
        'MET' : analysis_selections.luminosities["2017"]
    }
    
    bgReTaggingFactors = {
        "tautau" : analysis_selections.tautau_factors["2017"]["Muons"],
        "non-iso" : analysis_selections.non_iso_2l_factors["2017"]["Muons"]
    }
    
    jetIso = analysis_selections.jetIsos["Muons"]
    
    histograms_defs = [     
        #{ "obs" : "dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,1], "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
        #{ "obs" : "tautau", "formula" : "nmtautau%%%:dilepBDT%%%", "minX" : -1, "maxX" : 1, "minY" : -100, "mixY" : 200, "units" : "BDT", "bins" : 50, "binsY" : 50, "2D" : True},
        #{ "obs" : "dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.05,0.15,0.25,0.35,0.45,0.6,1], "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
        #{ "obs" : "dilepBDTphase1%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.05,0.15,0.25,0.35,0.45,0.6,1], "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
        #{ "obs" : "new_bin_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,1], "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
        #{ "obs" : "newer_bin_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.45,0.5,0.55,1], "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
        #{ "obs" : "newer_bin_dilepBDTphase1%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.45,0.5,0.55,1], "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
        
        #{ "obs" : "newest_bin_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.45,0.5,1], "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
        #{ "obs" : "newest_bin_dilepBDTphase1%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.45,0.5,1], "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
        #{ "obs" : "newestest_bin_dilepBDTphase1%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.45,1], "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
        
        { "obs" : "newestestest_bin_dilepBDTphase1%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT output", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,1], "legendCol" : 1, "legendCoor" : {"x1" : .63, "y1" : .68, "x2" : .99, "y2" : .89}, "linearYspace" : 1.6, "logYspace" : 3000 },
        
        
        #{ "obs" : "fine_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 40, "units" : "BDT", "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
        { "obs" : "fine_dilepBDTphase1%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 40, "units" : "BDT phase1", "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}}
    ]
    injectJetIsoToHistograms(histograms_defs, jetIso)

class dimuon_background_estimation_non_isolated_and_tautau_2018(dimuon_background_estimation_non_isolated_and_tautau_2017):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dimuon_background_estimation_non_isolated_and_tautau_2018.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = False
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_phase1/sum/slim_sum_total"
    data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim_phase1/slim_2018/"
    
    weightString = {
        #'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * puWeight * BranchingRatio",
        'MET' : "Weight * tEffhMetMhtRealXMht2018 * BranchingRatio",
    }
    
    calculatedLumi = {
        'MET' : analysis_selections.luminosities["2018"]
    }
    
    bgReTaggingFactors = {
        "tautau" : analysis_selections.tautau_factors["2018"]["Muons"],
        "non-iso" : analysis_selections.non_iso_2l_factors["2018"]["Muons"]
    }
    
    jetIso = analysis_selections.jetIsos["Muons"]
    
    cuts = [
        {"name":"none", "title": "None", "condition" : "(hemFailureVetoElectrons && hemFailureVetoJets && hemFailureVetoMuons && passedMhtMet6pack == 1 && passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0)"},
        {"name":"tautau", "title": "no tautau [40,130]", "condition" : "(hemFailureVetoElectrons && hemFailureVetoJets && hemFailureVetoMuons && passedMhtMet6pack == 1 && passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && (nmtautau%%% > 130 || nmtautau%%% < 40))"},
        {"name":"orth", "title": "orth", "condition" : "(hemFailureVetoElectrons && hemFailureVetoJets && hemFailureVetoMuons && passedMhtMet6pack == 1 && passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && (leptons%%%[1].Pt() <= 3.5 || deltaR%%% <= 0.3))"},
        #{"name":"orth-notautau", "title": "orth-notautau [50,150]", "condition" : "(passedMhtMet6pack == 1 && passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && (leptons%%%[1].Pt() <= 3.5 || deltaR%%% <= 0.3) && (nmtautau%%% > 150 || nmtautau%%% < 50) )"},
        {"name":"orth-notautau1", "title": "orth-notautau [40,130]", "condition" : "(hemFailureVetoElectrons && hemFailureVetoJets && hemFailureVetoMuons && passedMhtMet6pack == 1 && passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && (leptons%%%[1].Pt() <= 3.5 || deltaR%%% <= 0.3) && (nmtautau%%% > 130 || nmtautau%%% < 40) )"},
        #{"name":"orth-notautau2", "title": "orth-notautau2 [0,160]", "condition" : "(passedMhtMet6pack == 1 && passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && (leptons%%%[1].Pt() <= 3.5 || deltaR%%% <= 0.3) && (nmtautau%%% > 160 || nmtautau%%% < 0) )"},
    ]
    
    injectJetIsoToCuts(cuts, jetIso)

class dimuon_background_estimation_non_isolated_and_tautau_phase1(dimuon_background_estimation_non_isolated_and_tautau_2018):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dimuon_background_estimation_non_isolated_and_tautau_phase1.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = True
    calculatedLumi = {
        'MET' : analysis_selections.luminosities["phase1"],   
    }
    bgReTaggingFactors = {
        "tautau" : analysis_selections.tautau_factors["phase1"]["Muons"],
        "non-iso" : analysis_selections.non_iso_2l_factors["phase1"]["Muons"]
    }
    
    weightString = {
        #'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * puWeight * BranchingRatio",
        'MET' : "((41.15 * tEffhMetMhtRealXMht2017 + 58.09 * tEffhMetMhtRealXMht2018)/99.23) * Weight * passedMhtMet6pack * BranchingRatio * passesUniversalSelection",
    }
    
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_phase1/sum/slim_sum_total"
    data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim_phase1/slim_sum"
    
class dimuon_background_estimation_non_isolated_and_tautau_run2(dimuon_background_estimation_non_isolated_and_tautau_2016):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dimuon_background_estimation_non_isolated_and_tautau_run2.root"
    run2lumi = utils.LUMINOSITY/1000
    calculatedLumi2016 = 35.7389543
    calculatedLumi = {
        'MET' : calculatedLumi2016,   
    }
    bgReTaggingFactors = {
        "tautau" : [(run2lumi/calculatedLumi2016) * 1.44864,0.46772],
        "non-iso" : [(run2lumi/calculatedLumi2016) * 0.4604,0.06955]
    }

signals = [
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim_sum/higgsino_mu100_dm1p13Chi20Chipm_1.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim_sum/higgsino_mu100_dm1p47Chi20Chipm_1.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim_sum/higgsino_mu100_dm1p92Chi20Chipm_1.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim_sum/higgsino_mu100_dm3p28Chi20Chipm_1.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim_sum/higgsino_mu100_dm4p30Chi20Chipm_1.root"
              ]

signalNames = [
    "\Delta_{}M 1.13 Gev",
    "\Delta_{}M 1.47 Gev",
    "\Delta_{}M 1.9 Gev",
    "\Delta_{}M 3.2 Gev",
    "\Delta_{}M 4.3 Gev",
]

class dimuon_background_estimation_non_isolated_and_tautau_and_signal(dimuon_background_estimation_non_isolated_and_tautau_2016):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dimuon_background_estimation_non_isolated_and_tautau_and_signal.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = True
    plot_signal = True
    signal_dir = signals
    signal_names = signalNames

signals_2017 = [
              #"/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_phase1/slim_sum/mChipm100GeV_dm0p759GeV_1.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_phase1/slim_sum/mChipm100GeV_dm0p959GeV_1.root",
              #"/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_phase1/slim_sum/mChipm100GeV_dm1p259GeV_1.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_phase1/slim_sum/mChipm100GeV_dm1p759GeV_1.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_phase1/slim_sum/mChipm100GeV_dm2p259GeV_1.root",
              #"/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_phase1/slim_sum/mChipm100GeV_dm3p259GeV_1.root"
              
              ]

signalNames_2017 = [
    #"\Delta_{}m^{\pm} 0.75 GeV",
    "\Delta_{}m^{\pm} 0.95 GeV",
    #"\Delta_{}m^{\pm} 1.25 GeV",
    "\Delta_{}m^{\pm} 1.75 GeV",
    "\Delta_{}m^{\pm} 2.25 GeV",
    #"\Delta_{}m^{\pm} 3.25 GeV",
]


class dimuon_background_estimation_non_isolated_and_tautau_phase1_and_signal(dimuon_background_estimation_non_isolated_and_tautau_phase1):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dimuon_background_estimation_non_isolated_and_tautau_phase1_and_signal.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = True
    plot_signal = True
    signal_dir = signals_2017
    signal_names = signalNames_2017

class dimuon_background_estimation_non_isolated_and_tautau_simulation_only(dimuon_background_estimation_non_isolated_and_tautau_2016):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dimuon_background_estimation_non_isolated_and_tautau_simulation_only.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = False
    
    bgReTagging = {
        "tautau" : "tautau%%% && isoCr%%% == 0",
        "non-iso" : "!tautau%%% && isoCr%%% == 0"
    }
    
    jetIso = "CorrJetNoMultIso10Dr0.6"
    injectJetIsoToMapValues(bgReTagging, jetIso)
    
    bgReTaggingUseSources = False
    plot_data = False
    
    bgReTaggingNames = {}
    bgReTaggingSources = {}
    bgReTaggingFactors = {}

class dimuon_background_estimation_non_isolated_and_tautau_simulation_only_with_phase1_training_on_phase0_mc(dimuon_background_estimation_non_isolated_and_tautau_simulation_only):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dimuon_background_estimation_non_isolated_and_tautau_simulation_only_with_phase1_training_on_phase0_mc.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = False
    jetIso = "CorrJetNoMultIso10Dr0.6"
    
    histograms_defs = [     
        #{ "obs" : "dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,1], "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
        #{ "obs" : "tautau", "formula" : "nmtautau%%%:dilepBDT%%%", "minX" : -1, "maxX" : 1, "minY" : -100, "mixY" : 200, "units" : "BDT", "bins" : 50, "binsY" : 50, "2D" : True},
        { "obs" : "dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.05,0.15,0.25,0.35,0.45,0.6,1], "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
        { "obs" : "dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.05,0.15,0.25,0.35,0.45,0.6,1], "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
        #{ "obs" : "new_bin_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,1], "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
        { "obs" : "newer_bin_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.45,0.5,0.55,1], "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
        { "obs" : "newer_bin_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.45,0.5,0.55,1], "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
        { "obs" : "newest_bin_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.45,0.5,1], "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
        { "obs" : "newest_bin_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT phase1", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.45,0.5,1], "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
        { "obs" : "fine_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 40, "units" : "BDT", "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
        { "obs" : "fine_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "bins" : 40, "units" : "BDT phase1", "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}}
    ]
    injectJetIsoToHistograms(histograms_defs, jetIso)
    
    plot_signal = True
    signal_dir = signals
    signal_names = signalNames
    
class dimuon_background_estimation_non_isolated_and_tautau_simulation_only_phase1(dimuon_background_estimation_non_isolated_and_tautau_simulation_only):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dimuon_background_estimation_non_isolated_and_tautau_simulation_only_phase1.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = False
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_phase1/sum/slim_sum_total"
    weightString = {
        #'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * puWeight * BranchingRatio",
        'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2017 * BranchingRatio * passesUniversalSelection",
    }
    

class dimuon_background_data_estimation_vs_mc_non_isolated(BaseParams):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dimuon_background_data_estimation_vs_mc_non_isolated.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = False
    
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/slim_sum_total"
    data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim/slim_sum/"
    
    plot_error = True
    plot_data = False
    plot_data_for_bg_estimation = True
    
    plot_signal = False
    blind_data = False
    bg_retag = True
    
    jetIsoStr = ""
    
    jetIso = "CorrJetNoMultIso10Dr0.6"
    
    cuts = [
        {"name":"none", "title": "None", "condition" : "(passedMhtMet6pack == 1 && passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0)"},
        {"name":"orth", "title": "orth", "condition" : "(passedMhtMet6pack == 1 && passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && (leptons%%%[1].Pt() <= 3.5 || deltaR%%% <= 0.3))"},
    ]
    injectJetIsoToCuts(cuts, jetIso)

    histograms_defs = [     
        { "obs" : "dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,1], "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
        { "obs" : "new_bin_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,1], "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}},
        { "obs" : "fine_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 40, "units" : "BDT", "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}}
    ]
    injectJetIsoToHistograms(histograms_defs, jetIso)
    
    weightString = {
        #'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * puWeight * BranchingRatio",
        'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * BranchingRatio * passesUniversalSelection",
    }
    
    calculatedLumi = {
        'MET' : 35.7389543,
    }
    
    bgReTagging = {
        "mc" : "!tautau%%% && isoCr%%% == 0",
        "non-iso" : "isoCr%%% >= 1"
    }
    
    injectJetIsoToMapValues(bgReTagging, jetIso)
    
    bgReTaggingUseSources = True
    
    bgReTaggingOrder = {
        "mc" : 1,
        "non-iso" : 2
    }
    bgReTaggingNames = {
        "mc" : "MC",
        "non-iso" : "data-driven"
    }
    bgReTaggingSources = {
        "mc" : "bg",
        "non-iso" : "data"
    }
    
    bgReTaggingFactors = {
        "non-iso" : [0.4604,0.06955]
    }
    
    nostack = True
    plot_ratio = True
    plot_custom_ratio = True
    customRatios = [  [["mc"],["non-iso"]]  ]
    
    colorPalette = [
        { "name" : "yellow", "fillColor" : TColor.GetColor("#ffd700"), "lineColor" : kRed, "fillStyle" : 3444, "markerColor" : 5,  "markerStyle" : kOpenCircle},
        { "name" : "blue", "fillColor" : TColor.GetColor("#0057b7"), "lineColor" : kBlack, "fillStyle" : 3444, "markerColor" : 38,  "markerStyle" : kOpenCross },
    ]

class dimuon_background_data_estimation_vs_mc_non_isolated_run2_lumi(dimuon_background_data_estimation_vs_mc_non_isolated):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dimuon_background_data_estimation_vs_mc_non_isolated_run2_lumi.root"
    run2lumi = utils.LUMINOSITY/1000
    calculatedLumi2016 = 35.7389543
    calculatedLumi = {
        'MET' : run2lumi,   
    }
    bgReTaggingFactors = {
        "non-iso" : [(run2lumi/calculatedLumi2016) * 0.4604,0.06955]
    }

class dimuon_simulation_non_iso_and_tau_tau_training_scan(BaseParams):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dimuon_simulation_non_iso_and_tau_tau_training_scan3.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = False
    
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/slim_sum_total"
    plot_bg = True
    plot_data = False
    plot_signal = False
    
    weightString = {
        #'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * puWeight * BranchingRatio",
        'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * BranchingRatio * passesUniversalSelection",
    }
    
    
    cuts = [
        {"name":"none", "title": "None", "condition" : "1", "baseline" : "1", "sc" : "1"},
        #{"name":"bdt", "title": "BDT > 0.35", "condition" : "(dilepBDT%%% > 0.35 &&  MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 200 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
    ]
    
    
    histograms_defs = [
    
    ]
    
    for iso in ["CorrJetNoMultIso"]:
        for cat in utils.leptonIsolationCategories:
            #if iso == "CorrJetIso":
            #if iso == "CorrJetNoMultIso":
            ptRanges = utils.leptonCorrJetIsoPtRange
            drCuts = utils.leptonCorrJetIsoDrCuts

            for ptRange in ptRanges:
                if ptRange < 9:
                    continue
                for drCut in drCuts:
                    if drCut < 0.5:
                        continue
                    jetIso = ""
                    if len(str(ptRange)) > 0:
                        jetIso = iso + str(ptRange) + "Dr" + str(drCut) + cat
                    else:
                        continue
                   
                    #for obs in ["dilepBDT", "dilepBDT_fine", "dilepBDT_custom"]:
                    for obs in ["dilepBDT_custom", "dilepBDT_custom_tautau"]:
                    
                        #{ "obs" : "invMassCorrJetIso15Dr0.4", "minX" : 0, "maxX" : 13, "bins" : 6, "blind" : [4,None]}
                        hist_def = { "obs" : obs + "%%%", "formula" : "dilepBDT%%%" if "dilepBDT" in obs else (obs + "%%%"), "linearYspace" : 1.5, "minX" : 0 if obs == "invMass" else -1, "maxX" : 13 if obs == "invMass" else 1, "bins" : 40 if obs == "dilepBDT_fine" else 20, "blind" : [None, 0], "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,0.55,1] if obs == "dilepBDT_custom" else None,  "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && isoCr%%% == 0 " +  (" && (nmtautau%%% > 160 || nmtautau%%% < 0)" if obs == "dilepBDT_custom_tautau"  else "") +  ")", "baseline" : "!tautau%%%", "sc" : "tautau%%%"}
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
    sc_label = "#tau#tau"
    solid_bg = True
    plot_sc = True

class dimuon_simulation_non_iso_and_tau_tau_training_scan_2017(dimuon_simulation_non_iso_and_tau_tau_training_scan):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dimuon_simulation_non_iso_and_tau_tau_training_scan_2017.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = False
    
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_phase1/sum/slim_sum_total"
    
    weightString = {
        #'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * puWeight * BranchingRatio",
        'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2017 * BranchingRatio * passesUniversalSelection",
    }
    
    


















###############################################################
############ m_tautau plots to see tautau peak     ############
###############################################################


class dilepton_muons_bg_isocr_scan_tautau_vs_no_tautau(BaseParams):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_scan_tautau_vs_no_tautau.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = True 
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/slim_sum/type_sum"
    #signal_dir = signals
    #signal_names = signalNames
    #signal_dir =  "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim"
    plot_signal = False
    
    weightString = {
        #'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * puWeight * BranchingRatio",
        'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * BranchingRatio * passesUniversalSelection",
    }
    
    plot_error = True
    plot_sc = True
    plot_ratio = True
    
    cuts = [
        #{"name":"none", "title": "None", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 ) && isoCr%%% == 0", "baseline" : "1", "sc" : "1"},
        #{"name":"isoCr", "title": "isoCr", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 ) && isoCr%%% >= 1", "baseline" : "1", "sc" : "1"},
        {"name":"bdt", "title": "BDT < 0", "condition" : "(dilepBDT%%% < 0 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 ) && isoCr%%% == 0", "baseline" : "1", "sc" : "1"},
        {"name":"bdt2", "title": "BDT2 < 0", "condition" : "(dilepBDTphase1%%% < 0 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 ) && isoCr%%% == 0", "baseline" : "1", "sc" : "1"},
        #{"name":"loose", "title": "BDT < 0 loose", "condition" : "(dilepBDT%%% < 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 ) && isoCr%%% == 0", "baseline" : "1", "sc" : "1"},
        #{"name":"mtautau", "title": "nmtautau < 0 ||nmtautau > 160", "condition" : "((nmtautau%%% < 0 || nmtautau%%% > 160) && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 ) && isoCr%%% == 0", "baseline" : "1", "sc" : "1"},
        #{"name":"isoCr", "title": "isoCr", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 ) && isoCr%%% > 0", "baseline" : "1", "sc" : "1"},
        #{"name":"mtautau", "title": "mtautau > 200", "condition" : "isoCr%%% == 0 && mtautau%%% > 200", "baseline" : "isoCr%%% == 0", "sc" : "1"},
        #{"name":"bdt", "title": "BDT > 0.35", "condition" : "(dilepBDT%%% > 0.35 &&  MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 200 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
    ]
    jetIso = "CorrJetNoMultIso10Dr0.6"
    injectJetIsoToCuts(cuts, jetIso)
    
    histograms_defs = [
    #    { "obs" : "invMass%%%", "minX" : 0, "maxX" : 13, "bins" : 6, "blind" : [4,None]},# "customBins"  : [0,2,4,6,10,12] },
    #    { "obs" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 6, "blind" : [None,0.1]}
    ]
    
    sc_label = "#tau#tau"
    sc_ratio_label = "#tau#tau"
    sc_color = kRed
    plot_overflow = False
    normalise = False
    plot_reverse_ratio = True
    label_text = plotutils.StampStr.SIM
    
    calculatedLumi = {
        'MET' : 36.0,   
    }
    
    ratio_label = "non-#tau#tau"
    
   #  for iso in []:utils.leptonIsolationList:
#         for cat in utils.leptonIsolationCategories:
#             ptRanges = [""]
#             drCuts = [""]
#             if iso == "CorrJetIso":
#                 ptRanges = utils.leptonCorrJetIsoPtRange
#                 drCuts = utils.leptonCorrJetIsoDrCuts
#             else:
#                 continue
#             for ptRange in ptRanges:
#                 for drCut in drCuts:
                    # jetIso = ""
#                     if len(str(ptRange)) > 0:
#                         jetIso = iso + str(ptRange) + "Dr" + str(drCut) + cat
#                     else:
#                         continue
#                     if jetIso != "CorrJetIso10.5Dr0.55":
#                         continue
                    #for obs in ["invMass", "dilepBDT"]:
    
    for obs in ["dilepBDT", "dilepBDT_custom", "mtautau", "nmtautau"]:
        hist_def = { "obs" : obs + "%%%", "formula" : (obs + "%%%"), "linearYspace" : 1.9, "ratio1max" : 1 if (obs == "dilepBDT" or obs == "dilepBDT_custom") else 10, "minX" : -50 if "mtautau" in obs else -1, "maxX" : 300 if "mtautau" in obs else 1, "bins" : 20 if obs == "dilepBDT" else 30, "blind" : [None, 0],  "condition" : "1", "baseline" : "!tautau%%%", "sc" : "tautau%%%"}

        if obs == "mtautau_dilepBDT" or obs == "nmtautau_dilepBDT":
            hist_def["condition"] += " && dilepBDT%%% < 0"
            if obs == "mtautau_dilepBDT":
                hist_def["formula"] = "mtautau%%%"
            else:
                hist_def["formula"] = "nmtautau%%%"
        if obs == "mtautau":
            hist_def["units"] = "m_{#tau#tau} [GeV]"
        if obs == "nmtautau":
            hist_def["units"] = "m_{#tau#tau} [GeV]"
        if obs == "dilepBDT_custom":
            hist_def["formula"] = "dilepBDT"+ "%%%"
            hist_def["customBins"] = [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,1]
        #hist_def = { "obs" : obs + "%%%", "minX" : 0 if obs == "invMass" else -1, "maxX" : 13 if obs == "invMass" else 1, "bins" : 24, "blind" : [None, 0],  "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 200 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && isoCr%%% == 0 )", "baseline" : "!tautau%%%", "sc" : "tautau%%%"}
        #print(hist_def["obs"],jetIso)
        #print(hist_def["obs"].replace("%%%", jetIso))
        #print(hist_def["obs"])
        hist_def["obs"] = hist_def["obs"].replace("%%%", jetIso)
        hist_def["formula"] = hist_def["formula"].replace("%%%", jetIso)
        hist_def["condition"] = hist_def["condition"].replace("%%%", jetIso)
        hist_def["baseline"] = hist_def["baseline"].replace("%%%", jetIso)
        hist_def["sc"] = hist_def["sc"].replace("%%%", jetIso)
        histograms_defs.append(hist_def)  


class dilepton_electrons_bg_isocr_tautau_vs_no_tautau(dilepton_muons_bg_isocr_scan_tautau_vs_no_tautau):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_electrons_bg_isocr_tautau_vs_no_tautau.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = False 

    cuts = [
        {"name":"none", "title": "None", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Electrons\" && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 ) && isoCr%%% == 0", "baseline" : "1", "sc" : "1"},
        {"name":"isoCr", "title": "isoCr", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Electrons\" && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 ) && isoCr%%% >= 1", "baseline" : "1", "sc" : "1"},
        {"name":"bdt", "title": "BDT < 0", "condition" : "(dilepBDT%%% < 0 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Electrons\" && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 ) && isoCr%%% == 0", "baseline" : "1", "sc" : "1"},
        {"name":"mtautau", "title": "nmtautau < 0 ||nmtautau > 160", "condition" : "((nmtautau%%% < 0 || nmtautau%%% > 160) && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Electrons\" && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 ) && isoCr%%% == 0", "baseline" : "1", "sc" : "1"},
        #{"name":"isoCr", "title": "isoCr", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 ) && isoCr%%% > 0", "baseline" : "1", "sc" : "1"},
        #{"name":"mtautau", "title": "mtautau > 200", "condition" : "isoCr%%% == 0 && mtautau%%% > 200", "baseline" : "isoCr%%% == 0", "sc" : "1"},
        #{"name":"bdt", "title": "BDT > 0.35", "condition" : "(dilepBDT%%% > 0.35 &&  MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 200 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
    ]
    injectJetIsoToCuts(cuts, "CorrJetNoMultIso10Dr0.6")
    plot_overflow = False


class dilepton_muons_bg_isocr_scan_tautau_vs_no_tautau_phase1(dilepton_muons_bg_isocr_scan_tautau_vs_no_tautau):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_scan_tautau_vs_no_tautau_phase1.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = True 
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_phase1/sum/slim_sum/type_sum"
    #signal_dir = signals
    #signal_names = signalNames
    #signal_dir =  "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim"
    plot_signal = False
    
    weightString = {
        #'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * puWeight * BranchingRatio",
        'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2017 * BranchingRatio * passesUniversalSelection",
    }
    
    calculatedLumi = {
        'MET' : 101.0,   
    }
    
    cuts = [
        #{"name":"none", "title": "None", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 ) && isoCr%%% == 0", "baseline" : "1", "sc" : "1"},
        #{"name":"isoCr", "title": "isoCr", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 ) && isoCr%%% >= 1", "baseline" : "1", "sc" : "1"},
        {"name":"bdt", "title": "BDT < 0", "condition" : "(dilepBDT%%% < 0 && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 ) && isoCr%%% == 0", "baseline" : "1", "sc" : "1"},
        #{"name":"loose", "title": "BDT < 0 loose", "condition" : "(dilepBDT%%% < 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 ) && isoCr%%% == 0", "baseline" : "1", "sc" : "1"},
        #{"name":"mtautau", "title": "nmtautau < 0 ||nmtautau > 160", "condition" : "((nmtautau%%% < 0 || nmtautau%%% > 160) && MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 ) && isoCr%%% == 0", "baseline" : "1", "sc" : "1"},
        #{"name":"isoCr", "title": "isoCr", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 ) && isoCr%%% > 0", "baseline" : "1", "sc" : "1"},
        #{"name":"mtautau", "title": "mtautau > 200", "condition" : "isoCr%%% == 0 && mtautau%%% > 200", "baseline" : "isoCr%%% == 0", "sc" : "1"},
        #{"name":"bdt", "title": "BDT > 0.35", "condition" : "(dilepBDT%%% > 0.35 &&  MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 200 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
    ]
    jetIso = "CorrJetNoMultIso10Dr0.6"
    injectJetIsoToCuts(cuts, jetIso)

class dilepton_electrons_bg_isocr_tautau_vs_no_tautau_phase1(dilepton_electrons_bg_isocr_tautau_vs_no_tautau):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_electrons_bg_isocr_tautau_vs_no_tautau_phase1.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = False 
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_phase1/sum/slim_sum/type_sum"
    weightString = {
        #'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * puWeight * BranchingRatio",
        'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2017 * BranchingRatio * passesUniversalSelection",
    }

class dilepton_muons_bg_isocr_scan_tautau_vs_no_tautau_data(dilepton_muons_bg_isocr_scan_tautau_vs_no_tautau):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_bg_isocr_scan_tautau_vs_no_tautau_data.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = True 
    data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim/slim_sum"
    plot_data = True
    plot_bg = False
    plot_sc = False
    plot_signal = False
    plot_ratio = False
    normalise = False
    cuts = [
        {"name":"none", "title": "None", "condition" : "dilepBDT%%% < 0", "baseline" : "1", "sc" : "1"},
        #{"name":"bdt", "title": "BDT < 0", "condition" : "1", "baseline" : "1", "sc" : "1"},
        #{"name":"bdt", "title": "BDT > 0.35", "condition" : "(dilepBDT%%% > 0.35 &&  MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 200 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"},
    ]
    histograms_defs = [
        { "obs" : "mtautau%%%", "linearYspace" : 1.3, "ratio1max" : 10, "minX" : 40, "maxX" : 300, "bins" : 30, "blind" : [None, 0],  "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && isoCr%%% == 0 )"}
    ]
    jetIsoStr = "CorrJetIso10.5Dr0.55"
    injectJetIsoToCuts(cuts, jetIsoStr)
    injectJetIsoToHistograms(histograms_defs, jetIsoStr)
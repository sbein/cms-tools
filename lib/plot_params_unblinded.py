import sys
import os
from ROOT import *

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib"))

from plot_params_base import *
import plotutils
import analysis_selections


class unblinded_track_muon_sc_comparison(BaseParams):
    histrograms_file = BaseParams.histograms_root_files_dir + "/unblinded_track_muon_sc_comparison.root"
    #bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/type_sum"
    data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim/sum"
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
        #{ "obs" : "exTrack_dilepBDT_bins_no_cr%%%", "formula": "exTrack_dilepBDT%%%", "units" : "BDT", "minX" : -1, "maxX" : 1, "bins" : 30,  "sc_obs" : "sc_exTrack_dilepBDT%%%", "linearYspace" : 1.9, "lumiStringPrefix" : "Muons Phase 0", "customBins"  : [0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,1]},
        { "obs" : "exTrack_dilepBDT_bins_two%%%", "formula": "exTrack_dilepBDT%%%", "units" : "BDT", "minX" : -1, "maxX" : 1, "bins" : 30,  "sc_obs" : "sc_exTrack_dilepBDT%%%", "linearYspace" : 1.9, "lumiStringPrefix" : "Muons Phase 0", "customBins"  : [-1,0,1]},
    ]
    
    injectJetIsoToHistograms(histograms_defs, analysis_selections.jetIsos["Muons"])  
    
    weightString = {
        'MET' : "",
    }
    
    calculatedLumi = {
        'MET' : analysis_selections.luminosities["2016"],
    }
    
    plot_data = True
    plot_sc = True
    plot_ratio = True
    plot_signal = False
    plot_bg = False
    plot_error = True
    sc_color = kOrange + 1
    label_text = plotutils.StampStr.PRE
    ratio_label = "data"
    sc_label = "background"
    sc_ratio_label = "bg"
    stamp_scale_factor = True
    
    legend_coordinates = {"x1" : .40, "y1" : .60, "x2" : .92, "y2" : .89}
    
    log_minimum = 0.01
    sc_marker_style = kOpenCircle

class partial_unblinded_track_muon_sc_comparison(unblinded_track_muon_sc_comparison):
    histrograms_file = BaseParams.histograms_root_files_dir + "/partial_unblinded_track_muon_sc_comparison.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = True 
    baseConditions = analysis_selections.injectValues(analysis_selections.ex_track_cond, "2016", "Muons") + " && Entry$ % 10==0"
    scConditions = analysis_selections.injectValues(analysis_selections.sc_ex_track_cond, "2016", "Muons")
    cuts = [
        {"name":"none", "title": "None", "condition" : analysis_selections.common_preselection, "baseline" : baseConditions, "sc" : scConditions },
        #{"name":"sr", "title": "sr", "condition" : "(MHT >= 220 &&  MET >= 200 && BTagsDeepMedium == 0 )", "baseline" : "exclusiveTrack == 1 && trackBDT > 0 && exTrack_invMass < 30 && exclusiveTrackLeptonFlavour == \"Muons\" && exTrack_dilepBDT > 0.1", "sc" : "sc_exclusiveTrack == 1 && sc_trackBDT > 0 && sc_exTrack_invMass < 30 && sc_exclusiveTrackLeptonFlavour == \"Muons\"" }
    ]
    
    transfer_factor = 0.1 * 1.115
    transfer_factor_error = 0
    calculatedLumi = {
        'MET' : analysis_selections.luminosities["2016"] * 0.1,
    }
    stamp_scale_factor = False
    

class unblinded_track_muon_sc_comparison_phase1(unblinded_track_muon_sc_comparison):
    histrograms_file = BaseParams.histograms_root_files_dir + "/unblinded_track_muon_sc_comparison_phase1.root"
    data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim_phase1/sum"
    save_histrograms_to_file = True
    load_histrograms_from_file = True 
    baseConditions = analysis_selections.injectValues(analysis_selections.ex_track_cond, "phase1", "Muons")
    scConditions = analysis_selections.injectValues(analysis_selections.sc_ex_track_cond, "phase1", "Muons")
    cuts = [
        {"name":"none", "title": "None", "condition" : analysis_selections.common_preselection, "baseline" : baseConditions, "sc" : scConditions },
        #{"name":"sr", "title": "sr", "condition" : "(MHT >= 220 &&  MET >= 200 && BTagsDeepMedium == 0 )", "baseline" : "exclusiveTrack == 1 && trackBDT > 0 && exTrack_invMass < 30 && exclusiveTrackLeptonFlavour == \"Muons\" && exTrack_dilepBDT > 0.1", "sc" : "sc_exclusiveTrack == 1 && sc_trackBDT > 0 && sc_exTrack_invMass < 30 && sc_exclusiveTrackLeptonFlavour == \"Muons\"" }
    ]
    calculatedLumi = {
        'MET' : analysis_selections.luminosities["phase1"] * 0.1,
    }
    
    histograms_defs = [
        { "obs" : "exTrack_dilepBDT%%%", "units" : "BDT", "minX" : -1, "maxX" : 1, "bins" : 30,  "sc_obs" : "sc_exTrack_dilepBDT%%%", "linearYspace" : 1.9, "lumiStringPrefix" : "Muons Phase 1"},
        { "obs" : "exTrack_dilepBDT_bins%%%", "formula": "exTrack_dilepBDT%%%", "units" : "BDT", "minX" : -1, "maxX" : 1, "bins" : 30,  "sc_obs" : "sc_exTrack_dilepBDT%%%", "linearYspace" : 1.9, "lumiStringPrefix" : "Muons Phase 1", "customBins"  : [-1,0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,1]},
        { "obs" : "exTrack_dilepBDT_bins_two%%%", "formula": "exTrack_dilepBDT%%%", "units" : "BDT", "minX" : -1, "maxX" : 1, "bins" : 30,  "sc_obs" : "sc_exTrack_dilepBDT%%%", "linearYspace" : 1.9, "lumiStringPrefix" : "Muons Phase 1", "customBins"  : [-1,0,1]},
    ]
    
    injectJetIsoToHistograms(histograms_defs, analysis_selections.jetIsos["Muons"])

class partial_unblinded_track_muon_sc_comparison_phase1(unblinded_track_muon_sc_comparison_phase1):
    histrograms_file = BaseParams.histograms_root_files_dir + "/partial_unblinded_track_muon_sc_comparison_phase1.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = True 
    baseConditions = analysis_selections.injectValues(analysis_selections.ex_track_cond, "phase1", "Muons") + " && Entry$ % 10==0"
    scConditions = analysis_selections.injectValues(analysis_selections.sc_ex_track_cond, "phase1", "Muons")
    cuts = [
        {"name":"none", "title": "None", "condition" : analysis_selections.common_preselection, "baseline" : baseConditions, "sc" : scConditions },
        #{"name":"sr", "title": "sr", "condition" : "(MHT >= 220 &&  MET >= 200 && BTagsDeepMedium == 0 )", "baseline" : "exclusiveTrack == 1 && trackBDT > 0 && exTrack_invMass < 30 && exclusiveTrackLeptonFlavour == \"Muons\" && exTrack_dilepBDT > 0.1", "sc" : "sc_exclusiveTrack == 1 && sc_trackBDT > 0 && sc_exTrack_invMass < 30 && sc_exclusiveTrackLeptonFlavour == \"Muons\"" }
    ]
    
    transfer_factor = 0.1 * 1.096
    transfer_factor_error = 0
    stamp_scale_factor = False

class unblinded_track_electrons_sc_comparison(unblinded_track_muon_sc_comparison):
    histrograms_file = BaseParams.histograms_root_files_dir + "/unblinded_track_electrons_sc_comparison.root"

    save_histrograms_to_file = True
    load_histrograms_from_file = True 
    
    baseConditionsArr = [analysis_selections.ex_track_cond, analysis_selections.ex_track_electrons_filter]
    scConditionsArr = [analysis_selections.sc_ex_track_cond, analysis_selections.sc_ex_track_electrons_filter]
    
    
    baseConditions = analysis_selections.injectValues(analysis_selections.andStringSelections(baseConditionsArr), "2016", "Electrons")
    scConditions = analysis_selections.injectValues(analysis_selections.andStringSelections(scConditionsArr), "2016", "Electrons")
    cuts = [
        {"name":"none", "title": "None", "condition" : analysis_selections.common_preselection, "baseline" : baseConditions, "sc" : scConditions },
        #{"name":"sr", "title": "sr", "condition" : "(MHT >= 220 &&  MET >= 200 && BTagsDeepMedium == 0 )", "baseline" : "exclusiveTrack == 1 && trackBDT > 0 && exTrack_invMass < 30 && exclusiveTrackLeptonFlavour == \"Muons\" && exTrack_dilepBDT > 0.1", "sc" : "sc_exclusiveTrack == 1 && sc_trackBDT > 0 && sc_exTrack_invMass < 30 && sc_exclusiveTrackLeptonFlavour == \"Muons\"" }
    ]
    #injectJetIsoToCuts(cuts, "CorrJetNoMultIso10Dr0.6")
    
    histograms_defs = [
        { "obs" : "exTrack_dilepBDT%%%", "units" : "BDT", "minX" : -1, "maxX" : 1, "bins" : 30,  "sc_obs" : "sc_exTrack_dilepBDT%%%", "linearYspace" : 1.9, "lumiStringPrefix" : "Electrons Phase 0"},
        { "obs" : "exTrack_dilepBDT_bins%%%", "formula": "exTrack_dilepBDT%%%", "units" : "BDT", "minX" : -1, "maxX" : 1, "bins" : 30,  "sc_obs" : "sc_exTrack_dilepBDT%%%", "linearYspace" : 1.9, "lumiStringPrefix" : "Electrons Phase 0", "customBins"  : [-1,0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,1]},
        { "obs" : "exTrack_dilepBDT_bins_two%%%", "formula": "exTrack_dilepBDT%%%", "units" : "BDT", "minX" : -1, "maxX" : 1, "bins" : 30,  "sc_obs" : "sc_exTrack_dilepBDT%%%", "linearYspace" : 1.9, "lumiStringPrefix" : "Electrons Phase 0", "customBins"  : [-1,0,1]},
    ]
    
    injectJetIsoToHistograms(histograms_defs, analysis_selections.jetIsos["Electrons"])  

class partial_unblinded_track_electrons_sc_comparison(unblinded_track_electrons_sc_comparison):
    histrograms_file = BaseParams.histograms_root_files_dir + "/partial_unblinded_track_electrons_sc_comparison.root"

    save_histrograms_to_file = True
    load_histrograms_from_file = True 
    
    baseConditionsArr = [analysis_selections.ex_track_cond, analysis_selections.ex_track_electrons_filter, "Entry$ % 10==0"]
    scConditionsArr = [analysis_selections.sc_ex_track_cond, analysis_selections.sc_ex_track_electrons_filter]
    
    baseConditions = analysis_selections.injectValues(analysis_selections.andStringSelections(baseConditionsArr), "2016", "Electrons")
    scConditions = analysis_selections.injectValues(analysis_selections.andStringSelections(scConditionsArr), "2016", "Electrons")
    cuts = [
        {"name":"none", "title": "None", "condition" : analysis_selections.common_preselection, "baseline" : baseConditions, "sc" : scConditions },
        #{"name":"sr", "title": "sr", "condition" : "(MHT >= 220 &&  MET >= 200 && BTagsDeepMedium == 0 )", "baseline" : "exclusiveTrack == 1 && trackBDT > 0 && exTrack_invMass < 30 && exclusiveTrackLeptonFlavour == \"Muons\" && exTrack_dilepBDT > 0.1", "sc" : "sc_exclusiveTrack == 1 && sc_trackBDT > 0 && sc_exTrack_invMass < 30 && sc_exclusiveTrackLeptonFlavour == \"Muons\"" }
    ]
    
    transfer_factor = 0.1 * 0.954
    transfer_factor_error = 0
    
    calculatedLumi = {
        'MET' : analysis_selections.luminosities["2016"] * 0.1,
    }
    stamp_scale_factor = False

class unblinded_track_electrons_sc_comparison_phase1(unblinded_track_electrons_sc_comparison):
    histrograms_file = BaseParams.histograms_root_files_dir + "/unblinded_track_electrons_sc_comparison_phase1.root"
    data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_phase1/sum/type_sum"

    save_histrograms_to_file = True
    load_histrograms_from_file = True 
    
    baseConditionsArr = [analysis_selections.ex_track_cond, analysis_selections.ex_track_electrons_filter]
    scConditionsArr = [analysis_selections.sc_ex_track_cond, analysis_selections.sc_ex_track_electrons_filter]
    
    baseConditions = analysis_selections.injectValues(analysis_selections.andStringSelections(baseConditionsArr), "phase1", "Electrons")
    scConditions = analysis_selections.injectValues(analysis_selections.andStringSelections(scConditionsArr), "phase1", "Electrons")
    
    cuts = [
        {"name":"none", "title": "None", "condition" : analysis_selections.common_preselection, "baseline" : baseConditions, "sc" : scConditions },
        #{"name":"sr", "title": "sr", "condition" : "(MHT >= 220 &&  MET >= 200 && BTagsDeepMedium == 0 )", "baseline" : "exclusiveTrack == 1 && trackBDT > 0 && exTrack_invMass < 30 && exclusiveTrackLeptonFlavour == \"Muons\" && exTrack_dilepBDT > 0.1", "sc" : "sc_exclusiveTrack == 1 && sc_trackBDT > 0 && sc_exTrack_invMass < 30 && sc_exclusiveTrackLeptonFlavour == \"Muons\"" }
    ]
    #injectJetIsoToCuts(cuts, "CorrJetNoMultIso10Dr0.6")
    
    histograms_defs = [
        { "obs" : "exTrack_dilepBDT%%%", "units" : "BDT", "minX" : -1, "maxX" : 1, "bins" : 30,  "sc_obs" : "sc_exTrack_dilepBDT%%%", "linearYspace" : 1.9, "lumiStringPrefix" : "Electrons Phase 1"},
        { "obs" : "exTrack_dilepBDT_bins%%%", "formula": "exTrack_dilepBDT%%%", "units" : "BDT", "minX" : -1, "maxX" : 1, "bins" : 30,  "sc_obs" : "sc_exTrack_dilepBDT%%%", "linearYspace" : 1.9, "lumiStringPrefix" : "Electrons Phase 1", "customBins"  : [-1,0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,1]},
        { "obs" : "exTrack_dilepBDT_bins_two%%%", "formula": "exTrack_dilepBDT%%%", "units" : "BDT", "minX" : -1, "maxX" : 1, "bins" : 30,  "sc_obs" : "sc_exTrack_dilepBDT%%%", "linearYspace" : 1.9, "lumiStringPrefix" : "Electrons Phase 1", "customBins"  : [-1,0,1]},
    ]
    
    injectJetIsoToHistograms(histograms_defs, analysis_selections.jetIsos["Electrons"])  
    calculatedLumi = {
        'MET' : analysis_selections.luminosities["phase1"],
    }

class partial_unblinded_track_electrons_sc_comparison_phase1(unblinded_track_electrons_sc_comparison_phase1):
    histrograms_file = BaseParams.histograms_root_files_dir + "/partial_unblinded_track_electrons_sc_comparison_phase1.root"

    save_histrograms_to_file = True
    load_histrograms_from_file = True 
    
    baseConditionsArr = [analysis_selections.ex_track_cond, analysis_selections.ex_track_electrons_filter, "Entry$ % 10==0"]
    scConditionsArr = [analysis_selections.sc_ex_track_cond, analysis_selections.sc_ex_track_electrons_filter]
    
    baseConditions = analysis_selections.injectValues(analysis_selections.andStringSelections(baseConditionsArr), "phase1", "Electrons")
    scConditions = analysis_selections.injectValues(analysis_selections.andStringSelections(scConditionsArr), "phase1", "Electrons")
    cuts = [
        {"name":"none", "title": "None", "condition" : analysis_selections.common_preselection, "baseline" : baseConditions, "sc" : scConditions },
        #{"name":"sr", "title": "sr", "condition" : "(MHT >= 220 &&  MET >= 200 && BTagsDeepMedium == 0 )", "baseline" : "exclusiveTrack == 1 && trackBDT > 0 && exTrack_invMass < 30 && exclusiveTrackLeptonFlavour == \"Muons\" && exTrack_dilepBDT > 0.1", "sc" : "sc_exclusiveTrack == 1 && sc_trackBDT > 0 && sc_exTrack_invMass < 30 && sc_exclusiveTrackLeptonFlavour == \"Muons\"" }
    ]
    
    #transfer_factor = 0.1 * 1.075
    transfer_factor = 0.1 * 1.075
    transfer_factor_error = 0
    calculatedLumi = {
        'MET' : analysis_selections.luminosities["phase1"] * 0.1,
    }
    stamp_scale_factor = False

class unblinded_dimuon(BaseParams):
    histrograms_file = BaseParams.histograms_root_files_dir + "/unblinded_dimuon_topup.root"
    
    save_histrograms_to_file = True
    load_histrograms_from_file = True
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/slim_sum_total"
    data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim/slim_sum/"
    
    plot_error = True
    plot_data = True
    plot_ratio = True
    plot_data_for_bg_estimation = True
    
    plot_signal = False
    blind_data = False
    bg_retag = True
    
    jetIsoStr = ""
    
    jetIso = analysis_selections.jetIsos["Muons"]
    
    #two_leptons_iso_condition
    baseConditionsArr = [analysis_selections.common_preselection, analysis_selections.two_leptons_condition, analysis_selections.two_leptons_condition_zoo_removal, analysis_selections.two_leptons_opposite_sign, analysis_selections.mtautau_veto]
    
    baseConditions = analysis_selections.injectValues(analysis_selections.andStringSelections(baseConditionsArr), "2016", "Muons")
    baseConditionsSos = analysis_selections.injectValues(analysis_selections.andStringSelections(baseConditionsArr + [analysis_selections.sos_orth_condition]), "2016", "Muons")
    baseConditionsIso = analysis_selections.injectValues(analysis_selections.andStringSelections([analysis_selections.two_leptons_iso_condition]), "2016", "Muons")
    
    
    cuts = [
        {"name":"none", "title": "None", "condition" : baseConditions, "data_only" : baseConditionsIso},
        {"name":"sos", "title": "SOS", "condition" : baseConditionsSos, "data_only" : baseConditionsIso},
    ]
    injectJetIsoToCuts(cuts, jetIso)
    
    histograms_defs = [     
        { "obs" : "full_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT output", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,1], "legendCol" : 1, "legendCoor" : {"x1" : .63, "y1" : .63, "x2" : .99, "y2" : .89}, "linearYspace" : 1.6, "logYspace" : 3000 },
        { "obs" : "final_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "units" : "BDT output", "customBins"  : [-1,0,0.1,0.2,0.3,0.4,0.5,1] , "legendCol" : 1, "legendCoor" : {"x1" : .63, "y1" : .63, "x2" : .99, "y2" : .89}, "linearYspace" : 1.6, "logYspace" : 3000 },
        { "obs" : "fine_dilepBDTphase1%%%", "formula" : "dilepBDTphase1%%%", "minX" : -1, "maxX" : 1, "bins" : 40, "units" : "BDT phase1", "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}}
    ]
    injectJetIsoToHistograms(histograms_defs, jetIso)
    
    weightString = {
        'MET' : analysis_selections.full_sim_weights["2016"],
    }
    
    calculatedLumi = {
        'MET' : analysis_selections.luminosities["2016"]
    }
    
    bgReTaggingFactors = {
        "tautau" : analysis_selections.tautau_factors["2016"]["Muons"],
        #"non-iso" : analysis_selections.non_iso_2l_factors["2016"]["Muons"]
        #"non-iso" : [0.698,0.137]
        "non-iso" : [0.73,0.14]
    }
    
    bgReTagging = {
        "tautau" : "tautau%%% && isoCr%%% == 0",
        "non-iso" : "isoCr%%% >= 1"
    }
    
    stamp_scale_factor = True
    
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
    
    label_text = plotutils.StampStr.PRE
    
    log_minimum = 0.01

class partial_unblinded_dimuon(unblinded_dimuon):

    histrograms_file = BaseParams.histograms_root_files_dir + "/partial_unblinded_dimuon.root"
    
    save_histrograms_to_file = True
    load_histrograms_from_file = True

    jetIso = analysis_selections.jetIsos["Muons"]
    
    #two_leptons_iso_condition
    baseConditionsArr = [analysis_selections.common_preselection, analysis_selections.two_leptons_condition, analysis_selections.two_leptons_condition_zoo_removal, analysis_selections.two_leptons_opposite_sign, analysis_selections.mtautau_veto]
    
    baseConditions = analysis_selections.injectValues(analysis_selections.andStringSelections(baseConditionsArr), "2016", "Muons")
    baseConditionsSos = analysis_selections.injectValues(analysis_selections.andStringSelections(baseConditionsArr + [analysis_selections.sos_orth_condition]), "2016", "Muons")
    baseConditionsIso = analysis_selections.injectValues(analysis_selections.andStringSelections([analysis_selections.two_leptons_iso_condition, "Entry$ % 10==0"]), "2016", "Muons")
    
    
    cuts = [
        {"name":"none", "title": "None", "condition" : baseConditions, "data_only" : baseConditionsIso},
        {"name":"sos", "title": "SOS", "condition" : baseConditionsSos, "data_only" : baseConditionsIso},
    ]
    injectJetIsoToCuts(cuts, jetIso)
    
    
    bgReTaggingFactors = {
        "tautau" : [0.1 * analysis_selections.tautau_factors["2016"]["Muons"][0],analysis_selections.tautau_factors["2016"]["Muons"][1]],
        #"non-iso" : [0.1 * analysis_selections.non_iso_2l_factors["2016"]["Muons"][0], analysis_selections.non_iso_2l_factors["2016"]["Muons"][1]]
        "non-iso" : [0.079,0.037]
       
    }
    
    calculatedLumi = {
        'MET' : analysis_selections.luminosities["2016"] * 0.1,
    }
    stamp_scale_factor = False

class unblinded_dimuon_phase1(unblinded_dimuon):
    histrograms_file = BaseParams.histograms_root_files_dir + "/unblinded_dimuon_phase1_topup.root"
    
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_phase1/sum/slim_sum_total"
    data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim_phase1/slim_sum/"
    
    save_histrograms_to_file = True
    load_histrograms_from_file = True
    
    jetIso = analysis_selections.jetIsos["Muons"]
    
    baseConditionsArr = [analysis_selections.common_preselection, analysis_selections.two_leptons_condition, analysis_selections.two_leptons_condition_zoo_removal, analysis_selections.two_leptons_opposite_sign, analysis_selections.mtautau_veto]
    
    baseConditions = analysis_selections.injectValues(analysis_selections.andStringSelections(baseConditionsArr), "phase1", "Muons")
    baseConditionsSos = analysis_selections.injectValues(analysis_selections.andStringSelections(baseConditionsArr + [analysis_selections.sos_orth_condition]), "phase1", "Muons")
    baseConditionsIso = analysis_selections.injectValues(analysis_selections.andStringSelections([analysis_selections.two_leptons_iso_condition]), "phase1", "Muons")
    
    cuts = [
        {"name":"none", "title": "None", "condition" : baseConditions, "data_only" : baseConditionsIso},
        {"name":"sos", "title": "SOS", "condition" : baseConditionsSos, "data_only" : baseConditionsIso},
    ]
    injectJetIsoToCuts(cuts, jetIso)
    
    bgReTagging = {
        "tautau" : "tautau%%% && isoCr%%% == 0",
        "non-iso" : "isoCr%%% >= 1"
    }
    injectJetIsoToMapValues(bgReTagging, jetIso)
    
    bgReTaggingFactors = {
        "tautau" : analysis_selections.tautau_factors["phase1"]["Muons"],
        #"non-iso" : analysis_selections.non_iso_2l_factors["phase1"]["Muons"]
        
        #"non-iso" : [0.622,0.058]
        #"non-iso" : [0.615,0.057]
        "non-iso" : [0.615,0.057]
        
    }
    
    histograms_defs = [     
        { "obs" : "full_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT output", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,1], "legendCol" : 1, "legendCoor" : {"x1" : .63, "y1" : .63, "x2" : .99, "y2" : .89}, "linearYspace" : 1.6, "logYspace" : 3000 },
        { "obs" : "final_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "units" : "BDT output", "customBins"  : [-1,0,0.1,0.2,0.3,0.4,0.5,1] , "legendCol" : 1, "legendCoor" : {"x1" : .63, "y1" : .63, "x2" : .99, "y2" : .89}, "linearYspace" : 1.6, "logYspace" : 3000 },
        { "obs" : "fine_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 40, "units" : "BDT", "legendCol" : 1, "legendCoor" : {"x1" : .72, "y1" : .60, "x2" : .99, "y2" : .89}}
    ]
    injectJetIsoToHistograms(histograms_defs, jetIso)
    
    weightString = {
        'MET' : analysis_selections.full_sim_weights["phase1"],
    }
    
    calculatedLumi = {
        'MET' : analysis_selections.luminosities["phase1"]
    }
    
    dataWeights = {
        'MET' : "hemFailureVetoElectrons * hemFailureVetoJets * hemFailureVetoMuons"
    }

class partial_unblinded_dimuon_phase1(unblinded_dimuon_phase1):
    
    histrograms_file = BaseParams.histograms_root_files_dir + "/partial_unblinded_dimuon_phase1.root"
    
    save_histrograms_to_file = True
    load_histrograms_from_file = True

    jetIso = analysis_selections.jetIsos["Muons"]
    
    #two_leptons_iso_condition
    baseConditionsArr = [analysis_selections.common_preselection, analysis_selections.two_leptons_condition, analysis_selections.two_leptons_condition_zoo_removal, analysis_selections.two_leptons_opposite_sign, analysis_selections.mtautau_veto]
    
     
    baseConditions = analysis_selections.injectValues(analysis_selections.andStringSelections(baseConditionsArr), "phase1", "Muons")
    baseConditionsSos = analysis_selections.injectValues(analysis_selections.andStringSelections(baseConditionsArr + [analysis_selections.sos_orth_condition]), "phase1", "Muons")
    baseConditionsIso = analysis_selections.injectValues(analysis_selections.andStringSelections([analysis_selections.two_leptons_iso_condition, "Entry$ % 10==0"]), "phase1", "Muons")
    
    
    cuts = [
        {"name":"none", "title": "None", "condition" : baseConditions, "data_only" : baseConditionsIso},
        {"name":"sos", "title": "SOS", "condition" : baseConditionsSos, "data_only" : baseConditionsIso},
    ]
    injectJetIsoToCuts(cuts, jetIso)
    
    calculatedLumi = {
        'MET' : analysis_selections.luminosities["phase1"] * 0.1
    }
    
    bgReTaggingFactors = {
        "tautau" : [0.1 * analysis_selections.tautau_factors["phase1"]["Muons"][0],analysis_selections.tautau_factors["phase1"]["Muons"][1]],
        "non-iso" : [0.1 * analysis_selections.non_iso_2l_factors["phase1"]["Muons"][0], analysis_selections.non_iso_2l_factors["phase1"]["Muons"][1]]
        #"non-iso" : [0.077,0.017]
    }
    stamp_scale_factor = False

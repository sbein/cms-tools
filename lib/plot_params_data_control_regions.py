import sys
import os
import copy
import ROOT

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib"))

from plot_params_base import *
import plot_params_analysis_categories


class dilepton_muons_data_control_region(BaseParams):
    signal_dir = signals
    signal_names = signalNames
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/slim_sum/type_sum"
    data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim/slim_sum/"
    cuts = [
        #{"name":"none", "title": "None", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && isoCr%%% == 0 && sameSign%%% == 0 && dilepBDT%%% < 0)", "baseline" : "", "sc" : ""},
        {"name":"passesUniversalSelection", "title": "passesUniversalSelection", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && isoCr%%% == 0 && sameSign%%% == 0 && dilepBDT%%% < 0 && passesUniversalSelection == 1)", "baseline" : "", "sc" : ""},
        #{"name":"isocr", "title": "isocr", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && isoCr%%% > 0 && sameSign%%% == 0)", "baseline" : "", "sc" : ""},
        #{"name":"isocr_passesUniversalSelection", "title": "isocr_passesUniversalSelection", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && isoCr%%% > 0 && sameSign%%% == 0 && passesUniversalSelection == 1)", "baseline" : "", "sc" : ""},
        #{"name":"njets", "title": "NJets > 1", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && isoCr%%% == 0 && sameSign%%% == 0 && dilepBDT%%% < 0 && NJets > 1)", "baseline" : "", "sc" : ""},
        #{"name":"non-orth", "title": "Non Orth", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 200 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && dilepBDT%%% > 0.3 && isoCr%%% == 0)", "baseline" : "sameSign%%% == 0", "sc" : "sameSign%%% == 1"},
        #{"name":"orth", "title": "Orth", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 200 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && dilepBDT%%% > 0.1 && (leptons%%%[1].Pt() <= 3.5 || deltaR%%% <= 0.3) && isoCr%%% == 0)", "baseline" : "sameSign%%% == 0", "sc" : "sameSign%%% == 1"},
    ]
    
    #(twoLeptons == 1 && (leptons[1].Pt() <= 3.5 || deltaR <= 0.3) && MHT >= 220 &&  MET >= 200 && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && dilepBDT > 0.1 && BTagsDeepMedium == 0 && vetoElectronsPassIsoTightID == 0 && vetoMuonsPassIsoPassIso == 0 && @leptons.size() == 2 && leptonFlavour == \"" + lep + "\" && sameSign == 0)", True)
    histograms_defs = []
    histograms_defs.extend(copy.deepcopy(plot_params_analysis_categories.common_histograms))
    histograms_defs.extend(copy.deepcopy(plot_params_analysis_categories.two_leps_histograms))
    #histograms_defs.extend(extra_study_obs)
    
    weightString = {
        #'MET' : "BranchingRatio * Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * puWeight",
        'MET' : "BranchingRatio * Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2016",
        #'MET' : "BranchingRatio * Weight",
    }
    
    calculatedLumi = {
        #Before nomult
        #'MET' : 35.712736198,
        #Afrer nomult
        'MET' : 35.73895434
    }
    
    turnOnOnlyUsedObsInTree = False
    usedObs = ["BranchingRatio","Weight","passedMhtMet6pack","tEffhMetMhtRealXMht2016","puWeight","MinDeltaPhiMhtJets","BTagsDeepMedium","twoLeptons%%%","MHT","MET","leptonFlavour%%%","invMass%%%","vetoElectronsPassIso","vetoMuonsPassIso","isoCr%%%","sameSign%%%", "leptons%%%", "deltaR%%%"]
    
    plot_sc = False
    plot_data = True
    plot_signal = False
    plot_overflow = True
    plot_ratio = True
    
    blind_data = False

    save_histrograms_to_file = True
    load_histrograms_from_file = False
    
    
    jetIsoStr = "CorrJetNoMultIso10Dr0.6"
    #jetIsoStr = "NoIso"
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_data_control_region2.root"
    #"/afs/desy.de/user/n/nissanuv/CMSSW_10_1_0/src/cms-tools/analysis/scripts/dilepton_muons" + jetIsoStr + ".root"
    #cuts = copy.deepcopy(dilepton_muons.cuts)
    injectJetIsoToCuts(cuts, jetIsoStr)
    #histograms_defs = copy.deepcopy(dilepton_muons.histograms_defs)
    injectJetIsoToHistograms(histograms_defs, jetIsoStr)
    #usedObs = copy.deepcopy(dilepton_muons.usedObs)
    #print("before", usedObs)
    #injectJetIsoToList(usedObs, jetIsoStr)
    #print("after", usedObs)
    #exit(0)
    sig_line_width = 3
    plot_error = True


class dilepton_muons_data_control_region_iso_cr(dilepton_muons_data_control_region):
    cuts = [
        {"name":"none", "title": "Low BDT", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && isoCr%%% > 0 && sameSign%%% == 0 && dilepBDT%%% < 0)", "baseline" : "", "sc" : ""},
        {"name":"all", "title": "all", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && isoCr%%% > 0 && sameSign%%% == 0)", "baseline" : "", "sc" : ""},
        {"name":"njets", "title": "njets > 1", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && isoCr%%% > 0 && sameSign%%% == 0 && NJets > 1)", "baseline" : "", "sc" : ""},
        #{"name":"non-orth", "title": "Non Orth", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 200 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && dilepBDT%%% > 0.3 && isoCr%%% == 0)", "baseline" : "sameSign%%% == 0", "sc" : "sameSign%%% == 1"},
        #{"name":"orth", "title": "Orth", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 200 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && dilepBDT%%% > 0.1 && (leptons%%%[1].Pt() <= 3.5 || deltaR%%% <= 0.3) && isoCr%%% == 0)", "baseline" : "sameSign%%% == 0", "sc" : "sameSign%%% == 1"},
    ]
    jetIsoStr = "CorrJetIso10.5Dr0.55"
    #jetIsoStr = "NoIso"
    injectJetIsoToCuts(cuts, jetIsoStr)
    histograms_defs = []
    histograms_defs.extend(copy.deepcopy(plot_params_analysis_categories.common_histograms))
    histograms_defs.extend(copy.deepcopy(plot_params_analysis_categories.two_leps_histograms))
    injectJetIsoToHistograms(histograms_defs, jetIsoStr)
    normalise = True

class dilepton_muons_data_control_region_met_filters(dilepton_muons_data_control_region_iso_cr):
    histrograms_file = "/afs/desy.de/user/n/nissanuv/CMSSW_10_1_0/src/cms-tools/analysis/scripts/dilepton_muons_data_control_region_met_filters.root" 
    load_histrograms_from_file = True
    cuts = [
        {"name":"none", "title": "None", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && isoCr%%% == 0 && sameSign%%% == 0 )", "baseline" : "1", "sc" : "passesUniversalSelection == 1"},
        #{"name":"all", "title": "all", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && isoCr%%% > 0 && sameSign%%% == 0)", "baseline" : "", "sc" : ""},
        #{"name":"njets", "title": "njets > 1", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && isoCr%%% > 0 && sameSign%%% == 0 && NJets > 1)", "baseline" : "", "sc" : ""},
        #{"name":"non-orth", "title": "Non Orth", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 200 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && dilepBDT%%% > 0.3 && isoCr%%% == 0)", "baseline" : "sameSign%%% == 0", "sc" : "sameSign%%% == 1"},
        #{"name":"orth", "title": "Orth", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 200 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && dilepBDT%%% > 0.1 && (leptons%%%[1].Pt() <= 3.5 || deltaR%%% <= 0.3) && isoCr%%% == 0)", "baseline" : "sameSign%%% == 0", "sc" : "sameSign%%% == 1"},
    ]
    normalise = False
    jetIsoStr = "CorrJetNoMultIso10Dr0.6"
    injectJetIsoToCuts(cuts, jetIsoStr)
    histograms_defs = []
    
    histograms_defs = [
    
    { "obs" : "MET", "minX" : 0, "maxX" : 800, "bins" : 30 },
    ]
    
    #histograms_defs.extend(plot_params_analysis_categories.common_histograms)
    #injectJetIsoToHistograms(histograms_defs, jetIsoStr)
    data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim/sum/"
    plot_bg = False
    plot_sc = True
    sc_label = "passesUniversalSelection"
    sc_ratio_label = "US"
    plot_ratio = True

class dilepton_muons_data_control_region_phase1_new(dilepton_muons_data_control_region):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_data_control_region_phase1_new.root"
    load_histrograms_from_file = True
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_phase1/sum/slim_sum/type_sum"
    data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim_phase1/slim_sum/"
    baseConditions = analysis_selections.injectValues(analysis_selections.andStringSelections(analysis_selections.two_leptons_cr_conditions), "phase1", "Muons")
    cuts = [
        {"name":"none", "title": "None", "condition" : baseConditions, "baseline" : "", "sc" : ""},
        #{"name":"met", "title": "MET > 200", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 200 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && isoCr%%% == 0 && sameSign%%% == 0 && dilepBDT%%% < 0 && passesUniversalSelection == 1)", "baseline" : "", "sc" : ""},
    ]
    normalise = False
    jetIsoStr = analysis_selections.jetIsos["Muons"]
    #injectJetIsoToCuts(cuts, jetIsoStr)
    
    #print("BaseConditions", baseConditions)
    #print("BaseConditions orig", "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && isoCr%%% == 0 && sameSign%%% == 0 && dilepBDT%%% < 0 && passesUniversalSelection == 1)")
    
    y_title_offset = 0.8
    
    histograms_defs = []
    histograms_defs.extend(copy.deepcopy(plot_params_analysis_categories.common_histograms))
    histograms_defs.extend(copy.deepcopy(plot_params_analysis_categories.two_leps_histograms))
    injectJetIsoToHistograms(histograms_defs, jetIsoStr)
    
    turnOnOnlyUsedObsInTree = False
    #usedObs = ["passesUniversalSelection", "BranchingRatio","Weight","passedMhtMet6pack","tEffhMetMhtRealXMht2016","puWeight","MinDeltaPhiMhtJets","BTagsDeepMedium","twoLeptons%%%","MHT","MET","leptonFlavour%%%","invMass%%%","vetoElectronsPassIso","vetoMuonsPassIso","isoCr%%%","sameSign%%%", "leptons%%%", "deltaR%%%", "trackBDT%%%", "exclusiveTrack%%%", "exTrack_invMass%%%", "exclusiveTrackLeptonFlavour%%%", "sc_exclusiveTrack%%%", "sc_trackBDT%%%", "sc_exTrack_invMass%%%", "sc_exclusiveTrackLeptonFlavour%%%", "exTrack_dilepBDT%%%", "sc_exTrack_dilepBDT%%%"]
    #$injectJetIsoToList(usedObs, jetIsoStr)
    
    calculatedLumi = {
        #'MET' : 99.226209715
        'MET' : analysis_selections.luminosities["phase1"]
    }
    
    weightString = {
        #'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2017 * BranchingRatio",
        'MET' : analysis_selections.full_sim_weights["phase1"]
    }


class dilepton_muons_data_jpsi_control_region(dilepton_muons_data_control_region_phase1_new):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_data_jpsi_control_region.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = False
    
    normalise = True
    
    histograms_defs = [
    
    { "obs" : "MET", "minX" : 120, "maxX" : 800, "bins" : 5, "linearYspace" : 1.6 },
    { "obs" : "MHT", "minX" : 220, "maxX" : 500, "bins" : 5, "units" : "H_{T}^{Miss} [GeV]", "linearYspace" : 1.4 },
    { "obs" : "HT", "minX" : 0, "maxX" : 700, "bins" : 5, "logYspace" : 10000, "linearYspace" : 1.6 },
    { "obs" : "NJets", "minX" : 0, "maxX" : 7, "bins" : 7, "linearYspace" : 1.6 },
    { "obs" : "LeadingJetPt", "minX" : 0, "maxX" : 800, "bins" : 5, "units" : "p_{T}(j_{1}) [GeV]", "linearYspace" : 1.5 },
    { "obs" : "abs(LeadingJet.Eta())", "minX" : 0, "maxX" : 2.5, "bins" : 5, "usedObs" : ["LeadingJet"], "units" : "|\eta_{j_{1}}|", "linearYspace" : 1.8 },
    {"obs" : "invMass%%%", "minX" : 3.0, "maxX" : 3.21, "bins" : 9, "blind" : [4,None],"units" : "M_{ll} [GeV]", "linearYspace" : 2.0 },
    #{ "obs" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 10,"units" : "BDT", "linearYspace" : 1.8 },
    #{ "obs" : "custom_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 10, "logYspace" : 8000, "linearYspace" : 1.6, "blind" : [None,0.1],"units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,1] },
    ##{ "obs" : "dileptonPt%%%", "minX" : 0, "maxX" : 30, "bins" : 5, "units" : "p_{T}(ll) [GeV]", "linearYspace" : 1.6 },
    ##{ "obs" : "deltaEta%%%", "minX" : 0, "maxX" : 4, "bins" : 5, "units" : "\Delta_{}\eta", "linearYspace" : 1.6 },
    #{ "obs" : "deltaR%%%", "minX" : 0, "maxX" : 3, "bins" : 15, "units" : "\Delta_{}R_{ll}", "linearYspace" : 1.8 },
    { "obs" : "dilepHt%%%", "minX" : 200, "maxX" : 400, "bins" : 5 },
    { "obs" : "mt1%%%", "minX" : 0, "maxX" : 100, "bins" : 5, "units" : "m_{T}(l_{1}) [GeV]", "linearYspace" : 1.5 },
    { "obs" : "leptons%%%[0].Pt()", "minX" : 2, "maxX" : 15, "bins" : 5, "usedObs" : ["leptons%%%"], "units" : "p_{T}(l_{1}) [GeV]", "linearYspace" : 2.0 },
    { "obs" : "leptons%%%[1].Pt()", "minX" : 2, "maxX" : 15, "bins" : 5, "usedObs" : ["leptons%%%"], "units" : "p_{T}(l_{2}) [GeV]", "linearYspace" : 2.0 },
    { "obs" : "abs(leptons%%%[0].Eta())", "minX" : 0, "maxX" : 2.4, "bins" : 5, "usedObs" : ["leptons%%%"] },
    { "obs" : "abs(leptons%%%[1].Eta())", "minX" : 0, "maxX" : 2.4, "bins" : 5, "usedObs" : ["leptons%%%"] },
]
    
    
    jetIsoStr = analysis_selections.jetIsos["Muons"]
    injectJetIsoToHistograms(histograms_defs, jetIsoStr)
    
    colorPalette = plotutils.defaultOrigColorPalette
    
    #&& MinDeltaPhiMhtJets > 0.4
    common_preselection = "passedMhtMet6pack && passesUniversalSelection  && MHT >= 200 &&  MET >= 140 && BTagsDeepMedium >= 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0"
    #analysis_selections.two_leptons_iso_condition,
    #selections = [common_preselection, analysis_selections.two_leptons_condition,  "(invMass%%% > 3 && invMass%%% < 3.2)", analysis_selections.two_leptons_opposite_sign, "HT>MHT"]
    selections = [common_preselection, analysis_selections.two_leptons_condition,  "(invMass%%% > 3.05 && invMass%%% < 3.2)", analysis_selections.two_leptons_opposite_sign, "HT>MHT"]    
    cutString = analysis_selections.getDataString("2016", "Muons", selections)
    cuts = [ 
        {"name":"JPsi", "title": "JPsi cut", "condition" : cutString, "baseline" : "", "sc" : ""},
    ]
    
    calculatedLumi = {
        #'MET' : 99.226209715
        'MET' : analysis_selections.luminosities["phase1"]
    }
    
    weightString = {
        #'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2017 * BranchingRatio",
        'MET' : analysis_selections.full_sim_weights["phase1"]
    }
    
    bg_retag = True
    
    bgReTagging = {
        "jpsi" : "j_psi%%%",
        "non-jpsi" : "!j_psi%%%"
    }
    injectJetIsoToMapValues(bgReTagging, jetIsoStr)
    bgReTaggingOrder = {
        "non-jpsi" : 0,
        "jpsi" : 1
    }
    bgReTaggingNames = {
        "jpsi" : "J/#psi",
        "non-jpsi" : "Non-J/#psi"
    }
    
    label_text = plotutils.StampStr.PRE
    


class dilepton_muons_data_control_region_iso_cr(dilepton_muons_data_control_region):
    cuts = [
        {"name":"none", "title": "Low BDT", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && isoCr%%% > 0 && sameSign%%% == 0 && dilepBDT%%% < 0)", "baseline" : "", "sc" : ""},
        {"name":"all", "title": "all", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && isoCr%%% > 0 && sameSign%%% == 0)", "baseline" : "", "sc" : ""},
        {"name":"njets", "title": "njets > 1", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && isoCr%%% > 0 && sameSign%%% == 0 && NJets > 1)", "baseline" : "", "sc" : ""},
        #{"name":"non-orth", "title": "Non Orth", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 200 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && dilepBDT%%% > 0.3 && isoCr%%% == 0)", "baseline" : "sameSign%%% == 0", "sc" : "sameSign%%% == 1"},
        #{"name":"orth", "title": "Orth", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 200 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && dilepBDT%%% > 0.1 && (leptons%%%[1].Pt() <= 3.5 || deltaR%%% <= 0.3) && isoCr%%% == 0)", "baseline" : "sameSign%%% == 0", "sc" : "sameSign%%% == 1"},
    ]
    jetIsoStr = "CorrJetIso10.5Dr0.55"
    #jetIsoStr = "NoIso"
    injectJetIsoToCuts(cuts, jetIsoStr)
    histograms_defs = []
    histograms_defs.extend(copy.deepcopy(plot_params_analysis_categories.common_histograms))
    histograms_defs.extend(copy.deepcopy(plot_params_analysis_categories.two_leps_histograms))
    injectJetIsoToHistograms(histograms_defs, jetIsoStr)
    normalise = True

class dilepton_muons_data_control_region_met_filters(dilepton_muons_data_control_region_iso_cr):
    histrograms_file = "/afs/desy.de/user/n/nissanuv/CMSSW_10_1_0/src/cms-tools/analysis/scripts/dilepton_muons_data_control_region_met_filters.root" 
    load_histrograms_from_file = True
    cuts = [
        {"name":"none", "title": "None", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && isoCr%%% == 0 && sameSign%%% == 0 )", "baseline" : "1", "sc" : "passesUniversalSelection == 1"},
        #{"name":"all", "title": "all", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && isoCr%%% > 0 && sameSign%%% == 0)", "baseline" : "", "sc" : ""},
        #{"name":"njets", "title": "njets > 1", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && isoCr%%% > 0 && sameSign%%% == 0 && NJets > 1)", "baseline" : "", "sc" : ""},
        #{"name":"non-orth", "title": "Non Orth", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 200 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && dilepBDT%%% > 0.3 && isoCr%%% == 0)", "baseline" : "sameSign%%% == 0", "sc" : "sameSign%%% == 1"},
        #{"name":"orth", "title": "Orth", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 200 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && dilepBDT%%% > 0.1 && (leptons%%%[1].Pt() <= 3.5 || deltaR%%% <= 0.3) && isoCr%%% == 0)", "baseline" : "sameSign%%% == 0", "sc" : "sameSign%%% == 1"},
    ]
    normalise = False
    jetIsoStr = "CorrJetNoMultIso10Dr0.6"
    injectJetIsoToCuts(cuts, jetIsoStr)
    histograms_defs = []
    
    histograms_defs = [
    
    { "obs" : "MET", "minX" : 0, "maxX" : 800, "bins" : 30 },
    ]
    
    #histograms_defs.extend(plot_params_analysis_categories.common_histograms)
    #injectJetIsoToHistograms(histograms_defs, jetIsoStr)
    data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim/sum/"
    plot_bg = False
    plot_sc = True
    sc_label = "passesUniversalSelection"
    sc_ratio_label = "US"
    plot_ratio = True

class dilepton_muons_data_control_region_phase1_new(dilepton_muons_data_control_region):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_data_control_region_phase1_new.root"
    load_histrograms_from_file = True
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_phase1/sum/slim_sum/type_sum"
    data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim_phase1/slim_sum/"
    baseConditions = analysis_selections.injectValues(analysis_selections.andStringSelections(analysis_selections.two_leptons_cr_conditions), "phase1", "Muons")
    cuts = [
        {"name":"none", "title": "None", "condition" : baseConditions, "baseline" : "", "sc" : ""},
        #{"name":"met", "title": "MET > 200", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 200 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && isoCr%%% == 0 && sameSign%%% == 0 && dilepBDT%%% < 0 && passesUniversalSelection == 1)", "baseline" : "", "sc" : ""},
    ]
    normalise = False
    jetIsoStr = analysis_selections.jetIsos["Muons"]
    #injectJetIsoToCuts(cuts, jetIsoStr)
    
    print("BaseConditions", baseConditions)
    print("BaseConditions orig", "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && isoCr%%% == 0 && sameSign%%% == 0 && dilepBDT%%% < 0 && passesUniversalSelection == 1)")
    
    y_title_offset = 0.8
    
    histograms_defs = []
    histograms_defs.extend(copy.deepcopy(plot_params_analysis_categories.common_histograms))
    histograms_defs.extend(copy.deepcopy(plot_params_analysis_categories.two_leps_histograms))
    injectJetIsoToHistograms(histograms_defs, jetIsoStr)
    
    turnOnOnlyUsedObsInTree = False
    #usedObs = ["passesUniversalSelection", "BranchingRatio","Weight","passedMhtMet6pack","tEffhMetMhtRealXMht2016","puWeight","MinDeltaPhiMhtJets","BTagsDeepMedium","twoLeptons%%%","MHT","MET","leptonFlavour%%%","invMass%%%","vetoElectronsPassIso","vetoMuonsPassIso","isoCr%%%","sameSign%%%", "leptons%%%", "deltaR%%%", "trackBDT%%%", "exclusiveTrack%%%", "exTrack_invMass%%%", "exclusiveTrackLeptonFlavour%%%", "sc_exclusiveTrack%%%", "sc_trackBDT%%%", "sc_exTrack_invMass%%%", "sc_exclusiveTrackLeptonFlavour%%%", "exTrack_dilepBDT%%%", "sc_exTrack_dilepBDT%%%"]
    #$injectJetIsoToList(usedObs, jetIsoStr)
    
    calculatedLumi = {
        #'MET' : 99.226209715
        'MET' : analysis_selections.luminosities["phase1"]
    }
    
    weightString = {
        #'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2017 * BranchingRatio",
        'MET' : analysis_selections.full_sim_weights["phase1"]
    }
    
    
class track_muons_data_control_region(BaseParams):
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/type_sum"
    data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim/sum/"
    histrograms_file = BaseParams.histograms_root_files_dir + "/track_muons_data_control_region.root"
    
    histograms_defs = [
        { "obs" : "exTrack_dilepBDT%%%", "units" : "BDT", "minX" : -1, "maxX" : 1, "bins" : 30, "blind" : [0,1], "sc_obs" : "sc_exTrack_dilepBDT%%%", "linearYspace" : 1.5},
    ]
    
    jetIsoStr = "CorrJetNoMultIso10Dr0.6"
    injectJetIsoToHistograms(histograms_defs, jetIsoStr)  
    
    
    cuts = [
        {"name":"none", "title": "None", "condition" : "(passesUniversalSelection == 1 && MinDeltaPhiMhtJets > 0.4 && MHT >= 220 &&  MET >= 140 && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)", "baseline" : "exclusiveTrack%%% == 1 && trackBDT%%% > 0 && exTrack_invMass%%% < 12 && exclusiveTrackLeptonFlavour%%% == \"Muons\"", "sc" : "sc_exclusiveTrack%%% == 1 && sc_trackBDT%%% > 0 && sc_exTrack_invMass%%% < 12 && sc_exclusiveTrackLeptonFlavour%%% == \"Muons\"" },
        
    ]
    injectJetIsoToCuts(cuts, jetIsoStr)
    
    
    weightString = {
        'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * BranchingRatio",
    }
    
    calculatedLumi = {
        #Before nomult
        #'MET' : 35.712736198,
        #Afrer nomult
        'MET' : 35.73895434
    }
    
    turnOnOnlyUsedObsInTree = True
    usedObs = ["passesUniversalSelection", "BranchingRatio","Weight","passedMhtMet6pack","tEffhMetMhtRealXMht2016","puWeight","MinDeltaPhiMhtJets","BTagsDeepMedium","twoLeptons%%%","MHT","MET","leptonFlavour%%%","invMass%%%","vetoElectronsPassIso","vetoMuonsPassIso","isoCr%%%","sameSign%%%", "leptons%%%", "deltaR%%%", "trackBDT%%%", "exclusiveTrack%%%", "exTrack_invMass%%%", "exclusiveTrackLeptonFlavour%%%", "sc_exclusiveTrack%%%", "sc_trackBDT%%%", "sc_exTrack_invMass%%%", "sc_exclusiveTrackLeptonFlavour%%%", "exTrack_dilepBDT%%%", "sc_exTrack_dilepBDT%%%"]
    injectJetIsoToList(usedObs, jetIsoStr)
    
    
    plot_sc = True
    plot_data = True
    plot_signal = False
    plot_overflow = True
    plot_ratio = True
    
    blind_data = True

    save_histrograms_to_file = True
    load_histrograms_from_file = False
    

    sig_line_width = 3
    plot_error = True
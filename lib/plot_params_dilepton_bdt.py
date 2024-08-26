import sys
import os

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib"))

from plot_params_base import *
import analysis_selections

class dilepton_bdt_inputs_muons(BaseParams):
    
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_bdt_inputs_muons.root"
    
    save_histrograms_to_file = True
    load_histrograms_from_file = False 
    
    show_lumi = False
    use_calculated_lumi_weight = False
    use_bdt_file_as_input = True
    
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/cut_optimisation/tmva/dilepton_bdt_phase1/recoMuonsCorrJetNoMultIso10Dr0.6/recoMuonsCorrJetNoMultIso10Dr0.6.root"
    
    plot_signal = False
    no_weights = True
    nostack = True
    y_title = "Events"
    y_title_offset = 1.2
    legend_columns = 1
    legend_coordinates = {"x1" : .6, "y1" : .60, "x2" : .95, "y2" : .89}
    
    plot_overflow = True
    
    colorPalette = plotutils.bdtColors
    
    label_text = plotutils.StampStr.SIM
    
    cuts = [
        {"name":"none", "title": "None", "condition" : "1" },
    ]
    
    histograms_defs = [
        {"obs" : "invMass%%%", "units" : "M_{ll} [GeV]", "bins" : 50, "minX" : 0, "maxX" : 50, "linearYspace" : 1.2 },
        {"obs" : "deltaPhi%%%", "units" : "#Delta_{}\phi(ll)", "bins" : 50, "minX" : 0, "maxX" : 3.2 },
        {"obs" : "deltaR%%%", "units" : "#Delta_{}R(ll)", "bins" : 50, "minX" : 0, "maxX" : 6.3 },
        {"obs" : "deltaEta%%%", "units" : "|#Delta_{}\eta(ll)|", "bins" : 50, "minX" : 0, "maxX" : 5 },
        {"obs" : "NJets", "units" : "Number of jets", "bins" : 6, "minX" : 0, "maxX" : 6 },
        {"obs" : "MinDeltaPhiMhtJets", "units" : "min #Delta_{}\phi(H_{T}^{Miss},jets)", "bins" : 50, "minX" : 0, "maxX" : 3.2 },
        {"obs" : "HT", "units" : "HT [GeV]", "bins" : 50, "minX" : 0, "maxX" : 1000 },
        {"obs" : "MHT", "units" : "H_{T}^{Miss} [GeV]", "bins" : 50, "minX" : 100, "maxX" : 1000 },
        {"obs" : "LeadingJetPt", "units" : "p_{T}(leading jet) [GeV]", "bins" : 50, "minX" : 30, "maxX" : 1000 },
        {"obs" : "LeadingJet.Eta__", "units" : "\eta(leading jet)", "bins" : 50, "minX" : -2.5, "maxX" : 2.5, "linearYspace" : 1.6 },
        {"obs" : "dileptonPt%%%", "units" : "p_{T}(l_{1}+l_{2}) [GeV]", "bins" : 50, "minX" : 0, "maxX" : 30 },
        {"obs" : "mth1%%%", "units" : "m_{T}(l_{1}) [GeV]", "bins" : 50, "minX" : 0, "maxX" : 140 },
        {"obs" : "leptons%%%_0_.Pt__", "units" : "p_{T}(l_{1}) [GeV]", "bins" : 50, "minX" : 2, "maxX" : 15 },
        {"obs" : "leptons%%%_1_.Pt__", "units" : "p_{T}(l_{2}) [GeV]", "bins" : 50, "minX" : 2, "maxX" : 15 },
        {"obs" : "leptons%%%_0_.Eta__", "units" : "\eta(l_{1})", "bins" : 50, "minX" : -2.5, "maxX" : 2.5, "linearYspace" : 1.6 },
        {"obs" : "deltaPhiMhtLepton1%%%", "units" : "|#Delta_{}\phi(l_{1},H_{T}^{Miss})|", "bins" : 50, "minX" : 0, "maxX" : 3.2 },
        {"obs" : "deltaPhiMhtLepton2%%%", "units" : "|#Delta_{}\phi(l_{2},H_{T}^{Miss})|", "bins" : 50, "minX" : 0, "maxX" : 3.2 },
        {"obs" : "nmtautau%%%", "units" : "m_{#tau#tau} [GeV]", "bins" : 50, "minX" : 0, "maxX" : 200 },
    ]
    
    injectJetIsoToHistograms(histograms_defs, analysis_selections.jetIsos["Muons"])
    
    bg_retag = True
    
    bgReTagging = {
        "background" : "classID == 1",
        "signal" : "classID == 0",
    }
    
    bgReTaggingOrder = {
        "background"  : 1,
        "signal" : 2
    }
    bgReTaggingNames = {
        "background" : "Background",
        "signal" : "Signal"
    }

class extrack_bdt_inputs_muons(dilepton_bdt_inputs_muons):
    histrograms_file = BaseParams.histograms_root_files_dir + "/extrack_bdt_inputs_muons.root"
    
    save_histrograms_to_file = True
    load_histrograms_from_file = False 
    
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/cut_optimisation/tmva/dilepton_bdt_phase1/exTrackMuonsCorrJetNoMultIso10Dr0.6/exTrackMuonsCorrJetNoMultIso10Dr0.6.root"
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/cut_optimisation/tmva/dilepton_bdt/exTrackMuonsCorrJetNoMultIso10Dr0.6/exTrackMuonsCorrJetNoMultIso10Dr0.6.root"
    
    histograms_defs = [
        {"obs" : "exTrack_invMass%%%", "units" : "M_{ll} [GeV]", "bins" : 50, "minX" : 0, "maxX" : 15, "linearYspace" : 1.2 },
        {"obs" : "exTrack_deltaPhi%%%", "units" : "#Delta_{}\phi(ll)", "bins" : 50, "minX" : 0, "maxX" : 3.2 },
        {"obs" : "exTrack_deltaEta%%%", "units" : "|#Delta_{}\eta(ll)|", "bins" : 50, "minX" : 0, "maxX" : 5 },
        {"obs" : "exTrack_deltaR%%%", "units" : "#Delta_{}R(ll)", "bins" : 50, "minX" : 0, "maxX" : 6.3 },
        {"obs" : "NJets", "units" : "Number of jets", "bins" : 6, "minX" : 0, "maxX" : 6 },
        {"obs" : "MinDeltaPhiMhtJets", "units" : "min #Delta_{}\phi(H_{T}^{Miss},jets)", "bins" : 50, "minX" : 0, "maxX" : 3.2 },
        {"obs" : "HT", "units" : "HT [GeV]", "bins" : 50, "minX" : 0, "maxX" : 1000 },
        {"obs" : "MHT", "units" : "H_{T}^{Miss} [GeV]", "bins" : 50, "minX" : 100, "maxX" : 1000 },
        {"obs" : "LeadingJetPt", "units" : "p_{T}(leading jet) [GeV]", "bins" : 50, "minX" : 30, "maxX" : 1000 },
        {"obs" : "LeadingJet.Eta__", "units" : "\eta(leading jet)", "bins" : 50, "minX" : -2.5, "maxX" : 2.5, "linearYspace" : 1.6 },
        {"obs" : "mtl%%%", "units" : "m_{T}(l) [GeV]", "bins" : 50, "minX" : 0, "maxX" : 140 },
        {"obs" : "lepton%%%.Pt__", "units" : "p_{T}(l) [GeV]", "bins" : 50, "minX" : 2, "maxX" : 15 },
        {"obs" : "lepton%%%.Eta__", "units" : "\eta(l)", "bins" : 50, "minX" : -2.5, "maxX" : 2.5, "linearYspace" : 1.6 },
        {"obs" : "track%%%.Pt__ ", "units" : "p_{T}(t) [GeV]", "bins" : 50, "minX" : 2, "maxX" : 15 },
        {"obs" : "track%%%.Eta__", "units" : "\eta(t)", "bins" : 50, "minX" : -2.5, "maxX" : 2.5, "linearYspace" : 1.6 },
        {"obs" : "lepton%%%.Phi__", "units" : "\phi(l)", "bins" : 50, "minX" : -3.2, "maxX" : 3.2, "linearYspace" : 1.6 },
        {"obs" : "track%%%.Phi__", "units" : "\phi(t)", "bins" : 50, "minX" : -3.2, "maxX" : 3.2, "linearYspace" : 1.6 },
        {"obs" : "trackBDT%%%", "units" : "track BDT", "bins" : 50, "minX" : 0, "maxX" : 1 },
    ]
    #plot_error = True
    injectJetIsoToHistograms(histograms_defs, analysis_selections.jetIsos["Muons"])
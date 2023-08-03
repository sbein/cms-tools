import sys
import os
from ROOT import *

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib"))

import utils

from plot_params_base import *
# 
# signals = [
#               "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/sum/higgsino_mu100_dm0p86Chi20Chipm.root",
#               "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/sum/higgsino_mu100_dm1p92Chi20Chipm.root",
#               "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/sum/higgsino_mu100_dm3p28Chi20Chipm.root",
#               "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/sum/higgsino_mu100_dm9p73Chi20Chipm.root"
#               ]

signals = [
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/sum/higgsino_mu100_dm0p86Chi20Chipm*.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/sum/higgsino_mu100_dm1p13Chi20Chipm*.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/sum/higgsino_mu100_dm1p92Chi20Chipm*.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/sum/higgsino_mu100_dm3p28Chi20Chipm*.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/sum/higgsino_mu100_dm4p30Chi20Chipm*.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/sum/higgsino_mu100_dm5p63Chi20Chipm*.root"
              
              ]


# signalNames = [
#     "\Delta_{}m 0.8 GeV",
#     "\Delta_{}m 1.9 GeV",
#     "\Delta_{}m 3.2 GeV",
#     "\Delta_{}m 9.7 GeV",
# ]

signalNames = [
    "\Delta_{}m 0.8 GeV",
    "\Delta_{}m 1.1 GeV",
    "\Delta_{}m 1.9 GeV",
    "\Delta_{}m 3.2 GeV",
    "\Delta_{}m 4.3 GeV",
    "\Delta_{}m 5.6 GeV",
]
    
class lepton_selection_dm1p92(BaseParams):
    histrograms_file = BaseParams.histograms_root_files_dir + "/lepton_selection_mu100_dm1p92Chi20Chipm.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = False
    signal_dir = [
              #"/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/sum/higgsino_mu100_dm0p86Chi20Chipm.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_nlp/sum/higgsino_mu100_dm1p92Chi20Chipm_*.root",
              #"/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_nlp/sum/higgsino_mu100_dm3p28Chi20Chipm.root",
              #"/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/sum/higgsino_mu100_dm9p73Chi20Chipm.root"
              ]
    
    plot_bg = False
    plot_data = False
    plot_overflow = True
    object_retag = True
    glob_signal = True
    
    sig_line_width = 1

    legend_coordinates = {"x1" : .65, "y1" : .60, "x2" : .98, "y2" : .95}
    legend_columns = 1
    legend_border = 0
    signal_legend_string = 'lF'
    
    label_text = plotutils.StampStr.SIM
    
    cuts = [
        {"name":"none", "title": "No Cuts", "condition" : "1", "object" : {"e" : "Electrons.Pt() < 20", "m" : "Muons.Pt() < 20"  }},
        #{"name":"rlj", "title": "rlj", "condition" : "1", "object" : {"e" : "Electrons_deltaRLJ > 0.4 && Electrons.Pt() < 20", "m" : "Muons_deltaRLJ > 0.4"  }},
        #{"name":"pt", "title": "Pt", "condition" : "1", "object" : {"e" : "Electrons.Pt() < 20", "m" : "Muons.Pt() > 2 && Muons.Pt() < 20"  }},
        #{"name":"no_iso", "title": "no_iso", "condition": "1", "object" : {"e" : "Electrons_deltaRLJ > 0.4 && Electrons.Pt() < 20", "m" : "Muons.Pt() < 20 && Muons.Pt() > 2 && Muons_deltaRLJ > 0.4 && Muons_mediumID == 1 "  }},
    ]
    
    # histograms_defs = [
#         { "obs" : "Electrons_rlj", "formula" : "Electrons_deltaRLJ", "units" : "\Delta_{}R(j_{1}, e)", "bins" : 50, "minX" : 0, "maxX" : 5, "object" : "e", "y_title" : "Number of electrons" },
#         { "obs" : "Muons_pt", "formula" : "abs(Muons.Pt())", "units" : "Muon p_{T} [GeV]", "minX" : 0, "maxX" : 5, "bins" : 60, "object" : "m", "condition" : "1", "y_title_offset" : 1.2, "y_title" : "Number of muons" },
#         { "obs" : "Muons_rlj", "formula" : "Muons_deltaRLJ", "units" : "\Delta_{}R(j_{1}, \mu)", "minX" : 0, "maxX" : 5, "bins" : 60, "object" : "m", "condition" : "1", "y_title" : "Number of muons", "linearYspace" : 1.4 },
#         
#     ]
    
    
    histograms_defs = [
        
        

        {"obs" : "Electrons_rlj", "formula" : "Electrons_deltaRLJ", "units" : "\Delta_{}R(j_{1}, e)", "bins" : 50, "minX" : 0, "maxX" : 5, "object" : "e", "y_title" : "Number of electrons" },
        {"obs" : "Electrons_pt", "formula" : "abs(Electrons.Pt())", "units" : "Electron p_{T} [GeV]", "bins" : 60, "minX" : 5, "maxX" : 20, "object" : "e", "y_title" : "Number of electrons", "condition" : "Electrons_deltaRLJ > 0.4", "linearYspace" : 1.2 },
        {"obs" : "Electrons_eta", "formula" : "abs(Electrons.Eta())", "units" : "|\eta|_{e}", "bins" : 50, "minX" : 0, "maxX" : 2.5, "object" : "e", "y_title" : "Number of electrons", "condition" : "Electrons_deltaRLJ > 0.4 && Electrons.Pt() < 15", "linearYspace" : 1.2 },
        
        #{"obs" : "Electrons_eta_high", "formula" : "abs(Electrons.Eta())", "units" : "|\eta|_{e}", "bins" : 50, "minX" : 2, "maxX" : 3, "object" : "e", "y_title" : "Number of electrons", "condition" : "abs(Electrons.Eta())>2", "linearYspace" : 1.2 },
        #{"obs" : "Muons_eta_high", "formula" : "abs(Muons.Eta())", "units" : "|\eta|_{\mu}", "bins" : 50, "minX" : 2, "maxX" : 3, "object" : "m", "y_title" : "Number of electrons", "condition" : "abs(Muons.Eta())>2", "linearYspace" : 1.2 },
        
        { "obs" : "Electrons_medium", "formula" : "Electrons_mediumID", "units" : "Electron mediumID", "minX" : 0, "maxX" : 2, "bins" : 2, "object" : "e", "condition" : "Electrons.Pt() < 15 && Electrons_deltaRLJ > 0.4",  "y_title" : "Number of electrons", "Ndivisions" : 2, "binLabels" : ["fail", "pass"], "linearYspace" : 1.4, "y_title_offset" : 1.2 },
        { "obs" : "Electrons_tight", "formula" : "Electrons_tightID", "units" : "Electron tightID", "minX" : 0, "maxX" : 2, "bins" : 2, "object" : "e", "condition" : "Electrons.Pt() < 15 && Electrons_deltaRLJ > 0.4",  "y_title" : "Number of electrons", "Ndivisions" : 2, "binLabels" : ["fail", "pass"], "linearYspace" : 1.2, "y_title_offset" : 1.2 },
        { "obs" : "Electrons_iso", "formula" : "Electrons_passIso", "units" : "Electron isolation", "minX" : 0, "maxX" : 2, "bins" : 2, "object" : "e", "condition" : "Electrons.Pt() < 15 && Electrons_deltaRLJ > 0.4", "y_title" : "Number of electrons", "Ndivisions" : 2, "binLabels" : ["fail", "pass"], "linearYspace" : 1.7, "y_title_offset" : 1.2 },
        { "obs" : "Electrons_CorrJetNoMultIso11Dr0.5", "formula" : "Electrons_passCorrJetNoMultIso11Dr0.5", "units" : "Electron jet-isolation", "minX" : 0, "maxX" : 2, "bins" : 2, "object" : "e", "condition" : "Electrons.Pt() < 15 && Electrons_deltaRLJ > 0.4", "y_title" : "Number of electrons", "Ndivisions" : 2, "binLabels" : ["fail", "pass"], "linearYspace" : 1.7, "y_title_offset" : 1.2 },
        
        
        {"obs" : "Electrons_eta_jet_iso", "formula" : "abs(Electrons.Eta())", "units" : "|\eta|_{e}", "bins" : 50, "minX" : 0, "maxX" : 2.5, "object" : "e", "y_title" : "Number of electrons", "condition" : "Electrons_deltaRLJ > 0.4 && Electrons.Pt() < 15 && Electrons_passCorrJetNoMultIso11Dr0.5  == 1" },
        
        { "obs" : "Muons_Eta", "formula" : "abs(Muons.Eta())", "units" : "|\eta|_{\mu}", "minX" : 0, "maxX" : 2.4, "bins" : 60, "object" : "m", "condition" : "Muons_deltaRLJ > 0.4", "y_title" : "Number of muons", "linearYspace" : 1.8, "y_title_offset" : 1.2 },
        { "obs" : "Muons_Eta_after_pt", "formula" : "abs(Muons.Eta())", "units" : "|\eta|_{\mu}", "minX" : 0, "maxX" : 2.4, "bins" : 60, "object" : "m", "condition" : "Muons_deltaRLJ > 0.4 && Muons.Pt() > 2", "y_title" : "Number of muons", "linearYspace" : 1.8, "y_title_offset" : 1.2 },
        { "obs" : "Muons_Eta_all", "formula" : "abs(Muons.Eta())", "units" : "|\eta|_{\mu}", "minX" : 0, "maxX" : 2.4, "bins" : 60, "object" : "m", "condition" : "Muons_deltaRLJ > 0.4 && Muons.Pt() > 2 && Muons.Pt() < 15 && Muons_mediumID == 1", "y_title" : "Number of muons", "linearYspace" : 1.8, "y_title_offset" : 1.2 },
        
        { "obs" : "Muons_pt", "formula" : "abs(Muons.Pt())", "units" : "Muon p_{T} [GeV]", "minX" : 0, "maxX" : 20, "bins" : 60, "object" : "m", "condition" : "Muons_deltaRLJ > 0.4", "y_title" : "Number of muons", "y_title_offset" : 1.2, "linearYspace" : 1.3 },
        { "obs" : "Muons_pt_barrel", "formula" : "Muons.Pt()", "units" : "Barrel Muon p_{T} [GeV]", "minX" : 0, "maxX" : 20, "bins" : 60, "object" : "m", "condition" : "Muons_deltaRLJ > 0.4 && abs(Muons.Eta()) <= 1.2", "y_title" : "Number of muons", "y_title_offset" : 1.2, "linearYspace" : 1.3 },
        { "obs" : "Muons_pt_endcape", "formula" : "Muons.Pt()", "units" : "Endcaps Muon p_{T} [GeV]", "minX" : 0, "maxX" : 8, "bins" : 60, "object" : "m", "condition" : "Muons_deltaRLJ > 0.4 && abs(Muons.Eta()) >= 1.2 && abs(Muons.Eta()) <= 2.4", "y_title" : "Number of muons", "y_title_offset" : 1.2, "linearYspace" : 1.3 },
        
        { "obs" : "Muons_rlj", "formula" : "Muons_deltaRLJ", "units" : "\Delta_{}R(j_{1}, \mu)", "minX" : 0, "maxX" : 5, "bins" : 60, "object" : "m", "condition" : "1", "y_title" : "Number of muons", "linearYspace" : 1.5, "y_title_offset" : 1.2 },
        { "obs" : "Muons_rlj_barrel", "formula" : "Muons_deltaRLJ", "units" : "Barrel \Delta_{}R(j_{1}, \mu)", "minX" : 0, "maxX" : 5, "bins" : 60, "object" : "m", "condition" : "abs(Muons.Eta()) <= 1.2", "y_title" : "Number of muons", "y_title_offset" : 1.2 },
        { "obs" : "Muons_rlj_endcape", "formula" : "Muons_deltaRLJ", "units" : "Endcaps \Delta_{}R(j_{1}, \mu)", "minX" : 0, "maxX" : 5, "bins" : 60, "object" : "m", "condition" :  "abs(Muons.Eta()) >= 1.2 && abs(Muons.Eta()) <= 2.4", "y_title" : "Number of muons", "linearYspace" : 1.5, "y_title_offset" : 1.2 },
        
        { "obs" : "Muons_pt_medium", "formula" : "Muons_mediumID", "units" : "Muon mediumID", "minX" : 0, "maxX" : 2, "bins" : 2, "object" : "m", "condition" : "Muons_deltaRLJ > 0.4 && Muons.Pt() > 2 && Muons.Pt() < 15", "y_title" : "Number of muons", "Ndivisions" : 2, "binLabels" : ["fail", "pass"], "linearYspace" : 1.8, "y_title_offset" : 1.2 },
        { "obs" : "Muons_pt_barrel_medium", "formula" : "Muons_mediumID", "units" : "Barrel Muon mediumID", "minX" : 0, "maxX" : 2, "bins" : 2, "object" : "m", "condition" : "Muons_deltaRLJ > 0.4 && Muons.Pt() > 2 && Muons.Pt() < 15 && abs(Muons.Eta()) <= 1.2", "y_title" : "Number of muons", "Ndivisions" : 2, "binLabels" : ["fail", "pass"], "linearYspace" : 1.8, "y_title_offset" : 1.2 },
        { "obs" : "Muons_pt_endcape_medium", "formula" : "Muons_mediumID", "units" : "Endcaps Muon mediumID", "minX" : 0, "maxX" : 2, "bins" : 2, "object" : "m", "condition" : "Muons_deltaRLJ > 0.4 && Muons.Pt() > 2 && Muons.Pt() < 15 && abs(Muons.Eta()) >= 1.2 && abs(Muons.Eta()) <= 2.4", "y_title" : "Number of muons", "Ndivisions" : 2, "binLabels" : ["fail", "pass"], "linearYspace" : 1.8, "y_title_offset" : 1.2 },
        
        { "obs" : "Muons_pt_jet_iso", "formula" : "Muons_passCorrJetNoMultIso10Dr0.6", "units" : "Muon jet-isolation", "minX" : 0, "maxX" : 2, "bins" : 2, "object" : "m", "condition" : "Muons_deltaRLJ > 0.4 && Muons.Pt() > 2 && Muons.Pt() < 15 && Muons_mediumID == 1", "y_title" : "Number of muons", "Ndivisions" : 2, "binLabels" : ["fail", "pass"], "linearYspace" : 1.8, "y_title_offset" : 1.2 },
        { "obs" : "Muons_pt_barrel_jet_iso", "formula" : "Muons_passCorrJetNoMultIso10Dr0.6", "units" : "Barrel Muon jet-isolation", "minX" : 0, "maxX" : 2, "bins" : 2, "object" : "m", "condition" : "Muons_deltaRLJ > 0.4 && Muons.Pt() > 2 && Muons.Pt() < 15 && abs(Muons.Eta()) <= 1.2 && Muons_mediumID == 1", "y_title" : "Number of muons", "Ndivisions" : 2, "binLabels" : ["fail", "pass"], "linearYspace" : 1.8, "y_title_offset" : 1.2 },
        { "obs" : "Muons_pt_endcape_jet_iso", "formula" : "Muons_passCorrJetNoMultIso10Dr0.6", "units" : "Endcaps Muon jet-isolation", "minX" : 0, "maxX" : 2, "bins" : 2, "object" : "m", "condition" : "Muons_deltaRLJ > 0.4 && Muons.Pt() > 2 && Muons.Pt() < 15 && abs(Muons.Eta()) >= 1.2 && abs(Muons.Eta()) <= 2.4 && Muons_mediumID == 1", "y_title" : "Number of muons", "Ndivisions" : 2, "binLabels" : ["fail", "pass"], "linearYspace" : 1.8, "y_title_offset" : 1.2 },
        
        # { "obs" : "Muons_pt_jet_iso_loose", "formula" : "Muons_passCorrJetNoMultIso10Dr0.6", "units" : "Muon jet-isolation", "minX" : 0, "maxX" : 2, "bins" : 2, "object" : "m", "condition" : "Muons_deltaRLJ > 0.4 && Muons.Pt() > 2 && Muons.Pt() < 15", "y_title" : "Number of muons", "Ndivisions" : 2, "binLabels" : ["fail", "pass"], "linearYspace" : 1.8, "y_title_offset" : 1.2 },
#         { "obs" : "Muons_pt_barrel_jet_iso_loose", "formula" : "Muons_passCorrJetNoMultIso10Dr0.6", "units" : "Barrel Muon jet-isolation", "minX" : 0, "maxX" : 2, "bins" : 2, "object" : "m", "condition" : "Muons_deltaRLJ > 0.4 && Muons.Pt() > 2 && Muons.Pt() < 15 && abs(Muons.Eta()) <= 1.2", "y_title" : "Number of muons", "Ndivisions" : 2, "binLabels" : ["fail", "pass"], "linearYspace" : 1.8, "y_title_offset" : 1.2 },
#         { "obs" : "Muons_pt_endcape_jet_iso_loose", "formula" : "Muons_passCorrJetNoMultIso10Dr0.6", "units" : "Endcaps Muon jet-isolation", "minX" : 0, "maxX" : 2, "bins" : 2, "object" : "m", "condition" : "Muons_deltaRLJ > 0.4 && Muons.Pt() > 2 && Muons.Pt() < 15 && abs(Muons.Eta()) >= 1.2 && abs(Muons.Eta()) <= 2.4", "y_title" : "Number of muons", "Ndivisions" : 2, "binLabels" : ["fail", "pass"], "linearYspace" : 1.8, "y_title_offset" : 1.2 },
#         
        
        { "obs" : "Muons_tight", "formula" : "Muons_tightID", "units" : "Muon tightID", "minX" : 0, "maxX" : 2, "bins" : 2, "object" : "m", "condition" : "Muons_deltaRLJ > 0.4 && Muons.Pt() > 2 && Muons.Pt() < 15", "y_title" : "Number of muons", "Ndivisions" : 2, "binLabels" : ["fail", "pass"], "linearYspace" : 1.8, "y_title_offset" : 1.2 },
        { "obs" : "Muons_barrel_tight", "formula" : "Muons_tightID", "units" : "Barrel Muon tightID", "minX" : 0, "maxX" : 2, "bins" : 2, "object" : "m", "condition" : "Muons_deltaRLJ > 0.4 && Muons.Pt() > 2 && Muons.Pt() < 15 && abs(Muons.Eta()) <= 1.2", "y_title" : "Number of muons", "Ndivisions" : 2, "binLabels" : ["fail", "pass"], "linearYspace" : 1.8, "y_title_offset" : 1.2 },
        { "obs" : "Muons_endcape_tight", "formula" : "Muons_tightID", "units" : "Endcaps Muon tightID", "minX" : 0, "maxX" : 2, "bins" : 2, "object" : "m", "condition" : "Muons_deltaRLJ > 0.4 && Muons.Pt() > 2 && Muons.Pt() < 15 && abs(Muons.Eta()) >= 1.2 && abs(Muons.Eta()) <= 2.4", "y_title" : "Number of muons", "Ndivisions" : 2, "binLabels" : ["fail", "pass"], "linearYspace" : 1.8, "y_title_offset" : 1.2 },
        
    ]
    
    # lepConds = {
#         "e" : { "Zl" : "Electrons_matchGen == 1",
#                 "MM" : "Electrons_matchGen == 0"},
#         "m" : { "Zl" : "Muons_matchGen == 1",
#                 "MM" : "Muons_matchGen == 0"},
#     }

    object_retag_map = {
        "e" : [ 
                
                {"MM" : "Electrons_isZ == 0"},
                {"Zl" : "Electrons_isZ == 1"},
            ],
        "m" : [ 
                
                {"MM" : "Muons_isZ == 0"},
                {"Zl" : "Muons_isZ == 1"},
            ]
    }
    
    object_retag_labels = {
         "e" : {
            "Zl" : "#tilde{\chi}^{0}_{2} #rightarrow #tilde{\chi}^{0}_{1} ee",
            "MM" : "other"
            },

        "m" : {
            "Zl" : "#tilde{\chi}^{0}_{2} #rightarrow #tilde{\chi}^{0}_{1} \mu\mu",
            "MM" : "other"
            }
    }
    
    # weightString = {
#         'MET' : "1",
#         'SingleMuon' : "1"
#     }
#     
#     calculatedLumi = {
#         'MET' : 0.001,
#         'SingleMuon' : 0.001,
#     }
    
    use_calculated_lumi_weight = False
    no_weights = True
    show_lumi = False
    
    colorPalette = [
        { "name" : "yellow", "fillColor" : kYellow, "lineColor" : kYellow+1, "fillStyle" : 3444, "markerColor" : 5,  "markerStyle" : kOpenCircle},
        { "name" : "blue", "fillColor" : kBlue, "lineColor" : kBlue+2, "fillStyle" : 3444, "markerColor" : 38,  "markerStyle" : kOpenCross },
    ]

class lepton_selection_dm5p63(lepton_selection_dm1p92):
    histrograms_file = BaseParams.histograms_root_files_dir + "/lepton_selection_mu100_dm5p63Chi20Chipm.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = False
    signal_dir = [
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_nlp/sum/higgsino_mu100_dm5p63Chi20Chipm*.root",
              ]

# class lepton_selection_dm1p92_initial(lepton_selection_dm1p92):
#     histrograms_file = BaseParams.histograms_root_files_dir + "/lepton_selection_dm1p92_initial.root"
#     save_histrograms_to_file = True
#     load_histrograms_from_file = True
#     plot_overflow = False
#     cuts = [
#         {"name":"none", "title": "No Cuts", "condition" : "1", "object" : {"e" : "Electrons.Pt() < 20", "m" : "Muons.Pt() < 20"  }},
#         {"name":"rlj", "title": "rlj", "condition" : "1", "object" : {"e" : "Electrons_deltaRLJ > 0.4 && Electrons.Pt() < 20", "m" : "Muons_deltaRLJ > 0.4"  }},
#         {"name":"pt", "title": "pt", "condition" : "1", "object" : {"e" : "Electrons_deltaRLJ > 0.4 && Electrons.Pt() < 20", "m" : "Muons.Pt() >= 2"  }},
#     ]
#     
#     histograms_defs = [
#         {"obs" : "Electrons_rlj", "formula" : "Electrons_deltaRLJ", "units" : "\Delta_{}R(j_{1}, e)", "bins" : 50, "minX" : 0, "maxX" : 5, "object" : "e", "y_title" : "Number of electrons" },
#         { "obs" : "Muons_pt", "formula" : "abs(Muons.Pt())", "units" : "Muon p_{T} [GeV]", "minX" : 0, "maxX" : 5, "bins" : 60, "object" : "m", "condition" : "1", "y_title_offset" : 1.2, "y_title" : "Number of muons" },
#         { "obs" : "Muons_rlj", "formula" : "Muons_deltaRLJ", "units" : "\Delta_{}R(j_{1}, \mu)", "minX" : 0, "maxX" : 5, "bins" : 60, "object" : "m", "condition" : "1", "y_title" : "Number of muons", "linearYspace" : 1.4 },
#         
#     ]
#     
# class lepton_selection_dm5p63_initial(lepton_selection_dm1p92_initial): 
#     histrograms_file = BaseParams.histograms_root_files_dir + "/lepton_selection_dm5p63_initial.root"   
# 
#     signal_dir = [
#               "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_nlp/sum/higgsino_mu100_dm5p63Chi20Chipm*.root",
#               ]
# 
# class lepton_selection_dm1p13_initial(lepton_selection_dm1p92_initial): 
#     histrograms_file = BaseParams.histograms_root_files_dir + "/lepton_selection_dm1p13_initial.root"   
# 
#     signal_dir = [
#               "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_nlp/sum/higgsino_mu100_dm1p13Chi20Chipm*.root",
#               ]
              
class track_selection(lepton_selection_dm1p92):
    cuts = [
        {"name":"none", "title": "No Cuts", "condition" : "tracks.Pt() < 10"},
        {"name":"dxyz", "title": "dxyz", "condition" : "tracks.Pt() < 10 && tracks_dxyVtx < 0.02 && tracks_dzVtx < 0.02"},
        
    ]
    
    histograms_defs = [
        {"obs" : "tracks.Pt()", "bins" : 50, "minX" : 1.9, "maxX" : 10, "object" : "t" },
        #{"obs" : "Pt tracks_trackJetIso", "formula" : "tracks.Pt()", "bins" : 50, "minX" : 1.9, "maxX" : 10, "object" : "t", "condition" :  "tracks_CorrJetNoMultIso10Dr0.6 == 1" },
        {"obs" : "abs(tracks.Eta())", "bins" : 50, "minX" : 0, "maxX" : 3, "object" : "t" },
        #{"obs" : "Pt tracks_trackJetIso", "formula" : "tracks.Pt()", "bins" : 50, "minX" : 1.9, "maxX" : 20, "object" : "t", "condition" :  "tracks_passCorrJetIso5 == 1" },
        
        # {"obs" : "tracks_matchedCaloEnergy", "bins" : 50, "minX" : 0, "maxX" : 50, "object" : "t" },
#         {"obs" : "tracks_nMissingOuterHits", "bins" : 13, "minX" : 0, "maxX" : 13, "object" : "t" },
#         {"obs" : "tracks_nMissingMiddleHits", "bins" : 3, "minX" : 0, "maxX" : 3, "object" : "t" },
#         {"obs" : "tracks_chi2perNdof", "bins" : 50, "minX" : 0, "maxX" : 20, "object" : "t" },
#         {"obs" : "tracks_trackerLayersWithMeasurement", "bins" : 19, "minX" : 0, "maxX" : 19, "object" : "t" },
#         {"obs" : "tracks_trackQualityGoodIterative", "bins" : 2, "minX" : 0, "maxX" : 2, "object" : "t" },
#         {"obs" : "tracks_trkRelIso", "bins" : 50, "minX" : 0, "maxX" : 0.2, "object" : "t" },
#         {"obs" : "tracks_trkMiniRelIso", "bins" : 50, "minX" : 0, "maxX" : 0.0002, "object" : "t" },
#         {"obs" : "tracks_nValidPixelHits", "bins" : 8, "minX" : 0, "maxX" : 8, "object" : "t" },
#         {"obs" : "tracks_nValidTrackerHits", "bins" : 40, "minX" : 0, "maxX" : 40, "object" : "t" },
#         {"obs" : "tracks_trackJetIso", "bins" : 50, "minX" : 0, "maxX" : 2, "object" : "t" },
#         {"obs" : "tracks_passPFCandVeto", "bins" : 2, "minX" : 0, "maxX" : 2, "object" : "t" },
#         {"obs" : "tracks_dxyVtx", "bins" : 50, "minX" : 0, "maxX" : 0.1, "object" : "t" },
#         {"obs" : "tracks_dzVtx", "bins" : 50, "minX" : 0, "maxX" : 0.1, "object" : "t" },
#         {"obs" : "tracks_pixelLayersWithMeasurement", "bins" : 5, "minX" : 0, "maxX" : 5, "object" : "t" },
#         {"obs" : "tracks_minDrLepton", "bins" : 50, "minX" : 0, "maxX" : 10, "object" : "t" },
#         {"obs" : "tracks_deltaRLJ", "bins" : 50, "minX" : 0, "maxX" : 5, "object" : "t" },
#         {"obs" : "tracks_correctedMinDeltaRJets", "bins" : 50, "minX" : 0, "maxX" : 1, "object" : "t" },
#         {"obs" : "tracks_minDeltaRJets", "bins" : 50, "minX" : 0, "maxX" : 1, "object" : "t" },
#         {"obs" : "tracks_deltaEtaLJ", "bins" : 50, "minX" : 0, "maxX" : 1, "object" : "t" },
#         {"obs" : "tracks_matchedCaloEnergyJets", "bins" : 50, "minX" : 0, "maxX" : 3, "object" : "t" },
#         {"obs" : "tracks_nMissingOuterHits", "bins" : 14, "minX" : 0, "maxX" : 14, "object" : "t" },
#         {"obs" : "tracks_matchedCaloEnergy", "bins" : 50, "minX" : 0, "maxX" : 100, "object" : "t" },
        
    ]
    
    object_retag_map = {
        "t" : [ 
                {"MM" : "tracks_isZ == 0"},
                {"exZl" : "tracks_isZ == 1 && tracks_mi == -1 && tracks_ei == -1"},
                {"Zl" : "tracks_isZ == 1 && (tracks_mi != -1 || tracks_ei != -1)"},
                ],
        "m" : [ {"MM" : "Muons_isZ == 0"},
                {"Zl" : "Muons_isZ == 1"}],
    }
    
    legend_coordinates = {"x1" : .20, "y1" : .60, "x2" : .89, "y2" : .89}
    legend_columns = 2
    legend_border = 0

class jet_isolation_study(BaseParams):
    
    save_histrograms_to_file = True
    load_histrograms_from_file = True    
    
    histrograms_file = "/afs/desy.de/user/n/nissanuv/CMSSW_10_1_0/src/cms-tools/analysis/scripts/jetIsolationStudyHists.root"
    
    
    signal_dir = [
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/sum/higgsino_mu100_dm0p86Chi20Chipm.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/sum/higgsino_mu100_dm1p92Chi20Chipm.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/sum/higgsino_mu100_dm3p28Chi20Chipm.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/sum/higgsino_mu100_dm5p63Chi20Chipm.root"
              ]
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/type_sum"
    
    plot_bg = True
    plot_data = False
    plot_overflow = True
    object_retag = False
    
    #sig_line_width = 1

    #legend_coordinates = {"x1" : .75, "y1" : .75, "x2" : .89, "y2" : .89}
    #legend_columns = 1
    #legend_border = 1
    
    cuts = [
        {"name":"none", "title": "No Cuts", "condition" : "(MHT >= 220 &&  MET >= 200 && BTagsDeepMedium == 0)", "object" : {"e" : "1", "m" : "1"  }},
        #{"name":"no_iso", "title": "no_iso", "condition": "1", "object" : {"e" : "Electrons_deltaRLJ > 0.4 && Electrons.Pt() < 20", "m" : "Muons.Pt() < 20 && Muons.Pt() > 2 && Muons_deltaRLJ > 0.4 && Muons_mediumID == 1 "  }},
    ]

    
    histograms_defs_base = [
        { "obs" : "Muons_pt", "formula" : "abs(Muons.Pt())", "units" : "\mu p_{T}", "minX" : 2, "maxX" : 25, "bins" : 60, "object" : "m", "condition" : "Muons.Pt() >= 2" },
        { "obs" : "Muons_Eta", "formula" : "abs(Muons.Eta())", "units" : "|\eta|_{\mu}", "minX" : 0, "maxX" : 2.4, "bins" : 60, "object" : "m", "condition" : "Muons.Pt() >= 2 && abs(Muons.Pt()) >= 2" },
        { "obs" : "Muons_pt_barrel", "formula" : "Muons.Pt()", "units" : "barrel p_{T}", "minX" : 2, "maxX" : 20, "bins" : 60, "object" : "m", "condition" : "Muons.Pt() >= 2 && abs(Muons.Eta()) <= 0.9" },
        { "obs" : "Muons_pt_overlap", "formula" : "Muons.Pt()", "units" : "overlap p_{T}", "minX" : 2, "maxX" : 20, "bins" : 60, "object" : "m", "condition" : "Muons.Pt() >= 2 && abs(Muons.Eta()) > 0.9 && abs(Muons.Eta()) <= 1.2" },
        { "obs" : "Muons_pt_endcape", "formula" : "Muons.Pt()", "units" : "endcaps p_{T}", "minX" : 2, "maxX" : 20, "bins" : 60, "object" : "m", "condition" : "Muons.Pt() >= 2 && abs(Muons.Eta()) >= 1.2 && abs(Muons.Eta()) <= 2.4" },
        
        { "obs" : "Muons_rlj_barrel", "formula" : "Muons_deltaRLJ", "units" : "barrel \Delta_{}R(j_{1}, \mu)", "minX" : 0, "maxX" : 5, "bins" : 60, "object" : "m", "condition" : "Muons.Pt() >= 2 && abs(Muons.Eta()) <= 0.9" },
        { "obs" : "Muons_rlj_overlap", "formula" : "Muons_deltaRLJ", "units" : "overlap \Delta_{}R(j_{1}, \mu)", "minX" : 0, "maxX" : 5, "bins" : 60, "object" : "m", "condition" : "Muons.Pt() >= 2 && abs(Muons.Eta()) > 0.9 && abs(Muons.Eta()) <= 1.2" },
        { "obs" : "Muons_rlj_endcape", "formula" : "Muons_deltaRLJ", "units" : "endcaps \Delta_{}R(j_{1}, \mu)", "minX" : 0, "maxX" : 5, "bins" : 60, "object" : "m", "condition" : "Muons.Pt() >= 2 && abs(Muons.Eta()) >= 1.2 && abs(Muons.Eta()) <= 2.4" },
        
        { "obs" : "Muons_pt_barrel_medium", "formula" : "Muons_mediumID", "units" : "barrel mediumID", "minX" : 0, "maxX" : 2, "bins" : 2, "object" : "m", "condition" : "Muons.Pt() >= 2 && abs(Muons.Eta()) <= 0.9" },
        { "obs" : "Muons_pt_overlap_medium", "formula" : "Muons_mediumID", "units" : "overlap mediumID", "minX" : 0, "maxX" : 2, "bins" : 2, "object" : "m", "condition" : "Muons.Pt() >= 2 && abs(Muons.Eta()) > 0.9 && abs(Muons.Eta()) <= 1.2" },
        { "obs" : "Muons_pt_endcape_medium", "formula" : "Muons_mediumID", "units" : "endcaps mediumID", "minX" : 0, "maxX" : 2, "bins" : 2, "object" : "m", "condition" : "Muons.Pt() >= 2 && abs(Muons.Eta()) >= 1.2 && abs(Muons.Eta()) <= 2.4" },
        
        { "obs" : "Muons_pt_barrel_jet_iso", "formula" : "Muons_passCorrJetNoMultIso10Dr0.6", "units" : "barrel \mu CorrJetNoMultIso10Dr0.6", "minX" : 0, "maxX" : 2, "bins" : 2, "object" : "m", "condition" : "Muons.Pt() >= 2 && abs(Muons.Eta()) <= 0.9" },
        { "obs" : "Muons_pt_overlap_jet_iso", "formula" : "Muons_passCorrJetNoMultIso10Dr0.6", "units" : "overlap \mu CorrJetNoMultIso10Dr0.6", "minX" : 0, "maxX" : 2, "bins" : 2, "object" : "m", "condition" : "Muons.Pt() >= 2 && abs(Muons.Eta()) > 0.9 && abs(Muons.Eta()) <= 1.2" },
        { "obs" : "Muons_pt_endcape_jet_iso", "formula" : "Muons_passCorrJetNoMultIso10Dr0.6", "units" : "endcaps \mu CorrJetNoMultIso10Dr0.6", "minX" : 0, "maxX" : 2, "bins" : 2, "object" : "m", "condition" : "Muons.Pt() >= 2 && abs(Muons.Eta()) >= 1.2 && abs(Muons.Eta()) <= 2.4" },
        
        { "obs" : "Muons_pt_barrel_iso", "formula" : "Muons_passIso", "units" : "barrel \mu passIso", "minX" : 0, "maxX" : 2, "bins" : 2, "object" : "m", "condition" : "Muons.Pt() >= 2 && abs(Muons.Eta()) <= 0.9" },
        { "obs" : "Muons_pt_overlap_iso", "formula" : "Muons_passIso", "units" : "overlap \mu passIso", "minX" : 0, "maxX" : 2, "bins" : 2, "object" : "m", "condition" : "Muons.Pt() >= 2 && abs(Muons.Eta()) > 0.9 && abs(Muons.Eta()) <= 1.2" },
        { "obs" : "Muons_pt_endcape_iso", "formula" : "Muons_passIso", "units" : "endcaps \mu passIso", "minX" : 0, "maxX" : 2, "bins" : 2, "object" : "m", "condition" : "Muons.Pt() >= 2 && abs(Muons.Eta()) >= 1.2 && abs(Muons.Eta()) <= 2.4" },
        
    ]
    
    histograms_defs = []
    
    isoStrs = []
    isoConds = {}
    
    for CorrJetObs in utils.leptonIsolationList:
            ptRanges = [""]
            if CorrJetObs == "CorrJetIso":
                 ptRanges = utils.leptonCorrJetIsoPtRange
            for ptRange in ptRanges:
                #isoStr = "_pass" + CorrJetObs + str(ptRange)
                isoStr = CorrJetObs + str(ptRange)
                isoStrs.append(isoStr)
                isoConds[isoStr] = "twoLeptons" + isoStr + " == 1 && leptonFlavour" + isoStr + " == \"Muons\" && sameSign" + isoStr + " == 0 && @leptons" + isoStr + ".size() == 2"
    
    
    for isoStr in isoStrs:
        histograms_defs.append({ "obs" : "leptons" + isoStr + ".Pt()", "units" : "\mu " + isoStr +  " p_{T}", "minX" : 2, "maxX" : 20, "bins" : 60, "object" : "m", "condition" : isoConds[isoStr] })
    for isoStr in isoStrs:
        histograms_defs.append({ "obs" : "leptons" + isoStr +"_pt_gt_20", "formula" : "Muons.Pt()", "units" : "\mu " + isoStr +  " p_{T}", "minX" : 20, "maxX" : 50, "bins" : 60, "object" : "m", "condition" : isoConds[isoStr] + " && Muons.Pt() >= 20 && Muons_pass" + isoStr + " == 1" })
    for isoStr in isoStrs:
        histograms_defs.append({ "obs" : "invMass" + isoStr, "units" : "M_{ll} " + isoStr, "minX" : 0, "maxX" : 10, "bins" : 60, "object" : "m", "condition" : isoConds[isoStr] + " && invMass" + isoStr + " < 10"})
    for isoStr in isoStrs:
        histograms_defs.append({ "obs" : "dilepBDT" + isoStr, "units" : "dilepton BDT " + isoStr , "minX" : -1, "maxX" : 1, "bins" : 60, "object" : "m", "condition" : isoConds[isoStr] })
    for isoStr in isoStrs:
        histograms_defs.append({ "obs" : "vetoMuons" + isoStr, "minX" : 0, "maxX" : 2, "bins" : 2, "object" : "m", "condition" : isoConds[isoStr] })
    
    
    weightString = {
        'MET' : "passedMhtMet6pack * tEffhMetMhtRealXMht2016 * Weight",
    }
    
    calculatedLumi = {
        'MET' : utils.LUMINOSITY/1000.0,
        'SingleMuon' : 0.001,
    }
    
    #hist = utils.getHistogramFromTree(deltaM + "_2l_" + lep, c, "dilepBDT", 30, -0.6, 0.6, str(utils.LUMINOSITY) + "* passedMhtMet6pack * tEffhMetMhtRealXMht2016 * Weight * BranchingRatio * (twoLeptons == 1 && (leptons[1].Pt() <= 3.5 || deltaR <= 0.3) && MHT >= 220 &&  MET >= 200 && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && dilepBDT > 0.1 && BTagsDeepMedium == 0 && vetoElectronsTightID == 0 && vetoMuonsPassIso == 0 && @leptons.size() == 2 && leptonFlavour == \"" + lep + "\" && sameSign == 0)", True)
    #hist = utils.getHistogramFromTree(basename, c, "dilepBDT", 30, -0.6, 0.6, str(utils.LUMINOSITY) + "* passedMhtMet6pack * tEffhMetMhtRealXMht2016 * Weight * (twoLeptons == 1 && (leptons[1].Pt() <= 3.5 || deltaR <= 0.3) && MHT >= 220 &&  MET >= 200 && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && dilepBDT > 0.1 && BTagsDeepMedium == 0 && vetoElectronsTightID == 0 && vetoMuonsPassIso == 0 && @leptons.size() == 2 && leptonFlavour == \"" + lep + "\" && sameSign == 0)", True)

class jet_isolation_study_electrons(jet_isolation_study):
    
    histrograms_file = "/afs/desy.de/user/n/nissanuv/CMSSW_10_1_0/src/cms-tools/analysis/scripts/jetIsolationStudyElectronsHists.root"
    
    histograms_defs = []
    
    isoStrs = []
    isoConds = {}
    
    for CorrJetObs in utils.leptonIsolationList:
            ptRanges = [""]
            if CorrJetObs == "CorrJetIso":
                 ptRanges = utils.leptonCorrJetIsoPtRange
            for ptRange in ptRanges:
                #isoStr = "_pass" + CorrJetObs + str(ptRange)
                isoStr = CorrJetObs + str(ptRange)
                isoStrs.append(isoStr)
                isoConds[isoStr] = "twoLeptons" + isoStr + " == 1 && leptonFlavour" + isoStr + " == \"Electrons\" && sameSign" + isoStr + " == 0 && @leptons" + isoStr + ".size() == 2"
    
    
    for isoStr in isoStrs:
        histograms_defs.append({ "obs" : "leptons" + isoStr + ".Pt()", "units" : "e " + isoStr +  " p_{T}", "minX" : 2, "maxX" : 20, "bins" : 60, "object" : "e", "condition" : isoConds[isoStr] })
    for isoStr in isoStrs:
        histograms_defs.append({ "obs" : "leptons" + isoStr +"_pt_gt_20", "formula" : "Electrons.Pt()", "units" : "\mu " + isoStr +  " p_{T}", "minX" : 20, "maxX" : 50, "bins" : 60, "object" : "e", "condition" : isoConds[isoStr] + " && Electrons.Pt() >= 20 && Electrons_pass" + isoStr + " == 1" })
    for isoStr in isoStrs:
        histograms_defs.append({ "obs" : "invMass" + isoStr, "units" : "M_{ll} " + isoStr, "minX" : 0, "maxX" : 10, "bins" : 60, "object" : "e", "condition" : isoConds[isoStr] + " && invMass" + isoStr + " < 10"})
    for isoStr in isoStrs:
        histograms_defs.append({ "obs" : "invMass_orth" + isoStr, "formula" : "invMass" + isoStr, "units" : "M_{ll} orth " + isoStr, "minX" : 0, "maxX" : 10, "bins" : 60, "object" : "e", "condition" : isoConds[isoStr] + " && invMass" + isoStr + " < 10 && (leptons" + isoStr + "[1].Pt() <= 3.5 || deltaR" + isoStr + " <= 0.3) "})
    for isoStr in isoStrs:
        histograms_defs.append({ "obs" : "invMass_orth_dilep" + isoStr, "formula" : "invMass" + isoStr, "units" : "M_{ll} orth dilep" + isoStr, "minX" : 0, "maxX" : 10, "bins" : 60, "object" : "e", "condition" : isoConds[isoStr] + " && invMass" + isoStr + " < 10 && dilepBDT" + isoStr + " > 0 && (leptons" + isoStr + "[1].Pt() <= 3.5 || deltaR" + isoStr + " <= 0.3) "})
    for isoStr in isoStrs:
        histograms_defs.append({ "obs" : "dilepBDT" + isoStr, "units" : "dilepton BDT " + isoStr , "minX" : -1, "maxX" : 1, "bins" : 60, "object" : "e", "condition" : isoConds[isoStr] })
    for isoStr in isoStrs:
        histograms_defs.append({ "obs" : "dilepBDT_orth" + isoStr, "formula" : "dilepBDT" + isoStr, "units" : "dilepton BDT orth " + isoStr , "minX" : -1, "maxX" : 1, "bins" : 60, "object" : "e", "condition" : isoConds[isoStr] + " && (leptons" + isoStr + "[1].Pt() <= 3.5 || deltaR" + isoStr + " <= 0.3) "})
    for isoStr in isoStrs:
        histograms_defs.append({ "obs" : "vetoElectrons" + isoStr, "minX" : 0, "maxX" : 2, "bins" : 2, "object" : "e", "condition" : isoConds[isoStr] })
   

class track_selection_bg(track_selection):
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/type_sum"
    #bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/bla"
    signal_dir = [
              #"/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/sum/higgsino_mu100_dm0p86Chi20Chipm.root",
              #"/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/sum/higgsino_mu100_dm1p92Chi20Chipm.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/sum/higgsino_mu100_dm3p28Chi20Chipm.root",
              #"/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/sum/higgsino_mu100_dm9p73Chi20Chipm.root"
              ]
    weightString = {
        'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2016",
        'SingleMuon' : "1"
    }
    calculatedLumi = {
        'MET' : utils.LUMINOSITY/1000.0,
        'SingleMuon' : 0.001,
    }
    plot_bg = True
    plot_signal = True
    plot_data = False
    plot_overflow = True
    object_retag = False

signalsGen = [
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_nlp/sum/higgsino_mu100_dm0p86Chi20Chipm*.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_nlp/sum/higgsino_mu100_dm1p13Chi20Chipm*.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_nlp/sum/higgsino_mu100_dm1p92Chi20Chipm*.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_nlp/sum/higgsino_mu100_dm3p28Chi20Chipm*.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_nlp/sum/higgsino_mu100_dm4p30Chi20Chipm*.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_nlp/sum/higgsino_mu100_dm5p63Chi20Chipm*.root"
              
              ]

class count_signal_events(BaseParams):
    histrograms_file = BaseParams.histograms_root_files_dir + "/count_signal_events.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = True
    signal_dir = [signalsGen[1]]
    signal_names = [signalNames[1]]
    glob_signal = True
    cuts = [
        {"name":"none", "title": "No Cuts", "condition" : "genFlavour == \"Muons\""},
        #{"name":"twoLoptonsNoIso", "title": "twoLoptonsNoIso", "condition" : "genFlavour == \"Muons\" && twoLeptonsNoIso == 1 && leptonFlavourNoIso == \"Muons\""},
    ]
    histograms_defs = [
        #{ "obs" : "gen_delta_r_vs_pt_1", "formula" : "gen_deltaR:GenParticles[genLeptonsIdx[0]].Pt()", "units" : "p_{T}(\mu_{1}) [GeV]", "minX" : 0, "maxX" : 8, "minY" : 0, "maxY" : 8,  "bins" : 60, "binsY" : 60, "y_title" : "#Delta_{}R(\mu\mu)", "plotStr" : "colz", "2D" : True },
        #{ "obs" : "gen_delta_r_vs_pt_2", "formula" : "gen_deltaR:GenParticles[genLeptonsIdx[1]].Pt()", "units" : "p_{T}(\mu_{2}) [GeV]", "minX" : 0, "maxX" : 8, "minY" : 0, "maxY" : 8, "bins" : 60, "binsY" : 60, "y_title" : "#Delta_{}R(\mu\mu)", "plotStr" : "colz", "2D" : True },
        { "obs" : "base", "formula" : "gen_invMass", "units" : "p_{T}(\mu_{1}) [GeV]", "minX" : 0, "maxX" : 20, "bins" : 1 },
        { "obs" : "pt_cut", "formula" : "gen_invMass", "units" : "p_{T}(\mu_{1}) [GeV]", "minX" : 0, "maxX" : 20, "bins" : 1, "condition" : "GenParticles[genLeptonsIdx[0]].Pt() > 2 && GenParticles[genLeptonsIdx[1]].Pt() > 2" },
        { "obs" : "orth", "formula" : "gen_invMass", "units" : "p_{T}(\mu_{1}) [GeV]", "minX" : 0, "maxX" : 20, "bins" : 1, "condition" : "GenParticles[genLeptonsIdx[0]].Pt() > 2 && GenParticles[genLeptonsIdx[1]].Pt() > 2 && (GenParticles[genLeptonsIdx[1]].Pt() < 3.5 || gen_deltaR < 0.3)" },
        #{ "obs" : "gen_invmass_vs_pt_2", "formula" : "gen_invMass:GenParticles[genLeptonsIdx[1]].Pt()", "units" : "p_{T}(\mu_{2}) [GeV]", "minX" : 0, "maxX" : 8, "minY" : 0, "maxY" : 1.4, "bins" : 60, "binsY" : 60, "y_title" : "m_{\mu\mu} [GeV]", "plotStr" : "colz", "2D" : True },
    ]
    
    weightString = {
        'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * BranchingRatio",
        'SingleMuon' : "1"
    }
    
    plot_bg = False
    plot_data = False
    plot_overflow = True
    plot_legend = False
    show_lumi = True
    label_text = plotutils.StampStr.SIM
    
    padRightMargin = 0.1
    padLeftMargin = 0.1
    y_title_offset = 0.7

class count_signal_events_dm5(count_signal_events):
    histrograms_file = BaseParams.histograms_root_files_dir + "/count_signal_events_dm5.root"
    signal_dir = [signalsGen[5]]
    signal_names = [signalNames[5]]

class signal_muons_gen_delta_r_vs_pt(BaseParams):
    histrograms_file = BaseParams.histograms_root_files_dir + "/signal_muons_gen_delta_r_vs_pt.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = True
    signal_dir = [signalsGen[1]]
    signal_names = [signalNames[1]]
    glob_signal = True
    cuts = [
        {"name":"none", "title": "No Cuts", "condition" : "genFlavour == \"Muons\""},
        #{"name":"twoLoptonsNoIso", "title": "twoLoptonsNoIso", "condition" : "genFlavour == \"Muons\" && twoLeptonsNoIso == 1 && leptonFlavourNoIso == \"Muons\""},
    ]
    histograms_defs = [
        { "obs" : "gen_delta_r_vs_pt_1", "formula" : "gen_deltaR:GenParticles[genLeptonsIdx[0]].Pt()", "units" : "p_{T}(\mu_{1}) [GeV]", "minX" : 0, "maxX" : 8, "minY" : 0, "maxY" : 8,  "bins" : 60, "binsY" : 60, "y_title" : "#Delta_{}R(\mu\mu)", "plotStr" : "colz", "2D" : True },
        { "obs" : "gen_delta_r_vs_pt_2", "formula" : "gen_deltaR:GenParticles[genLeptonsIdx[1]].Pt()", "units" : "p_{T}(\mu_{2}) [GeV]", "minX" : 0, "maxX" : 8, "minY" : 0, "maxY" : 8, "bins" : 60, "binsY" : 60, "y_title" : "#Delta_{}R(\mu\mu)", "plotStr" : "colz", "2D" : True },
        { "obs" : "gen_invmass_vs_pt_1", "formula" : "gen_invMass:GenParticles[genLeptonsIdx[0]].Pt()", "units" : "p_{T}(\mu_{1}) [GeV]", "minX" : 0, "maxX" : 8, "minY" : 0, "maxY" : 1.4,  "bins" : 60, "binsY" : 60, "y_title" : "m_{\mu\mu} [GeV]", "plotStr" : "colz", "2D" : True },
        { "obs" : "gen_invmass_vs_pt_2", "formula" : "gen_invMass:GenParticles[genLeptonsIdx[1]].Pt()", "units" : "p_{T}(\mu_{2}) [GeV]", "minX" : 0, "maxX" : 8, "minY" : 0, "maxY" : 1.4, "bins" : 60, "binsY" : 60, "y_title" : "m_{\mu\mu} [GeV]", "plotStr" : "colz", "2D" : True },
    ]
    
    weightString = {
        'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * BranchingRatio",
        'SingleMuon' : "1"
    }
    
    plot_bg = False
    plot_data = False
    plot_overflow = True
    plot_legend = False
    show_lumi = True
    label_text = plotutils.StampStr.SIM
    
    padRightMargin = 0.1
    padLeftMargin = 0.1
    y_title_offset = 0.7
    

class signal_muons_gen_delta_r_vs_pt_dm5(signal_muons_gen_delta_r_vs_pt):
    histrograms_file = BaseParams.histograms_root_files_dir + "/signal_muons_gen_delta_r_vs_pt_dm5.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = True
    signal_dir = [signalsGen[5]]
    signal_names = [signalNames[5]]
    histograms_defs = [
        { "obs" : "gen_delta_r_vs_pt_1", "formula" : "gen_deltaR:GenParticles[genLeptonsIdx[0]].Pt()", "units" : "p_{T}(\mu_{1}) [GeV]", "minX" : 0, "maxX" : 25, "minY" : 0, "maxY" : 8,  "bins" : 60, "binsY" : 60, "y_title" : "#Delta_{}R(\mu\mu)", "plotStr" : "colz", "2D" : True },
        { "obs" : "gen_delta_r_vs_pt_2", "formula" : "gen_deltaR:GenParticles[genLeptonsIdx[1]].Pt()", "units" : "p_{T}(\mu_{2}) [GeV]", "minX" : 0, "maxX" : 25, "minY" : 0, "maxY" : 8, "bins" : 60, "binsY" : 60, "y_title" : "#Delta_{}R(\mu\mu)", "plotStr" : "colz", "2D" : True },
        { "obs" : "gen_invmass_vs_pt_1", "formula" : "gen_invMass:GenParticles[genLeptonsIdx[0]].Pt()", "units" : "p_{T}(\mu_{1}) [GeV]", "minX" : 0, "maxX" : 25, "minY" : 0, "maxY" : 6.5,  "bins" : 60, "binsY" : 60, "y_title" : "m_{\mu\mu} [GeV]", "plotStr" : "colz", "2D" : True },
        { "obs" : "gen_invmass_vs_pt_2", "formula" : "gen_invMass:GenParticles[genLeptonsIdx[1]].Pt()", "units" : "p_{T}(\mu_{2}) [GeV]", "minX" : 0, "maxX" : 25, "minY" : 0, "maxY" : 6.5, "bins" : 60, "binsY" : 60, "y_title" : "m_{\mu\mu} [GeV]", "plotStr" : "colz", "2D" : True },
    ]
    

class signal_muons(BaseParams):
    histrograms_file = BaseParams.histograms_root_files_dir + "/signal_muons.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = True
    signal_dir = signalsGen
    signal_names = signalNames
    glob_signal = True
    legend_text_size = 0.06
    legend_columns = 1
    legend_coordinates = {"x1" : .65, "y1" : .55, "x2" : .95, "y2" : .90}
    
    cuts = [
        {"name":"none", "title": "No Cuts", "condition" : "genFlavour == \"Muons\""},
        #{"name":"twoLoptonsNoIso", "title": "twoLoptonsNoIso", "condition" : "genFlavour == \"Muons\" && twoLeptonsNoIso == 1 && leptonFlavourNoIso == \"Muons\""},
    ]
    histograms_defs = [
        #{ "obs" : "Muons_pt_low", "formula" : "Muons.Pt()", "units" : "p_{T} [GeV]", "minX" : 0, "maxX" : 2, "bins" : 60, "condition" :  "Muons.Pt() <= 2 && Muons_isZ == 1", "legendCoor" : {"x1" : .60, "y1" : .60, "x2" : .89, "y2" : .89}, "legendCol" : 1, "linearYspace" : 1.2, "y_title" : "Number of muons" },
        { "obs" : "Muons_pt", "formula" : "Muons.Pt()", "units" : "p_{T} [GeV]", "minX" : 2, "maxX" : 25, "bins" : 60, "condition" :  "Muons.Pt() >= 2 && Muons_isZ == 1", "linearYspace" : 1.4, "y_title" : "Number of muons" },
        { "obs" : "Muons_Eta", "formula" : "abs(Muons.Eta())", "units" : "|\eta|", "minX" : 0, "maxX" : 2.4, "bins" : 60, "condition" :  "Muons.Pt() >= 2 && Muons_isZ == 1", "linearYspace" : 2, "y_title" : "Number of muons" },
        
        { "obs" : "deltaRNoIso", "units" : "#Delta_{}R(\mu\mu)", "minX" : 0, "maxX" : 6.3, "bins" : 60, "condition" :  "twoLeptonsNoIso == 1 && leptonFlavourNoIso == \"Muons\" && Muons_isZ[leptonsIdxNoIso[0]] == 1 &&  Muons_isZ[leptonsIdxNoIso[1]] == 1 ", "linearYspace" : 1.4 },
        { "obs" : "invMassNoIso", "units" : "m_{\mu\mu} [GeV]", "minX" : 0, "maxX" : 7, "bins" : 60, "condition" :  "twoLeptonsNoIso == 1 && leptonFlavourNoIso == \"Muons\" && Muons_isZ[leptonsIdxNoIso[0]] == 1 &&  Muons_isZ[leptonsIdxNoIso[1]] == 1 ", "linearYspace" : 1.9 },
        { "obs" : "deltaRNoIso_orth",  "formula" : "deltaRNoIso", "units" : "#Delta_{}R(\mu\mu)", "minX" : 0, "maxX" : 6.3, "bins" : 60, "condition" :  "twoLeptonsNoIso == 1 && leptonFlavourNoIso == \"Muons\" && Muons_isZ[leptonsIdxNoIso[0]] == 1 &&  Muons_isZ[leptonsIdxNoIso[1]] == 1 && (leptonsNoIso[1].Pt() <= 3.5 || deltaRNoIso <= 0.3)", "linearYspace" : 1.4 },
        { "obs" : "invMassNoIso_orth", "formula" : "invMassNoIso", "units" : "m_{\mu\mu} [GeV]", "minX" : 0, "maxX" : 7, "bins" : 60, "condition" :  "twoLeptonsNoIso == 1 && leptonFlavourNoIso == \"Muons\" && Muons_isZ[leptonsIdxNoIso[0]] == 1 &&  Muons_isZ[leptonsIdxNoIso[1]] == 1  && (leptonsNoIso[1].Pt() <= 3.5 || deltaRNoIso <= 0.3)", "linearYspace" : 1.5 },
        
        { "obs" : "deltaRCorrJetNoMultIso10Dr0.6", "units" : "#Delta_{}R(\mu\mu)", "minX" : 0, "maxX" : 6.3, "bins" : 60, "condition" :  "twoLeptonsCorrJetNoMultIso10Dr0.6 == 1 && leptonFlavourCorrJetNoMultIso10Dr0.6 == \"Muons\" && Muons_isZ[leptonsIdxCorrJetNoMultIso10Dr0.6[0]] == 1 &&  Muons_isZ[leptonsIdxCorrJetNoMultIso10Dr0.6[1]] == 1 ", "linearYspace" : 1.4 },
        { "obs" : "invMassCorrJetNoMultIso10Dr0.6", "units" : "m_{\mu\mu} [GeV]", "minX" : 0, "maxX" : 7, "bins" : 60, "condition" :  "twoLeptonsCorrJetNoMultIso10Dr0.6 == 1 && leptonFlavourCorrJetNoMultIso10Dr0.6 == \"Muons\" && Muons_isZ[leptonsIdxCorrJetNoMultIso10Dr0.6[0]] == 1 &&  Muons_isZ[leptonsIdxCorrJetNoMultIso10Dr0.6[1]] == 1 ", "linearYspace" : 1.9 },
        { "obs" : "deltaRCorrJetNoMultIso10Dr0.6_orth",  "formula" : "deltaRCorrJetNoMultIso10Dr0.6", "units" : "#Delta_{}R(\mu\mu)", "minX" : 0, "maxX" : 6.3, "bins" : 60, "condition" :  "twoLeptonsCorrJetNoMultIso10Dr0.6 == 1 && leptonFlavourCorrJetNoMultIso10Dr0.6 == \"Muons\" && Muons_isZ[leptonsIdxCorrJetNoMultIso10Dr0.6[0]] == 1 &&  Muons_isZ[leptonsIdxCorrJetNoMultIso10Dr0.6[1]] == 1 && (leptonsCorrJetNoMultIso10Dr0.6[1].Pt() <= 3.5 || deltaRCorrJetNoMultIso10Dr0.6 <= 0.3)", "linearYspace" : 1.4 },
        { "obs" : "invMassCorrJetNoMultIso10Dr0.6_orth", "formula" : "invMassCorrJetNoMultIso10Dr0.6", "units" : "m_{\mu\mu} [GeV]", "minX" : 0, "maxX" : 7, "bins" : 60, "condition" :  "twoLeptonsCorrJetNoMultIso10Dr0.6 == 1 && leptonFlavourCorrJetNoMultIso10Dr0.6 == \"Muons\" && Muons_isZ[leptonsIdxCorrJetNoMultIso10Dr0.6[0]] == 1 &&  Muons_isZ[leptonsIdxCorrJetNoMultIso10Dr0.6[1]] == 1  && (leptonsCorrJetNoMultIso10Dr0.6[1].Pt() <= 3.5 || deltaRCorrJetNoMultIso10Dr0.6 <= 0.3)", "linearYspace" : 1.5 },
        
        
        { "obs" : "Muons_m1_pt", "formula" : "leptonsCorrJetNoMultIso10Dr0.6[0].Pt()", "units" : "p_{T}(\mu_{1}) [GeV]", "minX" : 2, "maxX" : 20, "bins" : 60, "condition" :  "twoLeptonsCorrJetNoMultIso10Dr0.6 == 1 && leptonFlavourCorrJetNoMultIso10Dr0.6 == \"Muons\" && leptonsCorrJetNoMultIso10Dr0.6[0].Pt() < 25 && leptonsCorrJetNoMultIso10Dr0.6[0].Pt() > 2", "y_title" : "Number of muons", "linearYspace" : 1.4 },
        { "obs" : "Muons_m2_pt", "formula" : "leptonsCorrJetNoMultIso10Dr0.6[1].Pt()", "units" : "p_{T}(\mu_{2}) [GeV]", "minX" : 2, "maxX" : 20, "bins" : 60, "condition" :  "twoLeptonsCorrJetNoMultIso10Dr0.6 == 1 && leptonFlavourCorrJetNoMultIso10Dr0.6 == \"Muons\" && leptonsCorrJetNoMultIso10Dr0.6[1].Pt() < 25 && leptonsCorrJetNoMultIso10Dr0.6[1].Pt() > 2", "y_title" : "Number of muons", "linearYspace" : 1.4 },
        { "obs" : "Muons_m1_eta", "formula" : "abs(leptonsCorrJetNoMultIso10Dr0.6[0].Eta())", "units" : "|\eta|(\mu_{1})", "minX" : 0, "maxX" : 4, "bins" : 60, "condition" :  "twoLeptonsCorrJetNoMultIso10Dr0.6 == 1 && leptonFlavourCorrJetNoMultIso10Dr0.6 == \"Muons\" && leptonsCorrJetNoMultIso10Dr0.6[0].Pt() < 25 && leptonsCorrJetNoMultIso10Dr0.6[0].Pt() > 2", "linearYspace" : 1.4, "y_title" : "Number of muons" },
        { "obs" : "Muons_m2_eta", "formula" : "abs(leptonsCorrJetNoMultIso10Dr0.6[1].Eta())", "units" : "|\eta|(\mu_{2})", "minX" : 0, "maxX" : 4, "bins" : 60, "condition" :  "twoLeptonsCorrJetNoMultIso10Dr0.6 == 1 && leptonFlavourCorrJetNoMultIso10Dr0.6 == \"Muons\" && leptonsCorrJetNoMultIso10Dr0.6[1].Pt() < 25 && leptonsCorrJetNoMultIso10Dr0.6[1].Pt() > 2", "linearYspace" : 1.4, "y_title" : "Number of muons" },
        
        
        { "obs" : "Muons_pt_barrel", "formula" : "Muons.Pt()", "units" : "Barrel p_{T} [GeV]", "minX" : 2, "maxX" : 20, "bins" : 60, "condition" :  "Muons.Pt() >= 2 && Muons_isZ == 1 && abs(Muons.Eta()) < 1.2", "linearYspace" : 1.4, "y_title" : "Number of muons" },
        { "obs" : "Muons_pt_endcape", "formula" : "Muons.Pt()", "units" : "Endcaps p_{T} [GeV]", "minX" : 2, "maxX" : 20, "bins" : 60, "condition" :  "Muons.Pt() >= 2 && Muons_isZ == 1 && abs(Muons.Eta()) >= 1.2 && abs(Muons.Eta()) <= 2.4", "linearYspace" : 1.4, "y_title" : "Number of muons"},
    ]
    
    weightString = {
       'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * BranchingRatio",
       'SingleMuon' : "1"
    }
    
    plot_bg = False
    plot_data = False
    plot_overflow = True
    show_lumi = True
    label_text = plotutils.StampStr.SIM
    
    calculatedLumi = {
        'MET' : analysis_selections.recommended_luminosities["run2"],
    }

class signal_muons_gen(BaseParams):
    histrograms_file = BaseParams.histograms_root_files_dir + "/signal_muons_gen.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = True
    signal_dir = signalsGen
    signal_names = signalNames
    glob_signal = True
    plot_overflow = True
    legend_columns = 1
    legend_border = 0
    #legend_align = 32
    legend_text_size = 0.06
    legend_coordinates = {"x1" : .65, "y1" : .55, "x2" : .95, "y2" : .90}

    cuts = [
        {"name":"none", "title": "No Cuts", "condition" : "genFlavour == \"Muons\""},
    ]
    
    calculatedLumi = {
        'MET' : analysis_selections.recommended_luminosities["run2"],
    }
    
    histograms_defs = [
        #delta R, "condition" :  "GenParticles[genLeptonsIdx[0]].Pt() < 10 && GenParticles[genLeptonsIdx[1]].Pt() < 10"
        { "obs" : "Muons_pt", "formula" : "GenParticles.Pt()", "units" : "Gen p_{T} [GeV]", "minX" : 2, "maxX" : 25, "bins" : 60, "condition" :  "GenParticles.Pt() < 25 && GenParticles_Status == 1 && abs(GenParticles_PdgId) == 13 && GenParticles.Pt() > 2", "y_title" : "Number of muons" },
        { "obs" : "Muons_Eta", "formula" : "abs(GenParticles.Eta())", "units" : "Gen |\eta|", "minX" : 0, "maxX" : 4, "bins" : 60, "condition" :  "GenParticles.Pt() < 25 && GenParticles_Status == 1 && abs(GenParticles_PdgId) == 13 && GenParticles.Pt() > 2", "y_title" : "Number of muons", "linearYspace" : 1.4 },
        { "obs" : "gen_deltaR", "units" : "Gen #Delta_{}R(\mu\mu)", "minX" : 0, "maxX" : 6.3, "bins" : 60, "linearYspace" : 1.4  },
        { "obs" : "gen_deltaR_cut", "formula" : "gen_deltaR", "units" : "Gen #Delta_{}R(\mu\mu)", "minX" : 0, "maxX" : 6.3, "bins" : 60, "linearYspace" : 1.4, "condition" :  "GenParticles[genLeptonsIdx[0]].Pt() > 2 && GenParticles[genLeptonsIdx[1]].Pt() > 2" },
        { "obs" : "gen_deltaR_orth", "formula" : "gen_deltaR", "units" : "Gen #Delta_{}R(\mu\mu)", "minX" : 0, "maxX" : 6.3, "bins" : 60, "linearYspace" : 1.4, "condition" :  "GenParticles[genLeptonsIdx[0]].Pt() > 2 && GenParticles[genLeptonsIdx[1]].Pt() > 2 && (GenParticles[genLeptonsIdx[1]].Pt() < 3.5 || gen_deltaR < 0.3)" },
        { "obs" : "gen_invMass", "units" : "Gen m_{\mu\mu} [GeV]", "minX" : 0, "maxX" : 7, "bins" : 60, "linearYspace" : 1.4 },
        { "obs" : "gen_invMass_cut", "formula" : "gen_invMass", "units" : "Gen m_{\mu\mu} [GeV]", "minX" : 0, "maxX" : 7, "bins" : 60, "linearYspace" : 1.2, "condition" :  "GenParticles[genLeptonsIdx[0]].Pt() > 2 && GenParticles[genLeptonsIdx[1]].Pt() > 2", "linearYspace" : 2  },
        { "obs" : "gen_invMass_orth", "formula" : "gen_invMass", "units" : "Gen m_{\mu\mu} [GeV]", "minX" : 0, "maxX" : 7, "bins" : 60, "linearYspace" : 1.2, "condition" :  "GenParticles[genLeptonsIdx[0]].Pt() > 2 && GenParticles[genLeptonsIdx[1]].Pt() > 2  && (GenParticles[genLeptonsIdx[1]].Pt() < 3.5 || gen_deltaR < 0.3)", "linearYspace" : 2 },
        
        { "obs" : "Muons_m1_pt", "formula" : "GenParticles[genLeptonsIdx[0]].Pt()", "units" : "Gen p_{T}(\mu_{1}) [GeV]", "minX" : 2, "maxX" : 20, "bins" : 60, "condition" :  "GenParticles[genLeptonsIdx[0]].Pt() < 25 && GenParticles_Status[genLeptonsIdx[0]] == 1 && abs(GenParticles_PdgId[genLeptonsIdx[0]]) == 13 && GenParticles[genLeptonsIdx[0]].Pt() > 2", "y_title" : "Number of muons" },
        { "obs" : "Muons_m2_pt", "formula" : "GenParticles[genLeptonsIdx[1]].Pt()", "units" : "Gen p_{T}(\mu_{2}) [GeV]", "minX" : 2, "maxX" : 20, "bins" : 60, "condition" :  "GenParticles[genLeptonsIdx[1]].Pt() < 25 && GenParticles_Status[genLeptonsIdx[1]] == 1 && abs(GenParticles_PdgId[genLeptonsIdx[1]]) == 13 && GenParticles[genLeptonsIdx[1]].Pt() > 2", "y_title" : "Number of muons" },
        { "obs" : "Muons_m1_eta", "formula" : "abs(GenParticles[genLeptonsIdx[0]].Eta())", "units" : "Gen |\eta|(\mu_{1})", "minX" : 0, "maxX" : 4, "bins" : 60, "condition" :  "GenParticles[genLeptonsIdx[0]].Pt() < 25 && GenParticles_Status[genLeptonsIdx[0]] == 1 && abs(GenParticles_PdgId[genLeptonsIdx[0]]) == 13 && GenParticles[genLeptonsIdx[0]].Pt() > 2", "linearYspace" : 1.4, "y_title" : "Number of muons" },
        { "obs" : "Muons_m2_eta", "formula" : "abs(GenParticles[genLeptonsIdx[1]].Eta())", "units" : "Gen |\eta|(\mu_{2})", "minX" : 0, "maxX" : 4, "bins" : 60, "condition" :  "GenParticles[genLeptonsIdx[1]].Pt() < 25 && GenParticles_Status[genLeptonsIdx[1]] == 1 && abs(GenParticles_PdgId[genLeptonsIdx[1]]) == 13 && GenParticles[genLeptonsIdx[1]].Pt() > 2", "linearYspace" : 1.4, "y_title" : "Number of muons" },
        
        
        { "obs" : "Muons_pt_barrel", "formula" : "GenParticles.Pt()", "units" : "Gen Barrel p_{T} [GeV]", "minX" : 2, "maxX" : 20, "bins" : 60, "condition" :  "GenParticles.Pt() < 25 && GenParticles_Status == 1 && abs(GenParticles_PdgId) == 13 && GenParticles.Pt() > 2 && abs(GenParticles.Eta()) < 1.2", "y_title" : "Number of muons" },
        { "obs" : "Muons_pt_endcape", "formula" : "GenParticles.Pt()", "units" : "Gen Endcaps p_{T} [GeV]", "minX" : 2, "maxX" : 20, "bins" : 60, "condition" :  "GenParticles.Pt() < 25 && GenParticles_Status == 1 && abs(GenParticles_PdgId) == 13 && GenParticles.Pt() > 2 && abs(GenParticles.Eta()) >= 1.2 && abs(GenParticles.Eta()) <= 2.4", "y_title" : "Number of muons" },
    ]
    
    weightString = {
        'MET' : "Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * BranchingRatio",
        'SingleMuon' : "1"
    }
    
    plot_bg = False
    plot_data = False
    show_lumi = True
    label_text = plotutils.StampStr.SIM
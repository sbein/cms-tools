#!/usr/bin/env python

from ROOT import *
from glob import glob
from math import *
from sys import exit
from array import array
import argparse
import sys
import numpy as np
import os

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes"))
from lib import histograms
from lib import cuts
from lib import analysis_ntuples
from lib import analysis_tools
from lib import utils
from utils import UOFlowTH1F
from datetime import datetime

gROOT.SetBatch(1)
gStyle.SetOptStat(0)

gSystem.Load('LumiSectMap_C')
from ROOT import LumiSectMap

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Plot Lepton Observeables.')
parser.add_argument('-i', '--input_file', nargs=1, help='Input Filename', required=False)
parser.add_argument('-o', '--output_file', nargs=1, help='Output Filename', required=False)
parser.add_argument('-s', '--single', dest='single', help='Single', action='store_true')
parser.add_argument('-c', '--cut', nargs=1, help='Cut', required=False)
parser.add_argument('-obs', '--obs', nargs=1, help='Obs', required=False)
args = parser.parse_args()

input_file = None
output_file = None
if args.input_file:
    input_file = args.input_file[0]
else:    
    
    #input_files = ["/afs/desy.de/user/n/nissanuv/nfs/2lx1x2x1/bg/skim_nlp/sum/type_sum/*ZJetsToNuNu_HT-600To800*"]
    

    
    #input_files = ["/afs/desy.de/user/n/nissanuv/nfs/2lx1x2x1/signal/skim_nlp/sum/higgsino_mu100_dm9p73Chi20Chipm.root"]
    input_files = ["/afs/desy.de/user/n/nissanuv/nfs/2lx1x2x1/signal/skim_nlp/sum/higgsino_mu100_dm1p47Chi20Chipm.root"]
    input_files = ["/afs/desy.de/user/n/nissanuv/nfs/2lx1x2x1/signal_jet_iso_cat/skim_nlp/sum/higgsino_mu100_dm3p28Chi20Chipm.root"]
    input_files = ["/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/sum/higgsino_mu100_dm3p28Chi20Chipm.root"]
    #input_files = ["/afs/desy.de/user/n/nissanuv/nfs/2lx1x2x1/bg/skim_nlp/sum/type_sum/*ZJetsToNuNu_HT-600To800*"]
    #input_files = ["/afs/desy.de/user/n/nissanuv/nfs/2lx1x2x1/bg/skim_nlp/sum/type_sum/*TTJets_DiLept*"]
    
if args.output_file:
    output_file = args.output_file[0]
else:
    output_file = "leptons.pdf"

plot_single = args.single

req_cut = None
req_obs = None
if plot_single:
    print("Printing Single Plot")
    if args.cut is None:
        print("Must provide cut with single option.")
        exit(0)
    if args.obs is None:
        print("Must provide obs with single option.")
        exit(0)
    req_cut = args.cut[0]
    req_obs = args.obs[0]

######## END OF CMDLINE ARGUMENTS ########

lepTypes = ["MM", "Zl"]

plot_overflow = True

def tightID(c, lepFlavour, l, li, track, minCanT, ljet, params):
    return bool(eval("c." + lepFlavour + "_tightID")[li])

def deltaPhiLJ(c, lepFlavour, l, li, track, minCanT, ljet, params):
    if lepFlavour == "Electrons":
        return True
    return abs(l.DeltaPhi(c.Jets[ljet])) > 1
    


lepConds = {
    "e" : { "Zl" : "Electrons_matchGen == 1",
            "MM" : "Electrons_matchGen == 0"},
    "m" : { "Zl" : "Muons_matchGen == 1",
            "MM" : "Muons_matchGen == 0"},
}

lepConds = {
    "e" : { "Zl" : "Electrons_isZ == 1",
            "MM" : "Electrons_isZ == 0"},
    "m" : { "Zl" : "Muons_isZ == 1",
            "MM" : "Muons_isZ == 0"},
}

hist2DConds = {
    "e" : "Electrons_isZ == 1",
    "m" : "Muons_isZ == 1"
}

hist2DConds = {
    "e" : "",
    "m" : "",
    "g" : ""
}

cuts = [{"name":"none", "title": "No Cuts", "condition": {"e" : "1", "m" : "1"  }},

        

        {"name":"no_iso", "title": "no_iso", "condition": {"e" : "Electrons_deltaRLJ > 0.4 && Electrons.Pt() < 25", "m" : "Muons.Pt() < 25 && Muons.Pt() > 2 && Muons_deltaRLJ > 0.4 && Muons_mediumID == 1 "  }},
        {"name":"no_iso_lt2", "title": "no_iso lt2", "condition": {"e" : "Electrons_deltaRLJ > 0.4 && Electrons.Pt() < 2", "m" : "Muons.Pt() > 1.6 && Muons.Pt() < 2 && Muons_deltaRLJ > 0.4 && Muons_mediumID == 1 "  }},
        {"name":"no_iso_lt2_iso", "title": "no_iso lt2_iso", "condition": {"e" : "Electrons_deltaRLJ > 0.4 && Electrons.Pt() < 2", "m" : "Muons.Pt() > 1.6 && Muons.Pt() < 2 && Muons_deltaRLJ > 0.4 && Muons_mediumID == 1 && Muons_passCorrJetIso15 == 1"  }},
        {"name":"no_iso_lt2_tight", "title": "no_iso lt2 tight", "condition": {"e" : "Electrons_deltaRLJ > 0.4 && Electrons.Pt() < 2", "m" : "Muons.Pt() > 1.6 && Muons.Pt() < 2 && Muons_deltaRLJ > 0.4 && Muons_tightID == 1 "  }},
        {"name":"no_iso_2_25", "title": "no_iso 2_25", "condition": {"e" : "Electrons_deltaRLJ > 0.4 && Electrons.Pt() > 2", "m" : "Muons.Pt() < 25 && Muons.Pt() > 2 && Muons_deltaRLJ > 0.4 && Muons_mediumID == 1 "  }},
        #{"name":"no_iso_5_10", "title": "no_iso 5_10", "condition": {"e" : "Electrons_deltaRLJ > 0.4 && Electrons.Pt() < 10", "m" : "Muons.Pt() < 10 && Muons.Pt() > 5 && Muons_deltaRLJ > 0.4 && Muons_mediumID == 1 "  }},
        #{"name":"no_iso_10_25", "title": "no_iso 10_25", "condition": {"e" : "Electrons_deltaRLJ > 0.4 && Electrons.Pt() > 10 && Electrons.Pt() < 25", "m" : "Muons.Pt() < 25 && Muons.Pt() > 10 && Muons_deltaRLJ > 0.4 && Muons_mediumID == 1 "  }},



        #{"name":"no_iso", "title": "no_iso", "condition": {"e" : "Electrons_deltaRLJ > 0.4 && Electrons.Pt() < 25", "m" : "Muons.Pt() < 25 && Muons.Pt() > 2 && Muons_deltaRLJ > 0.4 && Muons_mediumID == 1 "  }},
        #{"name":"all", "title": "all", "condition": {"e" : "Electrons_deltaRLJ > 0.4 && Electrons.Pt() < 25 && Electrons_passIso == 1", "m" : "Muons.Pt() < 25 && Muons.Pt() > 2 && Muons_deltaRLJ > 0.4 && Muons_mediumID == 1 "  }},
        #{"name":"pt_lt2_iso", "title": "1 < Pt < 2 and jet iso", "condition": {"e" : "Electrons.Pt() < 5", "m" : "Muons.Pt() < 2 && Muons.Pt() > 1 && Muons_passJetIso == 1 && Muons_deltaRLJ > 0.4"  }},
        #{"name":"pt_lt1", "title": "1 < Pt < 1.5 and muon mediuimId and deltaRLJ > 0.4", "condition": {"e" : "Electrons_passJetIso == 1 && Electrons.Pt() < 5", "m" : "Muons.Pt() < 1.5 && Muons.Pt() > 1 && Muons_mediumID == 1 && Muons_deltaRLJ > 0.4 && Muons_passJetIso == 1"  }},
        
        
        # {"name":"pt_lt2", "title": "1.5 < Pt < 2 and muon mediuimId and deltaRLJ > 0.4", "condition": {"e" : "Electrons_passJetIso == 1 && Electrons.Pt() < 5", "m" : "Muons.Pt() < 2 && Muons.Pt() > 1.5 && Muons_mediumID == 1 && Muons_tightID == 1 && Muons_deltaRLJ > 0.4 && Muons_passJetIso == 1"  }},
#         {"name":"pt_lt5_iso", "title": "2 < Pt < 5 and jet iso", "condition": {"e" : "Electrons.Pt() < 5", "m" : "Muons.Pt() < 5 && Muons.Pt() > 2 && Muons_passJetIso == 1 && Muons_deltaRLJ > 0.4"  }},
#         {"name":"pt_lt5", "title": "2 < Pt < 5 and muon mediuimId and deltaRLJ > 0.4", "condition": {"e" : "Electrons_passJetIso == 1 && Electrons.Pt() < 5", "m" : "Muons.Pt() < 5 && Muons.Pt() > 2 && Muons_mediumID == 1 && Muons_deltaRLJ > 0.4 && Muons_passJetIso == 1"  }},
#         {"name":"pt_lt10_iso", "title": "5 < Pt < 10 and jet iso", "condition": {"e" : "Electrons_passJetIso == 1 && Electrons.Pt() < 10 && Electrons.Pt() > 5 && Electrons_deltaRLJ > 0.4", "m" : "Muons.Pt() < 10 && Muons.Pt() > 5 && Muons_passJetIso == 1 && Muons_deltaRLJ > 0.4"  }},
#         {"name":"pt_lt10", "title": "5 < Pt < 10 and Electrons_passIso and Muons_mediuimId", "condition": {"e" : "Electrons_passJetIso == 1 && Electrons_passIso == 1 && Electrons.Pt() < 10 && Electrons.Pt() > 5 && Electrons_deltaRLJ > 0.4", "m" : "Muons.Pt() < 10 && Muons.Pt() > 5 && Muons_mediumID == 1 && Muons_deltaRLJ > 0.4 && Muons_passJetIso == 1"  }},
#         {"name":"pt_gt10_iso", "title": "10 < Pt < 25 and jet iso", "condition": {"e" : "Electrons_passJetIso == 1 && Electrons.Pt() < 25 && Electrons.Pt() > 10 && Electrons_deltaRLJ > 0.4", "m" : "Muons.Pt() < 25 && Muons.Pt() > 10 && Muons_passJetIso == 1 && Muons_deltaRLJ > 0.4"  }},
#         {"name":"pt_gt10", "title": "10 < Pt < 25 and Electrons_passIso and Muons_mediuimId", "condition": {"e" : "Electrons_passJetIso == 1 && Electrons_passIso == 1 && Electrons.Pt() < 25 && Electrons.Pt() > 10 && Electrons_deltaRLJ > 0.4", "m" : "Muons.Pt() < 25 && Muons.Pt() > 10 && Muons_mediumID == 1 && Muons_deltaRLJ > 0.4 && Muons_passJetIso == 1"  }},
#         {"name":"pt_gt25", "title": "Pt > 25", "condition": {"e" : "Electrons.Pt() > 25", "m" : "Muons.Pt() > 25"  }},
#         {"name":"pt_gt25_jetiso", "title": "Pt > 25 and passJetIso", "condition": {"e" : "Electrons_passJetIso == 1 && Electrons.Pt() > 25", "m" : "Muons_passJetIso == 1 && Muons.Pt() > 25"  }},
#         {"name":"pt_gt25_iso", "title": "Pt > 25 and passIso", "condition": {"e" : "Electrons_passJetIso == 1 && Electrons_tightID == 1 && Electrons.Pt() > 25", "m" : "Muons_passIso == 1 && Muons.Pt() > 25 && Muons_passJetIso == 1"  }},
        
        
        #{"name":"mediuimId", "title": "mediuimId", "condition": {"e" : "1", "m" : "Muons_mediumID == 1 && Muons_deltaRLJ > 0.4"  }},
        {"name":"all", "title": "all", "condition": {"e" : "Electrons_passJetIso == 1 && Electrons.Pt() < 25 && Electrons_deltaRLJ > 0.4", "m" : "Muons_passJetIso == 1  && Muons_mediumID == 1 && Muons_deltaRLJ > 0.4 && Muons.Pt() < 25 && Muons.Pt() > 2"  }, "funcs":[deltaPhiLJ]},
    
    
        #{"name":"mediumId", "title": "mediumId", "funcs":[mediumId, pt]},
    #{"name":"passIso", "title": "passIso", "funcs":[passIso, pt]},
    #{"name":"tightID", "title": "tightID", "funcs":[tightID, pt]},
    
    
    #{"name":"pt", "title": "pt > 1.8", "funcs":[pt]},
    #{"name":"tightID", "title": "Eta < 2.6, deltaEtaLL < 1, deltaEtaLJ < 3.8", "funcs":[eta, deltaEtaLL, deltaEtaLJ]},
    #{"name":"Pt_Eta_dxy_dz", "title": "Eta < 2.6, Pt > 2.5, dxy < 0.05, dz < 0.06", "funcs":[eta, pt, dxy, dz]},
    #{"name":"Pt_Eta_dxy_dz_deltaEtaLL", "title": "Eta < 2.6, Pt > 2.5, dxy < 0.05, dz < 0.06, deltaEtaLL < 1", "funcs":[eta, pt, dxy, dz, deltaEtaLL]},
    #{"name":"Pt_Eta_dxy_dz_deltaEtaLL_deltaEtaLJ", "title": "Eta < 2.6, Pt > 2.5, dxy < 0.05, dz < 0.06, deltaEtaLL < 1, deltaEtaLJ < 3.8", "funcs":[eta, pt, dxy, dz, deltaEtaLL, deltaEtaLJ]},
    #{"name":"Pt_Eta_dxy_dz_deltaEtaLL_deltaRLJ", "title": "Eta < 2.6, Pt > 2.5, dxy < 0.05, dz < 0.06, deltaEtaLL < 1, deltaRLJ > 1.8", "funcs":[eta, pt, dxy, dz, deltaEtaLL, deltaRLJ]},
    #{"name":"Pt_Eta_dxy_dz_deltaEtaLL_deltaRLJ_deltaRLL", "title": "Eta < 2.6, Pt > 2.5, dxy < 0.05, dz < 0.06, deltaEtaLL < 1, deltaRLJ > 1.8, deltaRLL < 1.1", "funcs":[eta, pt, dxy, dz, deltaEtaLL, deltaRLJ, deltaRLL]}
]

histoDefs = [
    {"obs" : "abs(Electrons.Eta())", "bins" : 50, "minX" : 0, "maxX" : 2.5, "lep" : "e" },
    {"obs" : "abs(Muons.Eta())", "bins" : 50, "minX" : 0, "maxX" : 2.5, "lep" : "m" },
    #{"obs" : "abs(Electrons.Phi())", "bins" : 50, "minX" : 0, "maxX" : 3.5, "lep" : "e"},
    #{"obs" : "abs(Muons.Phi())", "bins" : 50, "minX" : 0, "maxX" : 3.5, "lep" : "m" },
    {"obs" : "abs(Electrons.Pt())", "bins" : 60, "minX" : 0, "maxX" : 30, "lep" : "e" },
    {"obs" : "abs(Muons.Pt())", "bins" : 60, "minX" : 0, "maxX" : 5, "lep" : "m" },
    {"obs" : "Muons_minDeltaRJets", "bins" : 30, "minX" : 0, "maxX" : 1, "lep" : "m" },
    {"obs" : "Electrons_minDeltaRJets", "bins" : 30, "minX" : 0, "maxX" : 1, "lep" : "e" },
    
    
    {"obs" : "Jets_muonEnergyFraction[Muons_closestJet]", "bins" : 60, "minX" : 0, "maxX" : 1, "lep" : "m" },
    {"obs" : "Jets_electronEnergyFraction[Electrons_closestJet]", "bins" : 60, "minX" : 0, "maxX" : 1, "lep" : "e" },
    
    {"obs" : "Jets_muonMultiplicity[Muons_closestJet]", "bins" : 7, "minX" : 0, "maxX" : 7, "lep" : "m" },
    {"obs" : "Jets_electronMultiplicity[Electrons_closestJet]", "bins" : 7, "minX" : 0, "maxX" : 7, "lep" : "e" },
    
    {"obs" : "Electrons_passIso", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "e" },
    {"obs" : "Muons_passIso", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "m" },
    {"obs" : "Electrons_mediumID", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "e" },
    {"obs" : "Muons_mediumID", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "m" },
    {"obs" : "Electrons_tightID", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "e" },
    {"obs" : "Muons_tightID", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "m" },
    {"obs" : "Electrons_deltaRLJ", "bins" : 50, "minX" : 0, "maxX" : 6, "lep" : "e"},
    {"obs" : "Muons_deltaRLJ", "bins" : 50, "minX" : 0, "maxX" : 6, "lep" : "m"},
    #{"obs" : "Electrons_deltaEtaLJ", "bins" : 50, "minX" : 0, "maxX" : 6, "lep" : "e"},
    #{"obs" : "Muons_deltaEtaLJ", "bins" : 50, "minX" : 0, "maxX" : 6, "lep" : "m"},
    
    
    {"obs" : "Electrons_passJetIso", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "e" },
    {"obs" : "Electrons_passNonJetIso", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "e" },
    {"obs" : "Electrons_passCorrJetIso0", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "e" },
    {"obs" : "Electrons_passCorrJetIso1", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "e" },
    {"obs" : "Electrons_passCorrJetIso5", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "e" },
    {"obs" : "Electrons_passCorrJetIso10", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "e" },
    {"obs" : "Electrons_passCorrJetIso15", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "e" },
    
    {"obs" : "Muons_passJetIso", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "m" },
    {"obs" : "Muons_passNonJetIso", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "m" },
    {"obs" : "Muons_passCorrJetIso0", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "m" },
    {"obs" : "Muons_passCorrJetIso1", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "m" },
    {"obs" : "Muons_passCorrJetIso5", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "m" },
    {"obs" : "Muons_passCorrJetIso10", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "m" },
    {"obs" : "Muons_passCorrJetIso15", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "m" },
    
    {"obs" : "twoLeptonsJetIso", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "g" },
    {"obs" : "twoLeptonsJetIsoLowPt", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "g" },
    {"obs" : "twoLeptonsJetIsoLowPtTight", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "g" },
    {"obs" : "twoLeptonsNonJetIso", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "g" },
    {"obs" : "twoLeptonsNonJetIsoLowPt", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "g" },
    {"obs" : "twoLeptonsNonJetIsoLowPtTight", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "g" },
    {"obs" : "twoLeptonsCorrJetIso0", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "g" },
    {"obs" : "twoLeptonsCorrJetIso0LowPt", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "g" },
    {"obs" : "twoLeptonsCorrJetIso0LowPtTight", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "g" },
    {"obs" : "twoLeptonsCorrJetIso1", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "g" },
    {"obs" : "twoLeptonsCorrJetIso1LowPt", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "g" },
    {"obs" : "twoLeptonsCorrJetIso1LowPtTight", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "g" },
    {"obs" : "twoLeptonsCorrJetIso5", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "g" },
    {"obs" : "twoLeptonsCorrJetIso5LowPt", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "g" },
    {"obs" : "twoLeptonsCorrJetIso5LowPtTight", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "g" },
    {"obs" : "twoLeptonsCorrJetIso10", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "g" },
    {"obs" : "twoLeptonsCorrJetIso10LowPt", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "g" },
    {"obs" : "twoLeptonsCorrJetIso10LowPtTight", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "g" },
    {"obs" : "twoLeptonsCorrJetIso15", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "g" },
    {"obs" : "twoLeptonsCorrJetIso15LowPt", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "g" },
    {"obs" : "twoLeptonsCorrJetIso15LowPtTight", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "g" }, 

    
    # {"name" : "passCorrJetIso - Electrons","obs" : "Electrons_correctedClosestJet < 0 || Electrons_correctedMinDeltaRJets >= 0.4 || Jets_electronCorrected[Electrons_correctedClosestJet].E() < 0 || (Electrons_correctedClosestJet >= 0 && Jets_multiplicity[Electrons_correctedClosestJet] < 10 &&  Jets_electronCorrected[Electrons_correctedClosestJet].Pt() < 15)", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "e"},
#     {"name" : "passCorrJetIso - Muons", "obs" : "Muons_correctedClosestJet < 0 || Muons_correctedMinDeltaRJets >= 0.4 || Jets_muonCorrected[Muons_correctedClosestJet].E() < 0 || (Muons_correctedClosestJet >=0 && Jets_multiplicity[Muons_correctedClosestJet] < 10 &&  Jets_muonCorrected[Muons_correctedClosestJet].Pt() < 15)", "bins" : 2, "minX" : 0, "maxX" : 2, "lep" : "m" },
#     
#    
    
    {"name" : "Jets_electronCorrected[Electrons_correctedClosestJet].E()", "obs" : "(Electrons_correctedMinDeltaRJets < 0.4) * Jets_electronCorrected[Electrons_correctedClosestJet].E()", "bins" : 100, "minX" : 0, "maxX" : 25, "lep" : "e" },
    {"name" : "Jets_muonCorrected[Muons_correctedClosestJet].E()", "obs" : "(Muons_correctedMinDeltaRJets < 0.4) * Jets_muonCorrected[Muons_correctedClosestJet].E()", "bins" : 100, "minX" : 0, "maxX" : 25, "lep" : "m" },
#     
     
     {"name" : "Jets_electronCorrected[Electrons_correctedClosestJet].Pt()", "obs" : "((Jets_electronCorrected[Electrons_correctedClosestJet].E() > 0 && Electrons_correctedMinDeltaRJets < 0.4) * Jets_electronCorrected[Electrons_correctedClosestJet].Pt())", "bins" : 100, "minX" : 0, "maxX" : 25, "lep" : "e" },
     {"name" : "Jets_muonCorrected[Muons_correctedClosestJet].Pt()", "obs" : "((Jets_muonCorrected[Muons_correctedClosestJet].E() > 0 && Muons_correctedMinDeltaRJets < 0.4) * Jets_muonCorrected[Muons_correctedClosestJet].Pt())", "bins" : 100, "minX" : 0, "maxX" : 25, "lep" : "m" },
#     
#     
    {"name" : "electronMultiplicity - Jets_electronCorrected[Electrons_correctedClosestJet].Pt()","obs" : "((Jets_electronCorrected[Electrons_correctedClosestJet].E() > 0 && Electrons_correctedMinDeltaRJets < 0.4) * Jets_electronCorrected[Electrons_correctedClosestJet].Pt())", "bins" : 100, "minX" : 0, "maxX" : 25, "lep" : "e", "extraConds" : "Jets_multiplicity[Electrons_correctedClosestJet] < 10"},
    {"name" : "muonMultiplicity - Jets_muonCorrected[Muons_correctedClosestJet].Pt()", "obs" : "((Jets_muonCorrected[Muons_correctedClosestJet].E() > 0 && Muons_correctedMinDeltaRJets < 0.4) * Jets_muonCorrected[Muons_correctedClosestJet].Pt())", "bins" : 100, "minX" : 0, "maxX" : 25, "lep" : "m", "extraConds" : "Jets_multiplicity[Muons_correctedClosestJet] < 10" },  
   
    # {"obs" : "Jets_multiplicity[Electrons_closestJet]:Electrons_minDeltaRJets", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "e", "extraConds" = "" },
#     {"obs" : "Jets_multiplicity[Muons_closestJet]:Muons_minDeltaRJets", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "m",  "extraConds" = ""},
#     
#     {"obs" : "Jets_electronEnergyFraction[Electrons_closestJet]:Electrons_minDeltaRJets", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "e", "extraConds" = "" },
#     {"obs" : "Jets_muonEnergyFraction[Muons_closestJet]:Muons_minDeltaRJets", "bins" : 2, "minX" : 0, "maxX" : 1, "lep" : "m", "extraConds" = "" },
    
#     
#     {"obs" : "MT2Activity", "title" : "MT2Activity", "bins" : 50, "minX" : 0, "maxX" : 0.1, "func" : lambda c, lepFlavour, lep, li, track, ti, lj, params: eval("c." + lepFlavour + "_MT2Activity")[li] },
#     
#     {"obs" : "deltaRLJ", "title" : "deltaRLJ", "bins" : 50, "minX" : 0, "maxX" : 6, "func" : lambda c, lepFlavour, lep, li, track, ti, lj, params:  abs(lep.DeltaR(c.Jets[lj])) },
#     {"obs" : "deltaPhiLJ", "title" : "deltaPhiLJ", "bins" : 50, "minX" : 0, "maxX" : 6, "func" : lambda c, lepFlavour, lep, li, track, ti, lj, params:  abs(lep.DeltaPhi(c.Jets[lj])) },
#     {"obs" : "deltaEtaLJ", "title" : "deltaEtaLJ", "bins" : 50, "minX" : 0, "maxX" : 6, "func" : lambda c, lepFlavour, lep, li, track, ti, lj, params:  abs(lep.Eta() - c.Jets[lj].Eta()) },
   
]

def createAllHistograms(files_to_process, histograms):
    for f in files_to_process:
        print(f)
        rootFile = TFile(f)
        c = rootFile.Get('tEvent')
        for cut in cuts:
            if plot_single and cut["name"] != req_cut:
                continue
            for hist_def in histoDefs:
                if plot_single and hist_def["obs"] != req_obs:
                    continue
                    
                
                if ":" in hist_def["obs"] or hist_def["lep"] == "g":
                    #2D histogram
                    histName = (hist_def["name"] if hist_def.get("name") is not None else hist_def["obs"]) + "_" + cut["name"]
                    drawString = hist2DConds.get(hist_def["lep"])
                    if hist_def["lep"] != "g":
                        if drawString is not None and len(drawString) > 0:
                            drawString += " && (" + cut["condition"][hist_def["lep"]] + ")"
                        else:
                            drawString = "(" + cut["condition"][hist_def["lep"]] + ")"
                    if hist_def.get("extraConds") is not None and len(hist_def["extraConds"]) > 0:
                        drawString += " && (" + hist_def["extraConds"] + ")"
                    print("Drawing histogram", histName, "with cond", drawString)
                    hist = utils.getHistogramFromTree(histName, c, hist_def.get("obs"), hist_def.get("bins"), hist_def.get("minX"), hist_def.get("maxX"), drawString, plot_overflow)
                    hist.Sumw2()
                    hist.SetTitle("")
                    if histograms.get(histName) is None:
                        histograms[histName] = hist
                    else:
                        histograms[histName].Add(hist)
                else:
                    for lepType in lepTypes:
                        histName = (hist_def["name"] if hist_def.get("name") is not None else hist_def["obs"]) + "_" + cut["name"] + "_" + lepType
                        drawString = lepConds[hist_def["lep"]][lepType] + " && (" + cut["condition"][hist_def["lep"]] + ")"
                        if hist_def.get("extraConds") is not None and len(hist_def["extraConds"]) > 0:
                            drawString += " && (" + hist_def["extraConds"] + ")"
                        print("Drawing histogram", histName, "with cond", drawString)
                        hist = utils.getHistogramFromTree(histName, c, hist_def.get("obs"), hist_def.get("bins"), hist_def.get("minX"), hist_def.get("maxX"), drawString, plot_overflow)
                        hist.Sumw2()
                        hist.SetTitle("")
                        if histograms[lepType].get(histName) is None:
                            histograms[lepType][histName] = hist
                        else:
                            histograms[lepType][histName].Add(hist)
        rootFile.Close()


def main():
    print("Start: " + datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    
    histograms = {"Zl" : {}, "MM" : {}}
    memory = []
    
    files_to_process = []
    for file_pattern in input_files:
        files_to_process.extend(glob(file_pattern))
    
    print("Going to process the following files:")
    print(files_to_process)
    
    createAllHistograms(files_to_process, histograms)

    c1 = TCanvas("c2", "c2", 800, 800)
    
    if plot_single:
        c1.SetBottomMargin(0.16)
        c1.SetLeftMargin(0.18)
    
    plot_title = True
    if plot_single:
        plot_title = False
    
    titlePad = None
    histPad = None
    t = None
    if plot_title:
        titlePad = TPad("titlePad", "",0.0,0.93,1.0,1.0)
        histPad = TPad("histPad", "",0.0,0.0,1.0,0.93)
        titlePad.Draw()
        t = TPaveText(0.0,0.93,1.0,1.0,"NB")
        t.SetFillStyle(0)
        t.SetLineColor(0)
        t.SetTextFont(40);
        t.AddText("No Cuts")
        t.Draw()
    else:
        histPad = c1
    
    histPad.Draw()
    if not plot_single:
        histPad.Divide(2,2)

    OUTPUT_FILE = output_file or "./lepton_obs.pdf"
    c1.Print(OUTPUT_FILE + "[");

    for cut in cuts:
        if plot_single and req_cut != cut["name"]:
            continue
        
        if plot_title:
            t.Clear()
            t.AddText(cut["title"])
            t.Draw()
            titlePad.Update()
        
        pId = 1
        needToDraw = False
        
        for histDef in histoDefs:
            if plot_single and req_obs != histDef["name"]:
                continue
            
            for log in [True, False]:
                if plot_single and log:
                    continue
                if plot_single:
                    pad = histPad.cd()
                else:
                    pad = histPad.cd(pId)
                    pad.cd()
            
                legend = TLegend(.75,.75,.89,.89)
                memory.append(legend)
                cP = 0
                maxY = 0
                drawSame = False
                if ":" in histDef["obs"] or histDef["lep"] == "g":
                    name = (histDef["name"] if histDef.get("name") is not None else histDef["obs"]) + "_" + cut["name"]
                    h = histograms[name]
                    utils.formatHist(h, utils.colorPalette[cP], 0.35, True)
                    needToDraw = True
                    h.GetXaxis().SetTitle(histDef["name"] if histDef.get("name") is not None else histDef["obs"])
                    h.Draw("HIST")
                else:
                    for lepType in lepTypes:
                        name = (histDef["name"] if histDef.get("name") is not None else histDef["obs"]) + "_" + cut["name"] + "_" + lepType
                        h = histograms[lepType][name]
                        maxY = max(maxY, h.GetMaximum())
                    for lepType in lepTypes:
                        name = (histDef["name"] if histDef.get("name") is not None else histDef["obs"]) + "_" + cut["name"] + "_" + lepType
                        h = histograms[lepType][name]
                        utils.formatHist(h, utils.colorPalette[cP], 0.35, True)
                        if plot_single:
                            utils.histoStyler(h)
                            h.GetYaxis().SetTitleOffset(1.15)
                    
                        cP += 1
                        h.SetMaximum(maxY)
                        #if log:
                        h.SetMinimum(0.01)
                        #else:
                        #h.SetMinimum(0)
                        legend.AddEntry(h, lepType, 'F')
                        if drawSame:
                            #print("DRAW SAME", name, lepType)
                            h.Draw("HIST SAME")
                        else:
                            #print("DRAW", name, lepType)
                            needToDraw = True
                            h.GetXaxis().SetTitle(histDef["name"] if histDef.get("name") is not None else histDef["obs"])
                            h.Draw("HIST")
                            drawSame = True
                legend.Draw("SAME")
                pad.SetLogy(log)
                c1.Update()
                pId += 1
    
            if pId > 4:
                pId = 1
                c1.Print(OUTPUT_FILE);
                needToDraw = False;
        
        if needToDraw and not plot_single:
            for id in range(pId, 5):
                print("Clearing pad " + str(id))
                pad = histPad.cd(id)
                pad.Clear()
            c1.Print(OUTPUT_FILE);
    if plot_single:
        utils.stamp_plot()
        c1.Print(OUTPUT_FILE);
    c1.Print(OUTPUT_FILE+"]");
    
    print("End: " + datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    exit(0)
    
main()

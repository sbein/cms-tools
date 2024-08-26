#!/usr/bin/env python

from ROOT import *
from glob import glob
from sys import exit
import argparse
import sys
import os
import re
from datetime import datetime
import math

#this script had trouble because the names of variables like MHT were different (Mht)

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes"))
import utils
import analysis_ntuples

gROOT.SetBatch(True)
gStyle.SetOptStat(0)

gSystem.Load('LumiSectMap_C')
from ROOT import LumiSectMap

#lumi = 5746.370
#weight = lumi / utils.LUMINOSITY

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Plot skims for x1x2x1 process with BDTs.')
parser.add_argument('-o', '--output_file', nargs=1, help='Output Filename', required=False)
parser.add_argument('-s', '--single', dest='single', help='Single', action='store_true')
parser.add_argument('-c', '--cut', nargs=1, help='Cut', required=False)
parser.add_argument('-obs', '--obs', nargs=1, help='Obs', required=False)
parser.add_argument('-lep', '--lep', dest='lep', help='Single', action='store_true')
parser.add_argument('-bt', '--bg_retag', dest='bg_retag', help='Background Retagging', action='store_true')
args = parser.parse_args()

output_file = None

plot_2l = args.lep
bg_retag = args.bg_retag


bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/type_sum/"

signal_dir = [
              "/nfs/dust/cms/user/beinsam/x1x2x1/signal/skim_sam/sum/mChipm100GeV_dm1p76GeV_1.root"
              ]

calculatedLumi = None
#signal_dir = None
sc_bg_dir = None
sc_data_dir = None

if plot_2l:
    #bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/2lx1x2x1/bg/skim_dilepton_signal_bdt/all/single"
    #bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/2lx1x2x1/bg/skim_nlp/sum/type_sum"
    #signal_dir = "/afs/desy.de/user/n/nissanuv/nfs/2lx1x2x1/signal/skim_dilepton_signal_bdt_all/single/higgsino_mu100_dm3p28Chi20Chipm.root"
    data_dir = "/afs/desy.de/user/n/nissanuv/nfs/2lx1x2x1/data/skim_dilepton_signal_bdt/all/single"
    sc_bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/2lx1x2x1/bg/skim_dilepton_signal_bdt_sc/all/single"
    sc_data_dir = "/afs/desy.de/user/n/nissanuv/nfs/2lx1x2x1/data/skim_dilepton_signal_bdt_sc/all/single"
    calculatedLumi = {
        'MET' : 35.350177774,
        'SingleMuon' : 22.143021976
    }
else:
    #bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_dilepton_signal_bdt/all/single"
    #signal_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_dilepton_signal_bdt_all/single/higgsino_mu100_dm3p28Chi20Chipm.root"
    data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim_dilepton_signal_bdt/all/single"
    sc_bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_dilepton_signal_bdt_sc/all/single"
    sc_data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim_dilepton_signal_bdt_sc/all/single"
    calculatedLumi = {
        'MET' : 35.380786178,
        'SingleMuon' : 22.143021976
    }

weightString = {
    'MET' : "passedMhtMet6pack * tEffhMetMhtRealXMht2016",
    'MET' : "1",
    'SingleMuon' : "1"
}

bgReTagging = {
    "tautau" : "tautau",
    "sc" : "sc * (!tautau)",
    "tc" : "tc * (!tautau)",
    "rf" : "rf",
    "ff" : "ff"
}

bgReTaggingOrder = {
    "tautau" : 0,
    "sc" : 2,
    "tc" : 3,
    "rf" : 4,
    "ff" : 1
}

# tree.Branch('tautau', var_tautau,'tautau/b')
# tree.Branch('rr', var_rr,'rr/b')
# tree.Branch('rf', var_rf,'rf/b')
# tree.Branch('ff', var_ff,'ff/b')
# tree.Branch('sc', var_sc,'sc/b')
# tree.Branch('n_body', var_n_body,'n_body/b')
# tree.Branch('tc', var_tc,'tc/b')
# tree.Branch('other', var_other,'other/b')
# 
# tree.Branch('omega', var_omega,'omega/b')
# tree.Branch('rho_0', var_rho_0,'rho_0/b')
# tree.Branch('eta', var_eta,'eta/b')
# tree.Branch('phi', var_phi,'phi/b')
# tree.Branch('eta_prime', var_eta_prime,'eta_prime/b')
# tree.Branch('j_psi', var_j_psi,'j_psi/b')
# tree.Branch('upsilon_1', var_upsilon_1,'upsilon_1/b')
# tree.Branch('upsilon_2', var_upsilon_2,'upsilon_2/b')

bgReTagging = {
    #"tautau" : "tautau",
    "tc" : "tc * (!tautau)",
    #"fake" : "(rf || ff)",
}

bgReTaggingOrder = {
    "tautau" : 0,
    "rr" : 1,
    "tc" : 3,
    "fake" : 2
}

# bgReTagging = {
#     "tcmuons" : "tc * (!tautau)",
#     "tctautau" : "tc * tautau",
#     "other" : "other * (!tautau) * (!omega) * (!rho_0) * (!eta) * (!phi) * (!eta_prime) * (!j_psi) * (!upsilon_1) * (!upsilon_2)",
#     "tautau" : "tautau * (!tc) * (!omega) * (!rho_0) * (!eta) * (!phi) * (!eta_prime) * (!j_psi) * (!upsilon_1) * (!upsilon_2)",
#     "omega" : "omega",
#     "rho" : "rho_0",
#     "eta" : "eta",
#     "phi" : "phi",
#     "etaprime" : "eta_prime",
#     "jpsi" : "j_psi",
#     "upsilon1" : "upsilon_1",
#     "upsilon2" : "upsilon_2",
#     #"tc" : "tc",
#     "nbody" : "n_body",
#     "sc" : "sc * (!tautau) * (!omega) * (!rho_0) * (!eta) * (!phi) * (!eta_prime) * (!j_psi) * (!upsilon_1) * (!upsilon_2)"
# 
#     # "tautau" : "tautau",
# #     "n_body" : "n_body",
# #     
# #     "sc" : "sc * (!tautau)"
# }
# 
bgReTagging = {
    #"tcmuons" : "tc * (!tautau)",
    #"tctautau" : "tc * tautau",
#    "other" : "other * (!tautau) * (!omega) * (!rho_0) * (!eta) * (!phi) * (!eta_prime) * (!j_psi) * (!upsilon_1) * (!upsilon_2)",
    #"tautau" : "tautau * (!tc) * (!omega) * (!rho_0) * (!eta) * (!phi) * (!eta_prime) * (!j_psi) * (!upsilon_1) * (!upsilon_2)",
    "omega" : "omega",
    "rho" : "rho_0",
    "eta" : "eta",
    "phi" : "phi",
    "etaprime" : "eta_prime",
    "jpsi" : "j_psi",
    "upsilon1" : "upsilon_1",
    "upsilon2" : "upsilon_2",
    #"tc" : "tc",
    "nbody" : "n_body",
    "scother" : "sc * (!tautau) * (!omega) * (!rho_0) * (!eta) * (!phi) * (!eta_prime) * (!j_psi) * (!upsilon_1) * (!upsilon_2)"

    # "tautau" : "tautau",
#     "n_body" : "n_body",
#     
#     "sc" : "sc * (!tautau)"
}

bgReTaggingOrder = {
#    "tcmuons" : -4,
#    "tctautau" : -3,
#    "tautau" : -2,
    "other" : -1,
    "omega" : 0,
    "rho" : 1,
    "eta" : 2,
    "phi" : 3,
    "etaprime" : 4,
    "jpsi" : 5,
    "upsilon1" : 6,
    "upsilon2" : 7,
    #"tc" : 8,
    "nbody" : 9,
    "scother" : 10


    # "tautau" : 0,
#     "sc" : 1,
}

bgReTagging = {
    "tautau" : "tautau",
    "sc" : "sc * (!tautau)",
    "tc_btag_veto" : "(BTagsDeepMedium == 0) * (tc || other) * (!tautau) * (!omega) * (!rho_0) * (!eta) * (!phi) * (!eta_prime) * (!j_psi) * (!upsilon_1) * (!upsilon_2)",
    "tc_2_btags" : "(BTagsDeepMedium == 2) * (tc || other) * (!tautau) * (!omega) * (!rho_0) * (!eta) * (!phi) * (!eta_prime) * (!j_psi) * (!upsilon_1) * (!upsilon_2)",
    "fake" : "(rf || ff)",
    "other_sc": "other * (!tautau) * (omega || rho_0 || eta || phi || eta_prime || j_psi || upsilon_1 || upsilon_2)",
    "other_no_sc" : "other * (!tautau) * (!omega) * (!rho_0) * (!eta) * (!phi) * (!eta_prime) * (!j_psi) * (!upsilon_1) * (!upsilon_2)",
    "n_body" : "n_body * (!tautau)"
}

bgReTaggingOrder = {
    "tc_btag_veto" : 0, 
    "tc_2_btags" : 1
}


#[  [["tc_btag_veto"],["tc_2_btags"]]  ]

# bgReTagging = {
#     "tautau" : "tautau",
#     "sc" : "((other || sc) * (!tautau))",
#     "tc" : "tc * (!tautau)",
#     "nbody" : "n_body",
#     "fake" : "(rf || ff)",
# }
# 
# bgReTaggingOrder = {
#     "tautau" : 0,
#     "sc" : 2,
#     "tc" : 3,
#     "nbody" : 4,
#     "fake" : 5,
#     #"ff" : 1
# }



plot_kind = "MET"

plot_signal = True
plot_rand = False
plot_fast = True
plot_title = True
plot_overflow = False
plot_significance = False
plot_error = False

plot_sc = False
plot_data = False
plot_ratio = False

create_canvas = False

plot_custom_ratio = False
#cutomRatios = [  [["DiBoson"],["TTJets"]],  [["WJetsToLNu"],["ZJetsToNuNu"]]  ]
cutomRatios = [  [["tc_btag_veto"],["tc_2_btags"]]  ]

choose_bg_files = False
choose_bg_files_list = ["TTJets"]
#choose_bg_files_list = ["WJetsToLNu"]

choose_bg_files_for_sc = True

ignore_bg_files = ["TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root", "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"]
#ignore_bg_files = []

blind_data = True

plot_log_x = False
plot_real_log_x = False

logXplots = ["invMass"]

#if plot_sc:
#    plot_signal = False

#if not plot_data:
#    plot_ratio = False

if args.output_file:
    output_file = args.output_file[0]
else:
    output_file = "obs.pdf"
    
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

histograms_defs = [
    #Z PEAK
#     { "obs" : "invMass", "minX" : 91.19 - 10.0, "maxX" : 91.19 + 10.0, "bins" : 30 },
#     { "obs" : "Met", "minX" : 0, "maxX" : 200, "bins" : 200 },
#     { "obs" : "Mht", "minX" : 0, "maxX" : 200, "bins" : 200 },
#     { "obs" : "Ht", "minX" : 0, "maxX" : 200, "bins" : 200 },    
#     { "obs" : "Mt2", "minX" : 0, "maxX" : 100, "bins" : 200 },
#     { "obs" : "Muons[0].Pt()", "minX" : 0, "maxX" : 300, "bins" : 300 },
#     { "obs" : "NJets", "minX" : 0, "maxX" : 7, "bins" : 7 },
    
    
    #DY
    #{ "obs" : "DYMuonsInvMass", "minX" : 0, "maxX" : 150, "bins" : 30, "units" : "GeV" },
    #{ "obs" : "DYMuons[0].Pt()", "minX" : 30, "maxX" : 100, "bins" : 30 },
    #{ "obs" : "DYMuons[1].Pt()", "minX" : 15, "maxX" : 100, "bins" : 30 },
    
    #NORMAL
    { "obs" : "invMass", "units" : "M_{ll}", "minX" : 0.1, "maxX" : 13, "bins" : 30 },
    { "obs" : 'int(leptonFlavour == "Muons")', "minX" : 0, "maxX" : 2, "bins" : 2},
    #{ "obs" : "dilepBDT", "minX" : -1, "maxX" : 1, "bins" : 30 },
    { "obs" : "dilepBDT", "units" : "BDT output", "minX" : 0.1, "maxX" : 0.8, "bins" : 30 },
    { "obs" : "Electrons.Pt()", "minX" : 0, "maxX" : 50, "bins" : 50 },
    { "obs" : "Muons.Pt()", "minX" : 0, "maxX" : 50, "bins" : 50 },
    { "obs" : "dileptonPt", "minX" : 0, "maxX" : 100, "bins" : 30 },
    { "obs" : "deltaPhi", "minX" : 0, "maxX" : 3.2, "bins" : 30 },
    { "obs" : "deltaEta", "minX" : 0, "maxX" : 4, "bins" : 30 },
    { "obs" : "deltaR", "minX" : 0, "maxX" : 4, "bins" : 30 },
    { "obs" : "pt3", "minX" : 0, "maxX" : 1000, "bins" : 30 },
    { "obs" : "Ht", "minX" : 0, "maxX" : 700, "bins" : 30 },
    { "obs" : "mtautau", "minX" : 0, "maxX" : 200, "bins" : 30 },
    { "obs" : "mt1", "minX" : 0, "maxX" : 200, "bins" : 30 },
    { "obs" : "mt2", "minX" : 0, "maxX" : 200, "bins" : 30 },
    { "obs" : "DeltaEtaLeadingJetDilepton", "minX" : 0, "maxX" : 4, "bins" : 30 },
    { "obs" : "DeltaPhiLeadingJetDilepton", "minX" : 0, "maxX" : 4, "bins" : 30 },
    { "obs" : "dilepHt", "minX" : 0, "maxX" : 400, "bins" : 30 },
    { "obs" : "NJets", "minX" : 0, "maxX" : 7, "bins" : 7 },
    { "obs" : "BTagsLoose", "minX" : 0, "maxX" : 7, "bins" : 7 },
    { "obs" : "BTagsMedium", "minX" : 0, "maxX" : 7, "bins" : 7 },
    { "obs" : "BTagsDeepLoose", "minX" : 0, "maxX" : 7, "bins" : 7 },
    { "obs" : "BTagsDeepMedium", "minX" : 0, "maxX" : 7, "bins" : 7 },
    
     { "obs" : "Met", "minX" : 120, "maxX" : 2000, "bins" : 30 },
     { "obs" : "Mht", "minX" : 0, "maxX" : 700, "bins" : 30 },
     { "obs" : "Ht", "minX" : 0, "maxX" : 700, "bins" : 30 },
     { "obs" : "LeadingJetQgLikelihood", "minX" : 0, "maxX" : 1, "bins" : 30 },
     { "obs" : "MinDeltaPhiMhtJets", "minX" : 0, "maxX" : 4, "bins" : 30 },
     { "obs" : "MinDeltaPhiMetJets", "minX" : 0, "maxX" : 4, "bins" : 30 },
     { "obs" : "Mt2", "minX" : 0, "maxX" : 100, "bins" : 30 },
     { "obs" : "LeadingJetPt", "minX" : 0, "maxX" : 800, "bins" : 30 },
     { "obs" : "abs(LeadingJet.Eta())", "minX" : 0, "maxX" : 4, "bins" : 30 },
     { "obs" : "MaxCsv25", "minX" : 0, "maxX" : 1, "bins" : 30 },
     { "obs" : "MaxDeepCsv25", "minX" : 0, "maxX" : 1, "bins" : 30 },
     { "obs" : "LeadingJetMinDeltaRElectrons", "minX" : 0, "maxX" : 5, "bins" : 30 },
     { "obs" : "LeadingJetMinDeltaRMuons", "minX" : 0, "maxX" : 5, "bins" : 30 },
     
     { "obs" : 'int(vetoElectronsPassIso)', "minX" : 0, "maxX" : 2, "bins" : 2},
     { "obs" : 'int(vetoElectronsPassJetIso)', "minX" : 0, "maxX" : 2, "bins" : 2},
     { "obs" : 'int(vetoElectronsMediumID)', "minX" : 0, "maxX" : 2, "bins" : 2},
     { "obs" : 'int(vetoElectronsTightID)', "minX" : 0, "maxX" : 2, "bins" : 2},
     
     { "obs" : 'int(vetoMuonsPassIso)', "minX" : 0, "maxX" : 2, "bins" : 2},
     { "obs" : 'int(vetoMuonsPassJetIso)', "minX" : 0, "maxX" : 2, "bins" : 2},
     { "obs" : 'int(vetoMuonsMediumID)', "minX" : 0, "maxX" : 2, "bins" : 2},
     { "obs" : 'int(vetoMuonsTightID)', "minX" : 0, "maxX" : 2, "bins" : 2},


     #{ "obs" : "abs(leptonParentPdgId)", "minX" : 0, "maxX" : 30, "bins" : 30 },
     #{ "obs" : "abs(trackParentPdgId)", "minX" : 0, "maxX" : 30, "bins" : 30 },
#     
    
    #DILEPTON
    
    
    #{ "obs" : "mw", "minX" : 0, "maxX" : 150, "bins" : 50, "func" : mw },
    #{ "obs" : "invMass2", "minX" : 0, "maxX" : 15, "bins" : 90, "func" : mw2 },   
]

cuts = [ #{"name":"none", "title": "No Cuts", "condition" : "1"},
         #{"name":"MET", "title": "MET >= 150", "condition" : 'Met >= 150 && invMass < 12 && leptonFlavour == "Muons"'},
         #{"name":"dileptonPt", "title": "dileptonPt", "condition" : "Met >= 200 && invMass < 30 && dileptonPt < 30"},
         
         
]

if plot_2l:
    histograms_defs.extend([
    { "obs" : "leptons[0].Pt()", "minX" : 2, "maxX" : 30, "bins" : 60 },
    { "obs" : "leptons[1].Pt()", "minX" : 2, "maxX" : 30, "bins" : 60 },
    { "obs" : "abs(leptons[0].Eta())", "minX" : 0, "maxX" : 3, "bins" : 60 },
    { "obs" : "abs(leptons[1].Eta())", "minX" : 0, "maxX" : 3, "bins" : 60 },
    { "obs" : "deltaPhiMetLepton1", "minX" : 0, "maxX" : 3.5, "bins" : 30 },
    { "obs" : "deltaPhiMetLepton2", "minX" : 0, "maxX" : 3.5, "bins" : 30 },
    { "obs" : "leptons_ParentPdgId[0]", "minX" : 0, "maxX" : 40, "bins" : 40 },
    { "obs" : "leptons_ParentPdgId[1]", "minX" : 0, "maxX" : 40, "bins" : 40 },
    
    { "obs" : "Electrons_minDeltaRJets[leptonsIdx[0]]", "minX" : 0, "maxX" : 1, "bins" : 60 },
    { "obs" : "Electrons_minDeltaRJets[leptonsIdx[1]]", "minX" : 0, "maxX" : 1, "bins" : 60 },
    
    { "obs" : "Muons_minDeltaRJets[leptonsIdx[0]]", "minX" : 0, "maxX" : 1, "bins" : 60 },
    { "obs" : "Muons_minDeltaRJets[leptonsIdx[1]]", "minX" : 0, "maxX" : 1, "bins" : 60 },
    
    { "obs" : "Electrons_deltaRLJ[leptonsIdx[0]]", "minX" : 0, "maxX" : 1, "bins" : 60 },
    { "obs" : "Electrons_deltaRLJ[leptonsIdx[1]]", "minX" : 0, "maxX" : 1, "bins" : 60 },
    
    { "obs" : "Muons_deltaRLJ[leptonsIdx[0]]", "minX" : 0, "maxX" : 1, "bins" : 60 },
    { "obs" : "Muons_deltaRLJ[leptonsIdx[1]]", "minX" : 0, "maxX" : 1, "bins" : 60 },
    
    { "obs" : "Electrons_deltaEtaLJ[leptonsIdx[0]]", "minX" : 0, "maxX" : 1, "bins" : 60 },
    { "obs" : "Electrons_deltaEtaLJ[leptonsIdx[1]]", "minX" : 0, "maxX" : 1, "bins" : 60 },
    
    { "obs" : "Muons_deltaEtaLJ[leptonsIdx[0]]", "minX" : 0, "maxX" : 1, "bins" : 60 },
    { "obs" : "Muons_deltaEtaLJ[leptonsIdx[1]]", "minX" : 0, "maxX" : 1, "bins" : 60 },
    
    
    
    ])
    cuts.extend([
        #{"name":"invMass_Muons", "title": "invMass - Muons", "condition" : "Met >= 200 && invMass < 12  && invMass > 0.4 && leptonFlavour == \"Muons\""},
        #{"name":"invMass_Electrons", "title": "invMass - Electrons", "condition" : "Met >= 200 && invMass < 12  && invMass > 0.4 && leptonFlavour == \"Electrons\""},
        
        #{"name":"real", "title": "real", "condition" : "Met >= 200 && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && !(invMass > 0.95 && invMass < 1.06)"},
        
        #{"name":"dilepBDT", "title": "dilepBDT", "condition" : "Met >= 200 && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && !(invMass > 0.95 && invMass < 1.06) && dilepBDT > 0.1"},
        #{"name":"noBDT", "title": "noBDT", "condition" : "BTagsDeepMedium == 0 && (leptons[1].Pt() <= 3.5 || deltaR <= 0.3) && Mht >= 220 &&  Met >= 200 && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81)"},
        #{"name":"orthSOS", "title": "orthSOS", "condition" : "BTagsDeepMedium == 0 && (leptons[1].Pt() <= 3.5 || deltaR <= 0.3) && Mht >= 220 &&  Met >= 200 && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && dilepBDT > 0.1"},
        
        #{"name":"noBVeto_Electrons", "title": "noBVeto - Electrons", "condition" : "(leptons[1].Pt() <= 3.5 || deltaR <= 0.3) && Mht >= 220 &&  Met >= 200 && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && dilepBDT > 0.1 && vetoElectronsTightID == 0 && vetoMuonsPassJetIso == 0 && leptonFlavour == \"Electrons\""},
        #{"name":"noBVeto_Muons", "title": "noBVeto - Muons", "condition" : "(leptons[1].Pt() <= 3.5 || deltaR <= 0.3) && Mht >= 220 &&  Met >= 200 && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && dilepBDT > 0.1 && vetoElectronsTightID == 0 && vetoMuonsPassJetIso == 0 && leptonFlavour == \"Muons\""},
        
        
        #{"name":"orthSOS-no_veto_Electrons", "title": "orthSOS no lepton veto - Electrons", "condition" : "BTagsDeepMedium == 0 && (leptons[1].Pt() <= 3.5 || deltaR <= 0.3) && Mht >= 220 &&  Met >= 200 && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && dilepBDT > 0.1 && leptonFlavour == \"Electrons\""},
        #{"name":"orthSOS-no_veto_Muons", "title": "orthSOS no lepton veto - Muons", "condition" : "BTagsDeepMedium == 0 && (leptons[1].Pt() <= 3.5 || deltaR <= 0.3) && Mht >= 220 &&  Met >= 200 && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && dilepBDT > 0.1 && leptonFlavour == \"Muons\""},
        
        
        {"name":"orthSOS-veto_Electrons", "title": "orthSOS lepton veto - Electrons", "condition" : "vetoElectronsTightID == 0 && vetoMuonsPassIso == 0 && BTagsDeepMedium == 0 && (leptons[1].Pt() <= 3.5 || deltaR <= 0.3) && Mht >= 220 &&  Met >= 200 && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && dilepBDT > 0.1 && leptonFlavour == \"Electrons\""},
        {"name":"orthSOS-veto_Muons", "title": "orthSOS lepton veto - Muons", "condition" : "vetoElectronsTightID == 0 && vetoMuonsPassIso == 0 && BTagsDeepMedium == 0 && (leptons[1].Pt() <= 3.5 || deltaR <= 0.3) && Mht >= 220 &&  Met >= 200 && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && dilepBDT > 0.1 && leptonFlavour == \"Muons\""},
        
        {"name":"veto_Electrons", "title": "lepton veto - Electrons", "condition" : "vetoElectronsTightID == 0 && vetoMuonsPassIso == 0 && BTagsDeepMedium == 0 && Mht >= 220 &&  Met >= 200 && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && dilepBDT > 0.1 && leptonFlavour == \"Electrons\""},
        {"name":"veto_Muons", "title": "lepton veto - Muons", "condition" : "vetoElectronsTightID == 0 && vetoMuonsPassIso == 0 && BTagsDeepMedium == 0 && Mht >= 220 &&  Met >= 200 && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && dilepBDT > 0.1 && leptonFlavour == \"Muons\""},
        
        
        #{"name":"tc", "title": "tc", "condition" : 'Met >= 200 && invMass < 30 && leptonFlavour == "Muons" && tc * (!tautau)'},
        #{"name":"tautau", "title": "tautau", "condition" : '(Met >= 200 && invMass < 30 && leptonFlavour == "Muons") * (tautau)'},
        #{"name":"scother", "title": "scother", "condition" : 'Met >= 200 && invMass < 30 && leptonFlavour == "Muons" && sc * (!tautau) * (!omega) * (!rho_0) * (!eta) * (!phi) * (!eta_prime) * (!j_psi) * (!upsilon_1) * (!upsilon_2)'},
        
        # {"name":"dilepBDT", "title": "dilepBDT", "condition" : 'Met >= 200 && invMass < 30 && leptonFlavour == "Muons" && dilepBDT > 0.2'},
#         {"name":"lowMet", "title": "lowMet", "condition" : 'Met <= 200 && invMass < 30 && leptonFlavour == "Muons"'},
#         {"name":"lowMetBDT", "title": "lowMetBDT", "condition" : 'Met <= 200 && invMass < 30 && leptonFlavour == "Muons" && dilepBDT > 0'},
        
        
        # {"name":"parent_100-250", "title": "parent 100-250", "condition" : "Met >= 200 && invMass < 30 && leptons_ParentPdgId[0] > 100 && leptons_ParentPdgId[0] < 250"},
#         {"name":"parent_300-350", "title": "parent 300-350", "condition" : "Met >= 200 && invMass < 30 && leptons_ParentPdgId[0] > 300 && leptons_ParentPdgId[0] < 350"},
#         {"name":"parent_400-450", "title": "parent 400-450", "condition" : "Met >= 200 && invMass < 30 && leptons_ParentPdgId[0] > 400 && leptons_ParentPdgId[0] < 450"},
#          {"name":"parent_500-600", "title": "parent 500-600", "condition" : "Met >= 200 && invMass < 30 && leptons_ParentPdgId[0] > 500 && leptons_ParentPdgId[0] < 600"},
#          {"name":"parent_600", "title": "parent >600", "condition" : "Met >= 200 && invMass < 30 && leptons_ParentPdgId[0] > 600"},
#         
    ])
else:
    histograms_defs.extend([
    #     #TRACK ONLY
    { "obs" : "trackBDT", "minX" : -0.7, "maxX" : 0.7, "bins" : 30 },
    { "obs" : "secondTrackBDT", "minX" : -1, "maxX" : 1, "bins" : 30 },
    { "obs" : "abs(track.Eta())", "minX" : 0, "maxX" : 3, "bins" : 60 },
    { "obs" : "abs(lepton.Eta())", "minX" : 0, "maxX" : 3, "bins" : 60 },
    { "obs" : "track.Pt()", "minX" : 0, "maxX" : 30, "bins" : 60 },
    { "obs" : "lepton.Pt()", "minX" : 2, "maxX" : 25, "bins" : 60 },
    { "obs" : "secondTrack.Pt()", "minX" : 0, "maxX" : 30, "bins" : 60 },
    { "obs" : "abs(secondTrack.Eta())", "minX" : 0, "maxX" : 3, "bins" : 60 },
    { "obs" : "abs(track.Phi())", "minX" : 0, "maxX" : 6, "bins" : 60 },
    { "obs" : "abs(lepton.Phi())", "minX" : 0, "maxX" : 6, "bins" : 60 },
    { "obs" : "mtl", "minX" : 0, "maxX" : 200, "bins" : 30 },
    { "obs" : "mtt", "minX" : 0, "maxX" : 200, "bins" : 30 },
    { "obs" : "NTracks", "minX" : 0, "maxX" : 7, "bins" : 7 },
    ])
    cuts.extend([
        {"name":"dilepBDT", "title": "dilepBDT", "condition" : "secondTrack.Pt() < 12 && lepton.Pt() < 18 && track.Pt() < 15 && abs(lepton.Eta()) < 2.4 && deltaEta < 2.5 && mt1 < 120 && dilepHt > 130 && deltaR > 0.25 &&  deltaR < 3 && dilepBDT > 0.1 && Met >= 200 && invMass < 30 && dileptonPt < 30"},
    ])

histograms_defs = []
cuts = [{"name":"none", "title": "No Cuts", "condition" : "vetoElectronsTightID == 0 && vetoMuonsPassIso == 0 && BTagsDeepMedium == 0 && Mht >= 220 &&  Met >= 200"}
]

#for lep in ["Electrons", "Muons"]:
for iso in utils.leptonIsolationList:
    for cat in utils.leptonIsolationCategories:
        ptRanges = [""]
        if iso == "CorrJetIso":
            ptRanges = utils.leptonCorrJetIsoPtRange
        for ptRange in ptRanges:
            for prefix in ["", "exTrack_"]:
                for lep in ["Muons", "Electrons"]:
                    cond = ""
                    if prefix == "":
                        cond = "twoLeptons"  + iso + str(ptRange) + cat + "== 1 && @leptons"  + iso + str(ptRange) + cat + ".size() == 2 && leptonFlavour" + iso + str(ptRange) + cat + ' == "' + lep + '"'
                    else:
                        cond = "exclusiveTrack"  + iso + str(ptRange) + cat + "== 1  && exclusiveTrackLeptonFlavour" + iso + str(ptRange) + cat + ' == "' + lep + '"'
                        histograms_defs.append({ "obs" : "trackBDT" + iso + str(ptRange) + cat, "namePostfix" : lep, "units": lep + "_trackBDT" + iso + str(ptRange) + cat,  "minX" : -1, "maxX" : 1, "bins" : 30, "cond": cond})
                    
                    histograms_defs.append({ "obs" : prefix + "dilepBDT" + iso + str(ptRange) + cat, "namePostfix" : lep, "units": lep + "_" + prefix + "dilepBDT" + iso + str(ptRange) + cat, "minX" : -1, "maxX" : 1, "bins" : 30, "cond" : cond})
                    histograms_defs.append({ "obs" : prefix + "invMass" + iso + str(ptRange) + cat, "namePostfix" : lep, "units": lep + "_" + prefix + "invMass" + iso + str(ptRange) + cat,"minX" : 0, "maxX" : 12, "bins" : 30, "cond" : cond})
                    histograms_defs.append({ "obs" : prefix + "invMass" + iso + str(ptRange) + cat + " ", "namePostfix" : lep, "units": lep + "_" + prefix + "invMass" + iso + str(ptRange) + cat + "_cut","minX" : 0, "maxX" : 12, "bins" : 30, "cond" : cond + " && " + prefix + "dilepBDT" + iso + str(ptRange) + cat + " > 0.2"})
                    if "LowPt" in cat:
                        if prefix == "exTrack_":
                            cond += " && " + "lepton" + iso + str(ptRange) + cat + ".Pt() < 2"
                        else:
                            cond += " && " + "leptons" + iso + str(ptRange) + cat + "[1].Pt() < 2"
                        histograms_defs.append({ "obs" : prefix + "dilepBDT" + iso + str(ptRange) + cat, "namePostfix" : lep + "Low", "units": lep + "_low_" + prefix + "dilepBDT" + iso + str(ptRange) + cat, "minX" : -1, "maxX" : 1, "bins" : 30, "cond" : cond})
                        histograms_defs.append({ "obs" : prefix + "invMass" + iso + str(ptRange) + cat, "namePostfix" : lep + "Low", "units": lep + "_low_" + prefix + "invMass" + iso + str(ptRange) + cat,"minX" : 0, "maxX" : 12, "bins" : 30, "cond" : cond})
                        histograms_defs.append({ "obs" : prefix + "invMass" + iso + str(ptRange) + cat + " ", "namePostfix" : lep + "Low", "units": lep + "_low_" + prefix + "invMass" + iso + str(ptRange) + cat + "_cut","minX" : 0, "maxX" : 12, "bins" : 30, "cond" : cond + " && " + prefix + "dilepBDT" + iso + str(ptRange) + cat + " > 0.2"})
                        
                    


def styleHist(hist, onlyY = False):
    hist.GetYaxis().SetTitleSize(10);
    hist.GetYaxis().SetTitleFont(43);
    hist.GetYaxis().SetTitleOffset(2.5);
    hist.GetYaxis().SetLabelFont(43); 
    hist.GetYaxis().SetLabelSize(10);
    
    if not onlyY:
        hist.GetXaxis().SetTitleSize(10);
        hist.GetXaxis().SetTitleFont(43);
        hist.GetXaxis().SetTitleOffset(8);
        hist.GetXaxis().SetLabelFont(43); 
        hist.GetXaxis().SetLabelSize(10);

def createPlots(rootfiles, type, histograms, weight=1):
    print("Processing ")
    print(rootfiles)
    lumiSecs = LumiSectMap()
    
    for f in rootfiles:
        print(f)
        if os.path.basename(f) in ignore_bg_files:
            print("File", f, "in ignore list. Skipping...")
            continue
        rootFile = TFile(f)
        c = rootFile.Get('tEvent')
        if type == "data":
            lumis = rootFile.Get('lumiSecs')
            col = TList()
            col.Add(lumis)
            lumiSecs.Merge(col)
        nentries = c.GetEntries()
        print('Analysing', nentries, "entries")
        for ientry in range(nentries):
            if ientry % 10000 == 0:
                print("Processing " + str(ientry))
            c.GetEntry(ientry)
            
            for cut in cuts:
                passed = True
                if cut.get("funcs") is not None:
                    for func in cut["funcs"]:
                        passed = func(c)
                        if not passed:
                            break
                if not passed:
                    continue
                
                for hist_def in histograms_defs:
                    histName =  cut["name"] + "_" + hist_def["obs"] + "_" + type
                    if hist_def.get("namePostfix"):
                        histName += hist_def["namePostfix"]
                    
                    hist = histograms[histName]
                    if type != "data":
                        #print("Weight=", c.Weight)
                        #print("weight=", weight)
                        if hist_def.get("func") is not None:
                            hist.Fill(hist_def["func"](c), c.Weight * weight)
                        else:
                            hist.Fill(eval('c.' + hist_def["obs"]), c.Weight * weight)
                    else:
                        hist.Fill(eval('c.' + hist_def["obs"]), 1)
        rootFile.Close()
    
    if type == "data":
        if calculatedLumi.get('MET') is not None:
            print("Found lumi=" + str(calculatedLumi['MET']))
            return calculatedLumi['MET']
        else:
            return utils.calculateLumiFromLumiSecs(lumiSecs)
        #return 3.939170474
        #return 35.574589421
        #return 35.493718415
        #return 27.360953311
        return 27.677964176


def createPlotsFast(rootfiles, type, histograms, weight=1, prefix=""):
    print("Processing ")
    print(rootfiles)
    lumiSecs = LumiSectMap()
    
    for f in rootfiles:
        print(f)
        if os.path.basename(f) in ignore_bg_files:
            print("File", f, "in ignore list. Skipping...")
            continue
        rootFile = TFile(f)
        c = rootFile.Get('tEvent')
        c.Show(0)
        if type == "data":
            lumis = rootFile.Get('lumiSecs')
            col = TList()
            col.Add(lumis)
            lumiSecs.Merge(col)
        
        for cut in cuts:
            for hist_def in histograms_defs:
                if prefix != "":
                    histName =  prefix + "_" + cut["name"] + "_" + hist_def["obs"] + "_" + type
                    if hist_def.get("namePostfix"):
                        histName += hist_def["namePostfix"]
                else:
                    histName =  cut["name"] + "_" + hist_def["obs"] + "_" + type
                    if hist_def.get("namePostfix"):
                        histName += hist_def["namePostfix"]
                #if type != "data" and type != "signal":
                #    hist = utils.getHistogramFromTree(histName, c, hist_def["obs"], hist_def["bins"], hist_def["minX"], hist_def["maxX"], "puWeight * (" + cut["condition"] + ")")
                #else:
                condition = cut["condition"]
                if hist_def.get("cond") is not None:
                    condition += " && " + hist_def["cond"]
                if type != "data":
                    drawString = weightString[plot_kind] + " * " + str(weight) + "* Weight * (" + condition + ")"
                    #print("drawString=" + drawString)
                    if plot_log_x and hist_def["obs"] == "invMass":
                        hist = utils.getRealLogxHistogramFromTree(histName, c, hist_def.get("obs"), hist_def.get("bins"), hist_def.get("minX"), hist_def.get("maxX"), drawString, plot_overflow)
                    else:
                        hist = utils.getHistogramFromTree(histName, c, hist_def.get("obs"), hist_def.get("bins"), hist_def.get("minX"), hist_def.get("maxX"), drawString, plot_overflow)
                else:
                    if plot_log_x and hist_def["obs"] == "invMass":
                        hist = utils.getRealLogxHistogramFromTree(histName, c, hist_def.get("obs"), hist_def.get("bins"), hist_def.get("minX"), hist_def.get("maxX"), weightString[plot_kind] + " * (" +condition + ")", plot_overflow)
                    else:
                        hist = utils.getHistogramFromTree(histName, c, hist_def.get("obs"), hist_def.get("bins"), hist_def.get("minX"), hist_def.get("maxX"), weightString[plot_kind] + " * (" + condition + ")", plot_overflow)
                if hist is None:
                    continue
                #if "leptonF" in histName:
                #    print("Made leptonFlavour for", histName, hist.GetXaxis().GetNbins())
                hist.GetXaxis().SetTitle("")
                hist.SetTitle("")
                hist.Sumw2()
                #if type != "data":
                #    c.GetEntry(0)
                #    hist.Scale(c.Weight * weight)
                if histograms.get(histName) is None:
                    histograms[histName] = hist
                else:
                    histograms[histName].Add(hist)
        
        rootFile.Close()
    
    if type == "data":
        return calculatedLumi.get(plot_kind)
        #return calculatedLumi.get('SingleMuon')
        
        if calculatedLumi.get('MET') is not None:
            print("Found lumi=" + str(calculatedLumi['MET']))
            return calculatedLumi['MET']
        else:
            return utils.calculateLumiFromLumiSecs(lumiSecs)
        #Z PEAK
        #return 27.677786572
        #Norman
        return 35.579533154
        #return utils.calculateLumiFromLumiSecs(lumiSecs)

def createRandomHist(name):
    h = utils.UOFlowTH1F(name, "", 100, -5, 5)
    h.Sumw2()
    h.FillRandom("gaus")
    styleHist(h)
    return h
    
def createCRPads(pId, ratioPads, twoRations = False):
    print("Creating pads for id", pId)

    histLowY = 0.21
    if twoRations:
        histLowY = 0.31
    histCPad = TPad("pad" + str(pId),"pad" + str(pId),0,histLowY,1,1)
    if twoRations:
        histRPad = TPad("rpad" + str(pId),"rpad" + str(pId),0,0,1,0.15)
        histR2Pad = TPad("r2pad" + str(pId),"r2pad" + str(pId),0,0.15,1,0.3)
    else:
        histRPad = TPad("rpad" + str(pId),"rpad" + str(pId),0,0,1,0.2)
    ratioPads[pId] = []
    ratioPads[pId].append(histCPad)
    ratioPads[pId].append(histRPad)
    if twoRations:
        histR2Pad.SetBottomMargin(0.2)
        ratioPads[pId].append(histR2Pad)
        histRPad.SetTopMargin(0)
    histCPad.SetBottomMargin(0)
    if not twoRations:
        histRPad.SetTopMargin(0.05)
    histRPad.SetBottomMargin(0.3)
    #if twoRations:
    #    histR2Pad.SetTopMargin(0.05)
    #    histR2Pad.SetBottomMargin(0.25)
    histRPad.Draw()
    histCPad.Draw()
    if twoRations:
        histR2Pad.Draw()
    if twoRations:
        return histCPad, histRPad, histR2Pad
    return histCPad, histRPad

def plotRatio(c1, pad, memory, dataHist, newBgHist, hist_def, title = "Data / BG",setTitle = True):
    print("Plotting ratio!")

    pad.cd()
    pad.SetGridx()
    pad.SetGridy()
    rdataHist = dataHist.Clone()
    memory.append(rdataHist)
    rdataHist.Divide(newBgHist)
    rdataHist.SetMinimum(-0.5)
    rdataHist.SetMaximum(3.5)
    if setTitle:
        rdataHist.GetXaxis().SetTitle(hist_def["obs"])
    else:
        rdataHist.GetXaxis().SetTitle("")
    rdataHist.GetYaxis().SetTitle(title)
    if setTitle:
        styleHist(rdataHist)
    else:
        styleHist(rdataHist, True)
    rdataHist.GetYaxis().SetNdivisions(505)
    rdataHist.Draw("p")
    rdataHist.Draw("same e0")
    line = TLine(rdataHist.GetXaxis().GetXmin(),1,rdataHist.GetXaxis().GetXmax(),1);
    line.SetLineColor(kRed);
    line.Draw("SAME");
    memory.append(line)
    c1.Modified()

def createAllHistograms(histograms, sumTypes):
    
    foundReqObs = False
    foundReqCut = False
    
    global cuts
    global histograms_defs
    global plot_title
    
    if plot_single:
        plot_title = False
        for obs in histograms_defs:
            if obs["obs"] == req_obs:
                foundReqObs = True
                histograms_defs = [obs]
                break
        if not foundReqObs:
            print("Could not find obs " + req_obs)
            exit(0)
        for cut in cuts:
            if cut["name"] == req_cut:
                foundReqCut = True
                cuts = [cut]
                break
        if not foundReqCut:
            print("Could not find cut " + req_cut)
            exit(0)
            
    if not plot_rand:
        c2 = TCanvas("c2")
        c2.cd()
        if bg_retag:
            for type in bgReTagging:
                sumTypes[type] = {}
        else:
            bg_files = glob(bg_dir + "/*")
        
            for f in bg_files: 
                filename = os.path.basename(f).split(".")[0]
                types = filename.split("_")
                type = None
            
                #if types[0] == "WJetsToLNu" or types[0] == "ZJetsToNuNu":
                #    continue
            
                if types[0] == "TTJets":
                    type = "_".join(types[0:2])
                elif types[0] == "ST":
                    type = "_".join(types[0:3])
                else:
                    type = types[0]
                if type not in sumTypes:
                    sumTypes[type] = {}
                #sumTypes[types[0]][types[1]] = True

        print(sumTypes)
        
        if not plot_fast:
            print("NOT PLOTTING FAST")
            for cut in cuts:
                    for hist_def in histograms_defs:
                        baseName = cut["name"] + "_" + hist_def["obs"]
                        if hist_def.get("namePostfix"):
                            baseName += hist_def["namePostfix"]
                        sigName = baseName + "_signal"
                        dataName = baseName + "_data"
                        histograms[sigName] = utils.UOFlowTH1F(sigName, "", hist_def["bins"], hist_def["minX"], hist_def["maxX"])
                        histograms[dataName] = utils.UOFlowTH1F(dataName, "", hist_def["bins"], hist_def["minX"], hist_def["maxX"])
                        utils.formatHist(histograms[sigName], utils.signalCp[0], 0.8)
                        for type in sumTypes:
                            if utils.existsInCoumpoundType(type):
                                continue
                            bgName = baseName + "_" + type
                            histograms[bgName] = utils.UOFlowTH1F(bgName, "", hist_def["bins"], hist_def["minX"], hist_def["maxX"])
                        for type in utils.compoundTypes:
                            bgName = baseName + "_" + type
                            histograms[bgName] = utils.UOFlowTH1F(bgName, "", hist_def["bins"], hist_def["minX"], hist_def["maxX"])
    
        calculated_lumi = None
        weight=0
        if plot_data:
            dataFiles = glob(data_dir + "/*")
            if plot_fast:
                calculated_lumi = createPlotsFast(dataFiles, "data", histograms)
            else:
                calculated_lumi = createPlots(dataFiles, "data", histograms)
            print("Calculated Luminosity: ", calculated_lumi)
            weight = calculated_lumi * 1000
        else:
            print("HERE")
            weight = utils.LUMINOSITY
        
        if plot_data and plot_sc:
            print("CREATING SC CATEGORY!")
            dataFiles = glob(sc_data_dir + "/*")
            createPlotsFast(dataFiles, "data", histograms, 1, "sc")
    
        if plot_signal:
            if plot_fast:
                print("Plotting Signal Fast")
                for signalFile in signal_dir:
                    signalBasename = os.path.basename(signalFile)
                    createPlotsFast([signalFile], signalBasename, histograms, weight)
            else:
                for signalFile in signal_dir:
                    signalBasename = os.path.basename(signalFile)
                    createPlots([signalFile], signalBasename, histograms, weight)
        allBgFiles = glob(bg_dir + "/*.root")
        for type in sumTypes:
            if bg_retag:
                bgFilesToPlot = []
                if choose_bg_files:
                    print("In choose_bg_files")
                    for bgChooseType in choose_bg_files_list:
                        if utils.isCoumpoundType(bgChooseType):
                            print("Compound", bgChooseType)
                            bgFilesToPlot.extend(utils.getFilesForCompoundType(bgChooseType, bg_dir))
                            print(bgFilesToPlot)
                        else:
                            print("Not in compound", bgChooseType)
                            bgFilesToPlot.extend(glob(bg_dir + "/*" + bgChooseType + "_*.root"))
                else:
                    bgFilesToPlot = allBgFiles
                
                print("Summing type", type)

                if plot_fast:
                    createPlotsFast(bgFilesToPlot, type, histograms, str(weight) + " * " + bgReTagging[type])
                else:
                    createPlots(bgFilesToPlot, type, histograms, str(weight) + " * " + bgReTagging[type])
            else:
                if utils.existsInCoumpoundType(type):
                    continue
                #if type == "ZJetsToNuNu" or type == "WJetsToLNu":
                #    continue
                if choose_bg_files and type not in choose_bg_files_list:
                    print("Skipping type", type, "because not in chosen list")
                    continue
                print("Summing type", type)
                rootfiles = glob(bg_dir + "/*" + type + "_*.root")
                if plot_fast:
                    createPlotsFast(rootfiles, type, histograms, weight)
                else:
                    createPlots(rootfiles, type, histograms, weight)
        if not bg_retag:
            for cType in utils.compoundTypes:
                
                if choose_bg_files and cType not in choose_bg_files_list:
                    print("Skipping cType", cType, "because not in chosen list")
                    continue
                
                print("Creating compound type", cType)
                
                rootFiles = utils.getFilesForCompoundType(cType, bg_dir)
                if len(rootFiles):
                    if plot_fast:
                        createPlotsFast(rootFiles, cType, histograms, weight)
                    else:
                        createPlots(rootFiles, cType, histograms, weight)
                else:
                    print("**Couldn't find file for " + cType)
        
        if plot_sc:
            print("CREATING SC CATEGORY!")
            
            bgFilesToPlot = []
            if choose_bg_files and choose_bg_files_for_sc:
                for bgChooseType in choose_bg_files_list:
                    if utils.isCoumpoundType(bgChooseType):
                        print(bgChooseType, "is a compound type!")
                        bgFilesToPlot.extend(utils.getFilesForCompoundType(bgChooseType, sc_bg_dir))
                    else:
                        bgFilesToPlot.extend(glob(sc_bg_dir + "/*" + bgChooseType + "_*.root"))
            else:
                bgFilesToPlot = glob(sc_bg_dir + "/*")

            createPlotsFast(bgFilesToPlot, "bg", histograms, weight, "sc")
        
        if plot_data and blind_data and plot_signal:
            for cut in cuts:
                for hist_def in histograms_defs:
                    firstSignalName = os.path.basename(signal_dir[0])
                    signal_hist_name = cut["name"] + "_" + hist_def["obs"] + "_" + firstSignalName
                    if hist_def.get("namePostfix"):
                        signal_hist_name += hist_def["namePostfix"]
                    signal_hist = histograms[signal_hist_name]
                    
                    prefixes = [""]
                    #if plot_sc:
                    #    prefixes.append("sc")
                    for prefix in prefixes:
                        histName = None
                        if prefix != "":
                            histName =  prefix + "_" + cut["name"] + "_" + hist_def["obs"] + "_data"
                        else:
                            histName =  cut["name"] + "_" + hist_def["obs"] + "_data"
                        if hist_def.get("namePostfix"):
                            histName += hist_def["namePostfix"]
                        data_hist = histograms[histName]
                        
                        bg_hist = None
                        
                        types = []
                        if bg_retag:
                            types = [k for k in bgReTagging]
                            types = sorted(types, key=lambda a: bgReTaggingOrder[a])
                        else:
                            types = [k for k in utils.bgOrder]
                            types = sorted(types, key=lambda a: utils.bgOrder[a])
                        for type in types:
                            hname = cut["name"] + "_" + hist_def["obs"] + "_" + type
                            if hist_def.get("namePostfix"):
                                hname += hist_def["namePostfix"]
                            if histograms.get(hname) is not None:
                                if bg_hist is None:
                                    bg_hist = histograms[hname].Clone()
                                else:
                                    bg_hist.Add(histograms[hname])

                        for i in range(1,data_hist.GetNbinsX() + 1):
                            data_num = data_hist.GetBinContent(i)
                            signal_num = signal_hist.GetBinContent(i)
                            bg_num = bg_hist.GetBinContent(i)
                            if data_num == 0:
                                continue
                            if bg_num == 0:
                                data_hist.SetBinContent(i, 0)
                                continue
                            if ((0.1 * signal_num / math.sqrt(bg_num)) > 0.1):
                                print("Blinding bin", i, "for", histName)
                                data_hist.SetBinContent(i, 0)

def main():
    print("Start: " + datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    
    #deltaM = utils.getDmFromFileName(signal_dir[0])
    #print("deltaM=" + deltaM)

    histograms = {}
    sumTypes = {}
    
    errorStr = ""
    if plot_error:
        errorStr = "e"
    
    createAllHistograms(histograms, sumTypes)

    print("Plotting observable")

    c1 = TCanvas("c1", "c1", 800, 800)
    
    if plot_single:
        c1.SetBottomMargin(0.16)
        c1.SetLeftMargin(0.18)
    
    c1.cd()
    
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
    
    canvasFile = None
    if create_canvas:
        canvasFile = TFile("canvas_" + output_file.split(".")[0] + ".root", "recreate")
    
    c1.Print(output_file+"[");

    plot_num = 0

    pId = 1
    needToDraw = False

    memory = []
    
    ratioPads = {}
    
    for cut in cuts:
        
        sigNum = 0
        bgNum = 0
        
        cutName = cut["name"]
        print("Cut " + cutName)
        if plot_title:
            t.Clear()
            t.AddText(cut["title"])
            t.Draw()
            titlePad.Update()
        pId = 1
        for hist_def in histograms_defs:
            
            needToDraw = True
            pad = None
            if plot_single:
                pad = histPad.cd()
            else:
                pad = histPad.cd(pId)
            histCPad = None
            histRPad = None
            histR2Pad = None
            if plot_ratio or plot_custom_ratio > 0:
                if ratioPads.get(pId) is None:
                    if (plot_sc and plot_data) or plot_custom_ratio > 1:
                        histCPad, histRPad, histR2Pad = createCRPads(pId, ratioPads, True)
                    else:
                        histCPad, histRPad = createCRPads(pId, ratioPads)
                else:
                    histCPad = ratioPads[pId][0]
                    histRPad = ratioPads[pId][1]
                    if (plot_sc and plot_data) or plot_custom_ratio > 1:
                        histR2Pad = ratioPads[pId][2]
                pad = histCPad
                pad.cd()
            
            #print("*", ratioPads)
            #print(histCPad, histRPad)
            #exit(0)
            hs = THStack(str(plot_num),"")
            plot_num += 1
            memory.append(hs)
            types = []
            if bg_retag:
                types = [k for k in bgReTagging]
                types = sorted(types, key=lambda a: bgReTaggingOrder[a])
            else:
                types = [k for k in utils.bgOrder]
                types = sorted(types, key=lambda a: utils.bgOrder[a])
            typesInx = []
            i = 0
            foundBg = False

            for type in types:
                hname = cut["name"] + "_" + hist_def["obs"] + "_" + type
                if hist_def.get("namePostfix"):
                    hname += hist_def["namePostfix"]
                if plot_rand:
                    histograms[hname] = createRandomHist(hname)
                if histograms.get(hname) is not None:
                    hs.Add(histograms[hname])
                    typesInx.append(i)
                    foundBg = True
                i += 1
            
            dataHistName = cut["name"] + "_" + hist_def["obs"] + "_data"
            if hist_def.get("namePostfix"):
                dataHistName += hist_def["namePostfix"]
            if plot_rand:
                histograms[dataHistName] = createRandomHist(dataHistName)
            
            dataHist = None
            sigHists = []
            sigHistsBaseNames = []
            sigHistsNames = []
            sigMax = 0
            if plot_signal: 
                for i in range(len(signal_dir)):
                    signalFile = signal_dir[i]
                    signalBasename = os.path.basename(signalFile)
                    sigHistsBaseNames.append(signalBasename.split(".")[0].split("_")[-1])
                    sigHistName = cut["name"] + "_" + hist_def["obs"] + "_" + signalBasename
                    if hist_def.get("namePostfix"):
                        sigHistName += hist_def["namePostfix"]
                    sigHistsNames.append(sigHistName)
                    sigHist = histograms[sigHistName]
                    print(sigHistName, sigHist.GetMaximum())
                    sigHists.append(sigHist)
                    utils.formatHist(sigHist, utils.signalCp[i], 0.8)
                    sigMax = max(sigHist.GetMaximum(), sigMax)
            maximum = sigMax
            if foundBg:
                bgMax = hs.GetMaximum()
                print("Bg coung:", bgMax)
                maximum = max(bgMax, sigMax)
            if plot_data:
                dataHist = histograms[dataHistName]
                dataHist.SetMinimum(0.01)
                dataHist.SetMarkerStyle(kFullCircle)
                dataHist.SetMarkerSize(0.5)
                dataMax = dataHist.GetMaximum()
                maximum = max(dataMax, maximum)
            
            if maximum == 0:
                maximum == 10
            
            legend = TLegend(.20,.60,.89,.89)
            legend.SetNColumns(2)
            legend.SetBorderSize(0)
            legend.SetFillStyle(0)
            newBgHist = None
            memory.append(legend)
            
            if foundBg:
                newBgHist = utils.styledStackFromStack(hs, memory, legend, "", typesInx, True)
                #newBgHist.SetFillColorAlpha(fillC, 0.35)
                newBgHist.SetMaximum(maximum*1000)
                newBgHist.SetMinimum(0.01)
                newBgHist.Draw("hist" + errorStr)
                
                if plot_single:
                    utils.histoStyler(newBgHist)
                if not plot_ratio:
                    if plot_single:
                        newBgHist.GetXaxis().SetTitle(hist_def["units"] if hist_def.get("units") is not None else "GeV")#hist_def["obs"])
                    else:
                        if newBgHist is not None and newBgHist.GetNhists() > 0:
                            print(hist_def)
                            print(newBgHist)
                            print(newBgHist.GetXaxis())
                            newBgHist.GetXaxis().SetTitle(hist_def["units"] if hist_def.get("units") is not None else hist_def["obs"])
                if newBgHist.GetHists() is not None and newBgHist.GetNhists() > 0:
                    newBgHist.GetYaxis().SetTitle("Number of events")
                if plot_single:
                    if newBgHist.GetHists() is not None and newBgHist.GetNhists() > 0:
                        newBgHist.GetYaxis().SetTitleOffset(1.15)

                #newBgHist.GetXaxis().SetLabelSize(0.055)
                c1.Modified()
            
            if plot_signal:
                for i in range(len(sigHists)):
                    legend.AddEntry(sigHists[i], sigHistsBaseNames[i], 'l')
            if foundBg and plot_signal:
                for i in range(len(sigHists)):
                    sigHists[i].SetMaximum(maximum)
            if plot_signal:
                for i in range(len(sigHists)):
                    sigHists[i].SetMinimum(0.01)
                    sigHists[i].SetLineWidth(2)
            if foundBg and plot_signal:
                for i in range(len(sigHists)):
                    sigHists[i].Draw("HIST SAME " + errorStr)
            elif plot_signal:
                for i in range(len(sigHists)):
                    sigHists[i].Draw("HIST" + errorStr)
            
            if plot_significance and hist_def["obs"] == "invMass":
                accBgHist = None
                for bgHist in newBgHist.GetHists():
                    if accBgHist is None:
                        accBgHist = bgHist.Clone()
                    else:
                        accBgHist.Add(bgHist)
                significance = utils.calcSignificance(sigHists[0], accBgHist)
                # sigNum = sigHist.Integral(1, sigHist.FindBin(8))
#                 bgNum = 0
#                 for bgHist in newBgHist.GetHists():
#                     bgNum += bgHist.Integral(1, bgHist.FindBin(8))
#                 significance = 0.1*sigNum/math.sqrt(bgNum)
                print("cutName ", cutName, "sig", significance)
                if not plot_single and plot_significance:
                    pt = TPaveText(.60,.1,.95,.2, "NDC")
                    pt.SetFillColor(0)
                    pt.SetTextAlign(11)
                    pt.SetBorderSize(0)
                    memory.append(pt)
                    pt.AddText("sigNum=" + str(sigNum))
                    pt.AddText("bgNum=" + str(bgNum))
                    pt.AddText("sig=" + str(significance))
                    pt.Draw()
                
            
            if plot_data:
                dataHist.Draw("P SAME")
                legend.AddEntry(dataHist, "data", 'p')
            
            scDataHist = None
            scBgHist = None
            if plot_sc:
                if plot_data:
                    scDataHistName = "sc_" + cut["name"] + "_" + hist_def["obs"] + "_data"
                    if hist_def.get("namePostfix"):
                        scDataHistName += hist_def["namePostfix"]
                    scDataHist = histograms[scDataHistName]
                    scDataHist.SetMinimum(0.01)
                    scDataHist.SetMarkerStyle(kFullCircle)
                    scDataHist.SetMarkerSize(0.5)
                    scDataHist.SetMarkerColor(kRed)
                    scDataHist.Draw("P SAME")
                    legend.AddEntry(scDataHist, "sc data", 'p')
                
                scBgHistName = "sc_" + cut["name"] + "_" + hist_def["obs"] + "_bg"
                if hist_def.get("namePostfix"):
                    scBgHistName += hist_def["namePostfix"]
                scBgHist = histograms[scBgHistName]
                scBgHist.SetMinimum(0.01)
                scBgHist.SetLineWidth(2)
                scBgHist.SetLineColor(6)
                scBgHist.Draw("HIST SAME" + errorStr)
                
                legend.AddEntry(scBgHist, "sc bg", 'l')
            
            legend.Draw("SAME")
            pad.SetLogy()
            if plot_log_x and hist_def["obs"] == "invMass":
                pad.SetLogx()
                if plot_ratio or plot_custom_ratio > 0:
                    histRPad.SetLogx()
                    if (plot_sc and plot_data) or plot_custom_ratio > 1:
                        histR2Pad.SetLogx()
            else:
                pad.SetLogx(0)
                if plot_ratio or  plot_custom_ratio > 0:
                    histRPad.SetLogx(0)
                    if (plot_sc and plot_data) or plot_custom_ratio > 1:
                        histR2Pad.SetLogx(0)
            
            c1.Update()
            
            #print("**", ratioPads)
            
            if plot_ratio or plot_custom_ratio > 0:
                if plot_sc:
                    #print("Going to plot for ", histRPad, dataHist, scDataHist, hist_def)
                    
                    #print("***********", pId, ratioPads)
                    stackSum = utils.getStackSum(newBgHist)
                    memory.append(stackSum)
                    plotRatio(c1, histRPad, memory, stackSum, scBgHist, hist_def, "Bg / Bg")
                    if plot_data:
                        plotRatio(c1, histR2Pad, memory, dataHist, scDataHist, hist_def, "Data / Data", False)
                    #print("-------", pId, ratioPads)
                else:
                    if plot_custom_ratio > 0:
                        bgHists = hs.GetHists()
                        for ratioNum in range(plot_custom_ratio):
                            cutomRatio = cutomRatios[ratioNum]
                            numDenHists = [None, None]
                            titles = [None, None]
                            for numDenHistInx in range(2):
                                for histName in cutomRatio[numDenHistInx]:
                                    if histName == "data":
                                        if numDenHists[numDenHistInx] is None:
                                            numDenHists[numDenHistInx] = dataHist.Clone()
                                            memory.append(numDenHists[numDenHistInx])
                                            titles[numDenHistInx] = "data"
                                        else:
                                            numDenHists[numDenHistInx].Add(dataHist)
                                            titles[numDenHistInx] = " + data"
                                    else:
                                        for i, hist in enumerate(bgHists):
                                            if histName == hist.GetName().split("_")[-1]:
                                                if numDenHists[numDenHistInx] is None:
                                                    numDenHists[numDenHistInx] = hist.Clone()
                                                    memory.append(numDenHists[numDenHistInx])
                                                    titles[numDenHistInx] = histName
                                                else:
                                                    numDenHists[numDenHistInx].Add(hist)
                                                    titles[numDenHistInx] = " + " + histName
                            if ratioNum == 0:
                                plotRatio(c1, histRPad, memory, numDenHists[0], numDenHists[1], hist_def, titles[0] + " / " + titles[1])
                            else:
                                plotRatio(c1, histR2Pad, memory, numDenHists[0], numDenHists[1], hist_def, titles[0] + " / " + titles[1], False)
                    else:
                        stackSum = utils.getStackSum(newBgHist)
                        memory.append(stackSum)
                        plotRatio(c1, histRPad, memory, dataHist, stackSum, hist_def)
            
            #print("***", ratioPads)
            
            if plot_single:
                utils.stamp_plot()
                break
            
            pId += 1

            if pId > 4:
                pId = 1
                c1.Print(output_file);
                if create_canvas:
                    c1.Write(cutName)
                needToDraw = False;
            
            linBgHist = newBgHist.Clone()
            memory.append(linBgHist)
            linBgHist.SetMaximum(maximum*1.1)
            linBgHist.SetMinimum(0)
            
            #print("****", ratioPads)
            
            pad = histPad.cd(pId)
            histCPad = None
            histRPad = None
            histR2Pad = None
            if plot_ratio or plot_custom_ratio > 0:
                if ratioPads.get(pId) is None:
                    if (plot_sc and plot_data) or plot_custom_ratio > 1:
                        histCPad, histRPad, histR2Pad = createCRPads(pId, ratioPads, True)
                        #print("After:", histCPad, histRPad, histR2Pad)
                    else:
                        histCPad, histRPad = createCRPads(pId, ratioPads)
                else:
                    histCPad = ratioPads[pId][0]
                    histRPad = ratioPads[pId][1]
                    if (plot_sc and plot_data) or plot_custom_ratio > 1:
                        histR2Pad = ratioPads[pId][2]
                    #print("Was trying to get Id", pId, ratioPads)
                    #print("After in here", histCPad, histRPad, histR2Pad)
                print("Assigning ", histCPad)
                pad = histCPad
                pad.cd()
            else:
                pad = histPad.cd(pId)
            
            pad.SetLogy(0)
            
            if plot_log_x and hist_def["obs"] == "invMass":
                pad.SetLogx()
                if plot_ratio or plot_custom_ratio > 0:
                    histRPad.SetLogx()
                    if (plot_sc and plot_data) or plot_custom_ratio > 1:
                        histR2Pad.SetLogx()
            else:
                pad.SetLogx(0)
                
                if plot_ratio or  plot_custom_ratio > 0:
                    histRPad.SetLogx(0)
                    if (plot_sc and plot_data) or plot_custom_ratio > 1:
                        histR2Pad.SetLogx(0)
                
            linBgHist.Draw("hist" + errorStr)
            if plot_signal:
                for i in range(len(sigHists)):
                    sigHists[i].Draw("HIST SAME" + errorStr)
            if plot_data:
                dataHist.Draw("P e SAME")
            if plot_sc:
                if plot_data:
                    scDataHist.Draw("P e SAME")
                linScBgHist = scBgHist.Clone()
                memory.append(linScBgHist)
                linScBgHist.SetMaximum(maximum*1.1)
                linScBgHist.SetMinimum(0)
                linScBgHist.Draw("HIST SAME" + errorStr)
            
            legend.Draw("SAME")
            
            if plot_ratio or plot_custom_ratio > 0:
                if plot_sc:
                    stackSum = utils.getStackSum(newBgHist)
                    memory.append(stackSum)
                    plotRatio(c1, histRPad, memory, stackSum, scBgHist, hist_def, "Bg / Bg")
                    if plot_data:
                        plotRatio(c1, histR2Pad, memory, dataHist, scDataHist, hist_def, "Data / Data", False)
                else:
                    if plot_custom_ratio > 0:
                        bgHists = hs.GetHists()
                        
                        for ratioNum in range(plot_custom_ratio):
                            cutomRatio = cutomRatios[ratioNum]
                            numDenHists = [None, None]
                            titles = [None, None]
                            for numDenHistInx in range(2):
                                for histName in cutomRatio[numDenHistInx]:
                                    if histName == "data":
                                        if numDenHists[numDenHistInx] is None:
                                            numDenHists[numDenHistInx] = dataHist.Clone()
                                            memory.append(numDenHists[numDenHistInx])
                                            titles[numDenHistInx] = "data"
                                        else:
                                            numDenHists[numDenHistInx].Add(dataHist)
                                            titles[numDenHistInx] = " + data"
                                    else:
                                        for i, hist in enumerate(bgHists):
                                            if histName == hist.GetName().split("_")[-1]:
                                                if numDenHists[numDenHistInx] is None:
                                                    numDenHists[numDenHistInx] = hist.Clone()
                                                    memory.append(numDenHists[numDenHistInx])
                                                    titles[numDenHistInx] = histName
                                                else:
                                                    numDenHists[numDenHistInx].Add(hist)
                                                    titles[numDenHistInx] = " + " + histName
                            if ratioNum == 0:
                                plotRatio(c1, histRPad, memory, numDenHists[0], numDenHists[1], hist_def, titles[0] + " / " + titles[1])
                            else:
                                plotRatio(c1, histR2Pad, memory, numDenHists[0], numDenHists[1], hist_def, titles[0] + " / " + titles[1], False)
                    else:
                        stackSum = utils.getStackSum(newBgHist)
                        memory.append(stackSum)
                        plotRatio(c1, histRPad, memory, dataHist, stackSum, hist_def)
            
            pId += 1

            if pId > 4:
                pId = 1
                c1.Print(output_file);
                if create_canvas:
                    c1.Write(cutName)
                needToDraw = False;
            
        
        if needToDraw and not plot_single:
            for id in range(pId, 5):
                print("Clearing pad " + str(id))
                pad = histPad.cd(id)
                if plot_ratio:
                    ratioPads[pId][0].Clear()
                    ratioPads[pId][1].Clear()
                    if (plot_sc and plot_data) or plot_custom_ratio > 1:
                        ratioPads[pId][2].Clear()
                else:
                    pad.Clear()
        if needToDraw:
            c1.Print(output_file);
            if create_canvas:
                c1.Write(cutName)
        
    c1.Print(output_file+"]");
    if create_canvas:
        print("Just created", canvasFile.GetName())
        canvasFile.Close()
    
    
    print("End: " + datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    exit(0)

main()



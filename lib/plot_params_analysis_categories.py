import sys
import os
import copy

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib"))

import crystal_ball_params
import utils

from plot_params_base import *

import analysis_selections


common_histograms = [
    
    { "obs" : "MET", "minX" : 120, "maxX" : 800, "bins" : 30, "linearYspace" : 1.6 },
    #{ "obs" : "MT2", "minX" : 0, "maxX" : 100, "bins" : 30 },
    { "obs" : "MHT", "minX" : 220, "maxX" : 500, "bins" : 30, "units" : "H_{T}^{Miss} [GeV]", "linearYspace" : 1.4 },
    { "obs" : "HT", "minX" : 0, "maxX" : 700, "bins" : 30, "logYspace" : 10000, "linearYspace" : 1.6 },
    #{ "obs" : "MetDHt", "minX" : 0, "maxX" : 700, "bins" : 30 },
    #{ "obs" : "leptonFlavour%%%", "minX" : 0, "maxX" : 2, "bins" : 2 },
    #{ "obs" : "int(genFlavour == \"Muons\")", "minX" : 0, "maxX" : 2, "bins" : 2, "usedObs" : ["genFlavour"] },
    #{ "obs" : "int(genFlavour == \"Electrons\")", "minX" : 0, "maxX" : 2, "bins" : 2, "usedObs" : ["genFlavour"] },
    
    { "obs" : "NJets", "minX" : 0, "maxX" : 7, "bins" : 7, "linearYspace" : 1.6,  "logYspace" : 20000 },
    #{ "obs" : "BTagsLoose", "minX" : 0, "maxX" : 7, "bins" : 7 },
    #{ "obs" : "BTagsMedium", "minX" : 0, "maxX" : 7, "bins" : 7 },
    #{ "obs" : "BTagsDeepLoose", "minX" : 0, "maxX" : 7, "bins" : 7 },
    #{ "obs" : "BTagsDeepMedium", "minX" : 0, "maxX" : 7, "bins" : 7 },
    
    #{ "obs" : "LeadingJetQgLikelihood", "minX" : 0, "maxX" : 1, "bins" : 30 },
    { "obs" : "MinDeltaPhiMhtJets", "minX" : 0, "maxX" : 3.2, "bins" : 20, "units" : "Min\Delta_{}\phi(H_{T}^{Miss}, Jets)", "linearYspace" : 1.7,  "logYspace" : 20000 },
    #{ "obs" : "MinDeltaPhiMetJets", "minX" : 0, "maxX" : 3.2, "bins" : 20, "units" : "Min\Delta_{}\phi(E_{T}^{Miss}, Jets)" },
    
    { "obs" : "LeadingJetPt", "minX" : 0, "maxX" : 800, "bins" : 30, "units" : "p_{T}(j_{1}) [GeV]", "linearYspace" : 1.5,  "logYspace" : 200000 },
    { "obs" : "abs(LeadingJet.Eta())", "minX" : 0, "maxX" : 2.5, "bins" : 30, "usedObs" : ["LeadingJet"], "units" : "|\eta_{j_{1}}|", "linearYspace" : 1.8,  "logYspace" : 200000 },
    #{ "obs" : "MaxCsv25", "minX" : 0, "maxX" : 1, "bins" : 30 },
    #{ "obs" : "MaxDeepCsv25", "minX" : 0, "maxX" : 1, "bins" : 30 },
    #{ "obs" : "LeadingJetMinDeltaRElectrons", "minX" : 0, "maxX" : 5, "bins" : 30 },
    #{ "obs" : "LeadingJetMinDeltaRMuons", "minX" : 0, "maxX" : 5, "bins" : 30 },
    #{ "obs" : 'int(vetoElectronsPassIso)', "minX" : 0, "maxX" : 2, "bins" : 2, "usedObs" : ["vetoElectronsPassIso"]},
    #{ "obs" : 'int(vetoElectronsCorrJetIso10)', "minX" : 0, "maxX" : 2, "bins" : 2},
    #{ "obs" : 'int(vetoElectronsMediumID)', "minX" : 0, "maxX" : 2, "bins" : 2},
    #{ "obs" : 'int(vetoElectronsTightID)', "minX" : 0, "maxX" : 2, "bins" : 2},
    #{ "obs" : 'int(vetoElectrons)', "minX" : 0, "maxX" : 2, "bins" : 2},
    #{ "obs" : 'int(vetoMuonsPassIso)', "minX" : 0, "maxX" : 2, "bins" : 2, "usedObs" : ["vetoMuonsPassIso"]},
    #{ "obs" : 'int(vetoMuonsCorrJetIso10)', "minX" : 0, "maxX" : 2, "bins" : 2},
    #{ "obs" : 'int(vetoMuonoMediumID)', "minX" : 0, "maxX" : 2, "bins" : 2},
    #{ "obs" : 'int(vetoMuonsTightID)', "minX" : 0, "maxX" : 2, "bins" : 2},
    #{ "obs" : 'int(vetoMuons)', "minX" : 0, "maxX" : 2, "bins" : 2},

]

two_leps_histograms = [
    
    #{ "obs" : "invMass%%%_coarse", "formula" : "invMass%%%","minX" : 0, "maxX" : 13, "bins" : 6, "blind" : [4,None],"units" : "M_{ll} [GeV]" },
    { "obs" : "invMass%%%", "minX" : 0, "maxX" : 12, "bins" : 30, "blind" : [4,None],"units" : "M_{ll} [GeV]", "linearYspace" : 1.5 },
    { "obs" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 60,"units" : "BDT", "linearYspace" : 1.8 },
    { "obs" : "custom_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 60, "logYspace" : 8000, "linearYspace" : 1.6, "blind" : [None,0.1],"units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,1] },
    { "obs" : "dileptonPt%%%", "minX" : 0, "maxX" : 30, "bins" : 30, "units" : "p_{T}(ll) [GeV]", "linearYspace" : 1.6 },
    #{ "obs" : "deltaPhi%%%", "minX" : 0, "maxX" : 3.2, "bins" : 30 },
    { "obs" : "deltaEta%%%", "minX" : 0, "maxX" : 4, "bins" : 30, "units" : "\Delta_{}\eta", "linearYspace" : 1.6 },
    { "obs" : "deltaR%%%", "minX" : 0, "maxX" : 4, "bins" : 30, "units" : "\Delta_{}R_{ll}", "linearYspace" : 1.8 },
    { "obs" : "dilepHt%%%", "minX" : 200, "maxX" : 400, "bins" : 30 },
    #{ "obs" : "pt3%%%", "minX" : 0, "maxX" : 1000, "bins" : 30 },
    #{ "obs" : "mtautau%%%", "minX" : 0, "maxX" : 200, "bins" : 30 },
    
    { "obs" : "mt1%%%", "minX" : 0, "maxX" : 100, "bins" : 30, "units" : "m_{T}(l_{1}) [GeV]", "linearYspace" : 1.5 },
    #{ "obs" : "mt2%%%", "minX" : 0, "maxX" : 200, "bins" : 30 },
    
    { "obs" : "leptons%%%[0].Pt()", "minX" : 2, "maxX" : 15, "bins" : 30, "usedObs" : ["leptons%%%"], "units" : "p_{T}(l_{1}) [GeV]", "linearYspace" : 1.5 },
    { "obs" : "leptons%%%[1].Pt()", "minX" : 2, "maxX" : 15, "bins" : 30, "usedObs" : ["leptons%%%"], "units" : "p_{T}(l_{2}) [GeV]" },
    { "obs" : "abs(leptons%%%[0].Eta())", "minX" : 0, "maxX" : 2.4, "bins" : 30, "usedObs" : ["leptons%%%"] },
    { "obs" : "abs(leptons%%%[1].Eta())", "minX" : 0, "maxX" : 2.4, "bins" : 30, "usedObs" : ["leptons%%%"] },
    
    
    #{ "obs" : "deltaPhiMhtLepton1%%%", "minX" : 0, "maxX" : 3.5, "bins" : 30, "units" : "\Delta\phi(H_{T}^{Miss},l_{1})" },
    #{ "obs" : "deltaPhiMhtLepton2%%%", "minX" : 0, "maxX" : 3.5, "bins" : 30, "units" : "\Delta\phi(H_{T}^{Miss},l_{1})" },
    
    
    
    
    
    
    #{ "obs" : "leptons_ParentPdgId%%%[0]", "minX" : 0, "maxX" : 40, "bins" : 40, "usedObs" : ["leptons_ParentPdgId%%%"] },
    #{ "obs" : "leptons_ParentPdgId%%%[1]", "minX" : 0, "maxX" : 40, "bins" : 40, "usedObs" : ["leptons_ParentPdgId%%%"] },
    
    #{ "obs" : "deltaEtaLeadingJetDilepton%%%", "minX" : 0, "maxX" : 4, "bins" : 30 },
    #{ "obs" : "deltaPhiLeadingJetDilepton%%%", "minX" : 0, "maxX" : 4, "bins" : 30 },
    
    # { "obs" : "Electrons_minDeltaRJets[leptonsIdx%%%[0]]", "minX" : 0, "maxX" : 1, "bins" : 60, "usedObs" : ["leptonsIdx%%%", "Electrons_minDeltaRJets"] },
#     { "obs" : "Electrons_minDeltaRJets[leptonsIdx%%%[1]]", "minX" : 0, "maxX" : 1, "bins" : 60, "usedObs" : ["leptonsIdx%%%", "Electrons_minDeltaRJets"] },
#     
#     { "obs" : "Muons_minDeltaRJets[leptonsIdx%%%[0]]", "minX" : 0, "maxX" : 1, "bins" : 60, "usedObs" : ["leptonsIdx%%%", "Muons_minDeltaRJets"] },
#     { "obs" : "Muons_minDeltaRJets[leptonsIdx%%%[1]]", "minX" : 0, "maxX" : 1, "bins" : 60, "usedObs" : ["leptonsIdx%%%", "Muons_minDeltaRJets"] },
#     
#     { "obs" : "Electrons_deltaRLJ[leptonsIdx%%%[0]]", "minX" : 0, "maxX" : 1, "bins" : 60, "usedObs" : ["leptonsIdx%%%", "Electrons_deltaRLJ"] },
#     { "obs" : "Electrons_deltaRLJ[leptonsIdx%%%[1]]", "minX" : 0, "maxX" : 1, "bins" : 60, "usedObs" : ["leptonsIdx%%%", "Electrons_deltaRLJ"] },
#     
#     { "obs" : "Muons_deltaRLJ[leptonsIdx%%%[0]]", "minX" : 0, "maxX" : 1, "bins" : 60, "usedObs" : ["leptonsIdx%%%", "Muons_deltaRLJ"] },
#     { "obs" : "Muons_deltaRLJ[leptonsIdx%%%[1]]", "minX" : 0, "maxX" : 1, "bins" : 60, "usedObs" : ["leptonsIdx%%%", "Muons_deltaRLJ"] },
#     
#     { "obs" : "Electrons_deltaEtaLJ[leptonsIdx%%%[0]]", "minX" : 0, "maxX" : 1, "bins" : 60, "usedObs" : ["leptonsIdx%%%", "Electrons_deltaEtaLJ"] },
#     { "obs" : "Electrons_deltaEtaLJ[leptonsIdx%%%[1]]", "minX" : 0, "maxX" : 1, "bins" : 60, "usedObs" : ["leptonsIdx%%%", "Electrons_deltaEtaLJ"] },
#     
#     { "obs" : "Muons_deltaEtaLJ[leptonsIdx%%%[0]]", "minX" : 0, "maxX" : 1, "bins" : 60, "usedObs" : ["leptonsIdx%%%", "Muons_deltaEtaLJ"] },
#     { "obs" : "Muons_deltaEtaLJ[leptonsIdx%%%[1]]", "minX" : 0, "maxX" : 1, "bins" : 60, "usedObs" : ["leptonsIdx%%%", "Muons_deltaEtaLJ"] },

]

pionsObs = {
    "TAPPionTracks"   : "TLorentzVector",
    "TAPPionTracks_activity" : "double",
    "TAPPionTracks_charge" : "int",
    "TAPPionTracks_mT"  : "double",
    "TAPPionTracks_trkiso"  : "double",
}

photonObs = {
    "Photons" : "TLorentzVector",
    "Photons_electronFakes" : "bool",
    "Photons_fullID" : "bool",
    "Photons_genMatched" : "double",
    "Photons_hadTowOverEM" : "double",
    "Photons_hasPixelSeed" : "double",
    "Photons_isEB" : "double",
    "Photons_nonPrompt" : "bool",
    "Photons_passElectronVeto" : "double",
    "Photons_pfChargedIso" : "double",
    "Photons_pfChargedIsoRhoCorr" : "double",
    "Photons_pfGammaIso" : "double",
    "Photons_pfGammaIsoRhoCorr" : "double",
    "Photons_pfNeutralIso" : "double",
    "Photons_pfNeutralIsoRhoCorr" : "double",
    "Photons_sigmaIetaIeta" : "double",
}

extra_study_obs = [
    { "obs" : "TAPPionTracks.Pt()", "minX" : 0, "maxX" : 100, "bins" : 60 },
    { "obs" : "@TAPPionTracks.size()", "minX" : 0, "maxX" : 6, "bins" : 6 },
    { "obs" : "Photons.Pt()", "minX" : 0, "maxX" : 600, "bins" : 60 },
    { "obs" : "@Photons.size()", "minX" : 0, "maxX" : 6, "bins" : 6 },
]

ex_track_histograms = [
    #     #TRACK ONLY

    { "obs" : "exTrack_invMass%%%", "minX" : 0, "maxX" : 13, "bins" : 30, "linearYspace" : 1.4, "units" : "M_{ll} [GeV]" },
    { "obs" : "exTrack_dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 30, "linearYspace" : 1.6, "units" : "Event BDT", "logYspace" : 16000 },
    { "obs" : "exTrack_dileptonPt%%%", "minX" : 0, "maxX" : 100, "bins" : 30, "linearYspace" : 1.6, "units" : "p_{T}(ll) [GeV]" },
    { "obs" : "exTrack_deltaPhi%%%", "minX" : 0, "maxX" : 3.2, "bins" : 30, "linearYspace" : 1.4, "units" : "\Delta_{}\phi" },
    { "obs" : "exTrack_deltaEta%%%", "minX" : 0, "maxX" : 4, "bins" : 30, "linearYspace" : 1.4, "units" : "\Delta_{}\eta" },
    { "obs" : "exTrack_deltaR%%%", "minX" : 0, "maxX" : 4, "bins" : 30, "linearYspace" : 1.4, "units" : "\Delta_{}R_{ll}" },
    #{ "obs" : "exTrack_dilepHt", "minX" : 0, "maxX" : 400, "bins" : 30 },
    #{ "obs" : "exTrack_pt3", "minX" : 0, "maxX" : 1000, "bins" : 30 },
    #{ "obs" : "exTrack_mtautau", "minX" : 0, "maxX" : 200, "bins" : 30 },
    
    { "obs" : "trackBDT%%%", "minX" : 0, "maxX" : 1, "bins" : 30, "linearYspace" : 1.2, "units" : "track BDT", "logYspace" : 8000 },
    #{ "obs" : "secondTrackBDT", "minX" : -1, "maxX" : 1, "bins" : 30 },
    { "obs" : "abs(track%%%.Eta())", "minX" : 0, "maxX" : 2.4, "bins" : 30, "sc_obs" : "abs(sc_track.Eta())", "linearYspace" : 1.6, "units" : "|\eta_{t}|" },
    { "obs" : "abs(lepton%%%.Eta())", "minX" : 0, "maxX" : 2.4, "bins" : 30, "sc_obs" : "abs(sc_lepton.Eta())", "linearYspace" : 1.6, "units" : "|\eta_{l}|" },
    { "obs" : "track%%%.Pt()", "minX" : 1.9, "maxX" : 10, "bins" : 30, "units" : "p_{T}(t) [GeV]" },
    { "obs" : "lepton%%%.Pt()", "minX" : 2, "maxX" : 15, "bins" : 30, "units" : "p_{T}(l) [GeV]" },
    #{ "obs" : "secondTrack%%%.Pt()", "minX" : 0, "maxX" : 30, "bins" : 60 },
    #{ "obs" : "abs(secondTrack.Eta())", "minX" : 0, "maxX" : 3, "bins" : 60, "sc_obs" : "abs(sc_secondTrack.Eta())" },
    { "obs" : "abs(track%%%.Phi())", "minX" : 0, "maxX" : 3.2, "bins" : 30, "sc_obs" : "abs(sc_track.Phi())", "linearYspace" : 1.4 },
    { "obs" : "abs(lepton%%%.Phi())", "minX" : 0, "maxX" : 3.2, "bins" : 30, "sc_obs" : "abs(sc_lepton.Phi())", "linearYspace" : 1.4 },
    { "obs" : "mtl%%%", "minX" : 0, "maxX" : 120, "bins" : 30, "linearYspace" : 1.4, "units" : "m_{T}(l) [GeV]" },
    { "obs" : "mtt%%%", "minX" : 0, "maxX" : 120, "bins" : 30, "linearYspace" : 1.4, "units" : "m_{T}(t) [GeV]" },
    #{ "obs" : "NTracks", "minX" : 0, "maxX" : 7, "bins" : 7 },
    
    # { "obs" : "deltaRMetTrack", "minX" : 0, "maxX" : 4, "bins" : 30 },
#     { "obs" : "deltaPhiMetTrack", "minX" : 0, "maxX" : 3.2, "bins" : 30 },
#     { "obs" : "deltaRMetLepton", "minX" : 0, "maxX" : 4, "bins" : 30 },
#     { "obs" : "deltaPhiMetLepton", "minX" : 0, "maxX" : 3.2, "bins" : 30 },
#     
    { "obs" : "exTrack_deltaEtaLeadingJetDilepton%%%", "minX" : 0, "maxX" : 4, "bins" : 30, "linearYspace" : 1.4 },
    { "obs" : "exTrack_deltaPhiLeadingJetDilepton%%%", "minX" : 0, "maxX" : 3.2, "bins" : 30, "linearYspace" : 1.6 },
]

for hist in ex_track_histograms:
    if hist.get("sc_obs") is None:
        hist["sc_obs"] = "sc_" + hist["obs"]

two_leps_cuts = [
        #{"name":"invMass_Muons", "title": "invMass - Muons", "condition" : "MET >= 140 && invMass < 12  && invMass > 0.4 && leptonFlavour == \"Muons\""},
        #{"name":"invMass_Electrons", "title": "invMass - Electrons", "condition" : "MET >= 140 && invMass < 12  && invMass > 0.4 && leptonFlavour == \"Electrons\""},
        
        #{"name":"real", "title": "real", "condition" : "MET >= 140 && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && !(invMass > 0.95 && invMass < 1.06)"},
        
        #{"name":"dilepBDT", "title": "dilepBDT", "condition" : "MET >= 140 && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && !(invMass > 0.95 && invMass < 1.06) && dilepBDT > 0.1"},
        #{"name":"noBDT", "title": "noBDT", "condition" : "BTagsDeepMedium == 0 && (leptons[1].Pt() <= 3.5 || deltaR <= 0.3) && Mht >= 220 &&  MET >= 140 && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81)"},
        #{"name":"orthSOS", "title": "orthSOS", "condition" : "BTagsDeepMedium == 0 && (leptons[1].Pt() <= 3.5 || deltaR <= 0.3) && Mht >= 220 &&  MET >= 140 && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && dilepBDT > 0.1"},
        
        #{"name":"noBVeto_Electrons", "title": "noBVeto - Electrons", "condition" : "(leptons[1].Pt() <= 3.5 || deltaR <= 0.3) && Mht >= 220 &&  MET >= 140 && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && dilepBDT > 0.1 && vetoElectronsPassIsoTightID == 0 && vetoMuonsPassIsoPassJetIso == 0 && leptonFlavour == \"Electrons\""},
        #{"name":"noBVeto_Muons", "title": "noBVeto - Muons", "condition" : "(leptons[1].Pt() <= 3.5 || deltaR <= 0.3) && Mht >= 220 &&  MET >= 140 && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && dilepBDT > 0.1 && vetoElectronsPassIsoTightID == 0 && vetoMuonsPassIsoPassJetIso == 0 && leptonFlavour == \"Muons\""},
        
        
        #{"name":"orthSOS-no_veto_Electrons", "title": "orthSOS no lepton veto - Electrons", "condition" : "BTagsDeepMedium == 0 && (leptons[1].Pt() <= 3.5 || deltaR <= 0.3) && Mht >= 220 &&  MET >= 140 && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && dilepBDT > 0.1 && leptonFlavour == \"Electrons\""},
        #{"name":"orthSOS-no_veto_Muons", "title": "orthSOS no lepton veto - Muons", "condition" : "BTagsDeepMedium == 0 && (leptons[1].Pt() <= 3.5 || deltaR <= 0.3) && Mht >= 220 &&  MET >= 140 && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && dilepBDT > 0.1 && leptonFlavour == \"Muons\""},
        
        
        {"name":"orthSOS-veto_Electrons", "title": "orthSOS lepton veto - Electrons", "condition" : "vetoElectronsPassIsoTightID == 0 && vetoMuonsPassIsoPassIso == 0 && BTagsDeepMedium == 0 && (leptons[1].Pt() <= 3.5 || deltaR <= 0.3) && Mht >= 220 &&  MET >= 140 && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && dilepBDT > 0.1 && leptonFlavour == \"Electrons\""},
        {"name":"orthSOS-veto_Muons", "title": "orthSOS lepton veto - Muons", "condition" : "vetoElectronsPassIsoTightID == 0 && vetoMuonsPassIsoPassIso == 0 && BTagsDeepMedium == 0 && (leptons[1].Pt() <= 3.5 || deltaR <= 0.3) && Mht >= 220 &&  MET >= 140 && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && dilepBDT > 0.1 && leptonFlavour == \"Muons\""},
        
        {"name":"veto_Electrons", "title": "lepton veto - Electrons", "condition" : "vetoElectronsPassIsoTightID == 0 && vetoMuonsPassIsoPassIso == 0 && BTagsDeepMedium == 0 && Mht >= 220 &&  MET >= 140 && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && dilepBDT > 0.1 && leptonFlavour == \"Electrons\""},
        {"name":"veto_Muons", "title": "lepton veto - Muons", "condition" : "vetoElectronsPassIsoTightID == 0 && vetoMuonsPassIsoPassIso == 0 && BTagsDeepMedium == 0 && Mht >= 220 &&  MET >= 140 && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && dilepBDT > 0.1 && leptonFlavour == \"Muons\""},
        
        
        #{"name":"tc", "title": "tc", "condition" : 'MET >= 140 && invMass < 30 && leptonFlavour == "Muons" && tc * (!tautau)'},
        #{"name":"tautau", "title": "tautau", "condition" : '(MET >= 140 && invMass < 30 && leptonFlavour == "Muons") * (tautau)'},
        #{"name":"scother", "title": "scother", "condition" : 'MET >= 140 && invMass < 30 && leptonFlavour == "Muons" && sc * (!tautau) * (!omega) * (!rho_0) * (!eta) * (!phi) * (!eta_prime) * (!j_psi) * (!upsilon_1) * (!upsilon_2)'},
        
        # {"name":"dilepBDT", "title": "dilepBDT", "condition" : 'MET >= 140 && invMass < 30 && leptonFlavour == "Muons" && dilepBDT > 0.2'},
#         {"name":"lowMet", "title": "lowMet", "condition" : 'Met <= 200 && invMass < 30 && leptonFlavour == "Muons"'},
#         {"name":"lowMetBDT", "title": "lowMetBDT", "condition" : 'Met <= 200 && invMass < 30 && leptonFlavour == "Muons" && dilepBDT > 0'},
        
        
        # {"name":"parent_100-250", "title": "parent 100-250", "condition" : "MET >= 140 && invMass < 30 && leptons_ParentPdgId[0] > 100 && leptons_ParentPdgId[0] < 250"},
#         {"name":"parent_300-350", "title": "parent 300-350", "condition" : "MET >= 140 && invMass < 30 && leptons_ParentPdgId[0] > 300 && leptons_ParentPdgId[0] < 350"},
#         {"name":"parent_400-450", "title": "parent 400-450", "condition" : "MET >= 140 && invMass < 30 && leptons_ParentPdgId[0] > 400 && leptons_ParentPdgId[0] < 450"},
#          {"name":"parent_500-600", "title": "parent 500-600", "condition" : "MET >= 140 && invMass < 30 && leptons_ParentPdgId[0] > 500 && leptons_ParentPdgId[0] < 600"},
#          {"name":"parent_600", "title": "parent >600", "condition" : "MET >= 140 && invMass < 30 && leptons_ParentPdgId[0] > 600"},
#         
]


ex_track_cuts = [
        {"name":"dilepBDT", "title": "dilepBDT", "condition" : "secondTrack.Pt() < 12 && lepton.Pt() < 18 && track.Pt() < 15 && abs(lepton.Eta()) < 2.4 && deltaEta < 2.5 && mt1 < 120 && dilepHt > 130 && deltaR > 0.25 &&  deltaR < 3 && dilepBDT > 0.1 && MET >= 140 && invMass < 30 && dileptonPt < 30"},
]

# signals = [
#               "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim/higgsino_mu100_dm1p13Chi20Chipm.root",
#               "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim/higgsino_mu100_dm1p47Chi20Chipm.root",
#               "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim/higgsino_mu100_dm1p92Chi20Chipm.root",
#               "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim/higgsino_mu100_dm3p28Chi20Chipm.root",
#               "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim/higgsino_mu100_dm4p30Chi20Chipm.root"
#               ]
# 
# signalNames = [
#     "\Delta_{}M 1.13 Gev",
#     "\Delta_{}M 1.47 Gev",
#     "\Delta_{}M 1.9 Gev",
#     "\Delta_{}M 3.2 Gev",
#     "\Delta_{}M 4.3 Gev",
# ]

signals = [
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim_sum/higgsino_mu100_dm0p86Chi20Chipm*.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim_sum/higgsino_mu100_dm1p13Chi20Chipm*.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim_sum/higgsino_mu100_dm1p92Chi20Chipm*.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim_sum/higgsino_mu100_dm3p28Chi20Chipm*.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim_sum/higgsino_mu100_dm4p30Chi20Chipm*.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim_sum/higgsino_mu100_dm5p63Chi20Chipm*.root"
              
              ]

signals_mini = [
              #"/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim_sum/higgsino_mu100_dm0p86Chi20Chipm*.root",
              #"/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim_sum/higgsino_mu100_dm1p13Chi20Chipm*.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim_sum/higgsino_mu100_dm1p92Chi20Chipm*.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim_sum/higgsino_mu100_dm3p28Chi20Chipm*.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim_sum/higgsino_mu100_dm4p30Chi20Chipm*.root",
              #"/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim_sum/higgsino_mu100_dm5p63Chi20Chipm*.root"
              
              ]
              

signalNames = [
    "\Delta_{}m 0.8 GeV",
    "\Delta_{}m 1.1 GeV",
    "\Delta_{}m 1.9 GeV",
    "\Delta_{}m 3.2 GeV",
    "\Delta_{}m 4.3 GeV",
    "\Delta_{}m 5.6 GeV",
]

signalNames_mini = [
    #"\Delta_{}m 0.8 GeV",
    #"\Delta_{}m 1.1 GeV",
    "\Delta_{}m 1.9 GeV",
    "\Delta_{}m 3.2 GeV",
    "\Delta_{}m 4.3 GeV",
    #"\Delta_{}m 5.6 GeV",
]

signals_2017 = [
              #"/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_phase1/slim_sum/mChipm100GeV_dm0p759GeV_1.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_phase1/slim_sum/mChipm100GeV_dm0p959GeV_1.root",
              #"/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_phase1/slim_sum/mChipm100GeV_dm1p259GeV_1.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_phase1/slim_sum/mChipm100GeV_dm1p759GeV_1.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_phase1/slim_sum/mChipm100GeV_dm2p259GeV_1.root",
              #"/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_phase1/slim_sum/mChipm100GeV_dm3p259GeV_1.root"
              
              ]

signals_2017_full = [
              #"/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_phase1/slim_sum/mChipm100GeV_dm0p759GeV_1.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_phase1/sum/mChipm100GeV_dm0p959GeV_1.root",
              #"/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_phase1/slim_sum/mChipm100GeV_dm1p259GeV_1.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_phase1/sum/mChipm100GeV_dm1p759GeV_1.root",
              "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_phase1/sum/mChipm100GeV_dm2p259GeV_1.root",
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

# For this SC we need baseline cuts and sc cuts

class dilepton_muons(BaseParams):
    signal_dir = signals
    signal_names = signalNames
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/slim_sum/type_sum"
    data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim/sum/"
    cuts = [
        {"name":"none", "title": "None", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && isoCr%%% == 0)", "baseline" : "sameSign%%% == 0", "sc" : "sameSign%%% == 1"},
        #{"name":"non-orth", "title": "Non Orth", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && dilepBDT%%% > 0.3 && isoCr%%% == 0)", "baseline" : "sameSign%%% == 0", "sc" : "sameSign%%% == 1"},
        #{"name":"orth", "title": "Orth", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && dilepBDT%%% > 0.1 && (leptons%%%[1].Pt() <= 3.5 || deltaR%%% <= 0.3) && isoCr%%% == 0)", "baseline" : "sameSign%%% == 0", "sc" : "sameSign%%% == 1"},
    ]
    
    #(twoLeptons == 1 && (leptons[1].Pt() <= 3.5 || deltaR <= 0.3) && MHT >= 220 &&  MET >= 140 && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && dilepBDT > 0.1 && BTagsDeepMedium == 0 && vetoElectronsPassIsoTightID == 0 && vetoMuonsPassIsoPassIso == 0 && @leptons.size() == 2 && leptonFlavour == \"" + lep + "\" && sameSign == 0)", True)
    histograms_defs = []
    histograms_defs.extend(copy.deepcopy(common_histograms))
    histograms_defs.extend(copy.deepcopy(two_leps_histograms))
    #histograms_defs.extend(extra_study_obs)
    
    weightString = {
        #'MET' : "BranchingRatio * Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * puWeight",
        'MET' : "BranchingRatio * Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * passesUniversalSelection",
        #'MET' : "BranchingRatio * Weight",
    }
    
    calculatedLumi = {
        #'MET' : 35.778598358,
        'MET' : 135,
    }
    
    turnOnOnlyUsedObsInTree = False
    usedObs = ["BranchingRatio","Weight","passedMhtMet6pack","tEffhMetMhtRealXMht2016","puWeight","MinDeltaPhiMetJets","BTagsDeepMedium","twoLeptons%%%","MHT","MET","leptonFlavour%%%","invMass%%%","vetoElectronsPassIso","vetoMuonsPassIso","isoCr%%%","sameSign%%%", "leptons%%%", "deltaR%%%"]
    
    plot_sc = False
    plot_data = False
    plot_overflow = True
    plot_ratio = False
    
    blind_data = True
    
    save_histrograms_to_file = True
    load_histrograms_from_file = False    
    histrograms_file = "/afs/desy.de/user/n/nissanuv/CMSSW_10_1_0/src/cms-tools/analysis/scripts/dilepton_muons.root"
    
    turnOnOnlyUsedObsInTree = False
    plot_signal = True
    glob_signal = True

class dilepton_muons_CorrJetIso10Dr0_6(dilepton_muons):
    save_histrograms_to_file = True
    load_histrograms_from_file = True  
    plot_signal = True
    jetIsoStr = "CorrJetNoMultIso10Dr0.6"
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons" + jetIsoStr + ".root"
    cuts = copy.deepcopy(dilepton_muons.cuts)
    injectJetIsoToCuts(cuts, jetIsoStr)
    histograms_defs = copy.deepcopy(dilepton_muons.histograms_defs)
    injectJetIsoToHistograms(histograms_defs, jetIsoStr)
    usedObs = copy.deepcopy(dilepton_muons.usedObs)
    #print("before", usedObs)
    injectJetIsoToList(usedObs, jetIsoStr)
    #print("after", usedObs)
    #exit(0)
    sig_line_width = 2
    plot_error = False
    
    signal_dir = signals_mini
    signal_names = signalNames_mini
    signalCp = plotutils.categorySignalCp
    label_text = plotutils.StampStr.SIM
    
    #legend_columns = 3
    
    calculatedLumi = {
        'MET' : 36,
    }
    legend_border = 0
    legend_coordinates = {"x1" : .43, "y1" : .62, "x2" : .94, "y2" : .91}

class dilepton_muons_CorrJetIso10Dr0_6_phase1_2017(dilepton_muons_CorrJetIso10Dr0_6):
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons_CorrJetIso10Dr0_6_phase1_2017.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = True
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_phase1/sum/slim_sum/type_sum"
    signal_dir = signals_2017
    signal_names = signalNames_2017
    sig_line_width = 6
    calculatedLumi = {
        'MET' : 41,
    }
    legend_coordinates = {"x1" : .42, "y1" : .62, "x2" : .93, "y2" : .91}
    weightString = {
        #'MET' : "BranchingRatio * Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * puWeight",
        'MET' : "BranchingRatio * Weight * passedMhtMet6pack * tEffhMetMhtRealXMht2017 * passesUniversalSelection",
        #'MET' : "BranchingRatio * Weight",
    }
    
class dilepton_muons_CorrJetIso10_5Dr0_55_bdt_only(dilepton_muons_CorrJetIso10Dr0_6):
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/slim_sum/type_sum"
    #data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim/sum/"
    jetIsoStr = "CorrJetIso10.5Dr0.55"
    histograms_defs = [
        { "obs" : "custom_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 60, "blind" : [None,0.1],"units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,1] },
        { "obs" : "dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 40, "blind" : [None,0.1],"units" : "BDT"},
    ]
    injectJetIsoToHistograms(histograms_defs, jetIsoStr)
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons" + jetIsoStr + "_bdt_only.root"
    cuts = [
        {"name":"none", "title": "None", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && isoCr%%% == 0)", "baseline" : "sameSign%%% == 0", "sc" : "sameSign%%% == 1"},
        {"name":"orth", "title": "Orth", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && isoCr%%% == 0 && (leptons%%%[1].Pt() <= 3.5 || deltaR%%% <= 0.3))", "baseline" : "sameSign%%% == 0", "sc" : "sameSign%%% == 1"},
        #{"name":"orth", "title": "Orth", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && dilepBDT%%% > 0.1 && (leptons%%%[1].Pt() <= 3.5 || deltaR%%% <= 0.3) && isoCr%%% == 0)", "baseline" : "sameSign%%% == 0", "sc" : "sameSign%%% == 1"},
    ]
    injectJetIsoToCuts(cuts, jetIsoStr)
    load_histrograms_from_file = False

class dilepton_electrons_no_iso_bdt_only(dilepton_muons_CorrJetIso10_5Dr0_55_bdt_only):
    histrograms_file = "/afs/desy.de/user/n/nissanuv/CMSSW_10_1_0/src/cms-tools/analysis/scripts/dilepton_electrons_no_iso_bdt_only.root"
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/slim_sum/type_sum"
    #data_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/data/skim/sum/"
    jetIsoStr = "NoIso"
    histograms_defs = [
        #{ "obs" : "custom_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 60, "blind" : [None,0.1],"units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,1] },
        { "obs" : "dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 40, "blind" : [None,0.1],"units" : "BDT"},
    ]
    injectJetIsoToHistograms(histograms_defs, jetIsoStr)
    
    cuts = [
        {"name":"none", "title": "None", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Electrons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && isoCr%%% == 0)", "baseline" : "sameSign%%% == 0", "sc" : "sameSign%%% == 1"},
        {"name":"orth", "title": "Orth", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Electrons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && isoCr%%% == 0 && (leptons%%%[1].Pt() <= 3.5 || deltaR%%% <= 0.3))", "baseline" : "sameSign%%% == 0", "sc" : "sameSign%%% == 1"},
        {"name":"no_invmass", "title": "No Invmass", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Electrons\" && invMass%%% < 12  && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && isoCr%%% == 0)", "baseline" : "sameSign%%% == 0", "sc" : "sameSign%%% == 1"},
        #{"name":"orth", "title": "Orth", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && dilepBDT%%% > 0.1 && (leptons%%%[1].Pt() <= 3.5 || deltaR%%% <= 0.3) && isoCr%%% == 0)", "baseline" : "sameSign%%% == 0", "sc" : "sameSign%%% == 1"},
    ]
    injectJetIsoToCuts(cuts, jetIsoStr)
    load_histrograms_from_file = False
    turnOnOnlyUsedObsInTree = False

class dilepton_electrons_iso_bdt_only(dilepton_electrons_no_iso_bdt_only):
    histrograms_file = "/afs/desy.de/user/n/nissanuv/CMSSW_10_1_0/src/cms-tools/analysis/scripts/dilepton_electrons_iso_bdt_only.root"
    jetIsoStr = "CorrJetIso10.5Dr0.55"
    histograms_defs = [
        #{ "obs" : "custom_dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 60, "blind" : [None,0.1],"units" : "BDT", "customBins"  : [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,1] },
        { "obs" : "dilepBDT%%%", "formula" : "dilepBDT%%%", "minX" : -1, "maxX" : 1, "bins" : 40, "blind" : [None,0.1],"units" : "BDT"},
    ]
    injectJetIsoToHistograms(histograms_defs, jetIsoStr)
    cuts = [
        {"name":"none", "title": "None", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Electrons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && isoCr%%% == 0)", "baseline" : "sameSign%%% == 0", "sc" : "sameSign%%% == 1"},
        {"name":"orth", "title": "Orth", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Electrons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && isoCr%%% == 0 && (leptons%%%[1].Pt() <= 3.5 || deltaR%%% <= 0.3))", "baseline" : "sameSign%%% == 0", "sc" : "sameSign%%% == 1"},
        {"name":"no_invmass", "title": "No Invmass", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Electrons\" && invMass%%% < 12  && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && isoCr%%% == 0)", "baseline" : "sameSign%%% == 0", "sc" : "sameSign%%% == 1"},
        #{"name":"orth", "title": "Orth", "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && dilepBDT%%% > 0.1 && (leptons%%%[1].Pt() <= 3.5 || deltaR%%% <= 0.3) && isoCr%%% == 0)", "baseline" : "sameSign%%% == 0", "sc" : "sameSign%%% == 1"},
    ]
    injectJetIsoToCuts(cuts, jetIsoStr)

class dilepton_muons_CorrJetIso10_5Dr0_55_bdt_only_2016(dilepton_muons_CorrJetIso10_5Dr0_55_bdt_only):
    jetIsoStr = "CorrJetIso10.5Dr0.55"
    histrograms_file = BaseParams.histograms_root_files_dir + "/dilepton_muons" + jetIsoStr + "_bdt_only_2016.root"
    
    calculatedLumi = {
        'MET' : 35.712736198,
    }
    save_histrograms_to_file = True
    load_histrograms_from_file = False

class dilepton_electrons(dilepton_muons):
    cuts = [
        {"name":"none", "title": "None", "condition" : "(twoLeptons == 1 && MHT >= 220 &&  MET >= 140 && @leptons.size() == 2 && leptonFlavour == \"Electrons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0)  && isoCr == 0", "baseline" : "sameSign == 0", "sc" : "sameSign == 1"},
        #{"name":"non-orth", "title": "Non Orth", "condition" : "(twoLeptons == 1 && MHT >= 220 &&  MET >= 140 && @leptons.size() == 2 && leptonFlavour == \"Electrons\"  && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && dilepBDT > 0.1)  && isoCr == 0", "baseline" : "sameSign == 0", "sc" : "sameSign == 1"},
        #{"name":"orth", "title": "Orth", "condition" : "(twoLeptons == 1 && MHT >= 220 &&  MET >= 140 && @leptons.size() == 2 && leptonFlavour == \"Electrons\" && invMass < 12  && invMass > 0.4 && !(invMass > 3 && invMass < 3.2) && !(invMass > 0.75 && invMass < 0.81) && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && dilepBDT > 0.1 && (leptons[1].Pt() <= 3.5 || deltaR <= 0.3))  && isoCr == 0", "baseline" : "sameSign == 0", "sc" : "sameSign == 1"},
    ]
    histrograms_file = "/afs/desy.de/user/n/nissanuv/CMSSW_10_1_0/src/cms-tools/analysis/scripts/dilepton_electrons.root"

class track_electron(dilepton_muons_CorrJetIso10Dr0_6_phase1_2017):
    histrograms_file = BaseParams.histograms_root_files_dir + "/track_electron_2017.root"
    save_histrograms_to_file = True
    load_histrograms_from_file = True
    cuts = [
        {"name":"none", "title": "None", "condition" : "(MinDeltaPhiMhtJets > 0.4 && MHT >= 220 &&  MET >= 140 && BTagsDeepMedium == 0 )", "baseline" : "exclusiveTrack == 1 && trackBDT > 0 && exTrack_invMass < 12 && exclusiveTrackLeptonFlavour == \"Electrons\"  && exTrack_deltaR > 0.05", "sc" : "sc_exclusiveTrack == 1 && sc_trackBDT > 0 && sc_exTrack_invMass < 30 && sc_exclusiveTrackLeptonFlavour == \"Electrons\" && sc_exTrack_deltaR > 0.05"}
    ]
    histograms_defs = []
    histograms_defs.extend(common_histograms)
    histograms_defs.extend(ex_track_histograms)
    histograms_defs.extend(extra_study_obs)
    
    plot_error = True
    bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim_phase1/sum/type_sum"

class track_muon_bg_signal(track_electron):

    save_histrograms_to_file = True
    load_histrograms_from_file = True
    baseConitions = analysis_selections.injectValues(analysis_selections.ex_track_cond, "2017", "Muons")
    cuts = [
        {"name":"none", "title": "None", "condition" : analysis_selections.common_preselection, "baseline" : baseConitions, "sc" : "1" },
        #{"name":"sr", "title": "sr", "condition" : "(MinDeltaPhiMhtJets > 0.4 && MHT >= 220 &&  MET >= 140 && BTagsDeepMedium == 0 )", "baseline" : "exclusiveTrack == 1 && trackBDT > 0 && exTrack_invMass < 30 && exclusiveTrackLeptonFlavour == \"Muons\" && exTrack_dilepBDT > 0.1", "sc" : "sc_exclusiveTrack == 1 && sc_trackBDT > 0 && sc_exTrack_invMass < 30 && sc_exclusiveTrackLeptonFlavour == \"Muons\"" }
    ]
    histrograms_file = BaseParams.histograms_root_files_dir + "/track_muon.root"
    signal_dir = signals_2017_full
    
    histograms_defs = []
    histograms_defs.extend(common_histograms)
    histograms_defs.extend(ex_track_histograms)
    injectJetIsoToHistograms(histograms_defs, analysis_selections.jetIsos["Muons"])
    
    sig_line_width = 6
    
    
    y_title_offset = 1.0
    plot_error = True
    
    



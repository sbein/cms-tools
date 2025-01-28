#!/usr/bin/python

commonFlatObs = {
    "RunNum" : "int",
    "LumiBlockNum" : "int",
    "EvtNum" : "float",
    "MT2" : "float",
    "NVtx" : "float",
}

commonRecalcFlatObs = {
    "MET" : "float",
    "METPhi" : "float",
    "HT" : "float",
    "MHT" : "float",
    "MHTPhi" : "float",
}

commonObservablesStringList = ["genFlavour"]

bgFlatObs = {
    "madHT" : "float",
    "puWeight" : "float",
    "CrossSection" : "float",
}

filtersObs = {
    "JetID" : "bool",
    "NVtx" : "int",
    "globalSuperTightHalo2016Filter" : "int",
    "globalTightHalo2016Filter" : "int",
    "HBHENoiseFilter" : "int",    
    "HBHEIsoNoiseFilter" : "int",
    "eeBadScFilter" : "int",      
    "BadChargedCandidateFilter" : "int",
    "BadPFMuonFilter" : "int",
    "CSCTightHaloFilter" : "int", 
    "EcalDeadCellTriggerPrimitiveFilter" : "int",
    #"ecalBadCalibReducedExtraFilter" : "int",
    #"ecalBadCalibReducedFilter" : "int",
    "ecalBadCalibFilter" : "int",
    "PrimaryVertexFilter" : "int"
}

commonCalcFlatObs = {
    "BranchingRatio" : "float",
    "NJets" : "int",
    "BTagsLoose" : "int",
    "BTagsMedium" : "int",
    "BTagsDeepLoose" : "int",
    "BTagsDeepMedium" : "int",
    "MetDHt" : "float",
    "NL" : "int",
    "LeadingJetPt" : "float",
    "NLGen" : "int",
    "NLGenZ" : "int",
    "CrossSection" : "float",
    "LeadingJetPartonFlavor" : "int",
    "LeadingJetQgLikelihood" : "float",
    "LeadingJetMinDeltaRMuons" : "float",
    "LeadingJetMinDeltaRElectrons" : "float",
    "MinDeltaPhiMetJets" : "float",
    "MinDeltaPhiMhtJets" : "float",
    "MinCsv30" : "float",
    "MinCsv25" : "float",
    "MaxCsv30" : "float",
    "MaxCsv25" : "float",
    "MinDeepCsv30" : "float",
    "MinDeepCsv25" : "float",
    "MaxDeepCsv30" : "float",
    "MaxDeepCsv25" : "float",
    "category" : "bool",
    "madHT" : "float",
    "puWeight" : "float",
}

vetosFlatObs = {
    "vetoElectronsPassIso" : "bool",
    "vetoElectronsMediumID" : "bool",
    "vetoElectronsTightID" : "bool",
    
    "vetoMuonsPassIso" : "bool",
    "vetoMuonsMediumID" : "bool",
    "vetoMuonsTightID" : "bool",
}

genParticlesObs = {
    "GenParticles" : "TLorentzVector",
    "GenParticles_ParentId" : "int",
    "GenParticles_ParentIdx" : "int",
    "GenParticles_PdgId" : "int",
    "GenParticles_Status" : "int",
}


jetsObs = {
    "Jets" : "TLorentzVector",
    "Jets_bDiscriminatorCSV" : "double",
    "Jets_bJetTagDeepCSVBvsAll" : "double",
    "Jets_electronEnergyFraction" : "double",
    "Jets_muonEnergyFraction" : "double",
    "Jets_muonMultiplicity" : "int",
    "Jets_multiplicity" : "int",
    "Jets_electronMultiplicity" : "int",
    "Jets_partonFlavor" : "int",
    "Jets_qgLikelihood" : "double",
    "Jets_neutralEmEnergyFraction" : "double"
}

jetsCalcObs = {
    "Jets_muonCorrected" : "TLorentzVector",
    "Jets_electronCorrected" : "TLorentzVector",
    "Jets_trackCorrected" : "TLorentzVector",
}


triggerObs = {
    "TriggerNames" : "string",
    "TriggerPass" : "int",
    "TriggerPrescales" : "int",
    "TriggerVersion" : "int",
}

tracksObs = {
    "tracks"          : "TLorentzVector",
    "tracks_charge"   : "int",
    "tracks_chi2perNdof" : "double",
    "tracks_dxyVtx"   : "double",
    "tracks_dzVtx"    : "double",
    "tracks_trackJetIso" : "double",
    "tracks_trkMiniRelIso" : "double",
    "tracks_trkRelIso" : "double",
    "tracks_trackQualityHighPurity" : "double",
    "tracks_chargedPtSum" : "double",
    "tracks_matchedCaloEnergy" : "double",
    "tracks_matchedCaloEnergyJets" : "double",
    "tracks_minDrLepton" : "double",
    "tracks_neutralPtSum" : "double",
    "tracks_neutralWithoutGammaPtSum" : "double",
    "tracks_nMissingInnerHits" : "int",
    "tracks_nMissingMiddleHits" : "int",
    "tracks_nMissingOuterHits" : "int",
    "tracks_nValidPixelHits" : "int",
    "tracks_nValidTrackerHits" : "int",
    "tracks_passPFCandVeto" : "bool",
    "tracks_pixelLayersWithMeasurement" : "int",
    "tracks_ptError" : "double",
    "tracks_trackerLayersWithMeasurement" : "int",
    "tracks_trackJetIso" : "double",
    "tracks_trackQualityConfirmed" : "bool",
    "tracks_trackQualityDiscarded" : "bool",
    "tracks_trackQualityGoodIterative" : "bool",
    "tracks_trackQualityHighPurity" : "bool",
    "tracks_trackQualityHighPuritySetWithPV" : "bool",
    "tracks_trackQualityLoose" : "bool",
    "tracks_trackQualityLooseSetWithPV" : "bool",
    "tracks_trackQualitySize" : "bool",
    "tracks_trackQualityTight" : "bool",
    "tracks_trackQualityUndef" : "bool",
}
#tracksObs = {}

tracksCalcObs = {
    "tracks_ei" : "int",
    "tracks_mi" : "int",
    
    "tracks_deltaRLJ" : "double",
    "tracks_deltaPhiLJ" : "double",
    "tracks_deltaEtaLJ" : "double",
    
    "tracks_minDeltaRJets" : "double",
    "tracks_closestJet" : "int",
    "tracks_correctedMinDeltaRJets" : "double",
    "tracks_correctedClosestJet" : "int",
    
    "tracks_matchGen" : "bool",
    "tracks_isZ" : "bool"
}

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

electronsObs = {
    "Electrons" : "TLorentzVector",
    "Electrons_charge" : "int",
    "Electrons_mediumID" : "bool",
    "Electrons_passIso" : "bool",
    "Electrons_tightID" : "bool",
    "Electrons_EnergyCorr" : "double",
    "Electrons_MiniIso" : "double",
    "Electrons_MT2Activity" : "double",
    "Electrons_MTW" : "double",
    "Electrons_TrkEnergyCorr" : "double",
}

electronsCalcObs = {
    "Electrons_deltaRLJ" : "double",
    "Electrons_deltaPhiLJ" : "double",
    "Electrons_deltaEtaLJ" : "double",
    "Electrons_matchGen" : "bool",
    "Electrons_minDeltaRJets" : "double",
    "Electrons_closestJet" : "int",
    "Electrons_correctedMinDeltaRJets" : "double",
    "Electrons_correctedClosestJet" : "int",
    "Electrons_ti" : "int",
    "Electrons_isZ" : "bool"
}

muonsObs = {
    "Muons" : "TLorentzVector",
    "Muons_charge" : "int",
    "Muons_mediumID" : "bool",
    "Muons_passIso" : "bool",
    "Muons_tightID" : "bool",
    "Muons_MiniIso" : "double",
    "Muons_MT2Activity" : "double",
    "Muons_MTW" : "double",
}

dyMuonsFlatObs = {
    "DYMuonsInvMass" : "float"
}

dyMuonsClassObs = {
    "DYMuonsSum" : "TLorentzVector",
}

origMuonsObs = {
    "Muons_orig" : "TLorentzVector",
}

muonsCalcObs = {
    "Muons_deltaRLJ" : "double",
    "Muons_deltaPhiLJ" : "double",
    "Muons_deltaEtaLJ" : "double",
    "Muons_matchGen" : "bool",
    "Muons_minDeltaRJets" : "double",
    "Muons_closestJet" : "int",
    "Muons_correctedMinDeltaRJets" : "double",
    "Muons_correctedClosestJet" : "int",
    "Muons_ti" : "int",
    "Muons_isZ" : "bool"
}

############ FROM utils.py ############

dileptonObservablesVecList = {
    "leptons" : "TLorentzVector",
    "leptonsIdx" : "int",
    "leptons_charge" : "int",
    "leptons_ParentPdgId" : "int"
}

genObservablesVecList = {
    "genLeptonsIdx" : "int"
}

dileptonObservablesStringList = ["leptonFlavour"]

# USED FOR GEN STUFF TOO
commonObservablesDTypesList = {
    "invMass" : "float",
    "dileptonPt" : "float",
    "deltaPhi" : "float",
    "deltaEta" : "float",
    "deltaR" : "float",
    "pt3" : "float",
    "mtautau" : "float",
    "nmtautau" : "float",
    "mt1" : "float",
    "mt2" : "float",
    "mth1" : "float",
    "mth2" : "float",
    "deltaEtaLeadingJetDilepton" : "float",
    "deltaPhiLeadingJetDilepton" : "float",
    "dilepHt" : "float",
}

extraObservablesDTypesList = {
    "sameSign" : "bool",
    "vetoElectrons" : "bool",
    "vetoMuons" : "bool",
}

dileptonObservablesDTypesList = {
    "twoLeptons" : "bool",
    
    "deltaPhiMetLepton1" : "float",
    "deltaPhiMetLepton2" : "float",
    
    "deltaPhiMhtLepton1" : "float",
    "deltaPhiMhtLepton2" : "float",
    
    "tautau" : "bool",
    "rr" : "bool",
    "rf" : "bool",
    "ff" : "bool",
    "sc" : "bool",
    "n_body" : "bool",
    "tc" : "bool",
    "other" : "bool",
    "omega" : "bool",
    "rho_0" : "bool",
    "eta" : "bool",
    "phi" : "bool",
    "eta_prime" : "bool",
    "j_psi" : "bool",
    "upsilon_1" : "bool",
    "upsilon_2" : "bool",
    "NSelectionLeptons" : "int",
    "isoCr" : "int",
    "isoCrMinDr" : "float"
}

commonPostBdtObservablesDTypesList = {
    "dilepBDT" : "float"
}

exclusiveTrackPostBdtObservablesDTypesList = {
    "leptonParentPdgId" : "int",
    "trackParentPdgId" : "int",
}

dileptonObservablesDTypesList.update(extraObservablesDTypesList)
dileptonObservablesDTypesList.update(commonObservablesDTypesList)

exclusiveTrackObservablesStringList = ["exclusiveTrackLeptonFlavour"]
exclusiveTrackObservablesDTypesList = {
    "exclusiveTrack" : "bool",
    "trackZ" : "bool",
    "ti" : "int",
    "sti" : "int",
    "lepton_charge" : "int",
    "leptonIdx" : "int",
    "mtt" : "float",
    "mtl" : "float",
    "NTracks" : "int",
    
    "deltaPhiMetTrack" : "float",
    "deltaPhiMetLepton" : "float",
    
    "deltaPhiMhtTrack" : "float",
    "deltaPhiMhtLepton" : "float",
    
    "trackBDT" : "float",
    "secondTrackBDT" : "float"
}

exclusiveTrackObservablesClassList = {
    "track" : "TLorentzVector",
    "lepton" : "TLorentzVector",
    "secondTrack" : "TLorentzVector",
    "l1" : "TLorentzVector",
    "l2" : "TLorentzVector",
}

dileptonBDTeventObservables = {
    'HT' : 'F',
    'MinDeltaPhiMhtJets' :'F',
    'MHT' : 'F',
    'LeadingJetPt' : 'F',
    # it's not in absolute sign because the lepton is not either 
    'LeadingJet.Eta()' : 'F',
    'NJets' : 'I',
}
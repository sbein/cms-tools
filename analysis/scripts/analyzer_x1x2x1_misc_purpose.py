#!/usr/bin/env python

from ROOT import *
from glob import glob
from math import *
from sys import exit
from array import array
import argparse
import sys

# load FWLite C++ libraries
# gSystem.Load("libFWCoreFWLite.so");
# gSystem.Load("libDataFormatsFWLite.so");
# FWLiteEnabler.enable()

# load FWlite python libraries
# from DataFormats.FWLite import Handle, Events
# import FWCore.ParameterSet.Config as cms

from lib import histograms
from lib import utils
from lib import cuts
from lib import analysis_ntuples
from lib import analysis_tools

cutsDef = histograms.cutsDefs
histList = None

def handleX10X20X10Cand(event, weight, params, cutFlow = False):
	#JETS
	nj, btags, ljet = analysis_ntuples.numberOfJets25Pt2_4Eta_Loose2(event)
	params["nj"] = nj
	params["BTags"] = btags
	params["ljet"] = ljet
	
	#MET
	met = event.MET
	params["met"] = met
	#LEPTONS
	nL = event.Electrons.size() + event.Muons.size()
	params["nL"] = nL
	#HT
	ht = event.HT
	params["ht"] = ht
	#METDHT
	metDHt = 9999999
	if ht != 0:
		metDHt = met / ht
	params["metDHt"] = metDHt
	
	#Dilepton
	dilepton = False
	params["dilepton"] = False
	if nL == 2:
		#REMOVE COMMENTS!
		#HT
		dilepHt = analysis_ntuples.htJet25(event)
		params["dilepHt"] = dilepHt
		if event.Electrons.size() == 2:# and event.Electrons_charge[0] * event.Electrons_charge[1] < 0:
			dilepton = True
			params["dilepton"] = True
			params["oppositeSign"] = event.Electrons_charge[0] * event.Electrons_charge[1] < 0
			if event.Electrons[0].Pt() > event.Electrons[1].Pt():
				params["leptons"] = event.Electrons
			else:
				params["leptons"] = [event.Electrons[1], event.Electrons[0]]
			params["leptonsType"] = "E"
			handleX10X20X10DiLepton(event.Electrons[0], event.Electrons[1], event, nj, weight, params, "E", cutFlow)
		if event.Muons.size() == 2:# and event.Muons_charge[0] * event.Muons_charge[1] < 0:
			dilepton = True
			params["dilepton"] = True
			params["oppositeSign"] = event.Muons_charge[0] * event.Muons_charge[1] < 0
			if event.Muons[0].Pt() > event.Muons[1].Pt():
				params["leptons"] = event.Muons
			else:
				params["leptons"] = [event.Muons[1], event.Muons[0]]
			params["leptonsType"] = "M"
			handleX10X20X10DiLepton(event.Muons[0], event.Muons[1], event, nj, weight, params, "M", cutFlow)
	
	if cutFlow:
		return nj
	
	utils.fillHistWithCuts("NJ", nj, histList, cutsDef, "ntuples", event, weight, params)
	utils.fillHistWithCuts("MET", met, histList, cutsDef, "ntuples", event, weight, params)
	utils.fillHistWithCuts("METDHT", metDHt, histList, cutsDef, "ntuples", event, weight, params)
	utils.fillHistWithCuts("HTWeight", ht, histList, cutsDef, "ntuples", event, weight, params)
	
	if nj == 1:
		utils.fillHistWithCuts("MET1J", met, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("METDHT1J", metDHt, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("HT1J", ht, histList, cutsDef, "ntuples", event, weight, params)
	elif nj ==2:
		utils.fillHistWithCuts("MET2J", met, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("METDHT2J", metDHt, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("HT2J", ht, histList, cutsDef, "ntuples", event, weight, params)
	if nj >= 1:
		utils.fillHistWithCuts("METGT1J", met, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("METDHTGT1J", metDHt, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("HTGT1J", ht, histList, cutsDef, "ntuples", event, weight, params)
		
	utils.fillHistWithCuts("NLCan", nL, histList, cutsDef, "ntuples", event, weight, params)
	
	leptons = {"E" : event.Electrons, "M" : event.Muons}
	
	for kind, leps in leptons.items():
		for lep in leps:
			utils.fillHistWithCuts("LPT", lep.Pt(), histList, cutsDef, "ntuples", event, weight, params)
			utils.fillHistWithCuts("LEta", lep.Eta(), histList, cutsDef, "ntuples", event, weight, params)
			utils.fillHistWithCuts("LPhi", lep.Phi(), histList, cutsDef, "ntuples", event, weight, params)
			utils.fillHistWithCuts(kind + "PT", lep.Pt(), histList, cutsDef, "ntuples", event, weight, params)
			utils.fillHistWithCuts(kind + "Eta", lep.Eta(), histList, cutsDef, "ntuples", event, weight, params)
			utils.fillHistWithCuts(kind + "Phi", lep.Phi(), histList, cutsDef, "ntuples", event, weight, params)
			if nj == 1:
				utils.fillHistWithCuts("LPT1J", lep.Pt(), histList, cutsDef, "ntuples", event, weight, params)
				utils.fillHistWithCuts("LEta1J", lep.Eta(), histList, cutsDef, "ntuples", event, weight, params)
				utils.fillHistWithCuts("LPhi1J", lep.Phi(), histList, cutsDef, "ntuples", event, weight, params)
				utils.fillHistWithCuts(kind + "PT1J", lep.Pt(), histList, cutsDef, "ntuples", event, weight, params)
				utils.fillHistWithCuts(kind + "Eta1J", lep.Eta(), histList, cutsDef, "ntuples", event, weight, params)
				utils.fillHistWithCuts(kind + "Phi1J", lep.Phi(), histList, cutsDef, "ntuples", event, weight, params)
			elif nj == 2: 
				utils.fillHistWithCuts("LPT2J", lep.Pt(), histList, cutsDef, "ntuples", event, weight, params)
				utils.fillHistWithCuts("LEta2J", lep.Eta(), histList, cutsDef, "ntuples", event, weight, params)
				utils.fillHistWithCuts("LPhi2J", lep.Phi(), histList, cutsDef, "ntuples", event, weight, params)
				utils.fillHistWithCuts(kind + "PT2J", lep.Pt(), histList, cutsDef, "ntuples", event, weight, params)
				utils.fillHistWithCuts(kind + "Eta2J", lep.Eta(), histList, cutsDef, "ntuples", event, weight, params)
				utils.fillHistWithCuts(kind + "Phi2J", lep.Phi(), histList, cutsDef, "ntuples", event, weight, params)
			if nj >= 1:
				utils.fillHistWithCuts("LPTGT1J", lep.Pt(), histList, cutsDef, "ntuples", event, weight, params)
				utils.fillHistWithCuts("LEtaGT1J", lep.Eta(), histList, cutsDef, "ntuples", event, weight, params)
				utils.fillHistWithCuts("LPhiGT1J", lep.Phi(), histList, cutsDef, "ntuples", event, weight, params)
				utils.fillHistWithCuts(kind + "PTGT1J", lep.Pt(), histList, cutsDef, "ntuples", event, weight, params)
				utils.fillHistWithCuts(kind + "EtaGT1J", lep.Eta(), histList, cutsDef, "ntuples", event, weight, params)
				utils.fillHistWithCuts(kind + "PhiGT1J", lep.Phi(), histList, cutsDef, "ntuples", event, weight, params)
	
	return nj
	

def handleX10X20X10DiLepton(l1, l2, event, nj, weight, params, type, cutFlow):
	invMass = (l1 + l2).M()
	params["invMass"] = invMass
	dileptonPt = abs((l1 + l2).Pt())
	params["dileptonPt"] = dileptonPt
	deltaPhi = abs(l1.DeltaPhi(l2))
	params["deltaPhi"] = deltaPhi
	deltaEta = abs(l1.Eta() - l2.Eta())
	params["deltaEta"] = deltaEta
	deltaR = abs(l1.DeltaR(l2))
	params["deltaR"] = deltaR
	
	params["pt3"] = analysis_tools.pt3(l1.Pt(),l1.Phi(),l2.Pt(),l2.Phi(),event.MET,event.METPhi)
	
	deltaEtaLeadingJetDilepton = None
	params["deltaEtaLeadingJetDilepton"] = None
	leadingJetPartonFlavor = None
	params["leadingJetPartonFlavor"] = None
	leadingJetQgLikelihood = None
	params["leadingJetQgLikelihood"] = None
	
	pt = TLorentzVector()
	pt.SetPtEtaPhiE(event.MET,0,event.METPhi,event.MET)
	
	params["mt1"] = analysis_tools.MT2(event.MET, event.METPhi, l1)
	params["mt2"] = analysis_tools.MT2(event.MET, event.METPhi, l2)
	
	mtautau = analysis_tools.PreciseMtautau(event.MET, event.METPhi, l1, l2)
	params["mtautau"] = mtautau
	
	if cutFlow:
		return
	
	if nj > 0:
		deltaEtaLeadingJetDilepton = abs((l1 + l2).Eta() - event.Jets[params["ljet"]].Eta())
		params["deltaEtaLeadingJetDilepton"] = deltaEtaLeadingJetDilepton
		leadingJetPartonFlavor = event.Jets_partonFlavor[params["ljet"]]
		params["leadingJetPartonFlavor"] = leadingJetPartonFlavor
		leadingJetQgLikelihood = event.Jets_qgLikelihood[params["ljet"]]
		params["leadingJetQgLikelihood"] = leadingJetQgLikelihood
		 
		utils.fillHistWithCuts("DeltaEtaLeadingJet", deltaEtaLeadingJetDilepton, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("LeadingJetPartonFlavor", leadingJetPartonFlavor, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("LeadingJetQgLikelihood", leadingJetQgLikelihood, histList, cutsDef, "ntuples", event, weight, params)
	
	utils.fillHistWithCuts("MTauTau", mtautau, histList, cutsDef, "ntuples", event, weight, params)
	utils.fillHistWithCuts("MT", params["mt1"], histList, cutsDef, "ntuples", event, weight, params)
	utils.fillHistWithCuts("MT", params["mt2"], histList, cutsDef, "ntuples", event, weight, params)
	
	utils.fillHistWithCuts("DuoLepPt", dileptonPt, histList, cutsDef, "ntuples", event, weight, params)
	utils.fillHistWithCuts("DuoLepCanInvMass", invMass, histList, cutsDef, "ntuples", event, weight, params)
	utils.fillHistWithCuts("DeltaRCan", deltaR, histList, cutsDef, "ntuples", event, weight, params)
	utils.fillHistWithCuts("DeltaEtaCan", deltaEta, histList, cutsDef, "ntuples", event, weight, params)
	utils.fillHistWithCuts("DeltaPhiCan", deltaPhi, histList, cutsDef, "ntuples", event, weight, params)
	utils.fillHistWithCuts(type + "DuoLepCanInvMass", invMass, histList, cutsDef, "ntuples", event, weight, params)
	utils.fillHistWithCuts(type + "DeltaRCan", deltaR, histList, cutsDef, "ntuples", event, weight, params)
	utils.fillHistWithCuts(type + "DeltaEtaCan", deltaEta, histList, cutsDef, "ntuples", event, weight, params)
	utils.fillHistWithCuts(type + "DeltaPhiCan", deltaPhi, histList, cutsDef, "ntuples", event, weight, params)
	
	if deltaEtaLeadingJetDilepton is not None:
		utils.fillHistWithCuts("MTauTau", mtautau, histList, cutsDef, "ntuples", event, weight, params)
	
	if params["met"] >= 125 and params["met"] <= 200:
		utils.fillHistWithCuts("DuoLepCanInvMassMET125-200", invMass, histList, cutsDef, "ntuples", event, weight, params)
		if params["pt3"] >= 125 and params["pt3"] <= 200:
			utils.fillHistWithCuts("DuoLepCanInvMassMET125-200Pt3", invMass, histList, cutsDef, "ntuples", event, weight, params)
	elif params["met"] >= 200 and params["met"] <= 250:
		utils.fillHistWithCuts("DuoLepCanInvMassMET200-250", invMass, histList, cutsDef, "ntuples", event, weight, params)
		if params["pt3"] >= 200 and params["pt3"] <= 250:
			utils.fillHistWithCuts("DuoLepCanInvMassMET200-250Pt3", invMass, histList, cutsDef, "ntuples", event, weight, params)
	elif params["met"] >= 250:
		utils.fillHistWithCuts("DuoLepCanInvMassMET250", invMass, histList, cutsDef, "ntuples", event, weight, params)
		if params["pt3"] >= 250:
			utils.fillHistWithCuts("DuoLepCanInvMassMET250Pt3", invMass, histList, cutsDef, "ntuples", event, weight, params)
	
	if nj == 1:
		utils.fillHistWithCuts("MTauTau1J", mtautau, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("MT1J", params["mt1"], histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("MT1J", params["mt2"], histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("DuoLepPt1J", dileptonPt, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("DuoLepCanInvMass1J", invMass, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("DeltaRCan1J", deltaR, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("DeltaEtaCan1J", deltaEta, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("DeltaPhiCan1J", deltaPhi, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts(type + "DuoLepCanInvMass1J", invMass, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts(type + "DeltaRCan1J", deltaR, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts(type + "DeltaEtaCan1J", deltaEta, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts(type + "DeltaPhiCan1J", deltaPhi, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("DeltaEtaLeadingJet1J", deltaEtaLeadingJetDilepton, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("LeadingJetPartonFlavor1J", leadingJetPartonFlavor, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("LeadingJetQgLikelihood1J", leadingJetQgLikelihood, histList, cutsDef, "ntuples", event, weight, params)
		
		if params["met"] >= 125 and params["met"] <= 200:
			utils.fillHistWithCuts("DuoLepCanInvMass1JMET125-200", invMass, histList, cutsDef, "ntuples", event, weight, params)
			if params["pt3"] >= 125 and params["pt3"] <= 200:
				utils.fillHistWithCuts("DuoLepCanInvMass1JMET125-200Pt3", invMass, histList, cutsDef, "ntuples", event, weight, params)
		elif params["met"] >= 200 and params["met"] <= 250:
			utils.fillHistWithCuts("DuoLepCanInvMass1JMET200-250", invMass, histList, cutsDef, "ntuples", event, weight, params)
			if params["pt3"] >= 200 and params["pt3"] <= 250:
				utils.fillHistWithCuts("DuoLepCanInvMass1JMET200-250Pt3", invMass, histList, cutsDef, "ntuples", event, weight, params)
		elif params["met"] >= 250:
			utils.fillHistWithCuts("DuoLepCanInvMass1JMET250", invMass, histList, cutsDef, "ntuples", event, weight, params)
			if params["pt3"] >= 250:
				utils.fillHistWithCuts("DuoLepCanInvMass1JMET250Pt3", invMass, histList, cutsDef, "ntuples", event, weight, params)
		
	elif nj ==2:
		utils.fillHistWithCuts("MTauTau2J", mtautau, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("MT2J", params["mt1"], histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("MT2J", params["mt2"], histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("DuoLepPt2J", dileptonPt, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("DuoLepCanInvMass2J", invMass, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("DeltaRCan2J", deltaR, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("DeltaEtaCan2J", deltaEta, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("DeltaPhiCan2J", deltaPhi, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts(type + "DuoLepCanInvMass2J", invMass, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts(type + "DeltaRCan2J", deltaR, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts(type + "DeltaEtaCan2J", deltaEta, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts(type + "DeltaPhiCan2J", deltaPhi, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("DeltaEtaLeadingJet2J", deltaEtaLeadingJetDilepton, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("LeadingJetPartonFlavor2J", leadingJetPartonFlavor, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("LeadingJetQgLikelihood2J", leadingJetQgLikelihood, histList, cutsDef, "ntuples", event, weight, params)
		
		if params["met"] >= 125 and params["met"] <= 200:
			utils.fillHistWithCuts("DuoLepCanInvMass2JMET125-200", invMass, histList, cutsDef, "ntuples", event, weight, params)
			if params["pt3"] >= 125 and params["pt3"] <= 200:
				utils.fillHistWithCuts("DuoLepCanInvMass2JMET125-200Pt3", invMass, histList, cutsDef, "ntuples", event, weight, params)
		elif params["met"] >= 200 and params["met"] <= 250:
			utils.fillHistWithCuts("DuoLepCanInvMass2JMET200-250", invMass, histList, cutsDef, "ntuples", event, weight, params)
			if params["pt3"] >= 200 and params["pt3"] <= 250:
				utils.fillHistWithCuts("DuoLepCanInvMass2JMET200-250Pt3", invMass, histList, cutsDef, "ntuples", event, weight, params)
		elif params["met"] >= 250:
			utils.fillHistWithCuts("DuoLepCanInvMass2JMET250", invMass, histList, cutsDef, "ntuples", event, weight, params)
			if params["pt3"] >= 250:
				utils.fillHistWithCuts("DuoLepCanInvMass2JMET250Pt3", invMass, histList, cutsDef, "ntuples", event, weight, params)
	if nj >= 1:
		utils.fillHistWithCuts("MTauTauGT1J", mtautau, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("MTGT1J", params["mt1"], histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("MTGT1J", params["mt2"], histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("DuoLepPtGT1J", dileptonPt, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("DuoLepCanInvMassGT1J", invMass, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("DeltaRCanGT1J", deltaR, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("DeltaEtaCanGT1J", deltaEta, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("DeltaPhiCanGT1J", deltaPhi, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts(type + "DuoLepCanInvMassGT1J", invMass, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts(type + "DeltaRCanGT1J", deltaR, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts(type + "DeltaEtaCanGT1J", deltaEta, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts(type + "DeltaPhiCanGT1J", deltaPhi, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("DeltaEtaLeadingJetGT1J", deltaEtaLeadingJetDilepton, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("LeadingJetPartonFlavorGT1J", leadingJetPartonFlavor, histList, cutsDef, "ntuples", event, weight, params)
		utils.fillHistWithCuts("LeadingJetQgLikelihoodGT1J", leadingJetQgLikelihood, histList, cutsDef, "ntuples", event, weight, params)
		
		if params["met"] >= 125 and params["met"] <= 200:
			utils.fillHistWithCuts("DuoLepCanInvMassGT1JMET125-200", invMass, histList, cutsDef, "ntuples", event, weight, params)
			if params["pt3"] >= 125 and params["pt3"] <= 200:
				utils.fillHistWithCuts("DuoLepCanInvMassGT1JMET125-200Pt3", invMass, histList, cutsDef, "ntuples", event, weight, params)
		elif params["met"] >= 200 and params["met"] <= 250:
			utils.fillHistWithCuts("DuoLepCanInvMassGT1JMET200-250", invMass, histList, cutsDef, "ntuples", event, weight, params)
			if params["pt3"] >= 200 and params["pt3"] <= 250:
				utils.fillHistWithCuts("DuoLepCanInvMassGT1JMET200-250Pt3", invMass, histList, cutsDef, "ntuples", event, weight, params)
		elif params["met"] >= 250:
			utils.fillHistWithCuts("DuoLepCanInvMassGT1JMET250", invMass, histList, cutsDef, "ntuples", event, weight, params)
			if params["pt3"] >= 250:
				utils.fillHistWithCuts("DuoLepCanInvMassGT1JMET250Pt3", invMass, histList, cutsDef, "ntuples", event, weight, params)
	

def handleX10X20X10NLGen(event, weight, params, nj):
	partSize = event.GenParticles.size()
	nL = 0
	l1 = None
	l2 = None
	t1 = None
	t2 = None
	
	duoTao = analysis_ntuples.isDuoTauEvent(event)
	
	neutrinos = []
	
	for ipart in range(partSize):
		if event.GenParticles_Status[ipart] == 1 and (abs(event.GenParticles_PdgId[ipart]) == 11 or abs(event.GenParticles_PdgId[ipart]) == 13):
			nL += 1
			minR = minDeltaR(ipart, event)
			if minR is not None:
				utils.fillHistWithCuts("DeltaRLepMatchCand", minR, histList, cutsDef, "ntuples", event, weight, params)
				if minR <= 0.1:
					utils.fillHistWithCuts("MatchLep", 1, histList, cutsDef, "ntuples", event, weight, params)
				else:
					utils.fillHistWithCuts("MatchLep", 0, histList, cutsDef, "ntuples", event, weight, params)
			else:
				#print("No minR")
				utils.fillHistWithCuts("MatchLep", 0, histList, cutsDef, "ntuples", event, weight, params)
			if l1 is None:
				l1 = ipart
			else:
				l2 = ipart
		if duoTao and abs(event.GenParticles_PdgId[ipart]) == 15:
			if t1 is None:
				t1 = ipart
			else:
				t2 = ipart
		
		if duoTao and abs(event.GenParticles_PdgId[ipart]) == 12 or abs(event.GenParticles_PdgId[ipart]) == 14 or abs(event.GenParticles_PdgId[ipart]) == 16:
			neutrinos.append(ipart)
			
			
	utils.fillHistWithCuts("NLGen", nL, histList, cutsDef, "ntuples", event, weight, params)
	
	if duoTao and nL == 2 and nj >= 1 and abs(event.GenParticles_PdgId[l1]) == abs(event.GenParticles_PdgId[l2]) and (event.GenParticles_PdgId[l1] * event.GenParticles_PdgId[l2] < 0):
		t1v = event.GenParticles[t1]
		t2v = event.GenParticles[t2]
		l1v = event.GenParticles[l1]
		l2v = event.GenParticles[l2]
	
		if len(neutrinos) == 4 and abs(event.GenParticles_ParentId[l1]) == 15 and abs(event.GenParticles_ParentId[l2]) == 15:
			pt = TLorentzVector()
			pt.SetPtEtaPhiE(event.GenMET,0,event.GenMETPhi,event.GenMET)
			mttgenrec = analysis_tools.Mtautau(pt, event.GenParticles[l1], event.GenParticles[l2])
			utils.fillHistWithCuts("MTauTauGenLep", mttgenrec, histList, cutsDef, "ntuples", event, weight, params)
			sum = event.GenParticles[l1] + event.GenParticles[l2]
			n1 = TLorentzVector()
			n2 = TLorentzVector()
			for i in range(len(neutrinos)):
				nv = event.GenParticles[neutrinos[i]]
				if abs(event.GenParticles_PdgId[neutrinos[i]]) == 16:
					if event.GenParticles_PdgId[neutrinos[i]] * event.GenParticles_PdgId[t1] > 0:
						n1 += nv
					else:
						n2 += nv
				else:
					if event.GenParticles_PdgId[neutrinos[i]] * event.GenParticles_PdgId[t1] < 0:
						n1 += nv
					else:
						n2 += nv
				sum += nv
			utils.fillHistWithCuts("MTauTauGenLepNeu", sum.M(), histList, cutsDef, "ntuples", event, weight, params)
			
	#if nL == 2 and abs(event.GenParticles_PdgId[l1]) == abs(event.GenParticles_PdgId[l2]) and (event.GenParticles_PdgId[l1] * event.GenParticles_PdgId[l2] < 0):
		#handleX10X20X10GenDiLepton(event, l1, l2, weight, params)

def minDeltaR(ipart, event):
	minimum = None
	minCan = None
	candidates = None
	if abs(event.GenParticles_PdgId[ipart]) == 11:
		candidates = event.Electrons
	else:
		candidates = event.Muons
	genV = event.GenParticles[ipart]
	canSize = candidates.size()
	for ican in range(canSize):
		canV = candidates[ican]
		deltaR = genV.DeltaR(canV)
		if minimum is None or deltaR < minimum:
			minimum = deltaR
	return minimum

def handleX10X20X10GenDiLepton(event, l1, l2, weight, params):
	l1v = event.GenParticles[l1]
	l2v = event.GenParticles[l2]
	deltaPhi = l1v.DeltaPhi(l2v)
	deltaR = l1v.DeltaR(l2v)
	deltaEta = abs(l1v.Eta() - l2v.Eta())
	utils.fillHistWithCuts("DeltaPhiGen", deltaPhi, histList, cutsDef, "ntuples", event, weight, params)
	utils.fillHistWithCuts("DeltaRGen", deltaR, histList, cutsDef, "ntuples", event, weight, params)
	utils.fillHistWithCuts("DeltaEtaGen", deltaEta, histList, cutsDef, "ntuples", event, weight, params)	

parser = argparse.ArgumentParser(description='Create histograms for x1x2x1 process.')
parser.add_argument('-i', '--input_file', nargs=1, help='Input Filename', required=False)
parser.add_argument('-o', '--output_file', nargs=1, help='Output Filename', required=False)
parser.add_argument('-madHTgt', '--madHTgt', nargs=1, help='madHT lower bound', required=False)
parser.add_argument('-madHTlt', '--madHTlt', nargs=1, help='madHT uppper bound', required=False)
parser.add_argument('-cf', '--cut_flow', nargs=1, help='Cut Flow', required=False)

parser.add_argument('-s', '--signal', dest='signal', help='Signal', action='store_true')
parser.add_argument('-bg', '--background', dest='bg', help='Background', action='store_true')
args = parser.parse_args()

madHTgt = None
madHTlt = None
if args.madHTgt:
	madHTgt = int(args.madHTgt[0])
	print("Got madHT lower bound of " + str(madHTgt))
if args.madHTlt:
	madHTlt = int(args.madHTlt[0])
	print("Got madHT upper bound of " + str(madHTlt))
	

signal = args.signal
bg = args.bg
cf = None

if args.cut_flow:
	cf = args.cut_flow[0]

input_file = None
if args.input_file:
	input_file = args.input_file[0]
output_file = None
if args.output_file:
	output_file = args.output_file[0]

if (bg and signal) or not (bg or signal):
	signal = True
	bg = False
	
################## CUT FLOW ##################
if cf:
	print("IN CUTFLOW")
	cutFlow = cuts.createCutFlow(cf, cutsDef, "ntuples")
	input_files = input_file.split(" ")
	for file in input_files:
		c = TChain("TreeMaker2/PreSelection");
		c.Add(file)
		nentries = c.GetEntries()
		print("nentries=" + str(nentries))
		for ientry in range(nentries):
			if ientry % 10000 == 0:
				print("processing entry" , ientry, "out of", nentries)
				#print(cutFlow)
			rightProcess = True
			c.GetEntry(ientry)
			if signal:
				rightProcess = analysis_ntuples.isX1X2X1Process(c)
			if rightProcess:
				params = {}
				handleX10X20X10Cand(c, 1, params, True)
				cuts.appendCutFlow(cf, cutsDef, cutFlow, "ntuples", c, params)
	cuts.printCutFlow(cf, cutsDef, cutFlow, "ntuples")
	exit(0)
##############################################

# Create the histograms
histDefs = histograms.commonHistDefs
histList = utils.createHistograms(histDefs, cutsDef)
	
if signal and not output_file:
	print("No output file for signal analysis. Assigning default.")
	output_file = "../../sim_x10x20x10/x10x20x10.root"

if signal and not input_file:
	print("No input file for signal analysis. Assigning default.")
	input_file = "/nfs/dust/cms/user/beinsam/CommonNtuples/MC_BSM/CompressedHiggsino/M1M2Scan/ntuple_sidecar/higgsino_mu100_dm3.28Chi20Chipm.root"

c = TChain("TreeMaker2/PreSelection");
c.Add(input_file)

def isX1X2X1Process(event):
	partSize = event.GenParticles.size()
	right = False
	x22 = 0
	x23 = 0
	x24 = 0
	x_24 = 0
	for ipart in range(partSize):
		if event.GenParticles_PdgId[ipart] == 1000022:
			#print("Found x10")
			x22 +=1
			if event.GenParticles_ParentId[ipart] == 1000023:
				#print("Mother x20")
				if not analysis_tools.isSusy(event.GenParticles_ParentId[event.GenParticles_ParentIdx[ipart]]):
					#print("Found!!!")
					right = True
		elif event.GenParticles_PdgId[ipart] == 1000023:
			x23 += 1
		elif event.GenParticles_PdgId[ipart] == 1000024:
			x24 += 1
		elif event.GenParticles_PdgId[ipart] == -1000024:
			x_24 += 1
	return (right, x22, x23, x24, x_24)

nentries = c.GetEntries()
print("nentries=" + str(nentries))

for ientry in range(nentries) :
	if ientry % 10000 == 0 :
		print("processing entry" , ientry, "out of", nentries)
	c.GetEntry(ientry)
	rightProcess = True
	if signal:
		(right, x22, x23, x24, x_24) = isX1X2X1Process(c)
		#if rightProcess: 
			#print("*******")
		print(right, x22, x23, x24, x_24)
	if not rightProcess:
		print("****NO******")

exit(0)
		

utils.printNullHistograms(histList)

fnew = TFile(output_file, "recreate")

if signal:
	sigma = 1.21547 #fb 
	N = histList["HT"].Integral(-1,99999999)+0.000000000001

	print("Number of HT event " + str(N))

	weight = sigma * utils.LUMINOSITY / N
	
	print("Weight=" + str(weight))

	utils.scaleHistograms(histList, histDefs, weight)
	
utils.writeHistograms(histList)
fnew.Close()

exit(0)

#################	END OF SCRIPT	##########################
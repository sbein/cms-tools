#!/usr/bin/python3

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

# load FWlite python3 libraries
# from DataFormats.FWLite import Handle, Events
# import FWCore.ParameterSet.Config as cms

sys.path.append("/afs/desy.de/user/n/nissanuv/cms-tools")
from lib import histograms
from lib import utils
from lib import cuts

# Create the histograms
histDefs = histograms.commonHistDefs
cutsDef = histograms.cutsDefs
histList = utils.createHistograms(histDefs, cutsDef)

def isSusy(pdgId):
	pdgId = abs(pdgId)
	if pdgId >= 1000001 and pdgId <= 1000006:
		return True
	if pdgId >= 1000011 and pdgId <= 1000016:
		return True
	if pdgId >= 2000001 and pdgId <= 2000006:
		return True
	if pdgId >= 1000021 and pdgId <= 1000025:
		return True
	if pdgId == 2000011 or pdgId == 2000013 or pdgId == 2000015 or pdgId == 1000035 or pdgId == 1000037 or pdgId == 1000039:
		return True
	return False

def handleX10X20X10MET(event, nj, weight):
	met = event.MET
	utils.fillHistWithCuts("MET", met, histList, cutsDef, "ntuples", event, weight)
	if nj == 1:
		utils.fillHistWithCuts("MET1J", met, histList, cutsDef, "ntuples", event, weight)
	elif nj ==2:
		utils.fillHistWithCuts("MET2J", met, histList, cutsDef, "ntuples", event, weight)

def handleX10X20X10Cand(event, nj, weight):
	nL = event.Electrons.size() + event.Muons.size()
	ht = event.HT
	histList["HT"].Fill(ht)
	utils.fillHistWithCuts("HTWeight", ht, histList, cutsDef, "ntuples", event, weight)
	if nj == 1:
		utils.fillHistWithCuts("HT1J", ht, histList, cutsDef, "ntuples", event, weight)
	elif nj ==2:
		utils.fillHistWithCuts("HT2J", ht, histList, cutsDef, "ntuples", event, weight)
	utils.fillHistWithCuts("NLCan", nL, histList, cutsDef, "ntuples", event, weight)
	
	for lep in event.Electrons:
		utils.fillHistWithCuts("LPT", lep.Pt(), histList, cutsDef, "ntuples", event, weight)
		utils.fillHistWithCuts("LEta", lep.Eta(), histList, cutsDef, "ntuples", event, weight)
		utils.fillHistWithCuts("LPhi", lep.Phi(), histList, cutsDef, "ntuples", event, weight)
		if nj == 1:
			utils.fillHistWithCuts("LPT1J", lep.Pt(), histList, cutsDef, "ntuples", event, weight)
			utils.fillHistWithCuts("LEta1J", lep.Eta(), histList, cutsDef, "ntuples", event, weight)
			utils.fillHistWithCuts("LPhi1J", lep.Phi(), histList, cutsDef, "ntuples", event, weight)
		elif nj == 2:
			utils.fillHistWithCuts("LPT2J", lep.Pt(), histList, cutsDef, "ntuples", event, weight)
			utils.fillHistWithCuts("LEta2J", lep.Eta(), histList, cutsDef, "ntuples", event, weight)
			utils.fillHistWithCuts("LPhi2J", lep.Phi(), histList, cutsDef, "ntuples", event, weight)
	
	if nL == 2:
		if event.Electrons.size() == 2 and event.Electrons_charge[0] * event.Electrons_charge[1] < 0:
			handleX10X20X10DiLepton(event.Electrons[0], event.Electrons[1], event, nj, weight)
		elif event.Muons.size() == 2 and event.Muons_charge[0] * event.Muons_charge[1] < 0:
			handleX10X20X10DiLepton(event.Muons[0], event.Muons[1], event, nj, weight)

def handleX10X20X10DiLepton(l1, l2, event, nj, weight):
	invMass = (l1 + l2).M()
	deltaPhi = l1.DeltaPhi(l2)
	deltaEta = abs(l1.Eta() - l2.Eta())
	deltaR = l1.DeltaR(l2)
	utils.fillHistWithCuts("DuoLepCanInvMass", invMass, histList, cutsDef, "ntuples", event, weight)
	utils.fillHistWithCuts("DeltaRCan", deltaR, histList, cutsDef, "ntuples", event, weight)
	utils.fillHistWithCuts("DeltaEtaCan", deltaEta, histList, cutsDef, "ntuples", event, weight)
	utils.fillHistWithCuts("DeltaPhiCan", deltaPhi, histList, cutsDef, "ntuples", event, weight)
	if nj == 1:
		utils.fillHistWithCuts("DuoLepCanInvMass1J", invMass, histList, cutsDef, "ntuples", event, weight)
		utils.fillHistWithCuts("DeltaRCan1J", deltaR, histList, cutsDef, "ntuples", event, weight)
		utils.fillHistWithCuts("DeltaEtaCan1J", deltaEta, histList, cutsDef, "ntuples", event, weight)
		utils.fillHistWithCuts("DeltaPhiCan1J", deltaPhi, histList, cutsDef, "ntuples", event, weight)
	elif nj ==2:
		utils.fillHistWithCuts("DuoLepCanInvMass2J", invMass, histList, cutsDef, "ntuples", event, weight)
		utils.fillHistWithCuts("DeltaRCan2J", deltaR, histList, cutsDef, "ntuples", event, weight)
		utils.fillHistWithCuts("DeltaEtaCan2J", deltaEta, histList, cutsDef, "ntuples", event, weight)
		utils.fillHistWithCuts("DeltaPhiCan2J", deltaPhi, histList, cutsDef, "ntuples", event, weight)
	
def handleX10X20X10Jets(event, weight):
	jetsNum = 0
	for ijet in range(event.Jets.size()):
		jet = event.Jets[ijet]
		if jet.Pt() >= 30 and abs(jet.Eta()) <= 2.4:
			jetsNum +=1
	utils.fillHistWithCuts("NJ", jetsNum, histList, cutsDef, "ntuples", event, weight)
	return jetsNum

def handleX10X20X10NLGen(event, weight):
	partSize = event.GenParticles.size()
	nL = 0
	l1 = None
	l2 = None
	for ipart in range(partSize):
		part = event.GenParticles[ipart]
		if event.GenParticles_Status[ipart] == 1 and (abs(event.GenParticles_PdgId[ipart]) == 11 or abs(event.GenParticles_PdgId[ipart]) == 13):
			nL += 1
			minR = minDeltaR(ipart, event)
			if minR is not None:
				utils.fillHistWithCuts("DeltaRLepMatchCand", minR, histList, cutsDef, "ntuples", event, weight)
				if minR <= 0.1:
					utils.fillHistWithCuts("MatchLep", 1, histList, cutsDef, "ntuples", event, weight)
				else:
					utils.fillHistWithCuts("MatchLep", 0, histList, cutsDef, "ntuples", event, weight)
			else:
				#print("No minR")
				utils.fillHistWithCuts("MatchLep", 0, histList, cutsDef, "ntuples", event, weight)
			if l1 is None:
				l1 = ipart
			else:
				l2 = ipart
	utils.fillHistWithCuts("NLGen", nL, histList, cutsDef, "ntuples", event, weight)
	if nL == 2 and abs(event.GenParticles_PdgId[l1]) == abs(event.GenParticles_PdgId[l2]) and (event.GenParticles_PdgId[l1] * event.GenParticles_PdgId[l2] < 0):
		handleX10X20X10GenDiLepton(event, l1, l2, weight)

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

def handleX10X20X10GenDiLepton(event, l1, l2, weight):
	l1v = event.GenParticles[l1]
	l2v = event.GenParticles[l2]
	deltaPhi = l1v.DeltaPhi(l2v)
	deltaR = l1v.DeltaR(l2v)
	deltaEta = abs(l1v.Eta() - l2v.Eta())
	utils.fillHistWithCuts("DeltaPhiGen", deltaPhi, histList, cutsDef, "ntuples", event, weight)
	utils.fillHistWithCuts("DeltaRGen", deltaR, histList, cutsDef, "ntuples", event, weight)
	utils.fillHistWithCuts("DeltaEtaGen", deltaEta, histList, cutsDef, "ntuples", event, weight)

def isRightProcess(event):
	partSize = event.GenParticles.size()
	for ipart in range(partSize):
		if event.GenParticles_PdgId[ipart] == 1000022:
			#print("Found x10")
			if event.GenParticles_ParentId[ipart] == 1000023:
				#print("Mother x20")
				if not isSusy(event.GenParticles_ParentId[event.GenParticles_ParentIdx[ipart]]):
					#print("Found!!!")
					return True
	return False 
	

parser = argparse.ArgumentParser(description='Create BG histograms for x1x2x1 process.')
parser.add_argument('-i', '--input_file', nargs=1, help='Input Filename', required=True)
parser.add_argument('-o', '--output_file', nargs=1, help='Output Filename', required=True)
args = parser.parse_args()

input_file = args.input_file[0]
output_file = args.output_file[0]

c = TChain("TreeMaker2/PreSelection");
c.Add(input_file)

nentries = c.GetEntries()
print("nentries=" + str(nentries))

for ientry in range(nentries) :
	if ientry % 10000 == 0 :
		print("processing entry" , ientry, "out of", nentries)
	c.GetEntry(ientry)
	if isRightProcess(c):
		weight = 1
		nj = handleX10X20X10Jets(c, weight)
		handleX10X20X10MET(c, nj, weight)
		handleX10X20X10Cand(c, nj, weight)
		handleX10X20X10NLGen(c, weight)
		cuts.resetCuts(cutsDef)


fnew = TFile(output_file, "recreate")

sigma = 1215.47 #fb 
LUMINOSITY = 35.900 #1/fb
N = histList["HT"].Integral(-1,99999999)+0.000000000001

print("Number of HT event " + str(N))

weight = sigma * LUMINOSITY / N

utils.scaleHistograms(histList, histDefs, weight)
utils.writeHistograms(histList)
fnew.Close()

exit(0)

#################	END OF SCRIPT	##########################
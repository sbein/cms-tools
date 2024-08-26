#!/usr/bin/python3

from ROOT import *
from glob import glob
from math import *
import sys
from sys import exit
from array import array

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
histDefs.update(histograms.genHistDefs)

cutsDef = histograms.cutsDefs
histList = utils.createHistograms(histDefs, cutsDef)

def trimTree(particle):
	trimedParticle = particle
	while(trimedParticle.numberOfDaughters() == 1 and trimedParticle.pdgId() == trimedParticle.daughter(0).pdgId() and not trimedParticle.isLastCopy()):
			trimedParticle = trimedParticle.daughter(0)
	return trimedParticle

def printTree(particleRef, shouldTrimTree = False, space=0):
	particle = particleRef
	if shouldTrimTree:
		particle = trimTree(particle)
	delim = ""
	if space > 0:
		delim = "|- "
	print(("|  " * space) + delim + str(particle.pdgId()) + "(" + str(particle.status()) + ")" + "(" + str(particle.isLastCopy()) + ")")
	if particle.numberOfDaughters() == 0:
		return
	for p in range(particle.numberOfDaughters()):
		printTree(particle.daughter(p), shouldTrimTree, space + 1)

def handleX10X20X10Gen(x20, x10, event):
	utils.fillHistWithCuts("X1PT", x10.pt(), histList, cutsDef, "aod", event)
	utils.fillHistWithCuts("X2PT", x20.pt(), histList, cutsDef, "aod", event)
		
	# We know that x20 has three daughters
	p1 = None
	p2 = None
	for i in range(x20.numberOfDaughters()):
		if x20.daughter(i).pdgId() != 1000022:
			if p1 is None:
				p1 = trimTree(x20.daughter(i))
			else:
				p2 = trimTree(x20.daughter(i))
	p1v = TLorentzVector(p1.px(), p1.py(), p1.pz(), p1.energy())
	p2v = TLorentzVector(p2.px(), p2.py(), p2.pz(), p2.energy())
	invMass = (p1v + p2v).M()
	#print("invMass=" + str(invMass) + "(" + str(p1.pdgId())+","+str(p2.pdgId())+")" +"(" + str(p1.isElectron())+","+str(p2.isMuon())+")")
	utils.fillHistWithCuts("InvMassGen", invMass, histList, cutsDef, "aod", event)

def handleX10X20X10MET(event, nj):
	pfMET, pfMETLabel = Handle("vector<reco::PFMET>"), "pfMet"
	event.getByLabel(pfMETLabel, pfMET)
	met = pfMET.product().front().pt()
	utils.fillHistWithCuts("MET", met, histList, cutsDef, "aod", event)
	if nj == 1:
		utils.fillHistWithCuts("MET1J", met, histList, cutsDef, "aod", event)
	elif nj ==2:
		utils.fillHistWithCuts("MET2J", met, histList, cutsDef, "aod", event)

def handleX10X20X10Cand(event, nj):
	pfCandidates, pfCandidatesLabel = Handle("vector<reco::PFCandidate>"), "particleFlow"
	event.getByLabel(pfCandidatesLabel, pfCandidates)
	candidates = pfCandidates.product()
	nL = 0
	l1 = None
	l2 = None
	for i,cand in enumerate(candidates):
		if (abs(cand.pdgId()) == 11 or abs(cand.pdgId()) == 13) and cand.pt() >= 5:
			nL += 1
			utils.fillHistWithCuts("LPT", cand.pt(), histList, cutsDef, "aod", event)
			utils.fillHistWithCuts("LEta", cand.eta(), histList, cutsDef, "aod", event)
			utils.fillHistWithCuts("LPhi", cand.phi(), histList, cutsDef, "aod", event)
			
			if nj == 1:
				utils.fillHistWithCuts("LPT1J", cand.pt(), histList, cutsDef, "aod", event)
				utils.fillHistWithCuts("LEta1J", cand.eta(), histList, cutsDef, "aod", event)
				utils.fillHistWithCuts("LPhi1J", cand.phi(), histList, cutsDef, "aod", event)
			elif nj == 2:
				utils.fillHistWithCuts("LPT2J", cand.pt(), histList, cutsDef, "aod", event)
				utils.fillHistWithCuts("LEta2J", cand.eta(), histList, cutsDef, "aod", event)
				utils.fillHistWithCuts("LPhi2J", cand.phi(), histList, cutsDef, "aod", event)
			if l1 is None:
				l1 = cand
			else:
				l2 = cand
	utils.fillHistWithCuts("NLCan", nL, histList, cutsDef, "aod", event)
	if nL == 2 and abs(l1.pdgId()) == abs(l2.pdgId()) and l1.pdgId() * l2.pdgId() < 0:
		handleX10X20X10DiLepton(l1, l2, event, nj)

def handleX10X20X10DiLepton(l1, l2, event, nj):
	invMass = (l1.p4() + l2.p4()).M()
	
	l1v = TLorentzVector()
	l2v = TLorentzVector()
	l1v.SetPxPyPzE(l1.p4().px(), l1.p4().py(), l1.p4().pz(), l1.p4().e())
	l2v.SetPxPyPzE(l2.p4().px(), l2.p4().py(), l2.p4().pz(), l2.p4().e())
	
	
	deltaPhi = l1v.DeltaPhi(l2v)
	deltaEta = abs(l1v.Eta() - l2v.Eta())
	utils.fillHistWithCuts("DeltaPhiCan", deltaPhi, histList, cutsDef, "aod", event)
	utils.fillHistWithCuts("DeltaRCan", l1v.DeltaR(l2v), histList, cutsDef, "aod", event)	
	utils.fillHistWithCuts("DeltaEtaCan", deltaEta, histList, cutsDef, "aod", event)
	utils.fillHistWithCuts("DuoLepCanInvMass", invMass, histList, cutsDef, "aod", event)
	if nj == 1:
		utils.fillHistWithCuts("DuoLepCanInvMass1J", invMass, histList, cutsDef, "aod", event)
		utils.fillHistWithCuts("DeltaPhiCan1J", deltaPhi, histList, cutsDef, "aod", event)
		utils.fillHistWithCuts("DeltaRCan1J", l1v.DeltaR(l2v), histList, cutsDef, "aod", event)	
		utils.fillHistWithCuts("DeltaEtaCan1J", deltaEta, histList, cutsDef, "aod", event)
	elif nj ==2:
		utils.fillHistWithCuts("DuoLepCanInvMass2J", invMass, histList, cutsDef, "aod", event)
		utils.fillHistWithCuts("DeltaPhiCan2J", deltaPhi, histList, cutsDef, "aod", event)
		utils.fillHistWithCuts("DeltaRCan2J", l1v.DeltaR(l2v), histList, cutsDef, "aod", event)	
		utils.fillHistWithCuts("DeltaEtaCan2J", deltaEta, histList, cutsDef, "aod", event)
	
def handleX10X20X10Jets(event, onlyForCrossSection):
	ak4PFJets, ak4PFJetsLabel = Handle("vector<reco::PFJet>"), "ak4PFJetsCHS"
	event.getByLabel(ak4PFJetsLabel, ak4PFJets)
	jetsNum = 0
	jets = ak4PFJets.product()
	pt = 0
	for i,jet in enumerate(jets):
		if jet.pt() >= 30 and abs(jet.eta()) <= 2.4:
			jetsNum +=1
			pt += jet.pt()
	
	histList["HT"].Fill(pt)
		
	if onlyForCrossSection:	
		return
	
	utils.fillHistWithCuts("NJ", jetsNum, histList, cutsDef, "aod", event)
	utils.fillHistWithCuts("HTWeight", pt, histList, cutsDef, "aod", event)
	if jetsNum == 1:
		utils.fillHistWithCuts("HT1J", pt, histList, cutsDef, "aod", event)
	elif jetsNum ==2:
		utils.fillHistWithCuts("HT2J", pt, histList, cutsDef, "aod", event)
	return jetsNum

def handleX10X20X10NLGen(genParticles, event):
	particles = genParticles.product()
	nL = 0
	l1 = None
	l2 = None
	for i,part in enumerate(particles):
		if part.isPromptFinalState() and part.isLastCopy() and (abs(part.pdgId()) == 11 or abs(part.pdgId()) == 13):
			nL += 1
			minR, minCan = minDeltaR(part, event)
			utils.fillHistWithCuts("DeltaRLepMatchCand", minR, histList, cutsDef, "aod", event)
			if minCan.pdgId() == part.pdgId():
				utils.fillHistWithCuts("MatchLep", 1, histList, cutsDef, "aod", event)
			else:
				utils.fillHistWithCuts("MatchLep", 0, histList, cutsDef, "aod", event)
				#print(minCan.pdgId(), " ", part.pdgId())
			if l1 is None:
				l1 = part
			else:
				l2 = part
	utils.fillHistWithCuts("NLGen", nL, histList, cutsDef, "aod", event)
	if nL == 2 and abs(l1.pdgId()) == abs(l2.pdgId()) and l1.pdgId() * l2.pdgId() < 0:
		handleX10X20X10GenDiLepton(l1, l2, event)

def minDeltaR(gen, event):
	pfCandidates, pfCandidatesLabel = Handle("vector<reco::PFCandidate>"), "particleFlow"
	event.getByLabel(pfCandidatesLabel, pfCandidates)
	candidates = pfCandidates.product()
	minimum = None
	minCan = None
	genV = TLorentzVector(gen.px(), gen.py(), gen.pz(), gen.energy())
	for i, can in enumerate(candidates):
		if can.charge() == 0:
			continue
		canV = TLorentzVector(can.px(), can.py(), can.pz(), can.energy())
		deltaR = genV.DeltaR(canV)
		if minimum is None or deltaR < minimum:
			minimum = deltaR
			minCan = can
	return minimum, minCan

def handleX10X20X10GenDiLepton(l1, l2, event):
	l1v = TLorentzVector(l1.px(), l1.py(), l1.pz(), l1.energy())
	l2v = TLorentzVector(l2.px(), l2.py(), l2.pz(), l2.energy())
	deltaPhi = l1v.DeltaPhi(l2v)
	deltaEta = abs(l1v.Eta() - l2v.Eta())
	utils.fillHistWithCuts("DeltaPhiGen", deltaPhi, histList, cutsDef, "aod", event)
	utils.fillHistWithCuts("DeltaRGen", l1v.DeltaR(l2v), histList, cutsDef, "aod", event)	
	utils.fillHistWithCuts("DeltaEtaGen", deltaEta, histList, cutsDef, "aod", event)
	
	
def printEvent(genParticles):
	products = genParticles.product()
	for j,product in enumerate(products):
  		if product.pdgId() == 2212 and product.isLastCopy():
  			print("----------------")
   			printTree(product, True)
   			break

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

def process(events):
	numberOfX10X20X10Processes = 0
	for i,event in enumerate(events):
		rightX20ForCS = False
		passedEvent = False
		genParticles, genParticleLabel = Handle("vector<reco::GenParticle>"), "genParticles"
		event.getByLabel(genParticleLabel,genParticles)
		products = genParticles.product()
		rightX10 = False
		rightX20 = False
		x20 = None
		x10 = None
		#print("-----")
		for j,product in enumerate(products):
			pdgId = product.pdgId()
			
			if not rightX10 and pdgId == 1000022:
				if not isSusy(product.mother().pdgId()):
					rightX10 = True
					x10 = trimTree(product)
			
			if not rightX20 and pdgId == 1000023:
				if not isSusy(product.mother().pdgId()):
					x20 = trimTree(product)
					#get rid of photons
					if x20.numberOfDaughters() == 3:
						for l in range(x20.numberOfDaughters()): 
							if x20.daughter(l).pdgId() == 1000022: 
								rightX20 = True
					else:
						for l in range(x20.numberOfDaughters()): 
							if trimTree(x20.daughter(l)).pdgId() == 1000022: 
								rightX20ForCS = True
								break
			if rightX10 and (rightX20ForCS or rightX20):
				break
			
		if rightX10 and rightX20ForCS:
			# Add these only for the HT count
			handleX10X20X10Jets(event, True)
		elif rightX10 and rightX20:
			passedEvent = True
 					
 		if passedEvent:
 			numberOfX10X20X10Processes += 1
 			handleX10X20X10Gen(x20, x10, event)
			nj = handleX10X20X10Jets(event, False)
			handleX10X20X10MET(event, nj)
			handleX10X20X10Cand(event, nj)
			handleX10X20X10NLGen(genParticles, event)
		
		cuts.resetCuts(cutsDef)
 					
 	return numberOfX10X20X10Processes
 						

FileList = glob("/afs/desy.de/user/n/nissanuv/cms-tools/sim_x10x20x10/simData*");
#FileList = glob("/nfs/dust/cms/user/beinsam/NaturalSusy/Output/aodsim/pMSSM_MCMC1_38_870285_dm7*");

numberOfX10X20X10Processes = 0
for f in FileList : 
	events = Events(f)
	numberOfX10X20X10Processes += process(events)
	print("Processed ", numberOfX10X20X10Processes, " X10X20X10 events." )

print("-------------------------")
print("Processed ", numberOfX10X20X10Processes, " X10X20X10 events.")

fnew = TFile("x10x20x10.root", "recreate")

sigma = 50. #fb 
LUMINOSITY = 35.900 #1/fb
N = histList["HT"].Integral(-1,99999999)+0.000000000001

print("Number of HT event " + str(N))

weight = sigma * LUMINOSITY / N

utils.scaleHistograms(histList, histDefs, weight)
utils.writeHistograms(histList)

fnew.Close()

exit(0)

#################	END OF SCRIPT	##########################
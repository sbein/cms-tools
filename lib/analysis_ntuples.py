from ROOT import *
import sys

from lib import analysis_tools

BTAG_CSV_LOOSE = 0.5426
BTAG_CSV_MEDIUM = 0.8484
BTAG_CSV_LOOSE2 = 0.46

BTAG_DEEP_CSV_LOOSE = 0.2219
BTAG_DEEP_CSV_MEDIUM = 0.6324


BTAG_DEEP_CSV_MEDIUM_2016 = 0.6324
BTAG_DEEP_CSV_MEDIUM_2017 = 0.4941
BTAG_DEEP_CSV_MEDIUM_2018 = 0.4184

# def printTree(event, pId, space=0):
# 	particle = event.GenParticles[l1]
# 	delim = ""
# 	if space > 0:
# 		delim = "|- "
# 	print ("|  " * space) + delim + str(event.GenParticles_PdgId[pId])+"("+str(particle.E())+","+str(particle.Px())+","+str(particle.Py())+","+str(particle.Pz())")"
# 	if particle.numberOfDaughters() == 0:
# 		return
# 	for p in range(particle.numberOfDaughters()):
# 		printTree(particle.daughter(p), space + 1)

triggerIndeces = {}
triggerIndeces['MhtMet6pack'] = [124,109,110,111,112,114,115,116]#123
triggerIndeces['SingleMuon'] = [49,50,65]
triggerIndeces['SingleElectron'] = [36,37,39,40]

def passTrig(c,trigname):
    for trigidx in triggerIndeces[trigname]: 
        if c.TriggerPass[trigidx]==1: return True
        #print "Passing trigger %s, index:%s"%(c.TriggerNames[trigidx],trigidx)
    return False

def printTrigNames(c, trigname):
    print(",".join([ c.TriggerNames[trigidx] for trigidx in triggerIndeces[trigname]]))
        

def getTrigEffGraph(file, name):
    ttrig = file.Get(name)
    hpass = ttrig.GetPassedHistogram().Clone('hpass')
    htotal = ttrig.GetTotalHistogram().Clone('htotal')
    gtrig = TEfficiency(hpass, htotal)
    return gtrig

def minMaxCsv(jets, jets_bDiscriminatorCSV, pt):
    minimum = 1
    maximum = 0
    for ijet in range(jets.size()):
        jet = jets[ijet]
        if jet.Pt() >= pt and abs(jet.Eta()) <= 2.4:
            if jets_bDiscriminatorCSV[ijet] >= 0 and jets_bDiscriminatorCSV[ijet] < minimum:
                minimum = jets_bDiscriminatorCSV[ijet]
            if jets_bDiscriminatorCSV[ijet] >= 0 and jets_bDiscriminatorCSV[ijet] > maximum:
                maximum = jets_bDiscriminatorCSV[ijet]
    return minimum, maximum

def numberOfJets(jets, jets_bDiscriminatorCSV, pt, eta, csv):
    #print csv
    nj = 0
    btags = 0
    leadingJet = None
    for ijet in range(jets.size()):
        jet = jets[ijet]
        if jet.Pt() >= pt and abs(jet.Eta()) <= eta:
            nj +=1
            if leadingJet is None:
                leadingJet = ijet
            elif jet.Pt() > jets[leadingJet].Pt():
                leadingJet = ijet
            if jets_bDiscriminatorCSV[ijet] > csv:
                btags += 1
    return nj, btags, leadingJet


def eventNumberOfJets30Pt2_4Eta_Loose(jets, jets_bDiscriminatorCSV):
    return numberOfJets(jets, jets_bDiscriminatorCSV, 30, 2.4, BTAG_CSV_LOOSE)

def eventNumberOfJets30Pt2_4Eta_Medium(jets, jets_bDiscriminatorCSV):
    return numberOfJets(jets, jets_bDiscriminatorCSV, 30, 2.4, BTAG_CSV_MEDIUM)

def eventNumberOfJets30Pt2_4Eta_DeepLoose(jets, jets_bDiscriminatorCSV):
    return numberOfJets(jets, jets_bDiscriminatorCSV, 30, 2.4, BTAG_DEEP_CSV_LOOSE)
    
def eventNumberOfJets30Pt2_4Eta_DeepMedium(jets, jets_bDiscriminatorCSV):
    #print("Current value", BTAG_DEEP_CSV_MEDIUM)
    #exit(0)
    return numberOfJets(jets, jets_bDiscriminatorCSV, 30, 2.4, BTAG_DEEP_CSV_MEDIUM)

def numberOfLooseBTags(event):
    loose = 0
    for ijet in range(event.Jets_bDiscriminatorCSV.size()):
        if event.Jets_bDiscriminatorCSV[ijet] > BTAG_CSV_LOOSE:
            loose+=1
    return loose

def htJet30(event):
    leps = [l for l in event.Electrons] + [m for m in event.Muons]
    cleanJets = [ j for j in event.Jets if min(j.DeltaR(l) for l in leps) > 0.4 ]
    objects30 = [ j for j in cleanJets if j.Pt() > 30 ] + leps
    return sum([x.Pt() for x in objects30])

def htJet30Leps(jets, leps):
    cleanJets = [ j for j in jets if min(j.DeltaR(l) for l in leps) > 0.4 ]
    objects30 = [ j for j in cleanJets if j.Pt() > 30 ] + leps
    return sum([x.Pt() for x in objects30])

def minDeltaPhiMetJets(jets, MET, METPhi, pt, eta):
    jets = [ j for j in jets if j.Pt() > pt and abs(j.Eta()) <= eta ]
    if len(jets) == 0:
        return -1
    metvec = TLorentzVector()
    metvec.SetPtEtaPhiE(MET, 0, METPhi, MET)
    return min([abs(j.DeltaPhi(metvec)) for j in jets])

def minDeltaPhiMhtJets(jets, MHT, MHTPhi, pt, eta):
    jets = [ j for j in jets if j.Pt() > pt and abs(j.Eta()) <= eta ]
    if len(jets) == 0:
        return -1
    mhtvec = TLorentzVector()
    mhtvec.SetPtEtaPhiE(MHT, 0, MHTPhi, MHT)
    return min([abs(j.DeltaPhi(mhtvec)) for j in jets])

def minDeltaPhiMetJets30Pt2_4Eta(event):
    return minDeltaPhiMetJets(event.Jets, event.MET, event.METPhi, 30, 2.4)

def minDeltaPhiMhtJets30Pt2_4Eta(event):
    return minDeltaPhiMhtJets(event.Jets, event.MHT, event.MHTPhi, 30, 2.4)

def eventMinDeltaPhiMetJets30Pt2_4Eta(jets, MET, METPhi):
    return minDeltaPhiMetJets(jets, MET, METPhi, 30, 2.4)

def eventMinDeltaPhiMhtJets30Pt2_4Eta(jets, MHT, MHTPhi):
    return minDeltaPhiMhtJets(jets, MHT, MHTPhi, 30, 2.4)


def numberOfMediumBTags(event):
	#./analyzer_x1x2x1.py -bg -i /pnfs/desy.de/cms/tier2/store/user/sbein/CommonNtuples/Summer16.QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_24_RA2AnalysisTree.root -o test.root | tee output
	medium = 0
	for ijet in range(event.Jets_bDiscriminatorCSV.size()):
		if event.Jets_bDiscriminatorCSV[ijet] > BTAG_CSV_MEDIUM:
			jet = event.Jets[ijet]
			if jet.Pt() >= 30 and abs(jet.Eta()) <= 2.4:
				medium+=1
	# if medium != event.BTags:
#  		print "******"
#  		print "Jets= " + str(event.Jets_bDiscriminatorCSV.size()) + " BTags=" + str(event.BTags) + " medium=" + str(medium)
#  		for ijet in range(event.Jets_bDiscriminatorCSV.size()):
#  			print event.Jets_bDiscriminatorCSV[ijet]
	return medium

def isDuoTauEvent(event):
	partSize = event.GenParticles.size()
	if partSize == 0:
		print("No Taus!")
		return False
	nT = 0
	t1 = None
	t2 = None
	for ipart in range(partSize):
		if abs(event.GenParticles_PdgId[ipart]) == 15:
			nT += 1
			if t1 is None:
				t1 = ipart
			else:
				t2 = ipart
	
	# Is this a duo Tau event?
	if nT == 2 and (event.GenParticles_PdgId[t1] * event.GenParticles_PdgId[t2] < 0) and event.GenParticles_ParentId[t1] == 23 and event.GenParticles_ParentId[t2]:
		#print "Mother=" + str(event.GenParticles_ParentId[t1]) + " Mother2=" + str(event.GenParticles_ParentId[t2])
		return True
	return False
	
def isX1X2X1Process(event):
	partSize = event.GenParticles.size()
	for ipart in range(partSize):
		if event.GenParticles_PdgId[ipart] == 1000022:
			#print "Found x10"
			if event.GenParticles_ParentId[ipart] == 1000023:
				#print "Mother x20"
				if not analysis_tools.isSusy(event.GenParticles_ParentId[event.GenParticles_ParentIdx[ipart]]):
					#print "Found!!!"
					return True
	return False
	
def classifyGenZLeptons(c):
    genZL, genNonZL = [], []
    partSize = c.GenParticles.size()
    #print partSize
    for ipart in range(partSize):
        if c.GenParticles_Status[ipart] == 1 and (abs(c.GenParticles_PdgId[ipart]) == 11 or abs(c.GenParticles_PdgId[ipart]) == 13):
            if c.GenParticles_ParentId[ipart] == 1000023 or c.GenParticles_ParentId[ipart] == 23:
                genZL.append(ipart)
            else:
                genNonZL.append(ipart)
    if len(genZL) != 2 or (abs(c.GenParticles_PdgId[genZL[0]]) != abs(c.GenParticles_PdgId[genZL[1]])) or (c.GenParticles_PdgId[genZL[0]] * c.GenParticles_PdgId[genZL[1]] > 0 ):
        for i in genZL:
            print("PdgId" + str(i) + "=" + str(c.GenParticles_PdgId[i]))
        return None, None
    # if len(genNonZL) == 0:
    # 		print "===="
    # 		print "partSize=" + str(partSize)
    # 		print "genZL=" + str(len(genZL))
    # 		for ipart in range(partSize):
    # 			print c.GenParticles_PdgId[ipart]
    # 		print "===="
        
    return genZL, genNonZL

def isLeptonMatchedGen(genParticles, genParticles_PdgId, genL, genNL, lidx, leptons, leptonsCharge, lepSignedPdgId):
    l = leptons[lidx]
    minZ, minCanZ = minDeltaRGenParticles(l, genL, genParticles)
    minNZ, minCanNZ = minDeltaRGenParticles(l, genNL, genParticles)
    min = 0
    if minNZ is None or minZ < minNZ:
        min = minZ
    else:
        min = minNZ
    if min > 0.01:
        return False
    elif minNZ is None or minZ < minNZ:
        if lepSignedPdgId != 0:
            if genParticles_PdgId[minCanZ] == lepSignedPdgId * leptonsCharge[lidx]:
                return True
            else:
                return False
        else:
            # we only care of the sign
            if leptonsCharge[lidx] * genParticles_PdgId[minCanZ] < 0:
                return True
            else:
                return False
    return False

def minDeltaRGenParticles(l, gens, genParticles):
    min = None
    minCan = None

    for ipart in gens:
        genV = genParticles[ipart]
        deltaR = abs(genV.DeltaR(l))
        if min is None or deltaR < min:
            min = deltaR
            minCan = ipart
    return min, minCan

def minDeltaRLepTracks(l, c):
    return minDeltaLepLeps(l, c.tracks)

def minDeltaLepLeps(lep, leps):
    min, minCan = None, None
    for i, l in enumerate(leps):
        deltaR = abs(lep.DeltaR(l))
        if min is None or deltaR < min:
            min = deltaR
            minCan = i
    return min, minCan


def leadingLepton(c):
    ll = None
    for v in [e for e in c.Electrons] + [m for m in c.Muons]:
        if ll is None:
            ll = v
            continue
        if v.Pt() > ll.Pt():
            ll = v
    return ll

def electronPassesKinematicSelection(i, electrons, electrons_deltaRLJ):
    return electrons[i].Pt() <= 15 and (electrons_deltaRLJ[i] >= 0.4 or electrons_deltaRLJ[i] < 0)

def electronPassesLooseSelection(i, electrons, electrons_passIso):
    return bool(electrons_passIso[i])

def electronPassesTightSelection(i, electrons, electrons_passIso, electrons_deltaRLJ):
    #print electrons[i].Pt(), electrons_deltaRLJ[i], electrons_passIso[i], electronPassesLooseSelection(i, electrons, electrons_passIso)
    return electronPassesKinematicSelection(i, electrons, electrons_deltaRLJ) and electronPassesLooseSelection(i, electrons, electrons_passIso)

def muonPassesKinematicSelection(i, muons, muons_deltaRLJ, muonLowerPt = 2):
    #if muonLowerPt<2:
        #print "low pt", muonLowerPt
    return muons[i].Pt()>= muonLowerPt and muons[i].Pt() <= 15 and (muons_deltaRLJ[i] >= 0.4 or muons_deltaRLJ[i] < 0)

def muonPassesLooseSelection(i, muons, muons_mediumID, muons_deltaRLJ, muonLowerPt = 2, muonLowerPtTight = False, muons_tightID = None):
    if not muonPassesKinematicSelection(i, muons, muons_deltaRLJ, muonLowerPt):
        return False
    if muons[i].Pt() < 2 and muonLowerPtTight:
        #print "looking for tight!"
        return bool(muons_tightID[i])
    else:
        return bool(muons_mediumID[i])

def muonPassesJetIsoSelection(i, muons, muons_mediumID):
    return bool(muons_mediumID[i]) and muons[i].Pt() > 2

def muonPassesTightSelection(i, muons, muons_mediumID, muons_passJetIso, muons_deltaRLJ, muonLowerPt = 2, muonLowerPtTight = False, muons_tightID = None):
    return muonPassesLooseSelection(i, muons, muons_mediumID, muons_deltaRLJ, muonLowerPt, muonLowerPtTight, muons_tightID) and bool(muons_passJetIso[i])

def getSingleLeptonAfterSelection(Electrons, Electrons_passJetIso, Electrons_deltaRLJ, Electrons_charge, Muons, Muons_passJetIso, Muons_mediumID, Muons_deltaRLJ, Muons_charge, muonLowerPt = 2, muonLowerPtTight = False, muons_tightID = None):
    lep = None
    lepCharge = None
    lepFlavour = None
    lepIdx = None
    nL = 0
    
    for i in range(Electrons.size()):
        e = Electrons[i]
        if electronPassesTightSelection(i, Electrons, Electrons_passJetIso, Electrons_deltaRLJ):
            nL += 1
            if nL > 1:
                return None, None, None, None
            lep = e
            lepCharge = Electrons_charge[i]
            lepFlavour = "Electrons"
            lepIdx = i
    for i in range(Muons.size()):
        m = Muons[i]
        if muonPassesTightSelection(i, Muons, Muons_mediumID, Muons_passJetIso, Muons_deltaRLJ, muonLowerPt, muonLowerPtTight, muons_tightID):
            nL += 1
            if nL > 1:
                return None, None, None, None
            lep = m
            lepCharge = Muons_charge[i]
            lepFlavour = "Muons"
            lepIdx = i
    
    return lep, lepIdx, lepCharge, lepFlavour

def countLeptonsAfterSelection(Electrons, Electrons_passJetIso, Electrons_deltaRLJ, Electrons_charge, Muons, Muons_passJetIso, Muons_mediumID, Muons_deltaRLJ, Muons_charge, muonLowerPt = 2, muonLowerPtTight = False, muons_tightID = None):
    nL = 0
    for i in range(Electrons.size()):
        e = Electrons[i]
        #print e, e.Pt(), bool(Electrons_passJetIso[i]), Electrons_deltaRLJ[i]
        if electronPassesTightSelection(i, Electrons, Electrons_passJetIso, Electrons_deltaRLJ):
            #print "here..."
            nL += 1
    for i in range(Muons.size()):
        m = Muons[i]
        if muonPassesTightSelection(i, Muons, Muons_mediumID, Muons_passJetIso, Muons_deltaRLJ, muonLowerPt, muonLowerPtTight, muons_tightID):
            nL += 1
    return nL

def hasHighPtJpsiMuon(highPtLeptonPtThreshold, Leptons, Leptons_passIso, leptons_tightID):
    for i in range(Leptons.size()):
        if Leptons[i].Pt() < highPtLeptonPtThreshold or not bool(Leptons_passIso[i]) or Leptons[i].Eta() > 2.4 or not bool(leptons_tightID[i]):
            continue
        return i
    return None

def hasHighPtJpsiElectron(highPtLeptonPtThreshold, Leptons):
    for i in range(Leptons.size()):
        if Leptons[i].Pt() < highPtLeptonPtThreshold:
            continue
        return i
    return None
    
def isleptonPassesJpsiSelection(i, lowPtLeptonPtThreshold, Leptons, Leptons_passJetIso, Leptons_mediumID, leptonLowerPt = 2, leptonLowerPtTight = False, leptons_tightID = None):
    if Leptons[i].Pt() > lowPtLeptonPtThreshold or Leptons[i].Pt() < leptonLowerPt:
        return False
    if Leptons[i].Eta() > 2.4 or not bool(Leptons_passJetIso[i]):
        return False
    if Leptons[i].Pt() < leptonLowerPt and (leptonLowerPtTight and not bool(leptons_tightID[i])):
        return False
    elif not bool(Leptons_mediumID[i]):
        return False
    return True

def isleptonPassesJpsiTagSelection(i, leptonLowerPt, Leptons, Leptons_passIso, Leptons_mediumID):
    if Leptons[i].Pt() < leptonLowerPt or Leptons[i ].Eta() > 2.4 or not bool(Leptons_mediumID[i]):
        return False
    return True

def isTrackPassesProbeJpsiSelection(tagI, probeI, probeLowerPt, probeHigherPt, Leptons, Leptons_charge, tracks, tracks_charge, lowEdge = 2.0, highEdge = 4.0):
    if tracks[probeI].Pt() < probeLowerPt or tracks[probeI].Pt() > probeHigherPt:
        return False
    if Leptons_charge[tagI] * tracks_charge[probeI] > 0:
        return False    
    
    mTrack = TLorentzVector()
    track = tracks[probeI]
    mTrack.SetXYZM(track.X(), track.Y(), track.Z(), 0.1057)
    invMass = (Leptons[tagI] + mTrack).M()
    if invMass < lowEdge or invMass > highEdge:
        return False
    #print "invMass", invMass, "lowEdge", lowEdge, "highEdge", highEdge
    return True
    

def getSingleJPsiLeptonAfterSelection(highPtLeptonPtThreshold, lowPtLeptonPtThreshold, Leptons, Leptons_passJetIso, Leptons_mediumID, Leptons_charge, tracks, tracks_charge, leptonLowerPt = 2, leptonLowerPtTight = False, leptons_tightID = None, Leptons_passIso = None):
    if Leptons.size() < 2:
        return None, None, None, None
    highPtLeptonIdx = hasHighPtJpsiMuon(highPtLeptonPtThreshold, Leptons, Leptons_passIso, leptons_tightID)
    if highPtLeptonIdx is None:
        return None, None, None, None
    highPtLepton = Leptons[highPtLeptonIdx]
    ll, leptonIdx, t, ti = None, None, None, None
    found = False
    for i in range(Leptons.size()):
        if i == 0:
            continue
        if not isleptonPassesJpsiSelection(i, lowPtLeptonPtThreshold, Leptons, Leptons_passJetIso, Leptons_mediumID, leptonLowerPt, leptonLowerPtTight, leptons_tightID):
            continue
        
        for j in range(len(tracks)):
            if Leptons_charge[i] * tracks_charge[j] > 0:
                continue
            if (Leptons[i] + tracks[j]).M() < 2.5 or (Leptons[i] + tracks[j]).M() > 3.5:
                continue
            
            ll, leptonIdx, t, ti = Leptons[i], i, tracks[j], j
        
            found = True
            break
        
        if found:
            break
    
    return ll, leptonIdx, t, ti

def getTwoJPsiLeptonsAfterSelection(highPtLeptonPtThreshold, lowPtLeptonPtThreshold, Leptons, Leptons_passJetIso, Leptons_mediumID, Leptons_charge, leptonLowerPt = 2, leptonLowerPtTight = False, leptons_tightID = None, Leptons_passIso = None):
    if Leptons.size() < 3:
        return None, None, None
    highPtLeptonIdx = hasHighPtJpsiMuon(highPtLeptonPtThreshold, Leptons, Leptons_passIso, leptons_tightID)
    if highPtLeptonIdx is None:
        return None, None, None
    highPtLepton = Leptons[highPtLeptonIdx]
    jpsiLeptons = []
    for i in range(Leptons.size()):
        if not isleptonPassesJpsiSelection(i, lowPtLeptonPtThreshold, Leptons, Leptons_passJetIso, Leptons_mediumID, leptonLowerPt, leptonLowerPtTight, leptons_tightID):
            continue
        if len(jpsiLeptons) == 0:
            jpsiLeptons.append(i)
        elif Leptons_charge[jpsiLeptons[0]] * Leptons_charge[i] > 0:
            continue
        elif (Leptons[jpsiLeptons[0]] + Leptons[i]).M() < 2.5 or (Leptons[jpsiLeptons[0]] + Leptons[i]).M() > 3.5:
            continue
        else:
            jpsiLeptons.append(i)
            break
        
    if len(jpsiLeptons) == 2:
        l1 = Leptons[jpsiLeptons[0]]
        l2 = Leptons[jpsiLeptons[1]]
        return [l1, l2], [jpsiLeptons[0], jpsiLeptons[1]], [Leptons_charge[jpsiLeptons[0]], Leptons_charge[jpsiLeptons[1]]]
    
    return None, None, None

def getTwoLeptonsAfterSelection(Electrons, Electrons_passJetIso, Electrons_deltaRLJ, Electrons_charge, Muons, Muons_passJetIso, Muons_mediumID, Muons_deltaRLJ, Muons_charge, muonLowerPt = 2, muonLowerPtTight = False, muons_tightID = None, createJetIsoCr = False, Electrons_passJetCrIso = None, Muons_passJetCrIso = None, Electrons_minDrD3Iso = None, Muons_minDrD3Iso = None):
    leps = []
    lepCharges = []
    lepIdx = []
    lepFlavour = None
    nL = 0
    jetIsoCr = 0
    minDrJetIsoCr = -1
    
    for i in range(Electrons.size()):
        e = Electrons[i]
        #print e, e.Pt(), bool(Electrons_passJetIso[i]), Electrons_deltaRLJ[i]
        if electronPassesTightSelection(i, Electrons, Electrons_passJetIso, Electrons_deltaRLJ):
            #print "here..."
            nL += 1
            if nL > 2:
                return None, None, None, None, None, None, None
            leps.append(e)
            lepIdx.append(i)
            lepCharges.append(Electrons_charge[i])
            lepFlavour = "Electrons"
    if createJetIsoCr and nL < 2:
        for i in range(Electrons.size()):
            e = Electrons[i]
            #print e, e.Pt(), bool(Electrons_passJetIso[i]), Electrons_deltaRLJ[i]
            if electronPassesTightSelection(i, Electrons, Electrons_passJetCrIso, Electrons_deltaRLJ):
                #print "here..."
                nL += 1
                if nL > 2:
                    return None, None, None, None, None, None, None
                leps.append(e)
                lepIdx.append(i)
                lepCharges.append(Electrons_charge[i])
                jetIsoCr += 1
                lepFlavour = "Electrons"
                if minDrJetIsoCr == -1:
                    minDrJetIsoCr = Electrons_minDrD3Iso[i]
                else:
                    minDrJetIsoCr = min(minDrJetIsoCr, Electrons_minDrD3Iso[i])
        
    if nL == 1 and jetIsoCr == 0:
        return None, None, None, None, None, None, None
    elif nL == 1 and jetIsoCr == 1:
        # reset - we don't care about a single CR electron
        leps = []
        lepCharges = []
        lepIdx = []
        lepFlavour = None
        nL = 0
        jetIsoCr = 0
        minDrJetIsoCr = -1
    
    for i in range(Muons.size()):
        m = Muons[i]
        if muonPassesTightSelection(i, Muons, Muons_mediumID, Muons_passJetIso, Muons_deltaRLJ, muonLowerPt, muonLowerPtTight, muons_tightID):
            nL += 1
            if nL > 2:
                return None, None, None, None, None, None, None
            leps.append(m)
            lepIdx.append(i)
            lepCharges.append(Muons_charge[i])
            lepFlavour = "Muons"
    
    if nL < 2 and createJetIsoCr:
        for i in range(Muons.size()):
            m = Muons[i]
            if muonPassesTightSelection(i, Muons, Muons_mediumID, Muons_passJetCrIso, Muons_deltaRLJ, muonLowerPt, muonLowerPtTight, muons_tightID):
                nL += 1
                if nL > 2:
                    return None, None, None, None, None, None, None
                leps.append(m)
                lepIdx.append(i)
                lepCharges.append(Muons_charge[i])
                lepFlavour = "Muons"
                jetIsoCr += 1
                if minDrJetIsoCr == -1:
                    minDrJetIsoCr = Muons_minDrD3Iso[i]
                else:
                    minDrJetIsoCr = min(minDrJetIsoCr, Muons_minDrD3Iso[i])
    
    if nL != 2:
        return None, None, None, None, None, None, None
    
    if lepIdx[0] == lepIdx[1]:
        print("How can two leptons have same idx?!")
        exit(1)
        
    same_sign = False
    if lepCharges[0] * lepCharges[1] > 0:
        same_sign = True
    
    if leps[0].Pt() < leps[1].Pt():
        leps = [leps[1], leps[0]]
        lepIdx = [lepIdx[1], lepIdx[0]]
        lepCharges = [lepCharges[1], lepCharges[0]]
    
    #if lepFlavour == "Electrons":
    #    print "YEY!!!"
    
    return leps, lepIdx, lepCharges, lepFlavour, same_sign, jetIsoCr, minDrJetIsoCr

################## FILTERS ##################

def passed2016BFilter(t, data=False):
    if not t.globalSuperTightHalo2016Filter: return False
    if not t.HBHENoiseFilter: return False    
    if not t.HBHEIsoNoiseFilter: return False
    if not t.eeBadScFilter: return False      
    if not t.BadChargedCandidateFilter: return False
    if not t.BadPFMuonFilter: return False
    if not t.CSCTightHaloFilter: return False 
    if not t.EcalDeadCellTriggerPrimitiveFilter: return False
    #if data:
    #    if not t.ecalBadCalibReducedExtraFilter: return False
    #    if not t.ecalBadCalibReducedFilter: return False
    return True

def mkmet(metPt, metPhi):
    met = TLorentzVector()
    met.SetPtEtaPhiE(metPt, 0, metPhi, metPt)
    return met

def passQCDHighMETFilter(t, MET, METPhi):
    metvec = mkmet(MET, METPhi)
    for ijet, jet in enumerate(t.Jets):
        if not (jet.Pt() > 200): continue
        if not (t.Jets_muonEnergyFraction[ijet]>0.5):continue 
        if (abs(jet.DeltaPhi(metvec)) > (3.14159 - 0.4)): return False
    return True


def passQCDHighMETFilter2(t, MET, METPhi):
    if len(t.Jets)>0:
        metvec = TLorentzVector()
        metvec.SetPtEtaPhiE(MET, 0, METPhi,0)
        if abs(t.Jets[0].DeltaPhi(metvec))>(3.14159-0.4) and t.Jets_neutralEmEnergyFraction[0]<0.03:
            return False
    return True

# def passesUniversalSelection(t, MET, METPhi):
#     if not bool(t.JetID): return False
#     if not t.NVtx>0: return False
#     if not passQCDHighMETFilter(t, MET, METPhi): return False
#     if not passQCDHighMETFilter2(t, MET, METPhi): return False
#     if not t.HBHENoiseFilter: return False    
#     if not t.HBHEIsoNoiseFilter: return False
#     if not t.eeBadScFilter: return False      
#     if not t.BadChargedCandidateFilter: return False
#     if not t.BadPFMuonFilter: return False
#     if not t.CSCTightHaloFilter: return False
#     if not t.EcalDeadCellTriggerPrimitiveFilter: return False      ##I think this one makes a sizeable difference    
#     return True


######### FROM VIKTOR ################

def passesUniversalSelection(t, MET, METPhi):
    #if not bool(t.JetID): return False
    if not t.PrimaryVertexFilter: return False
    if not t.globalSuperTightHalo2016Filter: return False
    if not t.HBHENoiseFilter: return False  
    if not t.HBHEIsoNoiseFilter: return False
    if not t.EcalDeadCellTriggerPrimitiveFilter: return False   ##I think this one makes a sizeable difference    
    if not t.BadPFMuonFilter: return False
    if not t.NVtx>0: return False
    
    
    
    
    if not passQCDHighMETFilter(t, MET, METPhi): return False
    if not passQCDHighMETFilter2(t, MET, METPhi): return False
    if not t.CSCTightHaloFilter: return False
    
    return True


def passesUniversalSelectionFastSim(t, MET, METPhi):
    #if not bool(t.JetID): return False
    # Recommended but not found in ntuples:
    # if not t.PrimaryVertexFilter: return False
#     if not t.HBHENoiseFilter: return False  
#     if not t.HBHEIsoNoiseFilter: return False
#     if not t.EcalDeadCellTriggerPrimitiveFilter: return False
#     if not t.BadPFMuonFilter: return False
   
    #if not t.NVtx>0: return False
    
    if not passQCDHighMETFilter(t, MET, METPhi): return False
    if not passQCDHighMETFilter2(t, MET, METPhi): return False
    return True    

def passesUniversalDataSelection(t, MET, METPhi):
    #if not bool(t.JetID) and
    if not t.PrimaryVertexFilter: return False
    if not t.globalSuperTightHalo2016Filter: return False
    if not t.HBHENoiseFilter: return False 
    if not t.HBHEIsoNoiseFilter: return False
    if not t.EcalDeadCellTriggerPrimitiveFilter: return False
    if not t.BadPFMuonFilter: return False
    if not t.BadChargedCandidateFilter: return False
    if not t.eeBadScFilter: return False
    if not t.NVtx>0: return False
    

    if not passQCDHighMETFilter(t, MET, METPhi): return False
    if not passQCDHighMETFilter2(t, MET, METPhi): return False
    if not t.CSCTightHaloFilter: return False
    
    
    #if not t.PFCaloMETRatio<5: return False
                             
    return True

# ORIGINAL
# def passesUniversalSelection(t, MET, METPhi):
#     if not bool(t.JetID): return False
#     if not t.NVtx>0: return False
#     if not passQCDHighMETFilter(t, MET, METPhi): return False
#     if not passQCDHighMETFilter2(t, MET, METPhi): return False
#     if not t.HBHENoiseFilter: return False    
#     if not t.HBHEIsoNoiseFilter: return False
#     if not t.eeBadScFilter: return False      
#     if not t.BadChargedCandidateFilter: return False
#     if not t.BadPFMuonFilter: return False
#     if not t.CSCTightHaloFilter: return False
#     if not t.EcalDeadCellTriggerPrimitiveFilter: return False      ##I think this one makes a sizeable difference    
#     return True


##############################################

#[36,37,39,40]
'''
0 HLT_AK8DiPFJet250_200_TrimMass30_v 0 15
1 HLT_AK8DiPFJet280_200_TrimMass30_v 0 10
2 HLT_AK8DiPFJet300_200_TrimMass30_v -1 1
3 HLT_AK8PFHT700_TrimR0p1PT0p03Mass50_v 0 1
4 HLT_AK8PFHT800_TrimMass50_v -1 1
5 HLT_AK8PFHT850_TrimMass50_v -1 1
6 HLT_AK8PFHT900_TrimMass50_v -1 1
7 HLT_AK8PFJet360_TrimMass30_v 0 1
8 HLT_AK8PFJet400_TrimMass30_v -1 1
9 HLT_AK8PFJet420_TrimMass30_v -1 1
10 HLT_AK8PFJet450_v -1 1
11 HLT_AK8PFJet500_v -1 1
12 HLT_AK8PFJet550_v -1 1
13 HLT_CaloJet500_NoJetID_v 0 1
14 HLT_CaloJet550_NoJetID_v -1 1
15 HLT_DiCentralPFJet55_PFMET110_v 0 1
16 HLT_DiPFJet40_DEta3p5_MJJ600_PFMETNoMu140_v 0 1
17 HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_DZ_PFHT350_v -1 1
18 HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_PFHT300_v 0 1
19 HLT_DoubleMu8_Mass8_PFHT300_v 0 1
20 HLT_DoubleMu8_Mass8_PFHT350_v -1 1
21 HLT_Ele105_CaloIdVT_GsfTrkIdT_v 0 1
22 HLT_Ele115_CaloIdVT_GsfTrkIdT_v 0 1
23 HLT_Ele135_CaloIdVT_GsfTrkIdT_v -1 1
24 HLT_Ele145_CaloIdVT_GsfTrkIdT_v -1 1
25 HLT_Ele15_IsoVVVL_PFHT350_PFMET50_v 0 1
26 HLT_Ele15_IsoVVVL_PFHT350_v 0 1
27 HLT_Ele15_IsoVVVL_PFHT400_v -1 1
28 HLT_Ele15_IsoVVVL_PFHT450_CaloBTagCSV_4p5_v -1 1
29 HLT_Ele15_IsoVVVL_PFHT450_PFMET50_v -1 1
30 HLT_Ele15_IsoVVVL_PFHT450_v -1 1
31 HLT_Ele15_IsoVVVL_PFHT600_v 0 1
32 HLT_Ele20_WPLoose_Gsf_v -1 1
33 HLT_Ele20_eta2p1_WPLoose_Gsf_v -1 1
34 HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v 0 1
35 HLT_Ele25_eta2p1_WPTight_Gsf_v 0 1
36 HLT_Ele27_WPTight_Gsf_v 0 1
37 HLT_Ele27_eta2p1_WPLoose_Gsf_v 0 1
38 HLT_Ele28_eta2p1_WPTight_Gsf_HT150_v -1 1
39 HLT_Ele32_WPTight_Gsf_v -1 1
40 HLT_Ele35_WPTight_Gsf_v -1 1
41 HLT_Ele45_WPLoose_Gsf_v 0 1
42 HLT_Ele50_IsoVVVL_PFHT400_v -1 1
43 HLT_Ele50_IsoVVVL_PFHT450_v -1 1
44 HLT_IsoMu16_eta2p1_MET30_v 0 1
45 HLT_IsoMu20_v 0 1
46 HLT_IsoMu22_eta2p1_v -1 1
47 HLT_IsoMu22_v 0 1
48 HLT_IsoMu24_eta2p1_v -1 1
49 HLT_IsoMu24_v 0 1
50 HLT_IsoMu27_v 0 1
51 HLT_IsoTkMu22_v 0 1
52 HLT_IsoTkMu24_v 0 1
53 HLT_Mu15_IsoVVVL_PFHT350_PFMET50_v 0 1
54 HLT_Mu15_IsoVVVL_PFHT350_v 0 1
55 HLT_Mu15_IsoVVVL_PFHT400_v -1 1
56 HLT_Mu15_IsoVVVL_PFHT450_CaloBTagCSV_4p5_v -1 1
57 HLT_Mu15_IsoVVVL_PFHT450_PFMET50_v -1 1
58 HLT_Mu15_IsoVVVL_PFHT450_v -1 1
59 HLT_Mu15_IsoVVVL_PFHT600_v 0 1
60 HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v 0 1
61 HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v 0 1
62 HLT_Mu45_eta2p1_v 0 1
63 HLT_Mu50_IsoVVVL_PFHT400_v -1 1
64 HLT_Mu50_IsoVVVL_PFHT450_v -1 1
65 HLT_Mu50_v 0 1
66 HLT_Mu55_v 0 1
67 HLT_PFHT1050_v -1 1
68 HLT_PFHT180_v -1 1
69 HLT_PFHT200_v 0 1
70 HLT_PFHT250_v 0 1
71 HLT_PFHT300_PFMET100_v 0 1
72 HLT_PFHT300_PFMET110_v 0 1
73 HLT_PFHT300_v 0 512
74 HLT_PFHT350_v 0 256
75 HLT_PFHT370_v -1 1
76 HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2_v -1 1
77 HLT_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2_v -1 1
78 HLT_PFHT380_SixPFJet32_v -1 1
79 HLT_PFHT400_SixJet30_DoubleBTagCSV_p056_v 0 1
80 HLT_PFHT400_SixJet30_v 0 2
81 HLT_PFHT400_v 0 128
82 HLT_PFHT430_SixJet40_BTagCSV_p056_v -1 1
83 HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5_v -1 1
84 HLT_PFHT430_SixPFJet40_v -1 1
85 HLT_PFHT430_v -1 1
86 HLT_PFHT450_SixJet40_BTagCSV_p056_v 0 1
87 HLT_PFHT450_SixJet40_v 0 1
88 HLT_PFHT450_SixPFJet40_PFBTagCSV_1p5_v -1 1
89 HLT_PFHT475_v 0 64
90 HLT_PFHT500_PFMET100_PFMHT100_IDTight_v -1 1
91 HLT_PFHT500_PFMET110_PFMHT110_IDTight_v -1 1
92 HLT_PFHT510_v -1 1
93 HLT_PFHT590_v -1 1
94 HLT_PFHT600_v 0 16
95 HLT_PFHT650_WideJetMJJ900DEtaJJ1p5_v 0 1
96 HLT_PFHT650_v 0 8
97 HLT_PFHT680_v -1 1
98 HLT_PFHT700_PFMET85_PFMHT85_IDTight_v -1 1
99 HLT_PFHT700_PFMET95_PFMHT95_IDTight_v -1 1
100 HLT_PFHT780_v -1 1
101 HLT_PFHT800_PFMET75_PFMHT75_IDTight_v -1 1
102 HLT_PFHT800_PFMET85_PFMHT85_IDTight_v -1 1
103 HLT_PFHT800_v 0 1
104 HLT_PFHT890_v -1 1
105 HLT_PFHT900_v 0 1
106 HLT_PFJet450_v 0 1
107 HLT_PFJet500_v 0 1
108 HLT_PFJet550_v -1 1
109 HLT_PFMET100_PFMHT100_IDTight_PFHT60_v -1 1
110 HLT_PFMET100_PFMHT100_IDTight_v 0 1
111 HLT_PFMET110_PFMHT110_IDTight_PFHT60_v -1 1
112 HLT_PFMET110_PFMHT110_IDTight_v 0 1
113 HLT_PFMET120_PFMHT120_IDTight_HFCleaned_v -1 1
114 HLT_PFMET120_PFMHT120_IDTight_PFHT60_HFCleaned_v -1 1
115 HLT_PFMET120_PFMHT120_IDTight_PFHT60_v -1 1
116 HLT_PFMET120_PFMHT120_IDTight_v 0 1
117 HLT_PFMET130_PFMHT130_IDTight_PFHT60_v -1 1
118 HLT_PFMET130_PFMHT130_IDTight_v -1 1
119 HLT_PFMET140_PFMHT140_IDTight_PFHT60_v -1 1
120 HLT_PFMET140_PFMHT140_IDTight_v -1 1
121 HLT_PFMET500_PFMHT500_IDTight_CalBTagCSV_3p1_v -1 1
122 HLT_PFMET700_PFMHT700_IDTight_CalBTagCSV_3p1_v -1 1
123 HLT_PFMET800_PFMHT800_IDTight_CalBTagCSV_3p1_v -1 1
124 HLT_PFMET90_PFMHT90_IDTight_v 0 1
125 HLT_PFMETNoMu100_PFMHTNoMu100_IDTight_PFHT60_v -1 1
126 HLT_PFMETNoMu100_PFMHTNoMu100_IDTight_v 0 1
127 HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_PFHT60_v -1 1
128 HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_v 0 1
129 HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_HFCleaned_v -1 1
130 HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60_v -1 1
131 HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v 0 1
132 HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_PFHT60_v -1 1
133 HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_v -1 1
134 HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_PFHT60_v -1 1
135 HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v -1 1
136 HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v 0 1
137 HLT_Photon135_PFMET100_v 0 1
138 HLT_Photon165_HE10_v 0 1
139 HLT_Photon165_R9Id90_HE10_IsoM_v 0 1
140 HLT_Photon175_v 0 1
141 HLT_Photon200_v -1 1
142 HLT_Photon300_NoHE_v 0 1
143 HLT_Photon90_CaloIdL_PFHT500_v 0 1
144 HLT_Photon90_CaloIdL_PFHT600_v 0 1
145 HLT_Photon90_CaloIdL_PFHT700_v -1 1
146 HLT_TkMu100_v -1 1
147 HLT_TkMu50_v -1 1
0 HLT_AK8DiPFJet250_200_TrimMass30_v 15 0.0
1 HLT_AK8DiPFJet280_200_TrimMass30_v 10 0.0
2 HLT_AK8DiPFJet300_200_TrimMass30_v 1 0.0
3 HLT_AK8PFHT700_TrimR0p1PT0p03Mass50_v 1 0.0
4 HLT_AK8PFHT800_TrimMass50_v 1 0.0
5 HLT_AK8PFHT850_TrimMass50_v 1 0.0
6 HLT_AK8PFHT900_TrimMass50_v 1 0.0
7 HLT_AK8PFJet360_TrimMass30_v 1 0.0
8 HLT_AK8PFJet400_TrimMass30_v 1 0.0
9 HLT_AK8PFJet420_TrimMass30_v 1 0.0
10 HLT_AK8PFJet450_v 1 0.0
11 HLT_AK8PFJet500_v 1 0.0
12 HLT_AK8PFJet550_v 1 0.0
13 HLT_CaloJet500_NoJetID_v 1 0.0
14 HLT_CaloJet550_NoJetID_v 1 0.0
15 HLT_DiCentralPFJet55_PFMET110_v 1 0.0
16 HLT_DiPFJet40_DEta3p5_MJJ600_PFMETNoMu140_v 1 0.0
17 HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_DZ_PFHT350_v 1 0.0
18 HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_PFHT300_v 1 0.0
19 HLT_DoubleMu8_Mass8_PFHT300_v 1 0.0
20 HLT_DoubleMu8_Mass8_PFHT350_v 1 0.0
21 HLT_Ele105_CaloIdVT_GsfTrkIdT_v 1 0.0
22 HLT_Ele115_CaloIdVT_GsfTrkIdT_v 1 0.0
23 HLT_Ele135_CaloIdVT_GsfTrkIdT_v 1 0.0
24 HLT_Ele145_CaloIdVT_GsfTrkIdT_v 1 0.0
25 HLT_Ele15_IsoVVVL_PFHT350_PFMET50_v 1 0.0
26 HLT_Ele15_IsoVVVL_PFHT350_v 1 0.0
27 HLT_Ele15_IsoVVVL_PFHT400_v 1 0.0
28 HLT_Ele15_IsoVVVL_PFHT450_CaloBTagCSV_4p5_v 1 0.0
29 HLT_Ele15_IsoVVVL_PFHT450_PFMET50_v 1 0.0
30 HLT_Ele15_IsoVVVL_PFHT450_v 1 0.0
31 HLT_Ele15_IsoVVVL_PFHT600_v 1 0.0
32 HLT_Ele20_WPLoose_Gsf_v 1 0.0
33 HLT_Ele20_eta2p1_WPLoose_Gsf_v 1 0.0
34 HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v 1 0.0
35 HLT_Ele25_eta2p1_WPTight_Gsf_v 1 0.0
36 HLT_Ele27_WPTight_Gsf_v 1 0.0
37 HLT_Ele27_eta2p1_WPLoose_Gsf_v 1 0.0
38 HLT_Ele28_eta2p1_WPTight_Gsf_HT150_v 1 0.0
39 HLT_Ele32_WPTight_Gsf_v 1 0.0
40 HLT_Ele35_WPTight_Gsf_v 1 0.0
41 HLT_Ele45_WPLoose_Gsf_v 1 0.0
42 HLT_Ele50_IsoVVVL_PFHT400_v 1 0.0
43 HLT_Ele50_IsoVVVL_PFHT450_v 1 0.0
44 HLT_IsoMu16_eta2p1_MET30_v 1 0.0
45 HLT_IsoMu20_v 1 0.0
46 HLT_IsoMu22_eta2p1_v 1 0.0
47 HLT_IsoMu22_v 1 0.0
48 HLT_IsoMu24_eta2p1_v 1 0.0
49 HLT_IsoMu24_v 1 0.0
50 HLT_IsoMu27_v 1 0.0
51 HLT_IsoTkMu22_v 1 0.0
52 HLT_IsoTkMu24_v 1 0.0
53 HLT_Mu15_IsoVVVL_PFHT350_PFMET50_v 1 0.0
54 HLT_Mu15_IsoVVVL_PFHT350_v 1 0.0
55 HLT_Mu15_IsoVVVL_PFHT400_v 1 0.0
56 HLT_Mu15_IsoVVVL_PFHT450_CaloBTagCSV_4p5_v 1 0.0
57 HLT_Mu15_IsoVVVL_PFHT450_PFMET50_v 1 0.0
58 HLT_Mu15_IsoVVVL_PFHT450_v 1 0.0
59 HLT_Mu15_IsoVVVL_PFHT600_v 1 0.0
60 HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v 1 0.0
61 HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v 1 0.0
62 HLT_Mu45_eta2p1_v 1 0.0
63 HLT_Mu50_IsoVVVL_PFHT400_v 1 0.0
64 HLT_Mu50_IsoVVVL_PFHT450_v 1 0.0
65 HLT_Mu50_v 1 0.0
66 HLT_Mu55_v 1 0.0
67 HLT_PFHT1050_v 1 0.0
68 HLT_PFHT180_v 1 0.0
69 HLT_PFHT200_v 1 0.0
70 HLT_PFHT250_v 1 0.0
71 HLT_PFHT300_PFMET100_v 1 0.0
72 HLT_PFHT300_PFMET110_v 1 0.0
73 HLT_PFHT300_v 512 0.0
74 HLT_PFHT350_v 256 0.0
75 HLT_PFHT370_v 1 0.0
76 HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2_v 1 0.0
77 HLT_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2_v 1 0.0
78 HLT_PFHT380_SixPFJet32_v 1 0.0
79 HLT_PFHT400_SixJet30_DoubleBTagCSV_p056_v 1 0.0
80 HLT_PFHT400_SixJet30_v 2 0.0
81 HLT_PFHT400_v 128 0.0
82 HLT_PFHT430_SixJet40_BTagCSV_p056_v 1 0.0
83 HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5_v 1 0.0
84 HLT_PFHT430_SixPFJet40_v 1 0.0
85 HLT_PFHT430_v 1 0.0
86 HLT_PFHT450_SixJet40_BTagCSV_p056_v 1 0.0
87 HLT_PFHT450_SixJet40_v 1 0.0
88 HLT_PFHT450_SixPFJet40_PFBTagCSV_1p5_v 1 0.0
89 HLT_PFHT475_v 64 0.0
90 HLT_PFHT500_PFMET100_PFMHT100_IDTight_v 1 0.0
91 HLT_PFHT500_PFMET110_PFMHT110_IDTight_v 1 0.0
92 HLT_PFHT510_v 1 0.0
93 HLT_PFHT590_v 1 0.0
94 HLT_PFHT600_v 16 0.0
95 HLT_PFHT650_WideJetMJJ900DEtaJJ1p5_v 1 0.0
96 HLT_PFHT650_v 8 0.0
97 HLT_PFHT680_v 1 0.0
98 HLT_PFHT700_PFMET85_PFMHT85_IDTight_v 1 0.0
99 HLT_PFHT700_PFMET95_PFMHT95_IDTight_v 1 0.0
100 HLT_PFHT780_v 1 0.0
101 HLT_PFHT800_PFMET75_PFMHT75_IDTight_v 1 0.0
102 HLT_PFHT800_PFMET85_PFMHT85_IDTight_v 1 0.0
103 HLT_PFHT800_v 1 0.0
104 HLT_PFHT890_v 1 0.0
105 HLT_PFHT900_v 1 0.0
106 HLT_PFJet450_v 1 0.0
107 HLT_PFJet500_v 1 0.0
108 HLT_PFJet550_v 1 0.0
109 HLT_PFMET100_PFMHT100_IDTight_PFHT60_v 1 0.0
110 HLT_PFMET100_PFMHT100_IDTight_v 1 0.0
111 HLT_PFMET110_PFMHT110_IDTight_PFHT60_v 1 0.0
112 HLT_PFMET110_PFMHT110_IDTight_v 1 0.0
113 HLT_PFMET120_PFMHT120_IDTight_HFCleaned_v 1 0.0
114 HLT_PFMET120_PFMHT120_IDTight_PFHT60_HFCleaned_v 1 0.0
115 HLT_PFMET120_PFMHT120_IDTight_PFHT60_v 1 0.0
116 HLT_PFMET120_PFMHT120_IDTight_v 1 0.0
117 HLT_PFMET130_PFMHT130_IDTight_PFHT60_v 1 0.0
118 HLT_PFMET130_PFMHT130_IDTight_v 1 0.0
119 HLT_PFMET140_PFMHT140_IDTight_PFHT60_v 1 0.0
120 HLT_PFMET140_PFMHT140_IDTight_v 1 0.0
121 HLT_PFMET500_PFMHT500_IDTight_CalBTagCSV_3p1_v 1 0.0
122 HLT_PFMET700_PFMHT700_IDTight_CalBTagCSV_3p1_v 1 0.0
123 HLT_PFMET800_PFMHT800_IDTight_CalBTagCSV_3p1_v 1 0.0
124 HLT_PFMET90_PFMHT90_IDTight_v 1 0.0
125 HLT_PFMETNoMu100_PFMHTNoMu100_IDTight_PFHT60_v 1 0.0
126 HLT_PFMETNoMu100_PFMHTNoMu100_IDTight_v 1 0.0
127 HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_PFHT60_v 1 0.0
128 HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_v 1 0.0
129 HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_HFCleaned_v 1 0.0
130 HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60_v 1 0.0
131 HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v 1 0.0
132 HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_PFHT60_v 1 0.0
133 HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_v 1 0.0
134 HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_PFHT60_v 1 0.0
135 HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v 1 0.0
136 HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v 1 0.0
137 HLT_Photon135_PFMET100_v 1 0.0
138 HLT_Photon165_HE10_v 1 0.0
139 HLT_Photon165_R9Id90_HE10_IsoM_v 1 0.0
140 HLT_Photon175_v 1 0.0
141 HLT_Photon200_v 1 0.0
142 HLT_Photon300_NoHE_v 1 0.0
143 HLT_Photon90_CaloIdL_PFHT500_v 1 0.0
144 HLT_Photon90_CaloIdL_PFHT600_v 1 0.0
145 HLT_Photon90_CaloIdL_PFHT700_v 1 0.0
146 HLT_TkMu100_v 1 0.0
147 HLT_TkMu50_v 1 0.0
2016: HLT_Ele27_WPTight_Gsf_v* 2017: HLT_Ele32_WPTight* (&& hltEGL1SingleEGOrFilter) 2018: HLT_Ele32_WPTight_Gsf_v*
'''

   
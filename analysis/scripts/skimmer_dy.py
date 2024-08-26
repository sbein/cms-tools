#!/usr/bin/env python

from ROOT import *
from glob import glob
from sys import exit
import argparse
import sys
import numpy as np
import os

sys.path.append("/afs/desy.de/user/n/nissanuv/cms-tools")
from lib import analysis_ntuples
from lib import analysis_tools
from lib import utils

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Create skims for x1x2x1 process.')
parser.add_argument('-i', '--input_file', nargs=1, help='Input Filename', required=False)
parser.add_argument('-o', '--output_file', nargs=1, help='Output Filename', required=False)
parser.add_argument('-madHTgt', '--madHTgt', nargs=1, help='madHT lower bound', required=False)
parser.add_argument('-madHTlt', '--madHTlt', nargs=1, help='madHT uppper bound', required=False)

parser.add_argument('-s', '--signal', dest='signal', help='Signal', action='store_true')
parser.add_argument('-bg', '--background', dest='bg', help='Background', action='store_true')
parser.add_argument('-data', '--data', dest='data', help='Data', action='store_true')
args = parser.parse_args()

print(args)

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
data = args.data

input_file = None
if args.input_file:
    input_file = args.input_file[0].strip()
output_file = None
if args.output_file:
    output_file = args.output_file[0].strip()

if (bg and signal):
    signal = True
    bg = False

######## END OF CMDLINE ARGUMENTS ########
def main():
    chain = TChain('TreeMaker2/PreSelection')
    chain.Add(input_file)
    c = chain.CloneTree()
    chain = None
    print("Creating " + output_file)
    fnew = TFile(output_file,'recreate')

    hHt = TH1F('hHt','hHt',100,0,3000)
    hHtWeighted = TH1F('hHtWeighted','hHtWeighted',100,0,3000)
    hHtAfterMadHt = TH1F('hHtAfterMadHt','hHtAfterMadHt',100,0,3000)
    hHt.Sumw2()

    var_Met = np.zeros(1,dtype=float)
    var_METPhi = np.zeros(1,dtype=float)
    var_CrossSection = np.zeros(1,dtype=float)
    var_NJets = np.zeros(1,dtype=int)
    var_BTags = np.zeros(1,dtype=int)
    var_Ht = np.zeros(1,dtype=float)
    var_Mht = np.zeros(1,dtype=float)
    var_MetDHt = np.zeros(1,dtype=float)
    #var_MetDHt2 = np.zeros(1,dtype=float)
    var_Mt2 = np.zeros(1,dtype=float)
    var_Electrons = ROOT.std.vector(TLorentzVector)()
    var_Electrons_charge = ROOT.std.vector(int)()
    var_Muons = ROOT.std.vector(TLorentzVector)()
    var_Muons_charge    = ROOT.std.vector(int)()
    var_NL = np.zeros(1,dtype=int)
    var_invMass = np.zeros(1,dtype=float)

    var_Jets = ROOT.std.vector(TLorentzVector)()

    var_MinDeltaPhiMetJets = np.zeros(1,dtype=float)
    var_MinDeltaPhiMhtJets = np.zeros(1,dtype=float)

    #### TRACKS ####

    tEvent = TTree('tEvent','tEvent')
    tEvent.Branch('Met', var_Met,'Met/D')
    tEvent.Branch('METPhi', var_METPhi,'METPhi/D')
    tEvent.Branch('CrossSection', var_CrossSection,'CrossSection/D')
    tEvent.Branch('NJets', var_NJets,'NJets/I')
    tEvent.Branch('BTags', var_BTags,'BTags/I')
    tEvent.Branch('NL', var_NL,'NL/I')
    tEvent.Branch('Ht', var_Ht,'Ht/D')
    tEvent.Branch('Mht', var_Mht,'Mht/D')
    tEvent.Branch('MetDHt', var_MetDHt,'MetDHt/D')
    #tEvent.Branch('MetDHt2', var_MetDHt2,'MetDHt2/D')
    tEvent.Branch('Mt2', var_Mt2,'Mt2/D')
    tEvent.Branch('invMass', var_invMass,'invMass/D')

    tEvent.Branch('Electrons', 'std::vector<TLorentzVector>', var_Electrons)
    tEvent.Branch('Electrons_charge', 'std::vector<int>', var_Electrons_charge)
    tEvent.Branch('Muons', 'std::vector<TLorentzVector>', var_Muons)
    tEvent.Branch('Muons_charge', 'std::vector<int>', var_Muons_charge)

    tEvent.Branch('Jets', 'std::vector<TLorentzVector>', var_Jets)

    tEvent.Branch('MinDeltaPhiMetJets', var_MinDeltaPhiMetJets,'MinDeltaPhiMetJets/D')
    tEvent.Branch('MinDeltaPhiMhtJets', var_MinDeltaPhiMhtJets,'MinDeltaPhiMhtJets/D')

    nentries = c.GetEntries()
    print('Analysing', nentries, "entries")

    count = 0
    afterPreselection = 0
    afterMET = 0
    afterBTAGS = 0
    afterNj = 0
    nLMap = {}

    crossSection = 1
    if signal:
        filename = (os.path.basename(input_file).split("Chi20Chipm")[0]).replace("p", ".")
        crossSection = utils.getCrossSection(filename)
        if crossSection is None:
            if utils.crossSections.get(filename) is not None:
                crossSection = utils.crossSections.get(filename)
            else:
                crossSection = 1.21547
    print("Starting Loop")
    for ientry in range(nentries):
        if ientry % 1000 == 0:
            print("Processing " + str(ientry))
        c.GetEntry(ientry)

        ### MADHT ###
        rightProcess = True
    
        if signal:
            rightProcess = analysis_ntuples.isX1X2X1Process(c)
        elif bg:
            crossSection = c.CrossSection
            if (madHTgt is not None and c.madHT < madHTgt) or (madHTlt is not None and c.madHT > madHTlt):
                rightProcess = False
        elif data:
            runnum = c.RunNum
            lumisec = c.LumiBlockNum
            if runnum not in runs:
                runs[runnum] = []
            if lumisec not in runs[runnum]:
                runs[runnum].append(lumisec)

        hHt.Fill(c.HT)
        #print("crossSection=" + str(crossSection))
        hHtWeighted.Fill(c.HT, crossSection)

        if not rightProcess:
            continue
        count += 1
        if not data:
            hHtAfterMadHt.Fill(c.madHT)

        nj, btags, ljet = analysis_ntuples.numberOfJets25Pt2_4Eta_Loose(c)
        nL = c.Electrons.size() + c.Muons.size()
    
        var_NL[0] = nL
    
        #### PRECUTS ###
        #if not signal:
        #    if not analysis_ntuples.passed2016BTrigger(c, data): continue
        
        partSize = c.GenParticles.size()
        genLeps = []
        for ipart in range(partSize):
            if c.GenParticles_Status[ipart] == 1 and (abs(c.GenParticles_PdgId[ipart]) == 11 or abs(c.GenParticles_PdgId[ipart]) == 13):
                genLeps.append(ipart)
        
        if len(genLeps) != 2 or abs(c.GenParticles_PdgId[genLeps[0]]) != abs(c.GenParticles_PdgId[genLeps[1]]) or c.GenParticles_PdgId[genLeps[0]] * c.GenParticles_PdgId[genLeps[1]] > 0:
           #  print("*********")
#             print("No!!! size=" + str(len(genLeps)))
#             for i in genLeps:
#                 print(c.GenParticles_ParentId[i])
            continue
        if c.GenParticles_ParentIdx[genLeps[0]] == c.GenParticles_ParentIdx[genLeps[1]]:
            print("HERE! ", c.GenParticles_ParentId[genLeps[0]])
        if c.GenParticles_ParentIdx[genLeps[0]] != c.GenParticles_ParentIdx[genLeps[1]] or (c.GenParticles_ParentId[genLeps[0]] != 22 and c.GenParticles_ParentId[genLeps[0]] != 23):
            continue
        
        #print("Yes! ", c.GenParticles_ParentId[genLeps[0]])
        #else:
        #    print("YES!!")
            
        
        #if nL != 2 or (c.Electrons.size() != 2 and c.Muons.size() != 2):
        #    continue

        l1 = None
        l2 = None
        
#         if c.Electrons.size() == 2:
#             if c.Electrons_charge[0] * c.Electrons_charge[1] > 0:
#                 continue
#             l1 = c.Electrons[0]
#             l2 = c.Electrons[1]
#         else:
#             if c.Muons_charge[0] * c.Muons_charge[1] > 0:
#                 continue
#             l1 = c.Muons[0]
#             l2 = c.Muons[1]
        
        #if l1.Pt() < 30 or l2.Pt() < 30:
        #   continue
        l1 = c.GenParticles[genLeps[0]]
        l2 = c.GenParticles[genLeps[1]]
            
        var_invMass[0] = (l1 + l2).M()
        
        #if var_invMass[0] < (91.19 - 10.0) or var_invMass[0] > (91.19 + 10.0):
        if var_invMass[0] > (91.19 + 10.0):
            continue

        afterPreselection += 1

        var_Met[0] = c.MET
        var_METPhi[0] = c.METPhi
        var_Mht[0] = c.MHT
        var_Ht[0] = c.HT
        var_Mt2[0] = c.MT2
        var_CrossSection[0] = crossSection
        var_NJets[0] = nj
        var_BTags[0] = btags
        
    
        var_Electrons = c.Electrons
        var_Electrons_charge= c.Electrons_charge
        var_Muons = c.Muons
        var_Muons_charge = c.Muons_charge
        var_Jets = c.Jets
        
    
        tEvent.SetBranchAddress('Electrons', var_Electrons)
        tEvent.SetBranchAddress('Electrons_charge', var_Electrons_charge)
        tEvent.SetBranchAddress('Muons', var_Muons)
        tEvent.SetBranchAddress('Muons_charge', var_Muons_charge)
        tEvent.SetBranchAddress('Jets', var_Jets)

        metDHt = 9999999
        if c.HT != 0:
            metDHt = c.MET / c.HT

        var_MetDHt[0] = metDHt
    
        tEvent.Fill()

    fnew.cd()
    tEvent.Write()
    print('just created', fnew.GetName())
    print("Total: " + str(nentries))
    print("After Preselection: " + str(afterPreselection))
    hHt.Write()
    print("*")
    hHtWeighted.Write()
    print("**")
    hHtAfterMadHt.Write()
    print("***")
    fnew.Close()
    print("****")
    
main()


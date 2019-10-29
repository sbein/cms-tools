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

gROOT.SetBatch(1)
gStyle.SetOptStat(0)

gSystem.Load('LumiSectMap_C')
from ROOT import LumiSectMap

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Plot Lepton Observeables.')
parser.add_argument('-i', '--input_file', nargs=1, help='Input Filename', required=False)
parser.add_argument('-o', '--output_file', nargs=1, help='Output Filename', required=False)
args = parser.parse_args()

input_file = None
output_file = None
if args.input_file:
    input_file = args.input_file[0]
else:
    #input_file = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/sum/higgsino_mu100_dm3p28Chi20Chipm.root"
    input_file = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/sum/higgsino_mu100_dm12p84Chi20Chipm.root"
    
    
    #input_file = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/sum/higgsino_mu100_dm2p51Chi20Chipm.root"
if args.output_file:
    output_file = args.output_file[0]
else:
    output_file = "leptons.pdf"

######## END OF CMDLINE ARGUMENTS ########

lepTypes = ["MM", "Zl"]

def passedCut(cut, c, lepFlavour, l, li, track, minCanT, ljet, params):
    for func in cut["funcs"]:
        if not func(c, lepFlavour, l, li, track, minCanT, ljet, params):
            return False
    return True

class CustomInsertTH1F(UOFlowTH1F):
    def setInsertFunc(self, func):
        self.insertFunc = func
    def insert(self, c, lepFlavour, lep, li, track, ti, lj, params):
        #print "In", self.GetName()
        #print "Value", self.insertFunc(c, lepFlavour, lep, li, track, ti, lj, params)
        self.Fill(self.insertFunc(c, lepFlavour, lep, li, track, ti, lj, params))

def mediumId(c, lepFlavour, l, li, track, minCanT, ljet, params):
    return bool(eval("c." + lepFlavour + "_mediumID")[li])

def tightID(c, lepFlavour, l, li, track, minCanT, ljet, params):
    return bool(eval("c." + lepFlavour + "_tightID")[li])

def pt(c, lepFlavour, l, li, track, minCanT, ljet, params):
    return l.Pt() < 25

def deltaRLJ(c, lepFlavour, l, li, track, minCanT, ljet, params):
    return abs(l.DeltaR(c.Jets[ljet])) > 0.6

def passIso(c, lepFlavour, l, li, track, minCanT, ljet, params):
    return bool(eval("c." + lepFlavour + "_passIso")[li])


def main():
    
    c = TChain('tEvent')
    print "Going to open the file"
    print input_file
    c.Add(input_file)
    
    nentries = c.GetEntries()
    print 'Analysing', nentries, "entries"

    histograms = {"Zl" : {}, "MM" : {}}
    memory = []
    
    global mediumId, tightID, pt, passIso

    cuts = [{"name":"none", "title": "No Cuts", "funcs":[]},
        {"name":"mediumId", "title": "mediumId", "funcs":[mediumId, pt]},
        {"name":"passIso", "title": "passIso", "funcs":[passIso, pt]},
        {"name":"tightID", "title": "tightID", "funcs":[tightID, pt]},
        #{"name":"pt", "title": "pt > 1.8", "funcs":[pt]},
        #{"name":"tightID", "title": "Eta < 2.6, deltaEtaLL < 1, deltaEtaLJ < 3.8", "funcs":[eta, deltaEtaLL, deltaEtaLJ]},
        #{"name":"Pt_Eta_dxy_dz", "title": "Eta < 2.6, Pt > 2.5, dxy < 0.05, dz < 0.06", "funcs":[eta, pt, dxy, dz]},
        #{"name":"Pt_Eta_dxy_dz_deltaEtaLL", "title": "Eta < 2.6, Pt > 2.5, dxy < 0.05, dz < 0.06, deltaEtaLL < 1", "funcs":[eta, pt, dxy, dz, deltaEtaLL]},
        #{"name":"Pt_Eta_dxy_dz_deltaEtaLL_deltaEtaLJ", "title": "Eta < 2.6, Pt > 2.5, dxy < 0.05, dz < 0.06, deltaEtaLL < 1, deltaEtaLJ < 3.8", "funcs":[eta, pt, dxy, dz, deltaEtaLL, deltaEtaLJ]},
        #{"name":"Pt_Eta_dxy_dz_deltaEtaLL_deltaRLJ", "title": "Eta < 2.6, Pt > 2.5, dxy < 0.05, dz < 0.06, deltaEtaLL < 1, deltaRLJ > 1.8", "funcs":[eta, pt, dxy, dz, deltaEtaLL, deltaRLJ]},
        #{"name":"Pt_Eta_dxy_dz_deltaEtaLL_deltaRLJ_deltaRLL", "title": "Eta < 2.6, Pt > 2.5, dxy < 0.05, dz < 0.06, deltaEtaLL < 1, deltaRLJ > 1.8, deltaRLL < 1.1", "funcs":[eta, pt, dxy, dz, deltaEtaLL, deltaRLJ, deltaRLL]}
        ]
    histoDefs = [
        {"name" : "Eta", "title" : "Eta", "bins" : 50, "minX" : 0, "maxX" : 2.5, "func" : lambda c, lepFlavour, lep, li, track, ti, lj, params: abs(lep.Eta()) },
        {"name" : "Phi", "title" : "Phi", "bins" : 50, "minX" : 0, "maxX" : 3, "func" : lambda c, lepFlavour, lep, li, track, ti, lj, params: abs(lep.Phi()) },
        {"name" : "Pt", "title" : "Pt", "bins" : 50, "minX" : 0, "maxX" : 25, "func" : lambda c, lepFlavour, lep, li, track, ti, lj, params: abs(lep.Pt()) },
        
        {"name" : "passIso", "title" : "passIso", "bins" : 2, "minX" : 0, "maxX" : 1, "func" : lambda c, lepFlavour, lep, li, track, ti, lj, params: bool(eval("c." + lepFlavour + "_passIso")[li]) },
        {"name" : "mediumID", "title" : "mediumID", "bins" : 2, "minX" : 0, "maxX" : 1, "func" : lambda c, lepFlavour, lep, li, track, ti, lj, params: bool(eval("c." + lepFlavour + "_mediumID")[li]) },
        {"name" : "tightID", "title" : "tightID", "bins" : 2, "minX" : 0, "maxX" : 1, "func" : lambda c, lepFlavour, lep, li, track, ti, lj, params: bool(eval("c." + lepFlavour + "_tightID")[li]) },
        #{"name" : "iso", "title" : "iso", "bins" : 50, "minX" : 0, "maxX" : 1, "func" : lambda c, lepFlavour, lep, li, track, ti, lj, params: eval("c." + lepFlavour + "_MiniIso")[li] },
        #{"name" : "MT2Activity", "title" : "MT2Activity", "bins" : 50, "minX" : 0, "maxX" : 1, "func" : lambda c, lepFlavour, lep, li, track, ti, lj, params: eval("c." + lepFlavour + "_MT2Activity")[li] },
        
        {"name" : "deltaRLJ", "title" : "deltaRLJ", "bins" : 50, "minX" : 0, "maxX" : 6, "func" : lambda c, lepFlavour, lep, li, track, ti, lj, params:  abs(lep.DeltaR(c.Jets[lj])) },
        {"name" : "deltaPhiLJ", "title" : "deltaPhiLJ", "bins" : 50, "minX" : 0, "maxX" : 6, "func" : lambda c, lepFlavour, lep, li, track, ti, lj, params:  abs(lep.DeltaPhi(c.Jets[lj])) },
        {"name" : "deltaEtaLJ", "title" : "deltaEtaLJ", "bins" : 50, "minX" : 0, "maxX" : 6, "func" : lambda c, lepFlavour, lep, li, track, ti, lj, params:  abs(lep.Eta() - c.Jets[lj].Eta()) },
        {"name" : "MT", "title" : "MT", "bins" : 50, "minX" : 0, "maxX" : 90, "func" : lambda c, lepFlavour, lep, li, track, ti, lj, params:  analysis_tools.MT2(c.Met, c.METPhi, lep) },
        
        
        
       
        
        # {"name" : "tracks_chi2perNdof", "title" : "tracks_chi2perNdof", "bins" : 50, "minX" : 0, "maxX" : 1, "func" : lambda c, lepFlavour, lep, li, track, ti, lj, params: eval("c.tracks_chi2perNdof")[ti] },
#         {"name" : "tracks_dxyVtx", "title" : "tracks_dxyVtx", "bins" : 50, "minX" : 0, "maxX" : 1, "func" : lambda c, lepFlavour, lep, li, track, ti, lj, params: eval("c.tracks_dxyVtx")[ti] },
#         {"name" : "tracks_dzVtx", "title" : "tracks_dzVtx", "bins" : 50, "minX" : 0, "maxX" : 1, "func" : lambda c, lepFlavour, lep, li, track, ti, lj, params: eval("c.tracks_dzVtx")[ti] },
#         {"name" : "tracks_trackJetIso", "title" : "tracks_trackJetIso", "bins" : 50, "minX" : 0, "maxX" : 1, "func" : lambda c, lepFlavour, lep, li, track, ti, lj, params: eval("c.tracks_trackJetIso")[ti] },
#         {"name" : "tracks_trkMiniRelIso", "title" : "tracks_trkMiniRelIso", "bins" : 50, "minX" : 0, "maxX" : 1, "func" : lambda c, lepFlavour, lep, li, track, ti, lj, params: eval("c.tracks_trkMiniRelIso")[ti] },
#         {"name" : "tracks_trackQualityHighPurity", "title" : "tracks_trackQualityHighPurity", "bins" : 2, "minX" : 0, "maxX" : 1, "func" : lambda c, lepFlavour, lep, li, track, ti, lj, params: bool(eval("c.tracks_trackQualityHighPurity")[ti]) },
    ]
    
    singlePerCut = {}
    
    for cut in cuts:
        singlePerCut[cut["name"]] = 0
        for lepType in lepTypes:
            for histDef in histoDefs:
                name = histDef["name"] + "_" + cut["name"] + "_" + lepType
                #print name
                histograms[lepType][name] = CustomInsertTH1F(name, "", histDef["bins"], histDef["minX"], histDef["maxX"])
                histograms[lepType][name].setInsertFunc(histDef["func"])
    
    notCorrect = 0
    
    totalZl = 0
    totalZlTracks = 0
    totalGenZl = 0
    totalRecoLeps = 0
    totalZlGenTracks = 0
    dileptonCorrect = 0
    singleLep = 0
    totalEvents = 0
    dileptonTotal = 0
    singleTotal = 0
    
    passedCutsCount = {"Zl" : {}, "MM" : {}}
    
    
    for ientry in range(nentries):
        if ientry % 5000 == 0:
            print "Processing " + str(ientry)
        c.GetEntry(ientry)
        
        if c.tracks.size() == 0:
            continue
        
        rightProcess = analysis_ntuples.isX1X2X1Process(c)
        if not rightProcess:
            print "No"
            notCorrect += 1
            continue
            
        nj, btags, ljet = analysis_ntuples.numberOfJets25Pt2_4Eta_Loose(c)
        if ljet is None: continue
        if btags > 0: continue
        if nj < 1: continue 
        
        genZL, genNonZL = analysis_ntuples.classifyGenZLeptons(c)
        if not genZL:
            continue
        #Only Electrons or Muons
        # if abs(c.GenParticles_PdgId[genZL[0]]) == 13:
#             continue
#         for i in  genZL:
#             if abs(c.GenParticles_PdgId[i]) == 13:
#                 print "WHAT"
#                 exit(0)
        
        totalEvents += 1
        
        totalGenZl += len(genZL)
        totalRecoLeps += len(c.Electrons) + len(c.Muons)
        
        zlTracksNonMatching = 0
        
        for i in genZL:
            l = c.GenParticles[i]
            minT, minCanT = analysis_ntuples.minDeltaRLepTracks(l, c)
            if minT < 0.01 and c.GenParticles_PdgId[i] * c.tracks_charge[minCanT] < 0:
                #print "GenParticles_PdgId[i]=", c.GenParticles_PdgId[i], " tracks_charge[minCanT]=", c.tracks_charge[minCanT]
                totalZlGenTracks += 1
        
        params = {}
        
        zl = 0
        passedLep = 0
        
        for lepVal in [["Electrons", -11]]:#["Electrons", -11], ["Muons", -13]:
            #print lepVal
            lepFlavour = lepVal[0]
            lepCharge = lepVal[1]
            
            leps = getattr(c, lepFlavour)
            for li in range(leps.size()):
                l = leps[li]
                
                passIso = bool(eval("c." + lepFlavour + "_passIso")[li])
                mediumID = bool(eval("c." + lepFlavour + "_mediumID")[li])
                tightID = bool(eval("c." + lepFlavour + "_tightID")[li])
                iso = eval("c." + lepFlavour + "_MiniIso")[li]
                MT2Activity = eval("c." + lepFlavour + "_MT2Activity")[li]
                
                #if not passIso:
                #    continue
                
                #if l.Pt() < 5:
                #    continue
                
                #print iso
                
                #print histograms
                #exit(0)
                
                passedLep += 1

                minZ, minCanZ = analysis_ntuples.minDeltaRGenParticles(l, genZL, c)
                minNZ, minCanNZ = analysis_ntuples.minDeltaRGenParticles(l, genNonZL, c)
                min = 0
                
                type = None
                
                if minNZ is None or minZ < minNZ:
                    min = minZ
                else:
                    min = minNZ
                if min > 0.01:
                    type = "MM"
                elif minNZ is None or minZ < minNZ:
                    if c.GenParticles_PdgId[minCanZ] == lepCharge * getattr(c, lepFlavour + "_charge")[li]:
                        type = "Zl"
                        totalZl += 1
                        zl += 1
                    else:
                        type = "MM"
                else:
                    type = "MM"
                
                minT, minCanT = analysis_ntuples.minDeltaRLepTracks(l, c)
                
                # if minT > 0.01:
#                     if type == "Zl":
#                         print "--------"
#                         print "min=", min
#                         print "type=", type
#                         print "iso=", iso
#                         print "passIso=", passIso
#                         print "mediumId=", mediumID
#                         print "tightId=", tightID
#                         print "MT2Activity=", MT2Activity
#                         print minT, minCanT
#                         print "NO TRACK!!! len=", len(c.tracks) 
#                         print "--------"
                    #continue
                    
                if type == "Zl":
                    totalZlTracks += 1
                
                track = c.tracks[minCanT] if minT < 0.01 else None
                
                for cut in cuts:
                    if passedCutsCount[type].get(cut['name']) is None:
                        passedCutsCount[type][cut['name']] = 0
                    
                    if not passedCut(cut, c, lepFlavour, l, li, track, minCanT, ljet, params):
                        continue
                    passedCutsCount[type][cut['name']] += 1
                    for histDef in histoDefs:
                        name = histDef["name"] + "_" + cut["name"] + "_" + type
                        h = histograms[type][name]
                        h.insert(c, lepFlavour, l, li, track, minCanT, ljet, params)
                
        if zl == 2:
            dileptonCorrect += 1
        elif zl == 1:
            singleLep += 1
        
        if passedLep == 2:
            dileptonTotal += 1
        elif passedLep == 1:
            singleTotal += 1
    
    print "totalEvents=", totalEvents
    print "Not Correct Procs=" + str(notCorrect)
    print "totalZl=", totalZl
    print "totalZlTracks=", totalZlTracks
    print "totalGenZl=", totalGenZl
    print "totalRecoLeps=", totalRecoLeps
    print "totalZlGenTracks=", totalZlGenTracks
    print "dileptonCorrect=", dileptonCorrect
    print "singleLep=", singleLep
    print "dileptonTotal=", dileptonTotal
    print "singleTotal=", singleTotal
    
    print passedCutsCount

    c1 = TCanvas("c1")

    titlePad = TPad("titlePad", "",0.0,0.93,1.0,1.0)
    histPad = TPad("histPad", "",0.0,0.0,1.0,0.93)

    titlePad.Draw()
    t = TPaveText(0.0,0.93,1.0,1.0,"NB")
    t.SetFillStyle(0)
    t.SetLineColor(0)
    t.SetTextFont(40);
    t.Draw()

    histPad.Draw()
    histPad.Divide(2,2)
    OUTPUT_FILE = output_file or "./lepton_obs.pdf"
    c1.Print(OUTPUT_FILE + "[");

    for cut in cuts:
        t.Clear()
        t.AddText(cut["title"])
        t.Draw();
        titlePad.Update()
        pId = 1
        needToDraw = False
        
        for histDef in histoDefs:
            
            #print histDef
            
            for log in [True, False]:
                pad = histPad.cd(pId)
                pad.cd()
            
                legend = TLegend(.69,.7,.85,.89)
                memory.append(legend)
                cP = 0
                maxY = 0
                drawSame = False
                for lepType in lepTypes:
                    name = histDef["name"] + "_" + cut["name"] + "_" + lepType
                    h = histograms[lepType][name]
                    maxY = max(maxY, h.GetMaximum())
                for lepType in lepTypes:
                    name = histDef["name"] + "_" + cut["name"] + "_" + lepType
                    h = histograms[lepType][name]
                    utils.formatHist(h, utils.colorPalette[cP])
                    cP += 1
                    h.SetMaximum(maxY)
                    #if log:
                    h.SetMinimum(0.01)
                    #else:
                    #h.SetMinimum(0)
                    legend.AddEntry(h, lepType, 'F')
                    if drawSame:
                        #print "DRAW SAME", name, lepType
                        h.Draw("HIST SAME")
                    else:
                        #print "DRAW", name, lepType
                        needToDraw = True
                        h.GetXaxis().SetTitle(histDef['title'])
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
        
        if needToDraw:
            for id in range(pId, 5):
                print "Clearing pad " + str(id)
                pad = histPad.cd(id)
                pad.Clear()
            c1.Print(OUTPUT_FILE);
    c1.Print(OUTPUT_FILE+"]");

main()
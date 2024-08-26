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
from array import array

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
args = parser.parse_args()

output_file = None

if args.output_file:
    output_file = args.output_file[0]
else:
    output_file = "eff.pdf"

efficiency_map = {
    "1t1l" : {},
    "2l" : {}
}

signal_files_path = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/sum/higgsino_mu100_*"
signal_files = glob(signal_files_path)

single_events = True

def main():
    
    c1 = TCanvas("c1", "c1", 800, 800)
    #c1.SetBottomMargin(0.16)
    #c1.SetLeftMargin(0.18)
    c1.cd()
    
    
    genLeptons = {}
    recoLeptons = {}
    recoSosLeptons = {}
    tracks = {}
    isoTracks = {}
    nonRecoTracks = {}
    nonRecoIsoTracks = {}
    
    genLeptons = {'7.39': 64296, '0.51': 50968, '5.63': 64650, '4.30': 69040, '1.92': 49318, '0.18': 49434, '9.73': 61856, '2.51': 67026, '1.13': 50304, '12.84': 58570, '0.30': 51918, '0.86': 49480, '3.28': 70130, '1.47': 49600}
    recoLeptons = {'7.39': 24367, '0.51': 177, '5.63': 20428, '4.30': 17509, '1.92': 4972, '0.18': 0, '9.73': 27388, '2.51': 9632, '1.13': 1932, '12.84': 29451, '0.30': 0, '0.86': 1071, '3.28': 13457, '1.47': 3171}
    recoSosLeptons = {'2.51': 3008, '1.13': 158, '7.39': 16709, '12.84': 24499, '0.30': 0, '0.51': 6, '0.86': 48, '5.63': 12247, '3.28': 5391, '1.47': 438, '4.30': 8858, '1.92': 1047, '0.18': 0, '9.73': 20955}
    tracks =  {'7.39': 31278, '0.51': 198, '5.63': 27335, '4.30': 24057, '1.92': 6956, '0.18': 2, '9.73': 33551, '2.51': 13848, '1.13': 2484, '12.84': 34425, '0.30': 11, '0.86': 1182, '3.28': 19334, '1.47': 4353}
    isoTracks =  {'7.39': 28724, '0.51': 176, '5.63': 25005, '4.30': 21996, '1.92': 6335, '0.18': 2, '9.73': 30856, '2.51': 12675, '1.13': 2278, '12.84': 31722, '0.30': 11, '0.86': 1051, '3.28': 17655, '1.47': 3993}
    nonRecoTracks =  {'7.39': 12113, '0.51': 177, '5.63': 11849, '4.30': 11718, '1.92': 4418, '0.18': 2, '9.73': 11344, '2.51': 8075, '1.13': 1822, '12.84': 9977, '0.30': 11, '0.86': 920, '3.28': 10457, '1.47': 2994}
    nonRecoIsoTracks =  {'7.39': 11069, '0.51': 158, '5.63': 10859, '4.30': 10721, '1.92': 4036, '0.18': 2, '9.73': 10380, '2.51': 7402, '1.13': 1679, '12.84': 9111, '0.30': 11, '0.86': 825, '3.28': 9527, '1.47': 2763}
    
    
    # Event
    if single_events:
        genLeptons = {'7.39': 32148, '0.51': 25484, '5.63': 32325, '4.30': 34520, '1.92': 24659, '0.18': 24717, '9.73': 30928, '2.51': 33513, '1.13': 25152, '12.84': 29285, '0.30': 25959, '0.86': 24740, '3.28': 35065, '1.47': 24800}
        recoLeptons = {'7.39': 5865, '0.51': 10, '5.63': 4329, '4.30': 3220, '1.92': 612, '0.18': 0, '9.73': 7412, '2.51': 1343, '1.13': 167, '12.84': 8775, '0.30': 0, '0.86': 66, '3.28': 2145, '1.47': 314}
        recoSosLeptons = {'7.39': 2337, '0.51': 1, '5.63': 1325, '4.30': 758, '1.92': 37, '0.18': 0, '9.73': 3752, '2.51': 149, '1.13': 0, '12.84': 5453, '0.30': 0, '0.86': 0, '3.28': 322, '1.47': 7}
        tracks =  {'7.39': 1624, '0.51': 0, '5.63': 1454, '4.30': 1212, '1.92': 210, '0.18': 0, '9.73': 1578, '2.51': 594, '1.13': 29, '12.84': 1346, '0.30': 0, '0.86': 3, '3.28': 925, '1.47': 87}
        isoTracks =  {'7.39': 1362, '0.51': 0, '5.63': 1235, '4.30': 1053, '1.92': 187, '0.18': 0, '9.73': 1347, '2.51': 509, '1.13': 25, '12.84': 1118, '0.30': 0, '0.86': 3, '3.28': 797, '1.47': 80}
        nonRecoTracks =  {'7.39': 3375, '0.51': 1, '5.63': 2580, '4.30': 1848, '1.92': 189, '0.18': 0, '9.73': 3897, '2.51': 553, '1.13': 8, '12.84': 4107, '0.30': 0, '0.86': 4, '3.28': 1089, '1.47': 73}
        nonRecoIsoTracks =  {'7.39': 3072, '0.51': 1, '5.63': 2359, '4.30': 1680, '1.92': 177, '0.18': 0, '9.73': 3553, '2.51': 505, '1.13': 8, '12.84': 3745, '0.30': 0, '0.86': 4, '3.28': 991, '1.47': 68}
    for input_file in signal_files:
        break
        print("Opening", input_file)
        file = TFile(input_file)
        c = file.Get('tEvent')
        
        dm = input_file.split("mu100_dm")[1].split("Chi20")[0].replace("p", ".")
        print("dm=" + str(dm))
    
        nentries = c.GetEntries()
        print('Analysing', nentries, "entries")

        afterPreselection = 0
        numOfGenLeptons = 0
        numOfRecoLeptons = 0
        numOfSosRecoLeptons = 0
        numOfTracks = 0
        numOfIsoTracks = 0
        
        numOfNonRecoTracks = 0
        numOfNonRecoIsoTracks = 0
        numOfTwoRecoTracks = 0
        numOfTwoRecoIsoTracks = 0
    
        print("Starting Loop")
        for ientry in range(nentries):
            if ientry % 1000 == 0:
                print("Processing " + str(ientry) + " out of " + str(nentries))
            c.GetEntry(ientry)

            ### PRECUTS ###

            # rightProcess = analysis_ntuples.isX1X2X1Process(c)
#         
#             nj, btags, ljet = analysis_ntuples.numberOfJets25Pt2_4Eta_Loose(c)
#             if ljet is None:
#                 #print("No ljet:",ljet )
#                 continue
#         
#             if analysis_ntuples.minDeltaPhiMetJets25Pt2_4Eta(c) < 0.4: continue
#             if c.MHT < 100: continue
#             if c.MET < 120: continue
#         
#             vminCsv25, maxCsv25 = analysis_ntuples.minMaxCsv(c, 25)
#         
#             if maxCsv25 > 0.7:
#                 continue
            ## END PRECUTS##
        
            genZL, genNonZL = analysis_ntuples.classifyGenZLeptons(c)
            if not genZL:
                continue
            
            if single_events:
                numOfGenLeptons += 1
            else:
                numOfGenLeptons += 2
            
            eventExclusiveTracks = 0
            eventExclusiveIsoTracks = 0
            eventRecoLeps = 0
            eventSosRecoLeps = 0
            
            
            
            for i in genZL:
                l = c.GenParticles[i]
                minT, minCanT = analysis_ntuples.minDeltaRLepTracks(l, c)
                foundTrack = minT is not None and minT < 0.01 and c.GenParticles_PdgId[i] * c.tracks_charge[minCanT] < 0
                if foundTrack:
                    #print("GenParticles_PdgId[i]=", c.GenParticles_PdgId[i], " tracks_charge[minCanT]=", c.tracks_charge[minCanT])
                    numOfTracks += 1
                    if c.tracks_trkRelIso[minCanT] < 0.1:
                        numOfIsoTracks += 1
                lepFlavour = "Electrons"
                lepCharge = -11
                if abs(c.GenParticles_PdgId[i]) == 13:
                    lepFlavour = "Muons"
                    lepCharge = -13
                
                min, minCan = analysis_ntuples.minDeltaLepLeps(l, getattr(c, lepFlavour))
                if min is not None and min < 0.01 and c.GenParticles_PdgId[i] == lepCharge * getattr(c, lepFlavour + "_charge")[minCan]:
                    eventRecoLeps += 1
                    if getattr(c, lepFlavour)[minCan].Pt() > 5:
                        eventSosRecoLeps += 1
                elif foundTrack:
                    eventExclusiveTracks +=1
                    if c.tracks_trkRelIso[minCanT] < 0.1:
                        eventExclusiveIsoTracks += 1
            
            if single_events:
                if eventRecoLeps == 2:
                    numOfRecoLeptons += 1
                if eventSosRecoLeps == 2:
                    numOfSosRecoLeptons += 1
                if eventRecoLeps == 1 and eventExclusiveTracks == 1:
                    numOfNonRecoTracks += 1
                if eventRecoLeps == 1 and eventExclusiveIsoTracks == 1:
                    numOfNonRecoIsoTracks += 1
                if eventExclusiveTracks == 2:
                    numOfTwoRecoTracks += 1
                if eventExclusiveIsoTracks == 2:
                    numOfTwoRecoIsoTracks += 1
            else:
                numOfRecoLeptons += eventRecoLeps
                numOfSosRecoLeptons += eventSosRecoLeps
                numOfNonRecoTracks += eventExclusiveTracks
                numOfNonRecoIsoTracks += eventExclusiveIsoTracks
                

        genLeptons[dm] = numOfGenLeptons
        recoLeptons[dm] = numOfRecoLeptons
        recoSosLeptons[dm] = numOfSosRecoLeptons
        if single_events:
            tracks[dm] = numOfTwoRecoTracks
            isoTracks[dm] = numOfTwoRecoIsoTracks
        else:
            tracks[dm] = numOfTracks
            isoTracks[dm] = numOfIsoTracks
        nonRecoTracks[dm] = numOfNonRecoTracks
        nonRecoIsoTracks[dm] = numOfNonRecoIsoTracks
        
    
    print("genLeptons =", genLeptons)
    print("recoLeptons =", recoLeptons)
    print("recoSosLeptons =", recoSosLeptons)
    print("tracks = ", tracks)
    print("isoTracks = ", isoTracks)
    print("nonRecoTracks = ", nonRecoTracks)
    print("nonRecoIsoTracks = ", nonRecoIsoTracks)
    
    multiGraph = TMultiGraph()
    legend = None
    if single_events:
        legend = TLegend(0.15, 0.7, 0.45, 0.85)
    else:
        legend = TLegend(0.15, 0.7, 0.45, 0.85)
    #
    
    n = len(genLeptons)
    x, y = array('d'), array('d')
    for i, j in genLeptons.items():
        eff = float(j)/genLeptons[i]
        x.append(float(i))
        y.append(eff) 
    print(n, x, y)
    genLeptonsGraph = TGraph(n, x, y)
    genLeptonsGraph.SetMarkerColor(kRed)
    genLeptonsGraph.SetMarkerStyle(20)
    #genLeptonsGraph.SetMarkerSize(2)
    
    

    #multiGraph.Add(genLeptonsGraph)
    
    n = len(tracks)
    x, y = array('d'), array('d')
    #loop = numOfTwoRecoTracks if single_events else tracks
    for i, j in tracks.items():
        eff = float(j)/genLeptons[i]
        x.append(float(i))
        y.append(eff)
    print(n, x, y)
    tracksGraph = TGraph(n, x, y)
    tracksGraph.SetMarkerColor(kGreen)
    tracksGraph.SetMarkerStyle(20)
    #tracksGraph.SetMarkerSize(2)
    
    multiGraph.Add(tracksGraph)
    
    if single_events:
        legend.AddEntry(tracksGraph, "Two Tracks", "lp")
    else:
        legend.AddEntry(tracksGraph, "Matched Tracks", "lp")
    
    n = len(isoTracks)
    x, y = array('d'), array('d')
    #loop = numOfTwoRecoTracks if single_events else tracks
    for i, j in isoTracks.items():
        eff = float(j)/genLeptons[i]
        x.append(float(i))
        y.append(eff)
    print(n, x, y)
    isoTracksGraph = TGraph(n, x, y)
    isoTracksGraph.SetMarkerColor(kGreen)
    isoTracksGraph.SetMarkerStyle(21)
    #tracksGraph.SetMarkerSize(2)
    #multiGraph.Add(isoTracksGraph)
    
    #if single_events:
    #    legend.AddEntry(isoTracksGraph, "Two Iso Tracks", "lp")
    #else:
    #    legend.AddEntry(isoTracksGraph, "Matched Iso Tracks", "lp")
    
    
    n = len(recoLeptons)
    x, y = array('d'), array('d')
    for i, j in recoLeptons.items():
        eff = float(j)/genLeptons[i]
        x.append(float(i))
        y.append(eff)
    print(n, x, y)
    recoLeptonsGraph = TGraph(n, x, y)
    recoLeptonsGraph.SetMarkerColor(kBlue)
    recoLeptonsGraph.SetMarkerStyle(20)
    #recoLeptonsGraph.SetMarkerSize(2)
    multiGraph.Add(recoLeptonsGraph)
    if single_events:
        legend.AddEntry(recoLeptonsGraph, "Two Reco", "lp")
    else:
        legend.AddEntry(recoLeptonsGraph, "Matched Reco Leptons", "lp")
    
    n = len(recoSosLeptons)
    x, y = array('d'), array('d')
    for i, j in recoSosLeptons.items():
        eff = float(j)/genLeptons[i]
        x.append(float(i))
        y.append(eff)
    print(n, x, y)
    recoSosLeptonsGraph = TGraph(n, x, y)
    recoSosLeptonsGraph.SetMarkerColor(kTeal-7)
    recoSosLeptonsGraph.SetMarkerStyle(20)
    #recoLeptonsGraph.SetMarkerSize(2)
    multiGraph.Add(recoSosLeptonsGraph)
    if single_events:
        legend.AddEntry(recoSosLeptonsGraph, "Two SOS Reco", "lp")
    else:
        legend.AddEntry(recoSosLeptonsGraph, "Matched SOS Reco Leptons", "lp")
    
    n = len(nonRecoTracks)
    x, y = array('d'), array('d')
    for i, j in nonRecoTracks.items():
        eff = float(j)/genLeptons[i]
        x.append(float(i))
        y.append(eff)
    print(n, x, y)
    nonRecoTracksGraph = TGraph(n, x, y)
    nonRecoTracksGraph.SetMarkerColor(kRed)
    nonRecoTracksGraph.SetMarkerStyle(20)
    #nonRecoTracksGraph.SetMarkerSize(2)
    if single_events:
        legend.AddEntry(nonRecoTracksGraph, "One Reco One Track", "lp")
    else:
        legend.AddEntry(nonRecoTracksGraph, "Exclusive Tracks", "lp")
    
    
    multiGraph.Add(nonRecoTracksGraph)
    
    n = len(nonRecoIsoTracks)
    x, y = array('d'), array('d')
    for i, j in nonRecoIsoTracks.items():
        eff = float(j)/genLeptons[i]
        x.append(float(i))
        y.append(eff)
    print(n, x, y)
    nonRecoIsoTracksGraph = TGraph(n, x, y)
    nonRecoIsoTracksGraph.SetMarkerColor(kRed)
    nonRecoIsoTracksGraph.SetMarkerStyle(21)
    #nonRecoTracksGraph.SetMarkerSize(2)
    #if single_events:
    #    legend.AddEntry(nonRecoIsoTracksGraph, "One Reco One Iso Track", "lp")
    #else:
    #    legend.AddEntry(nonRecoIsoTracksGraph, "Exclusive Iso Tracks", "lp")
    
    
    #multiGraph.Add(nonRecoIsoTracksGraph)
    
    multiGraph.Draw("AP")
    
    multiGraph.GetXaxis().SetTitle("#DeltaM")
    multiGraph.GetYaxis().SetTitle("Efficiency")
    
    multiGraph.GetYaxis().SetTitleOffset(1.15)
    
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetNColumns(1)
    legend.Draw("SAME")
    
    c1.Print("eff.pdf")
    
    
main()

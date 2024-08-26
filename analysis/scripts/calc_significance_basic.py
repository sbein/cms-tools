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
#import numpy

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/"))
#sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes"))
import utils
import analysis_ntuples

gROOT.SetBatch(True)
gStyle.SetOptStat(0)
TH1D.SetDefaultSumw2()

#gROOT.ProcessLine(open(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes/calcLlhdSingleCount.cc")).read())
#exec('from ROOT import *')

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Plot skims for x1x2x1 process with BDTs.')
parser.add_argument('-sam', '--sam', dest='sam', help='Sam', action='store_true')
args = parser.parse_args()

output_file = None

######## END OF CMDLINE ARGUMENTS ########

observable = "invMass"
binsNumber = 30
minX = 0
maxX = 15

observable = "dilepBDT"
binsNumber = 30
minX = -0.6
maxX = 0.6

sig_method = "rsb"

sam = args.sam

signal_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/sum"
bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/type_sum"

defaultJetIsoSetting = "CorrJetIso10"

categories = [
    {"name" : "veto", "condition" : "&& veto$LEPTONS$ISOSTR"},
    {"name" : "no-veto", "condition" : ""}
]

def main():
    print("Start: " + datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    
    c1 = TCanvas("c1", "c1", 800, 800)
    c1.cd()
    
    signal_histograms = {}
    bg_histograms = {}
    significance = {}
    
    for filename in glob(bg_dir + "/*"):
        print("Opening", filename)

        f = TFile(filename)
        c = f.Get('tEvent')
        
        # for CorrJetObs in utils.leptonIsolationList:
#             ptRanges = [""]
#             if CorrJetObs == "CorrJetIso":
#                  ptRanges = utils.leptonCorrJetIsoPtRange
#             for ptRange in ptRanges:
#                 isoStr = CorrJetObs + str(ptRange)
                
        isoStr = defaultJetIsoSetting

        for lep in ["Muons", "Electrons"]:
            
            shortLep ="m"
            if lep == "Electrons":
                shortLep ="e"
            
            for category in categories:
                
                catStr = category["name"]
                catCond = category["condition"].replace("$LEPTONS", lep).replace("$ISOSTR", isoStr)
                
                c1.cd()
                basename = os.path.basename(filename).split(".")[0]
                hist = utils.getHistogramFromTree(basename + "exTrack_dilepBDT" + lep + isoStr, c, "exTrack_dilepBDT" + isoStr, 10, -0.6, 0.7, str(utils.LUMINOSITY) + "* passedMhtMet6pack * tEffhMetMhtRealXMht2016 * Weight * (exclusiveTrack" + isoStr + " == 1 && MHT >= 220 && MET >= 200 && exTrack_invMass" + isoStr + " < 30 && BTagsDeepMedium == 0 && exclusiveTrackLeptonFlavour" + isoStr + " == \"" + lep + "\" " + catCond + ")", True)
                hist.Sumw2()
    
                if bg_histograms.get(isoStr) is None:
                    bg_histograms[isoStr] = {}
                if bg_histograms[isoStr].get(catStr) is None:
                    bg_histograms[isoStr][catStr] = {}
            
                if bg_histograms[isoStr][catStr].get("t" + shortLep) is None:
                    bg_histograms[isoStr][catStr]["t" + shortLep] = hist
                else:
                     bg_histograms[isoStr][catStr]["t" + shortLep].Add(hist)
            
                for orth in (True,False):
                    if not orth:
                        hist = utils.getHistogramFromTree(basename + "dilepBDT" + lep + isoStr, c, "dilepBDT" + isoStr, 10, 0, 0.7, str(utils.LUMINOSITY) + "* passedMhtMet6pack * tEffhMetMhtRealXMht2016 * Weight * (twoLeptons" + isoStr + " == 1 && MHT >= 220 &&  MET >= 200 && invMass" + isoStr + " < 12  && invMass" + isoStr + " > 0.4 && !(invMass" + isoStr + " > 3 && invMass" + isoStr + " < 3.2) && !(invMass" + isoStr + " > 0.75 && invMass" + isoStr + " < 0.81) && dilepBDT" + isoStr + " > 0 && BTagsDeepMedium == 0 && @leptons" + isoStr + ".size() == 2 && leptonFlavour" + isoStr + " == \"" + lep + "\" && sameSign" + isoStr + " == 0  " + catCond + ")", True)
                    else:
                        hist = utils.getHistogramFromTree(basename + "dilepBDT" + lep + isoStr, c, "dilepBDT" + isoStr, 10, 0, 0.7, str(utils.LUMINOSITY) + "* passedMhtMet6pack * tEffhMetMhtRealXMht2016 * Weight * (twoLeptons" + isoStr + " == 1 && (leptons" + isoStr + "[1].Pt() <= 3.5 || deltaR" + isoStr + " <= 0.3) && MHT >= 220 &&  MET >= 200 && invMass" + isoStr + " < 12  && invMass" + isoStr + " > 0.4 && !(invMass" + isoStr + " > 3 && invMass" + isoStr + " < 3.2) && !(invMass" + isoStr + " > 0.75 && invMass" + isoStr + " < 0.81) && dilepBDT" + isoStr + " > 0 && BTagsDeepMedium == 0 && @leptons" + isoStr + ".size() == 2 && leptonFlavour" + isoStr + " == \"" + lep + "\" && sameSign" + isoStr + " == 0  " + catCond + ")", True)
                    hist.Sumw2()
                    orthStr = "orth" if orth else "non-orth"
                    if bg_histograms[isoStr][catStr].get(shortLep + shortLep) is None:
                        bg_histograms[isoStr][catStr][shortLep + shortLep] = {}
                    if bg_histograms[isoStr][catStr][shortLep + shortLep].get(orthStr) is None:
                        bg_histograms[isoStr][catStr][shortLep + shortLep][orthStr] = hist
                    else:
                        bg_histograms[isoStr][catStr][shortLep + shortLep][orthStr].Add(hist)

        f.Close()
    
    print("Getting signals...")
    
    for filename in glob(signal_dir + "/*"):
        print("Opening", filename    )
        deltaM = os.path.basename(filename).split('_')[-1].split('Chi20Chipm')[0].split('dm')[1]
        mu = os.path.basename(filename).split('_')[1].split('mu')[1]
        print("deltaM=" + deltaM)
        print("mu=" + mu)
        f = TFile(filename)
        c = f.Get('tEvent')
        
        if signal_histograms.get(mu) is None:
            signal_histograms[mu] = {}
            significance[mu] = {}
        if signal_histograms[mu].get(deltaM) is None:
            signal_histograms[mu][deltaM] = {}
            significance[mu][deltaM] = {}
            
        # for CorrJetObs in utils.leptonIsolationList:
#             ptRanges = [""]
#             if CorrJetObs == "CorrJetIso":
#                  ptRanges = utils.leptonCorrJetIsoPtRange
#             for ptRange in ptRanges:
#                 isoStr = CorrJetObs + str(ptRange)
                
        isoStr = defaultJetIsoSetting
        
        if signal_histograms[mu][deltaM].get(isoStr) is None:
            signal_histograms[mu][deltaM][isoStr] = {}
            significance[mu][deltaM][isoStr] = {}
        
        for lep in ["Muons", "Electrons"]:
            print(mu, deltaM, isoStr, lep)
            
            shortLep ="m"
            if lep == "Electrons":
                shortLep ="e"
            
            for category in categories:
                
                catStr = category["name"]
                catCond = category["condition"].replace("$LEPTONS", lep).replace("$ISOSTR", isoStr)
                
                c1.cd()
                hist = utils.getHistogramFromTree(mu + deltaM + isoStr + "_1t_" + lep, c, "exTrack_dilepBDT" + isoStr, 10, -0.6, 0.7, str(utils.LUMINOSITY) + "* passedMhtMet6pack * tEffhMetMhtRealXMht2016 *  Weight * (exclusiveTrack" + isoStr + " == 1 && MHT >= 220 && MET >= 200 && exTrack_invMass" + isoStr + " < 30 && BTagsDeepMedium == 0 && exclusiveTrackLeptonFlavour" + isoStr + " == \"" + lep + "\" " + catCond + ")", True)
                hist.Sumw2()
                
                if signal_histograms[mu][deltaM][isoStr].get(catStr) is None:
                    signal_histograms[mu][deltaM][isoStr][catStr] = {}
                    significance[mu][deltaM][isoStr][catStr] = {}
                
                signal_histograms[mu][deltaM][isoStr][catStr]["t" + shortLep] = hist
                #sig = utils.calcSignificance(hist, bg_histograms[isoStr][catStr]["t" + shortLep], False)
                sig = utils.calcSignificanceNoAcc(hist, bg_histograms[isoStr][catStr]["t" + shortLep], False)
                
                significance[mu][deltaM][isoStr][catStr]["t" + shortLep] = sig
                for orth in (True,False):
                    if not orth:
                        hist = utils.getHistogramFromTree(mu + deltaM + isoStr + "_2l_" + lep, c, "dilepBDT" + isoStr, 10, 0, 0.7, str(utils.LUMINOSITY) + "* passedMhtMet6pack * tEffhMetMhtRealXMht2016 * Weight * (twoLeptons" + isoStr + " == 1 && MHT >= 220 &&  MET >= 200 && invMass" + isoStr + " < 12  && invMass" + isoStr + " > 0.4 && !(invMass" + isoStr + " > 3 && invMass" + isoStr + " < 3.2) && !(invMass" + isoStr + " > 0.75 && invMass" + isoStr + " < 0.81) && dilepBDT" + isoStr + " > 0 && BTagsDeepMedium == 0 && @leptons" + isoStr + ".size() == 2 && leptonFlavour" + isoStr + " == \"" + lep + "\" && sameSign" + isoStr + " == 0 " + catCond + ")", True)
                    else:
                        hist = utils.getHistogramFromTree(mu + deltaM + isoStr + "_2l_" + lep, c, "dilepBDT" + isoStr, 10, 0, 0.7, str(utils.LUMINOSITY) + "* passedMhtMet6pack * tEffhMetMhtRealXMht2016 * Weight * (twoLeptons" + isoStr + " == 1 && (leptons" + isoStr + "[1].Pt() <= 3.5 || deltaR" + isoStr + " <= 0.3) && MHT >= 220 &&  MET >= 200 && invMass" + isoStr + " < 12  && invMass" + isoStr + " > 0.4 && !(invMass" + isoStr + " > 3 && invMass" + isoStr + " < 3.2) && !(invMass" + isoStr + " > 0.75 && invMass" + isoStr + " < 0.81) && dilepBDT" + isoStr + " > 0 && BTagsDeepMedium == 0 && @leptons" + isoStr + ".size() == 2 && leptonFlavour" + isoStr + " == \"" + lep + "\" && sameSign" + isoStr + " == 0 " + catCond + ")", True)
                    hist.Sumw2()
                    orthStr = "orth" if orth else "non-orth"
                
                    if signal_histograms[mu][deltaM][isoStr][catStr].get(shortLep + shortLep) is None:
                        signal_histograms[mu][deltaM][isoStr][catStr][shortLep + shortLep] = {}
                        significance[mu][deltaM][isoStr][catStr][shortLep + shortLep] = {}
                
                    signal_histograms[mu][deltaM][isoStr][catStr][shortLep + shortLep][orthStr] = hist
                    sig = utils.calcSignificanceNoAcc(hist, bg_histograms[isoStr][catStr][shortLep + shortLep][orthStr], False)
                    significance[mu][deltaM][isoStr][catStr][shortLep + shortLep][orthStr] = sig
                    
        f.Close()
    
    print(significance)
    
    categoriesCSV = ",".join(sorted(significance[mu][deltaM][isoStr].keys()))
    
    print("mu,deltaM,iso,category,ee,orth-ee,mm,orth-mm,te,tm")

    for mu in sorted(significance.keys()):
        for deltaM in sorted(significance[mu].keys()):
            for isoStr in sorted(significance[mu][deltaM].keys()):
                for catStr in sorted(significance[mu][deltaM][isoStr].keys()):
                    print( ",".join((mu,deltaM,isoStr,catStr,"{:.2f}".format(significance[mu][deltaM][isoStr][catStr]["ee"]["non-orth"]),"{:.2f}".format(significance[mu][deltaM][isoStr][catStr]["ee"]["orth"]),"{:.2f}".format(significance[mu][deltaM][isoStr][catStr]["mm"]["non-orth"]),"{:.2f}".format(significance[mu][deltaM][isoStr][catStr]["mm"]["orth"]),"{:.2f}".format(significance[mu][deltaM][isoStr][catStr]["te"]),"{:.2f}".format(significance[mu][deltaM][isoStr][catStr]["tm"]))))

    
    print("End: " + datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    

main()
exit(0)


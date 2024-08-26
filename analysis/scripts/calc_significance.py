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
import numpy

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes"))
import utils
import analysis_ntuples

gROOT.SetBatch(True)
gStyle.SetOptStat(0)
TH1D.SetDefaultSumw2()

gROOT.ProcessLine(open(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes/calcLlhdSingleCount.cc")).read())
exec('from ROOT import *')

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Plot skims for x1x2x1 process with BDTs.')
parser.add_argument('-o', '--output_file', nargs=1, help='Output Filename', required=False)
parser.add_argument('-sam', '--sam', dest='sam', help='Sam', action='store_true')
args = parser.parse_args()

output_file = None

if args.output_file:
    output_file = args.output_file[0]
else:
    output_file = "obs.pdf"

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
#sig_method = "Llhd"

sam = args.sam

histograms_defs = [    
    #NORMAL
    { "obs" : "invMass", "minX" : 0, "maxX" : 30, "bins" : 90, "units" : "GeV" },
    { "obs" : "trackBDT", "minX" : 0, "maxX" : 0.7, "bins" : 30 },
    { "obs" : "dilepBDT", "minX" : -0.2, "maxX" : 0.6, "bins" : 30 },
]

cuts = {
    "2l" : "deltaR <= 1.2  && leptons[0].Pt() < 15 && Ht >= 120 && (leptons[1].Pt() <= 3.5 || deltaR < 0.3) && deltaEta < 1 && mt1 <= 40 && mt2 <= 40 && dilepHt >= 170 && DeltaPhiLeadingJetDilepton >= 1.7",
    "1t1l" : "lepton.Pt() < 15 && Mht >=140 && mtl <= 60 && deltaR <= 1.7 && MinDeltaPhiMhtJets >= 1 && DeltaEtaLeadingJetDilepton <= 2.2 && DeltaPhiLeadingJetDilepton >= 1.8 && deltaPhi <= 1.3 && deltaEta <= 1.2 && LeadingJetPt >= 100 && mtt <= 50 && mt1 <= 60 && mt2 <= 50 && Ht >= 140 &&  MinDeltaPhiMetJets >= 1.3"
}

paths = {
    "1t1l" : "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1",
    "2l" : "/afs/desy.de/user/n/nissanuv/nfs/2lx1x2x1"
}

lepton_training = True
compare_isolation = True
no_rect = True


def performScanForFile(file, type, maxSignalRange=None, ignoreCS = True, noScan = False):
    print("Performing Scan for file", file)
    print("Called with ignoreCS", ignoreCS, "noScan", noScan)
    scan = []
    basicCond = None
    if type == "2l":
        basicCond = str(utils.LUMINOSITY) + " * Weight * ((leptons[1].Pt() <= 3.5 || deltaR < 0.3) && Met >= 200 && invMass < 30 && dilepBDT >= "
    else:
        basicCond = str(utils.LUMINOSITY) + " * Weight * (Met >= 200 && invMass < 30 && dilepBDT >= "
    rootFile = TFile(file)
    c = rootFile.Get('tEvent')
    i = 0
    if noScan:
        print("Wanted no scan")
        dilepBDT = -0.3
        cond = basicCond + "{:.2f}".format(dilepBDT) + ")"
        hist = utils.getHistogramFromTree("sig_" + "{:.2f}".format(dilepBDT), c, observable, binsNumber, minX, maxX, cond, True)
        if not hist:
            print("WTF")
            exit(0)
        scan.append(hist)
    else:
        for dilepBDT in numpy.arange(-0.3, 0.6, 0.05):
            i += 1
            if maxSignalRange is not None and i > maxSignalRange:
                print("*** breaking scan because of signal at", i, "maxSignalRange=", maxSignalRange)
                break
            cond = basicCond + "{:.2f}".format(dilepBDT) + ")"
            if not ignoreCS:
                cond += " * BranchingRatio"
            #print("cond=" + cond)
            hist = utils.getHistogramFromTree("sig_" + "{:.2f}".format(dilepBDT), c, observable, binsNumber, minX, maxX, cond, True)
            if not hist:
                print("WTF")
                exit(0)
            if hist.Integral() == 0:
                print("Stopping at value", dilepBDT)
                break
            scan.append(hist)
    return scan

def main():
    print("Start: " + datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    
    significance = {}
    for type in ["1t1l","2l"]:
        bgHistograms = {}
        signalHistograms = {}    
        bgHistograms[type] = {}
        signalHistograms[type] = {}
        significance[type] = {}
        trainGroupsToCheck = utils.trainGroupsOrder + ["all", "1t1l","2l"]
        if sam:
            trainGroupsToCheck = ["all", "1t1l","2l"]
        for trainGroup in trainGroupsToCheck:
            print("Checking train group " + trainGroup)
        
            signalHistograms[type][trainGroup] = {}
        
            maxSignalRange = 0
        
            groups = None
            if trainGroup in ["all", "1t1l","2l"]:
                groups = [trainGroup]
            else:
                groups = utils.trainGroups[trainGroup]
        
            for group in groups:
                print("Checking group", group)
                signalFilesPath = None
                if group in ["all", "1t1l","2l"]:
                    if not sam:
                        signalFilesPath = paths[type] + "/signal/skim_dilepton_signal_bdt_all/single/*"
                    else:
                        signalFilesPath = paths[type] + "/signal/skim_sam_dilepton_signal_bdt_all/single/*"
                else:
                        signalFilesPath = paths[type] + "/signal/skim_dilepton_signal_bdt/single/*" + group + "*"
                #signalFiles = glob(signalFilesPath + "mChipm100GeV_dm2p26GeV_.root")
                signalFiles = glob(signalFilesPath)
                for signalFile in signalFiles:
                    signalFileName = os.path.basename(signalFile).split(".")[0]
                    print("Scanning file", signalFileName)
                    if group in ["1t1l","2l"]:
                        if group != type:
                            continue
                        cond = str(utils.LUMINOSITY) + " * Weight * (Met >= 200 && invMass < 30 && " + cuts[group] + ")"
                        if sam:
                            cond += " * BranchingRatio"
                        print("opening file", signalFile, "with cond ", cond)
                        rootFile = TFile(signalFile)
                        c = rootFile.Get('tEvent')
                        hist = utils.getHistogramFromTree("sig_" + group, c, observable, binsNumber, minX, maxX, cond, True)
                        signalHistograms[type][trainGroup][signalFileName] = hist
                    else:
                        ignoreCS = True
                        noScan = False
                        if sam:
                            ignoreCS = False
                        if observable == "dilepBDT":
                            noScan = True
                        print("calling scan with ignoreCS", ignoreCS, " noScan", noScan)
                        signalHistograms[type][trainGroup][signalFileName] = performScanForFile(signalFile, type, None, ignoreCS, noScan)
                        if len(signalHistograms[type][trainGroup][signalFileName]) > maxSignalRange:
                            maxSignalRange = len(signalHistograms[type][trainGroup][signalFileName])
        
            print("Maximum signal range for", trainGroup, " is", maxSignalRange)
            bgFilesPath = None
            if trainGroup in ["1t1l","2l"]:
                bgFilesPath = paths[type] + "/bg/skim_dilepton_signal_bdt/all/single/*"
            else:
                bgFilesPath = paths[type] + "/bg/skim_dilepton_signal_bdt/" + trainGroup + "/single/*"
            #print("Checking files", bgFilesPath)
            print("bgFilesPath", bgFilesPath)
            bgFiles = glob(bgFilesPath)
        
            for bgFile in bgFiles:
                print("Scanning", bgFile)
                if trainGroup in ["1t1l","2l"]:
                    print(">>>>>>> trainGroup", trainGroup)
                    if trainGroup != type:
                        print("Skipping trainGroup", trainGroup, "for type", type)
                        continue
                    print("******* BG trainGroup", trainGroup)
                    cond = str(utils.LUMINOSITY) + " * Weight * (Met >= 200 && invMass < 30 && " + cuts[group] + ")"
                    rootFile = TFile(bgFile)
                    c = rootFile.Get('tEvent')
                    hist = utils.getHistogramFromTree("bg_" + group, c, observable, binsNumber, minX, maxX, cond, True)
                    if bgHistograms[type].get(trainGroup) is None:
                        bgHistograms[type][trainGroup] = hist
                    else:
                        bgHistograms[type][trainGroup].Add(hist)
                else:
                    print("maxSignalRange", maxSignalRange)
                    scan = performScanForFile(bgFile, type, maxSignalRange)
                    if bgHistograms[type].get(trainGroup) is None:
                        bgHistograms[type][trainGroup] = scan
                    else:
                        for i in range(len(scan)):
                            if i >= len(bgHistograms[type][trainGroup]):
                                print("Expending scan")
                                bgHistograms[type][trainGroup].append(scan[i])
                            else:
                                bgHistograms[type][trainGroup][i].Add(scan[i])
            if bgHistograms[type].get(trainGroup) is None:
                print("bgHistograms not ready for", trainGroup)
                continue
            bgScan = bgHistograms[type][trainGroup]
            ignoreCS = False
            if sam:
                ignoreCS = True
            
            for signalFileName in signalHistograms[type][trainGroup]:
                if trainGroup in ["1t1l","2l"]:
                    if trainGroup != type:
                        continue
                    sigHist = signalHistograms[type][trainGroup][signalFileName]
                    bgHist = bgHistograms[type][trainGroup]
                    sig = 0
                    if sig_method == "rsb":
                        sig = utils.calcSignificance(sigHist, bgHist, ignoreCS)
                    else:
                        sig = utils.calcSignificanceLlhdSingleCount(sigHist, bgHist)
                    
                    #if sig > 0:
                    #    print("Greater!", sig, "for rect", signalFileName)
                    if significance[type].get(trainGroup) is None:
                        significance[type][trainGroup] = {}
                    print("Adding to significance file", signalFileName)
                    significance[type][trainGroup][signalFileName] = sig
                    #print("After addition")
                    #print(significance)
                else:
                    #print("Calculating Significance for", signalFileName)
                    sigScan = []
                    dilepBDT = -0.3
                    i = 0
                    for sigHist in signalHistograms[type][trainGroup][signalFileName]:
                        #print("dilepBDT=" + str(dilepBDT))
                        i += 1
                        dilepBDT += 0.05
                        if i > len(bgHistograms[type][trainGroup]):
                            print("Breaking scan at ", dilepBDT)
                            break
                        bgHist = bgHistograms[type][trainGroup][i-1]
                        sig = 0
                        if sig_method == "rsb":
                            sig = utils.calcSignificance(sigHist, bgHist, ignoreCS)
                        else:
                            sig = utils.calcSignificanceLlhdSingleCount(sigHist, bgHist)
                        #if sig > 0:
                        #    print("Greater!", sig, "for", type, signalFileName)
                        sigScan.append(sig)
            
                    print("sigScan for", trainGroup, signalFileName, sigScan#, "min", min(sigScan))
                    if significance[type].get(trainGroup) is None:
                        significance[type][trainGroup] = {}
                    if len(sigScan) == 0:
                        significance[type][trainGroup][signalFileName] = 0
                    else:
                        if sig_method == "rsb":
                            significance[type][trainGroup][signalFileName] = max(sigScan)
                        else:
                            significance[type][trainGroup][signalFileName] = min(sigScan)
    
    
    #significance = {'2l': {'2l': {'mChipm160GeV_dm0p44GeV_': 0.0, 'mChipm180GeV_dm5p29GeV_': 0.07551929728621258, 'mChipm200GeV_dm4p3GeV_': 0.02253163914333506, 'mChipm500GeV_dm0p53GeV_': 0.0, 'mChipm115GeV_dm6p27GeV_': 0.0, 'mChipm140GeV_dm4p28GeV_': 0.1261404896783124, 'mChipm200GeV_dm2p3GeV_': 0.028682721618256173, 'mChipm500GeV_dm2p33GeV_': 0.004089909531025812, 'mChipm115GeV_dm0p77GeV_': 0.23881328391373574, 'mChipm225GeV_dm0p8GeV_': 0.0, 'mChipm180GeV_dm6p29GeV_': 0.0, 'mChipm180GeV_dm0p59GeV_': 0.0, 'mChipm500GeV_dm5p33GeV_': 0.01577980402980185, 'mChipm160GeV_dm5p29GeV_': 0.36226096466070085, 'mChipm225GeV_dm2p3GeV_': 0.049369290394491554, 'mChipm100GeV_dm0p56GeV_': 0.0, 'mChipm180GeV_dm3p29GeV_': 0.8072665615521555, 'mChipm200GeV_dm6p3GeV_': 0.0, 'mChipm160GeV_dm3p29GeV_': 0.7631769821910923, 'mChipm180GeV_dm4p29GeV_': 0.19636477138395744, 'mChipm500GeV_dm1p03GeV_': 0.0, 'mChipm100GeV_dm0p96GeV_': 3.7680687765478655, 'mChipm500GeV_dm0p43GeV_': 0.0, 'mChipm250GeV_dm2p31GeV_': 0.04189351264856475, 'mChipm250GeV_dm0p61GeV_': 0.0, 'mChipm140GeV_dm1p78GeV_': 1.2165583079457931, 'mChipm115GeV_dm3p27GeV_': 2.3973607707258218, 'mChipm160GeV_dm1p29GeV_': 0.037799969783616535, 'mChipm200GeV_dm5p3GeV_': 0.03292756643109106, 'mChipm100GeV_dm0p41GeV_': 0.28336538493352775, 'mChipm115GeV_dm0p97GeV_': 0.6086150101226576, 'mChipm200GeV_dm1p0GeV_': 0.14582837352966277, 'mChipm140GeV_dm2p28GeV_': 0.7068266418892982, 'mChipm100GeV_dm2p26GeV_': 4.340224000828833, 'mChipm500GeV_dm4p33GeV_': 0.0032268627781113198, 'mChipm180GeV_dm0p49GeV_': 0.0, 'mChipm100GeV_dm6p26GeV_': 0.0, 'mChipm300GeV_dm0p46GeV_': 0.0, 'mChipm300GeV_dm1p31GeV_': 0.0, 'mChipm100GeV_dm4p26GeV_': 0.3806607613236031, 'mChipm160GeV_dm0p49GeV_': 0.07600709055800008, 'mChipm180GeV_dm1p79GeV_': 0.225089079018234, 'mChipm160GeV_dm2p29GeV_': 0.21201043661030672, 'mChipm140GeV_dm0p78GeV_': 0.0, 'mChipm400GeV_dm0p224GeV_': 0.004597262189298272, 'mChipm160GeV_dm1p79GeV_': 0.37047103377666624, 'mChipm200GeV_dm1p3GeV_': 0.3375344434279763, 'mChipm250GeV_dm4p31GeV_': 0.013176525166881524, 'mChipm100GeV_dm0p26GeV_': 0.0, 'mChipm300GeV_dm0p21GeV_': 0.0, 'mChipm250GeV_dm5p31GeV_': 0.045647177611062684, 'mChipm180GeV_dm2p29GeV_': 0.11234394971217414, 'mChipm180GeV_dm1p29GeV_': 0.42372219067547034, 'mChipm140GeV_dm5p28GeV_': 0.10032151486684084, 'mChipm115GeV_dm0p17GeV_': 0.0, 'mChipm500GeV_dm1p83GeV_': 0.0026669096581372034, 'mChipm115GeV_dm0p57GeV_': 0.0, 'mChipm115GeV_dm5p27GeV_': 0.09688162261455202, 'mChipm100GeV_dm0p76GeV_': 0.19418615944436338, 'mChipm115GeV_dm4p27GeV_': 0.5238589751879157, 'mChipm275GeV_dm0p312GeV_': 0.0, 'mChipm225GeV_dm0p45GeV_': 0.0, 'mChipm500GeV_dm1p33GeV_': 0.0, 'mChipm500GeV_dm3p33GeV_': 0.001357813409102185, 'mChipm500GeV_dm0p23GeV_': 0.0, 'mChipm100GeV_dm5p26GeV_': 4.060382235597963, 'mChipm140GeV_dm3p28GeV_': 1.213870824763569, 'mChipm250GeV_dm1p81GeV_': 0.00926684327213774, 'mChipm225GeV_dm0p2GeV_': 0.0, 'mChipm115GeV_dm2p27GeV_': 2.7408137466856104, 'mChipm300GeV_dm4p31GeV_': 0.011351442815145597, 'mChipm100GeV_dm1p76GeV_': 1.2753790791651751, 'mChipm100GeV_dm3p26GeV_': 1.1815185419462095, 'mChipm115GeV_dm1p27GeV_': 0.23823609659168726, 'mChipm275GeV_dm0p412GeV_': 0.0, 'mChipm225GeV_dm3p3GeV_': 0.1940271508125967, 'mChipm140GeV_dm0p98GeV_': 0.09956232656197977, 'mChipm160GeV_dm4p29GeV_': 0.3816257955321174, 'mChipm300GeV_dm3p31GeV_': 0.02548883786126789, 'mChipm250GeV_dm3p31GeV_': 0.0385846046701078, 'mChipm140GeV_dm0p28GeV_': 0.0, 'mChipm140GeV_dm0p38GeV_': 0.0, 'mChipm200GeV_dm3p3GeV_': 0.38279455194688944, 'mChipm300GeV_dm1p81GeV_': 0.014281247025868842, 'mChipm250GeV_dm1p01GeV_': 0.0, 'mChipm275GeV_dm0p212GeV_': 0.0, 'mChipm160GeV_dm0p99GeV_': 0.0, 'mChipm225GeV_dm1p8GeV_': 0.02195257572389453, 'mChipm500GeV_dm0p48GeV_': 0.0, 'mChipm300GeV_dm2p31GeV_': 0.07633037842893708, 'mChipm200GeV_dm1p8GeV_': 0.08427907461400076, 'mChipm225GeV_dm0p3GeV_': 0.0, 'mChipm115GeV_dm1p77GeV_': 0.6218820227342045, 'mChipm200GeV_dm0p8GeV_': 0.0, 'mChipm100GeV_dm1p26GeV_': 3.769446906945395, 'mChipm225GeV_dm1p0GeV_': 0.014243411827769453}, 'all': {'mChipm160GeV_dm0p44GeV_': 0, 'mChipm180GeV_dm5p29GeV_': 0, 'mChipm200GeV_dm4p3GeV_': 0, 'mChipm500GeV_dm0p53GeV_': 0, 'mChipm115GeV_dm6p27GeV_': 0, 'mChipm140GeV_dm4p28GeV_': 0, 'mChipm200GeV_dm2p3GeV_': 0, 'mChipm500GeV_dm2p33GeV_': 0, 'mChipm115GeV_dm0p77GeV_': 0, 'mChipm225GeV_dm0p8GeV_': 0, 'mChipm180GeV_dm6p29GeV_': 0, 'mChipm180GeV_dm0p59GeV_': 0, 'mChipm500GeV_dm5p33GeV_': 0, 'mChipm160GeV_dm5p29GeV_': 0, 'mChipm225GeV_dm2p3GeV_': 0, 'mChipm100GeV_dm0p56GeV_': 0, 'mChipm180GeV_dm3p29GeV_': 0, 'mChipm200GeV_dm6p3GeV_': 0, 'mChipm160GeV_dm3p29GeV_': 0, 'mChipm180GeV_dm4p29GeV_': 0, 'mChipm500GeV_dm1p03GeV_': 0, 'mChipm100GeV_dm0p96GeV_': 0, 'mChipm500GeV_dm0p43GeV_': 0, 'mChipm250GeV_dm2p31GeV_': 0, 'mChipm250GeV_dm0p61GeV_': 0, 'mChipm140GeV_dm1p78GeV_': 0, 'mChipm115GeV_dm3p27GeV_': 0, 'mChipm160GeV_dm1p29GeV_': 0, 'mChipm200GeV_dm5p3GeV_': 0, 'mChipm100GeV_dm0p41GeV_': 0, 'mChipm115GeV_dm0p97GeV_': 0, 'mChipm200GeV_dm1p0GeV_': 0, 'mChipm140GeV_dm2p28GeV_': 0, 'mChipm100GeV_dm2p26GeV_': 0, 'mChipm500GeV_dm4p33GeV_': 0, 'mChipm180GeV_dm0p49GeV_': 0, 'mChipm100GeV_dm6p26GeV_': 0, 'mChipm300GeV_dm0p46GeV_': 0, 'mChipm300GeV_dm1p31GeV_': 0, 'mChipm100GeV_dm4p26GeV_': 0, 'mChipm160GeV_dm0p49GeV_': 0, 'mChipm180GeV_dm1p79GeV_': 0, 'mChipm160GeV_dm2p29GeV_': 0, 'mChipm140GeV_dm0p78GeV_': 0, 'mChipm400GeV_dm0p224GeV_': 0, 'mChipm160GeV_dm1p79GeV_': 0, 'mChipm200GeV_dm1p3GeV_': 0, 'mChipm250GeV_dm4p31GeV_': 0, 'mChipm100GeV_dm0p26GeV_': 0, 'mChipm300GeV_dm0p21GeV_': 0, 'mChipm250GeV_dm5p31GeV_': 0, 'mChipm180GeV_dm2p29GeV_': 0, 'mChipm180GeV_dm1p29GeV_': 0, 'mChipm140GeV_dm5p28GeV_': 0, 'mChipm115GeV_dm0p17GeV_': 0, 'mChipm500GeV_dm1p83GeV_': 0, 'mChipm115GeV_dm0p57GeV_': 0, 'mChipm115GeV_dm5p27GeV_': 0, 'mChipm100GeV_dm0p76GeV_': 0, 'mChipm115GeV_dm4p27GeV_': 0, 'mChipm275GeV_dm0p312GeV_': 0, 'mChipm225GeV_dm0p45GeV_': 0, 'mChipm500GeV_dm1p33GeV_': 0, 'mChipm500GeV_dm3p33GeV_': 0, 'mChipm500GeV_dm0p23GeV_': 0, 'mChipm100GeV_dm5p26GeV_': 0, 'mChipm140GeV_dm3p28GeV_': 0, 'mChipm250GeV_dm1p81GeV_': 0, 'mChipm225GeV_dm0p2GeV_': 0, 'mChipm115GeV_dm2p27GeV_': 0, 'mChipm300GeV_dm4p31GeV_': 0, 'mChipm100GeV_dm1p76GeV_': 0, 'mChipm100GeV_dm3p26GeV_': 0, 'mChipm115GeV_dm1p27GeV_': 0, 'mChipm275GeV_dm0p412GeV_': 0, 'mChipm225GeV_dm3p3GeV_': 0, 'mChipm140GeV_dm0p98GeV_': 0, 'mChipm160GeV_dm4p29GeV_': 0, 'mChipm300GeV_dm3p31GeV_': 0, 'mChipm250GeV_dm3p31GeV_': 0, 'mChipm140GeV_dm0p28GeV_': 0, 'mChipm140GeV_dm0p38GeV_': 0, 'mChipm200GeV_dm3p3GeV_': 0, 'mChipm300GeV_dm1p81GeV_': 0, 'mChipm250GeV_dm1p01GeV_': 0, 'mChipm275GeV_dm0p212GeV_': 0, 'mChipm160GeV_dm0p99GeV_': 0, 'mChipm225GeV_dm1p8GeV_': 0, 'mChipm500GeV_dm0p48GeV_': 0, 'mChipm300GeV_dm2p31GeV_': 0, 'mChipm200GeV_dm1p8GeV_': 0, 'mChipm225GeV_dm0p3GeV_': 0, 'mChipm115GeV_dm1p77GeV_': 0, 'mChipm200GeV_dm0p8GeV_': 0, 'mChipm100GeV_dm1p26GeV_': 0, 'mChipm225GeV_dm1p0GeV_': 0}}, '1t1l': {'all': {'mChipm160GeV_dm0p44GeV_': 0, 'mChipm180GeV_dm5p29GeV_': 0, 'mChipm200GeV_dm4p3GeV_': 0, 'mChipm115GeV_dm0p42GeV_': 0, 'mChipm500GeV_dm0p53GeV_': 0, 'mChipm115GeV_dm6p27GeV_': 0, 'mChipm140GeV_dm4p28GeV_': 0, 'mChipm180GeV_dm0p44GeV_': 0, 'mChipm200GeV_dm2p3GeV_': 0, 'mChipm400GeV_dm0p174GeV_': 0, 'mChipm300GeV_dm0p31GeV_': 0, 'mChipm115GeV_dm0p27GeV_': 0, 'mChipm500GeV_dm2p33GeV_': 0, 'mChipm250GeV_dm0p81GeV_': 0, 'mChipm115GeV_dm0p77GeV_': 0, 'mChipm225GeV_dm0p8GeV_': 0, 'mChipm180GeV_dm6p29GeV_': 0, 'mChipm180GeV_dm0p59GeV_': 0, 'mChipm200GeV_dm0p3GeV_': 0, 'mChipm500GeV_dm0p48GeV_': 0, 'mChipm160GeV_dm5p29GeV_': 0, 'mChipm225GeV_dm2p3GeV_': 0, 'mChipm100GeV_dm0p56GeV_': 0, 'mChipm400GeV_dm0p424GeV_': 0, 'mChipm225GeV_dm0p5GeV_': 0, 'mChipm200GeV_dm0p4GeV_': 0, 'mChipm160GeV_dm3p29GeV_': 0, 'mChipm200GeV_dm6p3GeV_': 0, 'mChipm100GeV_dm0p46GeV_': 0, 'mChipm140GeV_dm0p78GeV_': 0, 'mChipm500GeV_dm1p03GeV_': 0, 'mChipm100GeV_dm0p96GeV_': 0, 'mChipm500GeV_dm0p43GeV_': 0, 'mChipm250GeV_dm2p31GeV_': 0, 'mChipm250GeV_dm0p61GeV_': 0, 'mChipm200GeV_dm0p6GeV_': 0, 'mChipm300GeV_dm0p41GeV_': 0, 'mChipm100GeV_dm6p26GeV_': 0, 'mChipm100GeV_dm0p36GeV_': 0, 'mChipm180GeV_dm0p19GeV_': 0, 'mChipm115GeV_dm3p27GeV_': 0, 'mChipm160GeV_dm1p29GeV_': 0, 'mChipm180GeV_dm0p39GeV_': 0, 'mChipm200GeV_dm5p3GeV_': 0, 'mChipm100GeV_dm0p41GeV_': 0, 'mChipm180GeV_dm4p29GeV_': 0, 'mChipm200GeV_dm1p0GeV_': 0, 'mChipm160GeV_dm0p29GeV_': 0, 'mChipm140GeV_dm2p28GeV_': 0, 'mChipm225GeV_dm0p4GeV_': 0, 'mChipm100GeV_dm2p26GeV_': 0, 'mChipm500GeV_dm4p33GeV_': 0, 'mChipm180GeV_dm0p49GeV_': 0, 'mChipm200GeV_dm0p5GeV_': 0, 'mChipm140GeV_dm1p78GeV_': 0, 'mChipm300GeV_dm0p46GeV_': 0, 'mChipm300GeV_dm1p31GeV_': 0, 'mChipm100GeV_dm4p26GeV_': 0, 'mChipm160GeV_dm0p49GeV_': 0, 'mChipm160GeV_dm0p79GeV_': 0, 'mChipm140GeV_dm1p28GeV_': 0, 'mChipm180GeV_dm1p79GeV_': 0, 'mChipm160GeV_dm2p29GeV_': 0, 'mChipm500GeV_dm0p63GeV_': 0, 'mChipm200GeV_dm0p45GeV_': 0, 'mChipm100GeV_dm0p16GeV_': 0, 'mChipm400GeV_dm0p224GeV_': 0, 'mChipm160GeV_dm1p79GeV_': 0, 'mChipm200GeV_dm1p3GeV_': 0, 'mChipm250GeV_dm4p31GeV_': 0, 'mChipm160GeV_dm0p39GeV_': 0, 'mChipm100GeV_dm0p26GeV_': 0, 'mChipm300GeV_dm0p21GeV_': 0, 'mChipm250GeV_dm5p31GeV_': 0, 'mChipm500GeV_dm1p83GeV_': 0, 'mChipm180GeV_dm2p29GeV_': 0, 'mChipm180GeV_dm1p29GeV_': 0, 'mChipm300GeV_dm0p81GeV_': 0, 'mChipm140GeV_dm5p28GeV_': 0, 'mChipm115GeV_dm0p17GeV_': 0, 'mChipm140GeV_dm0p18GeV_': 0, 'mChipm160GeV_dm0p19GeV_': 0, 'mChipm250GeV_dm1p31GeV_': 0, 'mChipm300GeV_dm1p01GeV_': 0, 'mChipm115GeV_dm0p57GeV_': 0, 'mChipm225GeV_dm1p3GeV_': 0, 'mChipm115GeV_dm5p27GeV_': 0, 'mChipm100GeV_dm0p76GeV_': 0, 'mChipm180GeV_dm0p29GeV_': 0, 'mChipm115GeV_dm4p27GeV_': 0, 'mChipm275GeV_dm0p312GeV_': 0, 'mChipm225GeV_dm0p45GeV_': 0, 'mChipm500GeV_dm1p33GeV_': 0, 'mChipm140GeV_dm0p48GeV_': 0, 'mChipm500GeV_dm3p33GeV_': 0, 'mChipm180GeV_dm0p79GeV_': 0, 'mChipm500GeV_dm0p23GeV_': 0, 'mChipm140GeV_dm0p58GeV_': 0, 'mChipm250GeV_dm0p31GeV_': 0, 'mChipm140GeV_dm3p28GeV_': 0, 'mChipm250GeV_dm1p81GeV_': 0, 'mChipm300GeV_dm0p61GeV_': 0, 'mChipm140GeV_dm0p43GeV_': 0, 'mChipm225GeV_dm0p2GeV_': 0, 'mChipm500GeV_dm0p83GeV_': 0, 'mChipm115GeV_dm2p27GeV_': 0, 'mChipm300GeV_dm4p31GeV_': 0, 'mChipm100GeV_dm1p76GeV_': 0, 'mChipm100GeV_dm3p26GeV_': 0, 'mChipm115GeV_dm1p27GeV_': 0, 'mChipm250GeV_dm0p51GeV_': 0, 'mChipm275GeV_dm0p412GeV_': 0, 'mChipm225GeV_dm3p3GeV_': 0, 'mChipm140GeV_dm0p98GeV_': 0, 'mChipm160GeV_dm4p29GeV_': 0, 'mChipm300GeV_dm3p31GeV_': 0, 'mChipm250GeV_dm3p31GeV_': 0, 'mChipm140GeV_dm0p28GeV_': 0, 'mChipm140GeV_dm0p38GeV_': 0, 'mChipm200GeV_dm3p3GeV_': 0, 'mChipm225GeV_dm0p6GeV_': 0, 'mChipm300GeV_dm1p81GeV_': 0, 'mChipm200GeV_dm1p8GeV_': 0, 'mChipm115GeV_dm0p47GeV_': 0, 'mChipm250GeV_dm1p01GeV_': 0, 'mChipm275GeV_dm0p212GeV_': 0, 'mChipm160GeV_dm0p99GeV_': 0, 'mChipm225GeV_dm1p8GeV_': 0, 'mChipm200GeV_dm0p2GeV_': 0, 'mChipm250GeV_dm0p46GeV_': 0, 'mChipm300GeV_dm2p31GeV_': 0, 'mChipm160GeV_dm0p59GeV_': 0, 'mChipm100GeV_dm5p26GeV_': 0, 'mChipm225GeV_dm0p3GeV_': 0, 'mChipm115GeV_dm0p97GeV_': 0, 'mChipm115GeV_dm1p77GeV_': 0, 'mChipm400GeV_dm0p324GeV_': 0, 'mChipm250GeV_dm0p21GeV_': 0, 'mChipm275GeV_dm0p512GeV_': 0, 'mChipm115GeV_dm0p37GeV_': 0, 'mChipm200GeV_dm0p8GeV_': 0, 'mChipm250GeV_dm0p41GeV_': 0, 'mChipm180GeV_dm0p99GeV_': 0, 'mChipm100GeV_dm1p26GeV_': 0, 'mChipm180GeV_dm3p29GeV_': 0, 'mChipm500GeV_dm5p33GeV_': 0, 'mChipm300GeV_dm0p51GeV_': 0, 'mChipm225GeV_dm1p0GeV_': 0}, '1t1l': {'mChipm160GeV_dm0p44GeV_': 0.00689757023462127, 'mChipm180GeV_dm5p29GeV_': 0.2837101250699646, 'mChipm200GeV_dm4p3GeV_': 0.21310144060427808, 'mChipm115GeV_dm0p42GeV_': 0.024554306591202706, 'mChipm500GeV_dm0p53GeV_': 0.0, 'mChipm115GeV_dm6p27GeV_': 0.610358958538046, 'mChipm140GeV_dm4p28GeV_': 0.5880484712140863, 'mChipm180GeV_dm0p44GeV_': 0.04973370834660533, 'mChipm200GeV_dm2p3GeV_': 0.162799422460962, 'mChipm400GeV_dm0p174GeV_': 0.0005336768787590724, 'mChipm300GeV_dm0p31GeV_': 0.0, 'mChipm115GeV_dm0p27GeV_': 0.0, 'mChipm500GeV_dm2p33GeV_': 0.0029452433331537365, 'mChipm250GeV_dm0p81GeV_': 0.0016680055927431505, 'mChipm115GeV_dm0p77GeV_': 0.3391636657443909, 'mChipm225GeV_dm0p8GeV_': 0.00126772470194455, 'mChipm180GeV_dm6p29GeV_': 0.2518175568964451, 'mChipm180GeV_dm0p59GeV_': 0.0, 'mChipm200GeV_dm0p3GeV_': 0.002125153632053275, 'mChipm500GeV_dm0p48GeV_': 0.0009737148788201116, 'mChipm160GeV_dm5p29GeV_': 0.3999095381718706, 'mChipm225GeV_dm2p3GeV_': 0.08175157463760614, 'mChipm100GeV_dm0p56GeV_': 0.055026624466963846, 'mChipm400GeV_dm0p424GeV_': 0.0009098416019210147, 'mChipm225GeV_dm0p5GeV_': 0.0, 'mChipm200GeV_dm0p4GeV_': 0.0, 'mChipm160GeV_dm3p29GeV_': 0.35495048236846305, 'mChipm200GeV_dm6p3GeV_': 0.7140755849536564, 'mChipm100GeV_dm0p46GeV_': 0.027888666159752867, 'mChipm140GeV_dm0p78GeV_': 0.04445395591428412, 'mChipm500GeV_dm1p03GeV_': 0.0006060033909069968, 'mChipm100GeV_dm0p96GeV_': 0.06970351865541863, 'mChipm500GeV_dm0p43GeV_': 0.0006300043816300224, 'mChipm250GeV_dm2p31GeV_': 0.0633367864035943, 'mChipm250GeV_dm0p61GeV_': 0.008892649217381213, 'mChipm200GeV_dm0p6GeV_': 0.0030635761869421177, 'mChipm300GeV_dm0p41GeV_': 0.0, 'mChipm100GeV_dm6p26GeV_': 1.4317321858786187, 'mChipm100GeV_dm0p36GeV_': 0.10103394693147388, 'mChipm180GeV_dm0p19GeV_': 0.015157961118278707, 'mChipm115GeV_dm3p27GeV_': 1.0142200482821984, 'mChipm160GeV_dm1p29GeV_': 0.1894590369225231, 'mChipm180GeV_dm0p39GeV_': 0.0032324413514466027, 'mChipm200GeV_dm5p3GeV_': 0.19249654066028407, 'mChipm100GeV_dm0p41GeV_': 0.1595761724129806, 'mChipm180GeV_dm4p29GeV_': 0.3481060072443589, 'mChipm200GeV_dm1p0GeV_': 0.020033248688189155, 'mChipm160GeV_dm0p29GeV_': 0.0, 'mChipm140GeV_dm2p28GeV_': 0.37717236914250946, 'mChipm225GeV_dm0p4GeV_': 0.0, 'mChipm100GeV_dm2p26GeV_': 1.2167551793742268, 'mChipm500GeV_dm4p33GeV_': 0.008454900693100429, 'mChipm180GeV_dm0p49GeV_': 0.0, 'mChipm200GeV_dm0p5GeV_': 0.04754653512072733, 'mChipm140GeV_dm1p78GeV_': 0.2918415789502378, 'mChipm300GeV_dm0p46GeV_': 0.0, 'mChipm300GeV_dm1p31GeV_': 0.004692227375344473, 'mChipm100GeV_dm4p26GeV_': 1.6495460195488063, 'mChipm160GeV_dm0p49GeV_': 0.0, 'mChipm160GeV_dm0p79GeV_': 0.0, 'mChipm140GeV_dm1p28GeV_': 0.12018200036858953, 'mChipm180GeV_dm1p79GeV_': 0.1228160803691891, 'mChipm160GeV_dm2p29GeV_': 0.3501282997932912, 'mChipm500GeV_dm0p63GeV_': 0.0007180772149953693, 'mChipm200GeV_dm0p45GeV_': 0.010876557167119862, 'mChipm100GeV_dm0p16GeV_': 0.2843975913620334, 'mChipm400GeV_dm0p224GeV_': 0.00023245178810405904, 'mChipm160GeV_dm1p79GeV_': 0.1899874946064316, 'mChipm200GeV_dm1p3GeV_': 0.04618254732663303, 'mChipm250GeV_dm4p31GeV_': 0.1160603406043768, 'mChipm160GeV_dm0p39GeV_': 0.0, 'mChipm100GeV_dm0p26GeV_': 0.0, 'mChipm300GeV_dm0p21GeV_': 0.007295490527942999, 'mChipm250GeV_dm5p31GeV_': 0.0967719332439017, 'mChipm500GeV_dm1p83GeV_': 0.0014869976443930707, 'mChipm180GeV_dm2p29GeV_': 0.20443686778205689, 'mChipm180GeV_dm1p29GeV_': 0.055952349229885456, 'mChipm300GeV_dm0p81GeV_': 0.0, 'mChipm140GeV_dm5p28GeV_': 0.6596841399933816, 'mChipm115GeV_dm0p17GeV_': 0.24499326278453798, 'mChipm140GeV_dm0p18GeV_': 0.0, 'mChipm160GeV_dm0p19GeV_': 0.0, 'mChipm250GeV_dm1p31GeV_': 0.015853232182233126, 'mChipm300GeV_dm1p01GeV_': 0.0041915689423126365, 'mChipm115GeV_dm0p57GeV_': 0.03722525022287641, 'mChipm225GeV_dm1p3GeV_': 0.0255843883720325, 'mChipm115GeV_dm5p27GeV_': 0.8024951654117263, 'mChipm100GeV_dm0p76GeV_': 0.05090245822367015, 'mChipm180GeV_dm0p29GeV_': 0.022736942520432502, 'mChipm115GeV_dm4p27GeV_': 0.9513375930353846, 'mChipm275GeV_dm0p312GeV_': 0.0, 'mChipm225GeV_dm0p45GeV_': 0.018272745793591467, 'mChipm500GeV_dm1p33GeV_': 0.0009574207088834994, 'mChipm140GeV_dm0p48GeV_': 0.0, 'mChipm500GeV_dm3p33GeV_': 0.006584109481913894, 'mChipm180GeV_dm0p79GeV_': 0.011937751653069456, 'mChipm500GeV_dm0p23GeV_': 0.003437623253865544, 'mChipm140GeV_dm0p58GeV_': 0.0, 'mChipm250GeV_dm0p31GeV_': 0.013248720171257077, 'mChipm140GeV_dm3p28GeV_': 0.6889671298609716, 'mChipm250GeV_dm1p81GeV_': 0.047989456450687876, 'mChipm300GeV_dm0p61GeV_': 0.0006985947814219381, 'mChipm140GeV_dm0p43GeV_': 0.0, 'mChipm225GeV_dm0p2GeV_': 0.0, 'mChipm500GeV_dm0p83GeV_': 0.00017603846417799167, 'mChipm115GeV_dm2p27GeV_': 0.7912670519126788, 'mChipm300GeV_dm4p31GeV_': 0.05604614685420679, 'mChipm100GeV_dm1p76GeV_': 0.892124083370378, 'mChipm100GeV_dm3p26GeV_': 1.4780178492596412, 'mChipm115GeV_dm1p27GeV_': 0.4245890550598446, 'mChipm250GeV_dm0p51GeV_': 0.006177013682524181, 'mChipm275GeV_dm0p412GeV_': 0.0, 'mChipm225GeV_dm3p3GeV_': 0.12581635826569101, 'mChipm140GeV_dm0p98GeV_': 0.04625133487556135, 'mChipm160GeV_dm4p29GeV_': 0.45568183971904785, 'mChipm300GeV_dm3p31GeV_': 0.04336339787981361, 'mChipm250GeV_dm3p31GeV_': 0.08782077427436072, 'mChipm140GeV_dm0p28GeV_': 0.0, 'mChipm140GeV_dm0p38GeV_': 0.008756618065151201, 'mChipm200GeV_dm3p3GeV_': 0.2497739909649137, 'mChipm225GeV_dm0p6GeV_': 0.001980616957871743, 'mChipm300GeV_dm1p81GeV_': 0.014640761178061342, 'mChipm200GeV_dm1p8GeV_': 0.07774894786469205, 'mChipm115GeV_dm0p47GeV_': 0.24096605922274159, 'mChipm250GeV_dm1p01GeV_': 0.0034448377443317157, 'mChipm275GeV_dm0p212GeV_': 0.0064236655326765195, 'mChipm160GeV_dm0p99GeV_': 0.09562270100666934, 'mChipm225GeV_dm1p8GeV_': 0.06189328571357645, 'mChipm200GeV_dm0p2GeV_': 0.010708103588948869, 'mChipm250GeV_dm0p46GeV_': 0.0, 'mChipm300GeV_dm2p31GeV_': 0.0394059971002393, 'mChipm160GeV_dm0p59GeV_': 0.02795619578109419, 'mChipm100GeV_dm5p26GeV_': 1.0384989223731345, 'mChipm225GeV_dm0p3GeV_': 0.0, 'mChipm115GeV_dm0p97GeV_': 0.23038821451912864, 'mChipm115GeV_dm1p77GeV_': 0.739966030349064, 'mChipm400GeV_dm0p324GeV_': 0.0008132286344158288, 'mChipm250GeV_dm0p21GeV_': 0.0, 'mChipm275GeV_dm0p512GeV_': 0.0006795995780545999, 'mChipm115GeV_dm0p37GeV_': 0.0, 'mChipm200GeV_dm0p8GeV_': 0.08767552989928645, 'mChipm250GeV_dm0p41GeV_': 0.006457787007036022, 'mChipm180GeV_dm0p99GeV_': 0.012685200276902895, 'mChipm100GeV_dm1p26GeV_': 0.32056337343048613, 'mChipm180GeV_dm3p29GeV_': 0.32567967521915997, 'mChipm500GeV_dm5p33GeV_': 0.009159146797849446, 'mChipm300GeV_dm0p51GeV_': 0.0, 'mChipm225GeV_dm1p0GeV_': 0.005959051266021664}}}
    #print("\n\n\n\n")
    #print(significance["1t1l"]["all"])
    
    print("==============")
    print("\n\n\n\n")
    print(significance)
    print(" ")
    print(" ")
    print(" ")
    if sam:
        for signalFileName in sorted(significance["1t1l"]["all"]):
            fileNameParts = signalFileName.split("_")
            mu = "mu" + fileNameParts[0].split("mChipm")[1].split("GeV")[0]
            dm = fileNameParts[1].split("GeV")[0]
            if significance["1t1l"]["all"].get(signalFileName) is None:
                significance["1t1l"]["all"][signalFileName] = 0
            if significance["1t1l"]["1t1l"].get(signalFileName) is None:
                significance["1t1l"]["1t1l"][signalFileName] = 0
            if significance["2l"]["all"].get(signalFileName) is None:
                significance["2l"]["all"][signalFileName] = 0
            if significance["2l"]["2l"].get(signalFileName) is None:
                significance["2l"]["2l"][signalFileName] = 0
            print(mu, dm, "{:.2f}".format(0.0), "{:.2f}".format(significance["1t1l"]["all"][signalFileName]), "{:.2f}".format(significance["1t1l"]["1t1l"][signalFileName]), "{:.2f}".format(0.0), "{:.2f}".format(significance["2l"]["all"][signalFileName]), "{:.2f}".format(significance["2l"]["2l"][signalFileName]), "{:.2f}".format(0.0), "{:.2f}".format(math.sqrt((significance["2l"]["all"][signalFileName])**2 + (significance["1t1l"]["all"][signalFileName])**2)), "{:.2f}".format(math.sqrt((significance["2l"]["2l"][signalFileName])**2 + (significance["1t1l"]["1t1l"][signalFileName])**2)))
    else:
        for trainGroup in significance["1t1l"]:
            if trainGroup in ["all", "1t1l","2l"]:
                continue
            for signalFileName in sorted(significance["1t1l"][trainGroup]):
                fileNameParts = signalFileName.split("_")
                mu = fileNameParts[1]
                dm = fileNameParts[2].split("Chi")[0]
                print(mu, dm, "{:.2f}".format(significance["1t1l"][trainGroup][signalFileName]), "{:.2f}".format(significance["1t1l"]["all"][signalFileName]), "{:.2f}".format(significance["1t1l"]["1t1l"][signalFileName]), "{:.2f}".format(significance["2l"][trainGroup][signalFileName]), "{:.2f}".format(significance["2l"]["all"][signalFileName]), "{:.2f}".format(significance["2l"]["2l"][signalFileName]), "{:.2f}".format(math.sqrt((significance["1t1l"][trainGroup][signalFileName])**2 + (significance["2l"][trainGroup][signalFileName])**2)), "{:.2f}".format(math.sqrt((significance["2l"]["all"][signalFileName])**2 + (significance["1t1l"]["all"][signalFileName])**2)), "{:.2f}".format(math.sqrt((significance["2l"]["2l"][signalFileName])**2 + (significance["1t1l"]["1t1l"][signalFileName])**2)))

    # c1 = TCanvas("c1", "c1", 800, 800)
#     c1.SetBottomMargin(0.16)
#     c1.SetLeftMargin(0.18)
#     c1.cd()
#     histPad = c1
#     histPad.Draw()
#     c1.Print("output.pdf[");
#     sigHist = signalHistograms["1t1l"]["low"]["higgsino_mu100_dm4p30Chi20Chipm"][10]
#     bgHist = bgHistograms["1t1l"]["low"][10]
#     utils.formatHist(bgHist, utils.signalCp[1], 0.8)
#     bgHist.Draw("hist")
#     sigHist.Draw("hist same")
#     c1.Print("output.pdf");
#     c1.Print("output.pdf]");
#     sig = utils.calcSignificance(sigHist, [bgHist])
#     print("sig=", sig)
    
#     trainGroups = {
#     "dm0" : ["dm0p"],
#     "dm1" : ["dm1p"],
#     "low" : ["dm2p", "dm3p", "dm4p"],
#     "dm7" : ["dm7p"],
#     "dm9" : ["dm9p"],
#     "high" : ["dm12p", "dm13p"]
# }
# 
# trainGroupsOrder = ["dm0", "dm1", "low", "dm7", "dm9", "high"]
    
    print("End: " + datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    exit(0)

main()



#!/usr/bin/env python

from ROOT import *
from glob import glob
from sys import exit
import numpy as np
import argparse
import sys
import os

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes"))
from lib import analysis_ntuples
from lib import analysis_tools
from lib import utils
from lib import analysis_observables

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Weight skims for x1x2x1 process.')
parser.add_argument('-i', '--input_file', nargs=1, help='Input Directory', required=True)
parser.add_argument('-wanted_phase', '--wanted_phase', nargs=1, help='Wanted Phase', required=False)

parser.add_argument('-f', '--force', dest='force', help='Force Update', action='store_true')
#parser.add_argument('-data', '--data', dest='data', help='data', action='store_true')
#parser.add_argument('-sam', '--sam', dest='sam', help='Sam Samples', action='store_true')
args = parser.parse_args()

input_file = args.input_file[0]
force = args.force
wanted_phase = "phase0"
if args.wanted_phase:
    wanted_phase = args.wanted_phase[0]

dilepBDTobs = "dilepBDTphase1"

#sam = args.sam
#data = args.data
######## END OF CMDLINE ARGUMENTS ########

#### 2006 version - with the thin bin next to the right wide one

#  FCN=9.07656 FROM MIGRAD    STATUS=CONVERGED      30 CALLS          31 TOTAL
#                      EDM=1.66947e-23    STRATEGY= 1      ERROR MATRIX ACCURATE 
#   EXT PARAMETER                                   STEP         FIRST   
#   NO.   NAME      VALUE            ERROR          SIZE      DERIVATIVE 
#    1  p0           9.00962e-01   6.66541e-02   1.02452e-04   0.00000e+00
#    2  p1          -3.06826e-01   1.47784e-01   2.27155e-04   3.91001e-11
# chi2perndof 1.8153120006731853

#### 2006 version - with even binning starting from 0.5 with 0.1 jumps

# yTitle Sim / CR numLabel Sim denLabel CR
#  FCN=6.72915 FROM MIGRAD    STATUS=CONVERGED      30 CALLS          31 TOTAL
#                      EDM=2.29455e-23    STRATEGY= 1      ERROR MATRIX ACCURATE 
#   EXT PARAMETER                                   STEP         FIRST   
#   NO.   NAME      VALUE            ERROR          SIZE      DERIVATIVE 
#    1  p0           9.31020e-01   6.98203e-02   9.20226e-05  -4.82587e-11
#    2  p1          -2.08527e-01   1.63332e-01   2.15270e-04   4.12588e-11
# chi2perndof 1.345829491830544


#### 2007 version - with the thin bin next to the right wide one

#  FCN=4.15105 FROM MIGRAD    STATUS=CONVERGED      30 CALLS          31 TOTAL
#                      EDM=2.33382e-24    STRATEGY= 1      ERROR MATRIX ACCURATE 
#   EXT PARAMETER                                   STEP         FIRST   
#   NO.   NAME      VALUE            ERROR          SIZE      DERIVATIVE 
#    1  p0           1.09097e+00   1.18257e-01   1.21539e-04   0.00000e+00
#    2  p1           1.06176e-01   2.67977e-01   2.75416e-04  -8.06215e-12
# chi2perndof 0.8302093486684967

#### 2007 version - with even binning starting from 0.5 with 0.1 jumps

# yTitle Sim / CR numLabel Sim denLabel CR
#  FCN=3.33211 FROM MIGRAD    STATUS=CONVERGED      30 CALLS          31 TOTAL
#                      EDM=8.42342e-24    STRATEGY= 1      ERROR MATRIX ACCURATE 
#   EXT PARAMETER                                   STEP         FIRST   
#   NO.   NAME      VALUE            ERROR          SIZE      DERIVATIVE 
#    1  p0           1.11780e+00   1.22230e-01   1.11955e-04   1.98334e-11
#    2  p1           1.95765e-01   2.88665e-01   2.64398e-04   8.39812e-12
# chi2perndof 0.6664220888271789


def funcBackground(x,par):
    return par[0]+par[1]*x[0]

# m = -0.307
# b = 0.901
# 
# m_s = 0.15
# b_s = 0.07


m = -0.208
m_s = 0.163

b = 0.931
b_s = 0.07

if wanted_phase == "phase1":
    print("Phase 1 wanted!")
    
    dilepBDTobs = "dilepBDT"
    
    m = 0.196
    m_s = 0.289
    
    b = 1.118
    b_s = 0.122

print("Line fit parameters m=", m, " b=", b)

# 0 = b, 1 = m

fLine = TF1('fLine', funcBackground, -1, 1, 2)
fLine.SetParameter(0, b)
fLine.SetParameter(1, m)

fLineSigmaM = TF1('fLineSigmaM', funcBackground, -1, 1, 2)
fLineSigmaM.SetParameter(0, b)
fLineSigmaM.SetParameter(1, m-m_s)

fLineSigmaB = TF1('fLineSigmaB', funcBackground, -1, 1, 2)
fLineSigmaB.SetParameter(0, b+b_s)
fLineSigmaB.SetParameter(1, m)

# print("fLine.Eval(0)", fLine.Eval(0))
# print("fLine.Eval(1)", fLine.Eval(1))
# print("fLine.Eval(2)", fLine.Eval(2))

newObservableStrs = ["muonsClosureLineFitWeight", "muonsClosureLineFitSigmaMWeight", "muonsClosureLineFitSigmaBWeight"]
wantedIso = "CorrJetNoMultIso10Dr0.6"

fileList = [input_file]

for filename in fileList:
    if os.path.isdir(filename): continue
    print("processing file " + filename)
    f = TFile(filename, "update")
    
    t = f.Get("tEvent")
    
    shouldSkipTree = False
    rewriteTree = False
    
    for iso in utils.leptonIsolationList:
        for cat in utils.leptonIsolationCategories:
            ptRanges = [""]
            drCuts = [""]
            if iso in ["CorrJetIso", "CorrJetNoMultIso"]:
                ptRanges = utils.leptonCorrJetIsoPtRange
                drCuts = utils.leptonCorrJetIsoDrCuts
            for ptRange in ptRanges:
                for drCut in drCuts:
                    cuts = ""
                    if len(str(ptRange)) > 0:
                        cuts = str(ptRange) + "Dr" + str(drCut)
                    if (iso + cuts + cat) != wantedIso:
                        continue
                    postfixi = [iso + cuts + cat]
                    if iso + cuts + cat == utils.defaultJetIsoSetting:
                        postfixi = [iso + cuts + cat, ""]
                    for postfix in postfixi:
                        obsStr = newObservableStrs[0] + postfix
                        if t.GetBranchStatus(obsStr):
                            if not force:
                                print("Tree", filename ,"already has", obsStr, "! Skipping...")
                                shouldSkipTree = True
                            else:
                                rewriteTree = True
                            break
    
          
    if shouldSkipTree:
        f.Close()
        continue

    nentries = t.GetEntries();
    
    obsMem = {}
    branches = {}
    
    print('Analysing', nentries, "entries")
    
    for ientry in range(nentries):
        if ientry % 1000 == 0:
            print("Processing " + str(ientry) + " out of " + str(nentries))
        t.GetEntry(ientry)
        
        for iso in utils.leptonIsolationList:
            for cat in utils.leptonIsolationCategories:
                ptRanges = [""]
                drCuts = [""]
                if iso in ["CorrJetIso", "CorrJetNoMultIso"]:
                    ptRanges = utils.leptonCorrJetIsoPtRange
                    drCuts = utils.leptonCorrJetIsoDrCuts
                for ptRange in ptRanges:
                    for drCut in drCuts:
                        cuts = ""
                        if len(str(ptRange)) > 0:
                            cuts = str(ptRange) + "Dr" + str(drCut)
                        postfixi = [iso + cuts + cat]
                        if (iso + cuts + cat) != wantedIso:
                            continue
                        if iso + cuts + cat == utils.defaultJetIsoSetting:
                            postfixi = [iso + cuts + cat, ""]
                        for postfix in postfixi:
                            
                            for newObservableStr in newObservableStrs:
                            
                                obsStr = newObservableStr + postfix
                            
                                if obsMem.get(obsStr) is None:
                                    obsMem[obsStr] = np.zeros(1,dtype=float)
            
                                    if t.GetBranchStatus(obsStr):
                                        print("Restting branch", obsStr)
                                        branch = t.GetBranch(obsStr)
                                        branch.Reset()
                                        branch.SetAddress(obsMem[obsStr])
                                        branches[obsStr] = branch
                                    else:
                                        branch = t.Branch(obsStr,obsMem[obsStr],obsStr+"/D");
                                        branches[obsStr] = branch

                                if getattr(t, "twoLeptons"  + postfix) == 1 and getattr(t, "leptons"  + postfix).size() == 2 and getattr(t, "leptonFlavour"  + postfix) == "Muons" and getattr(t, "isoCr"  + postfix) >= 1:
                                    #met = TLorentzVector()
                                    #met.SetPtEtaPhiE(t.MET,0,t.METPhi,t.MET)

                                    dilepBDT = getattr(t, dilepBDTobs  + postfix)
                                    if newObservableStr == "muonsClosureLineFitWeight":
                                        obsMem[obsStr][0] = fLine.Eval(dilepBDT)
                                    elif newObservableStr == "muonsClosureLineFitSigmaMWeight":
                                        #print("calculating for fLineSigmaM", dilepBDT, " by hand ", 1.114 + 0.383*dilepBDT, " eval ", fLineSigmaM.Eval(dilepBDT))
                                        obsMem[obsStr][0] = fLineSigmaM.Eval(dilepBDT)
                                    elif newObservableStr == "muonsClosureLineFitSigmaBWeight":
                                        obsMem[obsStr][0] = fLineSigmaB.Eval(dilepBDT)
                                else:
                                    obsMem[obsStr][0] = 1
                                    #print("NOT TWO LEPTONS", "twoLeptons"  + postfix, getattr(t, "twoLeptons"  + postfix), getattr(t, "leptons"  + postfix).size())
                                    #obsMem[obsStr][0] = -2
                                branches[obsStr].Fill()
   
    t.Write("tEvent",TObject.kOverwrite)
    print("Done")
    f.Close()


    

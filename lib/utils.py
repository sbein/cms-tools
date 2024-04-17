from ROOT import *
import sys
import numpy as np

#from lib import histograms
#from lib import cuts
import os, re
import json
import time
import array
import subprocess
import math
from glob import glob
import random
import string

gSystem.Load('LumiSectMap_C')
from ROOT import LumiSectMap

gStyle.SetOptStat(0)
TH1D.SetDefaultSumw2()

# gSystem.Load('LeptonCollectionMap_C')
# from ROOT import LeptonCollectionMap
# from ROOT import LeptonCollectionFilesMap
# from ROOT import LeptonCollection

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RED = '\033[31m'

crossSections = {
    "dm7"  : 1.21547,
    "dm13" : 1.21547,
    "dm20" : 1.21547
}

samCrossSections = {
    'mChipm100GeV' : 16.7972,
    'mChipm115GeV' : 10.6756,
    'mChipm140GeV' : 5.00942,
    'mChipm160GeV' : 2.99724,
    'mChipm180GeV' : 1.90530,
    'mChipm200GeV' : 1.33562,
    'mChipm225GeV' : 0.807605,
    'mChipm250GeV' : 0.577314,
    'mChipm275GeV' : 0.373229,
    'mChipm300GeV' : 0.284855,
    'mChipm400GeV' : 0.0887325,
    'mChipm500GeV' : 0.0338387,
    'mChipm600GeV' : 0.0146677,
    'mChipm700GeV' : 0.00689981,
    'mChipm800GeV' : 0.0048731,
    'mChipm900GeV' : 0.00346143,
    'mChipm1000GeV' : 0.000968853,
    'mChipm1100GeV' : 0.000731306    
}

dyCrossSections = {
    "DYJetsToLL_M-5to50_HT-70to100" : 301.2,
    "DYJetsToLL_M-5to50_HT-100to200" : 224.2,
    "DYJetsToLL_M-5to50_HT-200to400" : 37.2,
    "DYJetsToLL_M-5to50_HT-400to600" : 3.581,
    "DYJetsToLL_M-5to50_HT-600toInf": 1.124
}

# dyCrossSections = {
#     "DYJetsToLL_M-5to50_HT-70to100" : 301.0,
#     "DYJetsToLL_M-5to50_HT-100to200" : 224.4,
#     "DYJetsToLL_M-5to50_HT-200to400" : 37.87,
#     "DYJetsToLL_M-5to50_HT-400to600" : 3.628,
#     "DYJetsToLL_M-5to50_HT-600toInf": 1.107
# }

#LUMINOSITY = 35900. #pb^-1
LUMINOSITY = 135000.
#CMS_WD="/afs/desy.de/user/n/nissanuv/CMSSW_11_3_1/src"
CS_DIR="/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/cs/stdout"
LEPTON_COLLECTION_DIR="/pnfs/desy.de/cms/tier2/store/user/ynissan/NtupleHub/LeptonCollection"
LEPTON_COLLECTION_FILES_MAP_DIR="/pnfs/desy.de/cms/tier2/store/user/ynissan/NtupleHub/LeptonCollectionFilesMaps"

epsilon = 0.0000000001

TOOLS_BASE_PATH = os.path.expandvars("$CMSSW_BASE/src/cms-tools")#/analysis/scripts/condor_wrapper.sh")

compoundTypes = {
    "Rare" : ["WZZ", "WWZ", "ZZZ"],
    "DiBoson" : ["WZ", "WW", "ZZ", "WWTo1L1Nu2Q", "WZTo1L1Nu2Q", "WZTo1L3Nu", "ZZTo2L2Q"],
    "TTJets": ["ST_t-channel_antitop", "ST_t-channel_top", "TTJets_DiLept", "TTJets_SingleLeptFromT", "TTJets_SingleLeptFromTbar"]
}

trainGroups = {
    "dm1" : ["dm0p", "dm1p"],
    "low" : ["dm2p", "dm3p", "dm4p"],
    "dm7" : ["dm7p"],
    "dm9" : ["dm9p"],
    "high" : ["dm12p", "dm13p"]
}

trainGroupsOrder = ["dm1", "low", "dm7", "dm9", "high"]

#Normal
bgOrder = {
    "WZTo3LNu" : -1,
    "Rare" : 0,
    "DiBoson" : 1,
    "DYJetsToLL" : 2,
    "TTJets" : 3,
    "ZJetsToNuNu" : 4,
    "QCD" : 5,
    "WJetsToLNu" : 6,
    #"TT" : 7,
}

bgReTaggingNames = {
    "WZTo3LNu" : "WZTo3LNu",
    "Rare" : "Rare",
    "DiBoson" : "VV",
    "DYJetsToLL" : "DY+jets",
    "TTJets" : "t#bar{t}",
    "ZJetsToNuNu" : "Z+jets#rightarrow#nu#nu",
    "QCD" : "QCD multijet",
    "WJetsToLNu" : "W+jets#rightarrow_{}l#nu",
    #"TT" : 7,
}

#Z Jets
# bgOrder = {
#     "Rare" : 0,
#     "DiBoson" : 5,
#     "ZJetsToNuNu" : 1,
#     "DYJetsToLL" : 6,
#     "TTJets" : 4,
#     "WJetsToLNu" : 3,
#     "QCD" : 2,
# }

tracksVars = (
        {"name":"dxyVtx", "type":"double"},
        {"name":"dzVtx", "type":"double"},
        {"name":"chi2perNdof", "type":"double"},
        {"name":"trkMiniRelIso", "type":"double"},
        {"name":"trkRelIso", "type":"double"},
        {"name":"charge", "type":"int"},
        {"name":"trackJetIso", "type":"double"},
        {"name":"trackQualityHighPurity", "type":"bool"},
        #{"name":"trackLeptonIso", "type":"double"}
)


leptonsCorrJetVecList = {
    #"CorrJetIso" : "bool",
    #"CorrJetD3Iso" : "bool",
    #"NonJetIso" : "bool",
    
    
    "CorrJetNoMultIso" : "bool",
    "CorrJetNoMultD3Iso" : "bool",
    
    #"JetIso" : "bool",
    #"JetD3Iso" : "bool",
    
    "NoIso" : "bool",
}

#Original list - for full scan
#leptonCorrJetIsoPtRange = [0, 1, 5, 6, 7, 8, 9, 10, 10.5, 11, 11.5, 12, 12.5, 13, 15, 20]
#leptonCorrJetIsoDrCuts = [0.4,0.45,0.5,0.55,0.6]

leptonCorrJetIsoPtRange = [10]
leptonCorrJetIsoDrCuts = [0.5,0.6]
defaultJetIsoSetting = "NoIso"

#leptonIsolationList = [ "JetIso", "CorrJetIso", "NonJetIso" ]
#leptonIsolationList = [ "CorrJetIso", "NonJetIso", "NoIso" ]
#Old list
#leptonIsolationList = [ "CorrJetIso", "NoIso" ]
#New List
#leptonIsolationList = [ "NoIso", "CorrJetIso", "CorrJetNoMultIso", "JetIso" ]
#leptonIsolationCrList = [ "CorrJetD3Iso", "CorrJetNoMultD3Iso","JetD3Iso" ]


#Finalising
leptonIsolationList = [ "NoIso", "CorrJetNoMultIso" ]
leptonIsolationCrList = [ "CorrJetNoMultD3Iso" ]


leptonIsolationIncList = leptonIsolationList + leptonIsolationCrList
# leptonIsolationCategories = {
#     "" : { "lowPtTightMuons" : False, "muonPt" : 2},
#     "LowPt" : { "lowPtTightMuons" : False, "muonPt" : 1.5},
#     "LowPtTight" : { "lowPtTightMuons" : True, "muonPt" : 1.5}
# }

leptonIsolationCategories = {
    "" : { "lowPtTightMuons" : False, "muonPt" : 2},
    #"LowPt" : { "lowPtTightMuons" : False, "muonPt" : 1.5},
    #"LowPtTight" : { "lowPtTightMuons" : True, "muonPt" : 1.5}
}

typeTranslation = {
    "float" : "D",
    "bool" : "O",
    "int" : "I",
    "double" : "D"
}

# tl = TLatex()
# tl.SetNDC()
# cmsTextFont = 61
# extraTextFont = 52
# lumiTextSize = 0.6
# lumiTextOffset = 0.2
# cmsTextSize = 0.75
# cmsTextOffset = 0.1
# regularfont = 42
# originalfont = tl.GetTextFont()

class UOFlowTH1F(TH1F):
    epsilon = 0.0000000001
    def Fill(self, x, weight=1):
        #print "Called UOFlowTH1F Fill"
        super(UOFlowTH1F, self).Fill(min(max(x,self.GetXaxis().GetBinLowEdge(1)+self.epsilon),self.GetXaxis().GetBinLowEdge(self.GetXaxis().GetNbins()+1)-self.epsilon),weight)

class UOFlowTH2F(TH1F):
    epsilon = 0.0000000001
    def Fill(self, x, y, weight=1):
        #print "Called UOFlowTH1F Fill"
        super(UOFlowTH2F, self).Fill(min(max(x,h.GetXaxis().GetBinLowEdge(1)+epsilon),h.GetXaxis().GetBinLowEdge(h.GetXaxis().GetNbins()+1)-epsilon), min(max(y,h.GetYaxis().GetBinLowEdge(1)+epsilon),h.GetYaxis().GetBinLowEdge(h.GetYaxis().GetNbins()+1)-epsilon),weight)

def isCoumpoundType(key):
    #print "Looking for:" + key + "|:
    if key in compoundTypes:
        return True
    return False

def existsInCoumpoundType(key):
    #print "Looking for:" + key + "|:
    for cType in compoundTypes:
        if key in compoundTypes[cType]:
            return True
    return False

def getFilesForCompoundType(cType, directory):
    print("In getFilesForCompoundType", cType, directory)
    bgFiles = []
    #print compoundTypes[cType]
    for miniType in compoundTypes[cType]:
        #if miniType not in sumTypes:
        #    print "skipping", miniType, "because not in", sumTypes
        #    continue
        #print "globbing", miniType
        #if "ST_" in miniType:
            #print "In ST***"
            #print "Globing " + directory + "/" + miniType + ".root"
        #    bgFiles.extend(glob(directory + "/" + miniType + ".root"))
        #else:
            #print "Globing " + directory + "/" + miniType + "_*.root"
        #This line is to solve the ST problem that sometimes it comes without an underscore
        bgFiles.extend(glob(directory + "/" + miniType + ".root"))
        bgFiles.extend(glob(directory + "/" + miniType + "_*.root"))
    #print(bgFiles)
    return bgFiles


def createHistograms(definitions, cutsDef) :
    histograms = {}
    for name, definition in list(definitions.items()):
        for cut, cutDef in list(cutsDef.items()):
            histName = name
            if cut != "none":
                if name == "HT":
                    continue
                histName += "_" + cut
            defTitle = (cutDef["histDef"].get(name) and cutDef["histDef"].get(name).get("title")) or definition["title"]
            defBins = (cutDef["histDef"].get(name) and cutDef["histDef"].get(name).get("bins")) or definition["bins"]
            defMinX = (cutDef["histDef"].get(name) and cutDef["histDef"].get(name).get("minX")) or definition.get("minX")
            defMaxX = (cutDef["histDef"].get(name) and cutDef["histDef"].get(name).get("maxX")) or definition.get("maxX")
            defBinArr = (cutDef["histDef"].get(name) and cutDef["histDef"].get(name).get("binsArr")) or definition.get("binsArr")
            if defBinArr is not None:
                histograms[histName] = TH1F(histName, defTitle, defBins, array.array('d', defBinArr))
            else:
                histograms[histName] = TH1F(histName, defTitle, defBins, defMinX, defMaxX)
            histograms[histName].Sumw2()
    return histograms

def scaleHistograms(histograms, histDefs, weight):
    for name, hist in list(histograms.items()):
        if name in histDefs and "noScale" in histDefs[name] and histDefs[name]["noScale"] :
            print("Not scaling " + name + " ... Skipping.")
            continue
        histograms[name].Scale(weight)

def writeHistograms(histList):
    for name, hist in list(histList.items()):
        histList[name].Write()
    
def printNullHistograms(histList):
    for name, hist in list(histList.items()):
        if histList[name].GetMaximum() == 0:
            print("Null Historgram " + name)

def getSortedKeysFromRootFile(rootFile):
    hashKeys = rootFile.GetListOfKeys()
    keys = []
    for hashKey in hashKeys:
        keys.append(hashKey.GetName())
    keys.sort()
    return keys

def getSortedCutsFromRootFile(rootFile):
    hashKeys = rootFile.GetListOfKeys()
    cutsOrderMap = cuts.getCutsOrderMap(histograms.cutsOrder)
    cutsOrder = []
    for i, cut in enumerate(histograms.cutsOrder):
        cutsOrder.append({ "name" : cut, "hists" : []})
    print(cutsOrder)
    for hashKey in hashKeys:
        histName = hashKey.GetName()
        splitName = histName.split("_")
        cutName = "none"
        histName = splitName[0]
        if len(splitName) > 1:
            cutName = "_".join(splitName[1:])
        cutsOrder[cutsOrderMap[cutName]].get("hists").append(histName)
    
    
    for i, cut in enumerate(cutsOrder):
        cut.get("hists").sort()
    return cutsOrder
    
def pause(str_='push enter key when ready'):
    import sys
    print(str_)
    sys.stdout.flush() 
    a = input('')


def fillth1(h,x, weight=1):
    h.Fill(min(max(x,h.GetXaxis().GetBinLowEdge(1)+epsilon),h.GetXaxis().GetBinLowEdge(h.GetXaxis().GetNbins()+1)-epsilon),weight)
 
def fillHistWithCuts(key, value, hists, cutsDef, type, event, weight=1, eventParams={}):
    #print "Filling key=" + key
    for cutName in cutsDef:
        if cutName == "none":
            hists[key].Fill(value, weight)
            #print "Fill " + key + " weight=" + str(weight)
            continue
        cut = cutsDef[cutName]
        if cuts.applyCut(cut, event, eventParams, type, cutName):
            #print "Fill " + key + "_" + cutName + " weight=" + str(weight)
            hists[key + "_" + cutName].Fill(value, weight)#new filling with over/under flow!
        #else:
        #	print "Not filling " + key + "_" + cutName

def getBgOrder(file):
    basename = os.path.basename(file).split(".")[0]
    if basename in bgOrder:
        return bgOrder[basename]
    else:
        return -1

def orderBgFiles(files):
    return sorted(files, key=getBgOrder)

def addMemToTreeVarsDef(treeVarsDef):
    for v in treeVarsDef:
        if v.get("type2") is not None:
            v["var"] = eval(v["type2"] + "()")
        else:
            if v["type"] == "D":
                v["var"] = np.zeros(1,dtype=np.dtype(np.float64))
            elif v["type"] == "I":
                v["var"] = np.zeros(1,dtype=int)
            elif v["type"] == "I":
                v["var"] = np.zeros(1,dtype=bool)

def barchTreeFromVarsDef(tree, treeVarsDef):
    for v in treeVarsDef:
        if v.get("type2") is not None:
            tree.Branch(v["name"], v["type2"], v["var"])
        else:
            tree.Branch(v["name"], v["var"], v["name"] + "/" + v["type"])

def get_histogram_from_tree(tree, var, cutstring="", drawoptions="", nBinsX=False, xmin=False, xmax=False, nBinsY=False, ymin=False, ymax=False, numevents=-1, add_overflow = False):

    hName = str(uuid.uuid1()).replace("-", "")

    canvas = TCanvas("c_" + hName)

    if not nBinsY:
        histo = TH1F(hName, hName, nBinsX, xmin, xmax)
    else:
        histo = TH2F(hName, hName, nBinsX, xmin, xmax, nBinsY, ymin, ymax)

    if numevents>0:
        tree.Draw("%s>>%s" % (var, hName), cutstring, drawoptions, numevents)
    else:
        tree.Draw("%s>>%s" % (var, hName), cutstring, drawoptions)

    # add overflow bin(s) for 1D and 2D histograms:
    if add_overflow:
        if not nBinsY:
            bin = histo.GetNbinsX()+1
            overflow = histo.GetBinContent(bin)
            histo.AddBinContent((bin-1), overflow)
        else:
            binX = histo.GetNbinsX()+1
            binY = histo.GetNbinsX()+1
        
            # read and set overflow x values:
            for x in range(0, binX-1):
                overflow_up = histo.GetBinContent(x, binY)
                bin = histo.GetBin(x, binY-1)
                histo.SetBinContent(bin, overflow_up)
        
            # read and set overflow y values:
            for y in range(0, binY-1):
                overflow_right = histo.GetBinContent(binX, y)
                bin = histo.GetBin(binX-1, y)
                histo.SetBinContent(bin, overflow_right)
        
            # read and set overflow diagonal values:
            overflow_diag = histo.GetBinContent(binX, binY)
            bin = histo.GetBin(binX-1, binY-1)
            histo.SetBinContent(bin, overflow_diag)
   
    histo.SetDirectory(0)
    return histo

def getCrossSection(filename):
    cs = 0
    p = re.compile("^NLO\+NLL.*")
    for m in ("","-"):
        f = CS_DIR + "/" + filename + m + ".output"
        print("Checking ", f)
        fh = open(f, "r")
        for line in fh.readlines():
                if p.match(line):
                        print(line)
                        crossSection = float(line.split("(")[1].split(" ")[0])
                        print("CrossSection: ", crossSection)
                        fh.close()
                        cs += crossSection
                        break
                fh.close()
    print("Summed cs:", cs)
    if cs > 0:
        return cs
    return None

def insertToPythonLumiSection(lumiSecs, RunNum, LumiBlockNum):
    if lumiSecs.get(RunNum) is None:
        lumiSecs[RunNum] = []
    if LumiBlockNum not in lumiSecs[RunNum]:
        lumiSecs[RunNum].append(LumiBlockNum)

def deleteFromPythonLumiSection(lumiSecs, RunNum, LumiBlockNum):
    if lumiSecs.get(RunNum) is not None:
        lumiSecs[RunNum].remove(LumiBlockNum)
        if len(lumiSecs[RunNum]) == 0:
            del lumiSecs[RunNum]

def subtractPythonLumiSections(toSubtractLumiSecs, fromLumiSecs):
    for k, v in fromLumiSecs.items():
        for a in v:
            deleteFromPythonLumiSection(toSubtractLumiSecs, k, a)

def existsInPythonLumiSection(lumiSecs, RunNum, LumiBlockNum):
    return lumiSecs.get(RunNum) is not None and LumiBlockNum in lumiSecs[RunNum]

def pythonLumiSectionToObject(pythonLumiSecs, objectLumiSecs):
    for k, v in pythonLumiSecs.items():
        for a in v:
            objectLumiSecs.insert(k, a)

def printPythonLumiSection(lumiSecs):
    print("-----")
    for k, v in lumiSecs.items():
        print(str(k) + ":", ",".join([str(a) for a in v]))

def printLumiSection(lumiSecs):
    lumiMap = lumiSecs.getMap()
    print("-----")
    for k, v in lumiMap:
        print(str(k) + ":", ",".join([str(a) for a in v]))

def getJsonLumiSection(lumiSecs):
    lumiSecsDict = {}
    lumiMap = lumiSecs.getMap()
    for k, v in lumiMap:
        lumiSecsDict[k] = []
        lumis = []
        for a in v: 
            lumis.append(a)
        lumis.sort()
        #print "Before:"
        #print lumis
        for lumisec in lumis:
            if len(lumiSecsDict[k]) > 0 and lumisec == lumiSecsDict[k][-1][-1]+1:
                lumiSecsDict[k][-1][-1] = lumisec
            else:
                lumiSecsDict[k].append([lumisec, lumisec])
        #print "After:"
        #print lumiSecsDict[k]
    #print "End:"
    return json.dumps(lumiSecsDict)

def get_lumi_from_bril(json_file_name, cern_username, retry=False):
    #status, out = commands.getstatusoutput('ps axu | grep "itrac5117-v.cern.ch:1012" | grep -v grep')
    import subprocess
    subprocess.getstatusoutput('ls')
    status, out = subprocess.getstatusoutput('ps axu | grep "itrac5413-v.cern.ch:10121" | grep -v grep')
    
    if status != 0:
        print("Opening SSH tunnel for brilcalc...")
        os.system("ssh -f -N -L 10121:itrac5413-v.cern.ch:10121 %s@lxplus.cern.ch" % cern_username)
    else:
        print("Existing tunnel for brilcalc found")
    print("Getting lumi for %s..." % json_file_name)
    status, out = subprocess.getstatusoutput("eval `scram unsetenv -sh`; export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda/bin:$PATH; brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -u /fb -c offsite -i %s > %s.briloutput; grep '|' %s.briloutput | tail -n1" % (json_file_name, json_file_name, json_file_name))
    if status != 0:
        if not retry:
            print("Trying to re-establish the tunnel...")
            os.system("pkill -f itrac5413")
            get_lumi_from_bril(json_file_name, cern_username, retry=True)
        else:
            print("Error while running brilcalc!")
            if cern_username == "ynissan":
                print("Did you set your CERN username with '--cern_username'?")
        lumi = -1
    else:
        print("Output: " + out)
        lumi = float(out.split("|")[-2])
    
    print("lumi:", lumi)
    return lumi

def calculateLumiFromLumiSecs(lumiSecs):
    json = getJsonLumiSection(lumiSecs)
    #print "Json:"
    #print json
    timestamp = int(time.time())
    tmpJsonFile = "/tmp/tmp_json_" + str(timestamp) + ".json"
    with open(tmpJsonFile, "w") as fo:
        fo.write(json)
    print("Created json file: " + tmpJsonFile)
    lumi = get_lumi_from_bril(tmpJsonFile, 'ynissan')
    #lumi = "" 
    #os.remove(tmpJsonFile)
    return lumi
    
def getStackSum(hist):
    hists = hist.GetHists()
    newHist = hists[0].Clone()
    newHist.Sumw2()
    for i in range(1, len(hists)):
        newHist.Add(hists[i])
    return newHist

def mkhistlogx(name, title, nbins, xmin, xmax):
    logxmin = TMath.Log10(xmin)
    logxmax = TMath.Log10(xmax)
    
    binwidth = (logxmax-logxmin)/nbins
    #print "logxmin", logxmin, "logxmax", logxmax, "binwidth", binwidth
    xbins = array.array('d',[0]*(nbins+1))##might need to be defined out as 0's
    #xbins[0] = TMath.Power(10,logxmin)#xmin
    for i in range(0,nbins+1):
        binval = xmin + TMath.Power(10,logxmin+i*binwidth)
        #print "bin", i, "val", binval
        xbins[i] = xmin + TMath.Power(10,logxmin+i*binwidth)    
    #print 'xbins', xbins        
    h = TH1F(name,title,nbins,xbins);
    h.Sumw2()
    return h

def getRealLogxHistogramFromTree(name, tree, obs, bins, minX, maxX, condition, overflow=True):
    h = mkhistlogx(name + "_logx", "", bins, minX, maxX)
    h.Sumw2()
    return getHistogramFromTree(name, tree, obs, bins, minX, maxX, condition, overflow, name + "_logx", True)

def getHistogramFromTreeCustomBinsX(name, tree, obs, customBinsX, condition, overflow=True):
    xbins = array.array('d',[0]*(len(customBinsX)))
    for i in range(len(customBinsX)):
        xbins[i] = customBinsX[i]
    h = TH1F(name+"_customx","",len(customBinsX)-1, xbins)
    h.Sumw2()
    return getHistogramFromTree(name, tree, obs, None, None, None, condition, overflow, name + "_customx", True)
    
def foldOverflowBins(hist):
    over = hist.GetBinContent(hist.GetXaxis().GetNbins() + 1)
    if over:
        hist.Fill(hist.GetXaxis().GetBinCenter(hist.GetXaxis().GetNbins()), over)
    under = hist.GetBinContent(0)
    #print("under", under)
    if under:
        hist.Fill(hist.GetXaxis().GetBinCenter(1), under)

def getOverflowBinsRange(hist):
    maxRange = hist.GetXaxis().GetNbins()
    shouldChange = False
    over = hist.GetBinContent(hist.GetXaxis().GetNbins() + 1)
    print("overflow", over, hist.GetName())

    if over:
        maxRange = hist.GetXaxis().GetNbins() + 1
        shouldChange = True
        
    under = hist.GetBinContent(0)
    minRange = 1
    if under:
        minRange = 0
        shouldChange = True
    return shouldChange, minRange, maxRange

def setOverflowBins(hist):

    shouldChange, minRange, maxRange = getOverflowBinsRange(hist)

    if shouldChange:
        print("setting range", minRange, maxRange)
        hist.GetXaxis().SetRange(minRange, maxRange)

def setOverflowBinsStack(stack):
    if stack is None or stack.GetNhists() == 0:
        return 
   
    hists = stack.GetHists()
    
    shouldChange, minRange, maxRange = False, 1, 0
    
    for i, hist in enumerate(hists):
        shouldChangeH, minRangeH, maxRangeH = getOverflowBinsRange(hist)
        if shouldChangeH:
            shouldChange = True
            if minRangeH < minRange:
                minRange = minRangeH
            if maxRangeH > maxRange:
                maxRange = maxRangeH
    if shouldChange:
        for i, hist in enumerate(hists):
            print("here setting overflow", minRange, maxRange)
            hist.GetXaxis().SetRange(minRange, maxRange)
        stack.GetXaxis().SetRange(minRange, maxRange)

def getHistogramFromTree(name, tree, obs, bins, minX, maxX, condition, overflow=True, tmpName="hsqrt", predefBins = False, twoD = False, binsY = None, minBinsY = None, maxBinsY = None):
    if tree.GetEntries() == 0:
        return None
    binsStr = None
    
    print("Getting", name, "obs:", obs, "cond:", condition, "bins", bins, "minX", minX, "maxX", maxX, "overflow", overflow)
    
    # if tmpName == "hsqrt":
#         letters = string.ascii_lowercase
#         result_str = ''.join(random.choice(letters) for i in range(6))
#         tmpName += result_str
#         print "new tmp name is", tmpName
    if predefBins:
        binsStr = ">>" + tmpName
        tree.Draw(obs + binsStr, condition, "e")
    else:
        if bins is not None:
            binsStr = ">>" + tmpName + "(" + str(bins) + ","
            #print """tree.Draw(""" + obs + binsStr + str(minX) + "," + str(maxX) + ")", condition+""")"""
            if twoD:
                print("tree.Draw(" + obs + binsStr + str(minX) + "," + str(maxX) + "," + str(binsY) + "," + str(minBinsY) + "," + str(maxBinsY) +"))")
                tree.Draw(obs + binsStr + str(minX) + "," + str(maxX) + "," + str(binsY) + "," + str(minBinsY) + "," + str(maxBinsY) +")", condition, "e")
            else:
                tree.Draw(obs + binsStr + str(minX) + "," + str(maxX) + ")", condition, "e")
            #print obs + binsStr + str(minX) + "," + str(maxX) + ")"
            #print condition
        else:
            tree.Draw(obs + ">>" + tmpName, condition, "e")
    hist = tree.GetHistogram().Clone(name)
    hist.Sumw2()
    hist.SetDirectory(0)
    #if overflow:
    #    foldOverflowBins(hist)
    return hist



def madHtCheck(current_file_name, madHT):
    if (madHT>0) and \
       ("DYJetsToLL_M-50_Tune" in current_file_name and madHT>100) or \
       ("WJetsToLNu_TuneCUETP8M1_13TeV" in current_file_name and madHT>200) or \
       ("HT-100to200_" in current_file_name and (madHT<100 or madHT>200)) or \
       ("HT-200to300_" in current_file_name and (madHT<200 or madHT>300)) or \
       ("HT-200to400_" in current_file_name and (madHT<200 or madHT>400)) or \
       ("HT-300to500_" in current_file_name and (madHT<300 or madHT>500)) or \
       ("HT-400to600_" in current_file_name and (madHT<400 or madHT>600)) or \
       ("HT-600to800_" in current_file_name and (madHT<600 or madHT>800)) or \
       ("HT-800to1200_" in current_file_name and (madHT<800 or madHT>1200)) or \
       ("HT-1200to2500_" in current_file_name and (madHT<1200 or madHT>2500)) or \
       ("HT-2500toInf_" in current_file_name and madHT<2500) or \
       ("HT-500to700_" in current_file_name and (madHT<500 or madHT>700)) or \
       ("HT-700to1000_" in current_file_name and (madHT<700 or madHT>1000)) or \
       ("HT-1000to1500_" in current_file_name and (madHT<1000 or madHT>1500)) or \
       ("HT-1500to2000_" in current_file_name and (madHT<1500 or madHT>2000)) or \
       ("HT-600toInf_" in current_file_name and (madHT<600)) or \
       ("HT-70to100_" in current_file_name and (madHT<70 or madHT>100)) or \
       ("HT-100To200_" in current_file_name and (madHT<100 or madHT>200)) or \
       ("HT-200To300_" in current_file_name and (madHT<200 or madHT>300)) or \
       ("HT-200To400_" in current_file_name and (madHT<200 or madHT>400)) or \
       ("HT-300To500_" in current_file_name and (madHT<300 or madHT>500)) or \
       ("HT-400To600_" in current_file_name and (madHT<400 or madHT>600)) or \
       ("HT-500To700_" in current_file_name and (madHT<500 or madHT>700)) or \
       ("HT-600To800_" in current_file_name and (madHT<600 or madHT>800)) or \
       ("HT-700To1000_" in current_file_name and (madHT<700 or madHT>1000)) or \
       ("HT-800To1200_" in current_file_name and (madHT<800 or madHT>1200)) or \
       ("HT-1000To1500_" in current_file_name and (madHT<1000 or madHT>1500)) or \
       ("HT-1200To2500_" in current_file_name and (madHT<1200 or madHT>2500)) or \
       ("HT-1500To2000_" in current_file_name and (madHT<1500 or madHT>2000)) or \
       ("HT-2500ToInf_" in current_file_name and madHT<2500):
        #print "MADHT FALSE"
        return False
    else:
        return True

    #elif "Run2018D" in baseFileName and ".MET" in baseFileName:
    #    mapNameFile = "Run2018D_MET.root"

def getLeptonCollectionFileMapFile(baseFileName):
    currLeptonCollectionFileMapFile, currLeptonCollectionFileMap = None, None
    mapNameFile = ""
    if "Run2016" in baseFileName and ".MET" in baseFileName:
        mapNameFile = "Run2016_MET.root"
    elif "Run2016" in baseFileName and ".SingleMuon" in baseFileName:
        mapNameFile = "Run2016_SingleMuon.root"
    elif "Run2016" in baseFileName and "SingleElectron" in baseFileName:
        mapNameFile = "Run2016_SingleElectron.root"
    elif "Run2017" in baseFileName and ".MET" in baseFileName:
        mapNameFile = "Run2017_MET.root"
    elif "Run2018" in baseFileName and ".MET" in baseFileName:
        mapNameFile = "Run2018_MET.root"
    elif "RunIIFall17MiniAODv2" in baseFileName:
        mapNameFile = "Fall17." + ("_".join(baseFileName.split(".")[1].split("_")[0:3])).split("AOD")[0] + ".root"
    else:
        mapNameFile = ("_".join(baseFileName.split(".")[1].split("_")[0:3])).split("AOD")[0] + ".root"

    print(mapNameFile)
    if not os.path.isfile(LEPTON_COLLECTION_FILES_MAP_DIR + "/" + mapNameFile):
        print("File " + LEPTON_COLLECTION_FILES_MAP_DIR + "/" + mapNameFile + " does not exist.")
        return None
    print("Opening file map: " + LEPTON_COLLECTION_FILES_MAP_DIR + "/" + mapNameFile)
    currLeptonCollectionFileMapFile = TFile(LEPTON_COLLECTION_FILES_MAP_DIR + "/" + mapNameFile, "read")
    print("After open")
    if currLeptonCollectionFileMapFile is None:
        return None
    
    return currLeptonCollectionFileMapFile
    
def getLeptonCollectionFileMap(currLeptonCollectionFileMapFile, runNum, lumiBlockNum, evtNum):
    #import gc
    currLeptonCollectionFileMap = None
    keys = currLeptonCollectionFileMapFile.GetListOfKeys()
    print("Looping over keys")
    print([key.GetName() for key in keys])
    for key in keys:
        print(key.GetName())
        currLeptonCollectionFileMap = currLeptonCollectionFileMapFile.Get(key.GetName())
        if not currLeptonCollectionFileMap.contains(runNum, lumiBlockNum, evtNum):
            currLeptonCollectionFileMap.IsA().Destructor(currLeptonCollectionFileMap)
            #currLeptonCollectionFileMap.Delete()
            currLeptonCollectionFileMap = None
            #gc.collect()
            continue
        print("Found the correct file map!")
        return currLeptonCollectionFileMap
    print("Could not find file map for ", runNum, lumiBlockNum, evtNum)
    return None 
    
def getLeptonCollection(currLeptonCollectionFileName):
    print("Opening file map: " + LEPTON_COLLECTION_DIR + "/" + currLeptonCollectionFileName)
    currLeptonCollectionFile = TFile(LEPTON_COLLECTION_DIR + "/" + currLeptonCollectionFileName, "read")
    print("After open")
    leptonCollectionMap = currLeptonCollectionFile.Get("leptonCollectionMap")
    currLeptonCollectionFile.Close()
    return leptonCollectionMap

def getDmFromFileName(filename):
    print("Filename: " + filename)
    return filename.split('_')[-1].split('Chi20Chipm')[0]

def getPointFromFileName(filename):
    print("Filename: " + filename)
    return os.path.basename(filename).split('Chi20Chipm')[0].split('higgsino_')[1]


def getPointFromSamFileName(filename):
    print("Filename: " + filename)
    return "_".join(os.path.basename(filename).split('.')[0].split('_')[0:2])

def calcSignificance(sigHist, bgHist, ignoreCrossSection = False):
    sig = 0
    sigNum = 0
    bgNum = 0
    accumulate = False
    binsNumber = sigHist.GetNbinsX()
    cs = 1
    if not ignoreCrossSection:
        cs = 0.1
    #print "binsNumber=", binsNumber
    for bin in range(1, binsNumber + 1):
        if accumulate:
            sigNum += sigHist.GetBinContent(bin)
            bgNum += bgHist.GetBinContent(bin)
        else:
            sigNum = sigHist.GetBinContent(bin)
            bgNum = bgHist.GetBinContent(bin)
        if bgNum == 0:
            accumulate = True
        else:
            accumulate = False
            if bin <= binsNumber and bgHist.Integral(bin+1, binsNumber) == 0:
                sigNum += sigHist.Integral(bin, binsNumber)
                bgErr = 0.2 * bgNum
                sig = math.sqrt(sig**2 + (cs * (sigNum / math.sqrt(bgNum + bgErr**2)))**2)
                #print "**sigNum=", sigNum, "bgNum=", bgNum, "sig=", sig
                break
            else:
                #print "sigNum=", sigNum, "bgNum=", bgNum, "sig=", 0.1 * (sigNum / math.sqrt(bgNum))
                bgErr = 0.2 * bgNum
                sig = math.sqrt(sig**2 + (cs * (sigNum / math.sqrt(bgNum + bgErr**2)))**2)
    return sig

def calcSignificanceCutCount(sigHist, bgHist, binNum, binMax = -1):    
    binsNumber = sigHist.GetNbinsX()
    print("integrating from", binNum, "to", binsNumber if binMax == -1 else binMax)
    sigNum = sigHist.Integral(binNum, binsNumber if binMax == -1 else binMax)
    bgNum = bgHist.Integral(binNum, binsNumber if binMax == -1 else binMax)
    if bgNum == 0:
        return 0
    bgErr = 0.2 * bgNum
    print("sigNum", sigNum, "bgNum", bgNum)
    return sigNum / math.sqrt(bgNum + bgErr**2)
    # This is the version for a transfer factor of 0.8
    #return sigNum / math.sqrt(1.8*bgNum)


def calcSignificanceNoAcc(sigHist, bgHist, ignoreCrossSection = False):
    sig = 0
    sigNum = 0
    bgNum = 0
    #accumulate = False
    binsNumber = sigHist.GetNbinsX()
    #print "binsNumber", binsNumber
    cs = 1
    if not ignoreCrossSection:
        cs = 0.1
    #print "binsNumber=", binsNumber
    for bin in range(1, binsNumber + 1):
        #if accumulate:
        #    sigNum += sigHist.GetBinContent(bin)
        #    bgNum += bgHist.GetBinContent(bin)
        #else:
        sigNum = sigHist.GetBinContent(bin)
        bgNum = bgHist.GetBinContent(bin)
        
        if sigNum == 0:
            continue
        
        #if bgNum == 0:
        #    accumulate = True
        #else:
        #accumulate = False
        #if bin <= binsNumber and bgHist.Integral(bin+1, binsNumber) == 0:
        #    sigNum += sigHist.Integral(bin, binsNumber)
        #    bgErr = 0.2 * bgNum
        #    sig = math.sqrt(sig**2 + (cs * (sigNum / math.sqrt(bgNum + bgErr**2)))**2)
            #print "**sigNum=", sigNum, "bgNum=", bgNum, "sig=", sig
        #    break
        #else:
            #print "sigNum=", sigNum, "bgNum=", bgNum, "sig=", 0.1 * (sigNum / math.sqrt(bgNum))
        bgErr = 0.2 * bgNum
        sig = math.sqrt(sig**2 + (cs * (sigNum / math.sqrt(sigNum + bgNum + bgErr**2)))**2)
        #sig = math.sqrt(sig**2 + (cs * (sigNum / math.sqrt(bgNum + bgErr**2)))**2)
    return sig

def calcSignificanceTransferFactor(sigHist, bgHist, transferFactor, transferFactorError):
    sig = 0
    sigNum = 0
    bgNum = 0
    binsNumber = sigHist.GetNbinsX()
    startBin = bgHist.FindBin(0)
    for ibin in range(startBin, binsNumber + 1):
        
        sigNum = sigHist.GetBinContent(ibin)
        ncrCount = bgHist.GetBinContent(ibin)
        if ncrCount == 0:
            ncrCount = 1
        ncrError = bgHist.GetBinError(ibin)
        bgNum = ncrCount * transferFactor
        
        if sigNum == 0:
            continue
        
        #bgErr^2 = b^2*[ (ncrError/ncrCount)**2 + (transferFactorError/transferFactor)**2 ]
        #This is already squared
        bgErr2 = bgNum**2 * ( (ncrError/ncrCount)**2 + (transferFactorError/transferFactor)**2 )
        
        currSig = ( (sigNum / math.sqrt(bgNum + bgErr2)))
        print("sigNum,ncrCount,ncrError,bgNum,transferFactor,transferFactorError,bgErr2,currSig",sigNum,ncrCount,ncrError,bgNum,transferFactor,transferFactorError,bgErr2,currSig)
        
        
        sig = math.sqrt(sig**2 + currSig**2)
        
    return sig

def calcZ(lhdH1, lhdH0):
    bayesfactor = lhdH1/lhdH0
    z = math.log(bayesfactor)/abs(math.log(bayesfactor))*math.sqrt(2*abs(math.log(bayesfactor)))
    return z

def calcSignificanceLlhdSingleCount(sigHist, bgHist):
    sig = 0
    sigNum = 0
    bgNum = 0
    bgError = 0
    accumulate = False
    binsNumber = sigHist.GetNbinsX()
    lhdH0 = 1
    lhdH1 = 1
    
    #print "binsNumber=", binsNumber
    for bin in range(1, binsNumber + 1):
        if accumulate:
            sigNum += sigHist.GetBinContent(bin)          
            bgNum += bgHist.GetBinContent(bin)
            bgError = math.sqrt(bgError**2 + bgHist.GetBinError(bin)**2)
        else:
            sigNum = sigHist.GetBinContent(bin)
            bgNum = bgHist.GetBinContent(bin)
            bgError = bgHist.GetBinError(bin)
        if bgNum == 0:
            accumulate = True
        else:
            accumulate = False
            if bin <= binsNumber and bgHist.Integral(bin+1, binsNumber) == 0:
                sigNum += sigHist.Integral(bin, binsNumber)
                #lhd(double N,double s,double B,double dB)
                lhdH0 *= lhd(bgNum,0,bgNum,bgError)
                lhdH1 *= lhd(bgNum,0.1*sigNum,bgNum,bgError)
                
                if lhdH1 / lhdH0 != 1 and calcZ(lhdH1, lhdH0) > 0:
                    print("OOOOOOPPPPS!", "lhdH1", lhdH1, "lhdH0", lhdH0, "sigNum", sigNum, "bgNum", bgNum, "bgError", bgError, "Z", calcZ(lhdH1, lhdH0))
                #sig += 0.1 * (sigNum / math.sqrt(bgNum))
                #print "**sigNum=", sigNum, "bgNum=", bgNum, "sig=", sig
                break
            else:
                #print "sigNum=", sigNum, "bgNum=", bgNum, "sig=", 0.1 * (sigNum / math.sqrt(bgNum))
                if lhdH1 / lhdH0 != 1 and calcZ(lhdH1, lhdH0) > 0:
                    print("BEFORE OOOOOOPPPPS!", "lhdH1", lhdH1, "lhdH0", lhdH0, "sigNum", sigNum, "bgNum", bgNum, "bgError", bgError, "Z", calcZ(lhdH1, lhdH0))
                
                lhdH0 *= lhd(bgNum,0,bgNum,bgError)
                lhdH1 *= lhd(bgNum,0.1*sigNum,bgNum,bgError)
                
                if lhdH1 / lhdH0 != 1 and calcZ(lhdH1, lhdH0) > 0:
                    print("AFTER OOOOOOPPPPS!", "lhdH1", lhdH1, "lhdH0", lhdH0, "sigNum", sigNum, "bgNum", bgNum, "bgError", bgError, "Z", calcZ(lhdH1, lhdH0))
                
    
    if lhdH1 / lhdH0 == 1:
        return 0
                
    bayesfactor = lhdH1/lhdH0
    if math.log(bayesfactor)/abs(math.log(bayesfactor)) >0:
        print("WOW!! lhdH1", lhdH1, "lhdH0", lhdH0)
        
    return calcZ(lhdH1, lhdH0)

def scaleHistogram(hist, factor, factorErr):
    print("Scaling", hist.GetName(), " with ", factor, factorErr)
    tmpHist = hist.Clone()
    tmpHist.Sumw2()
    binsNumber = tmpHist.GetNbinsX()
    for binIdx in range(1, binsNumber + 1):
        tmpHist.SetBinContent(binIdx, factor)
        tmpHist.SetBinError(binIdx, factorErr)
    hist.Multiply(tmpHist)
    


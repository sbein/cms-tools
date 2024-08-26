#!/usr/bin/env python3

from ROOT import *
from glob import glob
from sys import exit
import argparse
import sys
import numpy as np
import os
import cppyy
import itertools
from datetime import datetime

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/"))
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib/classes"))

from lib import analysis_ntuples
from lib import analysis_tools
from lib import utils
from lib import analysis_observables
import plotutils

gROOT.SetBatch(True)
gStyle.SetOptStat(0)

bg_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/bg/skim/sum/slim_sum/type_sum"
number_of_files_processed = 0
histrograms_file = "tmp_histograms.root"
histograms = {}
processed_files = {}
histograms_defs = []

def createSumTypes(sumTypes):
    bg_files = glob(bg_dir + "/*")

    for f in bg_files: 
        filename = os.path.basename(f).split(".")[0]
        types = filename.split("_")
        type = None

        if types[0] == "TTJets":
            type = "_".join(types[0:2])
        elif types[0] == "ST":
            type = "_".join(types[0:3])
        else:
            type = types[0]
        if type not in sumTypes:
            sumTypes[type] = {}

def createPlotsFast(rootfiles, type_name, hist_def):
    global number_of_files_processed
    
    for f in rootfiles:

        print("\n\n\n\n\nopening", f)
        print("=============================================================")
        rootFile = TFile(f)

        c = rootFile.Get('tEvent')
        baseHistName = hist_def["obs"] + "_" + type_name
        weight_str = "135000.0 * passedMhtMet6pack * tEffhMetMhtRealXMht2016 * Weight * BranchingRatio"
        drawString = weight_str + " * (" + hist_def["condition"] + " && " + hist_def["baseline"] + ")"
        hist = utils.getHistogramFromTree(baseHistName + str(number_of_files_processed), c, hist_def["formula"], hist_def["bins"], hist_def["minX"], hist_def["maxX"], drawString, False)
        

        hist.GetXaxis().SetTitle("")
        hist.SetTitle("")
        hist.Sumw2()
        #print(hist)
        if histograms.get(baseHistName) is None:
            histograms[baseHistName] = hist.Clone(baseHistName)
            histograms[baseHistName].SetDirectory(0)
            #print("histograms", histograms)
        else:
            #print(histograms)
            histograms[baseHistName].Add(hist)
        
        all_hist_name = "all"
        if histograms.get(all_hist_name) is None:
            histograms[all_hist_name] = hist.Clone("all")
            histograms[all_hist_name].SetDirectory(0)
        else:
            #print(histograms)
            histograms[all_hist_name].Add(hist)
        
        
        drawString = weight_str + " * (" + hist_def["condition"] + " && " + hist_def["sc"] + ")"
        hist = utils.getHistogramFromTree(baseHistName + "_sc" + str(number_of_files_processed), c, hist_def["formula"], hist_def["bins"], hist_def["minX"], hist_def["maxX"], drawString, False)
        
        sc_hist_name = "sc"
        if histograms.get(sc_hist_name) is None:
            histograms[sc_hist_name] = hist.Clone("sc")
            histograms[sc_hist_name].SetDirectory(0)
        else:
            histograms[sc_hist_name].Add(hist)

        number_of_files_processed += 1
        if processed_files.get(f) is None:
            processed_files[f] = 1
        else:
            print("\n\n\n************WTF", f)
            processed_files[f] += 1
            
        rootFile.Close()

def createAllHistograms(sumTypes):

    
    calculated_lumi = utils.LUMINOSITY / 1000
    weight = utils.LUMINOSITY

    #allBgFiles = glob(bg_dir + "/*.root")    
    
    for type_name in sumTypes:
        if utils.existsInCoumpoundType(type_name):
            continue

        print("Summing type", type_name)
        rootfiles = glob(bg_dir + "/*" + type_name + "_*.root")
        createPlotsFast(rootfiles, type_name, hist_def)

    for cType in utils.compoundTypes:

        print(("Creating compound type", cType))

        rootFiles = utils.getFilesForCompoundType(cType, bg_dir)
        if len(rootFiles):
            createPlotsFast(rootFiles, cType, hist_def)
        else:
            print(("**Couldn't find file for " + cType))

def saveHistogramsToFile(histograms):
    print("\n\n\nSaving Histrograms to", histrograms_file)
    nFile = TFile(histrograms_file, "recreate")
    for k in histograms:
        histograms[k].Write(k)
    nFile.Close()

def loadAllHistograms(histograms):
    print("\n\n\nLoading Histrograms from", histrograms_file)
    nFile = TFile(histrograms_file, "read")
    keys = nFile.GetListOfKeys()
    for key in keys:
        name = key.GetName()#histogram name
        h = nFile.Get(name)
        h.SetDirectory(0)
        h.UseCurrentStyle()
        histograms[name] = h
    nFile.Close()

def main():
    
    
    jetIso = "CorrJetNoMultIso11Dr0.55"

    hist_def = { "obs" : "dilepBDT%%%", "formula" : "dilepBDT%%%", "linearYspace" : 1.5, "minX" : -1, "maxX" : 1, "bins" : 40, "condition" : "(MinDeltaPhiMhtJets > 0.4 && BTagsDeepMedium == 0 && twoLeptons%%% == 1 && MHT >= 220 &&  MET >= 140 && leptonFlavour%%% == \"Muons\" && invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81) && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0 && sameSign%%% == 0 && !tautau%%%)", "baseline" : "isoCr%%% == 0", "sc" : "isoCr%%% >= 1"}
    
    hist_def["obs"] = hist_def["obs"].replace("%%%", jetIso)
    hist_def["formula"] = hist_def["formula"].replace("%%%", jetIso)
    hist_def["condition"] = hist_def["condition"].replace("%%%", jetIso)
    hist_def["baseline"] = hist_def["baseline"].replace("%%%", jetIso)
    hist_def["sc"] = hist_def["sc"].replace("%%%", jetIso)
    histograms_defs.append(hist_def)
    
    #plotting = plotutils.Plotting()
    #currStyle = plotting.setStyle()

    # for ratio plots
    plotting = plotutils.Plotting(800,800)
    #plotting = plotutils.Plotting()
    currStyle = plotting.setStyle()
    
    sumTypes = {}
    
    load_histrograms_from_file = True
    save_histrograms_to_file = True
    
    loaded_from_file = False
    
    createSumTypes(sumTypes)
    print("sumTypes", sumTypes)
    
    c2 = TCanvas("c2")
    c2.cd()
    
    if load_histrograms_from_file and os.path.isfile(histrograms_file):
        print(("Loading histogram from file", histrograms_file))
        loadAllHistograms(histograms)
        loaded_from_file = True
    else:
        print("Creating histogram from scratch")
        createAllHistograms(sumTypes)
        
    print("---------------------")
    print(histograms)
    print("---------------------\n\n\n\n")
    print(sumTypes)
    print("---------------------\n\n\n\n")
    
    if save_histrograms_to_file and not loaded_from_file:#os.path.isfile(plot_par.histrograms_file):
        saveHistogramsToFile(histograms)
    
    print("\n\n\nnumber_of_files_processed", number_of_files_processed)
    print("len proc", len(processed_files), processed_files)
    
    processed_files_names = sorted([ os.path.basename(f) for f in processed_files.keys()])
    print("\n\n\n")
    for f in processed_files_names:
        print(f)
    
    c1 = plotting.createCanvas("c1")
    c1.cd()
    
    hs = THStack("","")

    types = [k for k in utils.bgOrder]
    types = sorted(types, key=lambda a: utils.bgOrder[a])
    
    typesInx = []
    i = 0
    
    normalise = False
    
    # normalise BG histograms:
    if normalise:
        bgSum = 0
        for type in types:
            hname = cut["name"] + "_" + hist_def["obs"] + "_" + type
            if histograms.get(hname) is not None:
                if plot_par.normalise_integral_positive_only:
                    for binIdx in range(1,histograms[hname].GetNbinsX() + 1):
                        content = histograms[hname].GetBinContent(binIdx)
                        print(("histogram", hname, "bin", binIdx, "content", content))
                        if content > 0:
                            bgSum += content
                else:
                    bgSum += histograms[hname].Integral()
        print(("Normalising BG sum", bgSum))
        if bgSum > 0:
            for type in types:
                hname = cut["name"] + "_" + hist_def["obs"] + "_" + type
                if histograms.get(hname) is not None and bgSum > 0:
                    histograms[hname].Scale(1./bgSum)

    for type in types:
        #print(histograms_defs)
        hname = histograms_defs[0]["obs"] + "_" + type
        
        if histograms.get(hname) is not None:
            hs.Add(histograms[hname])
            typesInx.append(i)
            
        i += 1
        
    #hs.Draw("hist e")
    memory = []
    legend = None
    newBgHist = histograms["all"]#plotutils.styledStackFromStack(hs, memory, legend, "", typesInx, True)

    SetOwnership(newBgHist, False)
    #newBgHist.SetFillColorAlpha(fillC, 0.35)
    
    maximum = newBgHist.GetMaximum()
    
    linearYspace = maximum*1.5


    histLowY = 0.3
    
    histCPad = TPad("cpad","cpad",0,histLowY,1,1)
    histCPad.SetBottomMargin(0.015)
    
    histRPad = TPad("rpad","rpad",0,0,1,0.3)
    histRPad.SetTopMargin(0)
    histRPad.SetBottomMargin( 0.3 )
    histRPad.SetTopMargin(0.05)

    histRPad.Draw()
    histCPad.Draw()
    
    

    
    histCPad.cd()
    newBgHist.SetMaximum(linearYspace)
    newBgHist.Draw("hist e")
    newBgHist.GetXaxis().SetLabelSize(0)
    c1.Modified()
    
    histCPad.cd()
    allHist = histograms["sc"]
    allHist.SetLineWidth(1)
    allHist.SetLineColor(kYellow)
    allHist.Draw("hist e same")
    
    histRPad.cd()
    print("Plotting ratio!")
    denHist = allHist
    styleRefHist = denHist
    
    stackSum = newBgHist.Clone()#.GetStack().Last().Clone("stackSum")
    stackSum.SetLineWidth(1)
    stackSum.SetLineWidth(kRed)
    numHist = stackSum
    memory.append(stackSum)

    chi2 = numHist.Chi2Test(denHist, "WW")

    factor = 7. / 3.
    rdataHist = None
    revRatio = False
    if revRatio:
        rdataHist = denHist.Clone()
    else:
        rdataHist = numHist.Clone()
    rdataHist.SetLineColor(styleRefHist.GetLineColor())
    rdataHist.SetLineWidth(styleRefHist.GetLineWidth())
    rdataHist.GetYaxis().SetNdivisions(505)
    rdataHist.SetMarkerStyle(1)
    rdataHist.SetMarkerSize(0)
    rdataHist.SetMarkerColor(styleRefHist.GetLineColor())
    #rdataHist.UseCurrentStyle()
    rdataHist.GetXaxis().SetLabelSize(0.05*factor)
    rdataHist.GetYaxis().SetLabelSize(0.05*factor)
    rdataHist.GetXaxis().SetTitleSize(0.06*factor)
    rdataHist.GetYaxis().SetTitleSize(0.06*factor)
    rdataHist.GetYaxis().SetTitleOffset(0.9 / factor)
    rdataHist.GetYaxis().CenterTitle()
   
    #
    memory.append(rdataHist)
    
    if revRatio:
        rdataHist.Divide(numHist)
    else:
        rdataHist.Divide(denHist)

    rdataHist.SetMinimum(0)
    rdataHist.SetMaximum(2)

    
    rdataHist.Draw("p")
    rdataHist.Draw("same e0")
    tline = TLine(rdataHist.GetXaxis().GetXmin(),1,rdataHist.GetXaxis().GetXmax(),1);
    tline.SetLineColor(kRed);
    tline.Draw("SAME");
    
    tl = TLatex()
    tl.SetNDC()
    tl.SetTextSize(0.15) 
    tl.SetTextFont(42)
    
    
    tl.DrawLatex(.2,.4,"p-value = " + "{:.2f}".format(chi2))
    
    
    memory.append(tline)
    c1.Modified()
    
    
    
    c1.Print("stack4.pdf")
    
main()
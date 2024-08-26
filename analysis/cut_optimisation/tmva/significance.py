#!/usr/bin/env python

from ROOT import *
from glob import glob
from sys import exit
import argparse
import sys
import math

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='Run TMVA.')
parser.add_argument('-i', '--input_dir', nargs=1, help='Input Directory', required=True)
args = parser.parse_args()


input_dir = None
if args.input_dir:
	input_dir = args.input_dir[0]
######## END OF CMDLINE ARGUMENTS ########

gROOT.SetBatch(1)
gStyle.SetOptStat(0)

def do_significance_plot(h_significance, h_mva_bdt_effB, h_mva_bdt_effS, eff_sg, eff_bg, max_cut_value, Z, output_filename):

	canvas_significance = TCanvas("significance", "significance", 520, 10, 1000, 1000)
	canvas_significance.SetTopMargin(0.5 * canvas_significance.GetTopMargin())
	canvas_significance.SetBottomMargin(0.9 * canvas_significance.GetBottomMargin())
	canvas_significance.SetLeftMargin(1 * canvas_significance.GetLeftMargin())
	canvas_significance.SetRightMargin(0.3 * canvas_significance.GetRightMargin())
	canvas_significance.cd()
	h_significance.SetLineColor(kRed)
	h_significance.SetLineWidth(2)
	h_significance.SetTitle(";BDT classifier; #epsilon, Z")
	h_significance.SetFillColor(0)
	h_significance.Draw("")
	h_significance.GetYaxis().SetTitleOffset(1.2)
	h_mva_bdt_effB.SetLineColor(kBlack)
	h_mva_bdt_effB.SetFillColor(0)
	h_mva_bdt_effB.Draw("same")
	h_mva_bdt_effB.SetLineWidth(2)
	h_mva_bdt_effS.SetLineColor(kBlue)
	h_mva_bdt_effS.SetLineWidth(2)
	h_mva_bdt_effS.SetFillColor(0)
	h_mva_bdt_effS.Draw("same")

	line = TLine(max_cut_value,0,max_cut_value,Z)
	line.SetLineWidth(2)
	line.SetLineStyle(3)
	line.Draw()

	legend_significance = TLegend(0.15, 0.2, 0.44, 0.4)
	legend_significance.SetHeader("x1x2x1")
	legend_significance.AddEntry(h_mva_bdt_effS, "#epsilon (signal)")
	legend_significance.AddEntry(h_mva_bdt_effB, "#epsilon (background)")
	legend_significance.AddEntry(h_significance, "Z = S/#sqrt{S+B}")
	legend_significance.SetBorderSize(0)
	legend_significance.SetFillStyle(0)
	legend_significance.SetNColumns(1)
	legend_significance.Draw()

	latex_significance=TLatex()
	latex_significance.SetNDC()
	latex_significance.SetTextAngle(0)
	latex_significance.SetTextColor(kBlack)
	latex_significance.SetTextFont(42)
	latex_significance.SetTextSize(0.035)
	latex_significance.DrawLatex(0.15, 0.9, "maximum Z:" + str(Z))
	latex_significance.DrawLatex(0.15, 0.85, "#epsilon_{sg}=%.2f, #epsilon_{bg}=%.4f" % (eff_sg, eff_bg))

	canvas_significance.SaveAs(output_filename)

def plot_significance():
	print("Getting best TMVA significance...")

	# get TMVA histograms
	print("Opening file", input_dir + "/output.root")
	fin = TFile(input_dir + "/output.root")
	
	trainTree = fin.Get("dataset/TrainTree")
	testTree = fin.Get("dataset/TestTree")
	
	h_mva_bdt_effB = fin.Get("dataset/Method_BDT/BDT/MVA_BDT_effB")
    	h_mva_bdt_effS = fin.Get("dataset/Method_BDT/BDT/MVA_BDT_effS")
	
	# trainTree.Draw("BDT>>hsqrt(20000,-1,1)", "weight * (classID==0)")
# 	trainSignalHistBDT = trainTree.GetHistogram().Clone()
# 	trainSignalHistBDT.SetDirectory(0)
# 	trainTree.Draw("BDT>>hsqrt(20000,-1,1)", "weight * (classID==1)")
# 	trainBgHistBDT = trainTree.GetHistogram().Clone()
# 	trainBgHistBDT.SetDirectory(0)
# 	testTree.Draw("BDT>>hsqrt(20000,-1,1)", "weight * (classID==0)")
# 	testSignalHistBDT = testTree.GetHistogram().Clone()
# 	testSignalHistBDT.SetDirectory(0)
# 	testTree.Draw("BDT>>hsqrt(20000,-1,1)", "weight * (classID==1)")
# 	testBgHistBDT = testTree.GetHistogram().Clone()
# 	testBgHistBDT.SetDirectory(0)
# 	
# 	print(trainSignalHistBDT.Integral())
# 	print(testSignalHistBDT.Integral())
# 	print(trainBgHistBDT.Integral())
# 	print(testBgHistBDT.Integral())
# 	
# 	return
	
	
	testTree.Draw("BDT>>hsqrt(10000)", "weight * (classID==0)")
	testSignalHistBDT = testTree.GetHistogram().Clone()
	testSignalHistBDT.SetDirectory(0)
	testTree.Draw("BDT>>hsqrt(10000)", "weight * (classID==1)")
	testBgHistBDT = testTree.GetHistogram().Clone()
	testBgHistBDT.SetDirectory(0)
	trainTree.Draw("BDT>>hsqrt(10000)", "weight * (classID==0)")
	trainSignalHistBDT = trainTree.GetHistogram().Clone()
	trainSignalHistBDT.SetDirectory(0)
	trainTree.Draw("BDT>>hsqrt(10000)", "weight * (classID==1)")
	trainBgHistBDT = trainTree.GetHistogram().Clone()
	trainBgHistBDT.SetDirectory(0)
	
	minX = max(testBgHistBDT.GetXaxis().GetXmin(), testSignalHistBDT.GetXaxis().GetXmin(), trainSignalHistBDT.GetXaxis().GetXmin(), trainBgHistBDT.GetXaxis().GetXmin())
	maxX = min(testBgHistBDT.GetXaxis().GetXmax(), testSignalHistBDT.GetXaxis().GetXmax(), trainSignalHistBDT.GetXaxis().GetXmax(), trainBgHistBDT.GetXaxis().GetXmax())
	
	print(minX, maxX)
	
	testTree.Draw("BDT>>hsqrt(10000," + str(minX) + "," + str(maxX) + ")", "weight * (classID==0)")
	testSignalHistBDT = testTree.GetHistogram().Clone()
	testSignalHistBDT.SetDirectory(0)
	testTree.Draw("BDT>>hsqrt(10000," + str(minX) + "," + str(maxX) + ")", "weight * (classID==1)")
	testBgHistBDT = testTree.GetHistogram().Clone()
	testBgHistBDT.SetDirectory(0)
	trainTree.Draw("BDT>>hsqrt(10000," + str(minX) + "," + str(maxX) + "", "weight * (classID==0)")
	trainSignalHistBDT = trainTree.GetHistogram().Clone()
	trainSignalHistBDT.SetDirectory(0)
	trainTree.Draw("BDT>>hsqrt(10000," + str(minX) + "," + str(maxX) + "", "weight * (classID==1)")
	trainBgHistBDT = trainTree.GetHistogram().Clone()
	trainBgHistBDT.SetDirectory(0)
	
 	print("testSignalHistBDT")
 	print(testSignalHistBDT.Integral(), testSignalHistBDT.GetNbinsX(), testSignalHistBDT.GetXaxis().GetXmin(), testSignalHistBDT.GetXaxis().GetXmax())
 	print("testBgHistBDT")
 	print(testBgHistBDT.Integral(), testBgHistBDT.GetNbinsX(), testBgHistBDT.GetXaxis().GetXmin(), testBgHistBDT.GetXaxis().GetXmax())

	numOfBins = testBgHistBDT.GetNbinsX()
	print("numOfBins=" , numOfBins)
	
	# custom histograms
	
	h_significance = TH1D("significance", "significance", numOfBins, minX, maxX)

	for i in range(numOfBins):
		
		S = trainSignalHistBDT.Integral(i,numOfBins+1) + testSignalHistBDT.Integral(i,numOfBins+1)
 		B = trainBgHistBDT.Integral(i,numOfBins+1) + testBgHistBDT.Integral(i,numOfBins+1)
		#S = 2 * testSignalHistBDT.Integral(i,numOfBins+1)
		#B = 2 * testBgHistBDT.Integral(i,numOfBins+1)
		if (S+B)>0:
			sign = 1.0 * S/math.sqrt(S+B)
			h_significance.SetBinContent(i, sign)
			#print("========")
			#print(i, sign)
			#print(testSignalHistBDT.GetBinCenter(i), testBgHistBDT.GetBinCenter(i))
			#print(S,B)
			h_significance.SetBinError(i, 0)
	
	print(h_significance.GetXaxis().GetXmin(), h_significance.GetXaxis().GetXmax())
	
	maxBin = h_significance.GetMaximumBin()
	
	S =  trainSignalHistBDT.Integral(maxBin,numOfBins+1) + testSignalHistBDT.Integral(maxBin,numOfBins+1)
	B = trainBgHistBDT.Integral(maxBin,numOfBins+1) + testBgHistBDT.Integral(maxBin,numOfBins+1)
	
	ST = trainSignalHistBDT.Integral() + testSignalHistBDT.Integral()
	BT = trainBgHistBDT.Integral() + testBgHistBDT.Integral()
	
	# S =  2 * testSignalHistBDT.Integral(maxBin,numOfBins+1)
# 	B = 2 * testBgHistBDT.Integral(maxBin,numOfBins+1)
# 	
# 	ST = 2 * testSignalHistBDT.Integral()
# 	BT = 2 * testBgHistBDT.Integral()
	
	print("(S,B)=(" + str(S) + "," + str(B) + ")")
	print("(ST,BT)=(" + str(ST) + "," + str(BT) + ")")
	
	max_cut_value = h_significance.GetBinCenter(maxBin)
	Z = h_significance.GetBinContent(maxBin)
	eff_sg = S / ST
	eff_bg = B / BT

	do_significance_plot(h_significance, h_mva_bdt_effB, h_mva_bdt_effS, eff_sg, eff_bg, max_cut_value, Z, input_dir + "/significance.pdf")

	fin.Close()

	return

if __name__ == "__main__":
	plot_significance()




from ROOT import *
from utils import *
from glob import glob
from random import shuffle
import heapq

gROOT.SetBatch(1)
gStyle.SetOptStat(0)
execfile('RandomGridSearch/RGS/examples/Higgs/HO1/python/optimalCutsDict.py')
execfile('python/EventCategories.py')
UseOptimizedCuts = True
dolog = True
lumi = 35900

sorsb = False
asimov = not sorsb

fnew = TFile('sr_canvases.root','recreate')

baseline = 'Ht>100'
rselection = '(SumTagPtOverMet>=0.2 && DPhiMetSumTags<=2.8)'
anabins = {}
anabins['bin1']  = 'Met>200 && Met<=300 && NTags==1 && NJets==1'
anabins['bin2']  = 'Met>200 && Met<=300 && NTags==1 && NJets>=2 && NJets<=3'
anabins['bin3']  = 'Met>200 && Met<=300 && NTags==1 && NJets>=4'
anabins['bin4']  = 'Met>300 && Met<=600 && NTags==1 && NJets==1'
anabins['bin5']  = 'Met>300 && Met<=600 && NTags==1 && NJets>=2 && NJets<=3'
anabins['bin6']  = 'Met>300 && Met<=600 && NTags==1 && NJets>=4'
anabins['bin7']  = 'Met>600 && NTags==1 && NJets==1'
anabins['bin8']  = 'Met>600 && NTags==1 && NJets>=2 && NJets<=3'
anabins['bin9']  = 'Met>600 && NTags==1 && NJets>=4'
#anabins['bin10']  = 'Met>200 && Met<=300 && NTags>=2'
#anabins['bin11']  = 'Met>300 && NTags>=2'
#anabins['binTest']  = 'Met>200 && NTags>=1 && NJets==1'
for key in anabins.keys():
	anabins[key] = anabins[key] + ' && '+baseline
	anabins[key.replace('bin','sr')] = anabins[key] + ' && ' + rselection
	anabins[key.replace('bin','cr')] = anabins[key] + ' && !' + rselection	

histframes = {}
#histframes['Ht'] = TH1F('Ht','',18,0,900)
#histframes['DPhiMetSumTags'] = TH1F('DPhiMetSumTags','',16,0,3.2)
histframes['SumTagPtOverMet'] = TH1F('SumTagPtOverMet','',12,0,2.4)

sigcounts = {}
binnedSensitivityDict = {}
bkgcounts = {}

for selkey in anabins:
 if not 'sr' in selkey: continue
 hists = {}
 histsStack = {}
 for histkey in histframes:
	cwaste = TCanvas('cwaste')
	growinghist = histframes[histkey].Clone(histkey)
	histframes[histkey].GetXaxis().SetTitle(namewizard(histframes[histkey].GetName()))
	growinghist.GetXaxis().SetTitle(namewizard(histkey))	
	histoStyler(growinghist, kGray+1)
	growinghist.SetFillStyle(1001)	
	nbins = histframes[histkey].GetXaxis().GetNbins()
	xlow = histframes[histkey].GetXaxis().GetBinLowEdge(1)
	xhigh = histframes[histkey].GetXaxis().GetBinUpEdge(nbins)
	drawarg = 'max(%f+0.001,min(%f-0.001,%s))>>hadc(%d,%f,%f)'%(xlow,xhigh,histkey,nbins,xlow,xhigh)
	weightstring = '('+anabins[selkey]+')*weight*'+str(lumi)
	if UseOptimizedCuts: weightstring+='*('+'1'+')'		
	for category in CategoryKeysSmallToBig:
		hCategory = histframes[histkey].Clone(histkey+'_cat')
		histoStyler(hCategory,ColorsByCategory[category])
		hCategory.SetFillColor(ColorsByCategory[category])
		hCategory.SetFillStyle(1001)
		histoStyler(growinghist,ColorsByCategory[category])
		growinghist.SetFillColor(ColorsByCategory[category])
		growinghist.SetFillStyle(1001)			
		for subcategory in SubcategoryChainDictsByCategoryDict[category]:
			SubcategoryChainDictsByCategoryDict[category][subcategory].Draw(drawarg,weightstring)
			h = SubcategoryChainDictsByCategoryDict[category][subcategory].GetHistogram()
			hCategory.Add(h)
		growinghist.Add(hCategory)			
		hists[category] = hCategory.Clone(category)
		histsStack[category] = growinghist.Clone(category+'_stack')
	b = histsStack[CategoryKeysBigToSmall[0]].Integral(-1,9999)
	bkgcounts[selkey] = b
	sighists = []
	for ikey, key in enumerate(SignalChainDict.keys()):
		SignalChainDict[key].Draw(drawarg,weightstring)
		hsig = SignalChainDict[key].GetHistogram()
		hsig.SetDirectory(0)
		hsig.SetTitle(key)
		sighists.append(hsig)
		histoStyler(sighists[-1],ColorsBySignal[key])
		sighists[-1].SetLineStyle(kDashed)		
		sighists[-1].SetLineColor(sighists[-1].GetMarkerColor())	
		model = '_'.join(key.split('_')[2:])
		if not model in sigcounts.keys(): 
			sigcounts[model] = {}
			binnedSensitivityDict[model] = {}	
		s = sighists[-1].Integral(-1,9999)
		sigcounts[model][selkey] = s
		if sorsb:
			try: binnedSensitivityDict[model][selkey] = s/TMath.Sqrt(s+b)
			except: binnedSensitivityDict[model][selkey] = 0
		elif asimov: binnedSensitivityDict[model][selkey] = TMath.Sqrt(2*((s+b)*TMath.Log(1+1.0*s/b)-s))			
	c1 = mkcanvas('c_'+histkey+'_'+selkey)
	if dolog: c1.SetLogy()
	histsStack[CategoryKeysBigToSmall[0]].SetLineColor(kGray+1)		
	if dolog:
		stackmax = histsStack[CategoryKeysBigToSmall[0]].GetMaximum()
		histsStack[CategoryKeysBigToSmall[0]].GetYaxis().SetRangeUser(0.1,300*stackmax)
	else:
		stackmax = histsStack[CategoryKeysBigToSmall[0]].GetMaximum()
		histsStack[CategoryKeysBigToSmall[0]].GetYaxis().SetRangeUser(0,1.3*stackmax)
	legBkg = mklegend(x1=.61, y1=.56, x2=.95, y2=.88, color=kWhite)
	arg = ''
	for category in CategoryKeysBigToSmall:
		histsStack[category].Draw('hist '+arg)
		legBkg.AddEntry(histsStack[category],category,'f')
		arg = 'same'
	histsStack[CategoryKeysBigToSmall[0]].Draw('same E0')
	legSig = mklegend(x1=.16, y1=.7, x2=.6, y2=.88, color=kWhite)	
	for sighist in sighists[:5]:
		sighist.Draw('hist same')
		legSig.AddEntry(sighist,sighist.GetTitle().replace('_MCMC1',''),'l')
	histsStack[CategoryKeysBigToSmall[0]].Draw('axis same')	
	legBkg.Draw()
	legSig.Draw()
	stamp(round(1.0*lumi/1000,1))
	c1.Update()
	fnew.cd()	
	c1.Write('c_'+str(selkey)+'_'+histkey+'_'+anabins[selkey].replace(' && ','&').replace('==','='))
	c1.Print('pdfs/kinematics/'+str(selkey)+'_'+histkey+'_'+anabins[selkey].replace(' && ','&').replace('==','=')+'.pdf')
	#pause()
print('just created', fnew.GetName())
fnew.Close()
		

textable = r'''
\frame{\frametitle{Most sensitive fiducial regions by model}
\begin{itemize}
\item{Sensitivity of 1st and 2nd best signal regions for each model, compared with the idealized RGS signal region.}
\end{itemize}
\rowcolors{1}{RoyalBlue!20}{RoyalBlue!5}
\scriptsize
\begin{tabular}{c c c c c c c c c c}
model & SR$^1$ & s$^1$ & b$^1$ & $\sigma^1$ & SR$^2$ & s$^2$ & b$^2$ & $\sigma^2$ & $\sigma^{\text{max}}$ \\ 
'''

for model in sorted(sigcounts.keys()):
		max_value = heapq.nlargest(1, binnedSensitivityDict[model].values())[0]
		max_value2 = heapq.nlargest(2, binnedSensitivityDict[model].values())[1]		
		max_keys = [k for k, v in binnedSensitivityDict[model].items() if v == max_value]
		max_keys2 = [k for k, v in binnedSensitivityDict[model].items() if v == max_value2]		
		#print('len(max_keys)', len(max_keys)		)
		theline = '\\texttt{%s} & %s & %.1f &  %.1f & \\textbf{%.1f} & %s & %.1f & %.1f & \\textbf{%.1f} & \\textbf{%.1f}' % (model.replace('_',r'\_'), max_keys[0].replace('sr',''),sigcounts[model][max_keys[0]], bkgcounts[max_keys[0]],binnedSensitivityDict[model][max_keys[0]],max_keys2[0].replace('sr',''),sigcounts[model][max_keys2[0]],bkgcounts[max_keys2[0]], binnedSensitivityDict[model][max_keys2[0]], sensitivityDict[model])+r'\\'
		textable+=theline+'\n'
	  # maximum value
textable+=r'''\end{tabular}
\begin{itemize}
\item{Some comment perhaps?}
\end{itemize}
}
'''
print(textable)
	

		
'''
for selkey in anabins:
	#print('='*5+selkey+'='*5)
	#print('n(bkg)=%2f' % bkgcounts[selkey])
	for key in SignalChainDict:
		model = '_'.join(key.split('_')[2:])
		#print('n('+model+')=%2f, sigma=%2f' % (sigcounts[model][selkey], binnedSensitivityDict[model][selkey]))
'''
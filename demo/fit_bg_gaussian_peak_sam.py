from ROOT import *
from utils import *
import os, sys
gStyle.SetOptStat(0)
gROOT.SetBatch(1)

try: mode = sys.argv[1]
except: 
    mode = 'HE_0p001'
    mode = 'SV'

    

if 'HE' in mode:
    infile=TFile('/nfs/dust/cms/user/tewsalex/CMSSW_10_5_0/src/plots/2020_03_02_V0Fitter/HEToVoComparison/Comparison_'+mode+'.root')
    hmass = infile.Get('h_tracksWithSV_invMass_KShort')

if mode=='SV':
    infile = TFile('V0FitterResult_dcaLTp02.root')
    canvas = infile.Get('canvas')
    lops = canvas.GetListOfPrimitives()
    for p in lops:
        print(p.GetName())
    hmass = canvas.GetPrimitive('mass__1').Clone()
if mode=='Lambda':
    infile = TFile('vertex_plots.root')
    infile.ls()
    hmass = infile.Get('mass_to4p0_Lambda')


hmass.SetLineWidth(2)
hmass.SetLineColor(kBlack)
hmass.SetMarkerColor(kBlack)
if not hmass.GetSumw2N(): hmass.Sumw2()    
xax = hmass.GetXaxis()
lowedge, highedge = xax.GetBinLowEdge(1), xax.GetBinUpEdge(xax.GetNbins())

newfile = TFile('rootfiles/kshorts_'+mode+'.root', 'recreate')
c1= mkcanvas('c1')
leg = mklegend(x1=.52, y1=.55, x2=.88, y2=.78, color=kWhite)

def funcBackground(x,par):
    return par[0]+par[1]*x[0]

def funcGaussian(x,par):
    return par[0]*TMath.Exp(-(x[0]-par[1])*(x[0]-par[1])/(2*par[2]*par[2]))

def funcFullModel(x,par):
    return par[0]*TMath.Exp(-(x[0]-par[1])*(x[0]-par[1])/(2*par[2]*par[2]))+par[3]+par[4]*x[0]

fFullModel = TF1('fFullModel', funcFullModel, lowedge,highedge,5)
fFullModel.SetParameter(0,50)
if mode=='Lambda':fFullModel.SetParameter(1,1.115)
else: fFullModel.SetParameter(1,.5)
fFullModel.SetParameter(2,.02)
fFullModel.SetParLimits(2,0,99)


fitresult = hmass.Fit(fFullModel,'s','',lowedge,highedge)

fGaussian = TF1('fGaussian', funcGaussian,lowedge,highedge,3)
fGaussian.SetParameter(0,fitresult.Parameter(0))
fGaussian.SetParameter(1,fitresult.Parameter(1))
fGaussian.SetParameter(2,fitresult.Parameter(2))

fBackground = TF1('fBackground', funcBackground,lowedge,highedge,2)
fBackground.SetParameter(0,fitresult.Parameter(3))
fBackground.SetParameter(1,fitresult.Parameter(4))


nsig = fGaussian.Integral(lowedge,highedge)/hmass.GetBinWidth(1)
nbkg = fBackground.Integral(lowedge,highedge)/hmass.GetBinWidth(1)

print('par 0 was', fGaussian.GetParameter(0))
peak = fGaussian.GetParameter(1)
width = fGaussian.GetParameter(2)
nsigPeak = fGaussian.Integral(peak-width,peak+width)/hmass.GetBinWidth(1)
nbkgPeak = fBackground.Integral(peak-width,peak+width)/hmass.GetBinWidth(1)

print('signal', nsig)
print('bkg', nbkg)

hmass.GetYaxis().SetRangeUser(0.0,1.3*hmass.GetMaximum())

nup = 100
hbkg = hmass.Clone('hbkg')
hbkg.Reset()
hbkg.SetTitle('linear bkg. model')
histoStyler(hbkg, kRed-7, 1.15)
hbkg.SetFillColor(hbkg.GetLineColor())
for i in range(int(nup*nbkg)):
    hbkg.Fill(fBackground.GetRandom(),1./nup)


function = hmass.GetListOfFunctions()[0].Clone('fmodel')
function.SetLineColor(kBlue)
hmass.GetListOfFunctions()[0].Delete()
    
hsig = hmass.Clone('hsig')
hsig.Reset()
if mode=='Lambda': hsig.SetTitle('#Lambda^{#pm} (gauss fit)')
else: hsig.SetTitle('K_{s}^{0} (gauss fit)')
histoStyler(hsig, kGreen-9, 1.15)
hsig.SetFillColor(hsig.GetLineColor())
for i in range(int(nup*nsig)):
    hsig.Fill(fGaussian.GetRandom(),1./nup)   
#hsig.GetListOfFunctions()[0].Delete()     

hmass.SetTitle('data (2016G)')
hsig_ = hsig.Clone()
hratio, pad1, pad2 = FabDraw(c1,leg,hmass,[hbkg,hsig_],datamc='data',lumi=epsi, title = '', LinearScale=True, fractionthing='data / fit res.')
leg.AddEntry(function, '5-parameter fit')

hratio.GetYaxis().SetRangeUser(0.0,2.6)
#hratio.GetYaxis().SetTitle('(B/A*C)/D')
#hratio.GetYaxis().SetRangeUser(-3,3)
hratio.SetLineColor(kBlack)
for ibin in range(1,hratio.GetXaxis().GetNbins()+1):
    if hratio.GetBinContent(ibin)==0:
        hratio.SetBinContent(ibin,-999)
histoStyler(hratio, kBlack, 2.1)
hratio.SetMarkerColor(kBlack)
#hratio.GetYaxis().SetTitleSize(0.095)
hratio.GetYaxis().SetTitleOffset(.44)
hratio.SetDirectory(0)


pad1.cd()
function.Draw('same')
hmass.SetTitle('')
hmass.Draw('p same')
hmass.Draw('e same')
tl.SetTextSize(1.1*tl.GetTextSize())
font = tl.GetTextFont()
tl.SetTextFont(extraTextFont)
tl.DrawLatex(.15,.62, mode)
tl.SetTextSize(1.0/1.1*tl.GetTextSize())
tl.SetTextFont(font)
tl.DrawLatex(.15,.55, 'n(s) @ peak#pm#sigma= %.2f '%nsigPeak)
tl.DrawLatex(.15,.5, 'n(b) @ peak#pm#sigma= %.2f '%nbkgPeak)
tl.DrawLatex(.15,.44, 'sig. purity: %.4f '% (nsigPeak/(nsigPeak+nbkgPeak)))
c1.Update()
newfile.cd()
c1.Write('c_kshorts_'+mode)
hsig.Write()
fGaussian.Write('fsignal')
c1.Print('kshorts_'+mode+'.png')
print('just created', newfile.GetName())
newfile.Close()



'''
python tools/SvSignalExtractDraw.py HE_0p001
python tools/SvSignalExtractDraw.py HE_0p01
python tools/SvSignalExtractDraw.py HE_0p02
python tools/SvSignalExtractDraw.py HE_0p03
python tools/SvSignalExtractDraw.py HE_0p05
python tools/SvSignalExtractDraw.py HE_0p10
'''


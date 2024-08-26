#!/usr/bin/python

texskeleton = \
r'''\documentclass[12pt,A4paper]{article}

\usepackage{cite}
\usepackage{hyperref}
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{mathtools}

\DeclarePairedDelimiter\abs{\lvert}{\rvert}

\begin{document}

\begin{table}
\begin{centering}
\begin{tabular}{ | c | c | c | }
\hline
selection & n(passed) & rel. eff. (tot. eff) \\
\hline
TABLEROWS
\hline
\end{tabular}
\caption{Cut flow of unweighted event counts derived from events in sample \texttt{*Summer16.TTJets\_TuneCUETP8M1\_13TeV*} in the attempt to carry out the SUS-16-048 selection.}
\end{centering}
\end{table}

At this point we think we are using all of the required collections with a couple of small modifications, which are a nuissance. The differences are our jets have a pT cut of 30 and not 25 GeV, and the leptons we are using are the EGamma POG's loose WP leptons, and not the super loose HIG POG leptons. We don't think these differences should result in enormous changes. However, there is a good chance something else is not perfectly synchronized yet. - Yuval and Sam.

\end{document}
'''
namedict = {}
namedict['Total'] = 'No cuts'
namedict['Dilepton'] = r'n($\ell$) = 2'
namedict['GT1J'] = r'n(jet) $\geq$ 1'
namedict['NoBTags'] = r'n(b) = 0'
namedict['MetCut'] = r'$E_{\text{T}}^{\text{miss}} \geq 125$ GeV'
namedict['DileptonPt'] = r'$p_{\text{T}}(\ell\ell) \geq 3$ GeV'
namedict['LeptonPt'] = r'$p_{\text{T}}(\ell_{1,2}) \in [5,30]$ GeV'
namedict['MetDHt'] = r'$0.6 \leq E_{\text{T}}^{\text{miss}}/H_{\text{T}} \leq$ 1.4'
namedict['Mt'] = r'$M_{\text{T}} \leq 70$ GeV'
namedict['DileptonInvMass'] = r'$M(\ell\ell) \in [4,9]$ or $[10.5,50]$'
namedict['Ht'] = r'$H_{\text{T}} \geq 100$ GeV'
namedict['Eta'] = r'$\abs{\eta_{\mu}}<2.4,\abs{\eta_{e}}<2.5$'
namedict['MtautauVeto'] = r'$M(\tau\tau)$ veto $[0,160]$ GeV'
namedict['DileptonLepCorMET'] = r'$\mu$-corr. $E_{\text{T}}^{\text{miss}} \geq 125$ GeV'

rawlines = open('rawtext.txt').readlines()
TABLEROWS = ''
for line in rawlines:
    fields = line.split()
    fields[0] = namedict[fields[0]]
    fields[2] = str(round(float(fields[2]),3))
    fields[3] = str(round(float(fields[3]),5))
    
    row = fields[0] + ' & ' + fields[1] + ' & ' + fields[2] + '(' + fields[3] + ')' +r' \\'
    TABLEROWS+=row+'\n'

print(TABLEROWS)

tabledoc = texskeleton.replace('TABLEROWS',TABLEROWS)
newfile = open('CutFlowTables.tex','w')
newfile.write(tabledoc)

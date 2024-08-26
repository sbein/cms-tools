#!/usr/bin/env python

print(r""")
\documentclass[12pt,A4paper]{article}
\usepackage{cite}
\usepackage{hyperref}
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{mathtools}
\usepackage{multirow}
\begin{document}

\begin{table}[]
\hspace*{-2cm}
\begin{tabular}{lllllllllll}
\cline{3-11}
                                             & \multicolumn{1}{l|}{}       & \multicolumn{3}{c|}{lt}                                        & \multicolumn{3}{c|}{2l}                                        & \multicolumn{3}{c|}{Total}                                     \\ \hline 
\multicolumn{1}{|l|}{$\mu$}                    & \multicolumn{1}{l|}{$\Delta\mathrm{M}$}     & \multicolumn{1}{l|}{category} & \multicolumn{1}{l|}{inclusive} & \multicolumn{1}{l|}{rect} & \multicolumn{1}{l|}{category} & \multicolumn{1}{l|}{inclusive} & \multicolumn{1}{l|}{rect} & \multicolumn{1}{l|}{category} & \multicolumn{1}{l|}{inclusive} & \multicolumn{1}{l|}{rect} \\ \hline
"""

f = open("significance", "r")
fl = f.read().splitlines() 
mu = None

muCount = {}

for l in fl:
    line = l.split(" ")
    if muCount.get(line[0]) is None:
        muCount[line[0]] = 1
    else:
        muCount[line[0]] += 1

currMuCount = 0
for l in fl:
    line = l.split(" ")
    if mu is None or line[0] != mu:
        currMuCount = 1
        mu = line[0]
        mun = line[0].split("mu")[1]
        dmn = line[1].split("dm")[1]
        print(r"""\multicolumn{1}{|l|}{\multirow{""" + str(muCount[line[0]]) + r"""}{*}{""" + mun + r"""}} & \multicolumn{1}{l|}{""" + dmn + r"""} & \multicolumn{1}{c|}{"""+line[2]+r"""}        & \multicolumn{1}{c|}{"""+line[3]+r"""}         & \multicolumn{1}{c|}{"""+line[4]+r"""}        & \multicolumn{1}{c|}{"""+line[5]+r"""}         & \multicolumn{1}{c|}{"""+line[6]+r"""}        & \multicolumn{1}{c|}{"""+line[7]+r"""}         & \multicolumn{1}{c|}{"""+line[8]+r"""}         & \multicolumn{1}{c|}{"""+line[9]+r"""}         & \multicolumn{1}{c|}{"""+line[10]+r"""}         \\ \cline{2-11} """)
    else:
        currMuCount += 1
        dmn = line[1].split("dm")[1]
        ending = ""
        if currMuCount < muCount[line[0]]:
            ending = r"""\cline{2-11}"""
        else:
            ending = r"""\hline"""
            currMuCount = 0
        print(r"""\multicolumn{1}{|l|}{} & \multicolumn{1}{l|}{""" + dmn + r"""} & \multicolumn{1}{c|}{"""+line[2]+r"""}        & \multicolumn{1}{c|}{"""+line[3]+r"""}         & \multicolumn{1}{c|}{"""+line[4]+r"""}        & \multicolumn{1}{c|}{"""+line[5]+r"""}         & \multicolumn{1}{c|}{"""+line[6]+r"""}        & \multicolumn{1}{c|}{"""+line[7]+r"""}        & \multicolumn{1}{c|}{"""+line[8]+r"""}        & \multicolumn{1}{c|}{"""+line[9]+r"""}        & \multicolumn{1}{c|}{"""+line[10]+r"""}         \\ """ + ending)
    
    
print(r""")
\end{tabular}
\end{table}
\end{document}
"""
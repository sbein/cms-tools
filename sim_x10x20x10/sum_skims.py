#!/usr/bin/env python3.8

from ROOT import *
from glob import glob
from math import *
from sys import exit
from array import array
from os import system
import argparse
import os
import sys
import argparse
import itertools

parser = argparse.ArgumentParser(description='Create skims for x1x2x1 process.')
parser.add_argument('-tl', '--tl', dest='two_leptons', help='Two Leptons', action='store_true')
parser.add_argument('-sam', '--sam', dest='sam', help='Sam Skims', action='store_true')
parser.add_argument('-slim', '--slim', dest='slim', help='Slim Skims', action='store_true')
parser.add_argument('-phase1', '--phase1', dest='phase1', help='Phase 1', action='store_true')
parser.add_argument('-phase1_2018', '--phase1_2018', dest='phase1_2018', help='Phase 1 2018', action='store_true')
parser.add_argument('-nlp', '--no_lepton_selection', dest='no_lepton_selection', help='No Lepton Selection Skim', action='store_true')
parser.add_argument('-jecup', '--jecup', dest='jecup', help='jec-up variation', action='store_true')
parser.add_argument('-jecdown', '--jecdown', dest='jecdown', help='jec-down variation', action='store_true')
args = parser.parse_args()

two_leptons = args.two_leptons
sam = args.sam
no_lepton_selection = args.no_lepton_selection
slim = args.slim
phase1 = args.phase1
phase1_2018 = args.phase1_2018
jecup = args.jecup; jecdown = args.jecdown

#skim_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/single/"
#output_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/sum"

skim_dir = "/nfs/dust/cms/user/beinsam/x1x2x1/signal/skim_sam/single/"
output_dir = "/nfs/dust/cms/user/beinsam/x1x2x1/signal/skim_sam/sum"

if slim:
    if phase1:
        skim_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_phase1/slim/"
        output_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_phase1/slim_sum"
    else:
        skim_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim/"
        output_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/slim_sum"

if sam:
    if phase1:
        skim_dir = "/nfs/dust/cms/user/beinsam/x1x2x1/signal/skim_phase1/single/"##to change
        output_dir = "/nfs/dust/cms/user/beinsam/x1x2x1/signal/skim_phase1/sum"##to change
    elif phase1_2018:
        skim_dir = "/nfs/dust/cms/user/beinsam/x1x2x1/signal/skim_phase1_2018/single/"##to change
        output_dir = "/nfs/dust/cms/user/beinsam/x1x2x1/signal/skim_phase1_2018/sum"##to change
    else:
        skim_dir = "/nfs/dust/cms/user/beinsam/x1x2x1/signal/skim_sam/single/"
        output_dir = "/nfs/dust/cms/user/beinsam/x1x2x1/signal/skim_sam/sum"
        

if two_leptons:
    skim_dir = "/afs/desy.de/user/n/nissanuv/nfs/2lx1x2x1/signal/skim/single/"
    output_dir = "/afs/desy.de/user/n/nissanuv/nfs/2lx1x2x1/signal/skim/sum"
    if sam:
        skim_dir = "/afs/desy.de/user/n/nissanuv/nfs/2lx1x2x1/signal/skim_sam/single/"
        output_dir = "/afs/desy.de/user/n/nissanuv/nfs/2lx1x2x1/signal/skim_sam/sum"
elif no_lepton_selection:
    skim_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_nlp/single/"
    output_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim_nlp/sum"

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

files = glob(skim_dir + "/*higgsino*");

if jecup: thing2grab = 'JecUp'
elif jecdown: thing2grab = 'JecDown'
else: thing2grab = 'Tree.roo'

points = {}

def chunker_longest(iterable, chunksize):
    return itertools.zip_longest(*[iter(iterable)] * chunksize)

for f in files:
    point = None
    if sam or phase1 or phase1_2018:
        if phase1 or phase1_2018:
            point = "_".join(os.path.basename(f).split("_")[3:5])
        else:
            point = "_".join(os.path.basename(f).split("_")[2:4])
    else:
        point = "_".join(os.path.basename(f).split("_")[0:3])
    if points.get(point) is None:
        points[point] = 1
    else:
        points[point] += 1

print(points)

default_file_num = 2

chunk_size = default_file_num

if slim or sam:
    chunk_size = 10000

for point in points:
    #print('point', point)
    #if not 'mChipm100GeV_dm6p26GeV' in point: continue
    point_files = sorted(glob(skim_dir + "/*" + point + "*"+thing2grab+"*"))
    print("\n\n\n\npoint=" + point)
    print("size=" + str(len(point_files)))
    
    i = 1
    
    for chunk in chunker_longest(point_files, chunk_size):
        output_file = output_dir + "/" + point + "_" + str(i) + ".root"
        if jecup: output_file = output_file.replace('.root','_JecUp.root')
        if jecdown: output_file = output_file.replace('.root','_JecDown.root') 
    
        if os.path.exists(output_file):
            print("File", output_file, " exists. Skipping")
            break
        else:
            files_list = " ".join([f for f in chunk if f is not None])
            command = "python ahadd.py -f " + output_file + " " + files_list
            print("Running cmd: " + command)
            i += 1
            system(command)

exit(0)




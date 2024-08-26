#!/usr/bin/env python

from ROOT import *
from glob import glob
from math import *
from sys import exit
from array import array
from os import system
import argparse
import os
import sys

ntuples_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/ntuples/single"
output_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/ntuples_sum/"

SUM_SIZE = 30

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

files = glob(ntuples_dir + "/higgsino*");

points = {}

for f in files:
    point = "_".join(os.path.basename(f).split("_")[0:3])
    if points.get(point) is None:
        points[point] = 1
    else:
        points[point] += 1

print(points)

for point in points:
    point_files = glob(ntuples_dir + "/" + point + "*")
    point_files.sort()
    print("point=" + point)
    print("size=" + str(len(point_files)))
    i = 0
    firstElement = 0
    lastElement = 0
    while(lastElement != -1):
        lastElement = (i+1)*SUM_SIZE + 1
        if lastElement > len(point_files):
            lastElement = -1
        print("Taking slice " + str(firstElement) + ":" + str(lastElement))
        slice = None
        if lastElement == -1:
            slice = point_files[firstElement:]
        else:
            slice = point_files[firstElement:lastElement]
        #print(slice)
        
        i += 1
        
        cmd = "hadd -f " + output_dir + "/" + point + "_" + str(i) + ".root " + " ".join(slice)
        print("Running cmd: " + cmd)
        system(cmd)
        firstElement = lastElement


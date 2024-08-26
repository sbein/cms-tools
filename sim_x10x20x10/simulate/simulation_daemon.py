#!/usr/bin/env python

from sys import exit
from os import system
from datetime import datetime
import argparse
import commands
import sys
import time
import os
import socket
import shutil

scripts_dir = "/afs/desy.de/user/n/nissanuv/cms-tools/sim_x10x20x10/simulate/"
output_dir = "/afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/"
logfile = scripts_dir + "daemon_log"
killfile = scripts_dir + "daemon_kill"

sleep_interval = 300

STATES = ["DEF","AOD","MINIAOD","NTPULES"]

####### CMDLINE ARGUMENTS #########

parser = argparse.ArgumentParser(description='ROC Comparison.')
parser.add_argument('-s', '--state', nargs=1, help='Starting State', required=True)
args = parser.parse_args()

state = args.state[0]

if state not in STATES:
    print("No such state: " + state)
    exit(1)

def createDef():
    log("In createDef.")
    log("Deleteing " + output_dir + "config")
    if os.path.exists(output_dir + "config"):
        shutil.rmtree(output_dir + "config")
    os.system(scripts_dir + "create_def.sh")

def createAod():
    log("In createAod.")
    log("Deleteing " + output_dir + "aod")
    if os.path.exists(output_dir + "aod"):
        shutil.rmtree(output_dir + "aod")
    os.system(scripts_dir + "create_aod.sh")

def createMiniaod():
    log("In createMiniaod.")
    log("Deleteing " + output_dir + "miniaod")
    if os.path.exists(output_dir + "miniaod"):
        shutil.rmtree(output_dir + "miniaod")
    os.system(scripts_dir + "create_miniaod.sh")

def createNtuples():
    log("In createNtuples.")
    os.system(scripts_dir + "create_ntuples.sh")

STATES_FUNCS = {
    "DEF" : createDef,
    "AOD" : createAod,
    "MINIAOD" : createMiniaod,
    "NTPULES" : createNtuples
}

logFile = open(logfile, 'a+')
logFile.write("\n\n\n")

queued_jobs = False

def log(str):
    logFile.write(time.ctime() + ": " + str + "\n")
    logFile.flush()
    
def waitForJobs(firstStep = False):
    global queued_jobs
    counter = 0
    while(True):
        if os.path.exists(killfile):
            log("Found kill file. Exiting...")
            exit(0)
        log("Checking running jobs...")
        status, out = commands.getstatusoutput('condor_q | grep \'nissanuv ID\'')
        if status == 0:
            log("Found running jobs. Sleeping for " + str(sleep_interval) + "...")
            queued_jobs = True
            log(out)
            counter += 1
            time.sleep(sleep_interval)
        else:
            log("No running jobs.")
            if firstStep or queued_jobs:
                break
            else:
                log("Jobs not queued yet... Sleeping for " + str(sleep_interval) + "...")
                time.sleep(sleep_interval)
    return counter

def advanceState():
    global state
    global STATES
    global queued_jobs
    if os.path.exists(killfile):
        log("Found kill file. Exiting...")
        exit(0)
    log("Finished state " + state)
    inx = STATES.index(state)
    if inx == len(STATES) - 1:
        log("Last step! Exiting...")
        exit(0)
        inx = 0
    else:
        inx += 1
    state = STATES[inx]
    log("New state " + state)
    
def performState():
    global state
    global queued_jobs
    queued_jobs = False
    if os.path.exists(killfile):
        log("Found kill file. Exiting...")
        exit(0)
    log("Performing state " + state)
    STATES_FUNCS[state]()

def main():
    global state
    global queued_jobs
    log("Simulation Daemon started.")
    log("Running on " + socket.gethostname())
    log("Current state: " + state)
    counter = waitForJobs()
    if counter > 0:
        advanceState()
    while(True):
        performState()
        waitForJobs()
        advanceState()
main()

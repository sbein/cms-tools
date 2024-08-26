from Condor.Production.jobSubmitter import *
from glob import glob
import os
import time
import commands

#slimmedProductionPath = "srm://dcache-se-cms.desy.de/pnfs/desy.de/cms/tier2/store/user/ynissan/NtupleHub/SlimmedProduction/"
slimmedProductionPath = "xroot://dcache-cms-xrootd.desy.de/pnfs/desy.de/cms/tier2/store/user/ynissan/NtupleHub/SlimmedProduction/"
leptonCollectionPath = "xroot://dcache-cms-xrootd.desy.de/pnfs/desy.de/cms/tier2/store/user/ynissan/NtupleHub/LeptonCollection/"
#root://dcache-cms-xrootd.desy.de
#leptonCollectionPath = "srm://dcache-se-cms.desy.de/pnfs/desy.de/cms/tier2/store/user/ynissan/NtupleHub/tmp/"

class jobSubmitterLC(jobSubmitter):
    def __init__(self,argv=None,parser=None):
        super(jobSubmitterLC,self).__init__(argv, parser)
        self.scripts = ["step1.sh","step2_lc.sh"]
        
    def addExtraOptions(self,parser):
        super(jobSubmitterLC,self).addExtraOptions(parser)
        parser.add_option("-N", "--nFiles", dest="nFiles", default=1, help="number of files to process (default = %default)")
        parser.add_option("-J", "--nFilesPerJob", dest="nFilesPerJob", default=1, help="number of files to process per job (default = %default)")
        parser.add_option("-o", "--output", dest="output", default="", help="path to output directory in which root files will be stored (required) (default = %default)")
        parser.add_option("-i", "--input", dest="input", default=slimmedProductionPath, help="input path to directory (default = %default)")
        parser.add_option("-d", "--dicts", dest="dicts", type="string", action="callback", callback=list_callback, default=None,
            help="comma-separated list of input sample names (default = %default)")
        parser.add_option("-F", "--fileList", dest="fileList", type="string", action="callback", callback=list_callback, default=None,
            help="comma-separated list of input files (default = %default)")
    
    def checkExtraOptions(self,options,parser):
        super(jobSubmitterLC,self).checkExtraOptions(options,parser)
        
        if len(options.output)==0:
            options.output = "srm://dcache-se-cms.desy.de:8443//pnfs/desy.de/cms/tier2/store/user/ynissan/NtupleHub/LeptonCollection/"
            #options.output = "xroot://dcache-cms-xrootd.desy.de//pnfs/desy.de/cms/tier2/store/user/ynissan/NtupleHub/LeptonCollection/"
            #options.output = "srm://dcache-se-cms.desy.de:8443//pnfs/desy.de/cms/tier2/store/user/ynissan/NtupleHub/tmp/"
    
    def generateExtra(self,job):
        super(jobSubmitterLC,self).generateExtra(job)
        job.patterns.update([
            ("JOBNAME",job.name+"_$(Process)_$(Cluster)"),
            ("EXTRAINPUTS","input/args_"+job.name+"_$(Process).txt"),
            #("EXTRAARGS","-j "+job.name+" -p $(Process) -o "+self.output + " -i " + "srm://dcache-se-cms.desy.de/pnfs/desy.de/cms/tier2/store/user/ynissan/NtupleHub/SlimmedProduction/"),
            ("EXTRAARGS","-j "+job.name+" -p $(Process) -o "+self.output + " -i " + "xroot://dcache-cms-xrootd.desy.de//pnfs/desy.de/cms/tier2/store/user/ynissan/NtupleHub/SlimmedProduction/"),
        ])
#("EXTRAARGS","-j "+job.name+" -p $(Process) -o "+self.output + " -i " + "root://dcache-cms-xrootd.desy.de//pnfs/desy.de/cms/tier2/store/user/ynissan/NtupleHub/SlimmedProduction/"),
    
    def generateSubmissionForFiles(self, job, files):
        # write job options to file - will be transferred with job
        if self.prepare:
            jname = job.makeName(job.nums[-1])
            args=""
            for file in files:
                args += file + " "
            with open("input/args_"+jname+".txt",'w') as argfile:
                argfile.write(args)
    
    def generateSubmission(self):
        # create protojob
        
        self.nFiles = int( self.nFiles )
        self.nFilesPerJob = int( self.nFilesPerJob )
        
        job = protoJob()
        job.name = "leptonCollection"
        self.generatePerJob(job)
        print("Wanted dicts", self.dicts)
        print("Wanted files", self.fileList)
        self.timenow = int(time.time())
        files = []
        nFiles = 0
        if self.fileList is None or len(self.fileList) == 0:
            print("Getting files in SlimmedProduction...", self.input)
            status, out = commands.getstatusoutput('eval `scram unsetenv -sh`; gfal-ls ' + self.input)
            #out = "Run2016H-17Jul2018-v1.SingleElectron_FCB308E4-E88A-E811-93CB-1866DA890A68.root"
            print(out)
            print("Getting files existing in LeptonCollection...", leptonCollectionPath)
            status, existingOut = commands.getstatusoutput('eval `scram unsetenv -sh`;gfal-ls ' + leptonCollectionPath)
            existingFiles = existingOut.split("\n")
            #existingFiles = []
            print(existingFiles)
            
            for file in out.split("\n"):
                #print("checking", file)
                if file in existingFiles:
                    #print("File", file, " alreading exists. Skipping.")
                    continue
                if self.dicts is not None and len(self.dicts) > 0:
                    shouldProcess = False
                    for dict in self.dicts:
                        if dict in file:
                            shouldProcess = True
                            break
                    if not shouldProcess:
                        continue
                print("Adding file=" + file)
                files.append(file)
                nFiles += 1
                print("len(files)", len(files), "self.nFilesPerJob", self.nFilesPerJob, "nFiles", nFiles, "self.nFiles", self.nFiles)
                if len(files) < self.nFilesPerJob and nFiles < self.nFiles:
                    print("***")
                    continue
                print("----")
                print("Adding job...")
            
                job.njobs += 1
                if self.count and not self.prepare:
                    files = []
                    if nFiles >= self.nFiles:
                        break
                    continue
                job.nums.append(job.njobs-1)
                # just keep list of jobs
                if self.missing and not self.prepare:
                    files = []
                    if nFiles >= self.nFiles:
                        break
                    continue
            
                self.generateSubmissionForFiles(job, files)
                files = []
                if nFiles >= self.nFiles:
                    break
        else:
            for file in self.fileList:
                print("Adding file=" + file)
                files.append(file)
                nFiles += 1
                job.njobs += 1
                job.nums.append(job.njobs-1)
                self.generateSubmissionForFiles(job, files)
        if len(files) > 0 and (self.fileList is None or len(self.fileList) == 0):
            print("---- REMAINING JOBS")
            print("Adding job...")
            job.njobs += 1
            job.nums.append(job.njobs-1)
            self.generateSubmissionForFiles(job, files)
        
        job.queue = "-queue "+str(job.njobs)
        print("Job queue", job.queue)
        self.protoJobs.append(job)
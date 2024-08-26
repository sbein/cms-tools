from Condor.Production.jobSubmitter import *
from glob import glob
import os
import time
import commands

slimmedProductionPath = "srm://dcache-se-cms.desy.de/pnfs/desy.de/cms/tier2/store/user/ynissan/NtupleHub/SlimmedProduction/"

class jobSubmitterTest(jobSubmitter):
    def __init__(self,argv=None,parser=None):
        super(jobSubmitterTest,self).__init__(argv, parser)
        self.scripts = ["step1.sh","step2_test.sh"]
        
    def addExtraOptions(self,parser):
        super(jobSubmitterTest,self).addExtraOptions(parser)
        parser.add_option("-N", "--nFiles", dest="nFiles", default=1, help="number of files to process (default = %default)")
        parser.add_option("-J", "--nFilesPerJob", dest="nFilesPerJob", default=1, help="number of files to process per job (default = %default)")
        parser.add_option("-o", "--output", dest="output", default="", help="path to output directory in which root files will be stored (required) (default = %default)")
        parser.add_option("-i", "--input", dest="input", default=slimmedProductionPath, help="input path to directory (default = %default)")
        parser.add_option("-d", "--dicts", dest="dicts", type="string", action="callback", callback=list_callback, default=None,
            help="comma-separated list of input sample names (default = %default)")
    
    def checkExtraOptions(self,options,parser):
        super(jobSubmitterTest,self).checkExtraOptions(options,parser)
        
        if len(options.output)==0:
            options.output = "srm://dcache-se-cms.desy.de/pnfs/desy.de/cms/tier2/store/user/ynissan/NtupleHub/LeptonCollection/"
    
    def generateExtra(self,job):
        super(jobSubmitterTest,self).generateExtra(job)
        job.patterns.update([
            ("JOBNAME",job.name+"_$(Process)_$(Cluster)"),
            ("EXTRAINPUTS","input/args_"+job.name+"_$(Process).txt"),
            ("EXTRAARGS","-j "+job.name+" -p $(Process) -o "+self.output + " -i " + "srm://dcache-se-cms.desy.de/pnfs/desy.de/cms/tier2/store/user/ynissan/NtupleHub/SlimmedProduction/"),
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
        
        job = protoJob()
        job.name = "test"
        self.generatePerJob(job)
        job.njobs += 1
        if not (self.count and not self.prepare):
            job.nums.append(job.njobs-1)
            if not (self.missing and not self.prepare):
                if self.prepare:
                    jname = job.makeName(job.nums[-1])
                    with open("input/args_"+jname+".txt",'w') as argfile:
                        args = "test"
                        argfile.write(args)
        
        job.queue = "-queue "+str(job.njobs)
        print("Job queue", job.queue)
        self.protoJobs.append(job)
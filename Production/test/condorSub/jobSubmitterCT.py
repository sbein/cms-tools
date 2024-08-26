from Condor.Production.jobSubmitter import *
from glob import glob
import os
import time
import commands

defaultModeLocations = {
    "def" : "srm://dcache-se-cms.desy.de/pnfs/desy.de/cms/tier2/store/user/ynissan/NtupleHub/def/",
    "aod" : "srm://dcache-se-cms.desy.de/pnfs/desy.de/cms/tier2/store/user/ynissan/NtupleHub/aod/"
}

defaultFileLocations = {
    "def" : "root://dcache-cms-xrootd.desy.de//pnfs/desy.de/cms/tier2/store/user/ynissan/NtupleHub/def/",
    "aod" : "root://dcache-cms-xrootd.desy.de//pnfs/desy.de/cms/tier2/store/user/ynissan/NtupleHub/aod/"
}


class jobSubmitterCT(jobSubmitter):
    def addExtraOptions(self,parser):
        super(jobSubmitterCT,self).addExtraOptions(parser)
        self.removeOptions(parser,"-m")
        parser.add_option("-m", "--mode", dest="mode", default="", help="mode to run (required) (default = %default)")
        parser.add_option("-o", "--output", dest="output", default="", help="path to output directory in which root files will be stored (required) (default = %default)")
    
    def checkExtraOptions(self,options,parser):
        super(jobSubmitterCT,self).checkExtraOptions(options,parser)
        
        if len(options.mode)==0 or options.mode not in ("def", "aod", "miniaod", "ntuples"):
            parser.error("Required option: --mode [mode]")
        
        if len(options.output)==0:
            options.output = defaultModeLocations[options.mode]
    
    def generateExtra(self,job):
        super(jobSubmitterCT,self).generateExtra(job)
        job.patterns.update([
            ("JOBNAME",job.name+"_$(Process)_$(Cluster)"),
            ("EXTRAINPUTS","input/args_"+job.name+"_$(Process).txt"),
            ("EXTRAARGS","-j "+job.name+" -p $(Process) -o "+self.output + " -m " + self.mode),
        ])
        job.appends.append(
                'requirements = (OpSysAndVer =?= "CentOS6")\n'
                '+SingularityAutoLoad = False\n'
            )
    
    def generateSubmission(self):
        # create protojob
        job = protoJob()
        job.name = self.mode
        self.generatePerJob(job)
        
        self.timenow = int(time.time())
        if self.mode == "def":
            modelLocation = os.path.expandvars("$CMSSW_BASE/src/Configuration/Generator/python")
            for file in glob(modelLocation + "/higgsino*.py"):
                print("Adding job for file=" + file)
                job.njobs += 1
                if self.count and not self.prepare:
                    continue
                job.nums.append(job.njobs-1)
                # just keep list of jobs
                if self.missing and not self.prepare:
                    continue
            
                # write job options to file - will be transferred with job
                if self.prepare:
                    jname = job.makeName(job.nums[-1])
                    with open("input/args_"+jname+".txt",'w') as argfile:
                        id = str(self.timenow) + str(job.njobs)
                        basename = os.path.basename(file)
                        cff_file = os.path.splitext(basename)[0]
                        base = basename.split("_cff.py")[0]
                        config_out = base + "_" + id + ".py"
                        file_out = base + "_" + id + "_AOD.root"
                        args = cff_file + " " + config_out + " " + file_out
                        argfile.write(args)
        elif self.mode == "aod":
            status, out = commands.getstatusoutput('gfal-ls ' + defaultModeLocations['def'])
            for file in out.split("\n"):
                print("Adding job for file=" + file)
                job.njobs += 1
                if self.count and not self.prepare:
                    continue
                job.nums.append(job.njobs-1)
                # just keep list of jobs
                if self.missing and not self.prepare:
                    continue
            
                # write job options to file - will be transferred with job
                if self.prepare:
                    jname = job.makeName(job.nums[-1])
                    with open("input/args_"+jname+".txt",'w') as argfile:
                        id = file.split("_")[-1].split(".")[0]
                        basename = os.path.basename(file)
                        config_out = defaultModeLocations['def'] + "/" + file
                        args = config_out
                        argfile.write(args)
        
        job.queue = "-queue "+str(job.njobs)
        print("Job queue", job.queue)
        self.protoJobs.append(job)
#!/bin/bash

#shopt -s nullglob

# necessary for running cmsenv
#shopt -s expand_aliases

OLD_PWD=$PWD

echo OLD_PWD=$PWD

# CMS ENV
#cd ~/CMSSW_11_3_1/src
cd /nfs/dust/cms/user/beinsam/NaturalSusy/CMSSW_13_3_3/src/

export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh

#cmsenv
eval `scramv1 runtime -sh`

echo CMSSW_BASE=$CMSSW_BASE

. "$CMSSW_BASE/src/cms-tools/lib/def.sh"
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$CMSSW_BASE/src/cms-tools/lib/classes"

cd $OLD_PWD

echo Running:
echo $@

$@

exit_code=$?
echo Output Code: $exit_code
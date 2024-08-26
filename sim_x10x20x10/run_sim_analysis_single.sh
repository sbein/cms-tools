#!/bin/bash

shopt -s nullglob

#---------- GET OPTIONS ------------
POSITIONAL=()
INPUT_FILES=()
while [[ $# -gt 0 ]]
do
    key="$1"

    case $key in
        -i|--input)
        #INPUT_FILES+=("$2") # Add the file to the array
        OLD_IFS="$IFS"
        IFS=',' read -r -a INPUT_FILES <<< "$2"
        # Restore the original IFS
        IFS="$OLD_IFS"
        shift # past argument
        shift # past value
        ;;
        -skim|--skim)
        SKIM=true
        shift # past argument
        ;;
        *)    # unknown option
        POSITIONAL+=("$1") # save it in an array for later
        shift # past argument
        ;;
    esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters
#---------- END OPTIONS ------------

# necessary for running cmsenv
shopt -s expand_aliases

# CMS ENV
#cd /nfs/dust/cms/user/beinsam/NaturalSusy/CMSSW_11_3_1/src/
cd /nfs/dust/cms/user/beinsam/NaturalSusy/CMSSW_13_3_3/src/

#singularity exec --contain --bind /afs:/afs --bind /nfs:/nfs --bind /pnfs:/pnfs --bind /cvmfs:/cvmfs --bind /var/lib/condor:/var/lib/condor --bind "$(pwd):$(pwd)" --pwd "$(pwd)" /cvmfs/unpacked.cern.ch/registry.hub.docker.com/cmssw/cc7:amd64 bash -c "exec bash"

export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh


cmsenv

. "$CMSSW_BASE/src/cms-tools/lib/def.sh"
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$CMSSW_BASE/src/cms-tools/lib/classes"
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/nfs/dust/cms/user/beinsam/NaturalSusy/CMSSW_13_3_3/src/cms-tools/lib/classes"

SCRIPT_PATH=$ANALYZER_PATH
if [ -n "$SKIM" ]; then
    echo "GOT SKIM"
    SCRIPT_PATH=$SKIMMER_PATH
fi

# Process each input filee
echo "gonna process these " $INPUT_FILES
for file in "${INPUT_FILES[@]}"; do
    #echo "Processing file: $file"
    echo $SCRIPT_PATH -i "$file" ${POSITIONAL[@]}
    $SCRIPT_PATH -i "$file" ${POSITIONAL[@]}
done

#!/bin/bash

. "$CMSSW_BASE/src/cms-tools/lib/def.sh"

shopt -s nullglob
shopt -s expand_aliases

#---------- GET OPTIONS ------------
POSITIONAL=()
while [[ $# -gt 0 ]]
do
    key="$1"

    case $key in
        -sc)
        SC=true
        POSITIONAL+=("$1")
        shift
        ;;
        -dy)
        DRELL_YAN=true
        POSITIONAL+=("$1")
        shift
        ;;
        --jpsi_muons)
        JPSI_MUONS=true
        POSITIONAL+=("$1")
        shift
        ;;
        --phase1)
        PHASE1=true
        POSITIONAL+=("$1")
        shift
        ;;
        --onphase0 )
        ONPHASE0=true
        POSITIONAL+=("$1")
        shift
        ;;
        *)    # unknown option
        POSITIONAL+=("$1") # save it in an array for later
        shift # past argument
        ;;
    esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters
#---------- END OPTIONS ------------

# CMS ENV
cd $CMS_WD
. /etc/profile.d/modules.sh
module use -a /afs/desy.de/group/cms/modulefiles/
module load cmssw
cmsenv

BDT_DIR=$OUTPUT_WD/cut_optimisation/tmva/dilepton_bdt
COMMAND=$SCRIPTS_WD/skimmer_x1x2x1_dilepton_bdt.py

if [ -n "$DRELL_YAN" ]; then
    echo "GOT DY"
    echo "HERE: $@"
    INPUT_DIR=$DY_SKIM_OUTPUT_DIR
elif [ -n "$JPSI_MUONS" ]; then
    INPUT_DIR=$SKIM_MASTER_OUTPUT_DIR
    BDT_DIR=$SKIM_MASTER_OUTPUT_DIR/split/tmva
    COMMAND=$SCRIPTS_WD/skimmer_jpsi_bdt.py
elif [ -n "$PHASE1" ]; then
    INPUT_DIR=$SKIM_PHASE1_OUTPUT_DIR
    BDT_DIR=$OUTPUT_WD/cut_optimisation/tmva/dilepton_bdt_phase1
elif [ -n "$ONPHASE0" ]; then
    INPUT_DIR=$SKIM_OUTPUT_DIR
    BDT_DIR=$OUTPUT_WD/cut_optimisation/tmva/dilepton_bdt_phase1
else
    if [ -n "$SC" ]; then
        echo "GOT SC"
        echo "HERE: $@"
        INPUT_DIR=$SKIM_BG_SIG_BDT_SC_OUTPUT_DIR
    else
        INPUT_DIR=$SKIM_OUTPUT_DIR
    fi
fi

echo INPUT_DIR=$INPUT_DIR
echo BDT_DIR=$BDT_DIR

timestamp=$(date +%Y%m%d_%H%M%S%N)
output_file="${WORK_DIR}/condor_submut.${timestamp}"
echo "output file: $output_file"

#request_memory = 16 GB
#

cat << EOM > $output_file
universe = vanilla
should_transfer_files = IF_NEEDED
executable = /bin/bash
notification = Never
+RequestRuntime = 86400
EOM

FILES=$INPUT_DIR/sum/type_sum/*
#FILES=$INPUT_DIR/sum/type_sum/WZTo3LNu_mllmin01*
#FILES=(ZJetsToNuNu_HT-400To600_13TeV-madgraph_1.root TTJets_DiLept_TuneCUETP8M1_9.root TTJets_SingleLeptFromT_TuneCUETP8M1_1.root WJetsToLNu_HT-1200To2500_TuneCUETP8M1_2.root ZJetsToNuNu_HT-400To600_13TeV-madgraph_2.root)
#FILES=(TTJets_SingleLeptFromT_TuneCUETP8M1_15.root ZJetsToNuNu_HT-400To600_13TeV-madgraph_4.root)
#FILES=(QCD_HT2000toInf_TuneCUETP8M1_34.root QCD_HT1500to2000_TuneCUETP8M1_16.root)


#FILES=(QCD_HT300to500_TuneCUETP8M1_3.root ST_t-channel_antitop_1.root)

for bg_file in ${FILES[@]}; do
    #bg_file=$INPUT_DIR/sum/type_sum/$bg_file
    cmd="$CONDOR_WRAPPER $COMMAND -i $bg_file -bdt $BDT_DIR -bg $@"
    bg_file_name=$(basename $bg_file .root)
    echo $cmd
    # echo INPUT_DIR = $INPUT_DIR
#     echo err = ${INPUT_DIR}/stderr/${bg_file_name}_dilepton.err
#     echo output = ${INPUT_DIR}/stdoutput/${bg_file_name}_dilepton.output
cat << EOM >> $output_file
arguments = $cmd
error = ${INPUT_DIR}/stderr/${bg_file_name}_dilepton.err
log = ${INPUT_DIR}/stderr/${bg_file_name}_dilepton.log
output = ${INPUT_DIR}/stdoutput/${bg_file_name}_dilepton.output
Queue
EOM
    
done
echo would tend to do: condor_submit $output_file
#condor_submit $output_file
#rm $output_file

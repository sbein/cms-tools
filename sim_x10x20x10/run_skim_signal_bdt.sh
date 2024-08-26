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
        --sam)
        SAM=true
        POSITIONAL+=("$1")
        shift
        ;;
        --phase1)
        PHASE1=true
        POSITIONAL+=("$1")
        shift
        ;;
        --phase1_2018)
        PHASE1_2018=true
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

#OUTPUT_DIR=$SKIM_SIG_BDT_OUTPUT_DIR
INPUT_DIR=$SKIM_SIG_OUTPUT_DIR
TRACK_SPLIT_DIR=$LEPTON_TRACK_SPLIT_DIR
#OUTPUT_DIR="$OUTPUT_WD/signal/skim_signal_bdt_tighter"

#if [ -n "$SC" ]; then
#     echo "GOT SC"
#     echo "HERE: $@"
#     OUTPUT_DIR=$SKIM_SIG_BDT_SC_OUTPUT_DIR
# fi

if [ -n "$SAM" ]; then
    echo "GOT SAM"
    echo "HERE: $@"
    INPUT_DIR=$SKIM_SIG_SAM_OUTPUT_DIR
    #OUTPUT_DIR=$SKIM_SAM_SIG_BDT_OUTPUT_DIR
elif [ -n "$PHASE1" ]; then
    echo "GOT PHASE1"
    echo "HERE: $@"
    INPUT_DIR=$SKIM_SIG_PHASE1_OUTPUT_DIR
    TRACK_SPLIT_DIR=$LEPTON_TRACK_PHASE1_SPLIT_DIR
elif [ -n "$PHASE1_2018" ]; then
    echo "GOT PHASE1 2018"
    echo "HERE: $@"
    INPUT_DIR=$SKIM_SIG_PHASE1_2018_OUTPUT_DIR
    TRACK_SPLIT_DIR=$LEPTON_TRACK_PHASE1_SPLIT_DIR
fi

timestamp=$(date +%Y%m%d_%H%M%S%N)
output_file="${WORK_DIR}/condor_submut.${timestamp}"
echo "output file: $output_file"

cat << EOM > $output_file
universe = vanilla
should_transfer_files = IF_NEEDED
executable = /bin/bash
notification = Never
+RequestRuntime = 86400
request_memory = 16 GB
EOM


echo -e "\n\nRUNNING ALL GROUP\n\n"


if [ -n "$SAM" ] || [ -n "$PHASE1" ] || [ -n "$PHASE1_2018" ]; then
    FILES=${INPUT_DIR}/sum/*
else
    FILES=${INPUT_DIR}/single/*
fi

#FILES=(higgsino_mu115_dm9p82Chi20Chipm.root higgsino_mu115_dm7p44Chi20Chipm.root higgsino_mu130_dm7p49Chi20Chipm.root)

for sim in ${FILES[@]}; do
    #sim=${INPUT_DIR}/sum/$sim
    if [ -n "$SAM" ]; then
        filename=`echo $(basename $sim .root)`
    else
        #filename=`echo $(basename $sim .root) | awk -F"_" '{print $1"_"$2"_"$3}'`
        filename=`echo $(basename $sim .root)`
    fi
    echo $filename
    #tb=all
    echo "Will run:"
    #echo $CONDOR_WRAPPER $SCRIPTS_WD/skimmer_x1x2x1_univ_bdt_track_bdt.py -i $sim -o ${OUTPUT_DIR}/single/${filename}.root -tb $LEPTON_TRACK_SPLIT_DIR/cut_optimisation/tmva/$tb  -ub $OUTPUT_WD/cut_optimisation/tmva/total_bdt $@
    echo $CONDOR_WRAPPER $SCRIPTS_WD/skimmer_x1x2x1_track_bdt.py -i $sim -tb $TRACK_SPLIT_DIR/cut_optimisation/tmva --signal $@
cat << EOM >> $output_file
arguments = $CONDOR_WRAPPER $SCRIPTS_WD/skimmer_x1x2x1_track_bdt.py -i $sim -tb $TRACK_SPLIT_DIR/cut_optimisation/tmva --signal $@
error = ${INPUT_DIR}/stderr/${filename}_track_bdt.err
output = ${INPUT_DIR}/stdout/${filename}_track_bdt.output
log = ${INPUT_DIR}/stdout/${filename}_track_bdt.log
Queue
EOM
done

condor_submit $output_file
echo "log file: $output_file"
#rm $output_file

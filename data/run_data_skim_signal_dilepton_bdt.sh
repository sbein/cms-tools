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
        --tl)
        TWO_LEPTONS=true
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
        --onphase0)
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


BDT_DIR=$DILEPTON_BDT_DIR
COMMAND=$SCRIPTS_WD/skimmer_x1x2x1_dilepton_bdt.py
EXTRA_FLAGS=""


# if [ -n "$TWO_LEPTONS" ]; then
#     if [ -n "$SC" ]; then
#         echo "GOT SC"
#         echo "HERE: $@"
#         OUTPUT_DIR=$SKIM_TWO_LEPTONS_DATA_SIG_DILEPTON_BDT_SC_OUTPUT_DIR
#         INPUT_DIR=$TWO_LEPTONS_SAME_SIGN_SKIM_DATA_OUTPUT_DIR/sum
#     else
#         OUTPUT_DIR=$SKIM_TWO_LEPTONS_DATA_SIG_DILEPTON_BDT_OUTPUT_DIR
#         INPUT_DIR=$TWO_LEPTONS_SKIM_DATA_OUTPUT_DIR/sum
#     fi
#     BDT_DIR=$TWO_LEPTONS_OUTPUT_WD/cut_optimisation/tmva/dilepton_bdt
if [ -n "$DRELL_YAN" ]; then
    echo "GOT DY"
    echo "HERE: $@"
    #OUTPUT_DIR=$SKIM_DATA_SIG_DILEPTON_BDT_DY_OUTPUT_DIR
    INPUT_DIR=$DY_SKIM_DATA_OUTPUT_DIR
elif [ -n "$JPSI_MUONS" ]; then
    echo "GOT JPSI_MUONS"
    echo "HERE: $@"
    #OUTPUT_DIR=$SKIM_DATA_SIG_DILEPTON_BDT_DY_OUTPUT_DIR
    #INPUT_DIR=$SKIM_DATA_JPSI_MUONS_OUTPUT_DIR
    INPUT_DIR=$SKIM_DATA_MASTER_OUTPUT_DIR
    BDT_DIR=$SKIM_MASTER_OUTPUT_DIR/split/tmva
    COMMAND=$SCRIPTS_WD/skimmer_jpsi_bdt.py
elif [ -n "$PHASE1" ]; then
    echo "GOT PHASE1"
    echo "HERE: $@"
    INPUT_DIR=$SKIM_DATA_PHASE1_OUTPUT_DIR
    BDT_DIR=$DILEPTON_BDT_PHASE1_DIR
else
    if [ -n "$SC" ]; then
        echo "GOT SC"
        echo "HERE: $@"
        OUTPUT_DIR=$SKIM_DATA_SIG_DILEPTON_BDT_SC_OUTPUT_DIR
        INPUT_DIR=$SKIM_DATA_BDT_SC_OUTPUT_DIR
        
    else
        echo HERE
        
        #OUTPUT_DIR=$SKIM_DATA_BDT_OUTPUT_DIR
        INPUT_DIR=$SKIM_DATA_OUTPUT_DIR
        echo $INPUT_DIR/sum/
        if [ -n "$ONPHASE0" ]; then
            BDT_DIR=$DILEPTON_BDT_PHASE1_DIR
        fi
        
    fi
fi

#echo OUTPUT_DIR=$OUTPUT_DIR
echo INPUT_DIR=$INPUT_DIR

timestamp=$(date +%Y%m%d_%H%M%S%N)
output_file="${WORK_DIR}/condor_submut.${timestamp}"
echo "output file: $output_file"

#echo $OUTPUT_DIR
#check output directory
#if [ ! -d "$OUTPUT_DIR" ]; then
#  mkdir $OUTPUT_DIR
#fi

cat << EOM > $output_file
universe = vanilla
should_transfer_files = IF_NEEDED
executable = /bin/bash
notification = Never
priority = 0
request_memory = 16 GB
+RequestRuntime = 86400
EOM

#for sim in $SKIM_BG_SIG_BDT_OUTPUT_DIR/*; do
# for sim in $BDT_DIR/*; do    
#     filename=`echo $(basename $sim)`
#     echo $filename
#     tb=$filename

    # if [ ! -d "$OUTPUT_DIR/$tb" ]; then
#       mkdir $OUTPUT_DIR/$tb
#     fi
# 
#     #check output directory
#     if [ ! -d "$OUTPUT_DIR/$tb/single" ]; then
#       mkdir "$OUTPUT_DIR/$tb/single"
#     fi
# 
#     if [ ! -d "$OUTPUT_DIR/$tb/stdout" ]; then
#       mkdir "$OUTPUT_DIR/$tb/stdout" 
#     fi
# 
#     if [ ! -d "$OUTPUT_DIR/$tb/stderr" ]; then
#       mkdir "$OUTPUT_DIR/$tb/stderr"
#     fi
#     
#     if [ -n "$TWO_LEPTONS" ]; then
#         DATA_DIR=$INPUT_DIR
#     else
#         DATA_DIR=$INPUT_DIR/$tb/single
#     fi

echo $INPUT_DIR/sum/

FILES=$INPUT_DIR/sum/*_topup_*
#FILES=(Run2018A-17Sep2018-v1.METAOD_1843.root)
#FILES=(Run2018D-PromptReco-v2.METAOD_2235.root Run2018D-PromptReco-v2.METAOD_2236.root)

for data_file in ${FILES[@]}; do
#for data_file in $INPUT_DIR/sum/*; do
    #data_file=$INPUT_DIR/sum/$data_file
    echo "Will run:"
    data_file_name=$(basename $data_file .root)
        #out_file=${OUTPUT_DIR}/$tb/single/${data_file_name}.root
        #if [ -f "$out_file" ]; then
        #    echo "$out_file exist. Skipping..."
        #    continue
        #fi
    cmd="$CONDOR_WRAPPER $COMMAND --data -i $data_file -bdt $BDT_DIR $@"
    echo $cmd
cat << EOM >> $output_file
arguments = $cmd
error = ${INPUT_DIR}/stderr/${data_file_name}_dilepton_phase1.err
output = ${INPUT_DIR}/stdout/${data_file_name}_dilepton_phase1.output
Queue
EOM
done
#done

condor_submit $output_file
rm $output_file

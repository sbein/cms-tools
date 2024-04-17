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

timestamp=$(date +%Y%m%d_%H%M%S%N)
output_file="${WORK_DIR}/condor_submut.${timestamp}"
echo "output file: $output_file"

OUTPUT_DIR=$SKIM_DATA_BDT_OUTPUT_DIR
INPUT_DIR=$SKIM_DATA_OUTPUT_DIR
LEPTON_TRACK_DIR=$LEPTON_TRACK_SPLIT_DIR

if [ -n "$SC" ]; then
    echo "GOT SC"
    echo "HERE: $@"
    OUTPUT_DIR=$SKIM_DATA_BDT_SC_OUTPUT_DIR
elif [ -n "$DRELL_YAN" ]; then
    echo "GOT DY"
    echo "HERE: $@"
    OUTPUT_DIR=$SKIM_DATA_BDT_DY_OUTPUT_DIR
    INPUT_DIR=$DY_SKIM_DATA_OUTPUT_DIR
elif [ -n "$JPSI_MUONS" ]; then
    echo "GOT DY"
    echo "HERE: $@"
    INPUT_DIR=$SKIM_DATA_JPSI_MUONS_OUTPUT_DIR
elif [ -n "$PHASE1" ]; then
    echo "GOT PHASE1"
    echo "HERE: $@"
    INPUT_DIR=$SKIM_DATA_PHASE1_OUTPUT_DIR
    LEPTON_TRACK_DIR=$LEPTON_TRACK_PHASE1_SPLIT_DIR
fi




echo $OUTPUT_DIR
#check output directory
if [ ! -d "$OUTPUT_DIR" ]; then
  mkdir $OUTPUT_DIR
fi

cat << EOM > $output_file
universe = vanilla
should_transfer_files = IF_NEEDED
executable = /bin/bash
notification = Never
priority = 0
request_memory = 12 GB
+RequestRuntime = 86400
EOM

#FILES=(Run2016E-17Jul2018-v1.METAOD_17.root Run2016E-17Jul2018-v1.METAOD_18.root Run2016E-17Jul2018-v1.METAOD_20.root Run2016F-17Jul2018-v1.METAOD_21.root Run2016G-17Jul2018-v1.METAOD_28.root)

#for sim in $LEPTON_TRACK_DIR/cut_optimisation/tmva/*; do
#    echo $sim
#    filename=$(basename $sim)
#    echo $filename
    # if [ ! -d "$OUTPUT_DIR/$filename" ]; then
#       mkdir $OUTPUT_DIR/$filename
#     fi
# 
#     #check output directory
#     if [ ! -d "$OUTPUT_DIR/$filename/single" ]; then
#       mkdir "$OUTPUT_DIR/$filename/single"
#     fi
# 
#     if [ ! -d "$OUTPUT_DIR/$filename/stdout" ]; then
#       mkdir "$OUTPUT_DIR/$filename/stdout" 
#     fi
# 
#     if [ ! -d "$OUTPUT_DIR/$filename/stderr" ]; then
#       mkdir "$OUTPUT_DIR/$filename/stderr"
#     fi

    #for bg_file in $SKIM_OUTPUT_DIR/sum/type_sum/*ZJetsToNuNu_HT-100To200*; do
for data_file in $INPUT_DIR/sum/*_topup_*; do
    data_file_name=$(basename $data_file .root)
        # out_file=${OUTPUT_DIR}/$filename/single/${data_file_name}.root
#         if [ -f "$out_file" ]; then
#             echo "$out_file exist. Skipping..."
#             continue
#         fi
        echo "Will run:"
        echo $CONDOR_WRAPPER $SCRIPTS_WD/skimmer_x1x2x1_track_bdt.py -i $data_file -tb $LEPTON_TRACK_DIR/cut_optimisation/tmva $@
cat << EOM >> $output_file
arguments = $CONDOR_WRAPPER $SCRIPTS_WD/skimmer_x1x2x1_track_bdt.py -i $data_file -tb $LEPTON_TRACK_DIR/cut_optimisation/tmva $@
error = ${INPUT_DIR}/stderr/${data_file_name}_track_bdt.err
output = ${INPUT_DIR}/stdout/${data_file_name}_track_bdt.output
log = ${INPUT_DIR}/stdout/${data_file_name}_track_bdt.log
Queue
EOM
    #done
done

condor_submit $output_file
rm $output_file

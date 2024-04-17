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
        --tl)
        TWO_LEPTONS=true
        POSITIONAL+=("$1")
        shift
        ;;
        --dy)
        DRELL_YAN=true
        POSITIONAL+=("$1")
        shift
        ;;
        --jpsi_muons)
        JPSI_MUONS=true
        POSITIONAL+=("$1")
        shift
        ;;
        --sc)
        SAME_SIGN=true
        POSITIONAL+=("$1")
        shift
        ;;
        --master)
        MASTER=true
        POSITIONAL+=("$1")
        shift
        ;;
        --phase1)
        PHASE1=true
        POSITIONAL+=("$1")
        shift
        ;;
        --jpsi_single_electron)
        JPSI_SINGLE_ELECTRON=true
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

OUTPUT_DIR=$SKIM_DATA_OUTPUT_DIR/sum
INPUT_DIR=$SKIM_DATA_OUTPUT_DIR/single
pattern="METAOD"
if [ -n "$TWO_LEPTONS" ]; then
        if [ -n "$SAME_SIGN" ]; then
            OUTPUT_DIR=$TWO_LEPTONS_SAME_SIGN_SKIM_DATA_OUTPUT_DIR/sum
            INPUT_DIR=$TWO_LEPTONS_SAME_SIGN_SKIM_DATA_OUTPUT_DIR/single
        else
            OUTPUT_DIR=$TWO_LEPTONS_SKIM_DATA_OUTPUT_DIR/sum
            INPUT_DIR=$TWO_LEPTONS_SKIM_DATA_OUTPUT_DIR/single
        fi
elif [ -n "$DRELL_YAN" ]; then
    pattern="SingleMuonAOD"
    OUTPUT_DIR=$DY_SKIM_DATA_OUTPUT_DIR/sum
    INPUT_DIR=$DY_SKIM_DATA_OUTPUT_DIR/single
elif [ -n "$JPSI_MUONS" ]; then
    pattern="SingleMuonAOD"
    INPUT_DIR=$SKIM_DATA_JPSI_MUONS_OUTPUT_DIR/single
    OUTPUT_DIR=$SKIM_DATA_JPSI_MUONS_OUTPUT_DIR/sum
elif [ -n "$MASTER" ]; then
    pattern="SingleMuonAOD"
    INPUT_DIR=$SKIM_DATA_MASTER_OUTPUT_DIR/single
    OUTPUT_DIR=$SKIM_DATA_MASTER_OUTPUT_DIR/sum
elif [ -n "$JPSI_SINGLE_ELECTRON" ]; then
    pattern="SingleElectronAOD"
    INPUT_DIR=$SKIM_DATA_JPSI_SINGLE_ELECTRON_OUTPUT_DIR/single
    OUTPUT_DIR=$SKIM_DATA_JPSI_SINGLE_ELECTRON_OUTPUT_DIR/sum
elif [ -n "$PHASE1" ]; then
    OUTPUT_DIR=$SKIM_DATA_PHASE1_OUTPUT_DIR/sum
    INPUT_DIR=$SKIM_DATA_PHASE1_OUTPUT_DIR/single
fi



count=0
input_files=""
files_per_job=20
output_count=1
lastfile=""
run_sums=""


if [ -n "$PHASE1" ]; then
    files_per_job=25
    #run_sums=`ls -1 $INPUT_DIR/ | awk -F"-" '{print $1}' | sort | uniq`
    run_sums=`ls -l $INPUT_DIR/ | grep -v '  2022 ' | awk -F" " '{print $9}' | grep -v "^$" | awk -F"-" '{print $1}' | sort | uniq`
fi

#mkdir $OUTPUT_DIR

#for run in $run_sums; do
for run in "$run_sums"; do
    echo Running for run $run
    #for fullname in $INPUT_DIR/${run}*; do
    for fullname in `ls -l $INPUT_DIR/ | grep -v '  2022 ' | grep "$run" | awk -F" " '{print $9}' | grep -v "^$"`; do
        lastfile=$fullname
        input_files="$input_files $INPUT_DIR/$fullname"
        ((count+=1))
        if [ $(($count % $files_per_job)) == 0 ]; then
            output_name=`echo $(basename $fullname .root) | awk -F"$pattern" "{print \\$1\"${pattern}_topup_${output_count}.root\"}"`
            ((output_count+=1))
            echo hadd -f $OUTPUT_DIR/$output_name $input_files
            hadd -f $OUTPUT_DIR/$output_name $input_files
            echo -e "\n\n\n\n\n\n\n"
            #echo rm $input_files
            #rm $input_files
            echo -e "\n\n\n\n\n\n\n"
            input_files=""
        fi
    done

    if [ $(($count % $files_per_job)) != 0 ]; then
        output_name=`echo $(basename $lastfile .root) | awk -F"$pattern" "{print \\$1\"${pattern}_topup_${output_count}.root\"}"`
        ((output_count+=1))
        echo hadd -f $OUTPUT_DIR/$output_name $input_files
        hadd -f $OUTPUT_DIR/$output_name $input_files
        echo -e "\n\n\n\n\n\n\n"
        #echo rm $input_files
        #rm $input_files
        echo -e "\n\n\n\n\n\n\n"
        input_files=""
    fi
done


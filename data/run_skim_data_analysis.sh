#!/bin/bash

. "$CMSSW_BASE/src/cms-tools/lib/def.sh"

shopt -s nullglob
shopt -s expand_aliases

# CMS ENV
cd $CMS_WD
. /etc/profile.d/modules.sh
module use -a /afs/desy.de/group/cms/modulefiles/
module load cmssw
cmsenv

#---------- GET OPTIONS ------------
POSITIONAL=()
while [[ $# -gt 0 ]]
do
    key="$1"

    case $key in
        --sc)
        SAME_SIGN=true
        POSITIONAL+=("$1")
        shift
        ;;
        --tl)
        TWO_LEPTONS=true
        POSITIONAL+=("$1")
        shift
        ;;
        --jpsi_muons)
        JPSI_MUONS=true
        POSITIONAL+=("$1")
        shift
        ;;
        --dy)
        DY=true
        POSITIONAL+=("$1")
        shift
        ;;
        --mini)
        MINI=true
        POSITIONAL+=("$1")
        shift
        ;;
        --master)
        MASTER=true
        POSITIONAL+=("$1")
        shift
        ;;
        --selection)
        SELECTION=true
        POSITIONAL+=("$1")
        shift
        ;;
        --jpsi_single_electron)
        JPSI_SINGLE_ELECTRON=true
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


if [ -n "$TWO_LEPTONS" ]; then
    if [ -n "$SAME_SIGN" ]; then
        OUTPUT_DIR=$TWO_LEPTONS_SAME_SIGN_SKIM_DATA_OUTPUT_DIR
    else
        OUTPUT_DIR=$TWO_LEPTONS_SKIM_DATA_OUTPUT_DIR
    fi
elif [ -n "$DY" ]; then
    OUTPUT_DIR=$DY_SKIM_DATA_OUTPUT_DIR
elif [ -n "$JPSI_MUONS" ]; then
    OUTPUT_DIR=$SKIM_DATA_JPSI_MUONS_OUTPUT_DIR
elif [ -n "$MINI" ]; then
    OUTPUT_DIR=$SKIM_DATA_MINI_OUTPUT_DIR
elif [ -n "$MASTER" ]; then
    OUTPUT_DIR=$SKIM_DATA_MASTER_OUTPUT_DIR
elif [ -n "$JPSI_SINGLE_ELECTRON" ]; then
    OUTPUT_DIR=$SKIM_DATA_JPSI_SINGLE_ELECTRON_OUTPUT_DIR
elif [ -n "$PHASE1" ]; then
    OUTPUT_DIR=$SKIM_DATA_PHASE1_OUTPUT_DIR
else
    OUTPUT_DIR=$SKIM_DATA_OUTPUT_DIR
fi

#check output directory
if [ ! -d "$OUTPUT_DIR" ]; then
  mkdir $OUTPUT_DIR
fi

#check output directory
if [ ! -d "$OUTPUT_DIR/single" ]; then
  mkdir "$OUTPUT_DIR/single"
fi

if [ ! -d "$OUTPUT_DIR/stdout" ]; then
  mkdir "$OUTPUT_DIR/stdout"
fi

if [ ! -d "$OUTPUT_DIR/stderr" ]; then
  mkdir "$OUTPUT_DIR/stderr"
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
EOM

file_limit=0
i=0
count=0
input_files=""
files_per_job=1
job_num=0

#files_per_job=1

FILE_OUTPUT="${OUTPUT_DIR}/single"

DATA_PATTERN="METAOD"
if [ -n "$DY" ] || [ -n "$JPSI_MUONS" ] || [ -n "$MINI" ] || [ -n "$MASTER" ]; then
    DATA_PATTERN="SingleMuon"
elif [ -n "$JPSI_SINGLE_ELECTRON" ]; then
    DATA_PATTERN="SingleElectron"
fi

#for fullname in ${DATA_NTUPLES_DIR}/Run2016*SingleMuon*; do

INPUT_DIR=${DATA_NTUPLES_DIR}

if [ -n "$SELECTION" ]; then
    INPUT_DIR=${DY_SKIM_DATA_OUTPUT_DIR}/single
fi
YEAR_PATTERN=Run2016
if [ -n "$PHASE1" ]; then
    YEAR_PATTERN="Run201[78]"
fi
#echo HERE: ${INPUT_DIR}/*${DATA_PATTERN}*
for fullname in ${INPUT_DIR}/${YEAR_PATTERN}*${DATA_PATTERN}*; do
    name=$(basename $fullname)
    if [ -z "$SELECTION" ] && [ -f "$FILE_OUTPUT/$name" ]; then
        #echo "$name exist. Skipping..."
        continue
    fi
    if [ -z "$input_files" ]; then
        input_files="$fullname"
    else
        input_files="$input_files $fullname"
    fi
    #input_files="$input_files $fullname"
    ((count+=1))
    if [ $(($count % $files_per_job)) == 0 ]; then
        ((job_num+=1))
        echo Job Num $job_num
        echo $DATA_DIR/run_skim_data_analysis_single.sh -i \"$input_files\" --data ${POSITIONAL[@]}
cat << EOM >> $output_file
arguments = $DATA_DIR/run_skim_data_analysis_single.sh -i $input_files --data ${POSITIONAL[@]}
error = ${OUTPUT_DIR}/stderr/$(basename $fullname .root).err
log = ${OUTPUT_DIR}/stdout/$(basename $fullname .root).log
output = ${OUTPUT_DIR}/stdout/$(basename $fullname .root).output
Queue
EOM
    input_files=""
    fi
    
    if [ $file_limit -gt 0 ]; then
        #check limit
        ((i+=1)) 
        if [ $i -ge $file_limit ]; then
            break
        fi
    fi
done

if [ $(($count % $files_per_job)) != 0 ]; then
    echo $DATA_DIR/run_skim_data_analysis_single.sh -i \"$input_files\" --data ${POSITIONAL[@]}
cat << EOM >> $output_file
arguments = $DATA_DIR/run_skim_data_analysis_single.sh -i $input_files --data ${POSITIONAL[@]}
error = ${OUTPUT_DIR}/stderr/$(basename $fullname .root).err
output = ${OUTPUT_DIR}/stdout/$(basename $fullname .root).output
Queue
EOM
fi


#for sim in ${SIG_DUP_OUTPUT_DIR}/single/*; do
# for sim in ${DATA_NTUPLES_DIR}/Run2016*METAOD*; do
#     filename=$(basename $sim .root)
#     echo "Will run:"
#     echo $DATA_DIR/run_skim_data_analysis_single.sh -i $sim -o ${OUTPUT_DIR}/single/${filename}.root --data ${POSITIONAL[@]}
# cat << EOM >> $output_file
# arguments = $DATA_DIR/run_skim_data_analysis_single.sh -i $sim -o ${OUTPUT_DIR}/single/${filename}.root --data ${POSITIONAL[@]}
# error = ${OUTPUT_DIR}/stderr/${filename}.err
# output = ${OUTPUT_DIR}/stdout/${filename}.output
# Queue
# EOM
# done

condor_submit $output_file
echo $output_file
#rm $output_file

#/tmp/condor_submut.20240328_012620878706385
#/tmp/condor_submut.20240328_013519377611143

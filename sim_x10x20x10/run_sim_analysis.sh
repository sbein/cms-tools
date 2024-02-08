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
        -skim|--skim)
        SKIM=true
        POSITIONAL+=("$1") # save it in an array for later
        shift # past argument
        ;;
        --sam)
        SAM=true
        POSITIONAL+=("$1")
        shift
        ;;
        -nlp)
        NLP=true
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

OUTPUT_DIR=$SKIM_SIG_OUTPUT_DIR
INPUT_DIR=$SIM_NTUPLES_DIR

    
if [ -n "$SAM" ]; then
    OUTPUT_DIR=$SKIM_SIG_SAM_OUTPUT_DIR
    INPUT_DIR=$SAM_NEW_SIM_NTUPLES_DIR
elif [ -n "$PHASE1" ]; then
    INPUT_DIR=$SAM_SIM_NTUPLES_17_DIR
    OUTPUT_DIR=$SKIM_SIG_PHASE1_OUTPUT_DIR
elif [ -n "$PHASE1_2018" ]; then
    INPUT_DIR=$SAM_SIM_NTUPLES_18_DIR
    OUTPUT_DIR=$SKIM_SIG_PHASE1_2018_OUTPUT_DIR
fi

if [ -n "$NLP" ]; then
    OUTPUT_DIR=$SKIM_SIG_NLP_OUTPUT_DIR
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
output_file="${WORK_DIR}/condor_submit.${timestamp}"
echo "output file: $output_file"

counter=0
files_per_job=5 # Set number of files per job
input_files=""
job_count=0

cat << EOM > $output_file
universe = vanilla
should_transfer_files = IF_NEEDED
executable = /bin/bash
notification = Never
request_memory = 16 GB
EOM

for sim in ${INPUT_DIR}/*higgsino*; do
    filename=$(basename $sim .root)
    if [ -f "${OUTPUT_DIR}/single/${filename}.root" ]; then
        echo "${OUTPUT_DIR}/single/${filename}.root exist. Skipping..."
        continue
    fi

    input_files="$sim,$input_files"
    ((counter++))

    if [ $(($counter % $files_per_job)) == 0 ]; then
        ((job_count++))
        cmd="$SIM_DIR/run_sim_analysis_single.sh -i $input_files -o ${OUTPUT_DIR}/single/ ${POSITIONAL[@]} --signal" 
        echo "Will run batch $job_count:"
        echo $cmd
        cat << EOM >> $output_file
arguments = $SIM_DIR/run_sim_analysis_single.sh -i $input_files -o ${OUTPUT_DIR}/single/ ${POSITIONAL[@]} --signal
error = ${OUTPUT_DIR}/stderr/${filename}_${job_count}.err
output = ${OUTPUT_DIR}/stdout/${filename}_${job_count}.output
Queue
EOM
        input_files=""
    fi
done

# Handle remaining files
if [ $(($counter % $files_per_job)) != 0 ]; then
    ((job_count++))
    cmd="$SIM_DIR/run_sim_analysis_single.sh -i $input_files -o ${OUTPUT_DIR}/single/ ${POSITIONAL[@]} --signal" 
    echo "Will run batch $job_count:"
    echo $cmd
    cat << EOM >> $output_file
arguments = $SIM_DIR/run_sim_analysis_single.sh -i $input_files -o ${OUTPUT_DIR}/single/${filename}.root ${POSITIONAL[@]} --signal
error = ${OUTPUT_DIR}/stderr/${filename}_${job_count}.err
output = ${OUTPUT_DIR}/stdout/${filename}_${job_count}.output
Queue
EOM
fi

echo "Number of jobs to be run: $job_count"
echo "Your Condor submission file is: $output_file"

echo $output_file
condor_submit $output_file
#rm $output_file

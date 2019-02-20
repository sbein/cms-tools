#!/bin/bash

. "/afs/desy.de/user/n/nissanuv/cms-tools/bg/def.sh"

shopt -s nullglob
shopt -s expand_aliases


# CMS ENV
cd $CMS_WD
. /etc/profile.d/modules.sh
module use -a /afs/desy.de/group/cms/modulefiles/
module load cmssw
cmsenv

OUTPUT_DIR=$SKIM_BG_SIG_DILEPTON_BDT_OUTPUT_DIR

timestamp=$(date +%Y%m%d_%H%M%S%N)
output_file="${WORK_DIR}/condor_submut.${timestamp}"
echo "output file: $output_file"

echo $OUTPUT_DIR
#check output directory
if [ ! -d "$OUTPUT_DIR" ]; then
  mkdir $OUTPUT_DIR
else
   rm -rf $OUTPUT_DIR
   mkdir $OUTPUT_DIR
fi

cat << EOM > $output_file
universe = vanilla
should_transfer_files = IF_NEEDED
executable = /bin/bash
notification = Never
priority = 0
EOM

for sim in $SKIM_BG_SIG_BDT_OUTPUT_DIR/*; do
	filename=$(basename $sim)
	
	if [ ! -d "$OUTPUT_DIR/$filename" ]; then
	  mkdir $OUTPUT_DIR/$filename
	fi

	#check output directory
	if [ ! -d "$OUTPUT_DIR/$filename/single" ]; then
	  mkdir "$OUTPUT_DIR/$filename/single"
	fi

	if [ ! -d "$OUTPUT_DIR/$filename/stdout" ]; then
	  mkdir "$OUTPUT_DIR/$filename/stdout" 
	fi

	if [ ! -d "$OUTPUT_DIR/$filename/stderr" ]; then
	  mkdir "$OUTPUT_DIR/$filename/stderr"
	fi

	for bg_file in $SKIM_BG_SIG_BDT_OUTPUT_DIR/$filename/single/*; do
		echo "Will run:"
		bg_file_name=$(basename $bg_file .root)
		echo $SCRIPTS_WD/run_skim_signal_dilepton_bdt_single.sh -i $bg_file -o ${OUTPUT_DIR}/$filename/single/${bg_file_name}.root -bdt $OUTPUT_WD/cut_optimisation/tmva/dilepton_bdt/$filename 
cat << EOM >> $output_file
arguments = $SCRIPTS_WD/run_skim_signal_dilepton_bdt_single.sh -i $bg_file -o ${OUTPUT_DIR}/$filename/single/${bg_file_name}.root -bdt $OUTPUT_WD/cut_optimisation/tmva/dilepton_bdt/$filename 
error = ${OUTPUT_DIR}/$filename/stderr/${bg_file_name}.err
output = ${OUTPUT_DIR}/$filename/stdout/${bg_file_name}.output
Queue
EOM
	done
done

condor_submit $output_file
rm $output_file

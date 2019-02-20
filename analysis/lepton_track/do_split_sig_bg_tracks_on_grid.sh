#!/bin/bash

. "/afs/desy.de/user/n/nissanuv/cms-tools/bg/def.sh"

shopt -s nullglob
shopt -s expand_aliases

OUTPUT_DIR=$LEPTON_TRACK_SPLIT_DIR

echo "output dir:" $OUTPUT_DIR

#check output directory

if [ ! -d "$OUTPUT_DIR/stdout" ]; then
  mkdir "$OUTPUT_DIR/stdout"
fi

if [ ! -d "$OUTPUT_DIR/stderr" ]; then
  mkdir "$OUTPUT_DIR/stderr"
fi

if [ ! -d "$OUTPUT_DIR/single" ]; then
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
priority = 0
+RequestRuntime = 86400
EOM

for f in /afs/desy.de/user/n/nissanuv/nfs/x1x2x1/signal/skim/single/*; do
	filename=$(basename $f .root)
	echo "Will run:"
	echo $LEPTON_TRACK_DIR/split_sig_bg_tracks_single.sh -i $f -o  $OUTPUT_DIR/single/${filename}
cat << EOM >> $output_file
arguments = $LEPTON_TRACK_DIR/split_sig_bg_tracks_single.sh -i $f -o  $OUTPUT_DIR/single/${filename}
error = ${OUTPUT_DIR}/stderr/${filename}.err
output = ${OUTPUT_DIR}/stdout/${filename}.output
Queue
EOM
done

condor_submit $output_file
rm $output_file



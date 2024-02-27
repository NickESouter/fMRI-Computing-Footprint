#!/bin/bash

#Defines the folder containing original data, and a list of all subjects.
BIDS_dir=<full path redacted>/CNP_BIDS

#IIterates over each subject folder.
for subject in "$BIDS_dir"/*; do
	if [[ -d "$subject" && "$subject" == *'sub-'* ]]; then

		#Extracts and prints the subject's ID.
		subject_id=$(basename "$subject")
		echo $subject_id

		#Defines an output path for this subject's data, creates it.
		outpath=<full path redacted>/SPM/CNP_SPM/$subject_id
		mkdir -p "$outpath"

		#Moves the subject's structural scan over, and zips it.
		rsync -av "$subject/anat/${subject_id}_T1w.nii.gz" "$outpath/anat/"	
		cd $outpath/anat
		gunzip -f ${subject_id}_T1w.nii.gz

		#Moves the subject's functional scan over, and zips it.
		rsync -av "$subject/func/${subject_id}_task-stopsignal_bold.nii.gz" "$outpath/func/"	
		cd $outpath/func
		gunzip -f ${subject_id}_task-stopsignal_bold.nii.gz


	fi
done

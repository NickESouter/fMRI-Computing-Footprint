#!/bin/bash

#Change working directory to the one containing thresholded files.
cd <full path redacted>/Analysis_Project_Output/Group_Level/Thresholded/

#A function to merge NIFTI files.
merge_nifti_files() {

	#Check if the correct number of arguments is provided
	if [ "$#" -ne 3 ]; then
		echo "Usage: merge_nifti_files <FSL_go_file> <fMRIPrep_go_file> <output_file>"
		return 1
	fi

	#Pulls out the input files and output file.
	input1="$1"
	input2="$2"
	output_file="$3"	

	#This series of fslmaths commandds generates the merged image we'll need. Voxels with above 0 in just
	#the first file have a value of 1, voxels with above 0 in just the second file have a value of 2,
	#and voxels above 0 in both maps have a value of 3.
	fslmaths $input1 -bin -mul $input2 -bin -add 2 -thr 3 Merged_temp
	fslmaths $input1 -bin -sub Merged_temp -bin -thr 1 input1_only
	fslmaths $input2 -bin -sub Merged_temp -bin -add 1 -thr 2 input2_only
	fslmaths input1_only -add input2_only -add Merged_temp "/research/cisc2/projects/rae_sustainability/Analysis_Project_Output/Group_Level/Merged/$output_file"

	#All temporary files generated are removed.
	rm -f Merged_temp.nii.gz
	rm -f input1_only.nii.gz
	rm -f input2_only.nii.gz
}

#Uses the function for each combination of files.
 merge_nifti_files 'FSL_go_thr.nii.gz' 'fMRIPrep_go_thr.nii.gz' 'FSL_fMRIprep_go'
 merge_nifti_files 'FSL_stop_thr.nii.gz' 'fMRIPrep_stop_thr.nii.gz' 'FSL_fMRIprep_stop'

 merge_nifti_files 'SPM_go_bin.nii.gz' 'fMRIPrep_go_thr.nii.gz' 'SPM_fMRIprep_go'
 merge_nifti_files 'SPM_stop_bin.nii.gz' 'fMRIPrep_stop_thr.nii.gz' 'SPM_fMRIprep_stop'

 merge_nifti_files 'FSL_go_thr.nii.gz' 'SPM_go_bin.nii.gz' 'FSL_SPM_go'
 merge_nifti_files 'FSL_stop_thr.nii.gz' 'SPM_stop_bin.nii.gz' 'FSL_SPM_stop'


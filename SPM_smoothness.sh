#!/bin/bash

#Defines a variable based on the location of FEAT preprocessed files.
spm_folders="<full path redacted>/SPM/CNP_SPM/"

#Tells the script to just go one level deep such that we can iterate over 'sub' subdirectories below.
subdirs=$(find "$spm_folders" -maxdepth 1 -type d -name "sub-*" | sort)

#Get the total number of subjects to be iterated over.
total_subjects=$(echo "$subdirs" | wc -l)

#Initialize a counter for the number of participants that have been iterated over.
count=0

#Begins iterating over subjects.
for subdir in $subdirs
do
	#Defines the subject identity as a variable.
	SUBJECTID=$(basename "$subdir")

	#Changes working directory to this subject's directory.		
	cd "${subdir}/func/"	

	#Any 'mask' files in this subject's directory are deleted to avoid issues with overwriting.
	find . -maxdepth 1 -name '*mask*' -type f -delete

	#An AFNI command is used to generate a 3D brain mark for this subject's preprocessed data.
	3dAutomask -prefix mask swr${SUBJECTID}_task-stopsignal_bold.nii

	#The output is converted to a NIFTI file, and intermediary AFNI files are deleted.
	3dAFNItoNIFTI mask+tlrc
	find . -maxdepth 1 -name '*tlrc*' -type f -delete

	#If it exists, the smoothness output file is deleted so that new versions can be created.
	#Avoids issues where files cannot be overwritten.
	find . -maxdepth 1 -name '*smoothness*' -type f -delete

	#Estimates the smoothness of the bold data that has and has not been smoothed. This is masked by the 'mask' file.
	#The files used to generate the estimates are deleted to avoid future overwriting issues.
	3dFWHMx -geom -detrend -mask mask.nii -out ${SUBJECTID}_SPM_smoothness_pre -input swr${SUBJECTID}_task-stopsignal_bold.nii
	find . -maxdepth 1 -name '*3dFWHMx*' -type f -delete

	3dFWHMx -geom -detrend -mask mask.nii -out ${SUBJECTID}_SPM_smoothness_post -input wr${SUBJECTID}_task-stopsignal_bold.nii
	find . -maxdepth 1 -name '*3dFWHMx*' -type f -delete

	#Defines the smoothness output directory as a variable.
	smoothness_dir="<full path redacted>/SPM/Smoothness/$SUBJECTID"

	#If the smoothness directory already exists, any files for this subject within
	#are deleted to avoid overwriting issues. If not, the directory is created.
	if [ -d "$smoothness_dir" ]; then
    		find "$smoothness_dir" -type f -name "*${SUBJECTID}*" -delete
	else
    		mkdir -p "$smoothness_dir"
	fi

	#Moves the 4D smoothness estimate to the smoothness output directory.
	mv ${SUBJECTID}_SPM_smoothness_pre $smoothness_dir
	mv ${SUBJECTID}_SPM_smoothness_post $smoothness_dir

	#Informs the user that the process is finished for a given subject.
	((count++))
	echo "Smoothness estimations are complete for $SUBJECTID, $count/$total_subjects"

done

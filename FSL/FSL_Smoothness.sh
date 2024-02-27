#!/bin/bash

#Defines a variable based on the location of FEAT preprocessed files.
feat_folders="<full path redacted>/FSL/first_level/"

#Tells the script to just go one level deep such that we can iterate over 'sub' subdirectories below.
subdirs=$(find "$feat_folders" -maxdepth 1 -type d -name "sub-*" | sort)

#Get the total number of subjects to be iterated over.
total_subjects=$(echo "$subdirs" | wc -l)

#Initialize a counter for the number of participants that have been iterated over.
count=0

#Begins iterating over subjects.
for subdir in $subdirs
do
	#Defines the subject identity as a variable.
	subject=$(basename "$subdir")
	SUBJECTID=$(echo "$subject" | sed 's/\.feat$//')

	#Changes wokring directory to this subject's directory.		
	cd "${subdir}"		

	#If it exists, the smoothness output file is deleted so that new versions can be created.
	#Avoids issues where files cannot be overwritten.
	find . -maxdepth 1 -name '*smoothness*' -type f -delete

	#Estimates the smoothness of the bold data that has not been smoothed. This is masked by the 'mask' file.
	#The files used to generate the estimate are deleted to avoid future overwriting issues.
	3dFWHMx -geom -detrend -mask mask.nii.gz -out ${SUBJECTID}_FSL_smoothness_post -input filtered_func_data.nii.gz
	find . -maxdepth 1 -name '*3dFWHMx*' -type f -delete

	#Defines the smoothness output directory for this subject as a variable.
	smoothness_dir="<full path redacted>/FSL/Smoothness/$SUBJECTID"

	#If the smoothness directory already exists, any files within
	#are deleted to avoid overwriting issues. If not, the directory is created.
	if [ -d "$smoothness_dir" ]; then
    		find "$smoothness_dir" -type f -name "*${SUBJECTID}*" -delete
	else
    		mkdir -p "$smoothness_dir"
	fi

	#Moves the 4D smoothness estimate to the smoothness output directory.
	mv ${SUBJECTID}_FSL_smoothness_post $smoothness_dir

	#Informs the user that the process is finished for a given subject.
	((count++))
	echo "Smoothness estimations are complete for $SUBJECTID, $count/$total_subjects"

done
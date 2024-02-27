#!/bin/bash

#The FEAT directory for this pipeline is defined.
feat_dir="<full path redacted>/fMRIPrep/first_level/"

#We need to iterate over the output folders for each subject and make changes to files generated during registration in FEAT.
#Group-level analysis requires this registration to have been run, but we've already registered in fMRIPrep. I followed the steps detailed
#here: https://www.youtube.com/watch?v=U3tG7JMEf7M&t=482s .

#Looks for each subject within the FEAT directory.
find "$feat_dir" -type d -name "*sub*" -print0 | while IFS= read -r -d '' subject; do

	#If a 'reg_standard' folder already exists, it's deleted.
	reg_standard_folder="$subject/reg_standard"
    
	if [ -d "$reg_standard_folder" ]; then
		rm -r "$reg_standard_folder"
	fi

	#Deletes any existing .mat files from the 'reg' folder.
	rm -f "$subject/reg/"*.mat

	#Copies the following files to the respective destinations (re-registered data is overwritten).
	cp "$FSLDIR/etc/flirtsch/ident.mat" "$subject/reg/example_func2standard.mat"
	cp "$subject/mean_func.nii.gz" "$subject/reg/standard.nii.gz"

	#Generates transformation and summary images that we'll need for Featquery to run successfully.
	updatefeatreg $subject -gifs

done

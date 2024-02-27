#Imports relevant modules
import glob
import os
import configparser
import shutil
import math

#Defines filepaths of interest including (a) input directory containing preprocessed data,
#(b) the location where FSF files should be saved, and (c) the location of both FSF templates.
inputdir = '<full path redacted>/fMRIPrep/Smoothed/'
fsfdir = '<full path redacted>/fMRIPrep/fsf_files/'
templates = '<full path redacted>/fMRIPrep/fsf_templates/'

#Checks whether the FSF directory exists. It's created if not.
if not os.path.exists(fsfdir):
	os.makedirs(fsfdir)

#Any files already within the FSF directory are deleted.
for root, dirs, files in os.walk(fsfdir):
        for found_file in files:
            file_path = os.path.join(root, found_file)
            os.remove(file_path)

#Iterates over subjects in the input directory.
for subject in sorted(os.listdir(inputdir)):

	#If a subfolder doesn't correspond to a specific subject, it's skipped.
	if 'sub' not in subject:
		continue

	#Defines the template for preprocessing FSF, and the output location for it.
	preproc_template = os.path.join(templates, 'Preproc_template.fsf')
	preproc_output = os.path.join(fsfdir, 'Preprocessing', '{}_preproc.fsf'.format(subject))

	#Opens the template and replaces any SUBNUM placeholder with this subject's ID.
	with open(preproc_template) as infile:
		with open(preproc_output, 'w') as outfile:

			for line in infile:

				line = line.replace('SUBNUM', subject)
				outfile.write(line)

	#A subject-specific directory containing EV files.
	EV_dir = '<full path redacted>/FSL/EVs/{}/'.format(subject)

	#If this participant has an 'erroneous' EV, we'll use the 6 EV template and tell the user. If not,
	#we'll use the 5 ev template instead. Note that each EV subfolder will include X exprimental EVs plus
	#the confounds file. Finally, if the number of files in this folder is not 6 or 7, the user is told that
	#something weird is happening and the rest of the loop is skipped.
	if 'erroneous_trials.txt' in os.listdir(EV_dir) and len(os.listdir(EV_dir)) == 6:
		stats_template = os.path.join(templates, 'EV6_template.fsf')
	elif 'erroneous_trials.txt' not in os.listdir(EV_dir) and len(os.listdir(EV_dir)) == 5:
		stats_template = os.path.join(templates, 'EV5_template.fsf')
	else:
		print('Unexpected number of EVs for {}, investigate.'.format(subject))
		continue

	#A subject-specific output name for the FSF file.
	stats_output = os.path.join(fsfdir, 'Statistics', '{}_stats.fsf'.format(subject))

	#Opens both the relevant template and the output file.
	with open(stats_template) as infile:
		with open(stats_output, 'w') as outfile:
			
			#Iterates over each line in the template, and replaces any subject placeholders.
			for line in infile:

				line = line.replace('SUBNUM', subject)
				outfile.write(line)

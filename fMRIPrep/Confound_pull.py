#Imports relevant modules.
import os
import shutil
import csv
import nibabel as nb
import numpy as np

#Defines the input and output directories.
preproc_dir = '/mnt/lustre/users/psych/ns605/Analysis/fMRIPrep/Preprocessing/derivatives/'
outdir = '/mnt/lustre/users/psych/ns605/Analysis/fMRIPrep/Confounds/'

#Iterates over each subject in the input directory.
for subject in os.listdir(preproc_dir):

	#Skips any irrelevant files/folders.
	if 'sub' not in subject or 'html' in subject:
		continue

	#If the first-level analysis directory doesn't exist, it's created.
	first_dir = '/mnt/lustre/users/psych/ns605/Analysis/fMRIPrep/first_level/{}'.format(subject)

	if not os.path.exists(first_dir):
		os.mkdir(first_dir)

	#Creates a dictionary to store relevant motion confounds.
	confound_dict = {'trans_x': [], 'trans_y': [], 'trans_z': [], 'rot_x': [], 'rot_y': [], 'rot_z': []}

	#Points to this subject's confound file, and opens it.
	confounds = os.path.join(preproc_dir, subject, 'func', '{}_task-stopsignal_desc-confounds_timeseries.tsv'.format(subject))	
	with open(confounds, 'r') as confounds_file:
		confounds_reader = csv.DictReader(confounds_file, delimiter = '\t')

		#Iterates over each row of this file, and then each confound key.
		for row in confounds_reader:
			for confound_key in confound_dict.keys():

				#Replaces any misses value, or just writes the relevant value in.
				if row[confound_key] == 'n/a':
					confound_dict[confound_key].append('0')
				else:
					confound_dict[confound_key].append(row[confound_key])

	#Creates and opens an output file for this subject.
	outpath = os.path.join(outdir, '{}_confounds.txt'.format(subject))	
	with open(outpath, 'w') as outfile:

		#For the number of rows (volumes), iterates over each parameter, and then writes in
		#the respective value to the output file.
		for i in range(len(confound_dict['trans_x'])):

			outrow = []

			for parameter in confound_dict:
				outrow.append(confound_dict[parameter][i])

			outfile.write(' '.join(outrow) + '\n')

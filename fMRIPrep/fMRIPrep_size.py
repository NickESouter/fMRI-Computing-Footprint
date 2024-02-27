#Imports relevant modules.
import os
import numpy as np
import csv

#Points to the input preprocessing and stats directories.
fmriprep_dir = '<full path redacted>/fMRIPrep/Preprocessing/'
stats_dir = '<full path redacted>/fMRIPrep/first_level/'

#Defines relevant subfolders that we'll be iterating through.
derivatives = os.path.join(fmriprep_dir, 'derivatives')
scratch = os.path.join(fmriprep_dir, 'scratch')

#This empty dictionary will be used to store the size of data for each subject.
subjects = {}

#Iterates through each subject output folder, and adds them
#to the above dictionary with another dictionary as a value. Any HTML report files are skipped.
for subject in sorted(os.listdir(derivatives)):
	if 'sub' not in subject or 'html' in subject:
		continue
	subjects[subject] = {'preproc': 0, 'analysis': 0, 'total': 0}

#This function is used to define the size of folders/files. It uses variables as input that
#are used to point to the filepath destination that we're interested in. If targetting a folder,
#counts the size of all the contents. If it's a file, just takes the size of the file. Then returns the total size.
def get_size(*args):
    path = os.path.join(*args)

    if os.path.isdir(path):

        if os.path.islink(path):
            return 0

        total_size = 0
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)

                if os.path.islink(file_path):
                    continue
                else:
                    total_size += os.path.getsize(file_path)
    else:
        total_size = os.path.getsize(path)

    return total_size

#Function to add the size of a folder/file to the relevant value.
def dict_add(filetype, size):
	subjects[subject][filetype] += size

#Iterates through folders within the derivatives folder.
for subject in sorted(os.listdir(derivatives)):

	#Skips any folders that don't correspond to a specific subject.
	if 'sub' not in subject:
		continue

	#Finds HTML output reports, adds to the preprocessing value.
	elif 'html' in subject:
		subject = subject[:-5]
		dict_add('preproc', get_size(derivatives, subject))
		dict_add('total', get_size(derivatives, subject))

	#For folders that contain subject-specific output files, they're added to the preproc key.
	else:

		dict_add('preproc', get_size(derivatives, subject))
		dict_add('total', get_size(derivatives, subject))

#This list will be used to track the size of scratch files that can't be linked to a specific participant.
scratch_1_sizes = []

#Iterates through each working directory in the scratch folder.
for wd in os.listdir(scratch):	

	#For the first level of this directory (excluding fMRIPrep folder), the size is appended to our above list.
	if 'fmriprep' not in wd:
		scratch_1_sizes.append(get_size(scratch, wd))

	#For the fMRIPrep working directory, iterates over each folder inside.
	else:
		for subfolder in sorted(os.listdir(os.path.join(scratch, wd))):

			#For working directories corresponding to specific subjects, the subject ID is first defined.
            		#Then calculates the size of all files inside.
			if 'single_subject' in subfolder:
				subject = 'sub-' + subfolder[-8:-3]
				dict_add('preproc', get_size(scratch, wd, subfolder))
				dict_add('total', get_size(scratch, wd, subfolder))

#For each subject, the mean size of our non-subject-specific file sizes are added to their value.
for subject in subjects:
	dict_add('preproc', np.mean(scratch_1_sizes))

#The same process is performed for statistical analysis files. We pick out the specific ones produced during stats.
for subject in os.listdir(stats_dir):

	if 'sub-' not in subject:
		continue

	#Defines subject directory and their ID.
	subject_dir = os.path.join(stats_dir, subject)
	subject = subject[:-5]

	#The following specific folders and files are counted as belonging to analysis.
	dict_add('analysis', get_size(subject_dir, 'custom_timing_files'))
	dict_add('analysis', get_size(subject_dir, 'tsplot'))
	dict_add('analysis', get_size(subject_dir, '.ramp.gif'))
	dict_add('analysis', get_size(subject_dir, 'confoundevs.txt'))
	dict_add('total', get_size(subject_dir, 'custom_timing_files'))
	dict_add('total', get_size(subject_dir, 'tsplot'))
	dict_add('total', get_size(subject_dir, '.ramp.gif'))
	dict_add('total', get_size(subject_dir, 'confoundevs.txt'))

	#Iterates over each item in this directory. Conditionally looks for strings
	#that correspond to multiple folders/files and adds them to the relevant value.
	for thing in os.listdir(subject_dir):

		if 'stat' in thing:
			dict_add('analysis', get_size(subject_dir, thing))
			dict_add('total', get_size(subject_dir, thing))

		if 'design' in thing:
			if 'fsf' in thing:
				continue
			else:
				dict_add('analysis', get_size(subject_dir, thing))
				dict_add('total', get_size(subject_dir, thing))

		if 'report' in thing:
			if 'prestats' in thing or 'reg' in thing or 'unwarp' in thing:
				continue
			else:
				dict_add('analysis', get_size(subject_dir, thing))
				dict_add('total', get_size(subject_dir, thing))


#Defines a path to the output file and provides headers.
output_file = '<full path redacted>/Analysis_Project_Output/File_Size/fMRIPrep_size.csv'
headers = ['Subject', 'Preprocessing', 'Statistical Analysis', 'Total']

#Opens the output file and writes out the headers.
with open(output_file, 'w', newline = '') as output:
	writer = csv.DictWriter(output, fieldnames = headers)
	writer.writeheader()

	#Iterates over each subject, writes out their ID, preprocessing size, analysis size,
	#and total size into the output file. File size in bytes is converted to GB.
	for subject in subjects:
		subject_row = {'Subject': subject,
		'Preprocessing': subjects[subject]['preproc']/(1024 ** 3),
		'Statistical Analysis': subjects[subject]['analysis']/(1024 ** 3),
		'Total': subjects[subject]['total']/(1024 ** 3)}
		writer.writerow(subject_row)

#Imports relevant modules.
import os
import csv

#This function is used to define the size of folders/files. It uses variables as input that
#are used to point to the filepath destination that we're interested in. If targetting a folder,
#counts the size of all the contents. If it's a file, just takes the size of the file. Then returns the total size.
#Returns 0 if the path doesn't exist.
def get_size(*args):
	path = os.path.join(*args)

	if not os.path.exists(path):
		return 0

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

#Function to add the size of a folder/file to the relevant key.
def dict_add(filetype, size):
	subjects[subject][filetype] += size

#Creates a dictionary to store size data for each subject.
subjects = {}

#Defines a variable containing first-level data for all subjects.
feat_dir = '<full path redacted>/FSL/first_level/'

#Iterates through each subject output folder, and adds them
#to the above dictionary with another dictionary as a value.
for subject in sorted(os.listdir(feat_dir)):
	if 'sub' not in subject:
		continue
	subjects[subject] = {'preproc': 0, 'analysis': 0, 'total': 0}

#Iterates over each subject again, and defines their specific path.
for subject in os.listdir(feat_dir):
	subject_dir = os.path.join(feat_dir, subject)

	#Adds total size of their folder to the dictionary. This may be larger
	#than the combination of preprocessing and analysis, in the case that other
	#things (e.g., Featquery) output have been generated post-first-level.
	dict_add('total', get_size(subject_dir))

	#Some specific folders/files are attributed to preprocessing.
	dict_add('preproc', get_size(subject_dir, '.files'))
	dict_add('preproc', get_size(subject_dir, 'logs'))
	dict_add('preproc', get_size(subject_dir, 'mc'))
	dict_add('preproc', get_size(subject_dir, 'reg'))
	dict_add('preproc', get_size(subject_dir, 'absbrainthresh.txt'))
	dict_add('preproc', get_size(subject_dir, 'mask.nii.gz'))

	#Other folders/files are labelled as analysis.
	dict_add('analysis', get_size(subject_dir, 'custom_timing_files'))
	dict_add('analysis', get_size(subject_dir, 'tsplot'))
	dict_add('analysis', get_size(subject_dir, '.ramp.gif'))
	dict_add('analysis', get_size(subject_dir, 'confoundevs.txt'))

	#Iterates over each item in this directory. Conditionally looks for strings
	#that correspond to multiple folders/files and adds them to the relevant value.
	for thing in os.listdir(subject_dir):

		if 'func' in thing:
			dict_add('preproc', get_size(subject_dir, thing))

		if 'stat' in thing:
			dict_add('analysis', get_size(subject_dir, thing))

		if 'design' in thing:
			if 'fsf' in thing:
				dict_add('preproc', get_size(subject_dir, thing))
			else:
				dict_add('analysis', get_size(subject_dir, thing))

		if 'report' in thing:
			if 'prestats' in thing or 'reg' in thing or 'unwarp' in thing:
				dict_add('preproc', get_size(subject_dir, thing))
			else:
				dict_add('analysis', get_size(subject_dir, thing))

#Defines a path to the output file and provides headers.
output_file = '<full path redacted>/File_Size/FSL_size.csv'
headers = ['Subject', 'Preprocessing', 'Statistical Analysis', 'Total']

#Opens the output file and writes out the headers.
with open(output_file, 'w', newline = '') as output:
	writer = csv.DictWriter(output, fieldnames = headers)
	writer.writeheader()

	#Iterates over each subject, writes out their ID, preprocessing size, analysis size,
	#and total size into the output file. File size in bytes is converted to GB.
	for subject in subjects:
		subject_row = {'Subject': subject[:-5],
		'Preprocessing': subjects[subject]['preproc']/(1024 ** 3),
		'Statistical Analysis': subjects[subject]['analysis']/(1024 ** 3),
		'Total': subjects[subject]['total']/(1024 ** 3)}
		writer.writerow(subject_row)

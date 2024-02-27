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

	if '.nfs' in path:
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
spm_dir = '<full path redacted>/SPM/CNP_SPM/'
stats_dir = '<full path redacted>/SPM/First_level/'

#Iterates through each subject output folder, and adds them
#to the above dictionary with another dictionary as a value.
for subject in sorted(os.listdir(spm_dir)):
	if 'sub' not in subject:
		continue
	subjects[subject] = {'preproc': 0, 'analysis': 0, 'total': 0, 'raw': 0}

#Iterates over each subject again, and defines their specific paths.
for subject in os.listdir(spm_dir):
	anat_dir = os.path.join(spm_dir, subject, 'anat')
	func_dir = os.path.join(spm_dir, subject, 'func')

	#Looks through their anatomical directory. The original T1w is counted as raw
	#data, everything else is added to preprocessing and the total count.
	for thing in os.listdir(anat_dir):
		if thing == '{}_T1w.nii'.format(subject):
			dict_add('raw', get_size(anat_dir, thing))
		else:
			dict_add('total', get_size(anat_dir, thing))		
			dict_add('preproc', get_size(anat_dir, thing))

	#Looks through their functional directory. Original functional data is counted as raw,
	#everything else is added to preprocessing and the total count.
	for thing in os.listdir(func_dir):
		if thing == '{}_task-stopsignal_bold.nii'.format(subject):
			dict_add('raw', get_size(func_dir, thing))
		else:
			dict_add('total', get_size(func_dir, thing))				
			dict_add('preproc', get_size(func_dir, thing))

	#Everything in this subject's stats directory is added to both analysis and the total count.
	dict_add('analysis', get_size(stats_dir, subject))
	dict_add('total', get_size(stats_dir, subject))

#Defines a path to the output file and provides headers.
output_file = '<full path redacted>/File_Size/SPM_size.csv'
headers = ['Subject', 'Preprocessing', 'Statistical Analysis', 'Total', 'Raw']

#Opens the output file and writes out the headers.
with open(output_file, 'w', newline = '') as output:
	writer = csv.DictWriter(output, fieldnames = headers)
	writer.writeheader()

	#Iterates over each subject, writes out their ID, preprocessing size, analysis size,
	#total size, and raw data size into the output file. File size in bytes is converted to GB.
	for subject in subjects:
		subject_row = {'Subject': subject,
		'Preprocessing': subjects[subject]['preproc']/(1024 ** 3),
		'Statistical Analysis': subjects[subject]['analysis']/(1024 ** 3),
		'Total': subjects[subject]['total']/(1024 ** 3),
		'Raw': subjects[subject]['raw']/(1024 ** 3)}
		writer.writerow(subject_row)

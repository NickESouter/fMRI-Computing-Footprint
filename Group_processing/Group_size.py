#Imports relevant modules.
import os
import csv

#This function is used to define the size of folders/files. It uses variables as input that
#are used to point to the filepath destination that we're interested in. If targetting a folder,
#counts the size of all the contents. If it's a file, just takes the size of the file. Then returns the total size.
#Returns 0 if the path doesn't exist. Also skips any temporary '.nsf' files.
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

#First for FSL, creates a variable to store size, then defines the first-level directory.
FSL_size = 0
FSL_dir = '<full path redacted>/Analysis/FSL/first_level/'

#Iterates over each subject for firt-level and finds the size of reg_standard, generated during group-level.
for subject in sorted(os.listdir(FSL_dir)):

	if 'sub-' not in subject:
		continue

	reg_standard = os.path.join(FSL_dir, subject, 'reg_standard')

	FSL_size += get_size(reg_standard)
	print(subject, FSL_size)

#Adds the size of the higher-level output.
FSL_size += get_size('<full path redacted>/Analysis/FSL/Higher_level/.gfeat/')

#The same process is completed for fMRIPrep.
fMRIPrep_size = 0
fMRIPrep_dir = '<full path redacted>/Analysis/fMRIPrep/first_level/'

for subject in sorted(os.listdir(fMRIPrep_dir)):

	if 'sub-' not in subject:
		continue

	reg_standard = os.path.join(fMRIPrep_dir, subject, 'reg_standard')

	fMRIPrep_size += get_size(reg_standard)
	print(subject, fMRIPrep_size)

fMRIPrep_size += get_size('<full path redacted>/Analysis/fMRIPrep/Higher_level/.gfeat/')

#For SPM, we just pull out the size of group-level output for both contrasts.
SPM_size = get_size('<full path redacted>/Analysis/SPM/Higher_level/Group_Go/') + get_size('<full path redacted>/Analysis/SPM/Higher_level/Group_Stop/')

print("FSL", FSL_size)
print("SPM", SPM_size)
print("fMRIPrep", fMRIPrep_size)

#Defines a path to the output file and provides headers.
output_file = '<full path redacted>/Analysis_Project_Output/Group_Level/Group_size.csv'

#Opens the output file and writes out the headers.
with open(output_file, 'w', newline = '') as output:
	writer = csv.DictWriter(output, fieldnames = ['FSL', 'SPM', 'fMRIPrep'])
	writer.writeheader()

	#Writes data out, file size in bytes is converted to GB.
	writer.writerow(
	{'FSL': FSL_size/(1024 ** 3),
	'SPM': SPM_size/(1024 ** 3),
	'fMRIPrep': fMRIPrep_size/(1024 ** 3)})

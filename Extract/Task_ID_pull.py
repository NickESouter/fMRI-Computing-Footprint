#Imports relevant modules.
import os
import csv

#Defines the package we're interested in. Can be FSL, SPM, or fMRIPrep.
package = 'FSL'

#Defines the folder for task IDs for this package.
package_path = '<full path redacted>/{}/Task_IDs'.format(package)

#Creates an empty dictionary to store task IDs.
tasks = {}

#If looking at FSL, we'll have a field for BET, but not for SPM or fMRIPrep.
if package == 'FSL':
	headers = ['Subject', 'BET', 'preproc', 'analysis', 'Featquery']
else:
	headers = ['Subject', 'preproc', 'analysis', 'Featquery']

#This function takes the name of the respective process, and locations the relevant input file.
#A subject-specific key is added to the above dictionary. The value is another dictionary containing
#the name of each process, and the relevant task ID, extracted from the input file. 
def dict_pull(process):

	if subject not in tasks.keys():
		tasks[subject] = {}
	
	infile = os.path.join(package_path, subject, 'Job_info_{}.txt'.format(process))

	if os.path.exists(infile):

		with open(infile) as open_file:
			for line in open_file:

				line = line.strip().split(" ")
				task_id = line[-1]
				tasks[subject][process] = task_id

	else:
		tasks[subject][process] = ''

#Iterates over all subjects in the package path, and checks they're actual subject folders.
for subject in sorted(os.listdir(package_path)):

	if 'sub-' not in subject:
		continue

	#Uses our above function to pull subject-specific task IDs for BET (for FSL only), preprocessing, statistics, and Featquery.
	if package == 'FSL':	
		dict_pull('BET')
	dict_pull('preproc')
	dict_pull('analysis')
	dict_pull('Featquery')

#Defines a path for an output file.
output_path = '<full path redacted>/Task_IDs/{}_Task_IDs.csv'.format(package)

#Opens the output file, and writes out headers to correspond to each process.
with open(output_path, mode = 'w', newline = '') as output_file:
	writer = csv.DictWriter(output_file, fieldnames = headers)
	writer.writeheader()

	#A subject ID key/value is appended to the start of the each subject-specific dictionary,
	#all is then written into the output file.
	for subject in tasks.keys():
		out_data = {'Subject': subject, **tasks[subject]}
		writer.writerow(out_data)

#Imports relevant modules.
import os
import csv
import json

#Defines the pipeline of interest. Can be FSL, SPM, or fMRIPrep.
package = 'FSL'

#Points to the file containing Task IDs for this package.
ID_file = '<full path redacted>/Task_IDs/{}_Task_IDs.csv'.format(package)

#Creates a dictionary to store subject-specific task IDs, and a list for all job IDs.
task_IDs = {}
jobs = []

#Opens the ID file and reads out the header.
with open(ID_file, 'r') as infile:
	infile.readline()

	#Iterates over each line in this file, splits them by comma.
	for line in infile.readlines():
		line = line.strip().split(',')

		#Finds the subject ID for a given row.
		subject = line[0]

		#The processes we'll need will vary between FSL and SPM/fMRIPrep.
		if package == 'FSL':
			task_IDs[subject] = {'BET': line[1], 'preproc': line[2], 'analysis': line[3], 'Featquery': line[4]}
		else:
			task_IDs[subject] = {'preproc': line[1], 'analysis': line[2], 'Featquery': line[3]}

		#In a given line, skips subject ID. Otherwise, all job IDs are pulled out and place in the above list.
		for item in line:
			if 'sub' in item:
				continue

			job = item.split('.')[0]

			if job not in jobs:
				jobs.append(job)

#Defines the location of the directory containing JSON files for each HPC job.
job_json_dir = '<full path redacted>/Calc_Carbon/Job_JSONs/'

#Defines the fieldnames to be used in the output file.
fieldnames = ['Subject', 'Task ID', 'Node', 'Num_CPU', 'Wallclock_seconds', 'Wallclock_hours', 'CPU_time', 'CPU_kWh', 'CPU_gCO2', 'Memory_max', 'Memory_kWh', 'Memory_gCO2', 'kWh', 'gCO2', 'kgCO2']

#This dictionary will store data by process rahter than by subject.
categorised_IDs = {}

#Iterates over each of the processes for the first subject in the above dictionary, and creates a key for each.
for process in task_IDs['sub-10159'].keys():
	categorised_IDs[process] = {}

#Iterates over all jobs for this package.
for job in jobs:

	#Finds the JSON file corresponding to this job.
	job_path = os.path.join(job_json_dir, 'calc_carbon_{}.json'.format(job))

	#Opens the JSON file and loads the data.
	with open(job_path) as json_file:
		data = json.load(json_file)

		#Iterates over each task in this job-specific file, pulls out the full task ID.
		for task in data[job]:
			full_ID = job + "." + task

			#Iterates over subject-specific task IDs, then over the processes inside.
			for subject in task_IDs:
				for process in task_IDs[subject]:

					#If the task ID in this file is the same as a subject-specific task, we pull
					#out all the info from this value and attach it to the respective subject in our
					#new dictionary.
					if task_IDs[subject][process] == full_ID:
						categorised_IDs[process][subject] = data[job][task]

#Iterates over each process in this dictionary.
for process in categorised_IDs:

	#Defines an output file for this package/process. Opens it and writes in the headers.
	outfile = '<full path redacted>/Calc_Carbon/{}_{}_carbon.csv'.format(package, process)

	with open(outfile, 'w', newline='') as csvfile:
		csvwriter = csv.DictWriter(csvfile, fieldnames = fieldnames)
		csvwriter.writeheader()

		#Iterates over each subject within a given process.
		for subject in categorised_IDs[process]:

			#Finds the row of data corresponding to this subject.
			inrow = categorised_IDs[process][subject]

			#Writes out a new row, pulling out all relevant information and calculating some new figures.
			outrow = {'Subject': subject,
			'Task ID': str(task_IDs[subject][process]),
			'Node': inrow['host'],
			'Num_CPU': inrow['NUM_CPU'],
			'Wallclock_seconds': inrow['wallclock'],
			'Wallclock_hours': float(inrow['wallclock'])/3600,
			'CPU_time': inrow['cpu'],
			'CPU_kWh': inrow['cpu_kWh'],
			'CPU_gCO2': inrow['cpu_gCO2'],
			'Memory_max': inrow['maxvmem'],
			'Memory_kWh': inrow['mem_kWh'],
			'Memory_gCO2': inrow['mem_gCO2'],
			'kWh': inrow['kWh'],
			'gCO2': inrow['gCO2'],
			'kgCO2': float(inrow['gCO2'])/1000}
			csvwriter.writerow(outrow)

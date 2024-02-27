#Imports relevant modules.
import os

#Defines the directory with EV files optimised for used in FSL.
ev_dir = '<full path redacted>/FSL/EVs/'

#Iterates over each subject, and non-subject folder is skipped.
for subject in os.listdir(ev_dir):

	if 'sub-' not in subject:
		continue

	#Defines the output path for this subject. Creates it if it doesn't exist.
	output_path = '<full path redacted>/SPM/Timing_files/{}/'.format(subject)

	if not os.path.exists(output_path):
		os.mkdir(output_path)

	#Iterates over each EV in the input folder.
	for ev in os.listdir(os.path.join(ev_dir, subject)):

		#Extracts the name of the EV and defines a path to it.
		ev_name = ev[:-4]
		ev_path = os.path.join(ev_dir, subject, ev)

		#Creates paths for onsent and duration files for this EV. Creates empty lists for each.
		onset_path = os.path.join(output_path, '{}_onset'.format(ev_name))
		duration_path = os.path.join(output_path, '{}_duration'.format(ev_name))

		onsets = []
		durations = []

		#Opens the EV file.
		with open(ev_path) as infile:

			#If it corresponds to response time data, we pull out the onset and specific duration.
			if '_rt' in ev:

				for line in infile:

					line = line.split(" ")
					onsets.append(line[0])
					durations.append(line[1])

			#If not, we just extract onset and assume duration is 1.5 seconds.
			else:

				for line in infile:

					line = line.split(" ")
					onsets.append(line[0])

				durations.append('1.5')

		#Opens the onset file and writes onset data into it.
		with open(onset_path, 'w') as onset_file:

			for onset in onsets:
				onset_file.write(onset + '\n')

		#Does the same for duration.
		with open(duration_path, 'w') as duration_file:

			for duration in durations:
				duration_file.write(duration + '\n')

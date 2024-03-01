#Imports relevant modules
import os
import numpy as np
import csv

#Defines the directory containing all packages.
analysis_dir = '<full path redacted>'

#Defines the package we're interested in. Can be FSL, SPM, or fMRIPrep.
package = 'SPM'

#Defines the filepath of this package.
package_dir = os.path.join(analysis_dir, package, 'Smoothness')

#Creates a path for an output file for this package and defines its headers in a list.
output_path = '<full path redacted>/Smoothness/{}_smoothness.csv'.format(package)

#For SPM and fMRIPrep we have pre-smoothed scores, but not for FSL.
if package == 'FSL':
	headers = ['Subject', 'Post', 'Post_x', 'Post_y', 'Post_z']
else:
	headers = ['Subject', 'Pre', 'Post', 'Pre_x', 'Pre_y', 'Pre_z', 'Post_x', 'Post_y', 'Post_z']

#The output file is opened and headers are written in.
with open(output_path, mode = 'w', newline = '') as output_file:
	writer = csv.DictWriter(output_file, fieldnames = headers)
	writer.writeheader()

	#Iterates over each subject in the directory for this package.
	for subject in os.listdir(package_dir):

		#Ignores a given folder if it doesn't correspond to a specific subject.
		if 'sub' not in subject:
			continue

		#This dictionary will store smoothness values for a given dimension for a given timepoint (pre-/post-smoothing).
		if package == 'FSL':
			categories = ['post']
			dimensions = {'post_x': [], 'post_y': [], 'post_z': []}
		else:
			categories = ['pre', 'post']
			dimensions = {'pre_x': [], 'pre_y': [], 'pre_z': [], 'post_x': [], 'post_y': [], 'post_z': []}

		#Iterates over the possible variants of the smoothing estimate files (pre- and post-smoothing).
		for suffix in categories:

			#Defines the smoothing file that we're interested in.
			smoothing_file = os.path.join(package_dir, subject, '{}_{}_smoothness_{}'.format(subject, package, suffix))

			#Opens and reads this file, then iterates over each row inside, which is stripped and split into numerical values.
			with open(smoothing_file, 'r') as file:
				for line in file:
					row = line.strip().split()

					#'float' versions of all values are appended to the respective list based on timepoint and dimension.
					dimensions['{}_x'.format(suffix)].append(float(row[0]))
					dimensions['{}_y'.format(suffix)].append(float(row[1]))
					dimensions['{}_z'.format(suffix)].append(float(row[2]))

		#Iterates over each key in the dictionary.
		for dimension in dimensions.keys():

			#Defines a high and low cutoff for detecting outliers (+/-3 standard deviations from the mean of this dimension).
			high_cutoff = np.mean(dimensions[dimension]) + 3*np.std(dimensions[dimension])
			low_cutoff =  np.mean(dimensions[dimension]) - 3*np.std(dimensions[dimension])

			#Any values found to exceed these cutoffs are removed from the repsective list.
			for i in dimensions[dimension]:
				if i >= high_cutoff or i <= low_cutoff:
					dimensions[dimension].remove(i)
			
		#Data for this subject are written into their output file, using the relevant mean values.
		if package == 'FSL':
			subject_row = {'Subject': subject,
				 	'Post': np.mean(dimensions['post_x'] + dimensions['post_y'] + dimensions['post_z']),
				 	'Post_x': np.mean(dimensions['post_x']),
				 	'Post_y': np.mean(dimensions['post_y']),
				 	'Post_z': np.mean(dimensions['post_z'])}

		else:
			subject_row = {'Subject': subject,
				 	'Pre': np.mean(dimensions['pre_x'] + dimensions['pre_y'] + dimensions['pre_z']),
				 	'Post': np.mean(dimensions['post_x'] + dimensions['post_y'] + dimensions['post_z']),
				 	'Pre_x': np.mean(dimensions['pre_x']),
				 	'Pre_y': np.mean(dimensions['pre_y']),
				 	'Pre_z': np.mean(dimensions['pre_z']),
				 	'Post_x': np.mean(dimensions['post_x']),
				 	'Post_y': np.mean(dimensions['post_y']),
				 	'Post_z': np.mean(dimensions['post_z'])}
		writer.writerow(subject_row)

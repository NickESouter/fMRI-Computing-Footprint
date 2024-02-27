#Imports relevant modules
import os
import csv

#Defines the package being interrogated. Can be FSL, SPM, or fMRIPrep.
package = 'FSL'

#Creates a path for the output file for this package and defines the relevant headers in a list.
output_path = '<full path redacted>/Featquery/{}_Featquery.csv'.format(package)
headers = ['Subject', 'Motor', 'Pre-sma', 'Auditory', 'Insula']

#Defines the root path of all packages.
root_path = '<full path redacted>'

#The exact Featquery directory will very depending on looking at SPM or FSL/fMRIPrep.
if package == 'SPM':
	stats_dir = os.path.join(root_path, 'SPM', 'Featquery')
else:
	stats_dir = os.path.join(root_path, package, 'first_level')

#The output file is opened and the header row is written.
with open(output_path, mode = 'w', newline = '') as output_file:
	writer = csv.DictWriter(output_file, fieldnames = headers)
	writer.writeheader()

	#Iterates over each subject in the package directory.
	for subject in sorted(os.listdir(stats_dir)):

		#A folder is skipped if it doesn't contain the 'sub' string.
		if 'sub' not in subject:
			continue

		#Subject ID is defined, this will need to be shortened if analysed in FEAT.
		if 'feat' in subject:
			subject_id = subject[:-5]
		else:
			subject_id = subject

		#Creates a dictionary for this subject which just contains their ID.
		zstats = {'Subject': subject_id}

		#Iterates over each ROI in the headers dictionary, skipping the 'subject' header.
		for region in headers:
			if region == 'Subject':
				continue
			
			#Defines a path to the relevant featquery report for this region.	
			featquery_report = os.path.join(stats_dir, subject, 'featquery_{}'.format(region), 'report.txt')

			#Opens the report, and pulls out the mean zstat value.
			with open(featquery_report, 'r') as f:
					mean_stat = f.readline().split()[5]

			#This value is added to the above dictionary with the region label as a key.
			zstats[region] = mean_stat

		#The subject-specific dictionary is written into the output file as a row.
		writer.writerow(zstats)

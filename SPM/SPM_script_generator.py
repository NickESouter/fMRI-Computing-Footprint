#Imports relevant modules.
import os

#Defines the filepath for SPM templates files, as input.
templates = '<full path redacted>/SPM/Templates/'

#Defines the directories containing input files for analysis, and the output location for scipts.
CNP_dir = '<full path redacted>/SPM/CNP_SPM/'
script_dir = '<full path redacted>/SPM/SPM_scripts/'

#Goes through the scripts directory and deletes any existing scripts.
for root, dirs, files in os.walk(script_dir):
	for file in files:
		os.remove(os.path.join(root, file))

#A function to save out subject-specific scripts using templates.
def script_save(temp, script_folder):

	#If the folder needed doesn't exist, it's created.
	if not os.path.exists(os.path.join(script_dir, script_folder)):
		os.makedirs(os.path.join(script_dir, script_folder))

	#Defines the name of the script to be generated, using the subject ID.
	script_name = temp.replace('Template', subject_alt)

	#Opens the input and output file, then goes through line by line and replaces placeholders with subject ID.
	with open(os.path.join(templates, temp)) as infile:
		with open(os.path.join(script_dir, script_folder, script_name), 'w') as outfile:
			for line in infile:
				outline = line.replace('SUBNUM', subject).replace('ALTSUB', subject_alt)
				outfile.write(outline)

#Iterates over each subject in the input directory.
for subject in sorted(os.listdir(CNP_dir)):

	#Ignores anything that doesn't relate to a specific subject.
	if 'sub-' not in subject:
		continue

	#We'll need an alternative subject ID for filenames, because MATLAB can't
	#run scripts if they have a hyphen in their name.
	subject_alt = 'sub_' + subject[4:]

	#Using our function, saves out scripts for preprocessing using templates.
	script_save('Template_preproc.m', 'Preprocessing/Run')
	script_save('Template_preproc_job.m', 'Preprocessing/Jobs')
	
	#At default the number of EVs (timing files) is assumed to be 5.
	EV_num = '5'

	#Defines a subject's timing file directory, then look through it for the presence
	#of 'erroneous' EVs. If found, we know this subject has 6 EVs and our variable above is updated.
	timing_dir = '<full path redacted>/SPM/Timing_files/{}/'.format(subject)
	for EV in os.listdir(timing_dir):
		if 'erroneous' in EV:
			EV_num = '6'
			break
	
	#Saves out the analysis script. Template used is dependent on whether this subject
	#has 5 or 6 EVs.
	if EV_num == '5':
		script_save('Template_analysis_EV5.m', 'Analysis/Run')
		script_save('Template_analysis_EV5_job.m', 'Analysis/Jobs')
	else:
		script_save('Template_analysis_EV6.m', 'Analysis/Run')
		script_save('Template_analysis_EV6_job.m', 'Analysis/Jobs')

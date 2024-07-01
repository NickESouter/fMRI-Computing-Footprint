#!/bin/bash

#Job ID name sent to HPC cluster.
#$ -N FEAT

#Number of requested parallel environments.
#$ -pe openmp 5

#Requested memory for HPC cluster.
#$ -l m_mem_free=8G

#Nodes not to use.
#$ -l 'h=!node001&!node072&!node017&!node018&!node019&!node041&!node063&!node065&!node066&!node067&!node068&!node069&!node070&!node071&!node073&!node074&!node075&!node076&!node077&!node078&!node079&!node080&!node081'

#This sets SGE_TASK_ID!, the number of subjects sent for preprocessing in this job (each is a seperate task).
#$ -t 1-248

#Sets the job class for HPC cluster.
#$ -jc test.short

#Makes sure we are in my home directory, then loads Anaconda (python) module and sets it up.
cd /its/home/ns605
module load Anaconda3/2022.10
source ~/conda_setup.sh

#Loads the FSL pacakge and unsets SGE_ROOT
module load FSL/6.0.3-foss-2019b-Python-3.7.4
unset SGE_ROOT

#Creates an array which contains each ROI as keys, with the number of the respective tstat file as values.
#These will be used to run Featquery below.
declare -A ROIs
ROIs=( ["Motor"]="1" ["Pre-sma"]="2" ["Auditory"]="2" ["Insula"]="2" )

#Defines the Featquery directory and changes into it.
featquery_dir=<full path redacted>/SPM/Featquery
cd "$featquery_dir"

#Creates an array of subjects to be iterated over, defines their index
subjects=($(find . -name "sub-*" -exec basename {} \; | sort))
subject_idx=$((SGE_TASK_ID - 1))
subject="${subjects[$subject_idx]}"

#Iterates over each ROI.
for roi in "${!ROIs[@]}"; do
			
	#Defines the value of this ROI as the tstat code we'll need.
	tstat=${ROIs[$roi]}
			
	#Runs Featquery on the respective ROI for this batch. This will run simultaneously across all subjects in a batch for the respective ROI.
	featquery 1 ${featquery_dir}/${subject}/ 1 stats/tstat$tstat featquery_$roi <full path redacted>/ROIs/SPM_space/${roi}_ROI_SPM.nii.gz

done

#Defines the output directory.
IDdir=<full path redacted>/SPM/Task_IDs

#Checks if the ID directory exists; if not, creates it.
if [ ! -d "${IDdir}/${subject}" ]; then
    mkdir -p "${IDdir}/${subject}"
fi

#Saves out a file with subject ID, and job/task ID.
echo "Subject ID: ${subject}, Task ID: $JOB_ID.$SGE_TASK_ID" > "${IDdir}/${subject}/Job_info_Featquery.txt"

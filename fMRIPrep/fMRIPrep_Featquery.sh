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
cd <full path redacted>
module load Anaconda3/2022.10
source ~/conda_setup.sh

#Loads the FSL pacakge and unsets SGE_ROOT
module load FSL/6.0.3-foss-2019b-Python-3.7.4
unset SGE_ROOT

#Creates an array which contains each ROI as keys, with the number of the respective tstat file as values.
#These will be used to run Featquery below.
declare -A ROIs
ROIs=( ["Motor"]="1" ["Pre-sma"]="2" ["Auditory"]="2" ["Insula"]="2" )

#Changes working directory to first-level output.
outdir=<full path redacted>/fMRIPrep/first_level
cd $outdir

#Creates an array of subjects to be iterated over, defines their index.
subjects=($(find . -name "sub-*.feat" -exec basename {} \; | sort))
subject_idx=$((SGE_TASK_ID - 1))
subject="${subjects[$subject_idx]}"

#Iterates over each ROI.
for roi in "${!ROIs[@]}"; do
			
	#Defines the value of this ROI as the tstat code we'll need.
	tstat=${ROIs[$roi]}
			
	#Runs Featquery on the respective ROI for this subject.
	featquery 1 ${outdir}/${subject}/ 1 stats/tstat$tstat featquery_$roi <full path redacted>/ROIs/fMRIPrep_space/${roi}_ANTs.nii.gz

done

#Extracts subject ID from the input subject string.
subject_id="${subject:0:9}"

#Defines the ID directory.
IDdir=<full path redacted>/fMRIPrep/Task_IDs

#Checks if the ID directory exists; if not, creates it.
if [ ! -d "${IDdir}/${subject_id}" ]; then
    mkdir -p "${IDdir}/${subject_id}"
fi

#Saves out a file with subject ID, and job/task ID.
echo "Subject ID: ${subject_id}, Task ID: $JOB_ID.$SGE_TASK_ID" > "${IDdir}/${subject_id}/Job_info_Featquery.txt"

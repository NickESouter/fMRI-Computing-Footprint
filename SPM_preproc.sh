#!/bin/bash

#Job ID name sent to HPC cluster.
#$ -N SPM

#Number of requested parallel environments.
#$ -pe openmp 5

#Requested memory for HPC cluster.
#$ -l m_mem_free=8G

#Nodes not to use.
#$ -l 'h=!node001&!node072&!node017&!node018&!node019&!node041&!node063&!node065&!node066&!node067&!node068&!node069&!node070&!node071&!node073&!node074&!node075&!node076&!node077&!node078&!node079&!node080&!node081'

#This sets SGE_TASK_ID!, the number of subjects sent for preprocessing in this job (each is a seperate task).
#$ -t 1-257

#Sets the job class for HPC cluster.
#$ -jc test.short

#Loads MATLAB and unsets SGE_ROOT.
module load matlab
unset SGE_ROOT

#Changes directory to that containing relevant scripts.
cd <full path redacted>/SPM/SPM_scripts/Preprocessing/Run

#Creates an array of subjects to be iterated over, defines their index.
subjects=($(find . -name "sub_*_preproc.m" -exec basename {} \; | sort))
subject_idx=$((SGE_TASK_ID - 1))
subject="${subjects[$subject_idx]%??}"

#Executes SPM in MATLAB for this subject.
matlab -nodisplay -nosplash -nodesktop -r "${subject}; exit"

#Extracts subject ID from the input subject string.
subject_id="${subject:0:3}-${subject:4:5}"

#Defines the output directory.
outdir=<full path redacted>/SPM/Task_IDs

#Checks if the output directory exists; if not, creates it.
if [ ! -d "${outdir}/${subject_id}" ]; then
    mkdir -p "${outdir}/${subject_id}"
fi

#Saves out a file with subject ID, and job/task ID.
echo "Subject ID: ${subject_id}, Task ID: $JOB_ID.$SGE_TASK_ID" > "${outdir}/${subject_id}/Job_info_preproc.txt"

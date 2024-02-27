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
#$ -t 1-257

#Sets the job class for HPC cluster.
#$ -jc test.short

#Makes sure we are in my home directory, then loads Anaconda (python) module and sets it up.
cd <full path redacted>
module load Anaconda3/2022.10
source ~/conda_setup.sh

#Loads the FSL pacakge and unsets SGE_ROOT
module load FSL/6.0.3-foss-2019b-Python-3.7.4
unset SGE_ROOT

#Changes directory to that containing relevant fsf files.
cd <full path redacted>/FSL/fsf_files/Preprocessing

#Defines the output directory.
outdir=<full path redacted>/FSL/first_level

#Creates an array of subjects to be iterated over, defines their index.
subjects=($(find . -name "sub-*_preproc.fsf" -exec basename {} \; | sort))
subject_idx=$((SGE_TASK_ID - 1))
subject="${subjects[$subject_idx]}"

#Executes FEAT for this subject.
feat "${subject}"

#Extracts subject ID from the input subject string.
subject_id="${subject:0:9}"

#Defines the ID directory.
IDdir=<full path redacted>/FSL/Task_IDs

#Checks if the ID directory exists; if not, creates it.
if [ ! -d "${IDdir}/${subject_id}" ]; then
    mkdir -p "${IDdir}/${subject_id}"
fi

#Saves out a file with subject ID, and job/task ID.
echo "Subject ID: ${subject_id}, Task ID: $JOB_ID.$SGE_TASK_ID" > "${IDdir}/${subject_id}/Job_info_preproc.txt"

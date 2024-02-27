#!/bin/bash

#Job ID name sent to HPC cluster.
#$ -N FEAT

#Number of requested parallel environments.
#$ -pe openmp 5

#Requested memory for HPC cluster.
#$ -l m_mem_free=8G

#Nodes not to use.
#$ -l 'h=!node001&!node072&!node018&!node019&!node041&!node063&!node065&!node066&!node067&!node068&!node069&!node070&!node071&!node073&!node074&!node075&!node076&!node077&!node078&!node079&!node080&!node081'

#This sets SGE_TASK_ID!, the number of subjects sent for preprocessing in this job (each is a seperate task).
#$ -t 1-257

#Sets the job class for HPC cluster.
#$ -jc test.short

#Makes sure we are in my home directory, then loads Anaconda (python) module and sets it up.
cd <full path redacted>
module load Anaconda3/2022.10
source ~/conda_setup.sh

#Loads the FSL pacakge and unsets SGE_ROOT.
module load FSL/6.0.3-foss-2019b-Python-3.7.4
unset SGE_ROOT

#Defines the BIDS input directory, changes working directory to it.
BIDSdir=<full path redacted>/CNP_BIDS
cd $BIDSdir

#Generates an array of subjects based on folder names. Defines their index and name.
subjects=($(find . -type d -name 'sub-*' -printf '%P\n'| sort))
subject_idx=$((SGE_TASK_ID - 1))
subject="${subjects[$subject_idx]}"

#BET brain extraction.
bet "${BIDSdir}"/"${subject}"/anat/"${subject}"_T1w.nii.gz "${BIDSdir}"/"${subject}"/anat/"${subject}"_T1w_brain.nii.gz

#Defines the ID directory.
IDdir=<full path redacted>/FSL/Task_IDs

#Checks if the ID directory exists; if not, creates it.
if [ ! -d "${IDdir}/${subject}" ]; then
    mkdir -p "${IDdir}/${subject}"
fi

#Saves out a file with subject ID, and job/task ID.
echo "Subject ID: ${subject}, Task ID: $JOB_ID.$SGE_TASK_ID" > "${IDdir}/${subject}/Job_info_BET.txt"

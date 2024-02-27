#!/bin/bash

#Job ID name sent to HPC cluster.
#$ -N FEAT

#Number of requested parallel environments.
#$ -pe openmp 5

#Requested memory for HPC cluster.
#$ -l m_mem_free=8G

#Nodes not to use.
#$ -l 'h=!node001&!node072&!node017&!node018&!node019&!node041&!node054&!node063&!node065&!node066&!node067&!node068&!node069&!node070&!node071&!node073&!node074&!node075&!node076&!node077&!node078&!node079&!node080&!node081'

#Sets the job class for HPC cluster.
#$ -jc test.long

#Makes sure we are in my home directory, then loads Anaconda (python) module and sets it up.
cd <full path redacted>
module load Anaconda3/2022.10
source ~/conda_setup.sh

#Loads the FSL pacakge and unsets SGE_ROOT
module load FSL/6.0.3-foss-2019b-Python-3.7.4
unset SGE_ROOT

#Executes FEAT for this subject.
feat <full path redacted>/fMRIPrep/Higher_level/fMRIPrep_Group.fsf

#Defines the output directory.
outdir=<full path redacted>/fMRIPrep/Higher_level

#Saves out a file with subject ID, and job/task ID.
echo "Group Analysis Task ID: $JOB_ID" > "${outdir}/Job_info_group.txt"



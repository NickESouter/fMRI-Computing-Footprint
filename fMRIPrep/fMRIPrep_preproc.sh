#!/bin/bash

#Job ID name sent to HPC cluster.
#$ -N fMRIPrep

#Number of requested parallel environments.
#$ -pe openmp 5

#Requested memory for HPC cluster.
#$ -l m_mem_free=8G

#Nodes not to use.
#$ -l 'h=!node001&!node072&!node017&!node018&!node019&!node041&!node063&!node065&!node066&!node067&!node068&!node069&!node070&!node071&!node073&!node074&!node075&!node076&!node077&!node078&!node079&!node080&!node081'

#This sets SGE_TASK_ID!, the number of subjects sent for preprocessing in this job (each is a seperate task).
#$ -t 1-248

#Sets the job class for HPC cluster.
#$ -jc test.long

#Stores fMRIPrep log files, and indicates that logs should be stored.
#$ -o '<full path redacted>/fMRIPrep/Preprocessing/logs'
#$ -e logs

#The overarching fMRIPrep preprocessing directory.
fMRIPrep_dir=<full path redacted>/fMRIPrep/Preprocessing/

#Defines key directories, including (1) input data, (2) working directory, and (3) output directory.
DATA_DIR=<full path redacted>/Sustainability/CNP_BIDS
SCRATCH_DIR=$fMRIPrep_dir/scratch
OUT_DIR=$fMRIPrep_dir/derivatives

#Location of the fMRIPrep license.
LICENSE=<full path redacted>/fs_license/license.txt  

#Changes working directory to the input data directory.
cd ${DATA_DIR}

#Creates an array of subject folders within this directory.
SUBJLIST=$(find sub-* -maxdepth 0  -type d)

#Changes working directory to home directory.
cd ${HOME}

#Prints out the subject's task ID.
echo "Task ID: $SGE_TASK_ID"

#Extracts the relevant subject ID from our above array, and prints it out. 
i=$(expr $SGE_TASK_ID - 1)
arr=($SUBJLIST)
SUBJECT=${arr[i]}
echo $SUBJECT

#Runs fMRIPrep for this subject, in a singularity container.
singularity run --cleanenv \
    -B ${DATA_DIR}:/data \
    -B ${OUT_DIR}/:/out \
    -B ${SCRATCH_DIR}:/wd \
    -B ${LICENSE}:/license \
    <full path redacted>/fmriprep_singularity/fmriprep_22.1.1.simg \
    --participant-label ${SUBJECT} \
    --fs-license-file /license \
    --skip-bids-validation \
    --work-dir /wd \
    --omp-nthreads 1 --nthreads 5 --mem_mb 30000 \
    --track-carbon \
    --country-code GBR \
    --ignore slicetiming \
    --random-seed 1234 \
    --skull-strip-fixed-seed \
    --fs-no-reconall \
    /data /out/ participant

echo Done

#Defines the ID directory.
IDdir=<full path redacted>/fMRIPrep/Task_IDs

#Checks if the ID directory exists; if not, creates it.
if [ ! -d "${IDdir}/${SUBJECT}" ]; then
    mkdir -p "${IDdir}/${SUBJECT}"
fi

#Saves out a file with subject ID, and job/task ID.
echo "Subject ID: ${SUBJECT}, Task ID: $JOB_ID.$SGE_TASK_ID" > "${IDdir}/${SUBJECT}/Job_info_preproc.txt"

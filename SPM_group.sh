#!/bin/bash

#Job ID name sent to HPC cluster.
#$ -N SPM

#Number of requested parallel environments.
#$ -pe openmp 5

#Requested memory for HPC cluster.
#$ -l m_mem_free=8G

#Nodes not to use.
#$ -l 'h=!node001&!node072&!node017&!node018&!node019&!node041&!node054&!node063&!node065&!node066&!node067&!node068&!node069&!node070&!node071&!node073&!node074&!node075&!node076&!node077&!node078&!node079&!node080&!node081'

#Sets the job class for HPC cluster.
#$ -jc test.long

#Loads MATLAB and unsets SGE_ROOT.
module load matlab
unset SGE_ROOT

#Defines the path of the 'go' and 'stop' group directories to be used.
go_dir=<full path redacted>/SPM/Higher_level/Group_Go
stop_dir=<full path redacted>/SPM/Higher_level/Group_Stop

#Deletes files in the specified directories while leaving folders intact.
find "$go_dir" -type f -exec rm {} +
find "$stop_dir" -type f -exec rm {} +

#Changes into the folder containing group-level scripts.
cd <full path redacted>/SPM/Higher_level/Scripts

#Runs the script.
matlab -nodisplay -nosplash -nodesktop -r "SPM_group; exit"

#Defines the output directory for task ID file.
outdir=<full path redacted>/SPM/Higher_level

#Saves out a file with subject ID, and job/task ID.
echo "Group Analysis Task ID: $JOB_ID" > "${outdir}/Job_info_group.txt"

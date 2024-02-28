# fMRI-Computing-Footprint

The scripts included in this repository were used to process and analyse fMRI data for the paper 'The carbon footprint of fMRI data preprocessing and analysis'. This proejct required processing the same existing datatset (LINK) in three different packages; FSL, SPM, and fMRIPrep. It was important for all to be run on the same high-performance computing (HPC) architecture in a manner that would allow for carbon tracking through the use of HPC logs. Most scripts are split by package, but sometowards the end of the process are used to aggregate data regardless of package. Following implementation of the steps detailed here, data and code used to faciliate statistical analysis reported in our paper are hosted on the Open Science Framework (OSF; https://osf.io/cdq6y/). 

We first discuss scripts provided for each individual package. Scripts and files are decribed in the order in which they were implemented on the raw data.

Scripts that are setup to run on our HPC cluster (specified below) are shells scripts includign falgs passed to the sun grid engine (SGE system). They each end by saving out the job and task ID associated with a given job, to facilitate carbon tracking more easily.

## FSL

### FSL_BET.sh

This shell script performs brain extraction on the raw fMRI data for each subject, using the BET function of FSL. Set up to run on our HPC cluster.

### fsf_templates

This folder contains fsf templates, which will be needed to create preprocessing and statistical analysis files for data processed in FSL. There is one for prepreprocessing, and two for statistical analysis (one is used per subject, depending on if they have an 'erroneous' EV timing file or not.

### fsf_generator.py

This Python script accesses the fsf template files described above and generates both necessary fsf files for each subject in our dataset.

### FSL_preproc.sh

This shell script initiates preprocessing in FSL FEAT for each subject, using the fsf files generated in the above step. Set up to run on our HPC cluster.

### FSL_Smoothness.sh

This shell script performs estimates of mean data smoothness for preprocessed and smoothed data from FSL FEAT. Estimates are generated using the 3dFWHMx function from AFNI. In this case, we're not able to generate 'pre-smoothing' smoothness estimates, given insufficient intermediary files.

### FSL_stats.sh

This shell script initiates first-level statistical analysis in FSL FEAT for each subject, using the directory created during preprocessing as input. Set up to run on our HPC cluster.

### FSL_Featquery.sh

This script script initates FSL Featquery reigon of interest (ROI) analysis on data statistically analysed in FSL FEAT. Performed for each subject for each of our 4 ROIs. Set up to run on our HPC cluster.

### FSL_Size.py

This Python script measures the total size of files generated throughout data processing in FSL FEAT. This is done seperately for files derived from preprocessing and statistical analysis.

### Group_fsf

This folder contains a single FSF file used to run group-level analysis in FSL FEAT. We only need one of these files, so the process was not automated as for first-level analysis.

### FSL_group.sh

This shell script performs group-level analysis for data already subjected to first-level analysis in FSL FEAT. Calls the group fsf file detailed above. Set up to run on our HPC cluster.

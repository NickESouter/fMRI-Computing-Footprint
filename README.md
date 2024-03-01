# fMRI-Computing-Footprint

The scripts included in this repository were used to process and analyse fMRI data for the paper '*The carbon footprint of fMRI data preprocessing and analysis*'. This project required processing the same [existing datatset][1] in three different packages; FSL, SPM, and fMRIPrep. It was important for all to be run on the same high-performance computing (HPC) architecture in a manner that would allow for carbon tracking through the use of HPC logs. Most scripts are split by package, but sometowards the end of the process are used to aggregate data regardless of package. Following implementation of the steps detailed here, data and code used to faciliate statistical analysis reported in our paper are hosted on the Open Science Framework (OSF; https://osf.io/cdq6y/). 

We first discuss scripts provided for each individual package. Scripts and files are decribed in the order in which they were implemented on the raw data.

Scripts that are setup to run on our HPC cluster (specified below) are shells scripts includign falgs passed to the sun grid engine (SGE system). They each end by saving out the job and task ID associated with a given job, to facilitate carbon tracking more easily.

## FSL

### FSL_BET.sh

This shell script performs brain extraction on the raw fMRI data for each subject, using the BET function of FSL. Set up to run on our HPC cluster.

### fsf_templates

This folder contains fsf templates, which will be needed to create preprocessing and statistical analysis files for data processed in FSL. There is one for prepreprocessing, and two for statistical analysis (one is used per subject, depending on if they have an 'erroneous' EV timing file or not).

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

## SPM

### SPM_reformat.sh

The raw data for this project included compressed nifti files (.nii.gz). For SPM, we'll need uncompressed files (.nii). This shell script finds the relevant structural and functional file for each subject, then copies them to a new directory and uncompresses them.

### SPM_timing.py

We'll also need to convert three column timing files usedduring first-level analysis in FSL FEAT into single file formats, containing onset and duration separately for each subject. This Python script does this for each subject.

### Templates

This folder contains template scripts for preprocessing and first-level analysis. There are two version of the first-level analysis script, dependent on whether the subject has an 'erroneous' EV present or not. Each script has a version used to call the MATLAB batch, and a 'job' script that contains the actual commands to be used. Once generated, job files for each subject can be opened in the SPM12 batch GUI. 

### SPM_script_generator.py

For each subject, this Python script generates preprocessing and first-level analysis MATLAB scripts, using the templates described above.

### SPM_preproc.sh

This shell script initiates preprocessing in SPM for each subject, using the Preprocessing scripts generated in the step above. Set up to run on our HPC cluster.

### SPM_smoothness.sh

This shell script performs estimates of mean data smoothness for preprocessed and smoothed data from SPM. Estimates are generated using the 3dFWHMx function from AFNI. In this case, we can generate 'pre-smoothing' smoothness estimates as well as post-smoothing estimates. However, pre-smoothing estimates were not analysed as part of this project.

### SPM_stats.sh

This shell script initiates first-level statistical analysis in SPM, using the analysis scripts generated above and taking preprocessed data as input. Set up to run on our cluster.

### SPM_Size.py

This Python script measures the total size of files generated throughout data processing in SPM. This is done seperately for files derived from preprocessing and statistical analysis. In this case we also account for the 'raw' input files that are included in the same directory as the output.

### SPM_Featquery_Prepare.sh

We next to run FSL Featquery ROI analysis on our data. Given that Featquery expects a certain file structure generated by FSL FEAT, we need to move and rename some files to essentially trick Featquery into thinking it's recieving FSL data as input. This includes creating a directory with sham files int he same space and boundary box as files processed in SPM, and moving statistical files from SPM into a 'stats' directory and compressing them. Beyond this, the Featquery process is exactly as it would be for FSL FEAT data.

### SPM_Featquery.sh

Using the file structure generated above, this shell script runs FSL Featquery ROI analysis on data analysed in SPM. Performs this for each of our four ROIs for each subject. Set up to run on our HPC cluster.

### Group_scripts

Contains a 'run' and 'job' script for higher-level analysis in SPM. Takes output of first-level analysis as input. We only need these two files, so the process was not automated as for first-level analysis. To provide full carbon tracking of this process, the job file includes a 'Results Report' module which contains a cluster correcting value only obtained from previously running higher-level analysis to completion. In order to do this, it was necessary to run this analysis once without this module, and once again with it.

### SPM_group.sh

This shell script is used to perform higher-level statistical analysis on data processed in SPM. Uses the scripts described above. Set up to run on our HPC cluster.

## fMRIPrep

### fMRIPrep_preproc.sh

This shell script performs preprocessing on fMRIPrep on raw data, for each subject. fMRIPrep is run in a Singularity container. Set up to run on our HPC cluster.

### fMRIPrep_Confound_pull.py

fMRIPrep preprocessing will have generated a file containing motion confounds. For first-level analysis, we'll want a file containing just 6 of these. This Python script generates a new file for each subject containing these specific values.

### fMRIPrep_Smoothing.sh

fMRIPrep does not contain a smoothing function. As such, we need to run smoothing outside of fMRIPrep. For this, we use the 3dBlurInMask function from AFNI. We also perform estimates of mean pre- and post-smoothing smoothness using AFNI 3dFWHMx (although post-smoothing estimates are not used in analysis). Ideally, smoothing would be carbon tracked such that it could be added to our existing carbon estimate for preprocessing fMRIPrep data. However, AFNI is not currently set up to run on our HPC cluster, meaning this was not possible.

### fsf_templates

This folder contains templates for fsf files for each subject for use in FSL FEAT. For each subject we'll need a preproc_post file (described below) and an analysis file. There are two version of the first-level analysis file, dependent on whether the subject has an 'erroneous' EV present or not.

### fMRIPrep_fsf_generator.py

This Python scripts generates the two fsf files needed for each subject, using the template files described above.

### fMRIPrep_preproc_post.sh

To facilitate group-level analysis of our fMRIPrep data, we effectively need to re-run registration in FSL FEAT. This is because group-analysis expects a certain file structure and naming convention that would otherwise not be present. This is set up to run on our HPC cluster. We carbon track this process, but given that it's not actually a part of fMRIPrep preprocessing, we do not include it in the overall estimate for preprocessing emissions.

### fMRIPrep_reg_cleanup.sh

To make sure our original registration files are used rather than the ones generated in the step above, we need to go into our first-level folder and cleanup new registration files and matrices. This effectively means that only registrations from fMRIPrep will be used going forward.

### fMRIPrep_stats.sh

This shell script initiates first-level statistical analysis in FSL FEAT, using the fsf files described above. Set up to run on our high-performance cluster.

### fMRIPrep_size.py

This Python script measures the total size of files generated throughout preprocessing in fMRIPrep and subseqent analysis in FSL FEAT. This is done seperately for files derived from preprocessing and statistical analysis.

### fMRIPrep_Featquery.sh

This script script initates FSL Featquery reigon of interest (ROI) analysis on data preprocessed in fMRIPrep, following first-level analysis. Performed for each subject for each of our 4 ROIs. Set up to run on our HPC cluster.

### Group_fsf

This folder contains a single FSF file used to run group-level analysis in FSL FEAT. We only need one of these files, so the process was not automated as for first-level analysis.

### fMRIPrep_group.sh

This shell script performs group-level analysis for data preprocessed in fMRIPrep and already subjected to first-level analysis in FSL FEAT. Calls the group fsf file detailed above. Set up to run on our HPC cluster.


[1]: https://openneuro.org/datasets/ds000030/versions/1.0.0

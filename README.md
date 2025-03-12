# fMRI-Computing-Footprint

The scripts included in this repository were used to process and analyse fMRI data for the paper '*The carbon footprint of fMRI data preprocessing and analysis*'. This project required processing the same [existing datatset][1] in three different packages; FSL, SPM, and fMRIPrep. It was important for all to be run on the same high-performance computing (HPC) architecture in a manner that would allow for carbon tracking through the use of HPC logs. Most scripts are split by package, but sometowards the end of the process are used to aggregate data regardless of package. Following implementation of the steps detailed here, data and code used to faciliate statistical analysis reported in our paper are hosted [on the Open Science Framework (OSF)][2]. Unthresholded group-level t-statistic maps generated for each pacakge during higher-level analysis are available [on Neurovault][3].

We first discuss scripts provided for each individual package, respectively contained in the folders 'FSL', 'SPM', and 'fMRIPrep'. Scripts and files are decribed in the order in which they were implemented on the raw data. Finally, scripts contained in the 'Extract' folder are used extract dependent variables across packages.

Scripts that are setup to run on the [University of Sussex HPC cluster][4] (specified below) are shells scripts including flags passed to the sun grid engine (SGE) system. They each end by saving out the job and task ID associated with a given job, to facilitate carbon tracking more easily.

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

fMRIPrep was run twice for this paper, once in the default output space (MNI152NLin2009cAsym) with native resolution, and once in MNI152NLin6Asym with a resolution of 2mm (for supplementary comparison). The scripts uploaded here were used for the former, but any case where deviations were needed in scripts to process 2mm data are specified. Otherwise, the scripts required for these two versions were identical.

### fMRIPrep_preproc.sh

This shell script performs preprocessing on fMRIPrep on raw data, for each subject. fMRIPrep is run in a Singularity container. Set up to run on our HPC cluster.

The 2mm version was the same, with this additional fMRIPrep flag in the command line:

```
--output-spaces MNI152NLin6Asym:res-2
```

### fMRIPrep_Confound_pull.py

fMRIPrep preprocessing will have generated a file containing motion confounds. For first-level analysis, we'll want a file containing just 6 of these. This Python script generates a new file for each subject containing these specific values.

### fMRIPrep_Smoothing.sh

fMRIPrep does not contain a smoothing function. As such, we need to run smoothing outside of fMRIPrep. For this, we use the 3dBlurInMask function from AFNI. We also perform estimates of mean pre- and post-smoothing smoothness using AFNI 3dFWHMx (although post-smoothing estimates are not used in analysis). Ideally, smoothing would be carbon tracked such that it could be added to our existing carbon estimate for preprocessing fMRIPrep data. However, AFNI is not currently set up to run on our HPC cluster, meaning this was not possible.

The version of this script for 2mm was the same, with the exception that the both instaces of 'MNI152NLin2009cAsym' are replaced with 'MNI152NLin6Asym:res-2' when identifying the input data.

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

Note that prior to running Featquery on fMRIPrep data, it was necessary to transform all ROI files to the native resolution of the input data and the standard output space generated in fMRIPrep by default (MNI152NLin2009cAsym). This was done using ANTs:

```
antsApplyTransforms -d 3 -i <ROI input> -r <reference file> -o <ROI output> -t tpl-MNI152NLin2009cAsym_from-MNI152NLin6Asym_mode-image_xfm.h5  -n NearestNeighbor --float
```

### Group_fsf

This folder contains a single FSF file used to run group-level analysis in FSL FEAT. We only need one of these files, so the process was not automated as for first-level analysis.

### fMRIPrep_group.sh

This shell script performs group-level analysis for data preprocessed in fMRIPrep and already subjected to first-level analysis in FSL FEAT. Calls the group fsf file detailed above. Set up to run on our HPC cluster.

## Extract

### Task_ID_Pull.py

This Python script extracts all SGE task IDs for relevant elements of data processing in each package. The 'package' variable at the top of this script should be appropriately updated to be either 'FSL', 'SPM', or 'fMRIPrep'. When excuting elements of preprocessing and statistical analysis for each package (see above) jobs and task IDs were extracted and placed in a folder. This way, for each subject for each stage of each package this script can pull out the relevant IDs and store them in a single CSV which is then acessed during Carbon_extract.py (below).

### Calc_carbon.py

This Python script is used to estimate carbon emissions resulting from computing, and is set up to run on the SGE system, with the following usage:

qacct -j JOB ID | python3 Calc_carbon.py

For example:

qacct -j 4043726 | python3 Calc_carbon.py

This must be done manually for each job. If, for example, job 4043726 corresponded to preprocessing in SPM for all 248 subjects, this code would grab relevant computing metrics (including wallclock, CPU time, max memory usage) for each subject (task), which would then be saved in a job-specific dictionary in a Job_JSONs folder, in the current working directory. 

This script was used for computing at the University of Sussex in early 2024. If using in another context, users will need to update global variables at teh top of the script, including g_per_kWh (this is average carbon intensity, which will vary by country, region, and year), and pue (power use effectiveness, which will be specific to to the computing architecture in use). See the paper for a full description of the methodology used to estimate carbon emissions.

### Carbon_extract.py

This Python script makes use of collated task IDs and carbon tracking metrics that have been extracted through the two steps above, for a given package. The 'package' variable at the top of this script should be appropriately updated to be either 'FSL', 'SPM', or 'fMRIPrep'. Specifically, it finds the task ID of each relevant stage of each package, then looks in the specified Jobs_JSONs folder to find metrics including duration, energy usage, and carbon emissions. This is paired with the relevant subject and processing stage which is placed in a file specific to a given stage for a given package.

### Smoothing_extract.py

This Python script is used to extract mean data smoothness metrics for each subject for a given package. The 'package' variable at the top of this script should be appropriately updated to be either 'FSL', 'SPM', or 'fMRIPrep'. This script accesses each subject-specific smoothness file. It then writes an output file for mean smoothness in the X, Y, and Z dimension for both pre- and post-smoothed data. An overall average for each stage is also provided. Before doing so, any outliers (+/- 3 standard deviations from the mean) for a given dimension for a given stage (e.g., X dimension for post-smoothed) are removed. Note that for FSL, a measure of pre-smoothed smoothness is not avaiable as the necessary interstitial file is not provided. Pre-smoothed smoothness is not analysed or discussed for any package in the paper. 

### Featquery_extract.py

This Python script extracts the mean t-statistics in each ROI for each subject for a given package. The 'package' variable at the top of this script should be appropriately updated to be either 'FSL', 'SPM', or 'fMRIPrep'. Specifically, this script finds Featquery reports generated during the above package-specific scripts, and pulls out the relevant values. All are placed into a single file corresponding to a given package.

## Group_processing

These scripts were used to set up input for figures or to report information about group-level output files.

### Dice_coeff.py

This script generates metrics used in Supplementary Table 5, including the the size of thresholded group-level output for each package, the dice coefficient with the relevant contrast for each other package, and the percentage of non-zero voxels which fall outside of the MNI brain mask template.

### Group_merge.sh

This script was used to merge together thresholded group-level files for the creation of Figure 3. The same function is applied to both contrasts for each combination of two packages.

### Group_size.py

This script was used to calculate the size of output files generated during group-level fMRI statistical analysis, for each package.


[1]: https://openneuro.org/datasets/ds000030/versions/1.0.0
[2]: https://osf.io/cdq6y/
[3]: https://neurovault.org/collections/QRJOSICN/
[4]: https://docs.hpc.sussex.ac.uk/apollo2/index.html

%Add SPM path
addpath('<full path redacted>/SPM_Cluster/spm12/')

% List of open inputs
nrun = 1; % enter the number of runs here
jobfile = {'<full path redacted>/SPM/SPM_scripts/Analysis/Jobs/ALTSUB_analysis_EV5_job.m'};
jobs = repmat(jobfile, 1, nrun);
inputs = cell(0, nrun);
for crun = 1:nrun
end
spm('defaults', 'FMRI');
spm_jobman('run', jobs, inputs{:});

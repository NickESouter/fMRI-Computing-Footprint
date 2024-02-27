%%

% Defines path to input data and timing files

CNP_path =  '<full path redacted>/SPM/CNP_SPM/SUBNUM/func/';
timing_path = '<full path redacted>/SPM/Timing_files/SUBNUM/';

% fMRI model specification

matlabbatch{1}.spm.stats.fmri_spec.dir = {'<full path redacted>/SPM/First_level/SUBNUM'};
matlabbatch{1}.spm.stats.fmri_spec.timing.units = 'secs';
matlabbatch{1}.spm.stats.fmri_spec.timing.RT = 2;
matlabbatch{1}.spm.stats.fmri_spec.timing.fmri_t = 16;
matlabbatch{1}.spm.stats.fmri_spec.timing.fmri_t0 = 8;
matlabbatch{1}.spm.stats.fmri_spec.sess.scans = cellstr(spm_select('ExtFPListRec', CNP_path, 'swr*', [1:184]));

% Condition 1 - Go

matlabbatch{1}.spm.stats.fmri_spec.sess.cond(1).name = 'go';
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(1).onset = importdata(fullfile(timing_path, 'go_onset'));
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(1).duration = 1.5;
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(1).tmod = 0;
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(1).pmod = struct('name', {}, 'param', {}, 'poly', {});
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(1).orth = 0;

% Condition 2 - Successful stop

matlabbatch{1}.spm.stats.fmri_spec.sess.cond(2).name = 'stop_success';
stop_success_onset = importdata(fullfile(timing_path, 'stop_success_onset'));
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(2).onset = stop_success_onset;
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(2).duration = 1.5;
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(2).tmod = 0;
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(2).pmod = struct('name', {}, 'param', {}, 'poly', {});
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(2).orth = 0;

% Condition 3 - Unsuccessful stop

matlabbatch{1}.spm.stats.fmri_spec.sess.cond(3).name = 'stop_unsuccess';
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(3).onset = importdata(fullfile(timing_path, 'stop_unsuccess_onset'));
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(3).duration = 1.5;
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(3).tmod = 0;
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(3).pmod = struct('name', {}, 'param', {}, 'poly', {});
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(3).orth = 0;

matlabbatch{1}.spm.stats.fmri_spec.sess.multi = {''};
matlabbatch{1}.spm.stats.fmri_spec.sess.regress = struct('name', {}, 'val', {});
matlabbatch{1}.spm.stats.fmri_spec.sess.multi_reg = {fullfile(CNP_path, 'rp_SUBNUM_task-stopsignal_bold.txt')};
matlabbatch{1}.spm.stats.fmri_spec.sess.hpf = 128;
matlabbatch{1}.spm.stats.fmri_spec.fact = struct('name', {}, 'levels', {});
matlabbatch{1}.spm.stats.fmri_spec.bases.hrf.derivs = [0 0];
matlabbatch{1}.spm.stats.fmri_spec.volt = 1;
matlabbatch{1}.spm.stats.fmri_spec.global = 'None';
matlabbatch{1}.spm.stats.fmri_spec.mthresh = 0.8;
matlabbatch{1}.spm.stats.fmri_spec.mask = {''};
matlabbatch{1}.spm.stats.fmri_spec.cvi = 'AR(1)';

% Model estimation

matlabbatch{2}.spm.stats.fmri_est.spmmat = {'<full path redacted>/SPM/First_level/SUBNUM/SPM.mat'};
matlabbatch{2}.spm.stats.fmri_est.write_residuals = 0;
matlabbatch{2}.spm.stats.fmri_est.method.Classical = 1;

% Contrast Manager

matlabbatch{3}.spm.stats.con.spmmat = {'<full path redacted>/SPM/First_level/SUBNUM/SPM.mat'};
matlabbatch{3}.spm.stats.con.consess{1}.tcon.name = 'go_stop_success';
matlabbatch{3}.spm.stats.con.consess{1}.tcon.weights = [1 -1 0];
matlabbatch{3}.spm.stats.con.consess{1}.tcon.sessrep = 'none';
matlabbatch{3}.spm.stats.con.consess{2}.tcon.name = 'stop_success_go';
matlabbatch{3}.spm.stats.con.consess{2}.tcon.weights = [-1 1 0];
matlabbatch{3}.spm.stats.con.consess{2}.tcon.sessrep = 'none';
matlabbatch{3}.spm.stats.con.delete = 0;

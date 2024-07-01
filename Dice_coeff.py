#Imports relevant modules.
import os
import nibabel as nb
import numpy as np
import csv

#Defines the directory with thresholded group level maps.
thr_dir = '<full path redacted>/Analysis_Project_Output/Group_Level/Thresholded/'

#Finds and opens a binary mask file that will be compared to each thresholded map.
mask_file = '<full path redacted>/Analysis_Project_Output/Group_Level/MNI_mask.nii.gz'
mask_img = nb.load(mask_file)
mask_data = mask_img.get_fdata()

#Opens the output CSV file and writes in headers.
with open(os.path.join(thr_dir, 'Dice_coef.csv'), 'w', newline='') as csvfile:
	writer = csv.DictWriter(csvfile, fieldnames = ['Contrast', 'Package', 'Num_vox', 'in_FSL', 'in_SPM', 'in_fMRIPrep', 'Outside_brain'])
	writer.writeheader()

	#Iterates over each thresholded map, skipping anything that is not a NIFTI file.
	for thr_map in sorted(os.listdir(thr_dir)):

		if 'nii.gz' not in thr_map or 'thr' not in thr_map:
			continue

		#Pulls out the overall name of the map as well as the package and constrast it corresponds to.
		map_name = thr_map[:-11]
		package = map_name.split('_')[0]
		contrast = map_name.split('_')[1]

		#Opens the file, and then counts and stores the number of voxels with a value above 0.
		img = nb.load(os.path.join(thr_dir, thr_map))
		open_img = img.get_fdata()
		num_vox = np.sum(open_img > 0)

		#Writes a row for this map including its name, number of voxels, and a blank value for same-package comparison.
		map_row = {'Map': map_name,
		'Num_vox': num_vox,
		'in_{}'.format(package): '-'}

		#Again, iterates over each thresholded nifti file.
		for other_map in sorted(os.listdir(thr_dir)):

			if 'nii.gz' not in other_map or 'thr' not in other_map:
				continue

			#Pulls out the overall name of the map as well as the package and constrast it corresponds to.
			other_name = other_map[:-11]
			other_package = other_name.split('_')[0]
			other_contrast = other_name.split('_')[1]

			#We skip a map if it corresponds to the same package or a different contrast.
			if package != other_package and contrast == other_contrast:

				#Opens this new file, then finds the number of voxels above 0 in both maps.
				other_img = nb.load(os.path.join(thr_dir, other_map))
				other_data = other_img.get_fdata()
				overlap_voxels = np.sum((open_img > 0) & (other_data > 0))

				#Calculates dice coefficient for the relevant combination of packages, rounded to 2 decimal places, and saves it out.
				dice_coeff = round(( 2 * overlap_voxels )/( np.sum(open_img > 0) + np.sum(other_data > 0) ), 2)
				map_row['in_{}'.format(other_package)] = dice_coeff

		#Caculate the number of voxels in the thresholded map that fall outside the MNI brain mask,
		#add it to this map's dictionary.
		mask_zero_voxels = ((open_img > 0) & (mask_data == 0)).sum()
		percent_mask_zero = (mask_zero_voxels / num_vox) * 100
		map_row['Outside_brain'] = round(percent_mask_zero, 2)
		
		#Writes an output row, calling all the relevant information from above.	
		outrow = {'Contrast': contrast,
		'Package': package,
		'Num_vox': map_row['Num_vox'],
		'in_FSL': map_row['in_FSL'],
		'in_SPM': map_row['in_SPM'],
		'in_fMRIPrep': map_row['in_fMRIPrep'],
		'Outside_brain': map_row['Outside_brain']}
		writer.writerow(outrow)

import os
import numpy as np
import h5py
import platform
from cshoreIO import cshoreIO

import subprocess

csio = cshoreIO()

class run_cshore_background(object):
	def __init__(self):

		self.runcshore_var = {}							#a placeholder.

	def init(self, meta_dict, reach):
		self.meta_dict = meta_dict						#setting up meta-dict
		self.make_h5file(reach)					#creating an output h5 file to write to (for each storm)
		self.run_cshore_win_serial(reach)				#runs cshore on windows in serial. user can add other options if desired (see below)
		self.delete_output_files()						#deletes the cshore output files
		self.close_h5file()								#closes the h5 file

	def make_h5file(self, reach):
		temp_path = os.getcwd()							#current directory (i.e. where infiles are)
		os.chdir(self.meta_dict['outfile_directory_reach'])									#moves up a directory (to read storm names)
		self.h5filename = reach + '.h5'	#sets h5 filename
		self.h5file = h5py.File(self.h5filename, 'w')	#creates h5 filename
		os.chdir(temp_path)								#back to the directory with infiles

	def write_h5file(self, infile_name, morpho, hydro):
		"""
		writing to h5file in feet. 
		note that the initial profile here is not exactly the initial profile created.
			CSHORE applies a smoothing function, and the smoothed profile is used. 
			minimal difference with original profile
		"""
		infile_name = infile_name.rsplit('.', 1)[0]		#reading the infilename, and taking the first part (i.e. not the extension "." infile)
		Profile_storm = self.h5file.create_group(infile_name)	#creates a group for the profile/storm combination
		init_data = np.column_stack((np.array(morpho['x'][0])/.3048, np.array(morpho['zb'][0])/.3048))		#creating dataset and converting to feet. 
		fin_data = np.column_stack((np.array(morpho['x'][-1])/.3048, np.array(morpho['zb'][-1])/.3048))		#creating dataset and converting to feet. 
		max_data, min_data = self.max_min_dictionary(morpho, 'zb')		#max and min value across all time steps at each spacing step. 
		max_hydro, _ = self.max_min_dictionary(hydro, 'mwl')
		max_wave, _ = self.max_min_dictionary(hydro, 'Hs')

		max_data = max_data/.3048			#max profile elevation (ft.)
		min_data = min_data/.3048			#min profile elevation (ft.)
		max_hydro = max_hydro/.3048			#max storm surge elevation (ft.)
		max_wave = max_wave/.3048			#max wave conditions (ft.)

		dset_init_profile = Profile_storm.create_dataset('Initial Profile', data = init_data)		#writing results to h5file
		dset_fin_profile = Profile_storm.create_dataset('Final Profile', data = fin_data)
		dset_max_profile = Profile_storm.create_dataset('Max Prof Elev', data = max_data)
		dset_min_profile = Profile_storm.create_dataset('Min Prof Elev', data = min_data)
		dset_hdryo = Profile_storm.create_dataset('Max Water Elev+Setup', data = max_hydro)
		dset_wave = Profile_storm.create_dataset('Max Wave Ht', data = max_wave)

	def close_h5file(self):
		self.h5file.close()					#self-explanatory

	def delete_output_files(self):
		for i in os.listdir('.'):			#removes files that start with "O" (cshore output.)
			if i.startswith('O'):
				os.remove(i)

	def max_min_dictionary(self, data, key):
		"""
		this function reads the max and min values of each dictionary. 
		cshore results vary across both space (offshore to onshore) and time (0-end).
		this function reads at each space step (x1, x2, ..., xn) the smallest and largest
			values across all time steps.  
		"""
		max_values = []														#setting up empty storage arrays
		min_values = []
		x_values = data['x'][0]												#x-values of data
		x_lengths = [len(data['x'][i]) for i in range(len(data['x']))]		#finding the length of each x-array at consecutive time steps (this varies across time)
		max_ind = x_lengths.index(max(x_lengths))							#index of where x-array is longest
		for i in range(max(x_lengths)):										#loop through longest x-array. e.g. starts at x=0, goes to landward most point across time, x=n
			temp = []														#empty temporary array
			for j in range(len(data[key])):									#loop through time steps (t=0 -> t=n)
				if i < len(data[key][j]):									#if there is some data at the "i"th space step and "j"th time step
					temp.append(data[key][j][i])							#	append the data there
				else:														#else
					temp.append(np.nan)						      		#	append an nan value
                                        #note that temp is an array of all of the elevations across time at the "i"th space
			max_values.append(np.nanmax(temp))								#finds the max value (excluding nan's) of temp
			min_values.append(np.nanmin(temp))								#	same as above except minimum values
		max_values = np.column_stack((np.array(data['x'][max_ind]), np.array(max_values)))	#stacking the x-values and "z"-values of the maximum arrays
		min_values = np.column_stack((np.array(data['x'][max_ind]), np.array(min_values)))	#	same as above except minimum values

		return max_values, min_values										#note that this function is confusing, and tough to explain. 


	def run_cshore_win_serial(self, reach):
                #first find the os
                ilinux=platform.system()=='Linux'

		#~~~ windows - serial ~~~
		"""
		used to run cshore serially on a windows machine. 
		"""

		infiles = os.listdir('.')						     #read files in directory
                                                                                        
		infiles = sorted([f for f in infiles if f.endswith('.infile')])		#sorting the files that end with ".infile"

		for infile in infiles:												#loop through infiles
			os.rename(infile, 'infile')						       		#rename the file we're working with here to "infile"

                        if ilinux:
                                os.system(os.path.join(self.meta_dict['exe_directory'], 'CSHORE_USACE_LINUX.out'))	#call on cshore
                        else:
                                os.system(os.path.join(self.meta_dict['exe_directory'], 'cshore_usace_win.out'))	#call on cshore                        

                        print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')	#space seperator
                        params, bc, veg, hydro, sed, morpho = csio.load_CSHORE_results(os.getcwd())	#reading cshore results
                        self.write_h5file(infile, morpho, hydro)						#writing what is needed to the h5 file
                        os.rename('infile', infile)								#renaming the infile to it's original name.


	def run_cshore_win_parallel(self, reach):
		"""
		this was an early attempt at 'parallelizing' cshore on a windows machine. 
		this has been abandoned due to time constraints.
		the windows version of python's parallelization is difficult due to the architecture of windows
			machines (threads vs. cpus; or something)
		note to look into this again when time permits.
		if the user is attempting this, note that I tried to use a module called "multiprocessing" 
			and imported is 'mp'.
		"""
		print('this has not been completed\nthe user is welcome to attempt this')

		# # ~~~~ attempt at parallel (windows) ~~~~
		# def run_cshore(i):
		# 	os.chdir(master_path + '/' + i)
		# 	files = os.listdir()
		# 	for ii in files:
		# 		if ii.endswith('infile'):
		# 			original_filename = ii[:]
		# 			os.rename(ii, 'infile')
		# 			os.system('G:\\FY18\\SRD_Sensitivity\\CSHORE\\cshore_usace_win.out')

		# def rename_infiles():
		# 	for i in model_run_names:
		# 		os.chdir(master_path + '/' + i)
		# 		files = os.listdir()
		# 		for ii in files:
		# 			if ii.endswith('infile'):
		# 				os.rename('infile', i + '.infile')

		# master_path = 'G:\\FY18\CSHORE\\BFx-CSHORE\\infiles'
		# os.chdir(master_path)
		# model_run_names = os.listdir()
		# for i in model_run_names:
		# 	if i == '.DS_Store':
		# 		model_run_names.remove('.DS_Store')

		# # create the CSHORE processes to be ran
		# processes = []
		# for i in model_run_names:
		# 	p = mp.Process(target=run_cshore, args=(i, ))
		# 	processes.append(p)

		# # start the processes
		# for p in processes:
		# 	p.start()

		# # end the processes
		# for p in processes:
		# 	p.join()

		# rename_infiles()

import os
import numpy as np
import h5py

class output_to_DAT_background(object):

	def init(self, h5_filename, meta_dict):
		self.meta_dict = meta_dict				#setting up meta dictionary values
		self.hdf5_to_DAT(h5_filename)			#converting h5 data to DAT files.

	def h5reader3(self, filename1, filename2, filename3):
		"""  
			-h5 file reader for storms from coastal hazards system data
			-user needs to know makeup of .h5 file (tree makeup: file1 -> file2 -> file3)
		"""
		with h5py.File(filename1, 'r') as hf:
			ret = hf.get(filename2+'/'+filename3)
			ret = np.array(ret)
		return ret
	
	def reverse_l_r(self, x_value, z_value,xoffset):
		"""
		reverses the order of arrays.
			beach-fx: seaward positive
			cshore: landward positive
		"""
		#~~~ x-values ~~~
		diff_temp = np.diff(x_value)
		diff_reverse = diff_temp[::-1]
		temp = np.cumsum(diff_reverse)
		#x_value = np.insert(temp, 0,0)
		x_value = xoffset-x_value[::-1]
                
		#~~~ z-values ~~~
		z_value = z_value[::-1]
		
		return x_value, z_value

	def hdf5_to_DAT(self, h5_filename):
		with h5py.File(h5_filename, 'r') as hf:					#reading profile/storm combinations in h5file
			dataset_names = list(hf.keys())
		
		os.chdir(self.meta_dict['outfile_directory_reach'])					#changing to dat path
		dat_filename = h5_filename.split('.')[0] + '.dat'		#dat filename comes from the h5 filename
		thefile = open(dat_filename, 'w')						#opening the dat file to write to

		for i in dataset_names:									#loop through each profile/storm combination
			init_profile = self.h5reader3(h5_filename, i, 'Initial Profile')	#reading the datafrom the h5file
                        fin_profile = self.h5reader3(h5_filename, i, 'Final Profile')
			max_profile = self.h5reader3(h5_filename, i, 'Max Prof Elev')
			min_profile = self.h5reader3(h5_filename, i, 'Min Prof Elev')
			max_wav = self.h5reader3(h5_filename, i, 'Max Wave Ht')
                        max_elv = self.h5reader3(h5_filename, i, 'Max Water Elev+Setup')

			init_profile[:,0], init_profile[:,1] = self.reverse_l_r(init_profile[:,0], init_profile[:,1],init_profile[-1,0]) #swithcing from cshore orientation to beach-fx orientation (seaward positive)
			fin_profile[:,0], fin_profile[:,1] = self.reverse_l_r(fin_profile[:,0], fin_profile[:,1],init_profile[-1,0])
			max_profile[:,0], max_profile[:,1] = self.reverse_l_r(max_profile[:,0], max_profile[:,1],init_profile[-1,0])
			min_profile[:,0], min_profile[:,1] = self.reverse_l_r(min_profile[:,0], min_profile[:,1],init_profile[-1,0])
			max_wav[:,0], max_wav[:,1] = self.reverse_l_r(max_wav[:,0], max_wav[:,1],init_profile[-1,0])
			max_elv[:,0], max_elv[:,1] = self.reverse_l_r(max_elv[:,0], max_elv[:,1],init_profile[-1,0])

			profile = i.split('-')[0]								#reading profile name
			storm = i.split('-')[1]									#reading storm name

			thefile.write('Initial Profile: %s, %s' %(profile, storm))	#writing to dat file
			thefile.write('\n%s\n' %len(init_profile[:,0]))
			for i, _ in enumerate(init_profile):
				thefile.write('%8.4f %8.4f\n' %(init_profile[i, 0], init_profile[i, 1]))
			
			thefile.write('Final Profile: %s, %s\n' %(profile, storm))
			thefile.write('%s\n' %len(fin_profile[:,0]))
			for i, _ in enumerate(fin_profile):
				thefile.write('%8.4f %8.4f\n' %(fin_profile[i, 0], fin_profile[i, 1]))

			thefile.write('Max Prof Elev: %s, %s\n' %(profile, storm))
			thefile.write('%s\n' %len(max_profile))
			for i, _ in enumerate(max_profile):
				thefile.write('%8.4f %8.4f\n' %(max_profile[i, 0], max_profile[i, 1]))

			thefile.write('Min Prof Elev: %s, %s\n' %(profile, storm))
			thefile.write('%s\n' %len(min_profile))
			for i, _ in enumerate(min_profile):
				thefile.write('%8.4f %8.4f\n' %(min_profile[i, 0], min_profile[i, 1]))
			
			thefile.write('Max Wave Ht: %s, %s\n' %(profile, storm))
			thefile.write('%s\n' %len(max_wav))
			for i, _ in enumerate(max_wav):
				thefile.write('%8.4f %8.4f\n' %(max_wav[i, 0], max_wav[i, 1]))

			thefile.write('Max Water Elev+Setup: %s, %s\n' %(profile, storm))
			thefile.write('%s\n' %len(max_elv))
			for i, _ in enumerate(max_elv):
				thefile.write('%8.4f %8.4f\n' %(max_elv[i, 0], max_elv[i, 1]))


		thefile.close()

from __future__ import division
import os
import numpy as np

class PopulateProfileSpace(object):
	def __init__(self):

		self.cshore_profiles = {}

	def init(self, meta_dict, profile_dict, reach_num, reach):
		self.meta_dict = meta_dict					#setting up self referenced values (sounds post-modern)
		self.profile_dict = profile_dict

		for i in os.listdir(self.meta_dict['work_directory']): 	#loop through work directory to find submerged profile
			if reach in i:										#reach name must be in submerged profile name
				self.submerged_file = i 						#setting saving submerged profile
		if not self.submerged_file:								#else, raise error (get mad)
			raise ValueError("Submerged profile not found. Naming convention: 'ReachName_submerged_profile.txt")

		self.setup_profile_max_min2(reach_num, reach)			#converting feet (from input) to meters (for cshore)
		self.create_profile_space2(reach_num, reach)			#compute profile space (variations between max and min profiles)
		self.submerged_file = None								#reset the submerged profile afterwards (otherwise, the error won't raise above, and self.submerged_file is stored indefinitely; not good in this po-mo code)
		
		return self.cshore_profiles

	def reverse_l_r(self, x_value, z_value):
		"""
		reverses the order of arrays.
			beach-fx: seaward positive
			cshore: landward positive
		"""
		#~~~ x-values ~~~
		diff_temp = np.diff(x_value) 				#step in x-values
		diff_reverse = diff_temp[::-1]				#reversing the step values above
		temp = np.cumsum(diff_reverse)				#computing cumulative sum on differences
		x_value = np.insert(temp, 0,0)				#adding the initial zero-value
		
		#~~~ z-values ~~~
		z_value = z_value[::-1]						#reversing z-values
		
		return x_value, z_value

	def setup_profile_max_min2(self, reach_num, reach):
		"""
		 convert input values to m. 
		"""
		self.uw = self.profile_dict['width_upland'][reach_num]*.3048
		self.ue = self.profile_dict['height_upland'][reach_num]*.3048
		self.be = self.profile_dict['height_berm'][reach_num]*.3048

		self.dh = [i*.3048 for i in self.profile_dict['height_dune'][reach_num]]
		self.dw = [i*.3048 for i in self.profile_dict['width_dune'][reach_num]]
		self.bw = [i*.3048 for i in self.profile_dict['width_berm'][reach_num]]
		
		self.ds = self.profile_dict['slope_dune'][reach_num]
		self.fs = self.profile_dict['slope_foreshore'][reach_num]
	

	def create_profile_space2(self, reach_num, reach):
		"""
		create profile space
		"""
		self.cshore_profiles['%s'%reach] = {}

		# setting up submerged profile
		os.chdir(self.meta_dict['work_directory'])
		submergedpath = os.path.join(self.meta_dict['work_directory'], self.submerged_file)
		sub = np.genfromtxt(submergedpath, delimiter = '\t')
		sub = sub*.3048

		x_sub = np.array(sub[:,0])		#x submerged
		z_sub = np.array(sub[:,1])		#z submerged

		for i_dh in self.dh:
			for i_dw in self.dw:
				for i_bw in self.bw:
					i_dw_temp = int(round(i_dw/.3048))		#for file naming convention
					i_bw_temp = int(round(i_bw/.3048))		#for file naming convention

					profile_name = '{:0>4.1f}_{:0>3d}_{:0>3d}'.format(i_dh/.3048, i_dw_temp, i_bw_temp)
					self.cshore_profiles['%s'%reach][profile_name] = {}
					self.cshore_profiles['%s'%reach][profile_name] = {}

					#stepping through and creating idealized profile (from left to right - Beach-fx input). x1 corresponds to z1, and etc.
					x1 = 0
					x2 = self.uw
					x3 = x2 + ((i_dh - self.ue)/self.ds) 
					x4 = x3 + i_dw
					x5 = x4 + ((i_dh - self.be)/self.ds)
					x6 = x5 + i_bw
					x7 = x6 + ((self.be - z_sub[0])/self.fs)
					temp_x = np.array((x1, x2, x3, x4, x5, x6, x7))
					x_sub_temp = x_sub + x7			#shifting x_sub to start at end of the above profile

					z1 = self.ue
					z2 = self.ue
					z3 = i_dh
					z4 = i_dh
					z5 = self.be
					z6 = self.be
					z7 = z_sub[0]
					temp_z = np.array((z1, z2, z3, z4, z5, z6, z7))

					new_x = np.concatenate((temp_x, x_sub_temp))		#appending things to form one x and z-array
					new_z = np.concatenate((temp_z, z_sub))
					new_x, new_z = self.reverse_l_r(new_x, new_z)		#flipping arrays
					self.cshore_profiles['%s'%reach][profile_name]['x'] = new_x		#storing in dictionaries
					self.cshore_profiles['%s'%reach][profile_name]['z'] = new_z




	def create_profile_space_lhc(self):
		"""
		under development
		"""
		print('under development and testing')

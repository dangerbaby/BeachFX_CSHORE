import os
import numpy as np
from cshoreIO import cshoreIO

csio = cshoreIO()


class MakeInfiles(object):
	def __init__(self):
		self.infiles = {}

	def init(self, meta_dict, cshore_dict, profiles, storms):	
		self.meta_dict = meta_dict			#setting up dictionaries
		self.cshore_dict = cshore_dict
		self.profiles = profiles	
		self.storms = storms

		self.make_indirectory()				#creating (and moving to) an infile directory
		self.make_infiles()					#writing to infile directory


	def make_indirectory(self):
		for reach in self.profiles.keys():
			infile_directory = os.path.join(self.meta_dict['work_directory'], 'infiles', reach)
			if not os.path.exists(infile_directory):
				os.makedirs(infile_directory)
			os.chdir(infile_directory)


	def make_infiles(self):
		count = 0
		for reach in self.profiles.keys():				#loop through reach
			os.chdir(os.path.join(self.meta_dict['work_directory'], 'infiles', reach))		#navigate to infile directory
			for storm in self.storms.keys():			#loop through storms
				for profile in self.profiles[reach].keys():		#loop through profiles

					BC_dict = {}								#creating boundary condtion dictionary
					BC_dict['timebc_wave'] 	= self.storms[storm]['time']
					BC_dict['Hs']			= self.storms[storm]['Hmo']
					BC_dict['Hrms']			= self.storms[storm]['Hrms']   #note: I updated cshoreIO.py such that only 'Hrms' is read
					BC_dict['Tp']			= self.storms[storm]['tp']
					BC_dict['Wsetup']		= np.zeros(len(BC_dict['Tp']))		#not including wave setup
					BC_dict['swlbc']		= self.storms[storm]['surge']
					BC_dict['angle']		= np.zeros(len(BC_dict['Tp']))	   #not including wave angle (everything is shore normal)
					BC_dict['x']			= self.profiles[reach][profile]['x']
					BC_dict['x_p']			= np.zeros(len(BC_dict['x']))		#not including permeable layer
					BC_dict['zb']			= self.profiles[reach][profile]['z']
					BC_dict['zb_p']			= np.zeros(len(BC_dict['x']))		#np including permeable layer
					BC_dict['fw']			= np.zeros(len(BC_dict['x']))		#not including variable bed friction. assumed constant in cshore
					BC_dict['d50']			= self.profiles[reach][profile]['d50']
					self.meta_dict['Reach'] = reach 							#adding infomation to meta_dict
					self.meta_dict['Profile'] = profile
					self.meta_dict['Storm'] = storm
					fname = reach + '_' + profile + '-' + storm + '.infile' 	#the infile name

					csio.make_CSHORE_infile(fname, BC_dict, self.meta_dict, self.cshore_dict) 	#making the infile
			count += 1








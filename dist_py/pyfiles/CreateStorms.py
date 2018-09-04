from __future__ import division
import os
import numpy as np
import math
import datetime 


class CreateStorms(object):
	def __init__(self):
		self.cshore_storms = {}


	def init(self, meta_dict, tide_dict):
		self.meta_dict = meta_dict
		self.tide_dict = tide_dict
		self.storm_dict = {}
		self.storm_dict['storm_file_type'] = '.dat' 			#note this is a placeholder. if the read_storms_h5 is implemented, this value needs to be moved to 1_file_creation.py

		if self.storm_dict['storm_file_type'] == '.h5':			#note: this feature hasn't been implemented yet; defaults to "elif" below
			self.read_storms_h5(storm_file, storm_name)

		elif self.storm_dict['storm_file_type'] == '.dat':
			for file in os.listdir(self.meta_dict['work_directory']):
				if file.endswith('.dat'):
					self.read_storms_dat(file)					#reading storms with file extension ".dat"
		return self.cshore_storms
	
	# ~~~ general functions ~~~
	def h5reader3(filename1, filename2, filename3):
		"""  
			-h5 file reader for storms from coastal hazards system data
			-user needs to know makeup of .h5 file (tree makeup: file1 -> file2 -> file3)
		"""
		with h5py.File(filename1, 'r') as hf:
			ret = hf.get(filename2+'/'+filename3)
			ret = np.array(ret)
		return ret


	# ~~~ read storm data ~~~
	def read_storms_h5(self, storm_file, storm_name):
		"""
		reading storm data from hdf5 file
		"""
		print('you need to work on this - read_storms_h5')

		# os.chdir(self.storm_directory[0])

		# hmo = h5reader3(storm_file, storm_name, 'Zero Moment Wave Height')		#read zero-moment wave height
		# hrms = hmo/np.sqrt(2)													#zero-moment wave height to root-mean-square wave height
		# h_time = h5reader3(storm_file, storm_name, 'yyyymmddHHMM')
		# tp = h5reader3(storm_file, storm_name, 'Peak Period')
		# surge = h5reader3(storm_file, storm_name, 'Water Elevation')

		# time = np.linspace(0,(len(h_time)-1), len(h_time))*3600					#time in seconds (each step is an hour)

		# self.cshore_storms[storm_name]['Hmo'] = hmo
		# self.cshore_storms[storm_name]['Hrms'] = hrms
		# self.cshore_storms[storm_name]['tp'] = tp
		# self.cshore_storms[storm_name]['surge'] = surge
		# self.cshore_storms[storm_name]['time'] = time

		# return hrms, tp, surge, time

	def read_storms_dat(self, storm_file):
		"""
		reading storm data from dat file
		"""
		file_path = os.path.join(self.meta_dict['work_directory'], storm_file)		#path to file.

		data = np.genfromtxt(storm_file, skip_header = 1)	#reading data
		date = data[:,0]					#yyyymmddHHMM
		hmo = data[:,1]						#note: reading Hmo(or Hs) in meters here.
		hrms = hmo/np.sqrt(2)				# 	converting to hrms for cshore. still in meters.
		tp = data[:,2]						#period
		surge = data[:,3]					#surge elevation

		date = [datetime.datetime.strptime(str(int(i)), "%Y%m%d%H%M") for i in date]	#getting date/time in "python" format
		dt = self.dt_calc(date)					#calculating time step (assumes constant time step; seconds)
		time = np.arange(0, len(hmo)*dt, dt)	#calculating time array	(seconds)

		with open(storm_file) as f:
			storm_id = f.readline().splitlines()[0]
			storm_id = storm_id.split()[0]
		storm_name = 'STM' + storm_id
		
		self.add_tides(storm_name, time, surge, hmo, hrms, tp)			#adding tides


	def dt_calc(self, date):
		dt_dd = (date[1].day - date[0].day)*86400			#day step (converted to seconds)
		dt_hh = (date[1].hour - date[0].hour)*3600			#hour step (converted to seconds)
		dt_mm = (date[1].minute - date[0].minute)*60		#min step (converted to seconds)
		return dt_dd + dt_hh + dt_mm						#returning sum of above (in seconds)

	def add_tides(self, storm_prfx, time, surge, hmo, hrms, tp):
		"""
		adding tidal contribution to surge
		"""
		w = 2*math.pi/(self.tide_dict['T']/24) 				#omega (1/day)
		time_days = time/86400								#converting time array from seconds to days
		max_ind =np.argmax(surge)							#index of max
		t_max = time_days[max_ind]							#time at max
		for i in self.tide_dict['phases']:									#loop through tide phases
			for j, obj in enumerate(self.tide_dict['amp']):				#loop through tide amplitudes
				tide = obj*np.sin(time_days*w + i*math.pi/2 -w*t_max)			#idealized tide with amplitude and shift applied
				storm_name = storm_prfx + '_TPh' + str(i) + '_TAmp' + str(j+1)	#update storm name for tide specific contribution

				self.cshore_storms[storm_name] = {}								#saving all to dictionary
				self.cshore_storms[storm_name]['Hmo'] = hmo
				self.cshore_storms[storm_name]['Hrms'] = hrms
				self.cshore_storms[storm_name]['tp'] = tp
				self.cshore_storms[storm_name]['surge'] = surge+tide 			#adding the tide contribution to surge
				self.cshore_storms[storm_name]['time'] = time

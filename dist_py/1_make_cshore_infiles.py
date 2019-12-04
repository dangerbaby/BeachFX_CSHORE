"""
this script is used to generate the infiles for CSHORE runs that will be used in Beach-fx modeling.
	-the infiles will be written to the following directory structure:
		../work/infiles/"reach"/infiles
	-the user should not remove the infiles from this location until the cshore runs have been completed. 
	-information about the required input values can be found throughout this script.
user input begins following "BEGIN USER INPUT"
	**Note that the units of the user input vary for Beach-fx (US) and CSHORE (SI)
	-the script performs necessary unit conversions assuming the input units are correct. 

Python scripts (except cshoreIO.py) written by 
	Dylan R. Sanderson
	Coastal and Hydraulics Laboratory
	Engineer Research and Development Center
	Vicksburg, MS
Work flow and tide creation from Brad Johnson. 
May, 2018
"""
import os
import sys
import tarfile

# ~~~ creating empty dictionaries ~~~
cshore_dict = {}
profile_dict = {}
tide_dict = {}

# ~~~~~~~~~~~ BEGIN USER INPUT ~~~~~~~~~~~
profile_dict['names'] 		= ['Reach1', 'Reach3']				#name of reaches specified as string (e.g. 'Reach1', 'Reach3', ...)
profile_dict['height_dune'] 	= [[10, 12], [9.9, 10.5]]  			#dune height (ft.)
profile_dict['width_dune'] 	= [[10] , [12, 13]]				#dune width (ft.)
profile_dict['width_berm'] 	= [[100, 150], [120]]				#berm width (ft.)
profile_dict['width_upland'] 	= [200, 220]					#upland width (ft.)
profile_dict['height_upland'] 	= [6, 7]					#upland elevation (ft.)
profile_dict['slope_dune'] 	= [0.25, 0.25]					#dune slope
profile_dict['height_berm'] 	= [4, 5]					#berm elevation (ft.)
profile_dict['slope_foreshore'] = [0.2, 0.2]					#foreshore slope
profile_dict['d50']	        = [0.3, 0.4]					#d_50 (mm.)


cshore_dict['dx'] 	= 1				#CSHORE grid spacing (m)
cshore_dict['gamma'] 	= 0.7			        #shallow water ratio of wave height to water depth 
cshore_dict['effb']	= 0.002				#suspension efficiency due to breaking eB

tide_dict['amp'] 	= [.15]				#tidal amplitude (m.)
tide_dict['T'] 	= 12.5					#tidal period (hrs.); typically 12.5 for semi-diurnal
tide_dict['phases'] 	= [1]		 	        #tidal phase; 1=high, 2=mid-falling, 3=low, 4=mid-rising
# ~~~~~~~~~~~ END USER INPUT ~~~~~~~~~~~



# ~~~ starting script ~~~
current_path = os.path.abspath(os.path.dirname(__file__))	       #reading current path
pypath = os.path.join(current_path, "pyfiles")                         #finding ../pyfiles subdirectory
sys.path.insert(0, pypath)					       #adding pyfiles subdirectory to this working path

from PopulateProfileSpace import PopulateProfileSpace		       #importing and setting up "background" pyfiles
from CreateStorms import CreateStorms
from MakeInfiles import MakeInfiles
PPS = PopulateProfileSpace()
strms = CreateStorms()
mkInfiles = MakeInfiles()

meta_dict = {}
meta_dict['work_directory'] = os.path.join(current_path, "work")	#setting up ../work directory

for reach_num, reach in enumerate(profile_dict['names']):		#loop through reaches
	profiles = PPS.init(meta_dict, profile_dict, reach_num, reach)	#populating profile parameter space for reach
	if reach_num == 0:						#if first time through loop, setting up storms
		storms = strms.init(meta_dict, tide_dict)

#printing some numbers that may be beneficial
print('Number of Reaches: %s' %len(profiles.keys()))
prof_in_reach = [(len(profiles[i].keys())) for i in profiles.keys()]	#calc number of profiles in each reach
print('Number of Profiles in each reach: %s' %prof_in_reach)		#print num profiles in each reach
print('Number of Storms: %s' %len(storms.keys()))			#print num storms
tot_num = sum([len(storms.keys()) * i for i in prof_in_reach])		#calc number of profile/storm combinations
print('\nWriting %s CSHORE infiles' %tot_num)				#print number of profile/storm combinations

mkInfiles.init(meta_dict, cshore_dict, profiles, storms)		#making infiles for each profile/storm combination

os.chdir(current_path)                                                  #making the hpc files  
tar = tarfile.open("to_hpc.tgz", "w:gz", dereference=True)
tar.add("run_all_infiles_hpc")
tar.add("work/infiles")
tar.add("executables")
tar.add("submit_script_onyx.pbs")
tar.close()

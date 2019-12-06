import os
import sys

# ~~~ begin script ~~~
current_path = os.path.abspath(os.path.dirname(__file__))			#adding pyfiles subdirectory to this working path
pypath = os.path.join(current_path, "pyfiles")
sys.path.insert(0, pypath)

from run_cshore_background import run_cshore_background				#loading background pyfiles
rcb = run_cshore_background()

meta_dict = {}														#setting up dictionaries
meta_dict['work_directory'] = os.path.join(current_path, "work")
meta_dict['infile_directory'] = os.path.join(meta_dict['work_directory'], 'infiles')
meta_dict['outfile_directory'] = os.path.join(meta_dict['work_directory'], 'outfiles')
meta_dict['exe_directory'] = os.path.join(current_path, "executables")

reaches = []
if not reaches:													#if the reaches list is blank, 
	reaches = os.listdir(meta_dict['infile_directory'])			# read all reaches in infile directory
	reaches = [f for f in reaches if not f.startswith('.')]		#remove hidden files that start with '.'

if not os.path.exists(meta_dict['outfile_directory']): 	#check if output path exists
	os.makedirs(meta_dict['outfile_directory'])			#if not, make directory

for reach in reaches:												#loop through reaches
	os.chdir(os.path.join(meta_dict['infile_directory'], reach))	#change to reach directory
	if not os.path.exists(os.path.join(meta_dict['outfile_directory'], reach)):
		os.makedirs(os.path.join(meta_dict['outfile_directory'], reach))
	meta_dict['outfile_directory_reach'] = os.path.join(meta_dict['outfile_directory'], reach)
	

	infiles = os.listdir(os.getcwd())
	rcb.init(meta_dict, reach)
        

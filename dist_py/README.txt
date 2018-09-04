# BFx-CSHORE
*Note that the current structure of this directory should not be modified. If it is, the
python scripts may not operate correctly.*

This directory contains a set of python scripts (2.7 and 3.6) that are used to setup and run cshore 
prior to use in Beach-fx. In most cases, after preprocessing cshore data (submerged profiles
and storm events), the user only needs to modify and run the following python files: 
	1_make_cshore_infiles.py - creates cshore infiles
	2_run_cshore.py - runs cshore and writes necessary output information to HDF5 file
	3_make_dat_file.py - converts HDF5 file to the appropriate DAT file for import to Beach-fx. 
The prefix in each of the above python files indicates the order that the files should be ran. 
Additional comments are provided throughout the code. 

Additional sub-directories are as follows:
	-cshore_executables: contains CSHORE executables for both Windows (default) and 
		linux (can be updated in ..\pyfiles\run_cshore_background.py 
	-pyfiles: background python files that are called on at runtime. these should 
		be modified only if extending current capabilities of this set of scripts.  
	-work: all required input files (submerged profiles and storm events). the cshore 
		infiles will be written to a new folder in this directory following use of 
		1_file_creation.py.

The required python modules are as follows:
	-os
	-sys
	-math
	-datetime
	-numpy
	-h5py
Of the six, only 'numpy' and 'h5py' are not native to python and need to be installed
in the user's python environment.



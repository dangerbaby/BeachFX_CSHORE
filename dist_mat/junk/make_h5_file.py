import os
import sys
import glob
import h5py
import numpy as np
from pyfiles import cshore_in_out 

reachname = (sys.argv[1])
print "Making the h5 file for %s" %reachname
h5filename = reachname + '.h5'	                                           #sets h5 filename
h5file = h5py.File('work/outfiles/'+reachname+'/'+h5filename, 'w')         #creates h5 filename

runs = glob.glob('work/infiles/'+reachname+'/*.OBPROF') # see what cshore runs have been completed

for run in runs:
    global_name = os.path.splitext(run)[0]
    infile_name =  os.path.relpath(global_name,'work/infiles/'+reachname)
    print 'Inside make_h5_file'+infile_name
    results=cshore_in_out.read_CSHORE_results(global_name)
    profile_storm = h5file.create_group(infile_name)   #creates a group for the profile/storm combination

    init_data = np.column_stack((np.array(results['x_morpho'])/.3048, np.array(results['initial_profile'])/.3048))
    fin_data = np.column_stack((np.array(results['x_morpho'])/.3048, np.array(results['final_profile'])/.3048))
    max_data = np.column_stack((np.array(results['x_morpho'])/.3048, np.array(results['max_profile_elev'])/.3048))
    min_data = np.column_stack((np.array(results['x_morpho'])/.3048, np.array(results['min_profile_elev'])/.3048))
    setup_data = np.column_stack((np.array(results['x_hydro'])/.3048, np.array(results['max_water_elevation_plus_setup'])/.3048))
    maxwave_data = np.column_stack((np.array(results['x_hydro'])/.3048, np.array(np.sqrt(2.)*results['max_hrms'])/.3048))

    dset_init_profile = profile_storm.create_dataset('Initial Profile', data = init_data)		#writing results to h5file
    dset_init_profile = profile_storm.create_dataset('Final Profile', data = fin_data)		#writing results to h5file
    dset_max_profile  = profile_storm.create_dataset('Max Prof Elev', data = max_data)
    dset_min_profile  = profile_storm.create_dataset('Min Prof Elev', data = min_data)
    dset_setup        = profile_storm.create_dataset('Max Water Elev+Setup', data = setup_data)
    dset_max_wave     = profile_storm.create_dataset('Max Wave Ht', data = maxwave_data)


h5file.close()					#self-explanatory


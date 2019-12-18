import os
import sys
import glob
import numpy as np
from pyfiles import cshore_in_out 

reachname = (sys.argv[1])
print "Making the dat file for %s" %reachname


dat_filename = reachname + '.dat'		#dat filename comes from the h5 filename
datfile = open('work/outfiles/'+reachname+'/'+dat_filename, 'w')	   #opening the dat file to write to


runs = sorted(glob.glob('work/infiles/'+reachname+'/*.OBPROF')) # see what cshore runs have been completed

for run in runs:
    global_name = os.path.splitext(run)[0]
    infile_name =  os.path.relpath(global_name,'work/infiles/'+reachname)
    print infile_name
    results=cshore_in_out.read_CSHORE_results(global_name)

    init_data = np.column_stack((np.array(results['x_morpho'])/.3048, np.array(results['initial_profile'])/.3048))
    fin_data = np.column_stack((np.array(results['x_morpho'])/.3048, np.array(results['final_profile'])/.3048))
    max_data = np.column_stack((np.array(results['x_morpho'])/.3048, np.array(results['max_profile_elev'])/.3048))
    min_data = np.column_stack((np.array(results['x_morpho'])/.3048, np.array(results['min_profile_elev'])/.3048))
    setup_data = np.column_stack((np.array(results['x_hydro'])/.3048, np.array(results['max_water_elevation_plus_setup'])/.3048))
    maxwave_data = np.column_stack((np.array(results['x_hydro'])/.3048, np.array(np.sqrt(2.)*results['max_hrms'])/.3048))

    init_data = init_data[::-1] # reversing the direction
    fin_data = fin_data[::-1] # reversing the direction
    max_data = max_data[::-1] # reversing the direction
    min_data = min_data[::-1] # reversing the direction
    setup_data = setup_data[::-1] # reversing the direction
    maxwave_data = maxwave_data[::-1] # reversing the direction
    
    profile = infile_name.split('-')[0] #reading profile name
    storm = infile_name.split('-')[1]									#reading storm name

    datfile.write('Initial Profile: %s, %s' %(profile, storm))	#writing to dat file
    datfile.write('\n%s\n' %len(init_data[:,0]))
    for i, _ in enumerate(init_data):
	datfile.write('%8.4f %8.4f\n' %(init_data[0,0]-init_data[i, 0], init_data[i, 1]))
    #
    datfile.write('Final Profile: %s, %s\n' %(profile, storm))
    datfile.write('%s\n' %len(fin_data[:,0]))
    for i, _ in enumerate(fin_data):
	datfile.write('%8.4f %8.4f\n' %(fin_data[0,0]-fin_data[i, 0], fin_data[i, 1]))
    #
    datfile.write('Max Prof Elev: %s, %s\n' %(profile, storm))
    datfile.write('%s\n' %len(max_data[:,0]))
    for i, _ in enumerate(fin_data):
	datfile.write('%8.4f %8.4f\n' %(max_data[0,0]-init_data[i, 0], max_data[i, 1]))
    #
    datfile.write('Min Prof Elev: %s, %s\n' %(profile, storm))
    datfile.write('%s\n' %len(min_data[:,0]))
    for i, _ in enumerate(min_data):
	datfile.write('%8.4f %8.4f\n' %(min_data[0,0]-init_data[i, 0], min_data[i, 1]))
    #
    datfile.write('Max Wave Ht: %s, %s\n' %(profile, storm))
    datfile.write('%s\n' %len(maxwave_data[:,0]))
    for i, _ in enumerate(maxwave_data):
	datfile.write('%8.4f %8.4f\n' %(init_data[0,0]-maxwave_data[i, 0], maxwave_data[i, 1]))
    #
    datfile.write('Max Water Elev+Setup: %s, %s\n' %(profile, storm))
    datfile.write('%s\n' %len(setup_data))
    for i, _ in enumerate(setup_data):
	datfile.write('%8.4f %8.4f\n' %(init_data[0,0]-setup_data[i, 0], setup_data[i, 1]))


    

datfile.close()					#self-explanatory


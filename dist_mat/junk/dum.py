import os
import sys
import h5py
import numpy as np
import glob
from pyfiles import cshore_in_out 

reachname = 'Reach1'
print "Making the h5 file for %s" %reachname


# now make new h5 file
runs = glob.glob('work/outfiles/'+reachname+'/*.OBPROF')

global_name = os.path.splitext(runs[3])[0]
infile_name =  os.path.relpath(global_name,'work/outfiles/'+reachname)
#print global_name
#print infile_name
results=cshore_in_out.read_CSHORE_results(global_name)
print results.keys()
#print np.sqrt(2)*results['max_hrms']/.3048

h5filename    = reachname + 'brad.h5'              #sets h5 filename
h5file        = h5py.File(h5filename, 'w')         #creates h5 filename
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

# load up Dylans version for comparision
print 'Dylans h5:'
with h5py.File('Reach1.h5', 'r') as hf:					#reading profile/storm combinations in h5file
    dataset_names = list(hf.keys())
    group = hf[hf.keys()[0]]
    for key2 in group.keys():
        print(key2)

for i in dataset_names:						#loop through each profile/storm combination
    print i
    with h5py.File('Reach1.h5', 'r') as hf:
	#ret = hf.get(i+'/'+'Max Wave Ht')
        #ret = hf.get(i+'/'+'Initial Profile')
        ret = hf.get(i+'/'+'Max Wave Ht')
	ret = np.array(ret)
        print(ret)


# load up my version for comparision
print 'My h5:'
with h5py.File(h5filename, 'r') as h5file:	
    dataset_names = list(h5file.keys())

for i in dataset_names:						#loop through each profile/storm combination
    print i
    with h5py.File(h5filename, 'r') as hf:
        #ret = hf.get(i+'/'+'Initial Profile')
        ret = hf.get(i+'/'+'Max Wave Ht')
	ret = np.array(ret)
        print(ret)














exit()

with h5py.File('Reach1.h5', 'r') as hf:					#reading profile/storm combinations in h5file
    dataset_names = list(hf.keys())

print(dataset_names[0])

for i in dataset_names:						#loop through each profile/storm combination
    print i
    with h5py.File('Reach1.h5', 'r') as hf:
	ret = hf.get(i+'/'+'Max Wave Ht')
	ret = np.array(ret)
	#return ret
    print(ret)

    #max_wav = h5reader3('Reach1.h5', i, 'Max Wave Ht')



exit()

print(f.keys()[0])
group = f[f.keys()[0]]
for key2 in group.keys():
    print(key2)



    

with h5py.File('dum.h5', 'w') as fw: # try writing to this 
    arr = np.random.randn(1000)
    fw.create_dataset(f.keys()[0],data = arr)
    #fw.create_dataset(f.keys()[0], data = arr)
    #dum = fw.create_dataset("mydataset",100)
    print(fw.keys()[0])
    #group = fw[fw.keys()[0]]
    #for key2 in group.keys():
    #    print(key2)
    #fw.fclose()



import numpy as np

def read_CSHORE_results(fn):
    print ('inside read_CSHORE_results with fn '+fn)
    #####################first get the morpho####################
    with open(fn+'.OBPROF', 'r') as fid:
        tot = fid.readlines()
    fid.close()
    tot = np.asarray(list(map(lambda s: s.strip(), tot)))
    timeall = []
    zball = []
    ii = 0
    rowind = 0
    while rowind<len(tot):
        ii = ii+1
        row1 = tot[rowind]
        #print ii,row1
        N = int(row1.split()[1])
        tme = float(row1.split()[2])
        timeall = np.append(timeall,tme)
        dum = tot[rowind+1:rowind+N+1]
        rowind = rowind+N+1
        x = np.zeros(N)
        zb = np.zeros(N)
        for ss in range(0, N):
	    x[ss] = float(dum[ss].split()[0])
	    zb[ss] = float(dum[ss].split()[1])
        if ii==1:
            zball = np.transpose(zb)
            #print N,np.shape(zball)
            #print zball
        else:
            zball = np.vstack((zball,np.transpose(zb)))
    results = {'x_morpho':x}
    #results['time_morpho']      = timeall
    results['initial_profile']  = zball[0]
    results['final_profile']    = zball[-1]
    results['max_profile_elev'] = np.amax(zball,axis=0)
    results['min_profile_elev'] = np.amin(zball,axis=0)

    ####################now get the hydro####################
    Nmorpho = N
    with open(fn+'.OSETUP', 'r') as fid:
        tot = fid.readlines()
    fid.close()
    tot = np.asarray(list(map(lambda s: s.strip(), tot)))
    timeall = []
    ii = 0
    rowind = 0
    while rowind<len(tot):
        ii = ii+1
        row1 = tot[rowind]
        #print ii,row1
        N = int(row1.split()[1])
        tme = float(row1.split()[2])
        timeall = np.append(timeall,tme)
        dum = tot[rowind+1:rowind+N+1]
        rowind = rowind+N+1
        setup = np.zeros(Nmorpho)-999.
        hrms = np.zeros(Nmorpho)-999.
        for ss in range(0, N):
	    setup[ss] = float(dum[ss].split()[1])
            hrms[ss] = np.sqrt(8)*float(dum[ss].split()[3])
        if ii==1:
            setupall = np.transpose(setup)
            hrmsall = np.transpose(hrms)
            #print N,np.shape(setupall)
            #print setupall
        else:
            setupall = np.vstack((setupall,np.transpose(setup)))
            hrmsall = np.vstack((hrmsall,np.transpose(hrms)))

    #results['time_hydro'] = timeall
    maxsetup = np.amax(setupall,axis=0)
    maxhrms = np.amax(hrmsall,axis=0)
    mask = maxhrms >= -100.
    maxhrms = maxhrms[mask]
    maxsetup = maxsetup[mask]
    x_hydro = x[mask]
    
    results['x_hydro'] = x_hydro
    results['max_water_elevation_plus_setup'] = maxsetup
    results['max_hrms'] = maxhrms
    
    #print results['max_hrms']

    return(results)

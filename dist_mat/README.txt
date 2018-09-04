
1) Make reach and model run data

   -separate domain into N blocks well represented by a single
    transect, name them Reach1, Reach2, ... ReachN.  Or name them
    whatever you want without spaces or underscores.
   
   -For existing conditions, use judgment to fix beach parameters such
    as dune height, dune width, berm width, etc to best describe the
    profiles for each reach in units of ft.  Use these idealized
    params as your first entries in the inp structure.

   -The project options are represented as arrays in the inp structure
    for height_dune, width_dune, and width_berm.  For instance a
    profile named Reach1 has an existing dune of 10 ft, and the
    options to build it to 11 and 12 are under consideration.  Reach2
    has a height of 9.5ft with the option to build to 10.5.  These
    options would be represented in the inp block in
    first_make_infiles as

inp.names       = {'Reach1' 'Reach2'}; 
inp.height_dune = {{10 11 12} {9.9 10.5}};
   
    Note the two sets of inner braces for height_dune are required
    because there are two reaches.
 
   -Provide the grain size for CSHORE as well as gamma, effb, where
    gamma is the saturated wave height to depth ratio and effb is an
    efficiency parameter ~.002.

   -Idealized tides are modeled as monochromatic water level
    variations and with input amplitudes, period, and
    phasing. Variation in tidal amplitudes is appropriately modeled
    with specification of two or more tidal amplitudes with values
    provided for small and large amplitudes, for instance.  The
    phasing of the tides with respect to the time of storm surge max
    remains random, however, and one approach is to run morphology
    predictions for several possibilities of phasing.  The system will
    automatically provide tidal variation with phasing relative to the
    time of max storm surge dictated by the tidal.phases variable
    where 1=max,2=falling,3=min,4=rising.  For example, to model tides
    with amplitudes of 0.5 and 1.2 m including cases of tides at max
    and tides at min:

tides.amp = [.5 1.2]; % in m per normal 
tides.T = 12.5; % Period of tides in hrs.  Typical semi-diurnal tide is about 12.5 hrs
tides.phases = [1 3]; % 1=max,2=falling,3=min,4=rising



   -Each reach must have a text file containing bathymetry associated
    with each reach.  The data should be in two columns: x z in units
    of feet with data starting near MSL and oriented positive
    offshore.  Name these files Reach1_submerged_profile.txt,
    Reach2_submerged_profile.txt, etc and put them in the work
    directory.


2) Make storms

   -An arbitrary number of storms hydrograph are provided as text
    files within the work directory, and any file with name storm*.dat
    is imported in this step.  Each file must have a 3-digit id as
    the first line of the file followed my two 4 columns of data: date
    Hs T water_level where date is in yyyymmddHHMM format, Sig wave
    height Hs [m], Period T [s], and water level [m].  The first
    several lines of an example storm with id of 204:

204 
200007120600 0.082157 2.911990 0.134639
200007120700 0.083399 2.906840 0.138414
200007120800 0.084491 2.911167 0.140420
200007120900 0.086214 2.909698 0.140830
200007121000 0.067202 2.947738 0.143338
.
.     
.

3) Execute first_make_cshore_infiles: Makes the infile dir structure and
populates it with the CSHORE infiles.  You can plot_all_profiles at
this point if you wish.


4) Execute second_run_cshore: All of the CSHORE infiles are discovered and
run sequentially.  The pertinent output results are saved in a
outfiles directory, that is created automatically.  The optional
plot_cshore_results script can be used at this point to create a plot
of pre and post profiles for each run.

4) Execute third_make_dat file: All CSHORE results are discovered and a
separate dat file designed for use with BeachFX is created for each
reach





    

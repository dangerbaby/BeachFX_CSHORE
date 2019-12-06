clear all
close all
addpath 'mfiles' 

iclean = 1; % iclean = 1 to remove all existing results in infile directory   
if iclean ;[j1,j1,j1]=rmdir('./work/infiles','s');clear j1 iclean;end

%START user inputs
inp.names       = {'Reach1' 'Reach3'}; 
inp.height_dune = {{10 12} num2cell(9.9:.02:10.5)}; %[ft]
inp.height_dune = {{10 12} {9.9 10.5}}; %[ft]
inp.height_dune = {{10} {9.9}}; %[ft]
inp.width_dune  = {10 {12 13}}; %[ft]
inp.width_berm  = {{100 150} 120}; %[ft]
inp.width_upland  = {200 220}; %[ft]
inp.height_upland  = {6 7}; %[ft]
inp.slope_dune  = {.25 .25};
inp.height_berm  = {4 5}; %[ft]
inp.slope_foreshore  = {.2 .2};
cshore.dx = 2; % [m] default 1
cshore.gamma = .7; % default .7
cshore.d50 = {.3 .4}; % [mm]
cshore.effb = .002; % default .002 
tides.amp = [.5]; % [m] 
tides.T = 12.5; % [hr] Period of tides.  Typical semi-diurnal is 12.5 hrs
tides.phases = [1]; % 1=max,2=falling,3=min,4=rising
%END user inputs

reaches=find_all_combos(inp);
reaches = make_profiles(reaches);
storms = make_storms(tides);
make_infiles(tides,reaches,storms,cshore);
tar('to_hpc.tgz',{'./work/infiles' 'executables' 'run_all_infiles_hpc' 'submit_script_onyx.pbs'});


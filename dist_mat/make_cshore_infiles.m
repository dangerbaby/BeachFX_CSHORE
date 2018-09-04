clear all
close all
addpath 'mfiles' 

iclean = 1; % iclean = 1 to remove all existing resultrs in infile directory   
if iclean ;[j1,j1,j1]=rmdir('./work/infiles','s');clear j1 iclean;end

% Start user inputs
inp.names       = {'Reach1' 'Reach3'}; 
inp.height_dune = {{10 12} {9.9 10.5}};
inp.width_dune  = {10 {12 13}};
inp.width_berm  = {{100 150} 120};
inp.width_upland  = {200 220};
inp.height_upland  = {6 7};
inp.slope_dune  = {.25 .25};
inp.height_berm  = {4 5};
inp.slope_foreshore  = {.2 .2};
cshore.dx = 1; % default 1
cshore.gamma = .7; % default .7
cshore.d50 = {.3 .4};
cshore.effb = .002; %default .002 
tides.amp = [.5]; % in m per normal 
tides.T = 12.5; % Period of tides in hrs.  Typical semi-diurnal tide is about 12.5 hrs
tides.phases = [1]; % 1=max,2=falling,3=min,4=rising
%END user inputs

reaches=find_all_combos(inp);
reaches = make_profiles(reaches);
storms = make_storms(tides);
make_infiles(tides,reaches,storms,cshore);
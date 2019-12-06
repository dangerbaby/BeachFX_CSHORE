
clear all

tic;
if exist('from_hpc.tgz','file')==2
  disp('untaring HPC results')
  untar('from_hpc.tgz')
  movefile('from_hpc.tgz','from_hpc.tgz.used')
end

dirnames = dir('./work/outfiles');
for i = 3:length(dirnames)
  %first check if the results are in raw OBPROF format
  obprofnames = dir(['./work/outfiles/',dirnames(i).name,'/*.OBPROF']);
  for j = 1:length(obprofnames)
    obprofname = [obprofnames(j).folder,'/',obprofnames(j).name(1:length(obprofnames(j).name)-7)];
    load(['work/infiles/',dirnames(i).name,'/',obprofnames(j).name(1:length(obprofnames(j).name)-7),'.mat'])
    results = load_results_bfx(obprofname);
    movefile([obprofname,'.OBPROF'],[obprofname,'.OBPROF.used'])
    movefile([obprofname,'.OSETUP'],[obprofname,'.OSETUP.used'])
    save([obprofname,'.mat'],'results','in')
  end
  
  
  fnames = dir(['./work/outfiles/',dirnames(i).name,'/*.mat']);
  fid = fopen(['./work/outfiles/',dirnames(i).name,'/',dirnames(i).name,'.dat'],'w');  
  for j = 1:1:length(fnames)
    disp(['working on /',dirnames(i).name,'/',fnames(j).name])
    load(['./work/outfiles/',dirnames(i).name,'/',fnames(j).name]);

    %write Initial Profile
    x = m2ft(flipud((in.x_offset-results.x)));
    x_off2 = x(1); % in ft so that we have 0 at first node!
    x = x-x_off2;
    z = m2ft(flipud((results.initial_profile)));
    fprintf(fid,'Initial Profile: %s\n',in.magic_text);
    fprintf(fid,'%d\n',length(z));
    fprintf(fid,'%8.4f %8.4f\n',[x z]');

    %write Final Profile
    z = m2ft(flipud((results.final_profile)));
    fprintf(fid,'Final Profile: %s\n',in.magic_text);
    fprintf(fid,'%d\n',length(z));
    fprintf(fid,'%8.4f %8.4f\n',[x z]');

    %write Max Prof Elev    
    z = m2ft(flipud((results.max_profile_elev)));
    fprintf(fid,'Max Prof Elev: %s\n',in.magic_text);
    fprintf(fid,'%d\n',length(z));
    fprintf(fid,'%8.4f %8.4f\n',[x z]');

    %write Min Prof Elev    
    z = m2ft(flipud((results.min_profile_elev)));
    fprintf(fid,'Min Prof Elev: %s\n',in.magic_text);
    fprintf(fid,'%d\n',length(z));
    fprintf(fid,'%8.4f %8.4f\n',[x z]');
    
    %write max Hs
    ind = ~isnan(results.max_hrms);
    Hs=sqrt(2)*m2ft(flipud(results.max_hrms(ind)));
    x = m2ft(flipud((in.x_offset-in.x(ind))'));
    x = x-x_off2;
    fprintf(fid,'Max Wave Ht: %s\n',in.magic_text); 
    fprintf(fid,'%d\n',length(Hs));
    fprintf(fid,'%8.4f %8.4f\n',[x Hs]');
    
    
    %write max water elevation
    ind = ~isnan(results.max_water_elevation_plus_setup);
    eta=m2ft(flipud(results.max_water_elevation_plus_setup(ind)));
    x = m2ft(flipud((in.x_offset-results.x(ind))));
    x = x-x_off2;
    fprintf(fid,'Max Water Elev+Setup: %s\n',in.magic_text); 
    fprintf(fid,'%d\n',length(eta));
    fprintf(fid,'%8.4f %8.4f\n',[x eta]');
    
  
  
  end
  fclose(fid);
  
  
  
  
end
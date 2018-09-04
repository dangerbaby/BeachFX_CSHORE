
clear all
dirnames = dir('./work/outfiles');
tic;
for i = 3:length(dirnames)
  fid = fopen(['./work/outfiles/',dirnames(i).name,'/',dirnames(i).name,'.dat'],'w');
  fnames = dir(['./work/outfiles/',dirnames(i).name,'/*.mat']);
  for j = 1:1:length(fnames)
    disp(['working on /',dirnames(i).name,'/',fnames(j).name])
    load(['./work/outfiles/',dirnames(i).name,'/',fnames(j).name]);

    %write Initial Profile
    x = m2ft(flipud((in.x_offset-results.x)));
    x_off2 = x(1); % in ft!
    x = x-x_off2;
    z = m2ft(flipud((results.initial_profile)));
    fprintf(fid,'Initial Profile: %s\n',in.magic_text);
    fprintf(fid,'%d\n',length(z));
    fprintf(fid,'%8.4f  %8.4f\n',[x z]');

    %write Final Profile
    z = m2ft(flipud((results.final_profile)));
    fprintf(fid,'Final Profile: %s\n',in.magic_text);
    fprintf(fid,'%d\n',length(z));
    fprintf(fid,'%8.4f  %8.4f\n',[x z]');

    %write Max Prof Elev    
    z = m2ft(flipud((results.max_profile_elev)));
    fprintf(fid,'Max Prof Elev: %s\n',in.magic_text);
    fprintf(fid,'%d\n',length(z));
    fprintf(fid,'%8.4f  %8.4f\n',[x z]');

    %write Min Prof Elev    
    z = m2ft(flipud((results.min_profile_elev)));
    fprintf(fid,'Min Prof Elev: %s\n',in.magic_text);
    fprintf(fid,'%d\n',length(z));
    fprintf(fid,'%8.4f  %8.4f\n',[x z]');
    
    %write max Hs
    ind = ~isnan(results.max_hrms);
    Hs=sqrt(2)*m2ft(flipud(results.max_hrms(ind)));
    x = m2ft(flipud((in.x_offset-in.x(ind))'));
    x = x-x_off2;
    fprintf(fid,'Max Wave Ht: %s\n',in.magic_text); 
    fprintf(fid,'%d\n',length(Hs));
    fprintf(fid,'%8.4f  %8.4f\n',[x Hs]');
    
    
    %write max water elevation
    ind = ~isnan(results.max_water_elevation_plus_setup);
    eta=m2ft(flipud(results.max_water_elevation_plus_setup(ind)));
    x = m2ft(flipud((in.x_offset-results.x(ind))));
    x = x-x_off2;
    fprintf(fid,'Max Water Elev+Setup: %s\n',in.magic_text); 
    fprintf(fid,'%d\n',length(eta));
    fprintf(fid,'%8.4f  %8.4f\n',[x eta]');
    
  
  
  end
  fclose(fid);
  
  
  
  
end
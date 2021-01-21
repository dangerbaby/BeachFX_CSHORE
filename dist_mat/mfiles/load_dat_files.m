function dat = load_dat_files

dirnames = dir('./work/outfiles');
for i = 3:length(dirnames)
  
  fnames = dir(['./work/outfiles/',dirnames(i).name,'/*.dat']);
  if isempty(fnames);disp('No dat file found');return;end
  fid = fopen(['./work/outfiles/',dirnames(i).name,'/',dirnames(i).name,'.dat'],'r');
  disp(['working on /',dirnames(i).name,'/',fnames(1).name])
  tot = textscan(fid,'%s','delimiter','\n');
  fclose(fid);
  tot = tot{:};

  dum =strfind(tot,'Initial');
  inds1 = find(~cellfun('isempty',dum));

  dum =strfind(tot,'Final');
  inds2 = find(~cellfun('isempty',dum));

  dum =strfind(tot,'Max Prof');
  inds3 = find(~cellfun('isempty',dum));

  dum =strfind(tot,'Min Prof');
  inds4 = find(~cellfun('isempty',dum));

  dum =strfind(tot,'Max Wav');
  inds5 = find(~cellfun('isempty',dum));

  dum =strfind(tot,'Max Water');
  inds6 = find(~cellfun('isempty',dum));

  for k = 1:length(inds1)
    inds = inds1;
    dat(k).name = cell2mat(tot(inds(k)));
    dat(k).name = dat(k).name(findstr(dat(k).name,':')+1:end);
    %initial prof
    numpts = str2num(cell2mat(tot(inds(k)+1)));
    dum= cellfun(@str2num,tot(inds(k)+2:inds(k)+2+numpts-1),'UniformOutput',false);
    dat(k).initial_profile=cell2mat(dum);
    %final prof
    inds = inds2;
    numpts = str2num(cell2mat(tot(inds(k)+1)));
    dum= cellfun(@str2num,tot(inds(k)+2:inds(k)+2+numpts-1),'UniformOutput',false);
    dat(k).final_profile=cell2mat(dum);
    %max prof
    inds = inds3;
    numpts = str2num(cell2mat(tot(inds(k)+1)));
    dum= cellfun(@str2num,tot(inds(k)+2:inds(k)+2+numpts-1),'UniformOutput',false);
    dat(k).max_profile=cell2mat(dum);
    %min prof
    inds = inds4;
    numpts = str2num(cell2mat(tot(inds(k)+1)));
    dum= cellfun(@str2num,tot(inds(k)+2:inds(k)+2+numpts-1),'UniformOutput',false);
    dat(k).min_profile=cell2mat(dum);
    %max wav
    inds = inds5;
    numpts = str2num(cell2mat(tot(inds(k)+1)));
    dum= cellfun(@str2num,tot(inds(k)+2:inds(k)+2+numpts-1),'UniformOutput',false);
    dat(k).max_wav=cell2mat(dum);
    %max water
    inds = inds6;
    numpts = str2num(cell2mat(tot(inds(k)+1)));
    dum= cellfun(@str2num,tot(inds(k)+2:inds(k)+2+numpts-1),'UniformOutput',false);
    dat(k).max_water=cell2mat(dum);
  
  end

end
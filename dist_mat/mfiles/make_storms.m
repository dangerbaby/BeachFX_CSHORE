function storm = make_storms(tides)

% expecting storm_???_ts.dat filenames contaning 4 columns:
%date Hs T eta
fnames = dir('./work/storm*.dat');
for i = 1:length(fnames)
  fid = fopen(['./work/',fnames(i).name],'r');
  id = textscan(fid,'%d',1);
  storm(i).id = id{:};
  tot = textscan(fid,'%s%f%f%f');
  storm(i).date=datenum((tot{1}),'yyyymmddHHMM');
  storm(i).Hs  =tot{2};
  storm(i).T  =tot{3};
  storm(i).storm_surge  =tot{4};
  fclose(fid);
end

% now add the tide phases 
w = 2*pi/(tides.T/24);%1/day
for i = 1:length(storm)
  [j1 j2] = max(storm(i).storm_surge);
  tmax = storm(i).date(j2);% in days
  cnt = 0;
  for j = tides.phases
    cnt = cnt+1;
    storm(i).normalized_tide(:,cnt) = sin(w*storm(i).date+j*pi/2 - w*tmax);
    %   storm(i).normalized_tide(:,2) = sin(w*storm(i).date+pi   - w*tmax);
    %   storm(i).normalized_tide(:,3) = sin(w*storm(i).date+3*pi/2-w*tmax);
    %   storm(i).normalized_tide(:,4) = sin(w*storm(i).date+      -w*tmax);
    % 
  end
  if 0
    figure(i)
    plot(storm(i).date,storm(i).storm_surge);hold all
    plot(storm(i).date,storm(i).normalized_tide(:,1),'k');hold all
  end
  
  
end




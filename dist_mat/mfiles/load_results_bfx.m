function out = load_results_bfx(fname)
if exist('fname')
  if isnumeric(fname)
    fname=[num2str(fname),'.'];
  elseif ischar(fname)
    fname=[fname,'.'];
  end

else
  fname = [];
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%a
params.iveg = 0;
params.isedav=0;

fid=fopen([fname,'OBPROF']);
cnt=0;
while 1
  tline = fgetl(fid);
  if ~ischar(tline), break, end
  cnt = cnt+1;
  tline = str2num(tline);
  if length(tline)==3;
    N = tline(2);
    tme = tline(3);
  elseif length(tline)==2;
    N = tline(1);
    tme=tline(2);
  end
  if (params.iveg&cnt>1)&params.isedav==0
    [tot]=fscanf(fid,'%f %f %f\n',[3,N])';
    morpho(cnt).ivegitated = tot(:,3);
  elseif params.isedav==1
    [tot]=fscanf(fid,'%f %f %f\n',[3,N])';
    morpho(cnt).zb_p = tot(:,3);
  else
    [tot]=fscanf(fid,'%f %f \n',[2,N])';
  end
  morpho(cnt).time = tme;
  morpho(cnt).x = tot(:,1);
  morpho(cnt).zb = tot(:,2);
end
fclose(fid);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

fid=fopen([fname,'OSETUP']);
%	  WRITE(22,1500) XB(J),(WSETUP(J)+SWLBC(IWAVE)),H(J),SIGMA(J)
cnt=0;
while 1
  tline = fgetl(fid);
  if ~ischar(tline), break, end
  cnt = cnt+1;
  tline = str2num(tline);
  if tline(1)==1
    N = tline(2);tme=tline(end);
  else
    N = tline(1);
  end
  [tot]=fscanf(fid,'%f %f %f %f \n',[4,N])';
  hydro(cnt).time_end = tme;
  hydro(cnt).x     = [tot(:,1); NaN(length(morpho(1).x)-size(tot,1),1)];
  hydro(cnt).setup = [tot(:,2); NaN(length(morpho(1).x)-size(tot,1),1)];
  hydro(cnt).depth = [tot(:,3); NaN(length(morpho(1).x)-size(tot,1),1)];
  hydro(cnt).sigma = [tot(:,4); NaN(length(morpho(1).x)-size(tot,1),1)];
  hydro(cnt).Hrms = sqrt(8)*hydro(cnt).sigma ;
end
fclose(fid);
num_output = cnt;
% BeachFX only wants a tiny bit of this info:


out.notes = 'All units are m';
dum = [morpho.zb];
out.x = morpho(1).x;
out.initial_profile = morpho(1).zb;
out.final_profile = morpho(end).zb;
out.max_profile_elev = [max(dum')]';
out.min_profile_elev = [min(dum')]';
dum = [hydro.Hrms];
out.max_hrms = [max(dum')]';
dum = [hydro.setup];
out.max_water_elevation_plus_setup = [max(dum')]';



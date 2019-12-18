function make_infiles(tides,reaches,storms,cshore)

in.iline  = 1;          % 1 = single line
in.iprofl = 1.1;          % 0 = no morph, 1 = run morph
in.isedav = 0;          % 0 = unlimited sand, 1 = hard bottom
in.iperm  = 0;          % 0 = no permeability, 1 = permeable
in.iover  = 1;          % 0 = no overtopping , 1 = include overtopping
in.infilt = 0;          % 1 = include infiltration landward of dune crest
in.iwtran = 0;          % 0 = no standing water landward of crest,
                        % 1 = wave transmission due to overtopping
in.ipond  = 0;          % 0 = no ponding seaward of SWL
in.iwcint = 0;          % 0 = no W & C interaction , 1 = include W & C interaction
in.iroll  = 0;          % 0 = no roller, 1 = roller
in.iwind  = 0;          % 0 = no wind effect
in.itide  = 0;          % 0 = no tidal effect on currents
in.iveg   = 0;          % vegitation effect
in.dx     = cshore.dx;  % constant dx 
                        %in.gamma  = .7;         % shallow water ratio of wave height to water depth
in.gamma  = cshore.gamma;% shallow water ratio of wave height to water depth
in.sporo  = 0.4;        % sediment porosity                        
in.sg = 2.65;           % specific gravity
                        %in.effb   = 0.002;      % suspension efficiency due to breaking eB     
in.effb   = cshore.effb;% suspension efficiency due to breaking eB     
in.efff   = 0.005;       % suspension efficiency due to friction ef 
in.slp    = .5;         % suspended load parameter               
in.slpot  = .1;         % overtopping suspended load parameter               
in.tanphi = .630;       % tangent (sediment friction angle)        
in.blp    = 0.001;      % bedload parameter                        
in.rwh = .02;           % numerical rununp wire height 
in.ilab = 0;            % controls the boundary condition timing. 
in.fric_fac = .015;     % bottom friction factor

if length(cshore.d50)==1;
  cshore.d50 = num2cell(cshore.d50{1}*ones(1,length(reaches)));
end



for i = 1:length(reaches)
  % first make a directory for each reach
  in.dirname=reaches(i).dirname;
  [success,message,messageid] = mkdir(['./work/infiles/',in.dirname]);
  in.d50 = cshore.d50{i};    % d_50 in mm  
  in.wf = vfall(in.d50,20,0); % fall velocity
  for j = 1:length(reaches(i).height_dune)
    for k = 1:length(storms)
      for l = 1:length(tides.phases)
        for m = 1:length(tides.amp)
          in.magic_text = [in.dirname,'_',num2str(reaches(i).height_dune(j)),'_',num2str(reaches(i).width_dune(j)), ...
                           '_',num2str(reaches(i).width_berm(j)),', STM',num2str(storms(k).id),'TPh_',...
                           num2str(tides.phases(l)),'_TAmp_',num2str(m)];
          % in.magic_text = [in.dirname,'_',num2str(reaches(i).height_dune(j)),'_',num2str(reaches(i).width_dune(j)), ...
          %                  '_',num2str(reaches(i).width_berm(j)),', STM',num2str(storms(k).id),'TPh_',...
          %                  num2str(tides.phases(l)),'_TAmp_',num2str(m)];
          in.name=strrep(in.magic_text,', ','-');
          
          in.header = {'------------------------------------------------------------'
                       in.magic_text
                       '------------------------------------------------------------'};
          
          % ftime = (storms(k).date(end)-storms(k).date(1))*24*3600;      % [sec] final time, dictates model duration
          % dt = 1*3600;         % time interval in seconds for wave and water level conditions
          % in.timebc_wave = [0:dt:ftime];
          in.timebc_wave = (storms(k).date-storms(k).date(1))*24*3600;
          in.datebc = storms(k).date(1)+in.timebc_wave/(24*3600); 
          in.timebc_surg = in.timebc_wave;
          in.nwave = length(in.timebc_wave); in.nsurg = in.nwave;dum = ones(1,in.nwave);
          in.Tp = interp1(storms(k).date,storms(k).T,in.datebc);
          in.Hrms = interp1(storms(k).date,storms(k).Hs/sqrt(2),in.datebc);
          eta = storms(k).storm_surge+tides.amp(m)*storms(k).normalized_tide(:,l);
          in.swlbc = interp1(storms(k).date,eta,in.datebc);; % water level at seaward boundary in meters
          in.Wsetup = zeros(size(in.Hrms));   % wave setup at seaward boundary in meters
          in.angle = zeros(size(in.Hrms));    % constant incident wave angle at seaward boundary in
          in.x_offset = 0.3048*max(reaches(i).profile(j).x_ft);
          x  = 0.3048*(max(reaches(i).profile(j).x_ft)-reaches(i).profile(j).x_ft);% x points
          zb = 0.3048*reaches(i).profile(j).z_ft; % zb points
          in.x = min(x):in.dx:max(x);
          [j1 j2] = unique(x); 
          in.zb = interp1(x(j2),zb(j2),in.x);
          in.fw = in.fric_fac*ones(size(in.zb)); % cross-shore values of bot fric

          makeinfile_bfx(in);
          
        end
      end
    end
  end
end


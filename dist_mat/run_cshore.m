% after make_cshore_infiles, run all infiles found in the infiles directory

addpath 'mfiles' 
iclean = 1; % iclean = 1 to remove all existing resultrs in outfile directory   
if iclean ;[j1,j1,j1]=rmdir('./work/outfiles','s');clear j1 iclean;end
dirnames = dir('./work/infiles');
tic;
for i = 3:length(dirnames)
  [success,message,messageid] = mkdir(['./work/outfiles/',dirnames(i).name]);
  fnames = dir(['./work/infiles/',dirnames(i).name,'/*.infile']);
  cnt = 0;
  for j = 1:1:length(fnames)
    disp(['working on /',dirnames(i).name,'/',fnames(j).name])
    copyfile(['./work/infiles/',dirnames(i).name,'/',fnames(j).name],'temp.infile');
    if isunix
      system('./executables/CSHORE_USACE_LINUX.out temp');
    else
      system('.\executables\cshore_usace_win.out temp');
    end
    results = load_results_bfx('temp');
    % matfilename= ['./work/infiles/',dirnames(i).name,'/',fnames(j).name(1:end-7),'.mat'];
    % if exist(matfilename,'file')
    %   load(matfilename);
    % else
    %   in.x_offset = results.x(end);
    % end

    
    %save(['./work/outfiles/',dirnames(i).name,'/',fnames(j).name(1:end-7),'.mat'],'results','in')
    save(['./work/outfiles/',dirnames(i).name,'/',fnames(j).name(1:end-7),'.mat'],'results')
    delete temp*
  end
end
toc


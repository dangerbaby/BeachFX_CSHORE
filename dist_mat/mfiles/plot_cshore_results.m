
clear all
iprint = 1;
dirnames = dir('./work/outfiles');

for i = 3:length(dirnames)
  fnames = dir(['./work/outfiles/',dirnames(i).name,'/*.mat']);
  for j = 1:1:length(fnames)
    disp(['working on /',dirnames(i).name,'/',fnames(j).name])
    load(['./work/outfiles/',dirnames(i).name,'/',fnames(j).name]);
    [j1 j2] = max(results.initial_profile);
    
    
    figure(1);clf
    %plot(in.x,in.zb,'b'); hold all
    hh(1)=plot(in.x,results.initial_profile,'r'); hold all
    hh(2)=plot(in.x,results.final_profile,'k'); hold all
    
    axis([in.x(j2)-100 in.x(j2)+10 -1 in.zb(j2)+2])
    legend(hh,'Initial','Final')
    title(in.magic_text,'interpreter','none')
    xlabel(' x [m]')
    ylabel(' z [m]')
    
    if iprint
      print('-dpng',['./work/outfiles/',dirnames(i).name,'/',in.name,'.png'])
    end

    
  end

  
  
  
  
end

for i = 1:length(reaches)
  figure(i);clf
  for j = 1:length(reaches(i).profile)
    plot(reaches(i).profile(j).x_ft,reaches(i).profile(j).z_ft);hold all
    %plot(.3048*reaches(i).profile(j).x_ft,.3048*reaches(i).profile(j).z_ft);hold all
  end
  xlabel('x')
  xlabel('z')
  title(reaches(i).name)

end

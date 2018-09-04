function reaches=find_all_combos(inp)
names = inp.names;
inp = rmfield(inp,'names');
fn = fieldnames(inp);

% first check to make sure there are no scalars --if so, populate array to fill number of reaches
for i = 1:length(names)
  for ii = 1:length(fn)
    dum = getfield(inp,fn{ii});
    if length(dum)==1;
      inp = setfield(inp,fn{ii},num2cell(dum{1}*ones(1,length(names))));
    end
  end
end

% find the number of profile combinations (the product of the param space) 
for i = 1:length(names)
  ncombos = 1;
  for ii = 1:length(fn)
    dum = getfield(inp,cell2mat(fn(ii)));
    if length(dum)==1;dum = num2cell(dum{1}*ones(1,length(names)));end
    if ~strcmp(fn(ii),'names')
      ncombos = ncombos*length(dum{i});
    end
  end
  allncombos(i) = ncombos;
end





% start by putting the first element in all ( will correct for dune height etc later
reach = [];
for i = 1:length(names)
  reach.name = names{i};
  reach.dirname = reach.name(~isspace(reach.name));
  for ii = 1:length(fn)
    dum = getfield(inp,fn{ii});
    dum = dum{i};
    if iscell(dum);dum = cell2mat(dum);end
    reach=setfield(reach,fn{ii},repmat(dum(1),1,allncombos(i)));
  end
  %finish the reach structure for height_dune, width_dune, width_berm, 
  dum = getfield(inp,'height_dune');
  dum = dum{i};
  if iscell(dum);dum = cell2mat(dum);end
  height_dune=dum ;
  dum = getfield(inp,'width_dune');
  dum = dum{i};
  if iscell(dum);dum = cell2mat(dum);end
  width_dune=dum ;
  dum = getfield(inp,'width_berm');
  dum = dum{i};
  if iscell(dum);dum = cell2mat(dum);end
  width_berm=dum; 
  cnt = 0;
  for j = 1:length(height_dune)
    for k = 1:length(width_dune)
      for l = 1:length(width_berm)
        cnt = cnt+1;
        reach.height_dune(cnt)= height_dune(j);
        reach.width_dune(cnt)= width_dune(k);
        reach.width_berm(cnt)= width_berm(l);
      end
    end
  end
  reaches(i)=reach;
end











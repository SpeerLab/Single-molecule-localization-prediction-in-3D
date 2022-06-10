%% Thresholding
clear ;clc;
base_path = 'X:\Chenghang\4_Color\Raw\12.21.2020_P8EA\';
storm_folder = [base_path 'stormtiffs\'];
%channel = [750 647 561 488];
channel = '647';

outpath = [base_path 'ML_result_647_new_sat\'];
%%
if exist(outpath,'dir') ~= 7
    mkdir(outpath);
end

files = [dir([storm_folder channel '*.tiff'])]; %#ok<*NBRAK>
%num_images = numel(files);
num_images = 50;
info = imfinfo([storm_folder files(1).name]);

disp('load images')
A = zeros(info.Height,info.Width,num_images);
parfor i = 1:num_images
    temp = imread([storm_folder files(i).name]);
    temp = temp / max(temp(:));
    A(:,:,i) = temp;
end
%%
%Creat A for cluster identification. B saves original info. 
B = A;
for i = 1:size(A,3)
    A(:,:,i) = imadjust(A(:,:,i),stretchlim(A(:,:,i),0.003));
end 
%%
A_thre = A(1:10:end);
threshfactorg = double(multithresh(A_thre,2));
t_use = threshfactorg(1);
disp(t_use);
%%
CG = false(size(A));
parfor k=1:size(A,3)
    CG(:,:,k) = imbinarize(A(:,:,k), t_use);
end
% Find connected component
disp('making CCG')
CCG = bwconncomp(CG,8);
disp('making statsG')

statsG = regionprops(CCG,B,'Area','PixelIdxList','PixelValues','PixelList','WeightedCentroid');
statsG_backup = statsG;
%%
%This block will get aligned data and extract some information about the tile.
%Not necessary if the information is known.
load('X:\Chenghang\Backup_Raw_Data\12.21.2020_P8EA_B\analysis\Result\5_V_Syn\R_paired_3.mat');
Image_x_dist = zeros(numel(statsRwater_ssss),1);
Image_y_dist = zeros(numel(statsRwater_ssss),1);
for i = 1:numel(statsRwater_ssss)
    PixList = statsRwater_ssss(i).PixelList;
    Max_pix = max(PixList,[],1);
    Min_pix = min(PixList,[],1);
    W_centroid = statsRwater_ssss(i).WeightedCentroid;
    Image_x_dist(i) = min(abs(W_centroid(1) - Min_pix(1)),abs(W_centroid(1) - Max_pix(1)));
    Image_y_dist(i) = min(abs(W_centroid(2) - Min_pix(2)),abs(W_centroid(2) - Max_pix(2)));
end
tile_size = 2*max(cat(1,Image_x_dist,Image_y_dist))+1;
disp(tile_size); %72
%%
tile_size = 72;

single_slice_size = [];
for i = 1:numel(statsRwater_ssss)
    PixList = statsRwater_ssss(i).PixelList;
    PixIntensity = statsRwater_ssss(i).PixelValues;
    PixList = PixList(PixIntensity>0,:);
    PixList_z = unique(PixList(:,3));
    for j = 1:numel(PixList_z)
        single_slice_size = cat(1,single_slice_size,numel(find(PixList(:,3) == PixList_z(j))));
    end
end
single_slice_size = log(single_slice_size);
Min_size = min(single_slice_size);
Max_size = max(single_slice_size);
disp(Min_size); %0
disp(Max_size); %6.9295
%%
h = histogram(single_slice_size,20);
hx = h.Values;
hy = h.BinEdges;
BinW = h.BinWidth;
%Convert into percentage.
hx = hx/sum(hx);
%%
Area = log([statsG.Area]);
sel = Area>=Min_size & Area<=Max_size + 0.0001;
statsG = statsG(sel);
clear sel
%%
%Make sure all cluster smaller than a certain size.
All_size_left = zeros(numel(statsG),3);
All_size_right = zeros(numel(statsG),3);
parfor j =1:numel(statsG)
    PList = statsG(j).PixelList;
    cur_size = max(PList,[],1) - min(PList,[],1) + [1,1,1];
    cur_weightedcentroid = statsG(j).WeightedCentroid;
    All_size_left(j,:) = abs(cur_weightedcentroid - min(PList,[],1));
    All_size_right(j,:) = abs(cur_weightedcentroid - max(PList,[],1));
end
All_size_left = All_size_left.*2;
All_size_right = All_size_right.*2;
%
sel = All_size_left(:,1) < tile_size & All_size_left(:,2) < tile_size & All_size_right(:,1) < tile_size & All_size_right(:,2) < tile_size;
statsG = statsG(sel);
%
% Centroid shouldn't be on the edge

W_centroid = zeros(numel(statsG),3);
for i = 1:numel(statsG)
    W_centroid(i,:) = statsG(i).WeightedCentroid;
end
sel = W_centroid(:,1) >= 50 & W_centroid(:,1) <= 6350 & W_centroid(:,2) >= 50 & W_centroid(:,2) <= 6350;
statsG = statsG(sel);
%%
%Delete if the no pixel value.
sel = ones(numel(statsG),1);
parfor i = 1:numel(statsG)
    P_Values = statsG(i).PixelValues;
    if max(P_Values) <= 0
        sel(i) = 0;
    end
end
sel = logical(sel);
statsG = statsG(sel);
%%
statsG_backup = statsG;
%%
%Check if it's okay to select a certain number of clusters.
number_test = 31000;
clear h sel Area
Area = log([statsG.Area]);
h = histogram(Area,hy);
hx_2 = h.Values;
sel = [];
for i = 1:20
    select_num = number_test * hx(i);
    select_num = floor(select_num);
    if select_num > hx_2(i)
        select_num = hx_2(i);
    end
    Fall_in_id = find((((i-1)*BinW)<=Area) & (Area<=i*BinW));
    sel_temp = randsample(Fall_in_id,select_num);
    sel = cat(1,sel,sel_temp');
end
disp('Total number of selected cluster');
disp(numel(sel));
disp('Total numebr of selected cluster > 64 pixel size');
disp(numel(find([statsG(sel).Area] >64)));
disp('ID of the first >64 pixel cluster')
disp(find([statsG(sel).Area]>64,1));
%%
statsG = statsG(sel);
figure;subplot(1,2,1);histogram(single_slice_size,hy);subplot(1,2,2);histogram(log([statsG.Area]),hy);
%%
%Find Max_pix. 
Max_pix = zeros(numel(statsG),1);
for i = 1:numel(statsG)
    Max_pix(i) = max(statsG(i).PixelValues);
end
max(Max_pix)
%% 
%Delete max==1 clusters
for i = numel(statsG):1
    if max(statsG(i).PixelValues) == 1
        statsG(i) = [];
    end
end
%%
histogram(Max_pix);
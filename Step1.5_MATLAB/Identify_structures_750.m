%% Thresholding
clear ;clc;
base_path = 'X:\Chenghang\4_Color\Raw\12.21.2020_P8EA\';
storm_folder = [base_path 'stormtiffs\'];
%channel = [750 647 561 488];
channel = '750';

outpath = [base_path 'ML_result_750\'];
%%
if exist(outpath,'dir') ~= 7
    mkdir(outpath);
end

files = [dir([storm_folder channel '*.tiff'])]; %#ok<*NBRAK>
num_images = numel(files);
info = imfinfo([storm_folder files(1).name]);

disp('load images')
A = zeros(info.Height,info.Width,num_images,'uint8');
parfor i = 1:num_images
    temp = imread([storm_folder files(i).name]);
    temp = temp / max(temp(:));
    temp = imadjust(temp,stretchlim(temp,0.003));
    temp = im2uint8(temp);
    A(:,:,i) = temp;
end
%%
A_thre = A(1:10:end);
threshfactorg = double(multithresh(A_thre,2));
t_use = threshfactorg(1)/255.0;
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

statsG = regionprops(CCG,A,'Area','PixelIdxList','PixelValues','PixelList','WeightedCentroid');
statsG_backup = statsG;
%%
%This block will get aligned data and extract some information about the tile.
%Not necessary if the information is known.
load('X:\Chenghang\Backup_Raw_Data\12.21.2020_P8EA_B\analysis\Result\5_V_Syn\G_paired_3.mat');
statsRwater_ssss = statsGwater_ssss;
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
disp(tile_size); %86
%%
tile_size = 86;

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
disp(Max_size); %7.2535
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
%Delete if the no pixel value >= 0.004.
sel = ones(numel(statsG),1);
parfor i = 1:numel(statsG)
    P_Values = statsG(i).PixelValues;
    if max(P_Values) < 1
        sel(i) = 0;
    end
end
sel = logical(sel);
statsG = statsG(sel);
%%
%Check if it's okay to select a certain number of clusters.
number_test = 18000;
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
%% New data format as the aligned data:
%
parfor j = 1:numel(statsG)
    disp(j/numel(statsG))
    WCentroid = statsG(j).WeightedCentroid;
    WCentroid = ceil(WCentroid);
    %Row, column, num_images, num_cluster, image_ID.
    PValues = statsG(j).PixelValues;
    PList_cur_tile = statsG(j).PixelList;
    PList_cur_tile = PList_cur_tile - WCentroid + [tile_size/2,tile_size/2,1];
    logic_clean = PList_cur_tile(:,1) > 0 & PList_cur_tile(:,1) <= tile_size & PList_cur_tile(:,2) > 0 & PList_cur_tile(:,2) <= tile_size;
    PList_cur_tile = PList_cur_tile(logic_clean,:);
    PValues = PValues(logic_clean);
    new_G = zeros(tile_size,tile_size,'uint8');
    for i = 1:size(PList_cur_tile,1)
        new_G(PList_cur_tile(i,2),PList_cur_tile(i,1)) = PValues(i);
    end
    imwrite(new_G,[outpath sprintf('%05d',j) '.tif']);
end
%%
%Find ROIs
ROIs = zeros(numel(statsG),4);
for i = 1:numel(statsG)
    W_centroid = statsG(i).WeightedCentroid;
    ROIs(i,1) = W_centroid(2) - tile_size/2 + 1;
    ROIs(i,2) = W_centroid(1) - tile_size/2 + 1;
    ROIs(i,3) = W_centroid(3);
    ROIs(i,4) = i;
end
% Write the starting coordinate
if exist([outpath 'ROI\'],'dir') ~= 7
    mkdir([outpath 'ROI\']);
end
fileID = fopen([outpath 'ROI\' channel '_ROIs.txt'],'w');
fprintf(fileID,['x(row),y(column),Num_image,Tile_ID\n']);
for i = 1:numel(statsG)
    fprintf(fileID,'%5.6f,%5.6f,%3d,%7d\n',ROIs(i,1),ROIs(i,2),ROIs(i,3),ROIs(i,4));
end
fclose(fileID);
%%
%Generate Pix_list. 
outpath_2 = [outpath 'Pix_txt\'];
if exist(outpath_2,'dir')~=7
    mkdir(outpath_2)
end
parfor i = 1:numel(statsG)
    PList = statsG(i).PixelList;
    PValues = statsG(i).PixelValues;
    ID = ones(size(PList,1),1);
    ID = ID.*i;
    out = cat(2,ID,PList,double(PValues));
    fileID = fopen([outpath_2 'Pix_' sprintf('%05d',i) '.txt'],'w');
    fprintf(fileID,['TileID,x(row),y(column),Num_image,Pix_values\n']);
    for j = 1:size(ID,1)
        fprintf(fileID,'%7d,%7d,%7d,%7d,%5.6f\n',out(j,1),out(j,3),out(j,2),out(j,4),out(j,5));
    end
    fclose(fileID);
end





%% Old data format with combined 140 images rendered.
% Generating images:
new_G_double = zeros(info.Height,info.Width,num_images);
for i = 1:numel(statsG)
    PList = statsG(i).PixelList;
    PValues = statsG(i).PixelValues;
    for j = 1:size(PList,1)
        new_G_double(PList(j,2),PList(j,1),PList(j,3)) = double(PValues(j));
    end
end
Im_out_path = [outpath '\stormtiffs\'];
if exist(Im_out_path,'dir') ~= 7
    mkdir(Im_out_path);
end
new_G_single = single(new_G_double);
%
for i = 1:size(new_G_single,3)
    disp(i);
    t = Tiff([Im_out_path sprintf('%03d',i) '.tiff'],'w');
    tagstruct.ImageLength = size(new_G_single,1);
    tagstruct.ImageWidth = size(new_G_single,2);
    tagstruct.Compression = Tiff.Compression.None;
    tagstruct.Photometric = Tiff.Photometric.MinIsBlack;
    tagstruct.BitsPerSample = 32;
    tagstruct.SamplesPerPixel = 1;
    tagstruct.SampleFormat = Tiff.SampleFormat.IEEEFP;
    tagstruct.PlanarConfiguration = Tiff.PlanarConfiguration.Chunky;
    setTag(t,tagstruct);
    write(t,new_G_single(:,:,i));
    close(t);
end
%
% Find ROIs
ROIs = zeros(numel(statsG),4);
for i = 1:numel(statsG)
    W_centroid = statsG(i).WeightedCentroid;
    ROIs(i,1) = W_centroid(2) - 43;
    ROIs(i,2) = W_centroid(1) - 43;
    ROIs(i,3) = W_centroid(3);
    ROIs(i,4) = i;
end
% Write the starting coordinate
fileID = fopen([outpath channel '_ROIs.txt'],'w');
fprintf(fileID,['x(row),y(column),Num_image,Tile_ID\n']);
for i = 1:numel(statsG)
    fprintf(fileID,'%5.6f,%5.6f,%3d,%7d\n',ROIs(i,1),ROIs(i,2),ROIs(i,3),ROIs(i,4));
end
fclose(fileID);
%
% Pixel text.
parfor i = 1:numel(statsG)
    PList = statsG(i).PixelList;
    PValues = statsG(i).PixelValues;
    ID = ones(size(PList,1),1);
    ID = ID.*i;
    out = cat(2,ID,PList,PValues);
    fileID = fopen([outpath 'Pix_' sprintf('%05d',i) '.txt'],'w');
    fprintf(fileID,['TileID,x(row),y(column),Num_image,Pix_values\n']);
    for j = 1:size(ID,1)
        fprintf(fileID,'%7d,%7d,%7d,%7d,%5.6f\n',out(j,1),out(j,3),out(j,2),out(j,4),out(j,5));
    end
    fclose(fileID);
end

%% Correction of the first line: No need for normal workflow.
base_path = 'X:\Chenghang\4_Color\Raw\12.21.2020_P8EA\';
outpath = [base_path 'ML_result_v2\'];
fileID = fopen([outpath 'test.txt'],'r');
addline = fread(fileID,Inf);
fclose(fileID);
parfor i = 1:num_stats
    fileID = fopen([outpath 'Pix_' sprintf('%06d',i) '.txt'],'r');
    fgetl(fileID);
    buffer = fread(fileID,Inf);
    fclose(fileID);

    fileID = fopen([outpath 'Pix_' sprintf('%06d',i) '.txt'],'w');
    buffer = cat(1,addline,buffer);
    fwrite(fileID,buffer);
    fclose(fileID);
end
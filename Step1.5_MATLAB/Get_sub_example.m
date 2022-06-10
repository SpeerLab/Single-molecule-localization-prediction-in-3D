%%
% Getting the same id from the original statsGwater_backup is not easy.
% Doing new watershedding with the same parameter.
clear ;clc;
base_path = 'X:\Chenghang\Backup_Raw_Data\12.21.2020_P8EA_B\';
clu_folder = [base_path 'analysis\Result\ML_Example_v3\'];
outpath = [clu_folder 'Compare_647\'];
if exist(outpath,'dir') ~=7
    mkdir(outpath);
end
inpath = 'X:\Chenghang\Backup_Raw_Data\12.21.2020_P8EA_B\analysis\Result\ML_data_batch_647pos\';
%%
get_tile_id = [127,128,129];
clu_id = 38;

Parameter_hmin = 2;
clear A
A = [];
for i = 1:numel(get_tile_id)
    temp = imread([inpath sprintf('%06d',get_tile_id(i)) '.tif']);
    A = cat(3,A,temp);
end
%
A_logical = logical(A);
CG = bwconncomp(A_logical,26);
statsG = regionprops(CG,A,'Area','PixelIdxList','PixelValues','PixelList','WeightedCentroid');
%
if numel(statsG) == 1
    statsVwater_ss = statsG;
    jj = 1;
    minpix = min(statsVwater_ss(jj).PixelList);
    maxpix = max(statsVwater_ss(jj).PixelList);
    len = maxpix - minpix + [1,1,1];
    curr = zeros(len(2),len(1),len(3),'uint8');
    for j=1: size(statsVwater_ss(jj).PixelList,1)
        curr(statsVwater_ss(jj).PixelList(j,2)-minpix(2)+1,statsVwater_ss(jj).PixelList(j,1)-minpix(1)+1, ...
            statsVwater_ss(jj).PixelList(j,3)-minpix(3)+1)=statsVwater_ss(jj).PixelValues(j,1);
    end

    %Interpolation
    curr1 = permute(curr,[1 3 2]);
    curr2 = zeros([ceil(size(curr1,1)),ceil(size(curr1,2)*70/15.5)],'uint8');
    for k = 1:ceil(size(curr1,3))
        curr2(:,:,k) = imresize(curr1(:,:,k), [ceil(size(curr1,1)) ...
            ceil(size(curr1,2)*70/15.5)],'lanczos2');
    end
    curr3 = permute(curr2,[1 3 2]);

    %Gaussian blur
    gausspix = 2;
    curr4 = imgaussfilt3(curr3,gausspix);

    DYs = false(size(curr4));
    t_use = double(multithresh(curr4(find(curr4)),2)) / 256.0;
    for k=1:size(curr4,3)
        DYs(:,:,k) = im2bw(curr4(:,:,k), t_use(2));
    end
    curr4_temp = uint8(DYs) .* curr4;
    for k = 1:size(curr4,3)
        curr4_temp(:,:,k) = imadjust(curr4_temp(:,:,k),stretchlim(curr4_temp(:,:,k)));
    end

    %figure;imagesc(curr3(:,:,20));
    %figure;imagesc(curr4_temp(:,:,20));

    I2 = imcomplement(curr4_temp);
    I3 = imhmin(I2,Parameter_hmin);
    L = watershed(I3,26);


else
    disp('More than one conn comp!');
end

%figure;imshow(curr4_temp(:,:,5));
disp(max(L(:)));
%
outpath_2 = [outpath 'clu_' sprintf('%03d',clu_id) '\'];
if exist(outpath_2,'dir')~=7
    mkdir(outpath_2);
end
for i = 1:size(curr4_temp,3)
    imwrite(curr4_temp(:,:,i).*uint8(logical(L(:,:,i))),[outpath_2 sprintf('%03d',i) '.tif']);
    imwrite(curr3(:,:,i).*uint8(logical(L(:,:,i))),[outpath_2 'Ori_' sprintf('%03d',i) '.tif']);
    imwrite(L(:,:,i),[outpath_2 'L_' sprintf('%03d',i) '.tif']);
end
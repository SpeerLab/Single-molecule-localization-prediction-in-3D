clear ;clc;
base_path = 'X:\Chenghang\4_Color\Raw\12.21.2020_P8EA\';
storm_folder = [base_path 'stormtiffs\'];
%channel = [750 647 561 488];
channel = '647';

outpath = [base_path 'stormtiffs_fake_u8_no_sat\'];
%%
if exist(outpath,'dir') ~= 7
    mkdir(outpath);
end

files = [dir([storm_folder channel '*.tiff'])]; %#ok<*NBRAK>
num_images = numel(files);
info = imfinfo([storm_folder files(1).name]);

disp('load images')
parfor i = 1:num_images
    temp = imread([storm_folder files(i).name]);
    temp = temp/max(temp(:))
    temp = im2uint8(temp);
    imwrite(temp,[outpath channel '_' sprintf('%03d',i) '.tif']);
end
%%

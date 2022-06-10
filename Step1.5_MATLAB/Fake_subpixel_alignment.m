clear ;clc;
base_path = 'X:\Chenghang\4_Color\Raw\12.21.2020_P8EA\';
storm_folder = [base_path 'stormtiffs_fake_int\'];
%channel = [750 647 561 488];
channel = '647';
Fake_path = [base_path 'stormtiffs_fake\'];

if exist(Fake_path,'dir')~=7
    mkdir(Fake_path);
end

files = [dir([storm_folder channel '*.tiff'])]; %#ok<*NBRAK>
num_images = numel(files);
num_images = 80;
info = imfinfo([storm_folder files(1).name]);
%%
parfor i = 1:num_images
    temp = imread([storm_folder files(i).name]);
    %Blur with sigma = 10
    temp_conv = imgaussfilt3(temp,10);
    temp_conv = imadjust(temp_conv,stretchlim(temp_conv,0.003));
    temp_conv = temp_conv + uint16(rand(size(temp))*40000);
    
    [temp_fake_output] = dftregistration(fft2(temp),fft2(temp_conv),100);

    xform647 = [ 1  0  0
        0  1  0
        (temp_fake_output(4)) (temp_fake_output(3))  1 ];
    tform_translate647 = maketform('affine',xform647); %#ok<*MTFA1>
    imagesize = size(temp);
    xdata = [1 imagesize(2)];
    ydata = [1 imagesize(1)];
    temp_fake = imtransform(temp, tform_translate647, 'XData',xdata,'YData',ydata);%#ok<*DIMTRNS>

    temp_fake = im2uint8(temp_fake);
    imwrite(temp_fake,[Fake_path channel '_' sprintf('%03d',i) '.tif']);
end
%% Thresholding
clear ;clc;
base_path = 'X:\Chenghang\Backup_Raw_Data\12.21.2020_P8EA_B\';
Result_folder = [base_path 'analysis\Result\'];
inpath = [Result_folder '4_CTB\'];
outpath = [base_path 'analysis\Result\ML_Example_v3\'];
storm_folder = [base_path 'analysis\elastic_align\storm_merged\'];
files = [dir([storm_folder '*.tif'])]; %#ok<*NBRAK>
num_images = numel(files);
info = imfinfo([storm_folder files(1).name]);

%%
load([inpath 'G_paired_VC.mat']);
%%
W_centroid = zeros(numel(statsGwater_sssss),3);
for i = 1:numel(statsGwater_sssss)
    W_centroid(i,:) = statsGwater_sssss(i).WeightedCentroid;
end
sel = W_centroid(:,1) >= 48 & W_centroid(:,1) <= info.Height - 48 & W_centroid(:,1) >= 50 & W_centroid(:,1) <= (info.Height - 48);
statsGwater_sssss = statsGwater_sssss(sel);
%%
Tile = [];
count = 1;
Empty_mark = [];
for j = 1:numel(statsGwater_sssss)
    disp(j);
    PList = statsGwater_sssss(j).PixelList;
    PList = PList(:,3);
    PList = unique(PList);
    WCentroid = statsGwater_sssss(j).WeightedCentroid;
    WCentroid = ceil(WCentroid);
    for k = 1:numel(PList)
        %Row, column, num_images, num_cluster, image_ID.
        Tile = cat(1,Tile,[WCentroid(2)-43,WCentroid(1)-43,PList(k),j,count]);
        PValues = statsGwater_sssss(j).PixelValues;
        PList_cur_tile = statsGwater_sssss(j).PixelList;
        PValues = PValues(PList_cur_tile(:,3) == PList(k));
        if numel(find(PValues)) >0
            Empty_mark = cat(1,Empty_mark,[0]);
            PList_cur_tile = PList_cur_tile(PList_cur_tile(:,3) == PList(k),:);
            PList_cur_tile = PList_cur_tile - WCentroid + [43,43,1];
            logic_clean = PList_cur_tile(:,1) > 0 & PList_cur_tile(:,1) <= 86 & PList_cur_tile(:,2) > 0 & PList_cur_tile(:,2) <= 86;
            PList_cur_tile = PList_cur_tile(logic_clean,:);
            PValues = PValues(logic_clean);
            new_G = zeros(86,86,'uint8');
            for i = 1:size(PList_cur_tile,1)
                new_G(PList_cur_tile(i,2),PList_cur_tile(i,1)) = PValues(i);
                imwrite(new_G,[outpath sprintf('%06d',count) '.tif']);
            end
            count = count+1;
        else
            Empty_mark = cat(1,Empty_mark,[1]);
        end
    end
end
%%
fileID = fopen([outpath channel 'test_ROIs.txt'],'w');
fprintf(fileID,['x(row),y(column),z(Num_image),Cluster_ID,Tile_ID\n']);
for i = 1:size(Tile,1)
    if Empty_mark(i) == 0
        fprintf(fileID,'%5.6f,%5.6f,%3d,%7d,%7d\n',Tile(i,1),Tile(i,2),Tile(i,3),Tile(i,4),Tile(i,5));
    end
end
fclose(fileID);
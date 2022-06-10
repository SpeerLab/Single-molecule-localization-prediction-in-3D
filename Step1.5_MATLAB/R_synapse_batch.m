%%
clear;clc
%
pathname = strings(18,1);
pathname(1) = ['X:\Chenghang\Backup_Raw_Data\1.2.2021_P2EA_B\']; %#ok<*NBRAK>
pathname(2) = ['X:\Chenghang\Backup_Raw_Data\1.4.2021_P2EB_B\'];
pathname(3) = ['X:\Chenghang\4_Color\Raw\1.6.2021_P2EC_B\'];
pathname(4) = ['X:\Chenghang\Backup_Raw_Data\7.29.2020_P4EB\'];
pathname(5) = ['X:\Chenghang\Backup_Raw_Data\9.25.2020_P4EC_B\'];
pathname(6) = ['X:\Chenghang\Backup_Raw_Data\12.5.2020_P4ED_B\'];
pathname(7) = ['X:\Chenghang\Backup_Raw_Data\12.21.2020_P8EA_B\'];
pathname(8) = ['X:\Chenghang\4_Color\Raw\12.23.2020_P8EB_B\'];
pathname(9) = ['X:\Chenghang\4_Color\Raw\1.12.2021_P8EC_B\'];
pathname(10) = ['X:\Chenghang\Backup_Raw_Data\9.29.2020_B2P2A_B\'];
pathname(11) = ['X:\Chenghang\4_Color\Raw\12.13.2020_B2P2B_B\'];
pathname(12) = ['X:\Chenghang\Backup_Raw_Data\12.18.2020_B2P2C_B\'];
pathname(13) = ['X:\Chenghang\Backup_Raw_Data\10.3.2020_B2P4A_B\'];
pathname(14) = ['X:\Chenghang\Backup_Raw_Data\10.27.2020_B2P4B_B\'];
pathname(15) = ['X:\Chenghang\Backup_Raw_Data\12.8.2020_B2P4C_B\'];
pathname(16) = ['X:\Chenghang\Backup_Raw_Data\12.12.2020_B2P8A_B\'];
pathname(17) = ['X:\Chenghang\4_Color\Raw\1.13.2021_B2P8B_B\'];
pathname(18) = ['X:\Chenghang\4_Color\Raw\1.11.2021_B2P8C_B\'];

%% Render all data
disp('Pos');
parfor file_id = 1:18
    base_path = char(pathname(file_id));
    disp(base_path);
    Result_folder = [base_path 'analysis\Result\'];
    inpath = [Result_folder '4_CTB\'];
    outpath = [base_path 'analysis\Result\ML_data_batch_647pos\'];
    if exist(outpath,'dir')~=7
        mkdir(outpath);
    end
    storm_folder = [base_path 'analysis\elastic_align\storm_merged\'];
    files = [dir([storm_folder '*.tif'])]; %#ok<*NBRAK>
    num_images = numel(files);
    info = imfinfo([storm_folder files(1).name]);
    load_variable = load([inpath 'R_paired_VC.mat'],'statsRwater_sssss');
    statsGwater_sssss = load_variable.statsRwater_sssss;

    % CTB_positive clusters
    W_centroid = zeros(numel(statsGwater_sssss),3);
    for i = 1:numel(statsGwater_sssss)
        W_centroid(i,:) = statsGwater_sssss(i).WeightedCentroid;
    end
    sel = W_centroid(:,1) >= 50 & W_centroid(:,1) <= info.Height - 50 & W_centroid(:,2) >= 50 & W_centroid(:,2) <= (info.Height - 50);
    statsGwater_sssss = statsGwater_sssss(sel);
    %
    Tile = [];
    count = 1;
    Empty_mark = [];
    for j = 1:numel(statsGwater_sssss)
        disp(j)
        PList = statsGwater_sssss(j).PixelList;
        PList = PList(:,3);
        PList = unique(PList);
        WCentroid = statsGwater_sssss(j).WeightedCentroid;
        WCentroid = ceil(WCentroid);
        for k = 1:numel(PList)
            %Row, column, num_images, num_cluster, image_ID.
            Tile = cat(1,Tile,[WCentroid(2)-36,WCentroid(1)-36,PList(k),j,count]);
            PValues = statsGwater_sssss(j).PixelValues;
            PList_cur_tile = statsGwater_sssss(j).PixelList;
            PValues = PValues(PList_cur_tile(:,3) == PList(k));
            if numel(find(PValues)) >0
                Empty_mark = cat(1,Empty_mark,[0]);
                PList_cur_tile = PList_cur_tile(PList_cur_tile(:,3) == PList(k),:);
                PList_cur_tile = PList_cur_tile - WCentroid + [36,36,1];
                logic_clean = PList_cur_tile(:,1) > 0 & PList_cur_tile(:,1) <= 72 & PList_cur_tile(:,2) > 0 & PList_cur_tile(:,2) <= 72;
                PList_cur_tile = PList_cur_tile(logic_clean,:);
                PValues = PValues(logic_clean);
                new_G = zeros(72,72,'uint8');
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

    if exist([outpath 'ROI\'],'dir') ~= 7
        mkdir([outpath 'ROI\']);
    end
    fileID = fopen([outpath 'ROI\' 'ROIs.txt'],'w');
    fprintf(fileID,['x(row),y(column),z(Num_image),Cluster_ID,Tile_ID\n']);
    for i = 1:size(Tile,1)
        if Empty_mark(i) == 0
            fprintf(fileID,'%5.6f,%5.6f,%3d,%7d,%7d\n',Tile(i,1),Tile(i,2),Tile(i,3),Tile(i,4),Tile(i,5));
        end
    end
    fclose(fileID);
end


disp('neg');
parfor file_id = 1:18
    base_path = char(pathname(file_id));
    disp(base_path);
    Result_folder = [base_path 'analysis\Result\'];
    inpath = [Result_folder '4_CTB\'];
    outpath = [base_path 'analysis\Result\ML_data_batch_647neg\'];
    if exist(outpath,'dir')~=7
        mkdir(outpath);
    end
    storm_folder = [base_path 'analysis\elastic_align\storm_merged\'];
    files = [dir([storm_folder '*.tif'])]; %#ok<*NBRAK>
    num_images = numel(files);
    info = imfinfo([storm_folder files(1).name]);
    load_variable = load([inpath 'R_paired_VC.mat'],'statsRwater_ssssn');
    statsGwater_sssss = load_variable.statsRwater_ssssn;

    % CTB_negative clusters
    W_centroid = zeros(numel(statsGwater_sssss),3);
    for i = 1:numel(statsGwater_sssss)
        W_centroid(i,:) = statsGwater_sssss(i).WeightedCentroid;
    end
    sel = W_centroid(:,1) >= 50 & W_centroid(:,1) <= info.Height - 50 & W_centroid(:,2) >= 50 & W_centroid(:,2) <= (info.Height - 50);
    statsGwater_sssss = statsGwater_sssss(sel);
    %
    Tile = [];
    count = 1;
    Empty_mark = [];
    for j = 1:numel(statsGwater_sssss)
        disp(j)
        PList = statsGwater_sssss(j).PixelList;
        PList = PList(:,3);
        PList = unique(PList);
        WCentroid = statsGwater_sssss(j).WeightedCentroid;
        WCentroid = ceil(WCentroid);
        for k = 1:numel(PList)
            %Row, column, num_images, num_cluster, image_ID.
            Tile = cat(1,Tile,[WCentroid(2)-36,WCentroid(1)-36,PList(k),j,count]);
            PValues = statsGwater_sssss(j).PixelValues;
            PList_cur_tile = statsGwater_sssss(j).PixelList;
            PValues = PValues(PList_cur_tile(:,3) == PList(k));
            if numel(find(PValues)) >0
                Empty_mark = cat(1,Empty_mark,[0]);
                PList_cur_tile = PList_cur_tile(PList_cur_tile(:,3) == PList(k),:);
                PList_cur_tile = PList_cur_tile - WCentroid + [36,36,1];
                logic_clean = PList_cur_tile(:,1) > 0 & PList_cur_tile(:,1) <= 72 & PList_cur_tile(:,2) > 0 & PList_cur_tile(:,2) <= 72;
                PList_cur_tile = PList_cur_tile(logic_clean,:);
                PValues = PValues(logic_clean);
                new_G = zeros(72,72,'uint8');
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

    if exist([outpath 'ROI\'],'dir') ~= 7
        mkdir([outpath 'ROI\']);
    end
    fileID = fopen([outpath 'ROI\' 'ROIs.txt'],'w');
    fprintf(fileID,['x(row),y(column),z(Num_image),Cluster_ID,Tile_ID\n']);
    for i = 1:size(Tile,1)
        if Empty_mark(i) == 0
            fprintf(fileID,'%5.6f,%5.6f,%3d,%7d,%7d\n',Tile(i,1),Tile(i,2),Tile(i,3),Tile(i,4),Tile(i,5));
        end
    end
    fclose(fileID);
end
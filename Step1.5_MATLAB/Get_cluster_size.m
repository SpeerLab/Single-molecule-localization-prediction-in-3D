clear;clc
%
pathname = strings(18,1);
pathname(1) = ['X:\Chenghang\Backup_Raw_Data\1.2.2021_P2EA_B\'];
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
%
out_r = [0,0,00];
out_l = [0,0,0];
for cur_path = 1:18
    load([char(pathname(cur_path)) 'analysis\Result\4_CTB\G_paired_VC.mat']);
    All_size_left = zeros(numel(statsGwater_sssss),3);
    All_size_right = zeros(numel(statsGwater_sssss),3);
    for j =1:numel(statsGwater_sssss)
        PList = statsGwater_sssss(j).PixelList;
        cur_size = max(PList) - min(PList) + [1,1,1];
        cur_weightedcentroid = statsGwater_sssss(j).WeightedCentroid;
        All_size_left(j,:) = abs(cur_weightedcentroid - min(PList));
        All_size_right(j,:) = abs(cur_weightedcentroid - max(PList));
    end
    out_r = cat(1,out_r,max(All_size_left)*2);
    out_l = cat(1,out_l,max(All_size_right)*2);
end
disp(max(out_r));
disp(max(out_l));
%%
%Look at the size of 'statsG'. 
All_size_left = zeros(numel(statsG),3);
All_size_right = zeros(numel(statsG),3);
for j =1:numel(statsG)
    PList = statsG(j).PixelList;
    cur_size = max(PList) - min(PList) + [1,1,1];
    cur_weightedcentroid = statsG(j).WeightedCentroid;
    All_size_left(j,:) = abs(cur_weightedcentroid - min(PList));
    All_size_right(j,:) = abs(cur_weightedcentroid - max(PList));
end
disp(max(All_size_left)*2);
disp(max(All_size_right)*2);

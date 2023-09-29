@echo off

echo Start processing
echo Prediction_647 step 2

set input_path="X:\\Chenghang\\04_4_Color\\Exp_Group\\1.4.2021_P2EB_B_V2\\"
set /A ID_Checker=10
echo Input path directory: %input_path%

python .\Prediction_647\3_prediction\tile_and_num_locs_plot.py %input_path% %ID_Checker%
pause
python .\Prediction_647\4_DBSCan\nn_pred_to_locs3d.py %input_path%
python .\Prediction_647\4_DBSCan\Get_sequence_from_rois.py %input_path%
python .\Prediction_647\4_DBSCan\locs_3d_sequence.py %input_path%
python .\Prediction_647\4_DBSCan\dbscan.py %input_path%
python .\Prediction_647\8_Cluster_Properties\get_cluster_properties_pred.py %input_path%
pause
python .\Prediction_647\5_Get_Ground_Truth\full_pixel_list.py %input_path%
python .\Prediction_647\5_Get_Ground_Truth\locs_per_storm_image_to_file.py %input_path%
python .\Prediction_647\7_DBScan_GroundTruth_No_Rand\make_data.py %input_path%
python .\Prediction_647\7_DBScan_GroundTruth_No_Rand\locs_3d_sequence.py %input_path%
python .\Prediction_647\7_DBScan_GroundTruth_No_Rand\dbscan.py %input_path%
python .\Prediction_647\8_Cluster_Properties\get_cluster_properties_gtgt.py %input_path%
echo finish processing
echo remember to clean the file structure manually
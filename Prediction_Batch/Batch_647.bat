@echo off

echo Start processing
echo Prediction_647 step 1

set input_path="X:\\Chenghang\\04_4_Color\\Exp_Group\\1.4.2021_P2EB_B_V2\\"
echo Input path directory: %input_path%

python .\Prediction_647\1_Estimation_Dict\make_num_locs_estimate_per_tile_parallel.py %input_path%
python .\Prediction_647\2_make_data_tiles\make_data.py %input_path%
python .\Prediction_647\3_prediction\experiment_pred_to_file.py %input_path%

echo Finish estimation
echo Remember to move the predicted file before continute to step 2
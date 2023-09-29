2022.9.6: 
The code is used to validate the localization predict results. 
Model trained based on 3D aligned data. 
2.15.2023. 
Step 1:  Find and save the old models. 
Estimation (647): 
coef1 = [0.026690684168400664, -0.003290712263685849]
coef2 = [7.612476425933639e-05, 0.01655408716870287, 0.0005903003540095866]
(750):
coef1 = [0.03569509613725669, -0.002025373366708513]
coef2 = [8.32001460591067e-05, 0.026301047938854002, 0.002096633957520183]

For data prediction: 
Step 1: Get prep data. 
    Run MATLAB code to get cluter information. 
	Before starting, rename ROI.txt into ROI.csv, and ensure y(row) x(column). 
    Using "make_num_locs_estimate_per_tile_parallel.py" to get initial estimation. 
    Output: chenghang_list_tilesize_86\\num_locs_estimate\\
    Using "make_data.py" to create input-output paires. We only need image tiles saved in python format. 
    Output: chenghang_list_tilesize_86\\tiles\\
    Specify model path. 
    Use "experiment_pred_to_file.py" for the prediction. 
    Output will go the to model folder. Move it under the expfolder. 
    Use "tile_and_num_locs_plot.py" to check the localizations. 
Step 2: Get DBscan results for both predicted results and the ground truth. 
    nn_pred_to_locs3d
    # remove_empty_locs3d_tile_list
    # tiles_sequence
    Get_sequence_from_rois.py 
    output:tile_sequences.
    locs_3d_sequence
    dbscan

    For plots: DBscan_plot
    To check the sequence: tiles_sequence_view_test

For ground truth data processing: 
    locs_per_storm_image_to_file.py
    output: locs_dictionary_tilesize_86\\
    full_pixel_list.py
    output: pix_list_full.csv under the datafolder. 
    make_data.py
    output: chenghang_list_" + "tilesize_" + str(tile_size) + "\\"
    Get_sequence_from_rois.py (Don't need if it has runned in pred data)
    output:tile_sequences.
DBScan for ground truth data: 
    nn_pred_to_locs3d
    # remove_empty_locs3d_tile_list
    # tiles_sequence
    locs_3d_sequence
    dbscan
DBScan for ground truth data with no randomization: 
    (requires storm_locs_per_image and full pix list)
    make_data.py
    # tiles_sequence
    locs_3d_sequence
    DBScan
Get info: 
    get_cluster_properties_pred and get_cluster_properties_gtgt
    cluster_properties_to_csv_pred and cluster_properties_to_csv_gtgt
    get_info_pred and get_info_gtgt
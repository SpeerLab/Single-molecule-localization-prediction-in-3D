"""
Script to create parallel processes for making estimations of number of localizations per pixel from stormtiff image tiles.
        
Swapnil 12/21
"""
"""
Simplified.
Note: the values are hard coded for the fitting. Change them everytime running a new instance (in locs_estimate_per_storm_image).

Chenghang 5/19/22
"""

import os
import glob
import pandas as pd
import multiprocessing
from multiprocessing import Semaphore

from locs_estimate_per_storm_image import locsEstimatePerStormImage
from locs_estimate_per_storm_image_2 import locsEstimatePerStormImage2

if __name__ == "__main__":

    # Are you analyzing uint8 data?
    uint8 = True
    # uint8 = False

    # Are you doing nearest neighbor averaging of pixel intensities for predicting localizations?
    nn_avg = True
    # nn_avg = False     

    # Set path to data files.
    expfolder = "X:\\Chenghang\\4_Color\\Raw\\12.21.2020_P8EA\\"
    data_directory = expfolder + "make_data\\"
    storm_exp_name = "647storm"    

    
    # Which channel do you want to analyze? Set experiment name.
    # channel = "561storm"
    channel = "647storm"    
    # channel = "750storm" 

    if (channel == "561storm"): tile_list_file = data_directory + "561_ROIs_shuffled.csv"
    
    elif (channel == "647storm"): tile_list_file = data_directory + "647_ROIs_shuffled.csv"
    
    elif (channel == "750storm"): tile_list_file = data_directory + "420_ROIs_shuffled.csv"    
    
    # Set tile size for square shaped tile. 
    tile_size = 72        

    # Specify ROI extension string.
    roi = "_ROIs"                    
    
    if uint8:
        if nn_avg:
            # Create directory for localization estimation with nearest neighbor averaging and uint8 data.
            locs_est_dict_directory = data_directory + "locs_estimate_dictionary_uint8_tilesize_" + str(tile_size) + roi + "\\"
            if not os.path.exists(locs_est_dict_directory):
                os.mkdir(locs_est_dict_directory)
        else:
            # Create directory for localization estimation without nearest neighbor averaging and uint8 data.         
            if not os.path.exists(storm_exp_directory + "locs_estimate_dictionary_no_nn_avg_uint8_tilesize_" + str(tile_size) + roi + "\\"):
                os.mkdir(storm_exp_directory + "locs_estimate_dictionary_no_nn_avg_uint8_tilesize_" + str(tile_size) + roi + "\\")
            locs_est_dict_directory = storm_exp_directory + "locs_estimate_dictionary_no_nn_avg_uint8_tilesize_" + str(tile_size) + roi + "\\"     

    else:
        if nn_avg:
            # Create directory for localization estimation with nearest neighbor averaging.         
            if not os.path.exists(storm_exp_directory + "locs_estimate_dictionary_tilesize_" + str(tile_size) + roi + "\\"):
                os.mkdir(storm_exp_directory + "locs_estimate_dictionary_tilesize_" + str(tile_size) + roi + "\\")
            locs_est_dict_directory = storm_exp_directory + "locs_estimate_dictionary_tilesize_" + str(tile_size) + roi + "\\"
        else:
            # Create directory for localization estimation without nearest neighbor averaging.         
            if not os.path.exists(storm_exp_directory + "locs_estimate_dictionary_no_nn_avg_tilesize_" + str(tile_size) + roi + "\\"):
                os.mkdir(storm_exp_directory + "locs_estimate_dictionary_no_nn_avg_tilesize_" + str(tile_size) + roi + "\\")
            locs_est_dict_directory = storm_exp_directory + "locs_estimate_dictionary_no_nn_avg_tilesize_" + str(tile_size) + roi + "\\"     
      
    # Get path to stormtiff directory.
    stormtiff_directory = expfolder + "ML_result_647\\"
    # stormtiff_directory = storm_exp_directory + "stormtiff_tiles\\"            

    # Make a dataframe from list of tile coordinates.
    df = pd.read_csv(tile_list_file)

    print("total tiles are {}" .format(len(df)))

    # Set scaling factor between raw image and stormtiff image.
    storm_image_scale = int(10)
    
    # Remove previously present files. 
    files = glob.glob(locs_est_dict_directory + "*")
    for f in files:
        os.remove(f)
    
    # Set Maximum number of parallel processes.
    # max_processes = 50
    max_processes = multiprocessing.cpu_count() - 4      
    
    # Setup process queue.
    jobs = []
    # process_count = 0
    # results = multiprocessing.Queue()
    sema = Semaphore(max_processes)    
    
    # Iterate over individual image numbers in dataframe.
    for img_num in df["Num_image"].unique():
        print("preparing " + str(img_num) + "th images")
        # Create a dataframe for particular "Num_img" entry.
        img_df = df[df["Num_image"]==img_num]
        
        # Create a dictionary filename.
        locs_est_dict_file_name_lin_fit = locs_est_dict_directory + "locs_dict_img_" + str(img_num) + "_lin_fit.data"
        locs_est_dict_file_name_quad_fit = locs_est_dict_directory + "locs_dict_img_" + str(img_num) + "_quad_fit.data"
        
        # Create a tupple of file names.
        locs_est_dict_file_name = (locs_est_dict_file_name_lin_fit, locs_est_dict_file_name_quad_fit)                
        
        # Once max_processes are running, block the main process.
        # the main process will continue only after one or more 
        # previously created processes complete.
        sema.acquire()                             
        
        # Assign process for each tile.        
        if nn_avg:
        
            # Process for localization estimation with nearest neighbor averaging. 
            process = multiprocessing.Process(target = locsEstimatePerStormImage, args=(stormtiff_directory, tile_size, storm_image_scale, img_df, locs_est_dict_file_name, channel, uint8, sema))
    
        else: 
    
            # Process for localization estimation without nearest neighbor averaging.         
            process = multiprocessing.Process(target = locsEstimatePerStormImage2, args=(stormtiff_directory, tile_size, storm_image_scale, img_df, locs_est_dict_file_name, channel, uint8, sema))
        
        jobs.append(process)
        process.start()
        
    # Block the execution of next lines in the main script until all the process are terminated. 
    for job in jobs:
        
        job.join()        

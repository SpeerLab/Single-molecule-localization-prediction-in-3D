"""
Script to make estimated number of localizations file for each stormtiff tile.
This script uses multiprocessing module for parallel processing.
        
Swapnil 3/22
"""

import math
import os
import glob
import pandas as pd
import multiprocessing
import sys
from multiprocessing import Semaphore

from num_locs_per_tile import numLocsPerTile

if __name__ == "__main__": 
    # Set path to data files.
    #expfolder = "X:\\Chenghang\\04_4_Color\\Exp_Group\\1.2.2021_P2EA_B_V2\\"
    expfolder = sys.argv[1]

    # storm_exp_name = "561storm"
    storm_exp_name = "ML_result_647"    
    storm_exp_directory = expfolder + storm_exp_name + "\\"

    # Get tile-list file.
    tile_list_file = storm_exp_directory + "ROIs.csv"        

    # Set tile size for square shaped tile.
    tile_size = 72 

    data_directory_str = "chenghang_list_" + "tilesize_" + str(tile_size) + "\\"              
        
    # Create new directory for num_locs from tiles.
    if not os.path.exists(storm_exp_directory + data_directory_str):
        os.mkdir(storm_exp_directory + data_directory_str)

    if not os.path.exists(storm_exp_directory + data_directory_str + "num_locs_estimate\\"):
        os.mkdir(storm_exp_directory + data_directory_str + "num_locs_estimate\\")
        
    num_locs_est_directory = storm_exp_directory + data_directory_str + "num_locs_estimate\\"

    # Remove previously present files. 
    files = glob.glob(num_locs_est_directory + "*")
    #for f in files:
    #    os.remove(f)        

    # Make a dataframe from csv file containing list of tile coordinates.
    df = pd.read_csv(tile_list_file)

    print("total tiles are {}" .format(len(df)))   
    
    # # Coefficients for 750 channel and uint8 datatype.
    coef1 = [0.026690684168400664, -0.003290712263685849]
    coef2 = [7.612476425933639e-05, 0.01655408716870287, 0.0005903003540095866]

    # Set Maximum number of parallel processes.
    max_processes = 36
    
    # Setup process queue.
    jobs = []
    sema = Semaphore(max_processes)       

    # Iterate over all rows in dataframe for given image number.
    for idx in df.index:

        # Get the tile coordinates.
        tile_start_pix_y = math.floor(df.loc[idx, 'y(row)'])
        tile_start_pix_x = math.floor(df.loc[idx, 'x(column)'])
        
        # Get the tile ID.
        tile_id = df.loc[idx, 'Tile_ID']
        print("Processing tile ID {}" .format(tile_id))

        # Initialize a list for localizations in given tile.
        locs_est_storm_lin_fit = []
        locs_est_storm_quad_fit = []

        # For post-aligned and filtered stormtiff images. 
        stormtiff_file = storm_exp_directory +  str(tile_id).zfill(6) + ".tif"

        # Create output files to store the number of localizations per pixel.
        # Note -  The localization estimates are given only in tile frame coordinates.
        num_locs_est_tile_lin_fit_file_name = num_locs_est_directory + "locs_est_lin_fit_tile_" + str(tile_id) + ".data"            
        num_locs_est_tile_quad_fit_file_name = num_locs_est_directory + "locs_est_quad_fit_tile_" + str(tile_id) + ".data"              

        # Once max_processes are running, block the main process.
        # the main process will continue only after one or more 
        # previously created processes complete.
        sema.acquire()

        # Assign process for each tile.        
        # Process for localization estimation with nearest neighbor averaging. 
        process = multiprocessing.Process(target = numLocsPerTile, args=(tile_size, tile_id, coef1, coef2, stormtiff_file, locs_est_storm_lin_fit, locs_est_storm_quad_fit, num_locs_est_tile_lin_fit_file_name, num_locs_est_tile_quad_fit_file_name, sema))        
            
        jobs.append(process)
        process.start()
        
    # Block the execution of next lines in the main script until all the processes are terminated.       
    for job in jobs:
        
        job.join()
       
                
        
        
        
        
        
        
        
        
        
        

 

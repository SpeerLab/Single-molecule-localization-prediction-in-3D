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
from multiprocessing import Semaphore

from num_locs_per_tile_missing import numLocsPerTile

if __name__ == "__main__": 
    # Set path to data files.
    expfolder = "X:\\Chenghang\\4_Color\\Raw\\12.5.2020_P4ED_B_V2\\"

    # storm_exp_name = "561storm"
    storm_exp_name = "ML_result_750_pos"    
    storm_exp_directory = expfolder + storm_exp_name + "\\"

    # Get tile-list file.
    tile_list_file = storm_exp_directory + "ROIs.csv"        

    # Set tile size for square shaped tile.
    tile_size = 86 

    data_directory_str = "chenghang_list_" + "tilesize_" + str(tile_size) + "\\"              
        
    # Create new directory for num_locs from tiles.
    if not os.path.exists(storm_exp_directory + data_directory_str):
        os.mkdir(storm_exp_directory + data_directory_str)

    if not os.path.exists(storm_exp_directory + data_directory_str + "num_locs_estimate\\"):
        os.mkdir(storm_exp_directory + data_directory_str + "num_locs_estimate\\")
        
    num_locs_est_directory = storm_exp_directory + data_directory_str + "num_locs_estimate\\"

    # Remove previously present files. 
    #files = glob.glob(num_locs_est_directory + "*")
    #files = sort(files)
    #for f in files:
        #os.remove(f)        

    # Make a dataframe from csv file containing list of tile coordinates.
    df = pd.read_csv(tile_list_file)

    print("total tiles are {}" .format(len(df)))   
    
    # # Coefficients for 750 channel and uint8 datatype.
    coef1 = [0.03569509613725669, -0.002025373366708513]
    coef2 = [8.32001460591067e-05, 0.026301047938854002, 0.002096633957520183]

    # Set Maximum number of parallel processes.
    max_processes = 22        
    
    # Setup process queue.
    #jobs = []
    #sema = Semaphore(max_processes)       

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
        #sema.acquire()

        # Assign process for each tile.        
        # Process for localization estimation with nearest neighbor averaging. 
        if not os.path.isfile(num_locs_est_tile_lin_fit_file_name):
            numLocsPerTile(tile_size, tile_id, coef1, coef2, stormtiff_file, locs_est_storm_lin_fit, locs_est_storm_quad_fit, num_locs_est_tile_lin_fit_file_name, num_locs_est_tile_quad_fit_file_name)
       

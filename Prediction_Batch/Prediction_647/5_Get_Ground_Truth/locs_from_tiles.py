"""
Function to create list of localizations and localization estimates from stormtiff image tile to be used as 
output of a neural network.
        
Swapnil 12/21
"""

import os
import multiprocessing
import glob
import pickle
import pandas as pd
import math
from multiprocessing import Semaphore

def locsFromTiles(expfolder, tile_size, num_locs_output, max_processes, tiles_df, locsPerTile2, clust_pix_list_full_file):
    
    
    data_directory_str = "chenghang_list_" + "tilesize_" + str(tile_size) + "\\"

    # Create new directory for num_locs from tiles.
    if not os.path.exists(expfolder + "ML_result_647_pos\\" + data_directory_str):
        os.mkdir(expfolder + "ML_result_647_pos\\" + data_directory_str)

    if not os.path.exists(expfolder + "ML_result_647_pos\\" + data_directory_str + "num_locs\\"):
        os.mkdir(expfolder + "ML_result_647_pos\\" + data_directory_str + "num_locs\\")

    num_locs_directory = expfolder + "ML_result_647_pos\\" + data_directory_str + "num_locs\\"  
    
    # Remove previously present files. 
    files = glob.glob(num_locs_directory + "*")
    for f in files:
        os.remove(f)          
    
    # Setup process queue.
    jobs = []

    # Initialize tile count.
    tile_count = 0
    
    # Make a dataframe from list of pixel coordinates.
    clstr_pix_list_full_df = pd.read_csv(clust_pix_list_full_file) 

    # Create a new column for tuple of row and column coordinates.
    clstr_pix_list_full_df['row_col_tup'] = clstr_pix_list_full_df[['x(row)', 'y(column)']].apply(tuple, axis=1)

    # # Convert the tuple column to list.            
    # clstr_pix_list = clstr_pix_list_full_df['row_col_tup'].tolist()

    # Setup process queue.
    jobs = []
    sema = Semaphore(max_processes)     
    
    # Iterate over individual image numbers.
    for img_num in tiles_df["z(Num_image)"].unique():
    
        # Create a dataframe for particular "Num_img" entry.
        img_df = tiles_df[tiles_df["z(Num_image)"]==img_num]

        # Get file for dictionary of localizations from all tiles in tiles_list for given image number.        
        locs_dict_directory = expfolder + "ML_result_647_pos\\" + "locs_dictionary_tilesize_" + str(tile_size) + "\\"
        locs_dict_file_name = locs_dict_directory + "locs_dict_img_" + str(img_num) + ".data"             
        
        # Read from the file and save it to a dictionary.
        print("Reading localizations dictionary from file ...\n")
        
        with open(locs_dict_file_name, 'rb') as filehandle:
            locs_storm = pickle.load(filehandle)
    
        # Iterate over all rows in dataframe for given image number.
        for idx in img_df.index:
            print('processing ' + str(idx) + 'th image')
            # Get the tile coordinates.
            tile_start_pix_y = math.floor(img_df.loc[idx, 'y(row)'])
            tile_start_pix_x = math.floor(img_df.loc[idx, 'x(column)'])
            tile_id = math.floor(img_df.loc[idx, 'Tile_ID'])            
            
            # Form a key from tile coordinates for given tile.
            key  =  "locs_"+str(tile_start_pix_y)+"_"+str(tile_start_pix_x)
            
            # From the localizations dictionary get list of localizations for given key.
            locs_storm_tile = locs_storm[key]                  

            # Create output files to store the number of localizations per pixel.
            # Note -  The localization estimates are given only in tile frame coordinates.
            num_locs_file_name = num_locs_directory + "storm_num_locs_tile_" + str(tile_id) + ".data"                        
  
            # From dataframe of full pixel list, create a dataframe of pixel-list coordinates that lie within given tile.
            cond = clstr_pix_list_full_df["TileID"] == tile_id             

            clstr_pix_list_df = clstr_pix_list_full_df[cond]
            

            # Convert the tuple column to list.            
            clstr_pix_list = clstr_pix_list_df['row_col_tup'].tolist()
            count = 0
            for list_t in clstr_pix_list:
                clstr_pix_list[count] = (list_t[0] + tile_start_pix_y,list_t[1] + tile_start_pix_x)
                count = count + 1
                
            
            # Once max_processes are running, block the main process.
            # This loop will continue only after one or more 
            # previously created processes complete.
            sema.acquire()            

            # Assign process for each tile.
            # process = multiprocessing.Process(target = locsPerTile, args=(h5_file, tile_start_pix_y, tile_start_pix_x, tile_size, max_locs_per_pixel, nm_per_pixel, storm_image_scale, locs_storm_file_name, locs_tile_file_name, locs_storm))
            process = multiprocessing.Process(target = locsPerTile2, args=(tile_start_pix_y, tile_start_pix_x, tile_size, num_locs_file_name, locs_storm_tile, clstr_pix_list, sema))                
            jobs.append(process)
            process.start()
            
            tile_count += 1
        
    # Block the execution of next lines in the main script.       
    for job in jobs:
        
        job.join()                       
            
    total_loc_files = tile_count        

    return total_loc_files            














         



        


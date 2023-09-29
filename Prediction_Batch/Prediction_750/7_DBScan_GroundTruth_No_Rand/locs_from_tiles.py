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
import random
import numpy as np

def locsFromTiles(expfolder, tile_size, max_processes, tiles_df, clust_pix_list_full_file):
    
    
    data_directory_str = "chenghang_list_" + "tilesize_" + str(tile_size) + "\\"

    # Create new directory for num_locs from tiles.
    if not os.path.exists(expfolder + "ML_result_750\\" + data_directory_str):
        os.mkdir(expfolder + "ML_result_750\\" + data_directory_str)

    if not os.path.exists(expfolder + "ML_result_750\\" + data_directory_str + "num_locs_gtgt\\"):
        os.mkdir(expfolder + "ML_result_750\\" + data_directory_str + "num_locs_gtgt\\")

    num_locs_directory = expfolder + "ML_result_750\\" + data_directory_str + "num_locs_gtgt\\"  
    
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
        locs_dict_directory = expfolder + "ML_result_750\\" + "locs_dictionary_tilesize_" + str(tile_size) + "\\"
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
            z_pos = img_df.loc[idx, 'z(Num_image)']
            fl_pt = 3
            z_pix_size = 70
            locs_storm_tile_3d = []

            for each_pos in locs_storm_tile:
                z_given = z_pix_size * random.randint((z_pos-1)*10**fl_pt,(z_pos)*10**fl_pt)/10**fl_pt
                locs_storm_tile_3d_cur = np.append(each_pos,z_given)
                locs_storm_tile_3d = np.row_stack((locs_storm_tile_3d,locs_storm_tile_3d_cur))
            
            with open(num_locs_directory + str(tile_id) + '.data', 'wb') as filehandle:
                pickle.dump(locs_storm_tile_3d, filehandle)

            














         



        


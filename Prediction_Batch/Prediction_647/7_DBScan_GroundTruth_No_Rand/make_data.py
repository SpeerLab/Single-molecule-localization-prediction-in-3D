"""
Function to collect input and output data for the convolutional neural network model.

Swapnil 12/21
"""

"""
Simplified. This file call several functions to prepare input-output data for each tile.
All output is stored in "chenghang_list_tilesize_72_uint8_ROIs_from_shuffled\\" folder in the make_data folder. 
Output inlcude:
    .data of each image tile.
    .data of ground-truth localizations.
    .data of estimated localizations (with two methods). 

Chenghang 5/19/22
"""

import math
import pandas as pd
import os
import glob
import pickle
import random
import numpy as np
import sys

from make_data_per_image import make_data_per_image
import multiprocessing
from multiprocessing import Semaphore

if __name__ == "__main__":

    # Set path to training data files
    #expfolder = "X:\\Chenghang\\04_4_Color\\Exp_Group\\1.2.2021_P2EA_B_V2\\"
    expfolder = sys.argv[1]
    data_directory = expfolder + "ML_Result_647\\"

    tile_list_file = data_directory + "ROIs.csv"                

    clust_pix_list_full_file = data_directory + "pix_list_full.csv"
    

    # Set tile size for square shaped tile.  
    tile_size = 72
    
    # Set Maximum number of parallel processes.
    max_processes = 8        
    
    # Setup process queue.
    jobs = []
    sema = Semaphore(max_processes)      
    
    # Make a dataframe from csv file containing list of tile coordinates.
    df = pd.read_csv(tile_list_file)
    tiles_df = df

    
    # Create input and output files from tiles.
    print("Call Model_input_output")
    
    data_directory_str = "chenghang_list_" + "tilesize_" + str(tile_size) + "\\"

    # Create new directory for num_locs from tiles.
    if not os.path.exists(expfolder + "ML_Result_647\\" + data_directory_str):
        os.mkdir(expfolder + "ML_Result_647\\" + data_directory_str)

    if not os.path.exists(expfolder + "ML_Result_647\\" + data_directory_str + "num_locs_gtgt\\"):
        os.mkdir(expfolder + "ML_Result_647\\" + data_directory_str + "num_locs_gtgt\\")

    num_locs_directory = expfolder + "ML_Result_647\\" + data_directory_str + "num_locs_gtgt\\"  
    
    # Remove previously present files. 
    files = glob.glob(num_locs_directory + "*")
    for f in files:
        os.remove(f)          

    # Initialize tile count.
    tile_count = 0
    
    print("Reading full pix list")
    # Make a dataframe from list of pixel coordinates.
    clstr_pix_list_full_df = pd.read_csv(clust_pix_list_full_file) 

    # Create a new column for tuple of row and column coordinates.
    clstr_pix_list_full_df['row_col_tup'] = clstr_pix_list_full_df[['x(row)', 'y(column)']].apply(tuple, axis=1)
    
    # Iterate over individual image numbers.
    for img_num in tiles_df["z(Num_image)"].unique():
        # Create a dataframe for particular "Num_img" entry.
        img_df = tiles_df[tiles_df["z(Num_image)"]==img_num]
        locs_dict_directory = expfolder + "ML_Result_647\\" + "locs_dictionary_tilesize_" + str(tile_size) + "\\"
        locs_dict_file_name = locs_dict_directory + "locs_dict_img_" + str(img_num) + ".data"  
        
        sema.acquire()
        
        process = multiprocessing.Process(target = make_data_per_image, args=(img_df,clstr_pix_list_full_df,locs_dict_file_name,num_locs_directory,sema))
        
        jobs.append(process)
        process.start()
    for job in jobs:
        job.join()
    

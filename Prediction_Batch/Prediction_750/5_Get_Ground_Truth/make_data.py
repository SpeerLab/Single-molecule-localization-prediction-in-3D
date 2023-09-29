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
import multiprocessing

from model_input_output import modelInputOutput
from locs_per_tile_2 import locsPerTile2
#from locs_per_tile_2_tmp import locsPerTile2Tmp

if __name__ == "__main__":

    # Set path to training data files
    expfolder = "X:\\Chenghang\\4_Color\\Raw\\12.5.2020_P4ED_B_V2\\"
    data_directory = expfolder + "ML_result_750\\"

    tile_list_file = data_directory + "ROIs.csv"                

    clust_pix_list_full_file = data_directory + "pix_list_full.csv"
    
    # Set Maximum number of parallel processes.  
    max_processes = multiprocessing.cpu_count() - 4 

    # Set tile size for square shaped tile.  
    tile_size = 86                
    
    # Make a dataframe from csv file containing list of tile coordinates.
    df = pd.read_csv(tile_list_file)

    
    # Create input and output files from tiles.
    print("Call Model_input_output")
    total_loc_files = modelInputOutput(expfolder, tile_size, max_processes, df, locsPerTile2, clust_pix_list_full_file)
    
    # print("total number of training localization files created are {}\n" .format(total_loc_files))
    print("total number of testing localization files created are {}\n" .format(total_loc_files))
    

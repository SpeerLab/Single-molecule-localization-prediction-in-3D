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
from locs_per_tile_2_tmp import locsPerTile2Tmp

if __name__ == "__main__":

    # Are you analyzing uint8 data?
    uint8 = True
    
    # Are you collecting training data or test data?
    training = True

    # Set path to training data files
    expfolder = "X:\\Chenghang\\4_Color\\Raw\\12.21.2020_P8EA\\"
    data_directory = expfolder + "make_data\\"
    ML_directory = expfolder + "ML_result_647\\"
    
    # storm_exp_name = "561storm"
    storm_exp_name = "647storm"    
    # storm_exp_name = "750storm"  

    tile_list_file = data_directory + "647_ROIs_shuffled.csv"           
    
    # Specify ROI extension string for data directory.
    roi = "_ROIs_from_shuffled"                     

    clust_pix_list_directory = ML_directory + "Pix_txt\\"
    clust_pix_list_full_file = data_directory + "pix_list_full.csv"
    
    # Set Maximum number of parallel processes.
    # max_processes = 50    
    max_processes = multiprocessing.cpu_count() - 4 

    # Set scaling factor between raw image and stormtiff image.
    storm_image_scale = int(10)

    # Which channel do you want to analyze? Set experiment name.
    # channel = "561storm"
    channel = "647storm"    
    # channel = "750storm"

    # Set tile size for square shaped tile.  
    tile_size = 72                
    
    # Set percentage of total data used for training.
    training_data_pctg = 90
    
    # Make a dataframe from csv file containing list of tile coordinates.
    df = pd.read_csv(tile_list_file)
    
    # Get total number of tiles.
    tiles_num = len(df)
    
    # Get number of tiles for training out of all tiles.
    tiles_train_num = math.ceil(tiles_num*(training_data_pctg/100))
    
    # Create training and testing dataframes.
    # Splitting dataframe by row index.
    tiles_df = df.iloc[:tiles_train_num,:]
    
    # Create input and output files from tiles.
    total_tiles, total_loc_files = modelInputOutput(expfolder, storm_exp_name, channel, tile_size, max_processes, storm_image_scale, tiles_df, locsPerTile2, locsPerTile2Tmp, uint8, roi, clust_pix_list_full_file)
    # total_tiles = modelInputOutput(storm_exp_directory, storm_exp_name, channel, tile_size, max_processes, storm_image_scale, tiles_df, locsPerTile2, locsPerTile2Tmp, uint8)

    # print("total number of training tiles created are {}\n" .format(total_tiles))
    print("total number of testing tiles created are {}\n" .format(total_tiles))
    
    # print("total number of training localization files created are {}\n" .format(total_loc_files))
    print("total number of testing localization files created are {}\n" .format(total_loc_files))
    

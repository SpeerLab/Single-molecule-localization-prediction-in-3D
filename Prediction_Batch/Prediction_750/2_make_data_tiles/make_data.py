

import math
import sys
import pandas as pd
import multiprocessing

from model_input_output import modelInputOutput


if __name__ == "__main__":
    # Set path to training data files
    #expfolder = "X:\\Chenghang\\04_4_Color\\Exp_Group\\1.4.2021_P2EB_B_V2\\"
    expfolder = sys.argv[1]
    data_directory = expfolder + "ML_result_750\\"

    tile_list_file = data_directory + "ROIs.csv"


    # Set tile size for square shaped tile.  
    tile_size = 86                

    
    # Make a dataframe from csv file containing list of tile coordinates.
    df = pd.read_csv(tile_list_file)
    
    # Get total number of tiles.
    tiles_num = len(df)
    
    # Create input and output files from tiles.
    print("call model input output")
    total_tiles = modelInputOutput(data_directory, tile_size, df)

    # print("total number of training tiles created are {}\n" .format(total_tiles))
    print("total number of testing tiles created are {}\n" .format(total_tiles))
    

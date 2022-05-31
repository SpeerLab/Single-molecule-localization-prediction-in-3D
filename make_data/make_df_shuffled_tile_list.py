"""
This script creates a (randomly) shuffled version of original tile-list.

Swapnil 2/22
"""

"""
Simplified.
XXX_ROI.txt should be converted to csv after MATLAB processing. (Simplied change the file name)

CHenghang 5/18/22
"""

import pandas as pd

# Are you analyzing uint8 data?
uint8 = True

# Set path to training data files
expfolder = "X:\\Chenghang\\4_Color\\Raw\\12.21.2020_P8EA\\"
make_data_directory = expfolder + "make_data\\"
training_data_directory = make_data_directory + "stormtiffs_uint8\\"

# Which channel do you want to analyze? Set experiment name.
# channel = "561storm"
channel = "647storm"    
# channel = "750storm"

# Get the tile_list file.
if (channel == "561storm"): tile_list_file = expfolder + "ML_result_561\\ROI\\" + "561_ROIs.csv"

elif (channel == "647storm"): tile_list_file = expfolder + "ML_result_647\\ROI\\" + "647_ROIs.csv"

elif (channel == "750storm"): tile_list_file = expfolder + "ML_result_750\\ROI\\" + "750_ROIs.csv" 

# Make a dataframe from csv file containing list of tile coordinates.
df = pd.read_csv(tile_list_file)

# shuffle the DataFrame rows.
# df = df.sample(frac = 1).reset_index(inplace=True, drop=True)
df_shuffled = df.sample(frac = 1).reset_index(drop=True)

# Get the output file for the concatenated dataframe.
# df_out_file = storm_exp_directory + "tile_list\\" + "647_ROIs_to_csv_full_shuffled.csv" 
df_out_file = make_data_directory + "647_ROIs_shuffled.csv"
# df_out_file = storm_exp_directory + "tile_list\\" + "647_ROIs_to_csv_from_10k_shuffled.csv"  
# df_out_file = storm_exp_directory + "tile_list\\" + "750_ROIs_to_csv_full_shuffled.csv" 

# Write the concatenated dataframe to .csv file.
df_shuffled.to_csv(df_out_file)        
    

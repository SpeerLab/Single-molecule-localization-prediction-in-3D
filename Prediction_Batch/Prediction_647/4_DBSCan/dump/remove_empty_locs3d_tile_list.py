"""
This script removes empty tiles(zero intensity everywhere) and returns updated tile-list. 
'Sorted' option if chosen, sorts the updated tile-list according to image number.

Swapnil 2/22
"""

import pickle
import pandas as pd


# Set path to data files
expfolder = "X:\\Chenghang\\4_Color\\Raw\\12.21.2020_P8EA_B_V2\\"

# storm_exp_name = "561storm"
storm_exp_name = "ML_Result_750"    
# storm_exp_name = "750storm"

exp_name = "experiment_1"

storm_exp_directory = expfolder + storm_exp_name + "\\"

stormtiff_directory = storm_exp_directory

# Get the filename for tile-list.
tile_list_file = storm_exp_directory + "ROIs.csv"

# Get the filename for updated tile-list.
tile_list_file_updt = storm_exp_directory + "ROIs_to_csv_no_empty_tiles_no_empty_locs3d_" + exp_name + ".csv"


# Get the filename for empty locs3d tile.
tile_list_no_locs3d_file = storm_exp_directory + "tile_list_no_locs3d_" + exp_name + ".data"

# Read from the file. 
with open(tile_list_no_locs3d_file, 'rb') as filehandle:
    tile_list_no_locs3d = pickle.load(filehandle)

print("There are {} tiles with no locs3d predictions." .format(len(tile_list_no_locs3d)))    

# Set tile size for square shaped tile.
tile_size = 86

# Make a dataframe from csv file containing list of tile coordinates.
df = pd.read_csv(tile_list_file)

# Get total number of tiles
tiles_num = len(df)

# Initialize tile count.
tile_count = 0

# Iterate over all rows in the dataframe.
for idx in df.index:

    # Get the tile ID.
    tile_id = df.loc[idx, 'Tile_ID']

    # If the tile is empty
    if tile_id in tile_list_no_locs3d:            
        # Remove the row from the dataframe.
        df.drop(index=idx, inplace=True) 

    # Print analysis status.
    div = tiles_num//10
    # div = 1000
    
    if ((tile_id)%div==0):
        print("{}th tile is analyzed\n" .format(tile_id))         

# Save the updated dataframe to .csv file. 

df_sorted = df.sort_values(["z(Num_image)"], ascending=True)
df_sorted.to_csv(tile_list_file_updt, index=False)









   

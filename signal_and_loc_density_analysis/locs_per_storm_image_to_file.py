"""
Script to collect number of localizations in some selected ROIs of stormtiff image.
        
Swapnil 2/22
"""

"""
IMPORTANT: switch from h5.localizationsIterator to tracksIterator. From now on all processing should use tracks rather than indivisual localizations.
IMPORTANT: Before running, go the the ROI file and change [x(row),y(xolumn)] into [y(row),x(column)]

Chenghang 5/18/22
"""
import numpy as np
import storm_analysis.sa_library.sa_h5py as saH5Py
import pickle
import math
import os
from tifffile import tifffile
import pandas as pd

# Set path to data files.
expfolder = "X:\\Chenghang\\4_Color\\Raw\\12.21.2020_P8EA\\"
data_directory = expfolder + "make_data\\"
storm_exp_directory = expfolder + "acquisition\\bins\\"
image_directory = data_directory + "stormtiffs_uint8\\"

# Get molecule-list file.
h5_file = storm_exp_directory + "647storm_000_mlist.hdf5" 

# Get stormtiff images for corresponding .hdf5 file.
stormtiff_file = image_directory + "647storm_000_mlist.tiff"
stormtiff_image_array = tifffile.imread(stormtiff_file)    # type(stormtiff_image_array) = numpy.ndarray
print("stormtiff image {} is loaded for analysis\n" .format(os.path.basename(stormtiff_file)))
stormtiff_image_size = stormtiff_image_array.shape

# Set tile size for square shaped tile.
tile_size = 72

# Get tile-list file.
# tile_list_file = storm_exp_directory + "tile_list\\" + "561_ROIs_to_csv_8k.csv"
tile_list_file = data_directory + "647_ROIs_shuffled.csv"
# tile_list_file = storm_exp_directory + "750_ROIs_to_csv_img1_trunc.csv" 

# Make a dataframe from csv file containing list of tile coordinates.
df = pd.read_csv(tile_list_file)

# Set image number of of stormtiff image to be analyzed.
img_num = 1

# Create a dataframe for particular "Num_img" entry.
img_df = df[df["Num_image"]==img_num]


# Set scaling factor between raw image and stormtiff image.
storm_image_scale = int(10)

locs_dict_directory = data_directory + "locs_dictionary\\"
# create new directory for localization dictionary.
if not os.path.exists(locs_dict_directory):
    os.mkdir(locs_dict_directory)
    
# Create a dictionary filename.
locs_dict_file_name = locs_dict_directory + "locs_dict_img_" + str(img_num) + "_trunc.data"

# Initialize dictionary of localizations in storm image section
locs_storm = {}

# Iterate over all rows in dataframe for given image number.
for idx in img_df.index:

    # Get the tile coordinates.
    tile_start_pix_y = math.floor(img_df.loc[idx, 'y(row)'])
    tile_start_pix_x = math.floor(img_df.loc[idx, 'x(column)'])

    # To dictionary of localizations in storm image, add pixel ids as key 
    # and initialize a list for localizations in given pixel as value for the key.
    locs_storm["locs_"+str(tile_start_pix_y)+"_"+str(tile_start_pix_x)] = []

# To read localizations from given hdf5 file.
h5 = saH5Py.SAH5Py(h5_file)

# Note: Add fields for amplitude and sigma (or any other useful properties) later
# fields = ["x", "y", "xsigma", "ysigma"].
fields = ["x", "y"]

cnt = 0
for locs in h5.tracksIterator(fields = fields):
    cnt += 1
    print("Analyzing track group {}" .format(cnt))
        
    locs_copy = locs.copy()

    # Iterate over number of localizations in given frame.
    for k in range(len(locs_copy["x"])):
    
        # Get raw image coordinates of localization found.
        x_raw = locs_copy["x"][k]
        y_raw = locs_copy["y"][k]

        # Get storm image coordinates of localization found.            
        x_storm = x_raw*storm_image_scale
        y_storm = y_raw*storm_image_scale
        
        # Looping over keys to find tile for the localization. 
        for key in locs_storm.keys():
        
            # Get the tile coordinates.
            tile_start_pix_y = int(key.split("_")[1])
            tile_start_pix_x = int(key.split("_")[2])
            
            if(((y_storm<=tile_start_pix_y+tile_size-1) & (tile_start_pix_y<=y_storm)) & ((x_storm<=tile_start_pix_x+tile_size-1) & (tile_start_pix_x<=x_storm))):
        
                # Add the localization to dictionary of localizations in storm image section with
                # key specified by pixel id.
                locs_storm[key].append(np.array([y_storm, x_storm]))   

# Writting locs dictionary to file.
print("Writing localizations dictionary to file ...")
with open(locs_dict_file_name, 'wb') as filehandle:
    # store the data as binary data stream
    pickle.dump(locs_storm, filehandle)

                      

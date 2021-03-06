"""
This is a script to plot number of localizations vs the signal intensity for a 
particular tile or image section from segmented stormtiff image. 
It also fits the plot with different functions and saves the fit parameters.

Swapnil 2/22
"""

"""
Simplified.
Only use the first img. 
It works now. Can also switch to batch processing.

Chenghang 5.19.2022
"""

"""
Another version of the locs vs. intenstiy mapping. Mapping number of locs to the one pixel rather than nearest neighbors. 

Chenghang 5.24.2022
"""

import numpy as np
import math
import itertools
import pickle
import os
import pandas as pd
import matplotlib.pyplot as plt
from tifffile import tifffile

# Set path to data files
expfolder = "X:\\Chenghang\\4_Color\\Raw\\12.21.2020_P8EA\\"
data_directory = expfolder + "make_data\\"
storm_exp_name = "stormtiffs_uint8"
storm_exp_directory = data_directory + storm_exp_name + "\\"
hdf_directory = expfolder + "acquisition\\bin\\"

plots_directory = storm_exp_directory + "plots\\"  
# create new directory for plots.
if not os.path.exists(plots_directory):
    os.mkdir(plots_directory)

# Get molecule-list file.
h5_file = hdf_directory + "647storm_000_mlist.hdf5" 

# Get stormtiff images for corresponding .hdf5 file
stormtiff_file = storm_exp_directory + "647storm_000_mlist.tiff"
stormtiff_image_array = tifffile.imread(stormtiff_file)    # type(stormtiff_image_array) = numpy.ndarray
print("stormtiff image {} is loaded for analysis\n" .format(os.path.basename(stormtiff_file)))
stormtiff_image_size = stormtiff_image_array.shape

# Set tile size for square shaped tile.
tile_size = 72

# Set image number of of stormtiff image to be analyzed.
img_num = 1

# Get tile-list file.
# tile_list_file = storm_exp_directory + "tile_list\\" + "561_ROIs_to_csv_8k.csv"
tile_list_file = data_directory + "647_ROIs_shuffled.csv"
# tile_list_file = storm_exp_directory + "750_ROIs_to_csv_img1_trunc.csv" 

# Make a dataframe from csv file containing list of tile coordinates.
tile_list_df = pd.read_csv(tile_list_file)

# Create a dataframe for particular "Num_img" entry.
img_df = tile_list_df[tile_list_df["Num_image"]==img_num] 

# Get the cluster pix-list file.
clust_pix_list_full_file = data_directory + "pix_list_full.csv"

# Make a dataframe from .csv file containing list of pixel coordinates.
clstr_pix_list_full_df = pd.read_csv(clust_pix_list_full_file)

print("dataframe for full pixel list is created.")

# Subtract 1 from all pixel coordinates.
# This is because pixel coordinates in pixel list provided start from 1 while those in our analysis always start from 0.
clstr_pix_list_full_df[["x(row)","y(column)"]] = clstr_pix_list_full_df[["x(row)","y(column)"]].subtract(1)

# Create a new column for tuple of row and column coordinates.
clstr_pix_list_full_df['row_col_tup'] = clstr_pix_list_full_df[['x(row)', 'y(column)']].apply(tuple, axis=1)    

# Get localization dictionary from file.
locs_dict_directory = data_directory + "locs_dictionary\\"
locs_dict_file_name = locs_dict_directory + "locs_dict_img_{}_trunc.data" .format(img_num)                  

# Read from the file and save it to a dictionary.        
with open(locs_dict_file_name, 'rb') as filehandle:
    locs_storm = pickle.load(filehandle)    
    
# Initialize signal intensity and number of localizations lists.
sig_int = []
num_loc = []

# Initialize nn-average signal intensity and number of localizations lists.
sig_int_nn_avg = []
num_loc_nn_avg = []

num_loc_nn_avg_lin_fit_list = []
num_loc_nn_avg_quad_fit_list = []

# Iterate over all rows in dataframe for given image number.
for idx in img_df.index:

    # Get the tile coordinates.
    tile_start_pix_y = math.floor(img_df.loc[idx, 'y(row)'])
    tile_start_pix_x = math.floor(img_df.loc[idx, 'x(column)'])
    tile_id = math.floor(img_df.loc[idx, 'Tile_ID'])
    
    tile = stormtiff_image_array[tile_start_pix_y:tile_start_pix_y+tile_size,tile_start_pix_x:tile_start_pix_x+tile_size]

    print("Analyzing {}th tile." .format(tile_id))
    
    # Form a key from tile coordinates for given tile.
    key  =  "locs_"+str(tile_start_pix_y)+"_"+str(tile_start_pix_x)
    
    # From the localizations dictionary get list of localizations for given key.
    locs_storm_tile = locs_storm[key]

    # Make a dataframe of array of localizations.
    df = pd.DataFrame(locs_storm_tile, columns=["y","x"])    
    
    # Add new column to dataframe with floor values of "y" column. This new column denotes y-coordinate of pixels within which localization lies.
    df["y_floor"] = df["y"].apply(math.floor)
    df["x_floor"] = df["x"].apply(math.floor)    

    # From dataframe of full pixel list, create a dataframe of pixel-list coordinates that lie within given tile.
    cond1 = ((tile_start_pix_y+tile_size) >= clstr_pix_list_full_df["x(row)"]) & ((tile_start_pix_y) <= clstr_pix_list_full_df["x(row)"])
    cond2 = ((tile_start_pix_x+tile_size) >= clstr_pix_list_full_df["y(column)"]) & ((tile_start_pix_x) <= clstr_pix_list_full_df["y(column)"])
    cond3 = clstr_pix_list_full_df["Num_image"] == img_num 

    clstr_pix_list_df = clstr_pix_list_full_df[cond1 & cond2 & cond3]
    
    # Convert the tuple column to list.            
    clstr_pix_list = clstr_pix_list_df['row_col_tup'].tolist()
        
    # Iterate over pixels from selected tile of stormtiff image.
    for j, i in itertools.product(range(tile_start_pix_y, tile_start_pix_y+tile_size), range(tile_start_pix_x, tile_start_pix_x+tile_size)):
    
        sig_int.append(stormtiff_image_array[j,i])            
        
        # Make a tuple of tile pixel coordinates j and i.
        tup = (j,i)
        
        # If tile pixels are in pixel list then get number of localizations from locs-dictionary dataframe else set them to zero.
        if tup in clstr_pix_list:
            num_loc.append(len(df[(df["y_floor"] == tup[0]) & (df["x_floor"] == tup[1])]))
        else:
            num_loc.append(0)            

    #Test: keep pixels who have at least one localizaion
    sig_int_new = []
    num_loc_new = []
    for i,j in zip(sig_int,num_loc):
        if j > 0:
            sig_int_new.append(i)
            num_loc_new.append(j)
    sig_int_nn_avg = sig_int_new
    num_loc_nn_avg = num_loc_new


# Linear fit to nn-average data.
coef1 = np.polyfit(sig_int_nn_avg, num_loc_nn_avg, 1)
coef2 = np.polyfit(sig_int_nn_avg, num_loc_nn_avg, 2)
# coef1 = np.polyfit(sig_int, num_loc, 1)
# coef2 = np.polyfit(sig_int, num_loc, 2)

# Plot for nearest-neighbor averaged intensity vs localization with linear fit.
plt.plot(sig_int_nn_avg, num_loc_nn_avg, 'yo', sig_int_nn_avg, np.poly1d(coef1)(sig_int_nn_avg), '--k')
plt.ylabel("8nn average of # of localizations")
plt.xlabel("8nn average of signal intensity")
plt.title("img1_ROIs_trunc_8nn_average", pad=30.0)
file1_name = "img1_ROIs_trunc_8nn_average_lin_uint8"
# file1_name = "img1_ROIs_trunc_lin_uint8"
# file1_name = "img1_ROIs_trunc_8nn_average_lin"
plt.savefig(plots_directory + file1_name)
plt.show()

# # Plot for intensity vs localization with linear fit.
# plt.plot(sig_int, num_loc, 'yo', sig_int, np.poly1d(coef1)(sig_int), '--k')
# plt.ylabel("# of localizations")
# plt.xlabel("signal intensity")
# plt.title("img1_ROIs_trunc", pad=30.0)
# file1_name = "img1_ROIs_trunc_lin_uint8"
# # file1_name = "img1_ROIs_trunc_lin_uint8"
# # file1_name = "img1_ROIs_trunc_8nn_average_lin"
# plt.savefig(plots_directory + file1_name)
# plt.show()

# Plot for nearest-neighbor averaged intensity vs localization with quadratic fit.
plt.plot(sig_int_nn_avg, num_loc_nn_avg, 'yo', sig_int_nn_avg, np.poly1d(coef2)(sig_int_nn_avg), '--k')
# plt.plot(sig_int_nn_avg, num_loc, 'yo', sig_int_nn_avg, np.poly1d(coef2)(sig_int_nn_avg), '--k')
plt.ylabel("8nn average of # of localizations")
plt.xlabel("8nn average of signal intensity")
plt.title("img1_ROIs_trunc_8nn_average", pad=30.0)
file2_name = "img1_ROIs_trunc_8nn_average_quad_uint8" 
# file2_name = "img1_ROIs_trunc_8nn_average_quad" 
file_name = "img1_ROIs_trunc_8nn_average_2"
plt.savefig(plots_directory + file2_name)
plt.show()

# # Plot for intensity vs localization with quadratic fit.
# plt.plot(sig_int, num_loc, 'yo', sig_int_nn_avg, np.poly1d(coef2)(sig_int_nn_avg), '--k')
# # plt.plot(sig_int_nn_avg, num_loc, 'yo', sig_int_nn_avg, np.poly1d(coef2)(sig_int_nn_avg), '--k')
# plt.ylabel("# of localizations")
# plt.xlabel("signal intensity")
# plt.title("img1_ROIs_trunc", pad=30.0)
# file2_name = "img1_ROIs_trunc_quad_uint8" 
# # file2_name = "img1_ROIs_trunc_8nn_average_quad" 
# file_name = "img1_ROIs_trunc_8nn_average_2"
# plt.savefig(plots_directory + file2_name)
# plt.show()

# Save coefficients of the fit to file.
with open(plots_directory + "linear_fit_8nn_average_uint8.csv","a") as f_out:
    f_out.write("With linear fit for tiles in {} we have, # of localizations = {}*signal intensity + {},  \n" .format("750_ROIs_to_csv_img1_trunc.csv", coef1[0], coef1[1]))
    f_out.write("With quadratic fit for for tiles in {} we have, # of localizations = {}*signal intensity**2 + {}*signal intensity + {},  \n" .format("750_ROIs_to_csv_img1_trunc.csv", coef2[0], coef2[1], coef2[2]))  


#store_hist = np.zeros(256)
#for i,j in zip(sig_int_nn_avg,num_loc_nn_avg): 
#    store_hist[int(i)] += 1
    

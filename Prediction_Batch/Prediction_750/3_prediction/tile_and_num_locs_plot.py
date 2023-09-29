"""
Script to plot localizations found in tiles from given image section.

Swapnil 10/21
"""

"""
You might need line 51 to change experiment id. 
"""

import numpy as np
import glob
import pickle
import itertools
import sys
import matplotlib.pyplot as plt
import random

# Are you plotting localizations from molecule list or from neural network prediction?
mol_list = False

# Set path to training data files
# expfolder = "X:\\Chenghang\\04_4_Color\\Exp_Group\\1.2.2021_P2EA_B_V2\\"
expfolder = sys.argv[1]
data_directory = expfolder + "ML_Result_750\\"

# storm_exp_name = "561storm"
#storm_exp_name = "647storm"
storm_exp_name = "750storm"
                   

# Specify the tile-size of storm image section for training data.
tile_size = 86

experiment_directory = expfolder + "model_predictions\\"


data_directory_str = "chenghang_list_" + "tilesize_" + str(tile_size) + "\\"



if mol_list:
    num_locs_directory = data_directory + data_directory_str + "num_locs\\"
    # num_locs_directory = storm_exp_directory + data_directory_str + "num_locs_estimate\\"
    # num_locs_directory = storm_exp_directory + data_directory_str + "num_locs_estimate_no_nn_avg\\"
    tiles_directory = data_directory + data_directory_str + "tiles\\"
    
else:
    num_locs_directory = experiment_directory
    tiles_directory = data_directory + data_directory_str + "tiles\\"    

# Get number of tiles.
total_tiles = len(glob.glob(tiles_directory + "*.data"))
    
# Which tile localizations do you want to plot?
tile_id = sys.argv[2]

# Get the ith tile.
tile_file = tiles_directory + "tile_" + str(tile_id) + ".data"

# Read from .data files. 
with open(tile_file, 'rb') as filehandle:
    tile = pickle.load(filehandle)

# Get the files where the number of localizations for ith tile is stored.
if mol_list:    
    num_locs_tile_file_name = num_locs_directory + "storm_num_locs_tile_" + str(tile_id) + ".data" 
    
else:
    num_locs_tile_file_name = num_locs_directory + "tile_pred_num_locs_tile_" + str(tile_id) + ".data"

# Read the localizations from file for number of localizations for ith tile.      
with open(num_locs_tile_file_name, 'rb') as filehandle:
    num_locs_tile = pickle.load(filehandle)
    
print("length of num_locs is {}" .format(len(num_locs_tile)))    
    
# Initialize localizations list.
a = []

counter = 0      
    
for j, i in itertools.product(range(0, tile_size), range(0, tile_size)):
    
    if mol_list:
        num_locs = num_locs_tile[counter]
        
    else:
        num_locs = num_locs_tile[0, counter]

    # Choose number of floating points for random floats.
    fl_pt = 3

    # New version which assigns all localizations different random position within pixel.
    # Initialize localizations list for random positions within pixel. 
    num_loc_pred_pixel = []
    num_loc_est_pixel = []
    num_loc_pixel = []    

    # For every localization in given pixel.
    for num_loc in range(int(round(num_locs))):
        num_loc_pixel.append(np.array([random.randint((j)*10**fl_pt, (j+1)*10**fl_pt)/10**fl_pt, random.randint((i)*10**fl_pt, (i+1)*10**fl_pt)/10**fl_pt]))                    

    a.extend(num_loc_pixel)    

    counter += 1

# Convert list to numpy array.
a = np.array(a)     

print("length of locs_est is {}" .format(len(a)))
print("shape of locs_est is {}" .format(a.shape))             
    
# Plot ith tile.
plt.subplot(1, 2, 1)
plt.imshow(tile, cmap='gray')
plt.colorbar()
plt.gca().xaxis.tick_top()
# plt.legend(labels=['tile'])
# plt.title("tile_{}" .format(tile_num), pad=30.0)
plt.title("tile_{}" .format(tile_id), pad=30.0)
# plt.title("tile_{}" .format(i), y=1.08)
# plt.show()

# Choose colormap to denote different scatter points in different color.
cmap = np.arange(len(a))

# Plot predicted localizations from ith tile.
plt.subplot(1, 2, 2) 
plt.scatter(a[:,1], a[:,0], c='r', marker="o", s=1)

plt.xlim(0, 86)
plt.ylim(0, 86)
plt.gca().invert_yaxis()
plt.gca().xaxis.tick_top()
plt.gca().set_aspect('equal', adjustable='box')
# plt.ylabel("y")
# plt.xlabel("x")
# plt.legend(labels=['prediction'])
# plt.title("pred_tile_{}" .format(tile_num), pad=30.0)
plt.title("tile: {}, molecule list: {}" .format(tile_id, mol_list), pad=30.0)
# plt.title("pred_tile_{}" .format(i), y=1.08)

# To stop axis labels from overlapping with neighboring plot.
plt.tight_layout()

# file_name = "pred_train_tile_{}.jpg" .format(i)
# plt.savefig(locs_pred_directory + file_name)
plt.show()


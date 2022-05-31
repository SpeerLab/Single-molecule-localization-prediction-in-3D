"""
This is a script to plot (in the form of image) the predicted localizations for a 
particular tile. The localization is assigned a random position within a given pixel. 

Swapnil 11/21
"""

import numpy as np
import math
import pickle
import itertools
import matplotlib.pyplot as plt
import random

# Are you analyzing data with nearest neighbor averaging of pixel intensities for predicting localizations from fit?
nn_avg = True

# Do you want to save the plots?
save = False

# Set path to data files
expfolder = "analysis_path\\experiment_name\\"
# data_directory = expfolder + "make_data\\"

# storm_exp_name = "561storm"
# storm_exp_name = "647storm"
storm_exp_name = "750storm"

storm_exp_directory = expfolder + storm_exp_name + "\\"

experiment_directory = storm_exp_directory + "experiment1\\"

# Specify the tile-size of storm image section for training data.
tile_size = 86

# data_directory_str = "chenghang_list_" + "tilesize_" + str(tile_size) + "\\"
# data_directory_str = "chenghang_list_" + "tilesize_" + str(tile_size) + "_filtered_sorted\\"
data_directory_str = "chenghang_list_" + "tilesize_" + str(tile_size) + "_sorted\\"                    

tiles_directory = storm_exp_directory + data_directory_str + "tiles\\"

if nn_avg: num_locs_est_directory = storm_exp_directory + data_directory_str + "num_locs_estimate\\"
else: num_locs_est_directory = storm_exp_directory + data_directory_str + "num_locs_estimate_no_nn_avg\\"

locs_pred_directory = experiment_directory + "model_predictions\\"

tile_start = 44
# tile_start = 342878
tile_stop = 44

# Plot the predicted and original ith tile for visual comparison.
# for num in range(tile_start,tile_start+10):
for num in range(tile_start,tile_stop+1):

    tile_file = tiles_directory + "tile_" + str(num) + ".data"
    num_loc_est_file = num_locs_est_directory + "storm_num_locs_est_lin_fit_tile_" + str(num) + ".data"    
    num_loc_pred_file = locs_pred_directory + "tile_pred_num_locs_tile_" + str(num) + ".data"

    # Read from .data files. 
    with open(tile_file, 'rb') as filehandle:
        tile = pickle.load(filehandle)

    with open(num_loc_est_file, 'rb') as filehandle:
        num_locs_est_tile = pickle.load(filehandle)          
        
    with open(num_loc_pred_file, 'rb') as filehandle:
        num_locs_pred_tile = pickle.load(filehandle)
    
    # Initialize localizations lists.
    num_loc_pred_list = []
    num_loc_est_list = []

    counter = 0      
        
    for j, i in itertools.product(range(0, tile_size), range(0, tile_size)):

        # num_locs_pred_tile.append(len(df[(df["y_floor"] == j) & (df["x_floor"] == i)]))
        num_locs_pred = num_locs_pred_tile[0, counter]
        num_locs_est = num_locs_est_tile[counter]   
        
        # Choose number of floating points for random floats.
        fl_pt = 3

        # New version which assigns all localizations different random position within pixel.
        # Initialize localizations list for random positions within pixel. 
        num_loc_pred_pixel = []
        num_loc_est_pixel = []

        # For every predicted localization in given pixel.
        for num_loc_pred in range(round(num_locs_pred)):
            num_loc_pred_pixel.append(np.array([random.randint((j)*10**fl_pt, (j+1)*10**fl_pt)/10**fl_pt, random.randint((i)*10**fl_pt, (i+1)*10**fl_pt)/10**fl_pt]))

        # For every estimated localization in given pixel.
        for num_loc_est in range(round(num_locs_est)):
            num_loc_est_pixel.append(np.array([random.randint((j)*10**fl_pt, (j+1)*10**fl_pt)/10**fl_pt, random.randint((i)*10**fl_pt, (i+1)*10**fl_pt)/10**fl_pt]))           
        
        # Add the pixel list to final localizations list.
        num_loc_pred_list.extend(num_loc_pred_pixel)
        num_loc_est_list.extend(num_loc_est_pixel)                
        
        counter += 1

    # Convert list to numpy array.
    num_loc_pred_arr = np.array(num_loc_pred_list)
        
    num_loc_est_arr = np.array(num_loc_est_list)                 
    
    # Plot ith tile.
    plt.subplot(1, 3, 1)
    # plt.subplot(2, 2, 1)    
    plt.imshow(tile, cmap='gray')
    plt.gca().xaxis.tick_top()
    # plt.legend(labels=['tile'])
    plt.title("tile_{}" .format(num), pad=30.0)
    # plt.title("tile_{}" .format(i), y=1.08)

    # Plot predicted localizations from ith tile.
    plt.subplot(1, 3, 2)
    # plt.subplot(2, 2, 3)     
    # plt.scatter(loc[(loc[:,0]>0)&(loc[:,1]>0)][:,1], loc[(loc[:,0]>0)&(loc[:,1]>0)][:,0], c='r', marker=".", s=0.1)
    # plt.scatter(loc[(loc[:,0]>0)&(loc[:,1]>0)][:,1], loc[(loc[:,0]>0)&(loc[:,1]>0)][:,0], c='r', marker="o", s=1)
    
    # If present plot locs estimates.
    if (len(num_loc_est_arr) != 0 ):
        plt.scatter(num_loc_est_arr[:,1], num_loc_est_arr[:,0], c='r', marker="o", s=1)
    # Else plot nothing.
    else:
        pass
        # plt.scatter(c='r', marker="o", s=1)
    
    # plt.scatter(num_loc_est_arr[:,1], num_loc_est_arr[:,0], c='r', marker="o", s=1)        
    plt.xlim(0, tile_size)
    plt.ylim(0, tile_size)
    plt.gca().invert_yaxis()
    plt.gca().xaxis.tick_top()
    plt.gca().set_aspect('equal', adjustable='box')
    # plt.ylabel("y")
    # plt.xlabel("x")
    # plt.legend(labels=['prediction'])
    plt.title("tile_{}_sig_vs_loc_fit_estimation" .format(num), pad=30.0)
    # plt.title("pred_tile_{}" .format(i), y=1.08)        

    # Plot predicted localizations from ith tile.
    plt.subplot(1, 3, 3)
    # plt.subplot(2, 2, 4)     
    # plt.scatter(loc[(loc[:,0]>0)&(loc[:,1]>0)][:,1], loc[(loc[:,0]>0)&(loc[:,1]>0)][:,0], c='r', marker=".", s=0.1)
    # plt.scatter(loc[(loc[:,0]>0)&(loc[:,1]>0)][:,1], loc[(loc[:,0]>0)&(loc[:,1]>0)][:,0], c='r', marker="o", s=1)
    
    # If present plot locs.
    if (len(num_loc_pred_arr) !=0 ):
        plt.scatter(num_loc_pred_arr[:,1], num_loc_pred_arr[:,0], c='r', marker="o", s=1)
    # Else plot nothing.
    else:
        pass
        # plt.scatter(c='r', marker="o", s=1)
        
    # plt.scatter(num_loc_pred_arr[:,1], num_loc_pred_arr[:,0], c='r', marker="o", s=1)    
    plt.xlim(0, tile_size)
    plt.ylim(0, tile_size)
    plt.gca().invert_yaxis()
    plt.gca().xaxis.tick_top()
    plt.gca().set_aspect('equal', adjustable='box')
    # plt.ylabel("y")
    # plt.xlabel("x")
    # plt.legend(labels=['prediction'])
    plt.title("tile_{}_nn_prediction" .format(num), pad=30.0)
    # plt.title("pred_tile_{}" .format(i), y=1.08)

    # To stop axis labels from overlapping with neighboring plot.
    plt.tight_layout()

    file_name = "pred_test_tile_{}_random.jpg" .format(num)
    
    if save: 
        # plt.savefig(locs_pred_directory + file_name, dpi = 300)
        plt.savefig(locs_pred_directory + file_name)
        
    plt.show()
    
    # Individual plots for better visualization.
    plt.imshow(tile, cmap='gray')
    plt.gca().xaxis.tick_top()
    # plt.legend(labels=['tile'])
    plt.title("tile_{}" .format(num), pad=30.0)
    # plt.title("tile_{}" .format(i), y=1.08)
    file_name = "tile_{}_random.jpg" .format(num)
    
    if save: 
     plt.savefig(locs_pred_directory + file_name)
    
    plt.show()

    # If present plot locs.
    if (len(num_loc_est_arr) !=0 ):
        plt.scatter(num_loc_est_arr[:,1], num_loc_est_arr[:,0], c='r', marker="o", s=1)
    # Else plot nothing.
    else:
        pass
        # plt.scatter(c='r', marker="o", s=1)        
    # plt.scatter(num_loc_est_arr[:,1], num_loc_est_arr[:,0], c='r', marker="o", s=1)    
    plt.xlim(0, tile_size)
    plt.ylim(0, tile_size)
    plt.gca().invert_yaxis()
    plt.gca().xaxis.tick_top()
    plt.gca().set_aspect('equal', adjustable='box')
    # plt.ylabel("y")
    # plt.xlabel("x")
    # plt.legend(labels=['prediction'])
    plt.title("tile_{}_sig_vs_loc_fit_estimation" .format(num), pad=30.0)
    # plt.title("pred_tile_{}" .format(i), y=1.08)
    file_name = "tile_{}_sig_vs_loc_fit_estimation_random.jpg" .format(num)
    
    if save:
        plt.savefig(locs_pred_directory + file_name)
    
    plt.show()


    # If present plot locs.
    if (len(num_loc_pred_arr) !=0 ):
        plt.scatter(num_loc_pred_arr[:,1], num_loc_pred_arr[:,0], c='r', marker="o", s=1)
    # Else plot nothing.
    else:
        pass
        # plt.scatter(c='r', marker="o", s=1)        
    # plt.scatter(num_loc_pred_arr[:,1], num_loc_pred_arr[:,0], c='r', marker="o", s=1)    
    plt.xlim(0, tile_size)
    plt.ylim(0, tile_size)
    plt.gca().invert_yaxis()
    plt.gca().xaxis.tick_top()
    plt.gca().set_aspect('equal', adjustable='box')
    # plt.ylabel("y")
    # plt.xlabel("x")
    # plt.legend(labels=['prediction'])
    plt.title("tile_{}_nn_prediction" .format(num), pad=30.0)
    # plt.title("pred_tile_{}" .format(i), y=1.08)
    file_name = "tile_{}_nn_prediction_random.jpg" .format(num)
    
    if save: 
        plt.savefig(locs_pred_directory + file_name)
    
    plt.show()
    
    plt.subplot(1, 2, 1)     
    # plt.scatter(loc[(loc[:,0]>0)&(loc[:,1]>0)][:,1], loc[(loc[:,0]>0)&(loc[:,1]>0)][:,0], c='r', marker=".", s=0.1)
    # plt.scatter(loc[(loc[:,0]>0)&(loc[:,1]>0)][:,1], loc[(loc[:,0]>0)&(loc[:,1]>0)][:,0], c='r', marker="o", s=1)
    
    # If present plot locs.
    if (len(num_loc_est_arr) !=0 ):
        plt.scatter(num_loc_est_arr[:,1], num_loc_est_arr[:,0], c='r', marker="o", s=1)
    # Else plot nothing.
    else:
        pass
        # plt.scatter(c='r', marker="o", s=1)    
    
    #plt.scatter(num_loc_est_arr[:,1], num_loc_est_arr[:,0], c='r', marker="o", s=1)    
    plt.xlim(0, tile_size)
    plt.ylim(0, tile_size)
    plt.gca().invert_yaxis()
    plt.gca().xaxis.tick_top()
    plt.gca().set_aspect('equal', adjustable='box')
    # plt.ylabel("y")
    # plt.xlabel("x")
    # plt.legend(labels=['prediction'])
    plt.title("tile_{}_sig_vs_loc_fit_estimation" .format(num), pad=30.0)
    # plt.title("pred_tile_{}" .format(i), y=1.08)        

    plt.subplot(1, 2, 2)     
    # plt.scatter(loc[(loc[:,0]>0)&(loc[:,1]>0)][:,1], loc[(loc[:,0]>0)&(loc[:,1]>0)][:,0], c='r', marker=".", s=0.1)
    # plt.scatter(loc[(loc[:,0]>0)&(loc[:,1]>0)][:,1], loc[(loc[:,0]>0)&(loc[:,1]>0)][:,0], c='r', marker="o", s=1)
    
    # If present plot locs.
    if (len(num_loc_pred_arr) !=0 ):
        plt.scatter(num_loc_pred_arr[:,1], num_loc_pred_arr[:,0], c='r', marker="o", s=1)
    # Else plot nothing.
    else:
        pass
        # plt.scatter(c='r', marker="o", s=1)    
    
    # plt.scatter(num_loc_pred_arr[:,1], num_loc_pred_arr[:,0], c='r', marker="o", s=1)    
    plt.xlim(0, tile_size)
    plt.ylim(0, tile_size)
    plt.gca().invert_yaxis()
    plt.gca().xaxis.tick_top()
    plt.gca().set_aspect('equal', adjustable='box')
    # plt.ylabel("y")
    # plt.xlabel("x")
    # plt.legend(labels=['prediction'])
    plt.title("tile_{}_nn_prediction" .format(num), pad=30.0)
    # plt.title("pred_tile_{}" .format(i), y=1.08)

    # To stop axis labels from overlapping with neighboring plot.
    plt.tight_layout()

    file_name = "tile_{}_predictions_random.jpg" .format(num)
    
    if save: 
        # plt.savefig(locs_pred_directory + file_name, dpi = 300)
        plt.savefig(locs_pred_directory + file_name)    
    
    plt.show()    
    
    

    



        
        


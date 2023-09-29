"""
Function to create number of localization estimates from given tile of stormtiff image.
        
Swapnil 3/22
"""
import numpy as np
import pickle
import itertools
import multiprocessing
import math
from tifffile import tifffile
from scipy.stats import truncnorm 

def numLocsPerTile(tile_size, tile_id, coef1, coef2, stormtiff_file, locs_est_storm_lin_fit, locs_est_storm_quad_fit, num_locs_est_tile_lin_fit_file_name, num_locs_est_tile_quad_fit_file_name):
    
    # Process details.
    curr_process = multiprocessing.current_process()
    # parent_process = multiprocessing.parent_process()
    #print("Process Name : {} (Daemon : {}), Process Identifier : {}\n".format(curr_process.name, curr_process.daemon, curr_process.pid))    
    
    tile = tifffile.imread(stormtiff_file)        
    
    # Iterate over pixels from selected tile.
    for j, i in itertools.product(range(0, tile_size), range(0, tile_size)):
        
        # Begin nn-average computations.
        # Initialize signal intensity and nn-counter.
        sig = 0
        nn_counter = 0
        
        # Iterating over 8 nearest neighbors.
        for m, n in itertools.product(range(j-1, j+2), range(i-1, i+2)):

        # # Iterating over 24 nearest neighbors.
        # for m, n in itertools.product(range(j-2, j+3), range(i-2, i+3)):    

            if ((m, n) in itertools.product(range(0, tile_size), range(0, tile_size))):
                
                sig += tile[m,n]
                nn_counter += 1
        
        sig_nn_avg = (sig/nn_counter)
        
        # Assign zero signal intensity of zero localizations else use fit to estimate localizations.
        if (sig_nn_avg == 0):
            num_loc_nn_avg_lin_fit = 0
            #num_loc_nn_avg_quad_fit = 0

        else: 
            num_loc_nn_avg_lin_fit = np.poly1d(coef1)(sig_nn_avg)
            #num_loc_nn_avg_quad_fit = np.poly1d(coef2)(sig_nn_avg)   
        
        # Add the list to final dictionary of lists.
        locs_est_storm_lin_fit.append(math.ceil(num_loc_nn_avg_lin_fit))
        #locs_est_storm_quad_fit.append(math.ceil(num_loc_nn_avg_quad_fit))        
        
    # Convert list of localizations to array of localizations.
    locs_est_storm_lin_fit = np.array(locs_est_storm_lin_fit)
    locs_est_storm_quad_fit = np.array(locs_est_storm_quad_fit)               
        
    # Writting locs per tile to files. 
    with open(num_locs_est_tile_lin_fit_file_name, 'wb') as filehandle:
        # store the data as binary data stream
        pickle.dump(locs_est_storm_lin_fit, filehandle) 

    # Writting locs per tile to files.
    #with open(num_locs_est_tile_quad_fit_file_name, 'wb') as filehandle:
        # store the data as binary data stream
        #pickle.dump(locs_est_storm_quad_fit, filehandle)
        
    # `release` will add 1 to `sema`, allowing other 
    # processes blocked on it to continue.
    #sema.release()         

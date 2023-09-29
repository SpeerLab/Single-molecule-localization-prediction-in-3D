"""
Function to create list of localizations and localization estimates from given tile of stormtiff image.
        
Swapnil 12/21
"""
import numpy as np
import pickle
import itertools
import multiprocessing
import pandas as pd
import math

def locsPerTile2(tile_start_pix_y, tile_start_pix_x, tile_size, num_locs_file_name, locs_storm_tile, clstr_pix_list, sema):
    
    # Process details.
    curr_process = multiprocessing.current_process()
    # parent_process = multiprocessing.parent_process()
    print("Process Name : {} (Daemon : {}), Process Identifier : {}\n".format(curr_process.name, curr_process.daemon, curr_process.pid))    
    
    # Intitialize locations per tile in raw image coordinates and tile coordinates. 
    num_locs_tile = []     
    
    # Convert list of localizations from dictionary to array of localizations.
    locs_storm_tile = np.array(locs_storm_tile)    
    
    # Make a dataframe of array of localizations.
    df = pd.DataFrame(locs_storm_tile, columns=["y","x"])     
    
    # Add new column to dataframe with floor values of "y" column. This new column denotes y-coordinate of pixels within which localization lies.
    df["y_floor"] = df["y"].apply(math.floor)
    df["x_floor"] = df["x"].apply(math.floor)

    # Finding the actual and estimated number of localizations in every pixel of the tile.
    for j, i in itertools.product(range(tile_start_pix_y, tile_start_pix_y+tile_size), range(tile_start_pix_x, tile_start_pix_x+tile_size)):
    
        # Make a tuple of tile pixel coordinates j and i.
        tup = (j,i)
        
        # If tile pixels are in pixel list then get number of localizations from locs-dictionary dataframe else set them to zero.
        if tup in clstr_pix_list:
            num_locs_tile.append(len(df[(df["y_floor"] == tup[0]) & (df["x_floor"] == tup[1])]))
        else:
            num_locs_tile.append(0)        
          

    # Convert list to numpy array.
    num_locs_tile = np.array(num_locs_tile) 
           
    # Writting locs per tile to files for future use (See https://stackabuse.com/reading-and-writing-lists-to-a-file-in-python/ for pickle method)
    with open(num_locs_file_name, 'wb') as filehandle:
        # store the data as binary data stream
        pickle.dump(num_locs_tile, filehandle)

    # `release` will add 1 to `sema`, allowing other 
    # processes blocked on it to continue.
    sema.release()         

"""
Script to create parallel processes for making dictionary of localizations in specified image tiles of 
stormtiff image list.
        
Swapnil 2/22
"""
"""
Simplified.
Called function 'locs_per_storm_image.py' has been modified so it calls tracks rather than single localizations now.
"""

import os
import pandas as pd
# import matplotlib
# from matplotlib.offsetbox import AnchoredText
import multiprocessing

from locs_per_storm_image import locsPerStormImage
from multiprocessing import Semaphore

if __name__ == "__main__":

    # Set path to data files.
    expfolder = "X:\\Chenghang\\4_Color\\Raw\\12.21.2020_P8EA\\"
    data_directory = expfolder + "make_data\\"
    storm_exp_name = "647storm"
    
    molecule_lists_directory = expfolder + "acquisition\\bins\\"
    
    tile_list_file = data_directory + "647_ROIs_shuffled.csv"
    
    # Set tile size for square shaped tile. 
    tile_size = 72        

    # Specify ROI extension string for data directory.
    roi = "_ROIs"
    
    locs_dict_directory = data_directory + "locs_dictionary_tilesize_" + str(tile_size) + roi + "\\"
    # If does not exists, create a directory for localization dictionary.
    if not os.path.exists(locs_dict_directory):
        os.mkdir(locs_dict_directory)
        
    # Make a dataframe from csv file containing list of tile coordinates.
    df = pd.read_csv(tile_list_file)
    print("total tiles are {}" .format(len(df)))

    # Initialize maximum localizations per tile.
    max_locs_per_tile = 0

    # Set scaling factor between raw image and stormtiff image.
    storm_image_scale = int(10)
    
    # Set Maximum number of parallel processes.
    # max_processes = 50
    max_processes = multiprocessing.cpu_count() - 4    
    
    # Setup process queue.
    jobs = []
    # process_count = 0
    # results = multiprocessing.Queue()
    sema = Semaphore(max_processes)        
    
    # Iterate over individual image numbers in dataframe.
    for img_num in df["Num_image"].unique():
        print("processing " + str(img_num) + " th images")
        # Create a dataframe for particular "Num_img" entry.
        img_df = df[df["Num_image"]==img_num]

        # Get molecule list file for given image number.        
        if ((img_num-1)//10 == 0): h5_file = molecule_lists_directory + storm_exp_name + "_00" + str(img_num-1) + "_mlist" + ".hdf5"
        elif (((img_num-1)//10)//10 == 0): h5_file = molecule_lists_directory + storm_exp_name + "_0" + str(img_num-1) + "_mlist" + ".hdf5"
        elif ((((img_num-1)//10)//10)//10 == 0): h5_file = molecule_lists_directory + storm_exp_name + "_" + str(img_num-1) + "_mlist" + ".hdf5"
        
        # Create a dictionary filename.
        locs_dict_file_name = locs_dict_directory + "locs_dict_img_" + str(img_num) + ".data"        

        sema.acquire()
        
        # Assign process for each tile.
        process = multiprocessing.Process(target = locsPerStormImage, args=(h5_file, tile_size, storm_image_scale, img_df, locs_dict_file_name, sema))
        jobs.append(process)
        process.start()
        
    # Block the execution of next lines in the main script until all the process are terminated.     
    for job in jobs:
        
        job.join()        

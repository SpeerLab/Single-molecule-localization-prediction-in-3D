"""
This is a script for non-linear transformation of pixel intensities (soft-saturation) in raw stormtiff image.
 
Swapnil 4/22
"""

import numpy as np
import glob
import os
from tifffile import tifffile
import cv2

# Set the image channel:
channel = "647"

# Set path to training data files (stormtiffs)
expfolder = "X:\\Chenghang\\4_Color\\Raw\\12.21.2020_P8EA\\"
makedata_directory = expfolder + "Make_data\\"
stormtiff_directory = expfolder + "stormtiffs\\"

# Create new directory for transformed images.
if not os.path.exists(expfolder + "stormtiffs_transformed\\"):
    os.mkdir(expfolder + "stormtiffs_transformed\\")
    
stormtiff_transformed_directory = expfolder + "stormtiffs_transformed\\"   

# Create new directory for transformed images.
if not os.path.exists(expfolder + "stormtiffs_transformed_blurred\\"):
    os.mkdir(expfolder + "stormtiffs_transformed_blurred\\")
    
stormtiff_transformed_blurred_directory = expfolder + "stormtiffs_transformed_blurred\\"         
    

# Set transformation parameters.
# This parameter is chosen such that the pixel intensity distribution (as seen in fiji) for transformed and blurred uint8 images 
# looks very similar to aligned uint8 images.
c = 0.38    

# The maximum intensity for raw stormtiff images is found out from 'max_sig_test_storm_image_list.py'
# Note: Use the mean value might make more sense, since the example value (1142) is actually an outlier. 
max_sig = 1142.524658203125

counter = 0
 
# Get image files. 
files = glob.glob(stormtiff_directory + channel +"*.tiff")

for file in files:
    # Get image tile.
    tile = tifffile.imread(file)    # type(stormtiff_image_array) = numpy.ndarray
    
    # Get the transformed tile.
    # Converting to 32-bit float format to be able to read by ImageJ.
    tile = (max_sig/np.tanh(c*max_sig))*np.tanh(c*tile).astype(np.float32)
    
    # Get the filename.
    # Note that raw data tiles are in .tif format (integer-valued intensity) and transformed files to be saved in .tiff format (float-valued intensity).
    # filename = stormtiff_transformed_directory + os.path.basename(file)[:-4] + ".tiff"
    filename = stormtiff_transformed_directory + os.path.basename(file)    
    
    # Save the transformed tile.
    tifffile.imsave(filename, tile)    
    # tifffile.imsave(filename, tile, frames.astype(np.uint16))
    
    # Apply guassian blur on image tile.
    tile = cv2.GaussianBlur(tile, ksize=[0,0], sigmaX=0.6, sigmaY=0.6, borderType=cv2.BORDER_DEFAULT)

    # Get the filename.
    # Note that raw data tiles are in .tif format (integer-valued intensity) and transformed files to be saved in .tiff format (float-valued intensity).
    # filename = stormtiff_transformed_blurred_directory + os.path.basename(file)[:-4] + ".tiff"
    filename = stormtiff_transformed_blurred_directory + os.path.basename(file)        
    
    # Save the transformed tile.
    tifffile.imsave(filename, tile)    
    # tifffile.imsave(filename, tile, frames.astype(np.uint16))    

    counter += 1
        
    if counter%10 == 0:
        print("{}th tile is transformed." .format(counter))        
    

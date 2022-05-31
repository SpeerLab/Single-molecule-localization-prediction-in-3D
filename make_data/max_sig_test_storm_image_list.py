"""
This is a test script to compute maximum pixel intensity signal for list of stormtiff images.  

Swapnil 1/22
"""
"""
Simplified, get max pixel intensity of all images and print it out.

Chenghang 5.16.22
"""

import numpy as np
import glob
import os
from tifffile import tifffile

# Set path to data files
expfolder = "X:\\Chenghang\\4_Color\\Raw\\12.21.2020_P8EA\\"
stormtiffs_directory = expfolder + "stormtiffs\\"

#storm_exp_name = "561storm"
storm_exp_name = "647storm"    
# storm_exp_name = "750storm"     

# Get all the images present in stormtiff folder. 
img_files = glob.glob(stormtiffs_directory + storm_exp_name + "*")

# Initialize maximum intensity.
max_int = 0

# Iterate over individual image files.
for img_file in img_files:

    # Load the image in the form of an array.
    stormtiff_image_array = tifffile.imread(img_file)    # type(stormtiff_image_array) = numpy.ndarray
    
    max_int_img = np.amax(stormtiff_image_array)
    print(max_int_img)

    if (max_int_img > max_int):
        max_int = max_int_img

print("Done! ")
print(max_int)

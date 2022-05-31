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
import storm_analysis.sa_library.sa_h5py as saH5Py

# Set path to data files
expfolder = "X:\\Chenghang\\4_Color\\Raw\\12.21.2020_P8EA\\"
data_directory = expfolder + "make_data\\"
storm_exp_name = "stormtiffs_uint8"
storm_exp_directory = data_directory + storm_exp_name + "\\"
hdf_directory = expfolder + "acquisition\\bins\\"

plots_directory = storm_exp_directory + "plots\\"  
# create new directory for plots.
if not os.path.exists(plots_directory):
    os.mkdir(plots_directory)

# Get molecule-list file.
h5_file = hdf_directory + "647storm_000_mlist.hdf5" 

# Get stormtiff images for corresponding .hdf5 file
stormtiff_file = storm_exp_directory + "647storm_000_mlist.tiff"
stormtiff_image_array = tifffile.imread(stormtiff_file)    # type(stormtiff_image_array) = numpy.ndarray
stormtiff_image_array = stormtiff_image_array/255.0
print("stormtiff image {} is loaded for analysis\n" .format(os.path.basename(stormtiff_file)))
stormtiff_image_size = stormtiff_image_array.shape

img_num = 1
storm_image_scale = 10

#Get all tracks in the current image. 
h5 = saH5Py.SAH5Py(h5_file)
fields = ["x", "y"]
num_locs_array = np.zeros((6400,6400),'int')
cnt = 0
for locs in h5.tracksIterator(fields = fields):
    cnt += 1
    print("Analyzing track group {}" .format(cnt))
    locs_copy = locs.copy()
    array_x = locs_copy["x"]
    array_y = locs_copy["y"]
    array_x *= 10
    array_y *= 10
    for i in range(len(array_x)):
        if (array_x[i]<6400) & (array_y[i]<6400):
            #IMPORTANT: x and y in the h5 file is reversed. (x for column)
            num_locs_array[int(array_y[i]),int(array_x[i])] += 1

num_locs = []
sig_int = []
for i in range(6400):
    if i%100 == 0:
        print("Processing row #{}".format(i))
    for j in range(6400):
        if (i>3000) & (i<5000) & (j>3000) & (j<5000):
            if stormtiff_image_array[i,j] > 0:
                #sigma = 0.5
                #P(center pixal) = 0.4725
                #P(4 connected pixels) = 0.1066 (each)
                #P(3 corner pixels) = 0.024(each)
                #Psum = 0.9949
                #nn_ave = 0
                #nn_ave = 0.4725 * stormtiff_image_array[i,j]
                nn_ave = stormtiff_image_array[i,j]
                #nn_ave += 0.1066 * (stormtiff_image_array[i-1,j] + stormtiff_image_array[i+1,j] + stormtiff_image_array[i,j-1] + stormtiff_image_array[i,j+1])
                #nn_ave += 0.024 * (stormtiff_image_array[i-1,j-1] + stormtiff_image_array[i-1,j+1] + stormtiff_image_array[i+1,j-1] + stormtiff_image_array[i+1,j+1])
                #nn_ave /= 0.9949
                sig_int.append(nn_ave)
                num_locs.append(num_locs_array[i,j])
plt.scatter(sig_int,num_locs,s=1)
plt.show()

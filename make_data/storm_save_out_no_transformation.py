"""
This fiji macro is based on macro 'storm_save_out.py'. It converts Stormtiff image from 'single' data 
format to 'unit16' (maximum intensity 65535) data format or 'unit8' (maximum intensity 255) data format without applying any alignment transformations.

Swapnil 1/22
"""
"""
Simplified. 

Chenghang 5/18/22
"""
import os,sys
import glob
import shutil
from ij import IJ  
from ij.process import ImageStatistics as IS
from ij import Prefs
import time

# get experiment folder from python
expfolder = "X:\\Chenghang\\4_Color\\Raw\\12.21.2020_P8EA\\"
make_data_directory = expfolder + "make_data\\"
# set paths
storm_exp_directory = make_data_directory + "stormtiffs_transformed" + "\\"
# storm_exp_directory = testing_data_directory + storm_exp_name + "\\"    
stormtiffs_directory = storm_exp_directory

stormtiffs_directory_uint8 = make_data_directory + "stormtiffs_uint8\\"
# If does not exists, create new directory for uint8 stormtiff images.
if not os.path.exists(stormtiffs_directory_uint8):
    os.mkdir(stormtiffs_directory_uint8)
    

# Get all the images present in stormtiff folder. 
img_files = glob.glob(stormtiffs_directory + "*")

# Iterate over individual image files.
for img_file in img_files:

    # Get image file name.
    img_filename = os.path.basename(img_file)

    print(img_filename)

    imp = IJ.openImage((img_file))
    IJ.run(imp, "16-bit", "")
    imp.show()
    # IJ.run("Enhance Contrast", "saturated=0.3")
    IJ.run("Enhance Contrast", "saturated=0.0")    
    IJ.run("Apply LUT")
    # IJ.run(imp, "16-bit", "")
    IJ.run(imp, "8-bit", "")    
    IJ.saveAs(imp, "Tiff", (stormtiffs_directory_uint8 + img_filename))
    imp.close();
    
IJ.run("Close All", "");

import os,sys
import glob
import shutil
from ij import IJ  
from ij.process import ImageStatistics as IS
from ij import Prefs
import time


# get experiment folder from python
#expfolder = getArgument()
expfolder = "X:\\Chenghang\\4_Color\\Raw\\12.21.2020_P8EA\\"
# set paths
storm_folder = expfolder + "stormtiffs\\"
print storm_folder
out_folder = expfolder + "stormtiffs_fake\\"
slicenum = len(glob.glob(storm_folder + "750*"))
print slicenum

channels = ["647storm_"]


for i in range(slicenum):
    for channel in channels:
        base = str(channel)
        imp = IJ.openImage((storm_folder + base + "%03d" % i + "_mlist.tiff"))
        IJ.run(imp, "16-bit", "")
        imp.show()
        IJ.run("Enhance Contrast", "saturated=0.01")
        IJ.run("Apply LUT")
        IJ.run(imp, "16-bit", "")
        IJ.saveAs(imp, "Tiff", (out_folder + base + "%03d" % i + ".tiff"))
        imp.close();
        IJ.run("Close All", "");

IJ.run("Quit");

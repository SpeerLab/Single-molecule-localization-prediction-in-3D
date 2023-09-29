"""
This script creates a single pixel list of all the pixels from the clusters (connected components) in 
given set of image tiles.  

Swapnil 2/22
"""

import glob
import pandas as pd
import sys
     

# Set path to data files.
#expfolder = "X:\\Chenghang\\04_4_Color\\Exp_Group\\1.4.2021_P2EB_B_V2\\"
expfolder = sys.argv[1]
data_directory = expfolder + "ML_result_750\\"

# Get path to the cluster pixel_list directory.
clust_pix_list_directory = data_directory + "Pix_list\\"

# Initialize dataframe list.
df_list = []

# Get all the cluster pixel-list files. 
files = glob.glob(clust_pix_list_directory + "*")

for file in files:
    clstr_pix_list_df = pd.read_csv(file)
    df_list.append(clstr_pix_list_df)    

# Create a concatenated dataframe from dataframe list. 
df = pd.concat(df_list, ignore_index=True)

# Get the output file for the concatenated dataframe and save to a csv file.
df_out_file = data_directory + "pix_list_full.csv"
df.to_csv(df_out_file)        
    

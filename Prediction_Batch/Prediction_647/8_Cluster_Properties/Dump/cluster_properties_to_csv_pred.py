"""
Script to write clusters properties to csv file.

Swapnil 2/22
"""

import glob
import pickle
import pandas as pd

expfolder = "X:\\Chenghang\\4_Color\\Raw\\1.11.2021_B2P8C_B_V2\\ML_result_750_neg\\"

# Get dbscan parameters.
eps = 20
min_samples = 6

clst_sz_fltr = 1

# If does not exist, create new directory for cluster stats from 3d localization sequences.
cl_stats_directory = expfolder + "cluster_stats_sequences_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\"

    
# Get number of 3d localization sequences present in cluster_stats directory.
total_seqs = len(glob.glob(cl_stats_directory + "*.data"))

files = glob.glob(cl_stats_directory + "*.data")         

# Iterate over sequences.
for file in files:    

    # Get the filename for cluster stats from given 3d localization sequence.
    cl_stats_file_name = file
    
    # Read from the file. 
    with open(cl_stats_file_name, 'rb') as filehandle:
        cl_stats = pickle.load(filehandle)

    # Get the sequence number present in the filename.
    seq = int(cl_stats_file_name.split("_")[-1][:-5])           

    # Get tupple of dictionaries (with unique cluster labels as key) for different cluster stats.
    dicts = cl_stats[2]             
    
    # Get dictionary for cluster centers.
    cl_cntr_dict = dicts[0]  

    # Get dictionary for cluster sizes.
    cl_sz_dict = dicts[1]

    # Get dictionary for cluster areas.
    cl_ar_dict = dicts[2] 

    # Get dictionary for cluster volumes.
    cl_vl_dict = dicts[3]
    
    # Initialize subcluster counter.
    sbclst_count  = 0
    
    # Create a dataframe with given column names.
    column_names = ["sub-cluster ID", "size", "center x", "center y", "center z", "area", "volume"]
    df = pd.DataFrame(columns = column_names)

    # Initialize dataframe row-number.
    row_num  = 0
    
    # Iterate over all values in dictionary.
    for key in cl_sz_dict.keys():
        if (cl_sz_dict[key] > clst_sz_fltr):
                
            # Increment subcluster counter.
            sbclst_count  += 1
            
            # Get subcluster size.
            cl_sz = cl_sz_dict[key]            

            # Get subcluster center coordinates.
            cl_cntr_x = cl_cntr_dict[key][0]
            cl_cntr_y = cl_cntr_dict[key][1]            
            cl_cntr_z = cl_cntr_dict[key][2]                            

            # Get subcluster area.
            cl_ar = cl_ar_dict[key]            

            # Get subcluster volume.
            cl_vl = cl_vl_dict[key]

            # append rows to the DataFrame.
            df = df.append({"sub-cluster ID" : sbclst_count, "size" : cl_sz, "center x" : cl_cntr_x, "center y" : cl_cntr_y, "center z" : cl_cntr_z, "area" : cl_ar, "volume" : cl_vl}, 
                ignore_index = True)

            row_num += 1
    
    # Set the csv filename for cluster stats from given 3d localization sequence.
    cl_stats_csv_file_name = cl_stats_directory + "cluster_stats_to_csv_sequence_" + str(seq) + ".csv"

    # Write the dataframe to .csv file.
    df.to_csv(cl_stats_csv_file_name)          
        
    if (seq%100 == 0):
        print("{}th sequence is analyzed." .format(seq))                         
            

            
    

    



        
        

